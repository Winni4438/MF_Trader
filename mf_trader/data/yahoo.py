"""Yahoo-Finance-Chart-API (ohne Key). Stündlich max. ~730 Tage, täglich ganze Historie."""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request

import pandas as pd

URL = "https://query2.finance.yahoo.com/v8/finance/chart/{t}?interval={i}&{r}&includePrePost=false"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def chart(ticker: str, interval: str = "1h", rng: str = "730d", retries: int = 6) -> pd.DataFrame:
    # range=max liefert bei langen Historien nur Monatswerte -> dann period1/period2 verwenden
    r = f"period1=0&period2={int(time.time())}" if rng == "max" else f"range={rng}"
    url = URL.format(t=urllib.parse.quote(ticker), i=interval, r=r)
    for k in range(retries):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60))
            res = d["chart"]["result"][0]
            q = res["indicators"]["quote"][0]
            df = pd.DataFrame({c: q.get(c) for c in ["open", "high", "low", "close", "volume"]},
                              index=pd.to_datetime(res["timestamp"], unit="s", utc=True))
            if "adjclose" in res["indicators"]:
                df["adjclose"] = res["indicators"]["adjclose"][0]["adjclose"]
            return df.dropna(subset=["close"])
        except Exception:  # noqa: BLE001
            time.sleep(3 * (k + 1))
    raise RuntimeError(f"yahoo failed: {ticker} {interval}")
