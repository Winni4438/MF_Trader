"""Wörtlicher Test der Nutzer-Idee: Tages-RSI(14) – Asset A überkauft (≥ 70) und Asset B überverkauft (≤ 30)
-> A short / B long. Ausstieg, sobald sich die Einschätzung auflöst (einer der beiden RSI kreuzt 50) oder
spätestens nach 2 Tagen. Alle Paare gleichzeitig, überlappend, netto verrechnet.

Zwei Umsetzungen:
 a) Tagesdaten 2007–2026 (ETFs + Krypto, Ausführung zum Schlusskurs bzw. zur nächsten Eröffnung)
 b) Stundendaten 2019–2026 (RSI aus Tagesschlüssen 21:00 UTC, Ausführung in der nächsten Stunde, Futures-/Perp-Kosten)
Varianten: RSI-Schwellen 70/30, 80/20, 90/10 und RSI(2) mit 90/10 (Connors).
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mf_trader import backtest as bt, flow  # noqa: E402
from mf_trader.data.panel import load_hourly  # noqa: E402
from mf_trader.meanrev import hysteresis  # noqa: E402
from mf_trader.universe import MR_BY_KEY  # noqa: E402

OUT = ROOT / "results" / "user_rsi_example"
OUT.mkdir(parents=True, exist_ok=True)


def rsi_df(C, n):
    d = C.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def pair_positions(R, ia, ib, hi, enter, max_hold):
    """Positionen je Paar (+1 = A long/B short, -1 = A short/B long).
    Einstieg nur, wenn A überkauft (RSI >= hi) UND B überverkauft (RSI <= 100-hi) bzw. umgekehrt;
    Ausstieg, sobald einer der beiden RSI die 50 kreuzt (Einschätzung löst sich auf) oder nach max_hold."""
    band = hi - 50.0
    x = (R[:, ia] - 50) / band          # >1: A überkauft
    y = (50 - R[:, ib]) / band          # >1: B überverkauft
    s_hot = np.maximum(np.minimum(x, y), -0.99)    # nur Short-A-Einstiege möglich
    s_cold = np.minimum(np.maximum(x, y), 0.99)    # nur Long-A-Einstiege möglich
    return hysteresis(s_hot, enter, 1.0, 0.0, max_hold) + hysteresis(s_cold, enter, 1.0, 0.0, max_hold)


results = []

# ---------------------------------------------------------------- a) Tagesdaten (Wiederverwendung der Daily-Pipeline)
import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("mrd", ROOT / "scripts" / "run_meanrev_daily.py")
# Daily-Daten direkt nachbauen (ohne das ganze Daily-Experiment erneut zu rechnen)
src = (ROOT / "scripts" / "run_meanrev_daily.py").read_text(encoding="utf-8")
head = src.split("# ---------------------------------------------------------------- Indikatoren")[0]
ns = {"__file__": str(ROOT / "scripts" / "run_meanrev_daily.py")}
exec(compile(head, "daily_head", "exec"), ns)
C, mask_d, ret_d, cost_d, vol_d, cls_d = ns["C"], ns["mask"], ns["ret"], ns["cost"], ns["vol"], ns["cls_of"]
gap, intra, cc = ns["gap"], ns["intra"], ns["cc"]
keys_d = list(C.columns)
pairs_d = list(itertools.combinations(range(len(keys_d)), 2))
ia_d = np.array([a for a, _ in pairs_d])
ib_d = np.array([b for _, b in pairs_d])


def run_daily(W, execution):
    W = W.fillna(0.0)
    pnl = (W.shift(1) * cc).sum(axis=1) if execution == "close" else (W.shift(2) * gap).sum(axis=1) + (W.shift(1) * intra).sum(axis=1)
    tc = (W.diff().abs() * cost_d / 1e4).sum(axis=1)
    return pnl, pnl - tc


def sharpe(x):
    x = x[x.ne(0).idxmax():] if x.ne(0).any() else x
    return x.mean() / x.std() * np.sqrt(252) if x.std() > 0 else np.nan


for n, (hi, lo) in [(14, (70, 30)), (14, (80, 20)), (14, (90, 10)), (2, (90, 10)), (2, (95, 5))]:
    R = rsi_df(C, n).values
    enter = mask_d.values[:, ia_d] & mask_d.values[:, ib_d]
    pos = pair_positions(R, ia_d, ib_d, hi, enter, 2)
    U = np.zeros((len(C), len(keys_d)))
    np.add.at(U.T, ia_d, pos.T.astype(float))
    np.add.at(U.T, ib_d, -pos.T.astype(float))
    W = pd.DataFrame(U, index=C.index, columns=keys_d) * 0.005 / vol_d
    for exe in ["close", "open"]:
        g, net = run_daily(W, exe)
        g, net = g.loc["2007-06-01":], net.loc["2007-06-01":]
        entries = int(((pos[1:] != 0) & (pos[:-1] == 0)).sum())
        results.append({"Daten": "Tagesdaten 2007–2026", "RSI": f"RSI({n}) {hi}/{lo}", "Ausführung": "Schlusskurs" if exe == "close" else "nächste Eröffnung",
                        "Paar-Trades_pa": entries / (len(C) / 252), "Sharpe_brutto": sharpe(g), "Sharpe_netto": sharpe(net),
                        "Sharpe_netto_bis2016": sharpe(net.loc[:"2016-12-31"]), "Sharpe_netto_ab2017": sharpe(net.loc["2017-01-01":])})
    # Trade-Statistik je Paar-Trade (brutto, Schluss-Ausführung), für die Klassiker-Variante
    if (n, hi) == (14, 70):
        r1 = np.expm1(ret_d.fillna(0).values)
        trades = []
        for p in range(len(pairs_d)):
            col = pos[:, p]
            starts = np.flatnonzero((col[1:] != 0) & (col[:-1] == 0)) + 1
            for s0 in starts:
                e = s0
                while e < len(col) and col[e] == col[s0]:
                    e += 1
                d_ = col[s0]
                a, b = ia_d[p], ib_d[p]
                # Rendite des Paares (gleich gewichtet, ohne Vol-Skalierung) über die Haltedauer
                pr = (r1[s0 + 1:e + 1, a] - r1[s0 + 1:e + 1, b]).sum() * d_
                trades.append({"date": C.index[s0].date(), "A": keys_d[a], "B": keys_d[b], "dir": int(d_), "days": e - s0,
                               "ret_pct": pr * 100, "class_A": cls_d[keys_d[a]], "class_B": cls_d[keys_d[b]]})
        tr = pd.DataFrame(trades)
        tr.to_csv(OUT / "daily_rsi14_7030_trades.csv", index=False)

# ---------------------------------------------------------------- b) Stundendaten
P = load_hourly("hourly_mr")
ret, mask, close = P["ret"], P["mask"], P["close"]
keys = list(ret.columns)
vol = flow.realized_daily_vol(ret)
stress = bt.stress_multiplier(ret)
td = bt.trading_day(ret.index)
daily_close = close.groupby(td).last()
pairs = list(itertools.combinations(range(len(keys)), 2))
ia = np.array([a for a, _ in pairs])
ib = np.array([b for _, b in pairs])
for n, (hi, lo) in [(14, (70, 30)), (14, (80, 20)), (2, (90, 10))]:
    Rd = rsi_df(daily_close, n)
    # Tageswert gilt ab dem Tagesschluss (21:00 UTC) -> auf Stunden des Folgetags abbilden
    Rh = Rd.shift(1).reindex(td)
    Rh.index = ret.index
    enter = mask.values[:, ia] & mask.values[:, ib]
    pos = pair_positions(Rh.values, ia, ib, hi, enter, 48)
    U = np.zeros((len(ret), len(keys)))
    np.add.at(U.T, ia, pos.T.astype(float))
    np.add.at(U.T, ib, -pos.T.astype(float))
    W = pd.DataFrame(U, index=ret.index, columns=keys) * 0.005 / vol
    res = bt.run(W.fillna(0.0), P, stress=stress).loc["2019-07-01":]
    entries = int(((pos[1:] != 0) & (pos[:-1] == 0)).sum())
    results.append({"Daten": "Stundendaten 2019–2026", "RSI": f"RSI({n}) {hi}/{lo}", "Ausführung": "nächste Stunde",
                    "Paar-Trades_pa": entries / (len(ret) / 24 / 365), "Sharpe_brutto": bt.metrics(res, "gross")["Sharpe"],
                    "Sharpe_netto": bt.metrics(res)["Sharpe"], "Sharpe_netto_bis2016": np.nan,
                    "Sharpe_netto_ab2017": np.nan, "Sharpe_netto_bis2022": bt.metrics(res.loc[:"2022-12-31"])["Sharpe"],
                    "Sharpe_netto_ab2023": bt.metrics(res.loc["2023-01-01":])["Sharpe"]})
    if (n, hi) == (14, 70):
        pd.DataFrame({"netto": bt.daily(res).cumsum(), "brutto": bt.daily(res, "gross").cumsum()}).to_csv(OUT / "hourly_rsi14_7030_curve.csv")
        # Konkretes Beispiel BTC vs. Gold
        if "BTC" in keys and "GOLD" in keys:
            p = pairs.index(tuple(sorted((keys.index("BTC"), keys.index("GOLD")))))
            n_e = int(((pos[1:, p] != 0) & (pos[:-1, p] == 0)).sum())
            w = pd.DataFrame({keys[ia[p]]: pos[:, p] * 0.02 / vol[keys[ia[p]]], keys[ib[p]]: -pos[:, p] * 0.02 / vol[keys[ib[p]]]}, index=ret.index)
            r2 = bt.run(w.fillna(0.0), P, stress=stress).loc["2019-07-01":]
            json.dump({"pair": f"{keys[ia[p]]}/{keys[ib[p]]}", "entries": n_e, "Sharpe_netto": bt.metrics(r2)["Sharpe"],
                       "Sharpe_brutto": bt.metrics(r2, "gross")["Sharpe"], "net_sum_pct": float(r2["net"].sum() * 100)},
                      open(OUT / "btc_gold_example.json", "w"), indent=1, default=float)

df = pd.DataFrame(results)
df.to_csv(OUT / "user_rsi_example.csv", index=False)
print(df.round(2).to_string())
if (OUT / "daily_rsi14_7030_trades.csv").exists():
    tr = pd.read_csv(OUT / "daily_rsi14_7030_trades.csv")
    print("Paar-Trades (Tagesdaten, RSI14 70/30):", len(tr), "Ø Rendite %", round(tr.ret_pct.mean(), 3), "Trefferquote", round((tr.ret_pct > 0).mean(), 3),
          "Ø Tage", round(tr.days.mean(), 2))
    print(tr.groupby(["class_A", "class_B"]).ret_pct.agg(["count", "mean"]).sort_values("count", ascending=False).head(12).round(3))
