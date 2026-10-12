"""Statistische Absicherung gegen Data-Mining."""
from __future__ import annotations

import numpy as np
from scipy import stats


def deflated_sharpe(returns: np.ndarray, sr_trials: np.ndarray) -> dict:
    """Deflated Sharpe Ratio (Bailey & López de Prado 2014).

    returns: Periodenrenditen (z. B. täglich) der ausgewählten Strategie.
    sr_trials: Sharpe Ratios (gleiche Periodenbasis, nicht annualisiert) aller getesteten Varianten.
    Rückgabe: Wahrscheinlichkeit, dass die wahre Sharpe > 0 ist, nachdem für die Anzahl und Streuung
    der Versuche, Schiefe und Wölbung korrigiert wurde.
    """
    r = np.asarray(returns, float)
    r = r[np.isfinite(r)]
    T = len(r)
    sr = r.mean() / r.std(ddof=1)
    g3 = stats.skew(r)
    g4 = stats.kurtosis(r, fisher=False)
    trials = np.asarray(sr_trials, float)
    trials = trials[np.isfinite(trials)]
    N = max(len(trials), 1)
    var_sr = trials.var(ddof=1) if N > 1 else 0.0
    emc = 0.5772156649
    sr0 = np.sqrt(var_sr) * ((1 - emc) * stats.norm.ppf(1 - 1 / N) + emc * stats.norm.ppf(1 - 1 / (N * np.e))) if N > 1 else 0.0
    denom = np.sqrt(1 - g3 * sr + (g4 - 1) / 4 * sr ** 2)
    z = (sr - sr0) * np.sqrt(T - 1) / denom
    return {"SR_period": float(sr), "SR0_period": float(sr0), "n_trials": int(N), "DSR": float(stats.norm.cdf(z)),
            "PSR_vs_0": float(stats.norm.cdf(sr * np.sqrt(T - 1) / denom))}
