"""Definition des Cross-Asset-Universums.

role:   'risk'   = Risikoasset (Kapital fließt bei Risk-off ab)
        'haven'  = (potentieller) sicherer Hafen
        'other'  = konjunktur-/inflationsgetrieben, keine feste Rolle (z. B. Öl, USD)
invert: True, wenn die Quelle als USD/XXX notiert und wir die Fremdwährung long betrachten
        (JPY = -USDJPY, CHF = -USDCHF, MXN = -USDMXN)
cost_bps: geschätzte Kosten pro Seite (Spread/2 + Kommission + Slippage) für ein
          automatisiertes Retail-Konto (IBKR-Futures bzw. Krypto-Perps), Normalbedingungen.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Instrument:
    key: str
    source: str        # histdata | dukascopy | binance
    symbol: str
    asset_class: str
    role: str
    invert: bool
    cost_bps: float
    vehicle: str       # womit man es in der Praxis handeln würde


UNIVERSE = [
    Instrument("SPX", "histdata", "SPXUSD", "Aktien USA", "risk", False, 1.0, "ES / MES Futures"),
    Instrument("NDX", "histdata", "NSXUSD", "Aktien USA Tech", "risk", False, 1.0, "NQ / MNQ Futures"),
    Instrument("DAX", "histdata", "GRXEUR", "Aktien Europa (DAX; 06/2020–12/2023 Euro Stoxx 50)", "risk", False, 1.2, "FDAX / FDXM / FESX Futures"),
    Instrument("NKY", "histdata", "JPXJPY", "Aktien Japan", "risk", False, 2.0, "NKD / MNK Futures"),
    Instrument("BTC", "binance", "BTCUSDT", "Krypto", "risk", False, 5.0, "BTC-Perp / MBT Futures"),
    Instrument("ETH", "binance", "ETHUSDT", "Krypto", "risk", False, 6.0, "ETH-Perp / MET Futures"),
    Instrument("AUDJPY", "histdata", "AUDJPY", "FX Carry", "risk", False, 1.0, "Spot-FX / 6A-6J"),
    Instrument("MXN", "histdata", "USDMXN", "FX EM-Carry", "risk", True, 2.0, "Spot-FX / 6M Futures"),
    Instrument("COPPER", "dukascopy", "COPPERCMDUSD", "Industriemetalle", "risk", False, 2.0, "HG / MHG Futures"),
    Instrument("UST", "dukascopy", "USTBONDTRUSD", "Staatsanleihen USA lang", "haven", False, 1.5, "ZB / ZN Futures"),
    Instrument("BUND", "dukascopy", "BUNDTREUR", "Staatsanleihen DE", "haven", False, 1.0, "FGBL Futures"),
    Instrument("GOLD", "histdata", "XAUUSD", "Edelmetalle", "haven", False, 1.0, "GC / MGC Futures"),
    Instrument("JPY", "histdata", "USDJPY", "FX sicherer Hafen", "haven", True, 0.7, "6J Futures / Spot-FX"),
    Instrument("CHF", "histdata", "USDCHF", "FX sicherer Hafen", "haven", True, 0.7, "6S Futures / Spot-FX"),
    Instrument("USD", "histdata", "UDXUSD", "US-Dollar", "other", False, 1.0, "DX Futures / Spot-FX"),
    Instrument("OIL", "histdata", "BCOUSD", "Energie (Brent)", "other", False, 1.5, "BZ / CL / MCL Futures"),
    Instrument("SILVER", "histdata", "XAGUSD", "Edelmetalle", "other", False, 2.0, "SI / SIL Futures"),
]

BY_KEY = {i.key: i for i in UNIVERSE}
RISK = [i.key for i in UNIVERSE if i.role == "risk"]
HAVEN = [i.key for i in UNIVERSE if i.role == "haven"]


# ---------------------------------------------------------------------------
# Erweitertes Universum für die Mean-Reversion-Studie ("Überhitzung")
# Klassen: Aktien, Anleihen, Edelmetalle, Industriemetalle, Energie, Agrar, Währungen, Krypto.
# Währungen jeweils als Fremdwährung gegen USD (long = Fremdwährung steigt).
MR_UNIVERSE = [
    # Aktienindizes
    Instrument("SPX", "histdata", "SPXUSD", "Aktien", "risk", False, 1.0, "ES / MES"),
    Instrument("NDX", "histdata", "NSXUSD", "Aktien", "risk", False, 1.0, "NQ / MNQ"),
    Instrument("RUT", "dukascopy", "USSC2000IDXUSD", "Aktien", "risk", False, 1.5, "RTY / M2K"),
    Instrument("DAX", "histdata", "GRXEUR", "Aktien", "risk", False, 1.2, "FDAX / FDXM"),
    Instrument("CAC", "histdata", "FRXEUR", "Aktien", "risk", False, 1.5, "FCE"),
    Instrument("FTSE", "histdata", "UKXGBP", "Aktien", "risk", False, 1.5, "Z (ICE)"),
    Instrument("NKY", "histdata", "JPXJPY", "Aktien", "risk", False, 2.0, "NKD / MNK"),
    Instrument("HSI", "dukascopy", "HKGIDXHKD", "Aktien", "risk", False, 2.0, "HSI / MHI"),
    Instrument("CN50", "dukascopy", "CHIIDXUSD", "Aktien", "risk", False, 2.5, "SGX FTSE China A50"),
    Instrument("ASX", "histdata", "AUXAUD", "Aktien", "risk", False, 2.0, "SPI 200"),
    # Staatsanleihen
    Instrument("UST", "dukascopy", "USTBONDTRUSD", "Anleihen", "haven", False, 1.5, "ZB / ZN"),
    Instrument("BUND", "dukascopy", "BUNDTREUR", "Anleihen", "haven", False, 1.0, "FGBL"),
    Instrument("GILT", "dukascopy", "UKGILTTRGBP", "Anleihen", "haven", False, 1.5, "Long Gilt (ICE)"),
    # Edelmetalle
    Instrument("GOLD", "histdata", "XAUUSD", "Edelmetalle", "haven", False, 1.0, "GC / MGC"),
    Instrument("SILVER", "histdata", "XAGUSD", "Edelmetalle", "other", False, 2.0, "SI / SIL"),
    # Industriemetalle
    Instrument("COPPER", "dukascopy", "COPPERCMDUSD", "Industriemetalle", "risk", False, 2.0, "HG / MHG"),
    # Energie
    Instrument("BRENT", "histdata", "BCOUSD", "Energie", "other", False, 1.5, "BZ"),
    Instrument("WTI", "histdata", "WTIUSD", "Energie", "other", False, 1.5, "CL / MCL"),
    Instrument("NATGAS", "dukascopy", "GASCMDUSD", "Energie", "other", False, 3.0, "NG / QG"),
    # Agrar
    Instrument("SOY", "dukascopy", "SOYBEANCMDUSX", "Agrar", "other", False, 3.0, "ZS"),
    Instrument("SUGAR", "dukascopy", "SUGARCMDUSD", "Agrar", "other", False, 4.0, "SB / White Sugar"),
    Instrument("COFFEE", "dukascopy", "COFFEECMDUSX", "Agrar", "other", False, 4.0, "KC"),
    Instrument("COCOA", "dukascopy", "COCOACMDUSD", "Agrar", "other", False, 4.0, "CC"),
    # Währungen (gegen USD)
    Instrument("EUR", "histdata", "EURUSD", "Währungen", "other", False, 0.5, "6E / Spot-FX"),
    Instrument("GBP", "histdata", "GBPUSD", "Währungen", "other", False, 0.6, "6B / Spot-FX"),
    Instrument("JPY", "histdata", "USDJPY", "Währungen", "haven", True, 0.6, "6J / Spot-FX"),
    Instrument("CHF", "histdata", "USDCHF", "Währungen", "haven", True, 0.7, "6S / Spot-FX"),
    Instrument("AUD", "histdata", "AUDUSD", "Währungen", "risk", False, 0.7, "6A / Spot-FX"),
    Instrument("NZD", "histdata", "NZDUSD", "Währungen", "risk", False, 0.9, "6N / Spot-FX"),
    Instrument("CAD", "histdata", "USDCAD", "Währungen", "risk", True, 0.7, "6C / Spot-FX"),
    Instrument("NOK", "histdata", "USDNOK", "Währungen", "risk", True, 1.5, "Spot-FX"),
    Instrument("MXN", "histdata", "USDMXN", "Währungen", "risk", True, 2.0, "6M / Spot-FX"),
    Instrument("ZAR", "histdata", "USDZAR", "Währungen", "risk", True, 2.5, "Spot-FX"),
    # Krypto
    Instrument("BTC", "binance", "BTCUSDT", "Krypto", "risk", False, 5.0, "BTC-Perp / MBT"),
    Instrument("ETH", "binance", "ETHUSDT", "Krypto", "risk", False, 6.0, "ETH-Perp / MET"),
    Instrument("SOL", "binance", "SOLUSDT", "Krypto", "risk", False, 7.0, "SOL-Perp"),
    Instrument("BNB", "binance", "BNBUSDT", "Krypto", "risk", False, 7.0, "BNB-Perp"),
    Instrument("XRP", "binance", "XRPUSDT", "Krypto", "risk", False, 7.0, "XRP-Perp"),
    Instrument("ADA", "binance", "ADAUSDT", "Krypto", "risk", False, 8.0, "ADA-Perp"),
    Instrument("DOGE", "binance", "DOGEUSDT", "Krypto", "risk", False, 8.0, "DOGE-Perp"),
    Instrument("AVAX", "binance", "AVAXUSDT", "Krypto", "risk", False, 8.0, "AVAX-Perp"),
    Instrument("LINK", "binance", "LINKUSDT", "Krypto", "risk", False, 8.0, "LINK-Perp"),
    Instrument("LTC", "binance", "LTCUSDT", "Krypto", "risk", False, 8.0, "LTC-Perp"),
]
MR_BY_KEY = {i.key: i for i in MR_UNIVERSE}
# Kosten-Lookup für den Backtester: MR-Instrumente ergänzen (gleiche Schlüssel haben gleiche Kosten)
for _i in MR_UNIVERSE:
    BY_KEY.setdefault(_i.key, _i)
