"""Referenz auf Tagesbasis (Swing, 2007–2026) mit ETF-Daten:
1) Rotations-Taxonomie: Häufigkeit typischer Muster und was danach passiert
2) Rotation Follower auf Tagesbasis (Tage bis Wochen)
3) Klassisches Cross-Asset-Momentum
4) Paar-Matrix 'welche Rotation lohnt sich' auf Swing-Horizont
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mf_trader.strategies import RotationParams, rotation_follower  # noqa: E402

OUT = ROOT / "results" / "daily"
OUT.mkdir(parents=True, exist_ok=True)
RAW = ROOT / "data" / "raw" / "yahoo"

# key: (Ticker, Rolle, Kosten bps/Seite)
U = {
    "SPY": ("SPY", "risk", 1), "QQQ": ("QQQ", "risk", 1), "IWM": ("IWM", "risk", 1.5), "EFA": ("EFA", "risk", 2),
    "EEM": ("EEM", "risk", 2), "HYG": ("HYG", "risk", 2), "AUD": ("FXA", "risk", 4), "BTC": ("BTC_USD", "risk", 10),
    "TLT": ("TLT", "haven", 1.5), "IEF": ("IEF", "haven", 1.5), "GLD": ("GLD", "haven", 1.5), "JPY": ("FXY", "haven", 4),
    "CHF": ("FXF", "haven", 5), "USD": ("UUP", "other", 3), "OIL": ("USO", "other", 3), "CMDTY": ("DBC", "other", 3),
    "SLV": ("SLV", "other", 3), "TIP": ("TIP", "other", 2), "REIT": ("VNQ", "other", 2), "UTIL": ("XLU", "other", 2),
}
px = {}
for k, (t, _, _) in U.items():
    df = pd.read_parquet(RAW / f"{t}_d1.parquet")
    s = (df["adjclose"] if "adjclose" in df else df["close"]).copy()
    s.index = s.index.tz_convert("America/New_York").normalize().tz_localize(None)
    px[k] = s[~s.index.duplicated(keep="last")]
px = pd.DataFrame(px)
bdays = px["SPY"].dropna().index
px = px.reindex(bdays).ffill(limit=3)
px = px.loc["2006-06-01":]
ret = np.log(px).diff()
mask = px.notna() & px.shift(1).notna()
ret = ret.where(mask)
risk = [k for k, v in U.items() if v[1] == "risk"]
haven = [k for k, v in U.items() if v[1] == "haven"]
cost = pd.Series({k: v[2] for k, v in U.items()})
sig = ret.rolling(60, min_periods=30).std().shift(1)
z = ret / sig
vol = sig * np.sqrt(252)
START = "2007-06-01"
IS_END = "2016-12-31"


def F_d(L):
    return ret.rolling(L, min_periods=L).sum() / (sig * np.sqrt(L))


def roro_z(L):
    F = F_d(L)
    r = (F[risk].mean(axis=1) - F[haven].mean(axis=1)) / np.sqrt(2)
    m = r.rolling(500, min_periods=120).mean().shift(1)
    s = r.rolling(500, min_periods=120).std().shift(1)
    return (r - m) / s


def run_daily(target, lag=1, cost_mult=1.0):
    # Ziel wird am Schluss von Tag t entschieden -> verdient frühestens die Rendite von t+1
    pos = target.shift(1 + lag).fillna(0.0)
    r = np.expm1(ret[target.columns].fillna(0.0))
    gross = (pos * r).sum(axis=1)
    c = (pos.diff().abs() * cost / 1e4).sum(axis=1) * cost_mult
    return pd.DataFrame({"gross": gross, "net": gross - c, "expo": pos.abs().sum(axis=1)})


def met(x, col="net"):
    d = x[col].loc[START:]
    d = d.loc[d.ne(0).idxmax():] if d.ne(0).any() else d
    eq = (1 + d).cumprod()
    yrs = len(d) / 252
    act = x["expo"].loc[d.index] > 0
    ep = (act != act.shift()).cumsum()[act]
    tp = d[act].groupby(ep).sum() if act.any() else pd.Series(dtype=float)
    return {"CAGR": eq.iloc[-1] ** (1 / yrs) - 1, "Vol": d.std() * np.sqrt(252),
            "Sharpe": d.mean() / d.std() * np.sqrt(252) if d.std() > 0 else np.nan,
            "MaxDD": (eq / eq.cummax() - 1).min(), "Trades_pa": ep.nunique() / yrs,
            "HitRate": (tp > 0).mean() if len(tp) else np.nan, "AvgTrade_bps": tp.mean() * 1e4 if len(tp) else np.nan,
            "TimeInMarket": act.mean()}


def split(x):
    return {"IS": met(x.loc[:IS_END]), "OOS": met(x.loc["2017-01-01":]), "ALL": met(x)}


# ---------------------------------------------------------------- 1) Rotations-Taxonomie
Z = z.loc[START:]
eq_, bd, gd, usd, jpy, oil = Z["SPY"], Z["TLT"], Z["GLD"], Z["USD"], Z["JPY"], Z["OIL"]
pat = pd.Series("Ruhig / ohne klares Muster", index=Z.index)
cond = [
    ("Klassisches Risk-off (Aktien↓, Anleihen↑, Gold/Yen↑)", (eq_ <= -1) & (bd >= 0.5) & ((gd >= 0) | (jpy >= 0.5))),
    ("Liquidation / Dash for Cash (alles↓, USD↑)", (eq_ <= -1) & (bd <= -0.5) & (gd <= -0.5) & (usd >= 0.5)),
    ("Sell America (Aktien↓, Anleihen↓, USD↓)", (eq_ <= -1) & (bd <= -0.5) & (usd <= -0.5)),
    ("Zins-/Inflationsschock (Aktien↓, Anleihen↓)", (eq_ <= -1) & (bd <= -0.5)),
    ("Aktien↓ ohne Hafen-Zufluss", (eq_ <= -1)),
    ("Reflations-Risk-on (Aktien↑, Anleihen↓)", (eq_ >= 1) & (bd <= -0.5)),
    ("Liquiditätsrally (Aktien↑, Anleihen↑, USD↓)", (eq_ >= 1) & (bd >= 0) & (usd <= 0)),
    ("Risk-on sonstig (Aktien↑)", (eq_ >= 1)),
    ("Rohstoff-/Ölimpuls (Öl↑↑)", (oil >= 1.5)),
    ("Flucht in Gold/Yen bei ruhigen Aktien", ((gd >= 1.5) | (jpy >= 1.5)) & (eq_.abs() < 1)),
]
assigned = pd.Series(False, index=Z.index)
for name, c in cond:
    c = c.fillna(False) & ~assigned
    pat[c] = name
    assigned |= c
pat.to_csv(OUT / "day_patterns.csv")
freq = pd.crosstab(pat.index.year, pat)
freq.to_csv(OUT / "pattern_frequency_by_year.csv")
# Folgerenditen (Fortsetzung vs. Umkehr) je Muster
rows = []
for h in [1, 5, 20]:
    fw = ret.shift(-1).rolling(h, min_periods=1).sum().shift(-(h - 1)).loc[START:]
    for name in pat.unique():
        idx = pat[pat == name].index
        x = fw.reindex(idx)
        for a in ["SPY", "QQQ", "TLT", "IEF", "GLD", "JPY", "CHF", "USD", "OIL", "BTC", "HYG"]:
            rows.append({"pattern": name, "h_days": h, "asset": a, "n": int(x[a].count()),
                         "mean_pct": x[a].mean() * 100, "t": x[a].mean() / x[a].std() * np.sqrt(x[a].count()) if x[a].count() > 2 else np.nan,
                         "hit": (x[a] > 0).mean()})
pd.DataFrame(rows).to_csv(OUT / "pattern_followthrough.csv", index=False)
# Gleichtägige Bewegungen je Muster (Charakteristik)
same = ret.loc[START:].groupby(pat).mean() * 100
same.to_csv(OUT / "pattern_same_day_mean_pct.csv")

# ---------------------------------------------------------------- 2) Rotation Follower auf Tagesbasis
Fd = {L: F_d(L) for L in [1, 2, 3, 5, 10, 20]}
RZd = {L: roro_z(L) for L in [1, 2, 3, 5, 10, 20]}
idx_utc = ret.index.tz_localize("UTC") + pd.Timedelta(hours=21)


def to_utc(x):
    x = x.copy()
    x.index = idx_utc
    return x


mask_d = to_utc(mask)
vol_d = to_utc(vol)
grid = []
for L, th, H, Lx, src_k, lag in itertools.product([1, 3, 5, 10], [1.5, 2.0, 2.5], [1, 3, 5, 10, 20], [1, 3], [0, 2], [0, 1]):
    p = RotationParams(window=L, theta=th, max_hold=H, exit_window=Lx, src_k=src_k, eod_flat=False, risk=risk, haven=haven,
                       per_leg_vol=0.05)
    tgt, tr = rotation_follower(p, to_utc(Fd[L]), to_utc(RZd[Lx]), to_utc(RZd[L]), vol_d, mask_d)
    tgt.index = ret.index
    x = run_daily(tgt, lag=lag)
    m = split(x)
    grid.append({"window_d": L, "theta": th, "max_hold_d": H, "exit_window_d": Lx, "src_k": src_k, "lag": lag,
                 **{f"{k}_{s}": v for s in m for k, v in m[s].items()}})
grid = pd.DataFrame(grid)
grid.to_csv(OUT / "grid_rotation_follower_daily.csv", index=False)

# ---------------------------------------------------------------- 3) Cross-Asset-Momentum (Swing/Position)
xs = []
for L, H, k in itertools.product([5, 20, 60, 120, 250], [5, 20], [3, 5]):
    F = ret.rolling(L, min_periods=L).sum().shift(0) / (sig * np.sqrt(L))
    rk = F.rank(axis=1, ascending=False)
    n = F.notna().sum(axis=1)
    for ls in ["long_only", "long_short"]:
        s = (rk <= k).astype(float)
        if ls == "long_short":
            s = s - (rk > n.values[:, None] - k).astype(float)
        w = (s.where(F.notna(), 0) * 0.05 / vol).fillna(0).rolling(H, min_periods=1).mean()
        x = run_daily(w, lag=1)
        m = split(x)
        xs.append({"lookback_d": L, "hold_d": H, "k": k, "type": ls, **{f"{kk}_{s_}": v for s_ in m for kk, v in m[s_].items()}})
pd.DataFrame(xs).to_csv(OUT / "grid_xs_momentum_daily.csv", index=False)

# ---------------------------------------------------------------- 4) Paar-Matrix Swing
pairs = []
keys = list(U)
for a, b in itertools.combinations(keys, 2):
    for L, H in [(5, 5), (20, 20), (60, 20)]:
        s = (F_d(L)[a] - F_d(L)[b]) / np.sqrt(2)
        sg = pd.Series(np.where(s > 1.0, 1.0, np.where(s < -1.0, -1.0, 0.0)), index=s.index).rolling(H, min_periods=1).mean()
        tgt = pd.DataFrame({a: sg * 0.05 / vol[a], b: -sg * 0.05 / vol[b]}).fillna(0.0)
        x = run_daily(tgt, lag=1)
        pairs.append({"A": a, "B": b, "L": L, "H": H, "Sharpe_brutto": met(x, "gross")["Sharpe"], "Sharpe_netto": met(x)["Sharpe"],
                      "Sharpe_netto_IS": met(x.loc[:IS_END])["Sharpe"], "Sharpe_netto_OOS": met(x.loc["2017-01-01":])["Sharpe"]})
pd.DataFrame(pairs).to_csv(OUT / "pair_matrix_daily.csv", index=False)

# Buy&Hold-Referenzen
bh = {k: met(pd.DataFrame({"gross": np.expm1(ret[k].fillna(0)), "net": np.expm1(ret[k].fillna(0)), "expo": 1.0})) for k in ["SPY", "QQQ", "TLT", "GLD", "BTC"]}
json.dump(bh, open(OUT / "buy_and_hold.json", "w"), indent=2)
print("FERTIG daily")
