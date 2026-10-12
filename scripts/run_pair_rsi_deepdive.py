"""Tiefenprüfung des einzigen konsistent positiven Intraday-Kandidaten:
Paare mit relativem RSI-Extrem auf langsamen Fenstern (48–168 Stunden), Haltedauer ≤ 48 h.

Prüfungen: Parameter-Umgebung, Klassenpaar-Beiträge, Long- vs. Short-Bein, Verzögerung, doppelte Kosten,
Placebo (zeitlich verschobene Signale), Deflated Sharpe (Familie), Jahreswerte, Konzentration.
Ergebnisse -> results/pair_rsi_deepdive/
"""
import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mf_trader import backtest as bt, flow, meanrev as mr, overheat as oh  # noqa: E402
from mf_trader.data.panel import load_hourly  # noqa: E402
from mf_trader.stats import deflated_sharpe  # noqa: E402
from mf_trader.universe import MR_BY_KEY  # noqa: E402

OUT = ROOT / "results" / "pair_rsi_deepdive"
OUT.mkdir(parents=True, exist_ok=True)
START, IS_END, OOS_START = "2019-07-01", "2022-12-31", "2023-01-01"
T0 = time.time()


def log(*a):
    print(f"[{time.time()-T0:6.0f}s]", *a, flush=True)


P = load_hourly("hourly_mr")
ret, mask, close = P["ret"], P["mask"], P["close"]
keys = list(ret.columns)
cls_of = {k: MR_BY_KEY[k].asset_class for k in keys}
vol = flow.realized_daily_vol(ret)
stress = bt.stress_multiplier(ret)
Mv = mask.values
ci = {c: i for i, c in enumerate(keys)}
all_pairs = list(itertools.combinations(keys, 2))
SCOPES = {"klassenübergreifend": [(a, b) for a, b in all_pairs if cls_of[a] != cls_of[b]],
          "gleiche Klasse": [(a, b) for a, b in all_pairs if cls_of[a] == cls_of[b]],
          "alle": all_pairs}
RSI = {n: ((oh.rsi(close, mask, n) - 50) / 50) for n in (48, 72, 96, 120, 168)}
log("RSI fertig")


def build(n, th, H, scope, delay=0):
    plist = SCOPES[scope]
    ia = np.array([ci[a] for a, _ in plist])
    ib = np.array([ci[b] for _, b in plist])
    Ov = RSI[n].values
    S = Ov[:, ia] - Ov[:, ib]
    enter = Mv[:, ia] & Mv[:, ib]
    pos = mr.hysteresis(S, enter, th, 0.0, H)
    U = np.zeros((len(ret), len(keys)))
    np.add.at(U.T, ia, pos.T.astype(float))
    np.add.at(U.T, ib, -pos.T.astype(float))
    W = pd.DataFrame(U, index=ret.index, columns=keys) * 0.01 / vol
    return W.fillna(0.0), pos, ia, ib


def evaluate(W, delay=0, cost_mult=1.0):
    return bt.run(W, P, delay=delay, cost_mult=cost_mult, stress=stress).loc[START:]


def m3(res):
    return {"Sharpe_IS": bt.metrics(res.loc[:IS_END])["Sharpe"], "Sharpe_OOS": bt.metrics(res.loc[OOS_START:])["Sharpe"],
            "Sharpe_ALL": bt.metrics(res)["Sharpe"], "Sharpe_brutto": bt.metrics(res, "gross")["Sharpe"]}


# 1) Parameter-Umgebung
rows = []
for n, th, H, scope in itertools.product([48, 72, 96, 120, 168], [0.5, 0.6, 0.7, 0.8, 0.9], [12, 24, 48], ["klassenübergreifend", "gleiche Klasse"]):
    W, pos, ia, ib = build(n, th, H, scope)
    entries = int(((pos[1:] != 0) & (pos[:-1] == 0)).sum())
    if entries < 30:
        rows.append({"rsi_h": n, "theta": th, "hold_h": H, "scope": scope, "entries": entries})
        continue
    res = evaluate(W)
    rows.append({"rsi_h": n, "theta": th, "hold_h": H, "scope": scope, "entries": entries, "entries_pa": entries / 7.25, **m3(res)})
    del W, pos
grid = pd.DataFrame(rows)
grid.to_csv(OUT / "neighbourhood_grid.csv", index=False)
log("Umgebung:", len(grid))

# Kandidat: mittig in der positiven Zone (nicht das Maximum), aus IS-Sicht
g = grid.dropna(subset=["Sharpe_IS"])
g = g[(g.scope == "klassenübergreifend") & (g.entries_pa >= 40)]
cand = g.sort_values("Sharpe_IS", ascending=False)
# Robustheit: Mittel der Nachbarn (gleiches rsi_h/theta, alle Haltedauern)
nb = g.groupby(["rsi_h", "theta"])[["Sharpe_IS", "Sharpe_OOS"]].mean().rename(columns=lambda c: c + "_nachbarn")
cand = cand.merge(nb, left_on=["rsi_h", "theta"], right_index=True)
pick = cand.sort_values("Sharpe_IS_nachbarn", ascending=False).iloc[0]
key = (int(pick.rsi_h), float(pick.theta), int(pick.hold_h), "klassenübergreifend")
log("Kandidat:", key, pick[["Sharpe_IS", "Sharpe_OOS", "Sharpe_IS_nachbarn", "Sharpe_OOS_nachbarn"]].to_dict())
W, pos, ia, ib = build(*key)
res = evaluate(W)
summary = {"candidate": {"rsi_h": key[0], "theta": key[1], "hold_h": key[2], "scope": key[3], **m3(res),
                         "entries_pa": float(pick.entries_pa)}}

# 2) Verzögerung & Kosten
lc = []
for dly, cm in itertools.product([0, 1, 2, 4], [1.0, 2.0]):
    r = evaluate(W, delay=dly, cost_mult=cm)
    lc.append({"delay_h": dly, "cost_mult": cm, **m3(r)})
pd.DataFrame(lc).to_csv(OUT / "latency_cost.csv", index=False)

# 3) Long- vs. Short-Bein: Gewinn aus dem unterkühlten (long) oder dem überhitzten (short) Bein?
legs = {}
for side, Ws in [("nur unterkühltes Bein (long)", W.clip(lower=0)), ("nur überhitztes Bein (short)", W.clip(upper=0))]:
    legs[side] = m3(evaluate(Ws))
summary["legs"] = legs

# 4) Beiträge je Klassenpaar (Brutto-P&L der Einzelpaare)
plist = SCOPES[key[3]]
r1 = np.expm1(ret.fillna(0.0).values)
v = vol.values
contrib = {}
trades = []
for p, (a, b) in enumerate(plist):
    col = pos[:, p]
    if not col.any():
        continue
    wa = col * 0.01 / v[:, ci[a]]
    wb = -col * 0.01 / v[:, ci[b]]
    wa = np.nan_to_num(wa)
    wb = np.nan_to_num(wb)
    pnl = np.r_[0, wa[:-1] * r1[1:, ci[a]] + wb[:-1] * r1[1:, ci[b]]]
    kk = tuple(sorted((cls_of[a], cls_of[b])))
    contrib.setdefault(kk, [0.0, 0])
    contrib[kk][0] += pnl[ret.index >= pd.Timestamp(START, tz="UTC")].sum()
    starts = np.flatnonzero((col[1:] != 0) & (col[:-1] == 0)) + 1
    contrib[kk][1] += len(starts)
    for s0 in starts:
        e = s0
        while e < len(col) and col[e] == col[s0]:
            e += 1
        hot = a if col[s0] == -1 else b
        cold = b if col[s0] == -1 else a
        pr = ((r1[s0 + 1:e + 1, ci[cold]] - r1[s0 + 1:e + 1, ci[hot]]).sum())
        trades.append({"start": ret.index[s0], "hot": hot, "cold": cold, "hours": e - s0, "ret_bps_gleichgewichtet": pr * 1e4,
                       "cost_bps": 2 * (MR_BY_KEY[hot].cost_bps + MR_BY_KEY[cold].cost_bps)})
cb = pd.DataFrame([{"Klasse_A": k[0], "Klasse_B": k[1], "P&L_brutto_rel": v_[0], "Trades": v_[1]} for k, v_ in contrib.items()])
cb = cb.sort_values("P&L_brutto_rel", ascending=False)
cb.to_csv(OUT / "class_pair_contribution.csv", index=False)
tr = pd.DataFrame(trades)
tr.to_csv(OUT / "trades.csv", index=False)
summary["trades"] = {"n": len(tr), "avg_hours": float(tr.hours.mean()), "avg_ret_bps": float(tr.ret_bps_gleichgewichtet.mean()),
                     "median_ret_bps": float(tr.ret_bps_gleichgewichtet.median()), "hit": float((tr.ret_bps_gleichgewichtet > tr.cost_bps).mean()),
                     "avg_cost_bps": float(tr.cost_bps.mean())}
hot_cnt = tr.hot.value_counts().head(10).to_dict()
cold_cnt = tr.cold.value_counts().head(10).to_dict()
summary["most_often_hot"] = hot_cnt
summary["most_often_cold"] = cold_cnt

# 5) Konzentration: mittlere Netto-Exposition je Asset (Vorzeichen)
summary["mean_net_weight_top"] = W.loc[START:].mean().sort_values().round(4).head(5).to_dict() | W.loc[START:].mean().sort_values().round(4).tail(5).to_dict()

# 6) Placebo: zeitlich zufällig verschobene Positionsspalten (gleiche Häufigkeit/Haltedauer)
rng = np.random.default_rng(23)
plc = []
for i in range(100):
    sh = rng.integers(24 * 30, len(pos) - 24 * 30, size=pos.shape[1])
    posr = np.stack([np.roll(pos[:, j], sh[j]) for j in range(pos.shape[1])], axis=1)
    U = np.zeros((len(ret), len(keys)))
    np.add.at(U.T, ia, posr.T.astype(float))
    np.add.at(U.T, ib, -posr.T.astype(float))
    Wr = (pd.DataFrame(U, index=ret.index, columns=keys) * 0.01 / vol).fillna(0.0)
    plc.append(bt.metrics(evaluate(Wr))["Sharpe"])
plc = np.array(plc)
summary["placebo"] = {"real": float(bt.metrics(res)["Sharpe"]), "mean": float(plc.mean()), "p95": float(np.percentile(plc, 95)),
                      "pctl": float((plc < bt.metrics(res)["Sharpe"]).mean())}
log("Placebo:", summary["placebo"])

# 7) Deflated Sharpe: alle Paar-Varianten dieser Studie als Versuchsmenge (Stunden-Paargitter + Umgebung)
pg = pd.read_csv(ROOT / "results" / "meanrev_hourly" / "pairs_grid.csv")
trials = np.r_[pg["Sharpe_ALL"].dropna().values, grid["Sharpe_ALL"].dropna().values] / np.sqrt(252)
d = bt.daily(res)
summary["deflated_sharpe_pairs_family"] = deflated_sharpe(d.values, trials)
summary["deflated_sharpe_pairs_family"]["n_trials"] = int(len(trials))

# 8) Jahreswerte & skalierte Kennzahlen
s10 = d * (0.10 / np.sqrt(252)) / d.std()
eq = (1 + s10).cumprod()
summary["at_10pct_vol"] = {"CAGR": float(eq.iloc[-1] ** (252 / len(s10)) - 1), "MaxDD": float((eq / eq.cummax() - 1).min()),
                           "yearly_pct": {int(k): round(float(v_) * 100, 1) for k, v_ in s10.groupby(s10.index.year).sum().items()},
                           "leverage_factor_vs_1pct_leg": float((0.10 / np.sqrt(252)) / d.std())}
pd.DataFrame({"Relative-RSI-Paare (netto)": d.cumsum(), "brutto": bt.daily(res, "gross").cumsum(),
              "Verzögerung 1 h (netto)": bt.daily(evaluate(W, delay=1)).cumsum()}).to_csv(OUT / "curve.csv")
json.dump(summary, open(OUT / "summary.json", "w"), indent=1, default=float, ensure_ascii=False)
log(json.dumps(summary, indent=1, default=float, ensure_ascii=False)[:3000])
log("FERTIG")
