"""Placebo-Test für den IBS-Dip-Kauf (Tagesdaten 2007–2026): gleiche Anzahl Einstiege je Asset, gleiche
Haltedauer (2 Tage), aber zufällige Einstiegstage. Vergleich der Sharpe-Verteilung mit dem echten Signal."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mf_trader.meanrev import hysteresis  # noqa: E402

src = (ROOT / "scripts" / "run_meanrev_daily.py").read_text(encoding="utf-8")
head = src.split("# ---------------------------------------------------------------- Indikatoren")[0]
ns = {"__file__": str(ROOT / "scripts" / "run_meanrev_daily.py")}
exec(compile(head, "daily_head", "exec"), ns)
C, Hi, Lo, mask, cost, vol, cc = (ns[k] for k in ["C", "Hi", "Lo", "mask", "cost", "vol", "cc"])
out = {}
for name, EQ in [("US (SPY, QQQ, IWM)", ["SPY", "QQQ", "IWM"]),
                 ("15 Aktienindizes", ["SPY", "QQQ", "IWM", "EFA", "VGK", "EWJ", "EEM", "EWG", "EWU", "EWA", "EWC", "EWY", "EWZ", "FXI", "EWW"])]:
    ibs = (C - Lo) / (Hi - Lo).replace(0, np.nan)
    S = np.minimum(-((0.5 - ibs[EQ]) / 0.3).values, 0.99)
    pos = hysteresis(S, mask[EQ].values, 1.0, 0.0, 2)

    def sharpe_of(p):
        W = pd.DataFrame(p, index=C.index, columns=EQ).clip(lower=0) * 0.10 / vol[EQ]
        W = W.fillna(0.0)
        pnl = (W.shift(1) * cc[EQ]).sum(axis=1) - (W.diff().abs() * cost[EQ] / 1e4).sum(axis=1)
        x = pnl.loc["2007-06-01":]
        return x.mean() / x.std() * np.sqrt(252)

    real = sharpe_of(pos)
    rng = np.random.default_rng(5)
    sims = []
    n_entries = ((pos[1:] > 0) & (pos[:-1] == 0)).sum(axis=0)
    valid = mask[EQ].values
    for _ in range(300):
        P = np.zeros_like(pos)
        for j in range(len(EQ)):
            cand = np.flatnonzero(valid[:, j])
            starts = np.sort(rng.choice(cand[:-3], size=int(n_entries[j]), replace=False))
            for s0 in starts:
                P[s0:s0 + 2, j] = 1
        sims.append(sharpe_of(P))
    sims = np.array(sims)
    out[name] = {"real": float(real), "placebo_mean": float(sims.mean()), "placebo_p95": float(np.percentile(sims, 95)),
                 "pctl": float((sims < real).mean())}
    print(name, out[name], flush=True)
(ROOT / "results" / "dip_buying").mkdir(exist_ok=True, parents=True)
json.dump(out, open(ROOT / "results" / "dip_buying" / "ibs_placebo.json", "w"), indent=1)
