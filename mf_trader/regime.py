"""Tagesregime-Filter (übergeordneter Zeitrahmen), strikt ohne Look-ahead (Vortageswerte)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from mf_trader.backtest import trading_day


def daily_close_returns(ret_h: pd.DataFrame) -> pd.DataFrame:
    return ret_h.groupby(trading_day(ret_h.index)).sum()


def to_hourly(daily: pd.DataFrame | pd.Series, hourly_index: pd.DatetimeIndex):
    """Tageswert von Tag d gilt erst ab dem Folgetag (shift(1)) und wird auf Stunden gemappt."""
    d = daily.shift(1)
    td = trading_day(hourly_index)
    out = d.reindex(td)
    out.index = hourly_index
    return out


def stock_bond_corr(dret: pd.DataFrame, eq: str = "SPX", bond: str = "UST", window: int = 60) -> pd.Series:
    return dret[eq].rolling(window, min_periods=40).corr(dret[bond])


def trend_ok(dret: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    """Asset ist im Aufwärtstrend (Summe der Log-Renditen der letzten N Tage > 0)."""
    return dret.rolling(lookback, min_periods=lookback // 2).sum() > 0


def daily_roro(dret: pd.DataFrame, risk: list[str], haven: list[str], vol_window: int = 60) -> pd.Series:
    z = dret / dret.rolling(vol_window, min_periods=20).std().shift(1)
    r = z[[c for c in risk if c in z]].mean(axis=1)
    h = z[[c for c in haven if c in z]].mean(axis=1)
    return (r - h) / np.sqrt(2)
