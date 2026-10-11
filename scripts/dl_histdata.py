"""Lädt HistData-1-Minuten-Daten und speichert Stundenkerzen je Instrument."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mf_trader.data.histdata import download_pair  # noqa: E402

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "histdata"
PAIRS = ["SPXUSD", "NSXUSD", "XAUUSD", "USDJPY", "USDCHF", "EURUSD", "AUDJPY", "WTIUSD",
         "GRXEUR", "JPXJPY", "XAGUSD", "UDXUSD", "AUDUSD", "BCOUSD", "USDMXN", "ETXEUR"]
YEARS = list(range(2018, 2026))
CURRENT = (2026, list(range(1, 10)))

for p in PAIRS:
    out = RAW / f"{p}_h1.parquet"
    if out.exists():
        print("skip", p, flush=True)
        continue
    t0 = time.time()
    try:
        df = download_pair(p, YEARS, CURRENT, RAW / "cache")
        df.to_parquet(out)
        print("done", p, len(df), df.index[0], df.index[-1], f"{time.time()-t0:.0f}s", flush=True)
    except Exception as e:  # noqa: BLE001
        print("FAIL", p, e, flush=True)
