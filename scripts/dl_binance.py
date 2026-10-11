import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mf_trader.data.binance import download  # noqa: E402

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "binance"
for sym in ["BTCUSDT", "ETHUSDT"]:
    df = download(sym, "2018-01", "2026-09", RAW / "cache")
    df.to_parquet(RAW / f"{sym}_h1.parquet")
    print("done", sym, len(df), df.index[0], df.index[-1], flush=True)
