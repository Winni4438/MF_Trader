import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mf_trader.data.fred import series  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "raw" / "fred_daily.parquet"
IDS = ["VIXCLS", "DGS10", "DGS2", "DGS3MO", "T10Y2Y", "T10YIE", "BAMLH0A0HYM2", "BAMLC0A0CM",
       "DTWEXBGS", "DEXJPUS", "DEXSZUS", "DEXUSEU", "SP500", "NASDAQCOM", "DCOILWTICO",
       "STLFSI4", "NFCI", "SOFR", "OVXCLS", "GVZCLS"]
cols = {}
for i in IDS:
    try:
        cols[i] = series(i)
        print("ok", i, cols[i].index[0].date(), cols[i].index[-1].date(), flush=True)
    except Exception as e:  # noqa: BLE001
        print("FAIL", i, e, flush=True)
pd.DataFrame(cols).to_parquet(OUT)
