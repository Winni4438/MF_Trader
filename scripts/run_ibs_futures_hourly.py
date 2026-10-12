"""Umsetzbarkeitstest für den IBS-Dip-Kauf mit Index-Futures auf Stundendaten (2019–2026).

Kassasitzung je Index (Ortszeit): High/Low/Close aus den Stundenkerzen der Sitzung. Einstieg in der Stunde
nach Kassaschluss (Futures handeln weiter), Ausstieg nach Kassaschluss eines Folgetags, sobald IBS > 0,5,
spätestens nach 2 Sitzungen. Kosten: Futures-Kosten aus dem Universum inkl. Stressaufschlag.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mf_trader import backtest as bt, flow  # noqa: E402
from mf_trader.data.panel import load_hourly  # noqa: E402

OUT = ROOT / "results" / "ibs_futures_hourly"
OUT.mkdir(parents=True, exist_ok=True)
P = load_hourly("hourly_mr")
ret, mask, close = P["ret"], P["mask"], P["close"]
hi_h = P["close"].copy()  # Platzhalter (Stundenkerzen-High/Low sind im Panel nicht gespeichert)
vol = flow.realized_daily_vol(ret)
stress = bt.stress_multiplier(ret)

# Kassasitzungen: (Zeitzone, erste Stunde, letzte Stunde [Bar-Beginn]); Close = Ende der letzten Stunde
SESS = {"SPX": ("America/New_York", 10, 15), "NDX": ("America/New_York", 10, 15), "RUT": ("America/New_York", 10, 15),
        "DAX": ("Europe/Berlin", 9, 17), "CAC": ("Europe/Paris", 9, 17), "FTSE": ("Europe/London", 8, 16),
        "NKY": ("Asia/Tokyo", 9, 14), "ASX": ("Australia/Sydney", 10, 15), "HSI": ("Asia/Hong_Kong", 10, 15)}
rows, curves = [], {}
W_all = pd.DataFrame(0.0, index=ret.index, columns=[k for k in SESS if k in ret])
for k, (tz, h0, h1) in SESS.items():
    if k not in ret:
        continue
    loc = ret.index.tz_convert(tz)
    in_sess = (loc.hour >= h0) & (loc.hour <= h1) & (loc.dayofweek < 5) & mask[k].values
    day = pd.Series(loc.normalize().tz_localize(None), index=ret.index)
    c = close[k]
    sess_close = c[in_sess].groupby(day[in_sess]).last()
    sess_hi = c[in_sess].groupby(day[in_sess]).max()
    sess_lo = c[in_sess].groupby(day[in_sess]).min()
    # Approximation: High/Low aus stündlichen Schlusskursen + Eröffnung der ersten Stunde
    ibs = (sess_close - sess_lo) / (sess_hi - sess_lo).replace(0, np.nan)
    last_bar = pd.Series(in_sess, index=ret.index) & (pd.Series(loc.hour, index=ret.index) == h1)
    # Zielposition nach jedem Sitzungsschluss
    pos = 0
    held = 0
    target = pd.Series(0.0, index=ret.index)
    cur = 0.0
    for t in np.flatnonzero(last_bar.values):
        d = day.iloc[t]
        x = ibs.get(d, np.nan)
        if pos:
            held += 1
            if (np.isfinite(x) and x > 0.5) or held >= 2:
                pos, held = 0, 0
        if not pos and np.isfinite(x) and x < 0.2:
            pos, held = 1, 0
        cur = pos * 0.10 / vol[k].iloc[t] if pos else 0.0
        target.iloc[t:] = cur   # gilt ab dem nächsten Bar (Ausführung nach Kassaschluss)
    W = target.to_frame(k).fillna(0.0)
    W_all[k] = W[k]
    res = bt.run(W, P, stress=stress).loc["2019-07-01":]
    m = bt.metrics(res)
    rows.append({"Index": k, "Sharpe_netto": m["Sharpe"], "Sharpe_brutto": bt.metrics(res, "gross")["Sharpe"],
                 "Sharpe_bis2022": bt.metrics(res.loc[:"2022-12-31"])["Sharpe"], "Sharpe_ab2023": bt.metrics(res.loc["2023-01-01":])["Sharpe"],
                 "Trades": m["Trades"], "Zeit_im_Markt": m["TimeInMarket"]})
res = bt.run(W_all, P, stress=stress).loc["2019-07-01":]
m = bt.metrics(res)
rows.append({"Index": "Korb (alle)", "Sharpe_netto": m["Sharpe"], "Sharpe_brutto": bt.metrics(res, "gross")["Sharpe"],
             "Sharpe_bis2022": bt.metrics(res.loc[:"2022-12-31"])["Sharpe"], "Sharpe_ab2023": bt.metrics(res.loc["2023-01-01":])["Sharpe"],
             "Trades": m["Trades"], "Zeit_im_Markt": m["TimeInMarket"]})
# Referenz: Buy & Hold desselben Korbs (risikogleich, dauerhaft investiert)
Wbh = pd.DataFrame({k: 0.10 / vol[k] for k in W_all.columns}).fillna(0.0) / len(W_all.columns) * 3
rb = bt.run(Wbh, P, stress=stress).loc["2019-07-01":]
rows.append({"Index": "Buy & Hold Korb", "Sharpe_netto": bt.metrics(rb)["Sharpe"], "Sharpe_bis2022": bt.metrics(rb.loc[:"2022-12-31"])["Sharpe"],
             "Sharpe_ab2023": bt.metrics(rb.loc["2023-01-01":])["Sharpe"]})
df = pd.DataFrame(rows)
df.to_csv(OUT / "ibs_futures_hourly.csv", index=False)
pd.DataFrame({"IBS-Dip-Kauf Index-Futures (netto)": bt.daily(res).cumsum(), "brutto": bt.daily(res, "gross").cumsum()}).to_csv(OUT / "curve.csv")
print(df.round(2).to_string())
