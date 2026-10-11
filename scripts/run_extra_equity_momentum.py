"""Zusatztest: Aktienindex-Momentum nach starken RORO-Signalen (aus der Ereignisstudie abgeleitet,
deshalb besonders auf Out-of-Sample achten)."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mf_trader import backtest as bt, flow  # noqa: E402
from mf_trader.data.panel import load_hourly  # noqa: E402
from mf_trader.universe import HAVEN, RISK  # noqa: E402

P = load_hourly()
ret, mask = P["ret"], P["mask"]
risk = [a for a in RISK if a in ret]
haven = [a for a in HAVEN if a in ret]
svar = flow.seasonal_var(ret)
vol = flow.realized_daily_vol(ret)
stress = bt.stress_multiplier(ret)
rows = []
for w in [4]:
    z = flow.standardize(flow.roro(flow.flow_score(ret, svar, w), risk, haven))
    for th in [2.5, 3.0, 3.5]:
        for side in ["on", "off"]:
            for hold in [2, 4, 8]:
                trig = (z >= th) & ~(z.shift(1) >= th) if side == "on" else (z <= -th) & ~(z.shift(1) <= -th)
                sgn = 1.0 if side == "on" else -1.0
                tgt = pd.DataFrame(0.0, index=ret.index, columns=["SPX", "NDX"])
                idx = np.flatnonzero(trig.values)
                for i in idx:
                    for a in ["SPX", "NDX"]:
                        tgt.iloc[i:i + hold, tgt.columns.get_loc(a)] = sgn * 0.05 / vol[a].iloc[i]
                res = bt.run(tgt.fillna(0.0), P, stress=stress).loc["2019-07-01":]
                m_is, m_oos = bt.metrics(res.loc[:"2022-12-31"]), bt.metrics(res.loc["2023-01-01":])
                rows.append({"side": side, "theta": th, "hold_h": hold, "Sharpe_brutto": bt.metrics(res, "gross")["Sharpe"],
                             "Sharpe_netto_IS": m_is["Sharpe"], "Sharpe_netto_OOS": m_oos["Sharpe"],
                             "AvgTrade_bps": bt.metrics(res)["AvgTrade_bps"], "Trades_pa": bt.metrics(res)["Trades_pa"]})
df = pd.DataFrame(rows)
df.to_csv(ROOT / "results" / "hourly" / "extra_equity_momentum.csv", index=False)
print(df.round(2).to_string())

# Placebo: gleiche Anzahl zufälliger Einstiege (gleiche Haltedauer) -> Sharpe-Verteilung
rng = np.random.default_rng(7)
pool = np.flatnonzero((ret.index >= pd.Timestamp("2019-07-01", tz="UTC")) & mask["SPX"].values)
out = {}
z = flow.standardize(flow.roro(flow.flow_score(ret, svar, 4), risk, haven))
for th, hold in ([(3.0, 4), (3.0, 8), (3.5, 4)] if "--placebo" in sys.argv else []):
    trig = (z >= th) & ~(z.shift(1) >= th)
    n = int(trig.loc["2019-07-01":].sum())
    real = df[(df.side == "on") & (df.theta == th) & (df.hold_h == hold)]
    sims = []
    for k in range(300):
        idx = rng.choice(pool, size=n, replace=False)
        tgt = pd.DataFrame(0.0, index=ret.index, columns=["SPX", "NDX"])
        for i in idx:
            for a in ["SPX", "NDX"]:
                tgt.iloc[i:i + hold, tgt.columns.get_loc(a)] = 0.05 / vol[a].iloc[i]
        res = bt.run(tgt.fillna(0.0), P, stress=stress).loc["2019-07-01":]
        sims.append(bt.metrics(res)["Sharpe"])
    res_real = None
    tgt = pd.DataFrame(0.0, index=ret.index, columns=["SPX", "NDX"])
    for i in np.flatnonzero(trig.values):
        for a in ["SPX", "NDX"]:
            tgt.iloc[i:i + hold, tgt.columns.get_loc(a)] = 0.05 / vol[a].iloc[i]
    real_all = bt.metrics(bt.run(tgt.fillna(0.0), P, stress=stress).loc["2019-07-01":])["Sharpe"]
    sims = np.array(sims)
    out[f"z{th}_h{hold}"] = {"real_sharpe_all": float(real_all), "placebo_mean": float(np.nanmean(sims)),
                            "placebo_p95": float(np.nanpercentile(sims, 95)), "pctl": float(np.nanmean(sims < real_all)), "n_events": n}
print(out) if out else None
if out:
    json.dump(out, open(ROOT / "results" / "hourly" / "extra_equity_momentum_placebo.json", "w"), indent=2)

# Equity-Kurve & Jahreswerte der Kernvariante (z>=3, 4h, long SPX+NDX)
trig = (z >= 3.0) & ~(z.shift(1) >= 3.0)
tgt = pd.DataFrame(0.0, index=ret.index, columns=["SPX", "NDX"])
for i in np.flatnonzero(trig.values):
    for a in ["SPX", "NDX"]:
        tgt.iloc[i:i + 4, tgt.columns.get_loc(a)] = 0.05 / vol[a].iloc[i]
res = bt.run(tgt.fillna(0.0), P, stress=stress).loc["2019-07-01":]
d = bt.daily(res)
pd.DataFrame({"Risk-on-Momentum Aktienindex (z≥3, 4h)": d.cumsum(),
              "Risk-on-Momentum Aktienindex (z≥3, 4h) (brutto)": bt.daily(res, "gross").cumsum()}).to_csv(
    ROOT / "results" / "hourly" / "extra_equity_momentum_curve.csv")
yr = (d.groupby(d.index.year).sum() * 100).round(2).to_dict()
m = bt.metrics(res)
json.dump({"yearly_pct": yr, "metrics_all": m, "metrics_IS": bt.metrics(res.loc[:"2022-12-31"]),
           "metrics_OOS": bt.metrics(res.loc["2023-01-01":])}, open(ROOT / "results" / "hourly" / "extra_equity_momentum_summary.json", "w"),
          indent=2, default=float)
print("Jahre:", yr, "Sharpe", round(m["Sharpe"], 2), "MaxDD", round(m["MaxDD"], 3), "CAGR", round(m["CAGR"], 4), "Vol", round(m["Vol"], 4))
