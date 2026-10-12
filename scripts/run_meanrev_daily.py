"""Mean Reversion / Überhitzung auf Tagesbasis (2007–2026), Haltedauer ≤ 2 Tage.

Universum: ~55 ETFs (Aktienindizes, Sektoren, Länder, Anleihen, Kredit, Rohstoffe, Edelmetalle,
Währungen, REITs) + Krypto (BTC/ETH/SOL/... aus Binance-Stundendaten, Schluss um 16:00 New York).
Ergebnisse -> results/meanrev_daily/
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
from mf_trader.meanrev import hysteresis  # noqa: E402

OUT = ROOT / "results" / "meanrev_daily"
OUT.mkdir(parents=True, exist_ok=True)
RAW = ROOT / "data" / "raw"
T0 = time.time()


def log(*a):
    print(f"[{time.time()-T0:6.0f}s]", *a, flush=True)


# key: (Quelle/Ticker, Klasse, Kosten bps je Seite)
U = {
    "SPY": ("SPY", "Aktien USA", 0.5), "QQQ": ("QQQ", "Aktien USA", 1), "IWM": ("IWM", "Aktien USA", 1.5),
    "VGK": ("VGK", "Aktien intl.", 3), "EWJ": ("EWJ", "Aktien intl.", 3), "EEM": ("EEM", "Aktien intl.", 2),
    "FXI": ("FXI", "Aktien intl.", 3), "EWZ": ("EWZ", "Aktien intl.", 3), "EWG": ("EWG", "Aktien intl.", 3),
    "EWU": ("EWU", "Aktien intl.", 3), "EWY": ("EWY", "Aktien intl.", 3), "EWA": ("EWA", "Aktien intl.", 3),
    "EWC": ("EWC", "Aktien intl.", 3), "EWW": ("EWW", "Aktien intl.", 3), "EFA": ("EFA", "Aktien intl.", 2),
    "XLK": ("XLK", "Sektoren", 2), "XLF": ("XLF", "Sektoren", 2), "XLE": ("XLE", "Sektoren", 2),
    "XLV": ("XLV", "Sektoren", 2), "XLI": ("XLI", "Sektoren", 2), "XLY": ("XLY", "Sektoren", 2),
    "XLP": ("XLP", "Sektoren", 2), "XLU": ("XLU", "Sektoren", 2), "XLB": ("XLB", "Sektoren", 2),
    "SMH": ("SMH", "Sektoren", 3), "XBI": ("XBI", "Sektoren", 3), "XME": ("XME", "Sektoren", 3),
    "GDX": ("GDX", "Sektoren", 3), "VNQ": ("VNQ", "Sektoren", 2),
    "SHY": ("SHY", "Anleihen", 1), "IEF": ("IEF", "Anleihen", 1.5), "TLT": ("TLT", "Anleihen", 1.5),
    "TIP": ("TIP", "Anleihen", 2), "LQD": ("LQD", "Anleihen", 2), "HYG": ("HYG", "Anleihen", 2),
    "EMB": ("EMB", "Anleihen", 3), "BWX": ("BWX", "Anleihen", 4), "MUB": ("MUB", "Anleihen", 3),
    "GLD": ("GLD", "Edelmetalle", 1.5), "SLV": ("SLV", "Edelmetalle", 3), "PPLT": ("PPLT", "Edelmetalle", 6),
    "USO": ("USO", "Rohstoffe", 3), "UNG": ("UNG", "Rohstoffe", 4), "DBA": ("DBA", "Rohstoffe", 5),
    "DBB": ("DBB", "Rohstoffe", 6), "DBC": ("DBC", "Rohstoffe", 4), "CPER": ("CPER", "Rohstoffe", 8),
    "WEAT": ("WEAT", "Rohstoffe", 8), "CORN": ("CORN", "Rohstoffe", 8),
    "UUP": ("UUP", "Währungen", 3), "FXE": ("FXE", "Währungen", 3), "FXB": ("FXB", "Währungen", 4),
    "FXY": ("FXY", "Währungen", 4), "FXF": ("FXF", "Währungen", 5), "FXA": ("FXA", "Währungen", 4),
    "FXC": ("FXC", "Währungen", 4),
    "BTC": ("BTCUSDT", "Krypto", 10), "ETH": ("ETHUSDT", "Krypto", 10), "SOL": ("SOLUSDT", "Krypto", 12),
    "XRP": ("XRPUSDT", "Krypto", 12), "BNB": ("BNBUSDT", "Krypto", 12), "ADA": ("ADAUSDT", "Krypto", 12),
    "DOGE": ("DOGEUSDT", "Krypto", 12),
}

# ---------------------------------------------------------------- Daten
O_, H_, L_, C_ = {}, {}, {}, {}
for k, (t, cls, _) in U.items():
    if cls == "Krypto":
        f = RAW / "binance" / f"{t}_h1.parquet"
        if not f.exists():
            continue
        h = pd.read_parquet(f)
        h.index = h.index.tz_convert("America/New_York")
        # Tageskerze 16:00–16:00 New York (synchron zum US-Schluss)
        g = h.shift(freq="8h").resample("1D")
        d = pd.DataFrame({"open": g["open"].first(), "high": g["high"].max(), "low": g["low"].min(), "close": g["close"].last()})
        d.index = d.index.tz_localize(None)
    else:
        f = RAW / "yahoo" / f"{t}_d1.parquet"
        if not f.exists():
            continue
        y = pd.read_parquet(f)
        y.index = y.index.tz_convert("America/New_York").normalize().tz_localize(None)
        y = y[~y.index.duplicated(keep="last")]
        adj = (y["adjclose"] / y["close"]) if "adjclose" in y else 1.0
        d = pd.DataFrame({"open": y["open"] * adj, "high": y["high"] * adj, "low": y["low"] * adj, "close": y["close"] * adj})
    O_[k], H_[k], L_[k], C_[k] = d["open"], d["high"], d["low"], d["close"]
C = pd.DataFrame(C_)
bdays = C["SPY"].dropna().index
C, Op, Hi, Lo = (pd.DataFrame(x).reindex(bdays) for x in (C_, O_, H_, L_))
C = C.loc["2006-06-01":]
Op, Hi, Lo = Op.loc[C.index], Hi.loc[C.index], Lo.loc[C.index]
mask = C.notna() & C.shift(1).notna()
ret = np.log(C).diff().where(mask)
gap = (Op / C.shift(1) - 1).where(mask)          # Schluss t-1 -> Eröffnung t
intra = (C / Op - 1).where(mask)                  # Eröffnung t -> Schluss t
cc = np.expm1(ret)
keys = list(C.columns)
cls_of = {k: U[k][1] for k in keys}
cost = pd.Series({k: U[k][2] for k in keys})
vol = (ret.rolling(60, min_periods=30).std() * np.sqrt(252))
log("Assets:", len(keys), "Tage:", len(C))
START, IS_END, OOS_START = "2007-06-01", "2016-12-31", "2017-01-01"

# ---------------------------------------------------------------- Indikatoren
def rsi(n):
    d = C.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))

sig_d = ret.rolling(60, min_periods=30).std().shift(1)
IND = {}
for n in (2, 5, 14):
    IND[f"RSI{n}"] = (rsi(n) - 50) / 50          # -1..+1
for L in (1, 3, 5):
    IND[f"Z{L}"] = ret.rolling(L, min_periods=L).sum() / (sig_d * np.sqrt(L))
for n in (5, 20):
    lp = np.log(C)
    IND[f"BB{n}"] = (lp - lp.rolling(n).mean()) / lp.rolling(n).std()
IND["IBS"] = ((C - Lo) / (Hi - Lo).replace(0, np.nan) - 0.5) * 2   # -1 Schluss am Tief, +1 am Hoch
log("Indikatoren:", list(IND))


# ---------------------------------------------------------------- Backtest
def run(W, execution="close", cost_mult=1.0):
    W = W.fillna(0.0)
    if execution == "close":
        pnl = (W.shift(1) * cc).sum(axis=1)
    else:  # Ausführung zur nächsten Eröffnung
        pnl = (W.shift(2) * gap).sum(axis=1) + (W.shift(1) * intra).sum(axis=1)
    tc = (W.diff().abs() * cost / 1e4).sum(axis=1) * cost_mult
    return pd.DataFrame({"gross": pnl, "net": pnl - tc, "expo": W.abs().sum(axis=1), "turn": W.diff().abs().sum(axis=1)})


def met(x, col="net"):
    d = x[col]
    d = d.loc[d.ne(0).idxmax():] if d.ne(0).any() else d
    if len(d) < 50 or d.std() == 0:
        return {"Sharpe": np.nan, "CAGR": np.nan, "MaxDD": np.nan, "t": np.nan}
    eq = (1 + d).cumprod()
    yrs = len(d) / 252
    return {"Sharpe": d.mean() / d.std() * np.sqrt(252), "CAGR": eq.iloc[-1] ** (1 / yrs) - 1,
            "MaxDD": (eq / eq.cummax() - 1).min(), "t": d.mean() / d.std() * np.sqrt(len(d)),
            "Vol": d.std() * np.sqrt(252), "Turnover_pa": x["turn"].loc[d.index].sum() / yrs,
            "Expo": x["expo"].loc[d.index].mean(), "CostShare": (x["gross"] - x["net"]).loc[d.index].sum() / max(x["gross"].loc[d.index].sum(), 1e-12)}


def summary(x, extra):
    m_all, m_is, m_oos = met(x.loc[START:]), met(x.loc[START:IS_END]), met(x.loc[OOS_START:])
    return {**extra, "Sharpe_IS": m_is["Sharpe"], "Sharpe_OOS": m_oos["Sharpe"], "Sharpe_ALL": m_all["Sharpe"],
            "t_ALL": m_all["t"], "CAGR_ALL": m_all["CAGR"], "MaxDD_ALL": m_all["MaxDD"], "Vol_ALL": m_all.get("Vol"),
            "Turnover_pa": m_all.get("Turnover_pa"), "CostShare": m_all.get("CostShare"),
            "Sharpe_brutto_ALL": met(x.loc[START:], "gross")["Sharpe"]}


THR = {"RSI2": [0.6, 0.8, 0.9], "RSI5": [0.4, 0.6], "RSI14": [0.2, 0.4], "Z1": [1.5, 2.0, 2.5], "Z3": [1.5, 2.0],
       "Z5": [1.5, 2.0], "BB5": [1.2, 1.5], "BB20": [1.5, 2.0], "IBS": [0.6, 0.8]}
Mv = mask.values

# 1) Einzelasset-Mean-Reversion
rows = []
for ind, ths in THR.items():
    O = IND[ind]
    for th, H, ex in itertools.product(ths, [1, 2], [0.0, -0.5]):
        theta_exit = ex * th
        pos = hysteresis(O.values, Mv, th, theta_exit, H)
        W = pd.DataFrame(pos, index=C.index, columns=keys) * 0.02 / vol
        for exe in ["close", "open"]:
            x = run(W, exe)
            rows.append(summary(x, {"family": "Einzelasset", "indicator": ind, "theta": th, "hold_max_d": H,
                                    "exit": "neutral" if ex == 0 else "Umkehr", "execution": exe}))
        # je Klasse (nur Schluss-Ausführung)
        if exe == "open":
            for c in sorted(set(cls_of.values())):
                mem = [k for k in keys if cls_of[k] == c]
                x = run(W[mem], "close")
                rows.append(summary(x, {"family": "Einzelasset je Klasse", "class": c, "indicator": ind, "theta": th,
                                        "hold_max_d": H, "exit": "neutral" if ex == 0 else "Umkehr", "execution": "close"}))
ts = pd.DataFrame(rows)
ts.to_csv(OUT / "single_asset_grid.csv", index=False)
log("Einzelasset:", len(ts))

# 2) Paare: alle Kombinationen (überlappend, netto verrechnet), getrennt nach 'gleiche Klasse' vs 'klassenübergreifend'
rows = []
all_pairs = list(itertools.combinations(keys, 2))
same = [(a, b) for a, b in all_pairs if cls_of[a] == cls_of[b]]
cross = [(a, b) for a, b in all_pairs if cls_of[a] != cls_of[b]]
log("Paare:", len(all_pairs), "gleiche Klasse:", len(same), "klassenübergreifend:", len(cross))
PTHR = {"RSI2": [1.2, 1.5], "RSI14": [0.6, 0.9], "Z1": [2.0, 2.5, 3.0], "Z3": [2.0, 2.5], "BB5": [2.0, 2.5]}
ci = {c: i for i, c in enumerate(keys)}
pair_store = {}
for ind, ths in PTHR.items():
    Ov = IND[ind].values
    for scope, plist in [("gleiche Klasse", same), ("klassenübergreifend", cross)]:
        ia = np.array([ci[a] for a, _ in plist])
        ib = np.array([ci[b] for _, b in plist])
        S = Ov[:, ia] - Ov[:, ib]
        if ind.startswith("Z"):
            S = S / np.sqrt(2)
        enter = Mv[:, ia] & Mv[:, ib]
        for th, H in itertools.product(ths, [1, 2]):
            pos = hysteresis(S, enter, th, 0.0, H)
            Uu = np.zeros((len(C), len(keys)))
            np.add.at(Uu.T, ia, pos.T.astype(float))
            np.add.at(Uu.T, ib, -pos.T.astype(float))
            W = pd.DataFrame(Uu, index=C.index, columns=keys) * 0.005 / vol
            for exe in ["close", "open"]:
                x = run(W, exe)
                r = summary(x, {"family": "Paare", "scope": scope, "indicator": ind, "theta": th, "hold_max_d": H,
                                "execution": exe, "n_pairs": len(plist),
                                "trades_pa": float((np.diff(pos, axis=0) != 0).sum() / 2 / (len(C) / 252))})
                rows.append(r)
            pair_store[(ind, scope, th, H)] = (pos, ia, ib)
pp = pd.DataFrame(rows)
pp.to_csv(OUT / "pairs_grid.csv", index=False)
log("Paare fertig:", len(pp))

# 2b) Einzelpaar-Statistik für den besten Paar-Indikator (Schluss-Ausführung): welche Paare tragen?
best = pp[(pp.execution == "close")].sort_values("Sharpe_IS", ascending=False).iloc[0]
pos, ia, ib = pair_store[(best.indicator, best.scope, best.theta, int(best.hold_max_d))]
plist = same if best.scope == "gleiche Klasse" else cross
indiv = []
for p, (a, b) in enumerate(plist):
    w = pd.DataFrame(0.0, index=C.index, columns=[a, b])
    w[a] = pos[:, p] * 0.02 / vol[a]
    w[b] = -pos[:, p] * 0.02 / vol[b]
    x = run(w, "close")
    n_tr = int((np.diff(pos[:, p]) != 0).sum() / 2)
    if n_tr < 10:
        continue
    indiv.append({"A": a, "B": b, "class_A": cls_of[a], "class_B": cls_of[b], "trades": n_tr,
                  "Sharpe_IS": met(x.loc[START:IS_END])["Sharpe"], "Sharpe_OOS": met(x.loc[OOS_START:])["Sharpe"],
                  "Sharpe_ALL": met(x.loc[START:])["Sharpe"]})
pd.DataFrame(indiv).to_csv(OUT / "pairs_individual_best_config.csv", index=False)
json.dump({k: (v if not isinstance(v, (np.floating, np.integer)) else float(v)) for k, v in best.to_dict().items()},
          open(OUT / "pairs_best_config.json", "w"), indent=2, default=str)

# 3) Korb gegen Korb (Klassen-Körbe) und Querschnitt
groups = {}
for k in keys:
    groups.setdefault(cls_of[k], []).append(k)
rows = []
for ind in ["RSI2", "RSI14", "Z1", "Z3", "BB5"]:
    Ov = IND[ind]
    B = pd.DataFrame({g: Ov[m].mean(axis=1) for g, m in groups.items()})
    Bopen = pd.DataFrame({g: mask[m].mean(axis=1) for g, m in groups.items()})
    names = list(groups)
    bpairs = list(itertools.combinations(names, 2))
    ga = np.array([names.index(a) for a, _ in bpairs])
    gb = np.array([names.index(b) for _, b in bpairs])
    S = B.values[:, ga] - B.values[:, gb]
    sd = np.nanstd(S[:2500], axis=0)          # Skalierung aus IS-Zeitraum
    S = S / sd
    enter = (Bopen.values[:, ga] >= 0.5) & (Bopen.values[:, gb] >= 0.5)
    for th, H in itertools.product([1.5, 2.0, 2.5], [1, 2]):
        pos = hysteresis(S, enter, th, 0.0, H)
        Ub = np.zeros((len(C), len(names)))
        np.add.at(Ub.T, ga, pos.T.astype(float))
        np.add.at(Ub.T, gb, -pos.T.astype(float))
        W = pd.DataFrame(0.0, index=C.index, columns=keys)
        for g, m in groups.items():
            for a in m:
                W[a] += Ub[:, names.index(g)] * 0.02 / len(m) / vol[a]
        for exe in ["close", "open"]:
            rows.append(summary(run(W, exe), {"family": "Korb gegen Korb", "indicator": ind, "theta": th, "hold_max_d": H, "execution": exe}))
    # Querschnitt: alle Assets bzw. klassenneutral
    for k_, H, neutral in itertools.product([3, 5], [1, 2], [False, True]):
        Om = Ov.where(mask)
        sig = pd.DataFrame(0.0, index=C.index, columns=keys)
        sets = groups.values() if neutral else [keys]
        for m in sets:
            if len(m) < 2 * k_ + 1 and neutral:
                kk = 1
            else:
                kk = k_
            if len(m) < 3:
                continue
            sub = Om[m]
            rk = sub.rank(axis=1)
            n = sub.notna().sum(axis=1)
            sig[m] += (rk <= kk).astype(float) - rk.gt(n - kk, axis=0).astype(float)
        W = (sig * 0.02 / vol).fillna(0.0).rolling(H, min_periods=1).mean()
        for exe in ["close", "open"]:
            rows.append(summary(run(W, exe), {"family": "Querschnitt" + (" klassenneutral" if neutral else ""), "indicator": ind,
                                              "k": k_, "hold_max_d": H, "execution": exe}))
bb = pd.DataFrame(rows)
bb.to_csv(OUT / "baskets_xs_grid.csv", index=False)
log("Körbe/Querschnitt:", len(bb))

# 4) Konditionierung: Volatilitätsregime (VIX) und Trendfilter für die beste Einzelasset-Variante
vix = pd.read_parquet(RAW / "yahoo" / "IDX_VIX_d1.parquet")["close"]
vix.index = vix.index.tz_convert("America/New_York").normalize().tz_localize(None)
vix = vix[~vix.index.duplicated()].reindex(C.index).ffill()
hi_vol = (vix > vix.rolling(250, min_periods=60).median()).values
trend_up = (C > C.rolling(100, min_periods=60).mean())
rows = []
for ind, th, H in [("RSI2", 0.8, 2), ("Z1", 2.0, 2), ("Z3", 2.0, 2), ("IBS", 0.8, 1), ("BB5", 1.5, 2)]:
    O = IND[ind]
    base = hysteresis(O.values, Mv, th, 0.0, H)
    for cond in ["keine", "VIX hoch", "VIX niedrig", "mit Trend", "gegen Trend"]:
        if cond == "keine":
            ok = Mv
        elif cond == "VIX hoch":
            ok = Mv & hi_vol[:, None]
        elif cond == "VIX niedrig":
            ok = Mv & ~hi_vol[:, None]
        elif cond == "mit Trend":   # long nur im Aufwärtstrend, short nur im Abwärtstrend (Connors)
            ok = Mv
        else:
            ok = Mv
        pos = hysteresis(O.values, ok, th, 0.0, H).astype(float)
        if cond == "mit Trend":
            tu = trend_up.values
            pos = np.where(((pos > 0) & tu) | ((pos < 0) & ~tu), pos, 0)
        if cond == "gegen Trend":
            tu = trend_up.values
            pos = np.where(((pos > 0) & ~tu) | ((pos < 0) & tu), pos, 0)
        W = pd.DataFrame(pos, index=C.index, columns=keys) * 0.02 / vol
        for side in ["beide", "nur long", "nur short"]:
            Ws = W.clip(lower=0) if side == "nur long" else (W.clip(upper=0) if side == "nur short" else W)
            rows.append(summary(run(Ws, "close"), {"indicator": ind, "theta": th, "hold_max_d": H, "condition": cond, "side": side}))
cd = pd.DataFrame(rows)
cd.to_csv(OUT / "conditioning.csv", index=False)
log("Konditionierung:", len(cd))

# Jahreswerte der besten Varianten je Familie (IS-Auswahl) für Grafiken
best_rows = {}
for fam, df in [("Einzelasset", ts[ts.family == "Einzelasset"]), ("Paare", pp), ("Korb/Querschnitt", bb)]:
    b = df[df.execution == "close"].sort_values("Sharpe_IS", ascending=False).iloc[0]
    best_rows[fam] = {k: (float(v) if isinstance(v, (np.floating, np.integer)) else v) for k, v in b.to_dict().items()}
json.dump(best_rows, open(OUT / "best_by_family.json", "w"), indent=2, default=str)
log("FERTIG")
