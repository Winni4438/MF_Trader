"""Hauptexperiment: Intraday-Rotationserkennung und -handel auf Stundenbasis (2019–2026).

Ergebnisse -> results/hourly/
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
from mf_trader import backtest as bt  # noqa: E402
from mf_trader import flow, regime  # noqa: E402
from mf_trader.data.panel import build_hourly, load_hourly, save_hourly  # noqa: E402
from mf_trader.strategies import RotationParams, pair_follow, rotation_follower, xs_momentum  # noqa: E402
from mf_trader.universe import BY_KEY, HAVEN, RISK  # noqa: E402

OUT = ROOT / "results" / "hourly"
OUT.mkdir(parents=True, exist_ok=True)
IS_END = "2022-12-31"
START = "2019-07-01"  # nach Aufwärmphase der rollierenden Schätzer
t_start = time.time()


def log(*a):
    print(f"[{time.time()-t_start:6.0f}s]", *a, flush=True)


# ---------------------------------------------------------------- Daten & Features
if "--rebuild" in sys.argv or not (ROOT / "data/processed/hourly_close.parquet").exists():
    save_hourly(build_hourly("2019-01-01", "2026-10-01"))
P = load_hourly()
ret, mask = P["ret"], P["mask"]
assets = list(ret.columns)
risk = [a for a in RISK if a in assets]
haven = [a for a in HAVEN if a in assets]
log("Assets:", assets)

svar = flow.seasonal_var(ret)
WINDOWS = [1, 2, 4, 8]
F = {w: flow.flow_score(ret, svar, w) for w in WINDOWS}
RZ = {w: flow.standardize(flow.roro(F[w], risk, haven)) for w in WINDOWS}
vol = flow.realized_daily_vol(ret)
stress = bt.stress_multiplier(ret)
BR = {w: flow.breadth(F[w], risk, haven) for w in WINDOWS}
log("Features fertig")

# Tagesregime
dret = regime.daily_close_returns(ret)
sbc = regime.stock_bond_corr(dret, "SPX", "UST") if "UST" in dret else None
droro = regime.daily_roro(dret, risk, haven)
droro20 = droro.rolling(20, min_periods=10).sum()
tr_ok = regime.trend_ok(dret, 20)
allow_off_trend = regime.to_hourly(droro20 < 0, ret.index).astype(bool)
allow_on_trend = regime.to_hourly(droro20 > 0, ret.index).astype(bool)
haven_trend_ok = regime.to_hourly(tr_ok, ret.index).astype(bool)
if sbc is not None:
    bonds_ok = regime.to_hourly(sbc < 0, ret.index).fillna(True).astype(bool)
    haven_sbc_ok = pd.DataFrame(True, index=ret.index, columns=assets)
    for b in ("UST", "BUND"):
        if b in assets:
            haven_sbc_ok[b] = bonds_ok
else:
    haven_sbc_ok = None
ny_h = pd.Series(ret.index.tz_convert("America/New_York").hour, index=ret.index)
ny_wd = pd.Series(ret.index.tz_convert("America/New_York").dayofweek, index=ret.index)
us_sess = ((ny_h >= 9) & (ny_h <= 14) & (ny_wd < 5))  # Einstiege 9:00–14:59 New York
FILTERS = {
    "keiner": dict(),
    "US-Sitzung": dict(allow_off=us_sess, allow_on=us_sess),
    "Hafen-Trend": dict(haven_ok=haven_trend_ok),
    "Aktien-Anleihe-Korr": dict(haven_ok=haven_sbc_ok),
    "Tages-RORO-Trend": dict(allow_off=allow_off_trend, allow_on=allow_on_trend),
}


def evaluate(target, delay=0, cost_mult=1.0, start=START, end=None):
    res = bt.run(target, P, delay=delay, cost_mult=cost_mult, stress=stress)
    res = res.loc[start:end]
    return res


def split_metrics(res):
    return {"IS": bt.metrics(res.loc[:IS_END]), "OOS": bt.metrics(res.loc[pd.Timestamp(IS_END, tz="UTC") + pd.Timedelta(days=1):]),
            "ALL": bt.metrics(res)}


def run_rf(p: RotationParams, filt: str = "keiner"):
    tgt, trades = rotation_follower(p, F[p.window], RZ[p.exit_window], RZ[p.window], vol, mask,
                                    BR[p.window], **FILTERS[filt])
    return tgt, trades


# ---------------------------------------------------------------- 1) Ereignisstudie
log("Ereignisstudie")
H = 48
fwd = {h: ret.shift(-1).rolling(h, min_periods=1).sum().shift(-(h - 1)) for h in range(1, H + 1)}
base = {h: fwd[h].loc[START:].mean() for h in fwd}  # unbedingte Durchschnittsrendite (Drift)


def event_study(trig: pd.Series, name: str):
    t_idx = trig[trig].index
    rows = []
    for h in [1, 2, 4, 8, 12, 24, 48]:
        x = fwd[h].reindex(t_idx)
        ex_ = x - base[h]
        rows.append(pd.DataFrame({"h": h, "asset": x.columns, "mean_bps": x.mean().values * 1e4,
                                  "excess_bps": ex_.mean().values * 1e4,
                                  "t_excess": (ex_.mean() / ex_.std() * np.sqrt(ex_.count())).values,
                                  "hit": (x > 0).mean().values, "n": x.count().values}))
    df = pd.concat(rows)
    df["trigger"] = name
    return df

ev_tables = []
for w in [2, 4, 8]:
    for th in [2.0, 3.0, 4.0]:
        z = RZ[w]
        off = (z <= -th) & ~(z.shift(1) <= -th)  # erstes Überschreiten
        off = off & ~off.rolling(12, min_periods=1).sum().shift(1).fillna(0).astype(bool)
        on = (z >= th) & ~(z.shift(1) >= th)
        on = on & ~on.rolling(12, min_periods=1).sum().shift(1).fillna(0).astype(bool)
        ev_tables.append(event_study(off.loc[START:], f"riskoff_w{w}_z{th}"))
        ev_tables.append(event_study(on.loc[START:], f"riskon_w{w}_z{th}"))
# Aufteilung nach Handelssitzung und Aktien-Anleihe-Regime (w=4, z=2.5)
z4 = RZ[4]
off4 = ((z4 <= -2.5) & ~(z4.shift(1) <= -2.5)).loc[START:]
on4 = ((z4 >= 2.5) & ~(z4.shift(1) >= 2.5)).loc[START:]
hr = off4.index.hour
sess = pd.Series(np.where((hr >= 23) | (hr < 7), "Asien", np.where(hr < 13, "Europa", "USA")), index=off4.index)
for sname in ["Asien", "Europa", "USA"]:
    ev_tables.append(event_study(off4 & (sess == sname), f"riskoff_w4_z2.5_{sname}"))
    ev_tables.append(event_study(on4 & (sess == sname), f"riskon_w4_z2.5_{sname}"))
if sbc is not None:
    neg = regime.to_hourly(sbc < 0, ret.index).fillna(False).astype(bool).loc[START:]
    ev_tables.append(event_study(off4 & neg, "riskoff_w4_z2.5_Korr<0"))
    ev_tables.append(event_study(off4 & ~neg, "riskoff_w4_z2.5_Korr>=0"))
    ev_tables.append(event_study(on4 & neg, "riskon_w4_z2.5_Korr<0"))
    ev_tables.append(event_study(on4 & ~neg, "riskon_w4_z2.5_Korr>=0"))
ev = pd.concat(ev_tables)
ev.to_csv(OUT / "event_study.csv", index=False)
# Pfade für Grafik (w=4, z=2.5)
z = RZ[4]
off = (z <= -2.5) & ~(z.shift(1) <= -2.5)
on = (z >= 2.5) & ~(z.shift(1) >= 2.5)
paths = {}
for nm, trig in [("riskoff", off.loc[START:]), ("riskon", on.loc[START:])]:
    t_idx = trig[trig].index
    pre = {-h: -ret.rolling(h).sum().shift(-h + 1).shift(h - 1).reindex(t_idx).mean() * 0 for h in []}
    m = pd.DataFrame({h: fwd[h].reindex(t_idx).mean() - base[h] for h in range(1, H + 1)}).T * 1e4
    back = pd.DataFrame({-h: -(ret.rolling(h).sum().reindex(t_idx).mean()) * 1e4 for h in range(1, 13)}).T
    m.loc[0] = 0.0
    paths[nm] = pd.concat([back, m]).sort_index()
    paths[nm].to_csv(OUT / f"event_path_{nm}.csv")
    log(nm, "Ereignisse:", len(t_idx))

# ---------------------------------------------------------------- 2) Parametergitter Rotation Follower (In-Sample)
log("Gitter Rotation Follower")
grid = []
QUICK = "--quick" in sys.argv
G = dict(w=[2, 4, 8], th=[2.0, 2.5, 3.0], mh=[4, 8, 24], ex=[1, 2], src=[0, 2], eod=[True, False], f=list(FILTERS))
if QUICK:
    G = dict(w=[4], th=[2.5], mh=[8], ex=[2], src=[0, 2], eod=[True], f=["keiner", "Hafen-Trend"])
for w, th, mh, exitw, src_k, eod, filt in itertools.product(G["w"], G["th"], G["mh"], G["ex"], G["src"], G["eod"], G["f"]):
    if not eod and mh < 8:
        continue
    p = RotationParams(window=w, theta=th, max_hold=mh, exit_window=exitw, src_k=src_k, eod_flat=eod)
    tgt, trades = run_rf(p, filt)
    res = evaluate(tgt)
    m = split_metrics(res)
    grid.append({"window": w, "theta": th, "max_hold": mh, "exit_window": exitw, "src_k": src_k,
                 "eod_flat": eod, "filter": filt,
                 **{f"{k}_{s}": v for s in ("IS", "OOS", "ALL") for k, v in m[s].items()}})
grid = pd.DataFrame(grid)
grid.to_csv(OUT / "grid_rotation_follower.csv", index=False)
log("Gitter:", len(grid), "Kombinationen")

# robuste Auswahl: beste IS-Sharpe mit Mindestanzahl Trades
cand = grid[grid["Trades_IS"] >= 30].sort_values("Sharpe_IS", ascending=False)
best = cand.iloc[0].to_dict()
log("Beste IS-Konfiguration:", {k: best[k] for k in ["window", "theta", "max_hold", "exit_window", "src_k", "eod_flat", "filter", "Sharpe_IS", "Sharpe_OOS"]})
json.dump({k: (v if not isinstance(v, (np.floating, np.integer)) else float(v)) for k, v in best.items()},
          open(OUT / "best_is_config.json", "w"), indent=2, default=str)

# ---------------------------------------------------------------- 3) Referenz-Konfigurationen
log("Referenzvarianten")
REF = {
    "RF Basis (long Ziel, 4h, z2.5, EOD)": (RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2), "keiner"),
    "RF + Short Quelle": (RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2, src_k=2), "keiner"),
    "RF nur Risk-off": (RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2, direction="off"), "keiner"),
    "RF nur Risk-on": (RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2, direction="on"), "keiner"),
    "Nutzer-Idee: Gold+Bonds long / BTC+NDX short": (RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2, direction="off",
                                                    fixed_dest_off=["GOLD", "UST"], fixed_src_off=["BTC", "NDX"]), "keiner"),
    "RF + Tages-RORO-Trend": (RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2), "Tages-RORO-Trend"),
    "RF + Hafen-Trend": (RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2), "Hafen-Trend"),
    "RF + Aktien-Anleihe-Korr": (RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2), "Aktien-Anleihe-Korr"),
    "RF nur US-Sitzung": (RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2), "US-Sitzung"),
    "RF Risk-off nur US-Sitzung": (RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2, direction="off"), "US-Sitzung"),
    "RF Risk-off US-Sitzung + Short Quelle": (RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2, direction="off", src_k=2), "US-Sitzung"),
    "IS-Optimum": (RotationParams(window=int(best["window"]), theta=float(best["theta"]), max_hold=int(best["max_hold"]),
                                  exit_window=int(best["exit_window"]), src_k=int(best["src_k"]), eod_flat=bool(best["eod_flat"])), best["filter"]),
}
ref_rows, curves, trade_logs = [], {}, {}
for name, (p, filt) in REF.items():
    tgt, trades = run_rf(p, filt)
    res = evaluate(tgt)
    m = split_metrics(res)
    ref_rows.append({"Strategie": name, **{f"{k}_{s}": v for s in ("IS", "OOS", "ALL") for k, v in m[s].items()}})
    curves[name] = bt.daily(res).cumsum()
    curves[name + " (brutto)"] = bt.daily(res, "gross").cumsum()
    trades["strategy"] = name
    trade_logs[name] = trades
pd.DataFrame(ref_rows).to_csv(OUT / "reference_strategies.csv", index=False)
pd.DataFrame(curves).to_csv(OUT / "equity_curves_daily_cum.csv")
pd.concat(trade_logs.values()).to_csv(OUT / "trades_reference.csv", index=False)

# ---------------------------------------------------------------- 3b) Gegenhalten statt Folgen
log("Fader-Gitter")
from mf_trader.strategies import FadeParams, rotation_fader  # noqa: E402
fg = []
fade_targets = {}
for w, th, wait, hold, hedge, dirn in itertools.product([4], [2.5, 3.0], [0, 1, 2, 4], [4, 8, 24], [False, True], ["off", "on", "both"]):
    fp = FadeParams(window=w, theta=th, wait=wait, hold=hold, hedge=hedge, direction=dirn)
    tgt, tl = rotation_fader(fp, F[w], RZ[w], vol, mask)
    res = evaluate(tgt)
    m = split_metrics(res)
    fg.append({"theta": th, "wait": wait, "hold": hold, "hedge": hedge, "direction": dirn,
               "Sharpe_brutto_ALL": bt.metrics(res, "gross")["Sharpe"],
               **{f"{k}_{s_}": v for s_ in ("IS", "OOS", "ALL") for k, v in m[s_].items()}})
fg = pd.DataFrame(fg)
fg.to_csv(OUT / "grid_fader.csv", index=False)
fb = fg[fg["Trades_IS"] >= 30].sort_values("Sharpe_IS", ascending=False).iloc[0]
log("Bester Fader IS:", fb[["theta", "wait", "hold", "hedge", "direction", "Sharpe_IS", "Sharpe_OOS"]].to_dict())
fpb = FadeParams(window=4, theta=float(fb["theta"]), wait=int(fb["wait"]), hold=int(fb["hold"]), hedge=bool(fb["hedge"]), direction=fb["direction"])
tgt_f, _ = rotation_fader(fpb, F[4], RZ[4], vol, mask)
res_f = evaluate(tgt_f)
mf = split_metrics(res_f)
ref_rows.append({"Strategie": "Gegenhalten (IS-Optimum)", **{f"{k}_{s_}": v for s_ in ("IS", "OOS", "ALL") for k, v in mf[s_].items()}})
pd.DataFrame(ref_rows).to_csv(OUT / "reference_strategies.csv", index=False)
curves["Gegenhalten (IS-Optimum)"] = bt.daily(res_f).cumsum()
curves["Gegenhalten (IS-Optimum) (brutto)"] = bt.daily(res_f, "gross").cumsum()
pd.DataFrame(curves).to_csv(OUT / "equity_curves_daily_cum.csv")

# ---------------------------------------------------------------- 3c) Placebo-Tests (zufällige Zeitpunkte)
log("Placebo-Tests")
rng = np.random.default_rng(42)


def placebo_trigger(n_events: int, allowed: pd.Series | None = None) -> pd.Series:
    pool = ret.loc[START:].index
    if allowed is not None:
        pool = pool[allowed.reindex(pool).fillna(False).values]
    pick = rng.choice(len(pool), size=n_events, replace=False)
    z = pd.Series(0.0, index=ret.index)
    z.loc[pool[pick]] = -10.0  # als 'Risk-off' markiert
    return z


plc = []
n_off_events = int(((RZ[4] <= -float(fb["theta"])) & ~(RZ[4].shift(1) <= -float(fb["theta"]))).loc[START:].sum())
for i in range(200):
    zr = placebo_trigger(n_off_events)
    tgt, _ = rotation_fader(FadeParams(window=4, theta=1.0, wait=int(fb["wait"]), hold=int(fb["hold"]),
                                       hedge=bool(fb["hedge"]), direction="off"), F[4], zr, vol, mask)
    plc.append({"test": "Gegenhalten", "i": i, "Sharpe": bt.metrics(evaluate(tgt))["Sharpe"]})
# Placebo für den Folger mit US-Sitzung (Long-Ziel, Risk-off): zufällige US-Stunden
p_us = RotationParams(window=4, theta=2.5, max_hold=8, exit_window=2, direction="off")
tgt_us, tr_us = run_rf(p_us, "US-Sitzung")
real_us = bt.metrics(evaluate(tgt_us))["Sharpe"]
n_us = len(tr_us)
for i in range(200):
    zr = placebo_trigger(n_us, us_sess)
    tgt, _ = rotation_follower(RotationParams(window=4, theta=5.0, max_hold=8, exit_window=2, direction="off"),
                               F[4], RZ[2], zr, vol, mask, BR[4])
    plc.append({"test": "Folgen US-Sitzung (Risk-off)", "i": i, "Sharpe": bt.metrics(evaluate(tgt))["Sharpe"]})
plc = pd.DataFrame(plc)
plc.to_csv(OUT / "placebo.csv", index=False)
summary_placebo = {
    "Gegenhalten": {"real": float(mf["ALL"]["Sharpe"]), "placebo_mean": float(plc[plc.test == "Gegenhalten"].Sharpe.mean()),
                    "pctl": float((plc[plc.test == "Gegenhalten"].Sharpe < mf["ALL"]["Sharpe"]).mean())},
    "Folgen US-Sitzung (Risk-off)": {"real": float(real_us), "placebo_mean": float(plc[plc.test != "Gegenhalten"].Sharpe.mean()),
                                    "pctl": float((plc[plc.test != "Gegenhalten"].Sharpe < real_us).mean())},
}
json.dump(summary_placebo, open(OUT / "placebo_summary.json", "w"), indent=2)
log("Placebo:", summary_placebo)

# ---------------------------------------------------------------- 4) Verzögerung & Kosten
log("Latenz/Kosten")
p0, f0 = REF["RF Basis (long Ziel, 4h, z2.5, EOD)"]
tgt0, _ = run_rf(p0, f0)
lat = []
for dly in [0, 1, 2, 3, 4]:
    for cm in [0.0, 1.0, 2.0]:
        m = bt.metrics(evaluate(tgt0, delay=dly, cost_mult=cm))
        lat.append({"delay_h": dly, "cost_mult": cm, **m})
pd.DataFrame(lat).to_csv(OUT / "latency_cost_sensitivity.csv", index=False)

# ---------------------------------------------------------------- 5) Querschnitts-Flow-Momentum
log("XS-Momentum")
xs = []
for w, hold, k in itertools.product([1, 2, 4, 8, 24], [1, 2, 4, 8, 24], [2, 3]):
    Fw = F[w] if w in F else flow.flow_score(ret, svar, w)
    tgt = xs_momentum(Fw.where(mask), vol, k=k, hold=hold)
    m = split_metrics(evaluate(tgt))
    xs.append({"window": w, "hold": hold, "k": k, **{f"{kk}_{s}": v for s in ("IS", "OOS", "ALL") for kk, v in m[s].items()},
               "Sharpe_brutto_ALL": bt.metrics(evaluate(tgt), "gross")["Sharpe"]})
pd.DataFrame(xs).to_csv(OUT / "grid_xs_momentum.csv", index=False)

# ---------------------------------------------------------------- 6) Paar-Matrix: welche Rotation lohnt sich?
log("Paar-Matrix")
pairs = []
for a, b in itertools.permutations(assets, 2):
    if a > b:
        continue
    for w, hold in [(4, 4), (8, 8)]:
        s = pair_follow(F[w][a], F[w][b], 2.0, hold)
        tgt = pd.DataFrame(0.0, index=ret.index, columns=[a, b])
        tgt[a] = s * 0.05 / vol[a]
        tgt[b] = -s * 0.05 / vol[b]
        res = evaluate(tgt.fillna(0.0))
        mg = bt.metrics(res, "gross")
        mn = bt.metrics(res, "net")
        pairs.append({"A": a, "B": b, "window": w, "hold": hold, "Sharpe_brutto": mg["Sharpe"], "Sharpe_netto": mn["Sharpe"],
                      "Trades_pa": mn["Trades_pa"], "AvgTrade_bps_brutto": mg["AvgTrade_bps"],
                      "Sharpe_netto_IS": bt.metrics(res.loc[:IS_END])["Sharpe"],
                      "Sharpe_netto_OOS": bt.metrics(res.loc["2023-01-01":])["Sharpe"]})
pd.DataFrame(pairs).to_csv(OUT / "pair_matrix.csv", index=False)

# ---------------------------------------------------------------- 7) Intraday-Momentum (Gao/Baltussen) je Asset
log("Intraday-Momentum letzte Stunde")
ny = ret.index.tz_convert("America/New_York")
im = []
for a in assets:
    r = ret[a]
    day = pd.Series(ny.normalize().tz_localize(None), index=ret.index)
    # Rendite von 16:00 ET Vortag bis 15:00 ET (Bars 16..23 Vortag + 0..14) -> rollierende 23h-Summe am 14:00-Bar
    s23 = r.rolling(23, min_periods=10).sum()
    sig_t = s23[(ny.hour == 14) & (ny.dayofweek < 5)]
    last = r.shift(-1)[(ny.hour == 14) & (ny.dayofweek < 5)]  # Rendite des 15:00-16:00-Bars
    df = pd.DataFrame({"sig": sig_t, "last": last}).dropna()
    df = df[df.index >= START]
    pnl = np.sign(df["sig"]) * df["last"] - 2 * BY_KEY[a].cost_bps / 1e4
    gross = np.sign(df["sig"]) * df["last"]
    im.append({"asset": a, "n": len(df), "corr": df["sig"].corr(df["last"]),
               "mean_bps_brutto": gross.mean() * 1e4, "mean_bps_netto": pnl.mean() * 1e4,
               "Sharpe_brutto": gross.mean() / gross.std() * np.sqrt(252), "Sharpe_netto": pnl.mean() / pnl.std() * np.sqrt(252),
               "Sharpe_netto_OOS": pnl.loc["2023":].mean() / pnl.loc["2023":].std() * np.sqrt(252)})
pd.DataFrame(im).to_csv(OUT / "intraday_momentum_last_hour.csv", index=False)

# ---------------------------------------------------------------- 8) Krypto als Frühindikator / Orderflow
log("Krypto-Extras")
ex = {}
if "BTC" in assets:
    # Wochenend-BTC -> Montagseröffnung Nasdaq/S&P (Sonntag 22/23 UTC Reopen-Bar)
    wk = []
    for fri in pd.date_range(START, "2026-09-25", freq="W-FRI", tz="UTC"):
        fri_close = fri + pd.Timedelta(hours=21)
        sun_open = fri_close + pd.Timedelta(hours=49)  # So 22:00 UTC
        btc_we = ret["BTC"].loc[fri_close:sun_open - pd.Timedelta(hours=1)].sum()
        for a in ["NDX", "SPX", "NKY", "GOLD"]:
            if a not in assets:
                continue
            seg = ret[a].loc[sun_open - pd.Timedelta(hours=1): sun_open + pd.Timedelta(hours=2)]
            gap = seg.sum()
            rest = ret[a].loc[sun_open + pd.Timedelta(hours=3): sun_open + pd.Timedelta(hours=22)].sum()
            wk.append({"week": fri.date(), "asset": a, "btc_weekend": btc_we, "gap": gap, "after_gap": rest})
    wk = pd.DataFrame(wk)
    wk.to_csv(OUT / "btc_weekend_vs_monday.csv", index=False)
    ex["weekend_corr_gap"] = wk.groupby("asset").apply(lambda d: d["btc_weekend"].corr(d["gap"])).to_dict()
    ex["weekend_corr_after_gap"] = wk.groupby("asset").apply(lambda d: d["btc_weekend"].corr(d["after_gap"])).to_dict()
    # Taker-Buy-Imbalance -> nächste Stunde
    tk = P["extra"].get("BTC_taker_ratio")
    if tk is not None:
        imb = (tk - 0.5)
        zimb = (imb - imb.rolling(24 * 30).mean()) / imb.rolling(24 * 30).std()
        nxt = ret.shift(-1)
        ex["taker_imbalance_corr_next_hour"] = {a: float(zimb.loc[START:].corr(nxt[a].loc[START:])) for a in ["BTC", "ETH", "NDX", "SPX"] if a in assets}
        ex["taker_imbalance_corr_same_hour_BTC"] = float(zimb.loc[START:].corr(ret["BTC"].loc[START:]))
    # Lead-Lag BTC(t) -> NDX(t+1) während US-Handelszeit
    us = (ny.hour >= 10) & (ny.hour <= 15) & (ny.dayofweek < 5)
    ex["btc_lead_ndx_next_hour_corr"] = float(ret["BTC"][us].corr(ret["NDX"].shift(-1)[us]))
    ex["ndx_lead_btc_next_hour_corr"] = float(ret["NDX"][us].corr(ret["BTC"].shift(-1)[us]))
json.dump(ex, open(OUT / "crypto_extras.json", "w"), indent=2, default=str)

# ---------------------------------------------------------------- 9) Episoden & Häufigkeit
log("Häufigkeiten")
freq = []
z = RZ[4]
for y in range(2019, 2027):
    zz = z.loc[str(y)]
    off = ((zz <= -2.5) & ~(zz.shift(1) <= -2.5)).sum()
    on = ((zz >= 2.5) & ~(zz.shift(1) >= 2.5)).sum()
    freq.append({"Jahr": y, "Risk-off-Signale": int(off), "Risk-on-Signale": int(on)})
pd.DataFrame(freq).to_csv(OUT / "signal_frequency.csv", index=False)
# Stärkste Stunden-Rotationen
top = z.loc[START:].dropna()
top_off = top.nsmallest(400)
picked = []
for t, v in top_off.items():
    if all(abs((t - p).total_seconds()) > 3 * 86400 for p, _ in picked):
        picked.append((t, v))
    if len(picked) >= 15:
        break
rows = []
for t, v in picked:
    r4 = ret.loc[t - pd.Timedelta(hours=3): t].sum() * 100
    r_next = ret.loc[t + pd.Timedelta(hours=1): t + pd.Timedelta(hours=8)].sum() * 100
    rows.append({"Zeit_UTC": t, "RORO_z": v, **{f"{a}_4h%": r4[a] for a in assets}, **{f"{a}_next8h%": r_next[a] for a in assets}})
pd.DataFrame(rows).to_csv(OUT / "top_riskoff_hours.csv", index=False)
log("FERTIG")
