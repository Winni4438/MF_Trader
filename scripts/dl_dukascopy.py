"""Lädt stündliche Dukascopy-Kerzen für Instrumente, die es bei HistData nicht gibt (Anleihen, Kupfer)."""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mf_trader.data.dukascopy import download  # noqa: E402

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "dukascopy"
# Symbol -> (Start, Dezimalfaktor)
INSTR = {
    "USTBONDTRUSD": ("2018-12", 1000.0),
    "BUNDTREUR": ("2018-06", 1000.0),
    "COPPERCMDUSD": ("2018-06", 10000.0),
}
EXTRA = {  # Erweiterung für die Mean-Reversion-Studie (Dezimalfaktor wird später empirisch geprüft)
    "UKGILTTRGBP": ("2018-06", 1000.0), "GASCMDUSD": ("2018-06", 1000.0), "SOYBEANCMDUSX": ("2018-06", 1000.0),
    "SUGARCMDUSD": ("2018-06", 1000.0), "COFFEECMDUSX": ("2018-06", 1000.0), "COCOACMDUSD": ("2018-06", 1000.0),
    "USSC2000IDXUSD": ("2018-08", 1000.0), "CHIIDXUSD": ("2018-06", 1000.0), "HKGIDXHKD": ("2018-06", 1000.0),
}
if "--extra" in sys.argv:
    INSTR = EXTRA
_only = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")]
if _only:
    INSTR = {k: v for k, v in EXTRA.items() if k in _only[0].split(",")}
END = next((a for a in sys.argv[1:] if not a.startswith("--")), "2026-09")

for sym, (start, fac) in INSTR.items():
    out = RAW / f"{sym}_h1.parquet"
    if out.exists():
        print("skip", sym, flush=True)
        continue
    t0 = time.time()
    df = download(sym, start, END, fac, cache_dir=RAW / "cache", workers=6)
    df.to_parquet(out)
    print("done", sym, len(df), df.index[0], df.index[-1], f"{time.time()-t0:.0f}s", flush=True)
