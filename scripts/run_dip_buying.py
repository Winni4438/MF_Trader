"""Dip-Kauf in Aktienindizes (nur long, Haltedauer ≤ 2 Tage) – die in der Literatur am besten belegte
Überverkauft-Nische. Tagesdaten 2007–2026 (ETFs als Proxy für Index-Futures), mit Trend- und VIX-Filter.
Ergebnisse -> results/dip_buying/
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mf_trader.meanrev import hysteresis  # noqa: E402

OUT = ROOT / "results" / "dip_buying"
OUT.mkdir(parents=True, exist_ok=True)
src = (ROOT / "scripts" / "run_meanrev_daily.py").read_text(encoding="utf-8")
head = src.split("# ---------------------------------------------------------------- Indikatoren")[0]
ns = {"__file__": str(ROOT / "scripts" / "run_meanrev_daily.py")}
exec(compile(head, "daily_head", "exec"), ns)
C, Hi, Lo, mask, ret, cost, vol, cc, gap, intra = (ns[k] for k in ["C", "Hi", "Lo", "mask", "ret", "cost", "vol", "cc", "gap", "intra"])

EQ = ["SPY", "QQQ", "IWM", "EFA", "VGK", "EWJ", "EEM", "EWG", "EWU", "EWA", "EWC", "EWY", "EWZ", "FXI", "EWW"]
EQ = [k for k in EQ if k in C]
RAW = ROOT / "data" / "raw"
vix = pd.read_parquet(RAW / "yahoo" / "IDX_VIX_d1.parquet")["close"]
vix.index = vix.index.tz_convert("America/New_York").normalize().tz_localize(None)
vix = vix[~vix.index.duplicated()].reindex(C.index).ffill()
vix_hi = (vix > vix.rolling(250, min_periods=60).median())


def rsi(n):
    d = C.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


sig_d = ret.rolling(60, min_periods=30).std().shift(1)
SIG = {
    "RSI(2) < 10": (50 - rsi(2)) / 40,                       # >1 heißt RSI2 < 10
    "IBS < 0,2": (0.5 - (C - Lo) / (Hi - Lo).replace(0, np.nan)) / 0.3,
    "Tagesrendite < −2σ": -(ret / sig_d) / 2.0,
    "3-Tage-Rendite < −2σ": -(ret.rolling(3).sum() / (sig_d * np.sqrt(3))) / 2.0,
}
trend = C > C.rolling(200, min_periods=120).mean()


def run(W, execution):
    W = W.fillna(0.0)
    pnl = (W.shift(1) * cc).sum(axis=1) if execution == "close" else (W.shift(2) * gap).sum(axis=1) + (W.shift(1) * intra).sum(axis=1)
    return pnl, pnl - (W.diff().abs() * cost / 1e4).sum(axis=1)


def stats_(x):
    x = x.loc["2007-06-01":]
    x = x[x.ne(0).idxmax():]
    eq = (1 + x).cumprod()
    return {"Sharpe": x.mean() / x.std() * np.sqrt(252), "MaxDD": (eq / eq.cummax() - 1).min(),
            "Sharpe_bis2016": x.loc[:"2016-12-31"].mean() / x.loc[:"2016-12-31"].std() * np.sqrt(252),
            "Sharpe_ab2017": x.loc["2017-01-01":].mean() / x.loc["2017-01-01":].std() * np.sqrt(252)}


rows, curves = [], {}
for name, S in SIG.items():
    for filt, exe, H in itertools.product(["kein Filter", "Trend (über 200-Tage-Linie)", "VIX über Median", "Trend + VIX"], ["close", "open"], [1, 2]):
        ok = mask.copy()
        if "Trend" in filt:
            ok &= trend
        if "VIX" in filt:
            ok &= vix_hi.values[:, None]
        # Konvention der Zustandsmaschine: Signal < -1 -> long. Überverkauft (S > 1) daher als -S übergeben,
        # Short-Einstiege durch Kappung bei +0.99 ausschließen; Ausstieg, sobald sich das Signal normalisiert.
        Sv = np.minimum(-S[EQ].values, 0.99)
        pos = hysteresis(Sv, ok[EQ].values, 1.0, 0.0, H)
        W = pd.DataFrame(pos, index=C.index, columns=EQ).clip(lower=0) * 0.10 / vol[EQ]
        g, n = run(W, exe)
        entries = int(((pos[1:] > 0) & (pos[:-1] == 0)).sum())
        r = {"Signal": name, "Filter": filt, "Ausführung": "Schlusskurs" if exe == "close" else "nächste Eröffnung", "Haltedauer_max_Tage": H,
             "Trades_pa": entries / (len(C) / 252), "Zeit_im_Markt": float((W.abs().sum(axis=1) > 0).mean()),
             **{f"{k}_netto": v for k, v in stats_(n).items()}, "Sharpe_brutto": stats_(g)["Sharpe"]}
        rows.append(r)
        if (exe, H) == ("close", 2) and filt in ("kein Filter", "Trend + VIX"):
            curves[f"{name} · {filt}"] = n.loc["2007-06-01":].cumsum()
df = pd.DataFrame(rows)
df.to_csv(OUT / "dip_buying_grid.csv", index=False)
pd.DataFrame(curves).to_csv(OUT / "dip_buying_curves.csv")
# Vergleich: Buy & Hold des gleichen Korbs (risikogleich)
Wbh = pd.DataFrame(1.0, index=C.index, columns=EQ).where(mask[EQ], 0.0) * 0.10 / vol[EQ] / len(EQ) * 3
g, n = run(Wbh, "close")
json.dump({"BuyHold_Korb": stats_(n)}, open(OUT / "buyhold_reference.json", "w"), indent=1, default=float)
pd.set_option("display.width", 250)
print(df.round(2).sort_values("Sharpe_netto", ascending=False).head(20).to_string())
print(df.groupby(["Signal", "Filter"])[["Sharpe_netto", "Sharpe_bis2016_netto", "Sharpe_ab2017_netto"]].mean().round(2))
