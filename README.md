# MF_Trader – Money-Flow- / Kapitalrotations-Research

Recherche- und Simulationsprojekt zur Frage: **Kann man Kapitalrotationen zwischen Anlageklassen
(z. B. Risk-off: Nasdaq/Bitcoin → Gold/Anleihen/Yen/Franken) erkennen, *während* sie stattfinden,
und gewinnbringend auf den fahrenden Zug aufspringen?** Fokus: Intraday (Stunden bis 1 Tag),
vollautomatische Ausführung, Retail-Konto (50–250 k€), freie Daten.

- **Bericht:** [`reports/Kapitalrotation und Money Flow Trading.md`](reports/Kapitalrotation%20und%20Money%20Flow%20Trading.md)
- **Recherche-Notizen (Quellen):** [`research_notes/Kapitalrotation und Money Flow Trading/`](research_notes/Kapitalrotation%20und%20Money%20Flow%20Trading/)
- **Ergebnisse (CSV/JSON) & Grafiken:** [`results/`](results/)

## Aufbau

```
mf_trader/
  universe.py        Instrumente, Rollen (Risiko/Hafen), Kostenannahmen je Instrument
  data/
    histdata.py      1-Minuten-Daten (Indizes, FX, Gold, Öl) von histdata.com -> Stundenkerzen
    dukascopy.py     Stundenkerzen (US-T-Bond, Bund, Kupfer) aus dem Dukascopy-Datafeed
    binance.py       BTC/ETH-Stundenkerzen inkl. Taker-Buy-Volumen (Orderflow)
    yahoo.py         Yahoo-Chart-API (stündlich ~2 Jahre, täglich komplette Historie)
    fred.py          Makro-/Stressreihen (FRED)
    panel.py         Synchrones UTC-Stunden-Panel inkl. Roll-Bereinigung
  flow.py            Flow-Messung: saisonal normierte Renditen, Flow-Score, RORO-Score, Breite
  regime.py          Tagesregime-Filter (Aktien-Anleihe-Korrelation, Trend, Tages-RORO)
  strategies.py      Rotation Follower, Gegenhalten (Fader), Querschnitts-Momentum, Paar-Flows
  backtest.py        Ausführung zur nächsten Stunde, nur bei offenem Markt, Kosten inkl. Stressaufschlag
scripts/
  dl_*.py            Daten-Downloads
  run_hourly.py      Hauptexperiment (Intraday, 2019–2026)
  run_daily.py       Referenz auf Tagesbasis (Swing, 2007–2026) + Rotations-Taxonomie
  make_charts.py     Grafiken für den Bericht
```

## Reproduzieren

```bash
pip install -r requirements.txt
python scripts/dl_histdata.py      # ~20 min
python scripts/dl_dukascopy.py     # Dukascopy drosselt stark: 10–60 min
python scripts/dl_binance.py
python scripts/dl_yahoo.py
python scripts/dl_fred.py
python scripts/run_hourly.py --rebuild   # ~30–40 min
python scripts/run_daily.py
python scripts/make_charts.py
```

## Wichtige Datenfallen (gefunden und behoben)

1. **HistData-Zeitstempel**: Laut Doku „EST ohne Sommerzeit“, tatsächlich aber New Yorker Ortszeit
   *mit* Sommerzeit (verifiziert gegen Yahoo-Futures und Dukascopy für 2019, 2021, 2023–2026).
   Unkorrigiert liegen alle Reihen im Sommer 1 Stunde zu spät – das erzeugte einen
   Schein-Effekt „Bitcoin führt den Nasdaq um 1 Stunde“ (Korrelation 0,23).
2. **Roll-Sprünge** in den Anleihe-Futures-Reihen (Dukascopy = Front-Month-ZB bzw. -FGBL):
   0,7–1,8 % Kurslücke beim Kontraktwechsel. Erkannt und per Back-Adjustment entfernt
   (Bund: Abgleich mit US-Treasuries, weil echte Zinsbewegungen parallel laufen, Rolls nicht).
3. **Look-ahead** im Tages-Backtest (Position verdiente die Rendite des Signaltags) – erkannt an
   einer Trefferquote von 100 % und korrigiert.
4. **Einzel-Asset-Schocks** (z. B. US-Kupferzoll Juli 2025: +12,6 % / −18,8 % in einer Stunde)
   dürfen nicht allein eine „Rotation“ auslösen → Flow-Scores werden vor der Mittelung auf ±4 begrenzt.

## Haftungsausschluss

Reine Forschung, keine Anlageberatung. Backtests sind keine Garantie für zukünftige Ergebnisse.
