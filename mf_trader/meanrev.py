"""Mean-Reversion-Engines: Einzelasset, Paare (überlappend), Körbe, Querschnitt.

Konvention: Ein Signal S > +theta heißt 'überhitzt' (-> short), S < -theta 'unterkühlt' (-> long).
Ausstieg, sobald sich die Einschätzung auflöst (S kreuzt theta_exit Richtung 0 bzw. darüber hinaus)
oder nach max_hold Bars. Positionen werden in Risikoeinheiten geführt und über die inverse
Volatilität in Gewichte (Notional/Kapital) umgerechnet.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def hysteresis(S: np.ndarray, can_enter: np.ndarray, theta: float, theta_exit: float, max_hold: int,
               can_exit: np.ndarray | None = None) -> np.ndarray:
    """Vektorisierte Zustandsmaschine über M Signale gleichzeitig (Schleife nur über die Zeit).
    Rückgabe: Positionen in {-1, 0, +1} (T×M); +1 = long (unterkühlt), -1 = short (überhitzt)."""
    T, M = S.shape
    pos = np.zeros(M)
    age = np.zeros(M)
    out = np.zeros((T, M), dtype=np.int8)
    for t in range(T):
        s = S[t]
        valid = np.isfinite(s)
        # Ausstieg
        held = pos != 0
        age[held] += 1
        ex = held & (((pos == -1) & valid & (s < theta_exit)) | ((pos == 1) & valid & (s > -theta_exit))
                     | (age >= max_hold))
        if can_exit is not None:
            ex &= can_exit[t]
        pos[ex] = 0
        age[ex] = 0
        # Einstieg (nur flach, Markt offen)
        flat = (pos == 0) & valid & can_enter[t] & ~ex
        pos[flat & (s > theta)] = -1
        pos[flat & (s < -theta)] = 1
        age[flat & (s > theta)] = 0
        age[flat & (s < -theta)] = 0
        out[t] = pos
    return out


def ts_meanrev(O: pd.DataFrame, mask: pd.DataFrame, vol: pd.DataFrame, theta: float, theta_exit: float,
               max_hold: int, budget: float = 0.05) -> pd.DataFrame:
    """Einzelasset: überhitzt -> short, unterkühlt -> long."""
    pos = hysteresis(O.values, mask[O.columns].values, theta, theta_exit, max_hold)
    return pd.DataFrame(pos, index=O.index, columns=O.columns) * budget / vol[O.columns]


def pair_meanrev(O: pd.DataFrame, mask: pd.DataFrame, vol: pd.DataFrame, pairs: list[tuple[str, str]],
                 theta: float, theta_exit: float, max_hold: int, budget: float = 0.01,
                 scale: float = 1.0) -> tuple[pd.DataFrame, np.ndarray]:
    """Paar-Mean-Reversion für viele (überlappende) Paare gleichzeitig.
    Spread = (O_a − O_b)/scale. Spread > theta: a relativ überhitzt -> short a / long b.
    Netto-Risikoeinheiten je Asset = Summe über alle offenen Paare (gegenläufige Beine heben sich auf)."""
    cols = list(O.columns)
    ci = {c: i for i, c in enumerate(cols)}
    ia = np.array([ci[a] for a, _ in pairs])
    ib = np.array([ci[b] for _, b in pairs])
    Ov, Mv = O.values, mask[cols].values
    S = (Ov[:, ia] - Ov[:, ib]) / scale
    enter = Mv[:, ia] & Mv[:, ib]
    pos = hysteresis(S, enter, theta, theta_exit, max_hold)
    T, N = len(O), len(cols)
    U = np.zeros((T, N))
    for p in range(len(pairs)):
        U[:, ia[p]] += pos[:, p]       # pos=+1: a unterkühlt -> long a
        U[:, ib[p]] -= pos[:, p]
    W = pd.DataFrame(U, index=O.index, columns=cols) * budget / vol[cols]
    return W, pos


def basket_signal(O: pd.DataFrame, groups: dict[str, list[str]]) -> pd.DataFrame:
    """Mittlere Überhitzung je Korb (z. B. Krypto-Korb, Hafen-Korb)."""
    return pd.DataFrame({g: O[[m for m in mem if m in O]].mean(axis=1) for g, mem in groups.items()})


def basket_pair_meanrev(O: pd.DataFrame, mask: pd.DataFrame, vol: pd.DataFrame, groups: dict[str, list[str]],
                        theta: float, theta_exit: float, max_hold: int, budget: float = 0.02,
                        scale: float = 1.0) -> pd.DataFrame:
    """Korb gegen Korb: Spread der Korb-Überhitzung; Beine sind risikogleich gewichtete Körbe."""
    B = basket_signal(O, groups)
    names = list(groups)
    pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
    Bv = B.values
    ci = {g: i for i, g in enumerate(names)}
    ia = np.array([ci[a] for a, _ in pairs])
    ib = np.array([ci[b] for _, b in pairs])
    S = (Bv[:, ia] - Bv[:, ib]) / scale
    # Korb handelbar, wenn mindestens die Hälfte der Mitglieder offen ist
    open_frac = pd.DataFrame({g: mask[[m for m in mem if m in mask]].mean(axis=1) for g, mem in groups.items()}).values
    enter = (open_frac[:, ia] >= 0.5) & (open_frac[:, ib] >= 0.5)
    pos = hysteresis(S, enter, theta, theta_exit, max_hold)
    U = np.zeros((len(O), len(names)))
    for p in range(len(pairs)):
        U[:, ia[p]] += pos[:, p]
        U[:, ib[p]] -= pos[:, p]
    W = pd.DataFrame(0.0, index=O.index, columns=O.columns)
    for g, mem in groups.items():
        mem = [m for m in mem if m in O]
        for m in mem:
            W[m] += U[:, ci[g]] * budget / len(mem) / vol[m]
    return W.fillna(0.0)


def xs_reversal(O: pd.DataFrame, mask: pd.DataFrame, vol: pd.DataFrame, k: int, rebalance: int, hold: int,
                budget: float = 0.05, groups: dict[str, list[str]] | None = None) -> pd.DataFrame:
    """Querschnitt: zu jedem Rebalancing-Zeitpunkt die k am stärksten unterkühlten Assets long, die k
    am stärksten überhitzten short; überlappende Portfolios über `hold` Stunden.
    Mit `groups`: Rangfolge innerhalb jeder Klasse (klassenneutral)."""
    Om = O.where(mask[O.columns])
    sig = pd.DataFrame(0.0, index=O.index, columns=O.columns)
    sets = groups.values() if groups else [list(O.columns)]
    for mem in sets:
        mem = [m for m in mem if m in O]
        if len(mem) < 2 * k + 1:
            continue
        sub = Om[mem]
        rk = sub.rank(axis=1)
        n = sub.notna().sum(axis=1)
        long_ = (rk <= k)
        short_ = rk.gt(n - k, axis=0) & sub.notna()
        sig[mem] += long_.astype(float) - short_.astype(float)
    reb = np.zeros(len(O), bool)
    reb[::rebalance] = True
    sig = sig.where(pd.Series(reb, index=O.index), np.nan).ffill().fillna(0.0)
    w = sig * budget / vol[O.columns]
    n_port = max(1, hold // rebalance)
    return w.rolling(n_port * rebalance, min_periods=1).mean().fillna(0.0) if n_port > 1 else w.fillna(0.0)
