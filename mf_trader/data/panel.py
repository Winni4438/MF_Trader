"""Baut ein synchrones Stunden-Panel (UTC) aus den Rohdaten aller Quellen."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from mf_trader.data.histdata import fix_utc_index
from mf_trader.universe import UNIVERSE

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
ROLL_REPORT: list = []


# Roll-Fenster für Future-basierte Reihen: Liste von (Monat, Tag von, Tag bis)
ROLL_WINDOWS = {
    # ZB: Wechsel vor First Notice Day Ende Feb/Mai/Aug/Nov (bis Anfang Folgemonat)
    "UST": [(m, 18, 31) for m in (2, 5, 8, 11)] + [(m, 1, 5) for m in (3, 6, 9, 12)],
    # FGBL: Liefertag 10. Mrz/Jun/Sep/Dez, Wechsel in den Tagen davor
    "BUND": [(m, 1, 12) for m in (3, 6, 9, 12)] + [(m, 25, 31) for m in (2, 5, 8, 11)],
}


def clean_roll_gaps(df: pd.DataFrame, key: str, report: list | None = None,
                    ref: pd.Series | None = None) -> pd.DataFrame:
    """Entfernt Roll-Sprünge (Kontraktwechsel) an Sitzungseröffnungen innerhalb der Roll-Fenster
    per Back-Adjustment. Ein Sprung gilt als Roll, wenn er der größte Eröffnungs-Gap im Fenster ist
    und das 99,5%-Quantil normaler Eröffnungs-Gaps übersteigt."""
    if key not in ROLL_WINDOWS:
        return df
    c = df["close"]
    lr = np.log(c).diff()
    is_open = c.index.to_series().diff() > pd.Timedelta(hours=1)
    in_win = np.zeros(len(c), bool)
    for m, d0, d1 in ROLL_WINDOWS[key]:
        in_win |= (c.index.month == m) & (c.index.day >= d0) & (c.index.day <= d1)
    # Fenster-ID: Roll-Quartal (Ende Feb + Anfang Mrz gehören zusammen)
    qid = pd.Series((c.index + pd.Timedelta(days=10)).to_period("Q").astype(str), index=c.index)
    adj = pd.Series(0.0, index=c.index)
    if ref is None:
        # nur Sitzungseröffnungen betrachten (Rolls passieren über Nacht)
        normal = lr[is_open & ~in_win].abs()
        thr = normal.quantile(0.995)
        cand = lr[is_open & in_win]
        score = cand.abs()
    else:
        # Rolls auch innerhalb der Sitzung: Residuum ggü. Referenzmarkt (echte Zinsbewegungen
        # laufen parallel in anderen Anleihemärkten, ein Kontraktwechsel nicht)
        r_ref = ref.reindex(lr.index).fillna(0.0)
        ok = lr.notna()
        beta = np.polyfit(r_ref[ok & ~in_win], lr[ok & ~in_win], 1)[0]
        resid = (lr - beta * r_ref)
        thr = resid[~in_win].abs().quantile(0.999)
        cand = lr[in_win & ok]
        score = resid[in_win & ok].abs()
    for _, g in score.groupby(qid[score.index]):
        t = g.idxmax()
        if g[t] > thr:
            adj[t] = lr[t]
            if report is not None:
                report.append((key, str(t), round(float(lr[t]) * 100, 3)))
    # Back-Adjustment: alle Preise vor dem Sprung um den Sprung verschieben
    factor = np.exp(-adj[::-1].cumsum()[::-1].shift(-1).fillna(0.0))
    out = df.copy()
    for col in ("open", "high", "low", "close"):
        out[col] = df[col] / factor
    return out


SPIKE_REPORT: list = []


def remove_spikes(df: pd.DataFrame, key: str, k: float = 30.0, min_abs: float = 0.10) -> pd.DataFrame:
    """Datenbereinigung für Fehl-Ticks und Niveaubrüche.

    1) Isolierter Fehl-Tick: |Rendite| > max(k * rollierende Median-Absolutrendite, min_abs) und
       die nächste Stunde kehrt fast vollständig um -> Bar verwerfen. (Echte Schocks wie FTX oder
       der 9. April 2025 bleiben erhalten, weil sie nicht in einer Stunde komplett umkehren.)
    2) Niveaubruch: |Rendite| > 40 % ohne Umkehr (z. B. HistData 'GRXEUR' liefert von 06/2020 bis
       12/2023 Euro-Stoxx-50-Niveaus statt DAX) -> per Back-Adjustment verketten."""
    c = df["close"]
    lr = np.log(c).diff()
    mad = lr.abs().rolling(500, min_periods=50).median().shift(1)
    nxt = lr.shift(-1)
    spike = ((lr.abs() > np.maximum(k * mad, min_abs)) & (np.sign(nxt) == -np.sign(lr))
             & ((lr + nxt).abs() < 0.1 * lr.abs())).fillna(False)
    for t in lr.index[spike]:
        SPIKE_REPORT.append((key, "Fehl-Tick", str(t), round(float(lr[t]) * 100, 2)))
    df = df[~spike]
    lr = np.log(df["close"]).diff()
    brk = (lr.abs() > 0.4).fillna(False)
    if brk.any():
        adj = lr.where(brk, 0.0)
        factor = np.exp(-adj[::-1].cumsum()[::-1].shift(-1).fillna(0.0))
        df = df.copy()
        for col in ("open", "high", "low", "close"):
            df[col] = df[col] / factor
        for t in lr.index[brk]:
            SPIKE_REPORT.append((key, "Niveaubruch", str(t), round(float(lr[t]) * 100, 2)))
    return df


def _load(inst) -> pd.DataFrame:
    if inst.source == "histdata":
        df = fix_utc_index(pd.read_parquet(RAW / "histdata" / f"{inst.symbol}_h1.parquet"))
        df = df[df["n_min"] >= 5]  # Stunden mit nur vereinzelten Ticks verwerfen
    elif inst.source == "dukascopy":
        df = pd.read_parquet(RAW / "dukascopy" / f"{inst.symbol}_h1.parquet")
        ref = None
        if inst.key == "BUND":
            ust = clean_roll_gaps(pd.read_parquet(RAW / "dukascopy" / "USTBONDTRUSD_h1.parquet"), "UST")
            ref = np.log(ust["close"]).diff()
        df = clean_roll_gaps(df, inst.key, ROLL_REPORT, ref)
    elif inst.source == "binance":
        df = pd.read_parquet(RAW / "binance" / f"{inst.symbol}_h1.parquet")
        df = df[df["volume"] > 0]
    else:
        raise ValueError(inst.source)
    df = df[["open", "high", "low", "close"] + [c for c in ("taker_buy_quote", "quote_volume") if c in df]]
    df = remove_spikes(df, inst.key)
    if inst.invert:
        o, h, l, c = 1 / df["open"], 1 / df["low"], 1 / df["high"], 1 / df["close"]
        df = df.assign(open=o, high=h, low=l, close=c)
    return df.sort_index()


def build_hourly(start="2019-01-01", end="2026-10-01", keys=None) -> dict[str, pd.DataFrame]:
    """Gibt dict mit 'close' (ffilled), 'open_mask' (Bar existiert), 'ret' (log-Returns close-to-close)."""
    insts = [i for i in UNIVERSE if keys is None or i.key in keys]
    idx = pd.date_range(start, end, freq="1h", tz="UTC", inclusive="left")
    close, opn, mask, extra = {}, {}, {}, {}
    for inst in insts:
        try:
            df = _load(inst)
        except FileNotFoundError:
            print("fehlt:", inst.key)
            continue
        df = df[~df.index.duplicated()].reindex(idx)
        mask[inst.key] = df["close"].notna()
        close[inst.key] = df["close"]
        opn[inst.key] = df["open"]
        if "taker_buy_quote" in df:
            extra[inst.key + "_taker_ratio"] = df["taker_buy_quote"] / df["quote_volume"]
    close = pd.DataFrame(close)
    mask = pd.DataFrame(mask)
    first_valid = close.apply(lambda s: s.first_valid_index())
    cf = close.ffill()
    ret = np.log(cf).diff()
    # vor Beginn der Historie eines Instruments: NaN lassen
    for k, t0 in first_valid.items():
        ret.loc[:t0, k] = np.nan
        mask.loc[:t0, k] = False
    return {"close": cf, "open": pd.DataFrame(opn), "mask": mask, "ret": ret, "extra": pd.DataFrame(extra)}


def save_hourly(panel: dict[str, pd.DataFrame], name="hourly"):
    PROC.mkdir(parents=True, exist_ok=True)
    for k, v in panel.items():
        v.to_parquet(PROC / f"{name}_{k}.parquet")


def load_hourly(name="hourly") -> dict[str, pd.DataFrame]:
    return {k: pd.read_parquet(PROC / f"{name}_{k}.parquet") for k in ("close", "open", "mask", "ret", "extra")}
