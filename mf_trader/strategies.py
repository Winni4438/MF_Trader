"""Handelsstrategien auf Basis der Flow-Messung."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from mf_trader.universe import HAVEN, RISK


@dataclass
class RotationParams:
    window: int = 4              # Stunden für den Flow-Score (Erkennung)
    theta: float = 2.5           # Einstiegsschwelle für den standardisierten RORO-Score (z)
    exit_window: int = 2         # kurzer Flow-Score für 'Momentum lässt nach'
    theta_exit: float = 0.0      # Ausstieg, wenn kurzer RORO-z auf diese Schwelle zurückläuft
    max_hold: int = 8            # maximale Haltedauer in Stunden
    eod_flat: bool = True        # vor US-Schluss (16:00 New York) glattstellen
    dest_k: int = 2              # Anzahl Ziel-Assets (long)
    src_k: int = 0               # Anzahl Quell-Assets (short); 0 = nur long
    min_dest_flow: float = 0.5   # Ziel muss tatsächlich Zufluss zeigen (Flow-Score > x)
    min_breadth: float = 0.0     # Mindestanteil Risikoassets mit Abfluss
    direction: str = "both"      # 'off' | 'on' | 'both'
    per_leg_vol: float = 0.05    # Risikobudget je Bein (annualisiert)
    cooldown: int = 1
    fixed_dest_off: list | None = None   # z. B. ['GOLD','UST'] (Nutzer-Variante)
    fixed_src_off: list | None = None    # z. B. ['BTC','NDX']
    risk: list = field(default_factory=lambda: list(RISK))
    haven: list = field(default_factory=lambda: list(HAVEN))


def rotation_follower(p: RotationParams, F: pd.DataFrame, Fx_roro_z: pd.Series, roro_z: pd.Series,
                      vol: pd.DataFrame, mask: pd.DataFrame, breadth_df: pd.DataFrame | None = None,
                      allow_off: pd.Series | None = None, allow_on: pd.Series | None = None,
                      haven_ok: pd.DataFrame | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Event-getriebener 'Rotation Follower'.

    Einstieg, wenn der RORO-Score extrem wird (Kapital rotiert gerade), long in die Assets mit dem
    stärksten Zufluss auf der Zielseite, optional short in die Assets mit dem stärksten Abfluss.
    Ausstieg nach max_hold, wenn das kurzfristige Momentum nachlässt oder vor US-Schluss.
    haven_ok: optionale Matrix (bool), welche Häfen im aktuellen Tagesregime zulässig sind.
    """
    cols = list(F.columns)
    ci = {c: i for i, c in enumerate(cols)}
    T, N = F.shape
    Fv, V, M = F.values, vol[cols].values, mask[cols].values
    R, RX = roro_z.values, Fx_roro_z.values
    ny_hour = F.index.tz_convert("America/New_York").hour.values
    a_off = np.ones(T, bool) if allow_off is None else allow_off.reindex(F.index).fillna(False).values
    a_on = np.ones(T, bool) if allow_on is None else allow_on.reindex(F.index).fillna(False).values
    HO = None if haven_ok is None else haven_ok.reindex(index=F.index, columns=cols).fillna(True).values
    br = None if breadth_df is None else breadth_df.reindex(F.index)
    risk_idx = [ci[c] for c in p.risk if c in ci]
    haven_idx = [ci[c] for c in p.haven if c in ci]

    target = np.zeros((T, N))
    log = []
    in_trade, d, held, cool, w, t0 = False, 0, 0, 0, None, 0
    for t in range(T):
        if in_trade:
            held += 1
            fade = np.isfinite(RX[t]) and d * RX[t] < p.theta_exit
            eod = p.eod_flat and ny_hour[t] == 15
            if held >= p.max_hold or fade or eod:
                in_trade = False
                cool = p.cooldown
                log.append((F.index[t0], F.index[t], d, held, "max" if held >= p.max_hold else ("fade" if fade else "eod")))
                continue
            target[t] = w
            continue
        if cool > 0:
            cool -= 1
            continue
        if not np.isfinite(R[t]) or (p.eod_flat and ny_hour[t] in (15,)):
            continue
        d = 0
        if p.direction in ("off", "both") and R[t] <= -p.theta and a_off[t]:
            if br is None or br["risk_out"].iat[t] >= p.min_breadth:
                d = -1
        if d == 0 and p.direction in ("on", "both") and R[t] >= p.theta and a_on[t]:
            if br is None or br["risk_in"].iat[t] >= p.min_breadth:
                d = 1
        if d == 0:
            continue
        dest_pool = haven_idx if d == -1 else risk_idx
        src_pool = risk_idx if d == -1 else haven_idx
        if d == -1 and p.fixed_dest_off is not None:
            dest = [ci[c] for c in p.fixed_dest_off if c in ci and M[t, ci[c]]]
            src = [ci[c] for c in (p.fixed_src_off or []) if c in ci and M[t, ci[c]]]
        else:
            cand = [j for j in dest_pool if M[t, j] and np.isfinite(Fv[t, j]) and Fv[t, j] * 1 > p.min_dest_flow
                    and (HO is None or d == 1 or HO[t, j])]
            dest = sorted(cand, key=lambda j: -Fv[t, j])[: p.dest_k]
            scand = [j for j in src_pool if M[t, j] and np.isfinite(Fv[t, j]) and Fv[t, j] < -p.min_dest_flow]
            src = sorted(scand, key=lambda j: Fv[t, j])[: p.src_k] if p.src_k > 0 else []
        if not dest:
            continue
        w = np.zeros(N)
        for j in dest:
            if np.isfinite(V[t, j]) and V[t, j] > 0:
                w[j] = p.per_leg_vol / V[t, j]
        for j in src:
            if np.isfinite(V[t, j]) and V[t, j] > 0:
                w[j] = -p.per_leg_vol / V[t, j]
        if not np.any(w):
            continue
        target[t] = w
        in_trade, held, t0 = True, 0, t
    trades = pd.DataFrame(log, columns=["entry", "exit", "dir", "hours", "reason"])
    return pd.DataFrame(target, index=F.index, columns=cols), trades


def xs_momentum(F: pd.DataFrame, vol: pd.DataFrame, k: int = 3, hold: int = 4, per_leg_vol: float = 0.05,
                long_only: bool = False) -> pd.DataFrame:
    """Querschnitts-Rotation: long die k Assets mit stärkstem Zufluss, short die k mit stärkstem Abfluss.
    Überlappende Portfolios (Jegadeesh/Titman) -> Haltedauer `hold` Stunden ohne Rebalancing-Sprünge."""
    rk = F.rank(axis=1, ascending=False)
    n = F.notna().sum(axis=1)
    sig = (rk <= k).astype(float)
    if not long_only:
        sig = sig - (rk > n.values[:, None] - k).astype(float)
    sig = sig.where(F.notna(), 0.0)
    w = sig * per_leg_vol / vol[F.columns]
    return w.rolling(hold, min_periods=1).mean().fillna(0.0)


def pair_follow(Fa: pd.Series, Fb: pd.Series, theta: float, hold: int) -> pd.Series:
    """+1 = long A / short B, wenn Kapital messbar von B nach A fließt (Spread-Flow > theta)."""
    s = (Fa - Fb) / np.sqrt(2)
    sig = pd.Series(np.where(s > theta, 1.0, np.where(s < -theta, -1.0, 0.0)), index=s.index)
    return sig.rolling(hold, min_periods=1).mean()


@dataclass
class FadeParams:
    window: int = 4
    theta: float = 2.5
    wait: int = 2               # Stunden warten nach dem Signal (Erschöpfung abwarten)
    hold: int = 8               # Haltedauer
    k: int = 2                  # Anzahl Assets je Seite
    hedge: bool = False         # zusätzlich Gegenposition im Ziel-Asset (Hafen short)
    direction: str = "both"
    per_leg_vol: float = 0.05
    eod_flat: bool = False
    risk: list = field(default_factory=lambda: list(RISK))
    haven: list = field(default_factory=lambda: list(HAVEN))


def rotation_fader(p: FadeParams, F: pd.DataFrame, roro_z: pd.Series, vol: pd.DataFrame,
                   mask: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gegenhalten: Nach einer extremen Rotation `wait` Stunden warten und dann die
    stärksten Verlierer der Quellseite kaufen (bei Risk-off: Risikoassets), optional die
    Gewinner der Zielseite (Häfen) verkaufen. Testet die Umkehr-Hypothese aus der Literatur
    (Flow-Druck kehrt sich über Stunden/Tage teilweise um)."""
    cols = list(F.columns)
    ci = {c: i for i, c in enumerate(cols)}
    T, N = F.shape
    Fv, V, M, R = F.values, vol[cols].values, mask[cols].values, roro_z.values
    ny_hour = F.index.tz_convert("America/New_York").hour.values
    risk_idx = [ci[c] for c in p.risk if c in ci]
    haven_idx = [ci[c] for c in p.haven if c in ci]
    target = np.zeros((T, N))
    log = []
    busy_until = -1
    for t in range(T):
        if t <= busy_until or not np.isfinite(R[t]):
            continue
        d = 0
        if p.direction in ("off", "both") and R[t] <= -p.theta and not (t > 0 and R[t - 1] <= -p.theta):
            d = -1
        elif p.direction in ("on", "both") and R[t] >= p.theta and not (t > 0 and R[t - 1] >= p.theta):
            d = 1
        if d == 0:
            continue
        te = t + p.wait
        if te >= T:
            break
        # Gegenhalten bei Risk-off: Risikoassets mit dem stärksten Abfluss kaufen
        buy_pool = risk_idx if d == -1 else haven_idx
        sell_pool = haven_idx if d == -1 else risk_idx
        sgn = 1 if d == -1 else -1
        buy = sorted([j for j in buy_pool if np.isfinite(Fv[t, j]) and sgn * Fv[t, j] * -1 > 0],
                     key=lambda j: sgn * Fv[t, j])[: p.k]
        sell = sorted([j for j in sell_pool if np.isfinite(Fv[t, j]) and sgn * Fv[t, j] > 0],
                      key=lambda j: -sgn * Fv[t, j])[: p.k] if p.hedge else []
        w = np.zeros(N)
        for j in buy:
            if np.isfinite(V[te, j]) and V[te, j] > 0:
                w[j] = p.per_leg_vol / V[te, j]
        for j in sell:
            if np.isfinite(V[te, j]) and V[te, j] > 0:
                w[j] = -p.per_leg_vol / V[te, j]
        if not np.any(w):
            continue
        end = min(T - 1, te + p.hold - 1)
        for u in range(te, end + 1):
            if p.eod_flat and ny_hour[u] == 15:
                end = u - 1
                break
            target[u] = w
        busy_until = end
        log.append((F.index[t], F.index[te], d, end - te + 1))
    return pd.DataFrame(target, index=F.index, columns=cols), pd.DataFrame(log, columns=["signal", "entry", "dir", "hours"])
