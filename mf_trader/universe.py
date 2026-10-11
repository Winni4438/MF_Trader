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
