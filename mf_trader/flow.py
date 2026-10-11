"""Flow-Messung: saisonal normalisierte Renditen, Flow-Scores, Risk-on/Risk-off-Faktor."""
from __future__ import annotations

import numpy as np
import pandas as pd


def seasonal_var(ret: pd.DataFrame, lookback_days: int = 60, min_days: int = 20) -> pd.DataFrame:
    """Erwartete Varianz je Asset und Stunde des Tages (UTC) aus den letzten N Tagen,
    strikt aus der Vergangenheit (shift), damit kein Look-ahead entsteht.
    Berücksichtigt, dass z. B. die US-Eröffnung volatiler ist als die Asien-Nacht."""
    r2 = ret.pow(2)
    hour = r2.index.hour
    out = r2.groupby(hour).transform(
        lambda s: s.rolling(lookback_days, min_periods=min_days).mean().shift(1))
    # Untergrenze: 5 % des mittleren Stundenrisikos, damit geschlossene Stunden nicht explodieren
    floor = out.rolling(24 * 250, min_periods=24 * 20).mean() * 0.05
    return out.clip(lower=floor)


def flow_score(ret: pd.DataFrame, svar: pd.DataFrame, window: int) -> pd.DataFrame:
    """Kumulierte Rendite der letzten `window` Stunden geteilt durch ihre erwartete
    Standardabweichung -> 'wie ungewöhnlich stark fließt gerade Geld in/aus diesem Asset'."""
    num = ret.rolling(window, min_periods=window).sum()
    den = np.sqrt(svar.rolling(window, min_periods=window).sum())
    return num / den


def roro(F: pd.DataFrame, risk: list[str], haven: list[str], clip: float = 4.0) -> pd.Series:
    """Risk-on/Risk-off-Score: mittlerer Flow der Risikoassets minus mittlerer Flow der Häfen.
    Negativ = Kapital flieht aus Risiko in Sicherheit. Einzelne Ausreißer (z. B. Zoll-News nur
    für Kupfer) werden auf ±clip begrenzt, damit eine 'Rotation' breit getragen sein muss."""
    Fc = F.clip(-clip, clip)
    r = Fc[[c for c in risk if c in Fc]].mean(axis=1)
    h = Fc[[c for c in haven if c in Fc]].mean(axis=1)
    return (r - h) / np.sqrt(2)


def standardize(x: pd.Series, window: int = 24 * 250, min_periods: int = 24 * 60) -> pd.Series:
    """Rollierende Standardisierung (nur Vergangenheit)."""
    m = x.rolling(window, min_periods=min_periods).mean().shift(1)
    s = x.rolling(window, min_periods=min_periods).std().shift(1)
    return (x - m) / s


def breadth(F: pd.DataFrame, risk: list[str], haven: list[str], c: float = 0.5) -> pd.DataFrame:
    """Anteil der Risikoassets mit Abfluss (F<-c) und der Häfen mit Zufluss (F>c).
    Echte Rotation = beides hoch; Liquidation ('dash for cash') = Risiko runter, Häfen auch runter."""
    rk = [c_ for c_ in risk if c_ in F]
    hv = [c_ for c_ in haven if c_ in F]
    return pd.DataFrame({
        "risk_out": (F[rk] < -c).sum(axis=1) / F[rk].notna().sum(axis=1),
        "haven_in": (F[hv] > c).sum(axis=1) / F[hv].notna().sum(axis=1),
        "risk_in": (F[rk] > c).sum(axis=1) / F[rk].notna().sum(axis=1),
        "haven_out": (F[hv] < -c).sum(axis=1) / F[hv].notna().sum(axis=1),
    })


def realized_daily_vol(ret: pd.DataFrame, days: int = 20) -> pd.DataFrame:
    """Annualisierte realisierte Volatilität aus Stundenrenditen der letzten N Tage (nur Vergangenheit)."""
    v = ret.pow(2).rolling(24 * days, min_periods=24 * 5).sum() / days
    return np.sqrt(v * 252).shift(1)
