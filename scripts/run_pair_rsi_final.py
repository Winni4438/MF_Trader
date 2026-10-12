"""Finale Kennzahlen des bereinigten Paar-Kandidaten (RSI 96 h, Abstand 30 Punkte, Haltedauer ≤ 24 h,
klassenübergreifend, ohne Altcoins und Soja) inkl. Placebo, Verzögerung, Kosten, Jahreswerte, Beine."""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mf_trader import backtest as bt, flow, meanrev as mr, overheat as oh  # noqa: E402
from mf_trader.data.panel import load_hourly  # noqa: E402
from mf_trader.universe import MR_BY_KEY  # noqa: E402

OUT = ROOT / "results" / "pair_rsi_deepdive"
P = load_hourly("hourly_mr")
ret, mask, close = P["ret"], P["mask"], P["close"]
vol = flow.realized_daily_vol(ret)
stress = bt.stress_multiplier(ret)
EX = ["SOL", "BNB", "XRP", "ADA", "DOGE", "AVAX", "LINK", "LTC", "SOY"]
keys = [k for k in ret.columns if k not in EX]
cls_of = {k: MR_BY_KEY[k].asset_class for k in keys}
O = ((oh.rsi(close, mask, 96) - 50) / 50)[keys].values
Mv = mask[keys].values
ci = {c: i for i, c in enumerate(keys)}
plist = [(a, b) for a, b in itertools.combinations(keys, 2) if cls_of[a] != cls_of[b]]
ia = np.array([ci[a] for a, _ in plist]); ib = np.array([ci[b] for _, b in plist])
pos = mr.hysteresis(O[:, ia] - O[:, ib], Mv[:, ia] & Mv[:, ib], 0.6, 0.0, 24)


def weights(p):
    U = np.zeros((len(ret), len(keys)))
    np.add.at(U.T, ia, p.T.astype(float)); np.add.at(U.T, ib, -p.T.astype(float))
    return (pd.DataFrame(U, index=ret.index, columns=keys) * 0.01 / vol[keys]).fillna(0.0)


W = weights(pos)
ev = lambda W_, d=0, c=1.0: bt.run(W_, P, delay=d, cost_mult=c, stress=stress).loc["2019-07-01":]  # noqa: E731
res = ev(W)
S = {"universe": keys, "n_pairs": len(plist), "entries": int(((pos[1:] != 0) & (pos[:-1] == 0)).sum())}
S["entries_pa"] = S["entries"] / 7.25
for tag, r in [("netto", res)]:
    S[tag] = {"Sharpe_ALL": bt.metrics(r)["Sharpe"], "Sharpe_IS": bt.metrics(r.loc[:"2022-12-31"])["Sharpe"],
              "Sharpe_OOS": bt.metrics(r.loc["2023-01-01":])["Sharpe"], "Sharpe_brutto": bt.metrics(r, "gross")["Sharpe"]}
S["latency_cost"] = {f"delay{d}_cost{c}": bt.metrics(ev(W, d, c))["Sharpe"] for d, c in itertools.product([0, 1, 2, 4], [1.0, 2.0])}
S["legs"] = {"long (unterkühlt)": bt.metrics(ev(W.clip(lower=0)))["Sharpe"], "short (überhitzt)": bt.metrics(ev(W.clip(upper=0)))["Sharpe"]}
d = bt.daily(res)
s10 = d * (0.10 / np.sqrt(252)) / d.std()
eq = (1 + s10).cumprod()
S["at_10pct_vol"] = {"CAGR": float(eq.iloc[-1] ** (252 / len(s10)) - 1), "MaxDD": float((eq / eq.cummax() - 1).min()),
                     "yearly_pct": {int(k): round(float(v) * 100, 1) for k, v in s10.groupby(s10.index.year).sum().items()},
                     "Hebel_vs_1pct_je_Bein": float((0.10 / np.sqrt(252)) / d.std()),
                     "mittlere_Brutto_Exposure_bei_10pct_vol": float(res["gross_exposure"].mean() * (0.10 / np.sqrt(252)) / d.std())}
hot, cold, hrs = [], [], []
for p in range(pos.shape[1]):
    st = np.flatnonzero((pos[1:, p] != 0) & (pos[:-1, p] == 0)) + 1
    for s0 in st:
        a, b = plist[p]
        hot.append(a if pos[s0, p] == -1 else b); cold.append(b if pos[s0, p] == -1 else a)
S["hot_top"] = pd.Series(hot).value_counts().head(8).to_dict()
S["cold_top"] = pd.Series(cold).value_counts().head(8).to_dict()
rng = np.random.default_rng(31)
plc = []
for i in range(60):
    sh = rng.integers(24 * 30, len(pos) - 24 * 30, size=pos.shape[1])
    plc.append(bt.metrics(ev(weights(np.stack([np.roll(pos[:, j], sh[j]) for j in range(pos.shape[1])], axis=1))))["Sharpe"])
S["placebo"] = {"real": S["netto"]["Sharpe_ALL"], "mean": float(np.mean(plc)), "p95": float(np.percentile(plc, 95)),
                "pctl": float(np.mean(np.array(plc) < S["netto"]["Sharpe_ALL"]))}
json.dump(S, open(OUT / "final_candidate.json", "w"), indent=1, default=float, ensure_ascii=False)
cr = pd.read_csv(OUT / "curve.csv", index_col=0, parse_dates=True)
cr["Relative-RSI-Paare (netto)"] = d.cumsum().reindex(cr.index)
cr["Verzögerung 1 h (netto)"] = bt.daily(ev(W, 1)).cumsum().reindex(cr.index)
cr["brutto"] = bt.daily(res, "gross").cumsum().reindex(cr.index)
cr.to_csv(OUT / "curve.csv")
print(json.dumps({k: v for k, v in S.items() if k != "universe"}, indent=1, default=float, ensure_ascii=False))
