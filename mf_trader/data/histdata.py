"""Downloader für freie 1-Minuten-Daten von histdata.com (FX, Gold, Silber, Öl, Indizes-CFDs).

Zeitstempel bei HistData: laut Doku "EST ohne Sommerzeit" (fix UTC-5). Der Abgleich mit
Yahoo-Futures und Dukascopy (2019, 2021, 2023, 2024-2026) zeigt aber eindeutig: Die Daten folgen
der New Yorker Ortszeit MIT Sommerzeit. _parse() speichert zunächst "Ortszeit + 5h";
fix_utc_index() korrigiert das auf echtes UTC. Ohne diese Korrektur liegen alle Reihen im
Sommer eine Stunde zu spät und erzeugen Schein-Lead-Lag-Effekte (z. B. "BTC führt Nasdaq").
"""
from __future__ import annotations

import http.cookiejar
import io
import re
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

BASE = "https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/{pair}/{path}"
GET = "https://www.histdata.com/get.php"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def _opener():
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def _download_zip(pair: str, year: int, month: int | None, retries: int = 6) -> bytes:
    path = f"{year}" if month is None else f"{year}/{month}"
    page_url = BASE.format(pair=pair.lower(), path=path)
    for attempt in range(retries):
        try:
            op = _opener()
            html = op.open(urllib.request.Request(page_url, headers={"User-Agent": UA}), timeout=60).read().decode("utf-8", "ignore")
            fields = dict(re.findall(r'name="(tk|date|datemonth|platform|timeframe|fxpair)" id="\w+" value="([^"]*)"', html))
            if "tk" not in fields:
                raise RuntimeError("no token")
            req = urllib.request.Request(GET, data=urllib.parse.urlencode(fields).encode(),
                                         headers={"User-Agent": UA, "Referer": page_url})
            blob = op.open(req, timeout=180).read()
            if blob[:2] != b"PK":
                raise RuntimeError("not a zip")
            return blob
        except Exception as e:  # noqa: BLE001
            time.sleep(5 * (attempt + 1))
            last = e
    raise RuntimeError(f"histdata failed {pair} {path}: {last}")


def _parse(blob: bytes) -> pd.DataFrame:
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        name = [n for n in z.namelist() if n.endswith(".csv")][0]
        df = pd.read_csv(z.open(name), sep=";", header=None,
                         names=["ts", "open", "high", "low", "close", "vol"], dtype={"ts": str})
    ts = pd.to_datetime(df["ts"], format="%Y%m%d %H%M%S") + pd.Timedelta(hours=5)
    df.index = ts.dt.tz_localize("UTC")
    return df[["open", "high", "low", "close"]]


def fix_utc_index(df: pd.DataFrame) -> pd.DataFrame:
    """Index 'NY-Ortszeit + 5h' -> echtes UTC (Sommerzeit berücksichtigt)."""
    local = (df.index.tz_convert(None) - pd.Timedelta(hours=5))
    utc = local.tz_localize("America/New_York", ambiguous="NaT", nonexistent="NaT").tz_convert("UTC")
    out = df.copy()
    out.index = utc
    out = out[out.index.notna()]
    return out[~out.index.duplicated(keep="first")]


def to_hourly(m1: pd.DataFrame) -> pd.DataFrame:
    g = m1.resample("1h", label="left", closed="left")
    h = pd.DataFrame({"open": g["open"].first(), "high": g["high"].max(), "low": g["low"].min(),
                      "close": g["close"].last(), "n_min": g["close"].count()})
    return h[h["n_min"] > 0]


def download_pair(pair: str, years: list[int], months_current: tuple[int, list[int]] | None,
                  cache_dir: Path) -> pd.DataFrame:
    cache_dir.mkdir(parents=True, exist_ok=True)
    jobs = [(y, None) for y in years]
    if months_current:
        jobs += [(months_current[0], m) for m in months_current[1]]
    parts = []
    for y, m in jobs:
        cf = cache_dir / f"{pair}_{y}{'' if m is None else f'_{m:02d}'}_h1.parquet"
        if not cf.exists():
            h = to_hourly(_parse(_download_zip(pair, y, m)))
            h.to_parquet(cf)
            time.sleep(1.5)
        parts.append(pd.read_parquet(cf))
    df = pd.concat(parts).sort_index()
    return df[~df.index.duplicated(keep="last")]
