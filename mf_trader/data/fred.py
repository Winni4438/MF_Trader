"""Tägliche Makro-/Stressreihen von FRED (ohne API-Key über fredgraph.csv)."""
from __future__ import annotations

import io
import time
import urllib.request

import pandas as pd

URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"


def series(sid: str, retries: int = 5) -> pd.Series:
    for k in range(retries):
        try:
            raw = urllib.request.urlopen(URL.format(sid=sid), timeout=60).read()
            df = pd.read_csv(io.BytesIO(raw), na_values=".")
            s = df.set_index(pd.to_datetime(df.iloc[:, 0]))[df.columns[1]].astype(float)
            s.name = sid
            return s
        except Exception:  # noqa: BLE001
            time.sleep(3 * (k + 1))
    raise RuntimeError(sid)
