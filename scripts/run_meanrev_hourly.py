"""Mean Reversion / Überhitzung auf Stundenbasis (07/2019–09/2026), Haltedauer ≤ 48 Stunden.

Familien:
 1) Einzelasset: überhitzt -> short, unterkühlt -> long
 2) Paare: alle Kombinationen, überlappend und netto verrechnet (gleiche Klasse vs. klassenübergreifend)
 3) Korb gegen Korb (Anlageklassen-Körbe)
 4) Querschnitt (alle Assets bzw. klassenneutral)
 5) Faktor-Residuen (PCA, Avellaneda/Lee-Stil)
 6) Krypto-Funding-Extreme (Hebel-Überhitzung)
 + Konditionierung (Stressregime, nur long/nur short), Placebo, Deflated Sharpe
Ergebnisse -> results/meanrev_hourly/
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
from mf_trader.data.panel import ROLL_REPORT, SPIKE_REPORT, build_hourly, load_hourly, save_hourly  # noqa: E402
from mf_trader.stats import deflated_sharpe  # noqa: E402
from mf_trader.universe import MR_BY_KEY, MR_UNIVERSE  # noqa: E402

OUT = ROOT / "results" / "meanrev_hourly"
OUT.mkdir(parents=True, exist_ok=True)
START, IS_END, OOS_START = "2019-07-01", "2022-12-31", "2023-01-01"
T0 = time.time()
QUICK = "--quick" in sys.argv


def log(*a):
    print(f"[{time.time()-T0:6.0f}s]", *a, flush=True)


# ---------------------------------------------------------------- Daten
if "--rebuild" in sys.argv or not (ROOT / "data/processed/hourly_mr_close.parquet").exists():
    save_hourly(build_hourly("2019-01-01", "2026-10-01", universe=MR_UNIVERSE), "hourly_mr")
    json.dump({"spikes": SPIKE_REPORT, "rolls": ROLL_REPORT}, open(OUT / "data_cleaning_report.json", "w"), indent=1)
P = load_hourly("hourly_mr")
ret, mask, close = P["ret"], P["mask"], P["close"]
keys = list(ret.columns)
cls_of = {k: MR_BY_KEY[k].asset_class for k in keys}
groups = {}
for k in keys:
    groups.setdefault(cls_of[k], []).append(k)
# Währungen in 'Risiko-FX' und 'Hafen-FX' trennen, Krypto in Majors und Altcoins
if "Währungen" in groups:
    groups["Hafen-FX"] = [k for k in groups["Währungen"] if k in ("JPY", "CHF")]
    groups["Risiko-FX"] = [k for k in groups["Währungen"] if k in ("AUD", "NZD", "CAD", "NOK", "MXN", "ZAR")]
    groups["Euro/Pfund"] = [k for k in groups["Währungen"] if k in ("EUR", "GBP")]
    del groups["Währungen"]
if "Krypto" in groups:
    groups["Krypto-Majors"] = [k for k in groups["Krypto"] if k in ("BTC", "ETH")]
    groups["Altcoins"] = [k for k in groups["Krypto"] if k not in ("BTC", "ETH")]
    del groups["Krypto"]
groups = {g: m for g, m in groups.items() if m}
log("Assets:", len(keys), keys)
log("Körbe:", {g: len(m) for g, m in groups.items()})
# größte Stundenbewegungen zur Kontrolle
top = {k: [(str(t)[:13], round(float(v) * 100, 2)) for t, v in ret[k].abs().nlargest(5).items()] for k in keys}
json.dump(top, open(OUT / "largest_hourly_moves.json", "w"), indent=1)

svar = flow.seasonal_var(ret)
vol = flow.realized_daily_vol(ret)
stress = bt.stress_multiplier(ret)
Mv = mask.values
log("Basisgrößen fertig")

# ---------------------------------------------------------------- Indikatoren
IND = {}
for n in ([14, 48] if QUICK else [6, 14, 48, 96]):
    IND[f"RSI{n}"] = (oh.rsi(close, mask, n) - 50) / 50
for L in ([12, 24] if QUICK else [4, 12, 24, 48]):
    IND[f"Z{L}"] = flow.flow_score(ret, svar, L)
if not QUICK:
    IND["BB72"] = oh.zscore_ma(close, mask, 72)
zret = (ret / np.sqrt(svar)).clip(-8, 8)
IND["RES24"] = oh.pca_residual_scores(zret.where(mask), k=3, window=24 * 30, step=24, L=24)
log("Indikatoren:", list(IND))


def evaluate(W):
    return bt.run(W.fillna(0.0), P, stress=stress).loc[START:]


def mets(res):
    out = {}
    for tag, sl in [("IS", slice(START, IS_END)), ("OOS", slice(OOS_START, None)), ("ALL", slice(START, None))]:
        m = bt.metrics(res.loc[sl])
        out[f"Sharpe_{tag}"] = m["Sharpe"]
        if tag == "ALL":
            out.update({"CAGR_ALL": m["CAGR"], "Vol_ALL": m["Vol"], "MaxDD_ALL": m["MaxDD"], "t_ALL": m["t_stat"]})
    out["Sharpe_brutto_ALL"] = bt.metrics(res, "gross")["Sharpe"]
    g, c = res["gross"].sum(), res["cost"].sum()
    out["Kosten_bps_pa"] = c / (len(res) / 24 / 365) * 1e4
    out["Brutto_bps_pa"] = g / (len(res) / 24 / 365) * 1e4
    out["Turnover_pa"] = res["turnover"].sum() / (len(res) / 24 / 365)
    return out


def entries_pa(pos):
    e = ((pos[1:] != 0) & (pos[:-1] == 0)).sum()
    return float(e / (len(pos) / 24 / 365))


THR_TS = {"RSI6": [0.6, 0.8], "RSI14": [0.4, 0.6], "RSI48": [0.3, 0.5], "RSI96": [0.2, 0.4], "Z4": [2.0, 2.5, 3.0], "Z12": [2.0, 2.5, 3.0],
          "Z24": [2.0, 2.5, 3.0], "Z48": [2.0, 2.5], "BB72": [2.0, 2.5], "RES24": [2.0, 2.5, 3.0]}
HOLDS = [12, 24, 48] if not QUICK else [24]
store = {}

# ---------------------------------------------------------------- 1) Einzelasset
rows = []
for ind, O in IND.items():
    for th, H in itertools.product(THR_TS[ind][:(1 if QUICK else 3)], HOLDS):
        pos = mr.hysteresis(O.values, Mv, th, 0.0, H)
        W = pd.DataFrame(pos, index=ret.index, columns=keys) * 0.05 / vol
        res = evaluate(W)
        rows.append({"family": "Einzelasset", "indicator": ind, "theta": th, "hold_max_h": H, "entries_pa": entries_pa(pos), **mets(res)})
        store[("ts", ind, th, H)] = res
        if not QUICK:
            for g, mem in groups.items():
                r2 = evaluate(W[mem])
                rows.append({"family": "Einzelasset je Klasse", "class": g, "indicator": ind, "theta": th, "hold_max_h": H, **mets(r2)})
            for side, Ws in [("nur long", W.clip(lower=0)), ("nur short", W.clip(upper=0))]:
                rows.append({"family": f"Einzelasset {side}", "indicator": ind, "theta": th, "hold_max_h": H, **mets(evaluate(Ws))})
ts = pd.DataFrame(rows)
ts.to_csv(OUT / "single_asset_grid.csv", index=False)
log("Einzelasset:", len(ts))

# ---------------------------------------------------------------- 2) Paare (alle Kombinationen, überlappend)
all_pairs = list(itertools.combinations(keys, 2))
same = [(a, b) for a, b in all_pairs if cls_of[a] == cls_of[b]]
cross = [(a, b) for a, b in all_pairs if cls_of[a] != cls_of[b]]
log("Paare gesamt", len(all_pairs), "gleiche Klasse", len(same), "klassenübergreifend", len(cross))
ci = {c: i for i, c in enumerate(keys)}
THR_P = {"RSI14": [0.8, 1.1], "RSI48": [0.6, 0.9], "RSI96": [0.4, 0.7], "Z12": [2.5, 3.0], "Z24": [2.5, 3.0], "Z48": [2.5, 3.0], "RES24": [2.5, 3.0]}
rows = []
pair_trials = []
for ind, ths in THR_P.items():
    if ind not in IND:
        continue
    Ov = IND[ind].values
    for scope, plist in [("gleiche Klasse", same), ("klassenübergreifend", cross)]:
        ia = np.array([ci[a] for a, _ in plist])
        ib = np.array([ci[b] for _, b in plist])
        S = Ov[:, ia] - Ov[:, ib]
        if ind.startswith(("Z", "RES")):
            S = S / np.sqrt(2)
        enter = Mv[:, ia] & Mv[:, ib]
        for th, H in itertools.product(ths[:(1 if QUICK else 2)], HOLDS):
            pos = mr.hysteresis(S, enter, th, 0.0, H)
            Uu = np.zeros((len(ret), len(keys)))
            np.add.at(Uu.T, ia, pos.T.astype(float))
            np.add.at(Uu.T, ib, -pos.T.astype(float))
            W = pd.DataFrame(Uu, index=ret.index, columns=keys) * 0.01 / vol
            res = evaluate(W)
            r = {"family": "Paare", "scope": scope, "indicator": ind, "theta": th, "hold_max_h": H,
                 "n_pairs": len(plist), "entries_pa": entries_pa(pos), **mets(res)}
            rows.append(r)
            store[("pair", ind, scope, th, H)] = (res, pos, ia, ib)
pp = pd.DataFrame(rows)
pp.to_csv(OUT / "pairs_grid.csv", index=False)
log("Paare:", len(pp))

# Einzelpaare der besten IS-Konfiguration
bp = pp.sort_values("Sharpe_IS", ascending=False).iloc[0]
_, pos, ia, ib = store[("pair", bp.indicator, bp.scope, bp.theta, int(bp.hold_max_h))]
plist = same if bp.scope == "gleiche Klasse" else cross
indiv = []
for p, (a, b) in enumerate(plist):
    n_e = int(((pos[1:, p] != 0) & (pos[:-1, p] == 0)).sum())
    if n_e < 20:
        continue
    w = pd.DataFrame({a: pos[:, p] * 0.02 / vol[a], b: -pos[:, p] * 0.02 / vol[b]}, index=ret.index)
    res = evaluate(w)
    indiv.append({"A": a, "B": b, "class_A": cls_of[a], "class_B": cls_of[b], "entries": n_e,
                  "Sharpe_IS": bt.metrics(res.loc[:IS_END])["Sharpe"], "Sharpe_OOS": bt.metrics(res.loc[OOS_START:])["Sharpe"],
                  "Sharpe_ALL": bt.metrics(res)["Sharpe"], "Sharpe_brutto": bt.metrics(res, "gross")["Sharpe"]})
pd.DataFrame(indiv).to_csv(OUT / "pairs_individual_best_config.csv", index=False)
log("Einzelpaare:", len(indiv))

# ---------------------------------------------------------------- 3) Korb gegen Korb
rows = []
for ind in ["RSI14", "RSI48", "RSI96", "Z12", "Z24", "Z48", "RES24"]:
    if ind not in IND:
        continue
    for th, H in itertools.product([1.5, 2.0, 2.5][:(1 if QUICK else 3)], HOLDS):
        B = mr.basket_signal(IND[ind], groups)
        # Spreads auf IS-Streuung normieren, damit Schwellen vergleichbar sind
        names = list(groups)
        bpairs = list(itertools.combinations(names, 2))
        ga = np.array([names.index(a) for a, _ in bpairs])
        gb = np.array([names.index(b) for _, b in bpairs])
        S = B.values[:, ga] - B.values[:, gb]
        sd = np.nanstd(S[(ret.index <= pd.Timestamp(IS_END, tz="UTC"))], axis=0)
        S = S / sd
        open_frac = pd.DataFrame({g: mask[m].mean(axis=1) for g, m in groups.items()}).values
        enter = (open_frac[:, ga] >= 0.5) & (open_frac[:, gb] >= 0.5)
        pos = mr.hysteresis(S, enter, th, 0.0, H)
        Ub = np.zeros((len(ret), len(names)))
        np.add.at(Ub.T, ga, pos.T.astype(float))
        np.add.at(Ub.T, gb, -pos.T.astype(float))
        W = pd.DataFrame(0.0, index=ret.index, columns=keys)
        for g, m in groups.items():
            for a in m:
                W[a] += Ub[:, names.index(g)] * 0.03 / len(m) / vol[a]
        res = evaluate(W)
        rows.append({"family": "Korb gegen Korb", "indicator": ind, "theta": th, "hold_max_h": H, "entries_pa": entries_pa(pos), **mets(res)})
        store[("basket", ind, th, H)] = res
bk = pd.DataFrame(rows)

# ---------------------------------------------------------------- 4) Querschnitt
for ind in ["RSI14", "Z12", "Z24", "RES24"]:
    if ind not in IND:
        continue
    for k_, reb, H, neutral in itertools.product([3, 5], [4, 24], [24, 48], [False, True]):
        if QUICK and (k_ == 5 or reb == 4):
            continue
        W = mr.xs_reversal(IND[ind], mask, vol, k=k_ if not neutral else 1, rebalance=reb, hold=H, budget=0.03,
                           groups=groups if neutral else None)
        res = evaluate(W)
        bk = pd.concat([bk, pd.DataFrame([{"family": "Querschnitt" + (" klassenneutral" if neutral else ""), "indicator": ind,
                                           "k": k_ if not neutral else 1, "rebalance_h": reb, "hold_max_h": H, **mets(res)}])])
bk.to_csv(OUT / "baskets_xs_grid.csv", index=False)
log("Körbe/Querschnitt:", len(bk))

# ---------------------------------------------------------------- 5) Krypto-Funding-Extreme
rows = []
fund = {}
for k, sym in [("BTC", "BTCUSDT"), ("ETH", "ETHUSDT"), ("SOL", "SOLUSDT"), ("XRP", "XRPUSDT"), ("DOGE", "DOGEUSDT"),
               ("BNB", "BNBUSDT"), ("ADA", "ADAUSDT")]:
    f = ROOT / "data" / "raw" / "binance" / f"{sym}_funding.parquet"
    if f.exists() and k in keys:
        s = pd.read_parquet(f)["funding_rate"]
        s.index = s.index.floor("h")
        s = s[~s.index.duplicated()]
        fund[k] = s.reindex(ret.index).ffill(limit=8)
if fund:
    FR = pd.DataFrame(fund)
    FRz = (FR - FR.rolling(24 * 30, min_periods=24 * 10).mean()) / FR.rolling(24 * 30, min_periods=24 * 10).std()
    for th, H, combo in itertools.product([1.5, 2.0, 2.5], [12, 24, 48], ["nur Funding", "Funding + Preis"]):
        S = FRz.copy()
        if combo == "Funding + Preis":
            Zp = IND["Z24"][FR.columns]
            S = S.where((np.sign(S) == np.sign(Zp)) & (Zp.abs() > 1.5))   # Preis überhitzt UND Hebel überhitzt
        pos = mr.hysteresis(S.values, mask[FR.columns].values, th, 0.0, H)
        W = pd.DataFrame(pos, index=ret.index, columns=FR.columns) * 0.05 / vol[FR.columns]
        res = evaluate(W)
        rows.append({"family": "Krypto-Funding", "variant": combo, "theta": th, "hold_max_h": H, "entries_pa": entries_pa(pos), **mets(res)})
        # relativ: Coin mit überhitztem Funding short gegen BTC long (marktneutral)
        if combo == "nur Funding":
            alts = [c for c in FR.columns if c != "BTC"]
            pos2 = mr.hysteresis((FRz[alts].values - FRz[["BTC"]].values) / np.sqrt(2), mask[alts].values, th, 0.0, H)
            W2 = pd.DataFrame(0.0, index=ret.index, columns=list(FR.columns))
            for j, a in enumerate(alts):
                W2[a] += pos2[:, j] * 0.02 / vol[a]
                W2["BTC"] -= pos2[:, j] * 0.02 / vol["BTC"]
            rows.append({"family": "Krypto-Funding relativ zu BTC", "variant": combo, "theta": th, "hold_max_h": H, **mets(evaluate(W2))})
fu = pd.DataFrame(rows)
fu.to_csv(OUT / "funding_grid.csv", index=False)
log("Funding:", len(fu))

# ---------------------------------------------------------------- 6) Konditionierung: Stressregime
spx_vol = flow.realized_daily_vol(ret[["SPX"]])["SPX"]
hi = (spx_vol > spx_vol.rolling(24 * 250, min_periods=24 * 60).median()).values
rows = []
for ind, th, H in [("Z24", 2.5, 48), ("RSI14", 0.6, 24), ("Z12", 2.5, 24), ("RES24", 2.5, 24)]:
    if ind not in IND:
        continue
    for cond in ["keine", "Stress (Vol hoch)", "ruhig (Vol niedrig)"]:
        ok = Mv if cond == "keine" else (Mv & hi[:, None] if cond.startswith("Stress") else Mv & ~hi[:, None])
        pos = mr.hysteresis(IND[ind].values, ok, th, 0.0, H)
        W = pd.DataFrame(pos, index=ret.index, columns=keys) * 0.05 / vol
        for side, Ws in [("beide", W), ("nur long", W.clip(lower=0)), ("nur short", W.clip(upper=0))]:
            rows.append({"indicator": ind, "theta": th, "hold_max_h": H, "condition": cond, "side": side, **mets(evaluate(Ws))})
# Klasse × Richtung (z. B. 'Aktienindizes nur long' = Dip-Kauf)
for ind, th, H in [("Z24", 2.5, 48), ("RSI48", 0.3, 48), ("RSI14", 0.6, 24), ("Z12", 2.5, 24)]:
    if ind not in IND:
        continue
    pos = mr.hysteresis(IND[ind].values, Mv, th, 0.0, H)
    W = pd.DataFrame(pos, index=ret.index, columns=keys) * 0.05 / vol
    for g, mem in groups.items():
        for side, Ws in [("beide", W[mem]), ("nur long", W[mem].clip(lower=0)), ("nur short", W[mem].clip(upper=0))]:
            for cond in ["keine", "Stress (Vol hoch)"]:
                Wc = Ws if cond == "keine" else Ws.where(pd.Series(hi, index=ret.index), 0.0)
                rows.append({"indicator": ind, "theta": th, "hold_max_h": H, "condition": cond, "side": side, "class": g,
                             **mets(evaluate(Wc))})
cd = pd.DataFrame(rows)
cd.to_csv(OUT / "conditioning.csv", index=False)
log("Konditionierung:", len(cd))

# ---------------------------------------------------------------- 7) Gesamtauswahl, Placebo, Deflated Sharpe
allg = pd.concat([ts.assign(fam=ts.family), pp.assign(fam="Paare " + pp.scope), bk.assign(fam=bk.family), fu.assign(fam=fu.family)],
                 ignore_index=True)
allg.to_csv(OUT / "all_trials.csv", index=False)
n_trials = int(allg["Sharpe_IS"].notna().sum())
best_by_fam = {}
for fam, df in allg.groupby("fam"):
    b = df.sort_values("Sharpe_IS", ascending=False).iloc[0]
    best_by_fam[fam] = {k: (float(v) if isinstance(v, (np.floating, np.integer)) else v) for k, v in b.items() if pd.notna(v)}
json.dump(best_by_fam, open(OUT / "best_by_family.json", "w"), indent=1, default=str)
summary = {"n_trials": n_trials, "share_IS_positive": float((allg.Sharpe_IS > 0).mean()),
           "share_OOS_positive": float((allg.Sharpe_OOS > 0).mean()),
           "share_both_positive": float(((allg.Sharpe_IS > 0) & (allg.Sharpe_OOS > 0)).mean()),
           "corr_IS_OOS": float(allg[["Sharpe_IS", "Sharpe_OOS"]].corr().iloc[0, 1]),
           "mean_brutto": float(allg.Sharpe_brutto_ALL.mean())}

# Deflated Sharpe für die beste Paar-Konfiguration (tägliche Renditen)
res_best = store[("pair", bp.indicator, bp.scope, bp.theta, int(bp.hold_max_h))][0]
d_best = bt.daily(res_best)
sr_trials = allg["Sharpe_ALL"].dropna().values / np.sqrt(252)
summary["DSR_best_pair"] = deflated_sharpe(d_best.values, sr_trials)

# Placebo: Paar-Signale zeitlich zufällig verschoben (gleiche Häufigkeit/Haltedauer, echte Kosten)
rng = np.random.default_rng(11)
_, pos, ia, ib = store[("pair", bp.indicator, bp.scope, bp.theta, int(bp.hold_max_h))]
plc = []
for i in range(0 if QUICK else 40):
    shift = rng.integers(24 * 30, len(pos) - 24 * 30, size=pos.shape[1])
    posr = np.stack([np.roll(pos[:, j], shift[j]) for j in range(pos.shape[1])], axis=1)
    Uu = np.zeros((len(ret), len(keys)))
    np.add.at(Uu.T, ia, posr.T.astype(float))
    np.add.at(Uu.T, ib, -posr.T.astype(float))
    W = pd.DataFrame(Uu, index=ret.index, columns=keys) * 0.01 / vol
    plc.append(bt.metrics(evaluate(W))["Sharpe"])
if plc:
    real = bt.metrics(res_best)["Sharpe"]
    summary["placebo_best_pair"] = {"real": float(real), "placebo_mean": float(np.mean(plc)), "placebo_p95": float(np.percentile(plc, 95)),
                                    "pctl": float(np.mean(np.array(plc) < real))}
json.dump(summary, open(OUT / "summary.json", "w"), indent=1, default=float)
log("Zusammenfassung:", summary)

# Kurven der besten Variante je Familie (IS-Auswahl) für Grafiken
curves = {}
for fam_key, key in [("Einzelasset", None), ("Paare", None), ("Korb gegen Korb", None)]:
    pass
bts = ts[ts.family == "Einzelasset"].sort_values("Sharpe_IS", ascending=False).iloc[0]
curves["Einzelasset (bestes IS-Setup)"] = bt.daily(store[("ts", bts.indicator, bts.theta, int(bts.hold_max_h))]).cumsum()
curves["Paare (bestes IS-Setup)"] = bt.daily(res_best).cumsum()
curves["Paare (bestes IS-Setup) brutto"] = bt.daily(res_best, "gross").cumsum()
bkb = bk[bk.family == "Korb gegen Korb"].sort_values("Sharpe_IS", ascending=False).iloc[0]
curves["Korb gegen Korb (bestes IS-Setup)"] = bt.daily(store[("basket", bkb.indicator, bkb.theta, int(bkb.hold_max_h))]).cumsum()
pd.DataFrame(curves).to_csv(OUT / "equity_curves_best.csv")
log("FERTIG")
