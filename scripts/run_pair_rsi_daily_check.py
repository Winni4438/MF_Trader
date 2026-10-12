"""Unabhängiger Gegencheck auf Tagesdaten 2007–2026: relative RSI-Paare mit kurzen Tages-RSI (3–7 Tage),
klassenübergreifend, Haltedauer ≤ 2 Tage. Entspricht den Stunden-Fenstern 72–168 h."""
import itertools
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
C, mask, cost, vol, cc, gap, intra, cls_of = (ns[k] for k in ["C", "mask", "cost", "vol", "cc", "gap", "intra", "cls_of"])
keys = list(C.columns)
ci = {c: i for i, c in enumerate(keys)}


def rsi(n):
    d = C.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return (100 - 100 / (1 + up / dn.replace(0, np.nan)) - 50) / 50


def sh(x):
    x = x[x.ne(0).idxmax():] if x.ne(0).any() else x
    return x.mean() / x.std() * np.sqrt(252) if x.std() > 0 else np.nan


rows = []
for scope in ["klassenübergreifend", "ohne Krypto, klassenübergreifend"]:
    ks = [k for k in keys if not (scope.startswith("ohne") and cls_of[k] == "Krypto")]
    plist = [(a, b) for a, b in itertools.combinations(ks, 2) if cls_of[a] != cls_of[b]]
    ia = np.array([ci[a] for a, _ in plist]); ib = np.array([ci[b] for _, b in plist])
    enter = mask.values[:, ia] & mask.values[:, ib]
    for n, th, H in itertools.product([3, 5, 7, 10], [0.9, 1.1, 1.3, 1.5], [1, 2]):
        O = rsi(n).values
        pos = hysteresis(O[:, ia] - O[:, ib], enter, th, 0.0, H)
        U = np.zeros((len(C), len(keys)))
        np.add.at(U.T, ia, pos.T.astype(float)); np.add.at(U.T, ib, -pos.T.astype(float))
        W = (pd.DataFrame(U, index=C.index, columns=keys) * 0.005 / vol).fillna(0.0)
        for exe in ["close", "open"]:
            pnl = (W.shift(1) * cc).sum(axis=1) if exe == "close" else (W.shift(2) * gap).sum(axis=1) + (W.shift(1) * intra).sum(axis=1)
            net = (pnl - (W.diff().abs() * cost / 1e4).sum(axis=1)).loc["2007-06-01":]
            rows.append({"scope": scope, "rsi_tage": n, "abstand_pkt": int(th * 50), "hold_d": H, "execution": exe,
                         "entries_pa": float(((pos[1:] != 0) & (pos[:-1] == 0)).sum() / (len(C) / 252)),
                         "entries_per_pair_year": float(((pos[1:] != 0) & (pos[:-1] == 0)).sum() / (len(C) / 252) / len(plist)),
                         "Sharpe_brutto": sh(pnl.loc["2007-06-01":]), "Sharpe_netto": sh(net),
                         "2007-2012": sh(net.loc[:"2012-12-31"]), "2013-2018": sh(net.loc["2013":"2018"]), "2019-2026": sh(net.loc["2019":])})
df = pd.DataFrame(rows)
df.to_csv(ROOT / "results" / "pair_rsi_deepdive" / "daily_check_2007_2026.csv", index=False)
pd.set_option("display.width", 250)
print(df[df.entries_per_pair_year.between(0.05, 0.6)].groupby(["scope", "execution", "rsi_tage"])[["entries_per_pair_year", "Sharpe_brutto", "Sharpe_netto", "2007-2012", "2013-2018", "2019-2026"]].mean().round(2).to_string())
print("Anteil netto>0:", df.groupby(["scope", "execution"]).Sharpe_netto.apply(lambda s: (s > 0).mean()).round(2).to_dict())
print(df.sort_values("Sharpe_netto", ascending=False).head(8).round(2).to_string())
