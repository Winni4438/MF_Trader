"""Überhitzungs-/Unterkühlungs-Indikatoren.

Alle Indikatoren werden je Asset auf seiner *eigenen* Bar-Folge berechnet (nur Stunden, in denen
der Markt offen war) und danach auf das gemeinsame Zeitraster vorwärts gefüllt. So verwässern
geschlossene Stunden (Wochenende, Sitzungspausen) die Werte nicht.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _per_asset(close: pd.DataFrame, mask: pd.DataFrame, fn) -> pd.DataFrame:
    out = {}
    for c in close.columns:
        s = close[c][mask[c]]
        out[c] = fn(s).reindex(close.index).ffill()
    return pd.DataFrame(out)


def rsi(close: pd.DataFrame, mask: pd.DataFrame, n: int = 14) -> pd.DataFrame:
    """Wilder-RSI (0–100) auf den eigenen Bars jedes Assets."""
    def f(s):
        d = s.diff()
        up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
        dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
        return 100 - 100 / (1 + up / dn.replace(0, np.nan))
    return _per_asset(close, mask, f)


def zscore_ma(close: pd.DataFrame, mask: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Abstand des Log-Preises vom gleitenden Mittel in Standardabweichungen (Bollinger-z)."""
    def f(s):
        lp = np.log(s)
        return (lp - lp.rolling(n, min_periods=n).mean()) / lp.rolling(n, min_periods=n).std()
    return _per_asset(close, mask, f)


def ibs(df_open_high_low_close: dict) -> pd.DataFrame:
    """Internal Bar Strength (Tagesdaten): (Close − Low)/(High − Low); 0 = Schluss am Tief."""
    h, l, c = df_open_high_low_close["high"], df_open_high_low_close["low"], df_open_high_low_close["close"]
    return (c - l) / (h - l).replace(0, np.nan)


def pca_residual_scores(z: pd.DataFrame, k: int = 3, window: int = 24 * 30, step: int = 24,
                        L: int = 24) -> pd.DataFrame:
    """Avellaneda/Lee-artige Faktor-Residuen.

    z: normierte Renditen (T×N, NaN=0). Alle `step` Stunden werden auf den letzten `window` Stunden
    die k Hauptkomponenten geschätzt; für die folgenden `step` Stunden wird die Rendite in
    Faktoranteil und Residuum zerlegt (Projektion). s-Score = kumuliertes Residuum über L Stunden,
    geteilt durch dessen Standardabweichung im Schätzfenster. Positiv = Asset ist relativ zu
    seinen Faktoren 'überhitzt'.
    """
    Z = z.fillna(0.0).values
    T, N = Z.shape
    E = np.full((T, N), np.nan)
    sd = np.full((T, N), np.nan)
    for t0 in range(window, T, step):
        W = Z[t0 - window:t0]
        Wc = W - W.mean(axis=0)
        _, _, Vt = np.linalg.svd(Wc, full_matrices=False)
        V = Vt[:k].T                          # N×k
        res_w = W - (W @ V) @ V.T
        s_w = res_w.std(axis=0)
        blk = Z[t0:t0 + step]
        E[t0:t0 + step] = blk - (blk @ V) @ V.T
        sd[t0:t0 + step] = s_w
    Es = pd.DataFrame(E, index=z.index, columns=z.columns)
    cum = Es.rolling(L, min_periods=L).sum()
    return cum / (pd.DataFrame(sd, index=z.index, columns=z.columns) * np.sqrt(L))
