"""Robustheit der relativen RSI-Paare: Konzentration, Ausschluss einzelner Assets/Klassen, Jahreswerte."""
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
ALT = ["SOL", "BNB", "XRP", "ADA", "DOGE", "AVAX", "LINK", "LTC"]
EXCL = {"alle 42 Märkte": [], "ohne AVAX und Soja": ["AVAX", "SOY"], "ohne Altcoins und Soja": ALT + ["SOY"],
        "ohne Krypto": ALT + ["BTC", "ETH"], "nur Krypto-Majors + traditionelle Märkte, ohne Soja": ALT + ["SOY"]}
rows, yearly = [], {}
RSI = {}
for (n, th, H), (name, ex) in itertools.product([(96, 0.6, 24), (120, 0.6, 24), (168, 0.5, 24), (96, 0.8, 12)], EXCL.items()):
    if name.startswith("nur Krypto-Majors"):
        continue
    keys = [k for k in ret.columns if k not in ex]
    cls_of = {k: MR_BY_KEY[k].asset_class for k in keys}
    if n not in RSI:
        RSI[n] = (oh.rsi(close, mask, n) - 50) / 50
    Ov = RSI[n][keys].values
    Mv = mask[keys].values
    ci = {c: i for i, c in enumerate(keys)}
    plist = [(a, b) for a, b in itertools.combinations(keys, 2) if cls_of[a] != cls_of[b]]
    ia = np.array([ci[a] for a, _ in plist]); ib = np.array([ci[b] for _, b in plist])
    pos = mr.hysteresis(Ov[:, ia] - Ov[:, ib], Mv[:, ia] & Mv[:, ib], th, 0.0, H)
    U = np.zeros((len(ret), len(keys)))
    np.add.at(U.T, ia, pos.T.astype(float)); np.add.at(U.T, ib, -pos.T.astype(float))
    W = (pd.DataFrame(U, index=ret.index, columns=keys) * 0.01 / vol[keys]).fillna(0.0)
    res = bt.run(W, P, stress=stress).loc["2019-07-01":]
    # Konzentration: Anteil der Einstiege, bei denen das häufigste 'heiße' Asset beteiligt ist
    hot = []
    for p in range(pos.shape[1]):
        st = np.flatnonzero((pos[1:, p] != 0) & (pos[:-1, p] == 0)) + 1
        for s0 in st:
            hot.append(plist[p][0] if pos[s0, p] == -1 else plist[p][1])
    hs = pd.Series(hot).value_counts()
    d = bt.daily(res)
    s10 = d * (0.10 / np.sqrt(252)) / d.std()
    yr = {int(k): round(float(v) * 100, 1) for k, v in s10.groupby(s10.index.year).sum().items()}
    tag = f"RSI {n} h, Abstand {int(th*50)} Pkt., {H} h"
    rows.append({"Variante": tag, "Universum": name, "Einstiege": len(hot), "Sharpe_IS": bt.metrics(res.loc[:"2022-12-31"])["Sharpe"],
                 "Sharpe_OOS": bt.metrics(res.loc["2023-01-01":])["Sharpe"], "Sharpe_ALL": bt.metrics(res)["Sharpe"],
                 "Sharpe_ohne_2020": bt.metrics(res[(res.index < pd.Timestamp("2020-01-01", tz="UTC")) | (res.index >= pd.Timestamp("2021-01-01", tz="UTC"))])["Sharpe"],
                 "häufigstes_heißes_Asset": f"{hs.index[0]} ({hs.iloc[0]/len(hot):.0%})" if len(hot) else "",
                 "Top3_Anteil": float(hs.head(3).sum() / max(len(hot), 1)), "Jahre_positiv": sum(v > 0 for v in yr.values()), "Jahre": yr})
    print(rows[-1], flush=True)
df = pd.DataFrame(rows)
df.to_csv(OUT / "robustness_exclusions.csv", index=False)
