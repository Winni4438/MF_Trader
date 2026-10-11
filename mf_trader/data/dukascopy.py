"""Downloader für stündliche Dukascopy-Kerzen (frei verfügbar, ~24h-Handel, CFD/Spot-Preise).

Dateiformat: pro Monat eine LZMA-komprimierte .bi5-Datei mit 24-Byte-Records
(int32 Sekunden-Offset, int32 open, int32 close, int32 low, int32 high, float32 volume),
Big Endian. Monate sind 0-indiziert. Preise sind Ganzzahlen / decimal_factor.
"""
from __future__ import annotations

import lzma
import struct
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

URL = "https://datafeed.dukascopy.com/datafeed/{sym}/{y}/{m:02d}/{side}_candles_hour_1.bi5"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) MF_Trader research"}


def _fetch(url: str, retries: int = 40) -> bytes | None:
    delay = 1.0
    for _ in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=40) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
        except Exception:
            pass
        time.sleep(delay)
        delay = min(delay * 1.3, 15)
    raise RuntimeError(f"download failed: {url}")


def _decode(blob: bytes, month_start: pd.Timestamp) -> pd.DataFrame:
    if not blob:
        return pd.DataFrame()
    raw = lzma.decompress(blob)
    n = len(raw) // 24
    arr = np.frombuffer(raw[: n * 24], dtype=np.dtype([("t", ">i4"), ("o", ">i4"), ("c", ">i4"),
                                                       ("l", ">i4"), ("h", ">i4"), ("v", ">f4")]))
    idx = month_start + pd.to_timedelta(arr["t"].astype(np.int64), unit="s")
    return pd.DataFrame({"open": arr["o"].astype(float), "high": arr["h"].astype(float),
                         "low": arr["l"].astype(float), "close": arr["c"].astype(float),
                         "volume": arr["v"].astype(float)}, index=idx)


def download_month(sym: str, year: int, month: int, side: str = "BID") -> pd.DataFrame:
    """month: 1..12"""
    blob = _fetch(URL.format(sym=sym, y=year, m=month - 1, side=side))
    return _decode(blob, pd.Timestamp(year=year, month=month, day=1, tz="UTC")) if blob else pd.DataFrame()


def download(sym: str, start: str, end: str, decimal_factor: float, side: str = "BID",
             cache_dir: Path | None = None, workers: int = 2) -> pd.DataFrame:
    months = pd.period_range(start, end, freq="M")
    cache_dir = Path(cache_dir) if cache_dir else None

    def one(p: pd.Period) -> pd.DataFrame:
        cf = cache_dir / f"{sym}_{side}_{p.year}_{p.month:02d}.parquet" if cache_dir else None
        if cf is not None and cf.exists():
            return pd.read_parquet(cf)
        df = download_month(sym, p.year, p.month, side)
        if cf is not None:
            cf.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(cf)
        return df

    with ThreadPoolExecutor(max_workers=workers) as ex:
        parts = list(ex.map(one, months))
    df = pd.concat([p for p in parts if len(p)]).sort_index()
    df = df[~df.index.duplicated()]
    df[["open", "high", "low", "close"]] /= decimal_factor
    # Stunden ohne Handel sind als flache Kerze mit volume==0 kodiert -> entfernen
    return df[df["volume"] > 0]
