"""Vektorisierter Stunden-Backtester mit realistischer Ausführung und Kosten.

Konvention: target.loc[t] = gewünschte Gewichte (Notional / Kapital), entschieden mit
Informationen bis zum Schluss der Stunde t. Ausgeführt wird zum Beginn der nächsten Stunde
(t+1+delay), aber nur, wenn der Markt des Assets dann offen ist; sonst bleibt die alte Position.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from mf_trader.universe import BY_KEY


def positions_from_target(target: pd.DataFrame, mask: pd.DataFrame, delay: int = 0) -> pd.DataFrame:
    tgt = target.shift(1 + delay)
    pos = tgt.where(mask[tgt.columns]).ffill().fillna(0.0)
    return pos


def stress_multiplier(ret: pd.DataFrame, cap: float = 3.0) -> pd.DataFrame:
    """Kostenaufschlag in Stressphasen: Spreads weiten sich mit der Volatilität."""
    rv = ret.abs().rolling(24, min_periods=6).mean()
    med = rv.rolling(24 * 250, min_periods=24 * 30).median()
    return np.sqrt(rv / med).clip(lower=1.0, upper=cap).fillna(1.0)


def run(target: pd.DataFrame, panel: dict, delay: int = 0, cost_mult: float = 1.0,
        stress: pd.DataFrame | None = None) -> pd.DataFrame:
    cols = list(target.columns)
    ret = panel["ret"][cols].fillna(0.0)
    pos = positions_from_target(target, panel["mask"], delay)
    simple = np.expm1(ret)
    gross = (pos * simple).sum(axis=1)
    costs_bps = pd.Series({c: BY_KEY[c].cost_bps for c in cols})
    trades = pos.diff().abs().fillna(pos.abs())
    m = stress[cols] if stress is not None else 1.0
    cost = (trades * m * costs_bps / 1e4).sum(axis=1) * cost_mult
    return pd.DataFrame({"gross": gross, "cost": cost, "net": gross - cost,
                         "gross_exposure": pos.abs().sum(axis=1), "turnover": trades.sum(axis=1)})


def trading_day(idx: pd.DatetimeIndex) -> pd.DatetimeIndex:
    """Handelstag endet 21:00 UTC (≈ US-Schluss); Wochenend-Stunden zählen zum Montag."""
    d = (idx + pd.Timedelta(hours=3)).normalize().tz_localize(None)
    wd = d.dayofweek
    return d + pd.to_timedelta(np.where(wd == 5, 2, np.where(wd == 6, 1, 0)), unit="D")


def daily(res: pd.DataFrame, col: str = "net") -> pd.Series:
    return res[col].groupby(trading_day(res.index)).sum()


def metrics(res: pd.DataFrame, col: str = "net", target_vol: float | None = None) -> dict:
    d = daily(res, col)
    d = d[d.index >= d.ne(0).idxmax()] if d.ne(0).any() else d
    if target_vol and d.std() > 0:
        d = d * (target_vol / np.sqrt(252)) / d.std()
    eq = (1 + d).cumprod()
    dd = eq / eq.cummax() - 1
    yrs = len(d) / 252
    active = res["gross_exposure"] > 0
    ep = (active != active.shift()).cumsum()[active]
    n_trades = ep.nunique()
    trade_pnl = res.loc[active, col].groupby(ep).sum() if n_trades else pd.Series(dtype=float)
    sd = d.std()
    return {
        "CAGR": eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
        "Vol": sd * np.sqrt(252),
        "Sharpe": d.mean() / sd * np.sqrt(252) if sd > 0 else np.nan,
        "t_stat": d.mean() / sd * np.sqrt(len(d)) if sd > 0 else np.nan,
        "MaxDD": dd.min(),
        "Trades": n_trades,
        "Trades_pa": n_trades / yrs if yrs > 0 else np.nan,
        "HitRate": (trade_pnl > 0).mean() if n_trades else np.nan,
        "AvgTrade_bps": trade_pnl.mean() * 1e4 if n_trades else np.nan,
        "TimeInMarket": active.mean(),
        "CostShare": res["cost"].sum() / res["gross"].sum() if res["gross"].sum() > 0 else np.nan,
        "Skew": d.skew(),
    }


def vol_weights(keys: list[str], vol: pd.Series, per_leg_vol: float) -> dict[str, float]:
    """Inverse-Vol-Gewichte: jedes Bein trägt per_leg_vol (annualisiert) Risiko."""
    w = {}
    for k in keys:
        v = vol.get(k, np.nan)
        if np.isfinite(v) and v > 0:
            w[k] = per_leg_vol / v
    return w
