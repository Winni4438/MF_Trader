"""Krypto-Stundenkerzen inkl. Taker-Buy-Volumen (echter Orderflow) von data.binance.vision."""
from __future__ import annotations

import io
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

URL = "https://data.binance.vision/data/spot/monthly/klines/{sym}/1h/{sym}-1h-{y}-{m:02d}.zip"
COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume",
        "trades", "taker_buy_base", "taker_buy_quote", "ignore"]


def _get(url: str, retries: int = 6) -> bytes | None:
    for i in range(retries):
        try:
            return urllib.request.urlopen(url, timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
        except Exception:  # noqa: BLE001
            pass
        time.sleep(2 * (i + 1))
    raise RuntimeError(url)


def download(sym: str, start: str, end: str, cache_dir: Path) -> pd.DataFrame:
    cache_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    for p in pd.period_range(start, end, freq="M"):
        cf = cache_dir / f"{sym}_{p.year}_{p.month:02d}.parquet"
        if not cf.exists():
            blob = _get(URL.format(sym=sym, y=p.year, m=p.month))
            if blob is None:
                continue
            with zipfile.ZipFile(io.BytesIO(blob)) as z:
                df = pd.read_csv(z.open(z.namelist()[0]), header=None, names=COLS)
            if not str(df.iloc[0, 0]).isdigit():  # Header-Zeile in neueren Dateien
                df = df.iloc[1:].astype(float)
            t = df["open_time"].astype("int64")
            unit = "us" if t.iloc[0] > 10**14 else "ms"  # ab 2025 Mikrosekunden
            df.index = pd.to_datetime(t, unit=unit, utc=True)
            df = df[["open", "high", "low", "close", "volume", "quote_volume", "trades",
                     "taker_buy_base", "taker_buy_quote"]].astype(float)
            df.to_parquet(cf)
        parts.append(pd.read_parquet(cf))
    df = pd.concat(parts).sort_index()
    return df[~df.index.duplicated()]
