import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mf_trader.data.yahoo import chart  # noqa: E402

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "yahoo"
RAW.mkdir(parents=True, exist_ok=True)
FUT = ["ES=F", "NQ=F", "RTY=F", "ZT=F", "ZF=F", "ZN=F", "ZB=F", "GC=F", "SI=F", "HG=F", "CL=F",
       "BZ=F", "6J=F", "6S=F", "6E=F", "6A=F", "DX=F", "BTC=F"]
IDX = ["^VIX", "^VIX3M", "^VVIX", "^MOVE", "^GSPC", "^NDX", "^TNX", "^IRX"]
ETF = ["SPY", "QQQ", "IWM", "TLT", "IEF", "SHY", "GLD", "HYG", "LQD", "XLU", "XLP", "XLK", "UUP",
       "FXY", "FXF", "EEM", "IBIT", "SMH", "KRE"]
FX = ["JPY=X", "CHF=X", "EURUSD=X", "AUDJPY=X", "MXN=X", "BTC-USD", "ETH-USD"]
for t in FUT + IDX + ETF + FX:
    safe = t.replace("=", "_").replace("^", "IDX_").replace("-", "_")
    for interval, rng, tag in [("1h", "730d", "h1"), ("1d", "max", "d1")]:
        f = RAW / f"{safe}_{tag}.parquet"
        if f.exists():
            continue
        try:
            df = chart(t, interval, rng)
            df.to_parquet(f)
            print("done", t, tag, len(df), df.index[0], df.index[-1], flush=True)
        except Exception as e:  # noqa: BLE001
            print("FAIL", t, tag, e, flush=True)
        time.sleep(1.0)
