"""Zusätzliche Daten für die Mean-Reversion-Studie: Altcoins, Funding/Open Interest, weitere HistData-Märkte, ETFs."""
import io
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mf_trader.data import binance, histdata, yahoo  # noqa: E402

RAW = ROOT / "data" / "raw"
what = sys.argv[1]

if what == "alts":
    for sym in ["SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT"]:
        out = RAW / "binance" / f"{sym}_h1.parquet"
        if out.exists():
            continue
        df = binance.download(sym, "2019-01", "2026-09", RAW / "binance" / "cache")
        df.to_parquet(out)
        print("done", sym, len(df), df.index[0], flush=True)

elif what == "funding":
    base = "https://data.binance.vision/data/futures/um/monthly/fundingRate/{s}/{s}-fundingRate-{y}-{m:02d}.zip"
    for sym in ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "BNBUSDT", "ADAUSDT"]:
        parts = []
        for p in pd.period_range("2019-09", "2026-09", freq="M"):
            try:
                blob = urllib.request.urlopen(base.format(s=sym, y=p.year, m=p.month), timeout=60).read()
            except Exception:  # noqa: BLE001
                continue
            with zipfile.ZipFile(io.BytesIO(blob)) as z:
                df = pd.read_csv(z.open(z.namelist()[0]))
            parts.append(df)
        df = pd.concat(parts)
        tcol = [c for c in df.columns if "time" in c.lower()][0]
        rcol = [c for c in df.columns if "rate" in c.lower() and "interval" not in c.lower()][0]
        t = pd.to_numeric(df[tcol], errors="coerce")
        s = pd.Series(pd.to_numeric(df[rcol], errors="coerce").values,
                      index=pd.to_datetime(t, unit="ms", utc=True)).sort_index()
        s = s[~s.index.duplicated()]
        s.to_frame("funding_rate").to_parquet(RAW / "binance" / f"{sym}_funding.parquet")
        print("done funding", sym, len(s), s.index[0], flush=True)

elif what == "metrics":
    base = "https://data.binance.vision/data/futures/um/daily/metrics/{s}/{s}-metrics-{d}.zip"
    for sym in ["BTCUSDT", "ETHUSDT"]:
        cache = RAW / "binance" / "metrics_cache" / sym
        cache.mkdir(parents=True, exist_ok=True)
        for d in pd.date_range("2021-12-01", "2026-09-30", freq="D"):
            f = cache / f"{d.date()}.parquet"
            if f.exists():
                continue
            try:
                blob = urllib.request.urlopen(base.format(s=sym, d=d.date()), timeout=60).read()
            except Exception:  # noqa: BLE001
                continue
            with zipfile.ZipFile(io.BytesIO(blob)) as z:
                df = pd.read_csv(z.open(z.namelist()[0]))
            df.to_parquet(f)
        parts = [pd.read_parquet(f) for f in sorted(cache.glob("*.parquet"))]
        df = pd.concat(parts)
        df.index = pd.to_datetime(df["create_time"], utc=True)
        num = df.select_dtypes("number")
        num.resample("1h").last().to_parquet(RAW / "binance" / f"{sym}_metrics_h1.parquet")
        print("done metrics", sym, len(df), df.index[0], flush=True)

elif what == "histdata":
    for p in ["UKXGBP", "FRXEUR", "AUXAUD", "GBPUSD", "USDCAD", "NZDUSD", "USDZAR", "USDNOK", "WTIUSD", "EURCHF"]:
        out = RAW / "histdata" / f"{p}_h1.parquet"
        if out.exists():
            continue
        try:
            df = histdata.download_pair(p, list(range(2018, 2026)), (2026, list(range(1, 10))), RAW / "histdata" / "cache")
            df.to_parquet(out)
            print("done", p, len(df), flush=True)
        except Exception as e:  # noqa: BLE001
            print("FAIL", p, e, flush=True)

elif what == "etf":
    for t in ["XLF", "XLE", "XLV", "XLI", "XLY", "XLB", "EWZ", "FXI", "EWG", "EWU", "EWY", "INDA", "EMB", "BWX",
              "UNG", "DBB", "WEAT", "CORN", "PPLT", "FXE", "FXB", "FXC", "MUB", "SHY", "IEF", "TLT", "IWM",
              "XME", "GDX", "SOXX", "XBI", "KWEB", "VGK", "EWA", "EWC", "EWW"]:
        f = RAW / "yahoo" / f"{t}_d1.parquet"
        if f.exists():
            continue
        try:
            df = yahoo.chart(t, "1d", "max")
            df.to_parquet(f)
            print("done", t, len(df), df.index[0].date(), flush=True)
        except Exception as e:  # noqa: BLE001
            print("FAIL", t, e, flush=True)
        time.sleep(1)
