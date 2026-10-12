# Eigene Simulation: Überhitzung, relative Mean Reversion (Haltedauer ≤ 2 Tage) – Ergebnisse

Quelle: eigene Berechnungen im Repo `MF_Trader` (Code: `mf_trader/overheat.py`, `mf_trader/meanrev.py`,
`mf_trader/stats.py`, `scripts/run_meanrev_daily.py`, `scripts/run_meanrev_hourly.py`, `scripts/run_user_rsi_example.py`,
`scripts/run_dip_buying.py`, `scripts/run_ibs_futures_hourly.py`, `scripts/run_ibs_placebo.py`,
`scripts/run_pair_rsi_deepdive.py`, `scripts/run_pair_rsi_robustness.py`, `scripts/run_pair_rsi_daily_check.py`,
`scripts/run_pair_rsi_final.py`; Ergebnisse unter `results/meanrev_daily/`, `results/meanrev_hourly/`,
`results/user_rsi_example/`, `results/dip_buying/`, `results/ibs_futures_hourly/`, `results/pair_rsi_deepdive/`;
Grafiken `results/charts_meanrev/m01…m06*.png`). Alle Zahlen nach Kosten, sofern nicht „brutto“.

## 1. Setup

- **Stundendaten 07/2019–09/2026, 42 Märkte in 11 Körben:** Aktienindizes (S&P 500, Nasdaq 100, Russell 2000, DAX, CAC 40,
  FTSE 100, Nikkei, Hang Seng, China A50, ASX 200), Staatsanleihen (US-T-Bond, Bund, Gilt), Edelmetalle (Gold, Silber),
  Kupfer, Energie (Brent, Erdgas), Agrar (Soja, Zucker, Kaffee, Kakao), Währungen gegen USD (EUR, GBP, JPY, CHF, AUD,
  NZD, CAD, NOK, MXN, ZAR) und Krypto (BTC, ETH + 8 Altcoins: SOL, BNB, XRP, ADA, DOGE, AVAX, LINK, LTC).
  Körbe: Aktien, Anleihen, Edelmetalle, Industriemetalle, Energie, Agrar, Hafen-FX (JPY, CHF), Risiko-FX
  (AUD, NZD, CAD, NOK, MXN, ZAR), Euro/Pfund, Krypto-Majors, Altcoins.
- **Tagesdaten 2007–2026, 63 Märkte:** ETFs (US/Intl.-Aktien, 14 Sektoren/Themen, Anleihen inkl. Kredit/EM, Edelmetalle,
  Rohstoffe inkl. Agrar, Währungen, REITs) + Krypto (Binance, Tagesschluss 16:00 New York, ab 2018).
- **Signale:** RSI (Stunden: 6/14/48/96/120/168 h; Tage: 2/5/14), z-Score der Rendite (4–48 h bzw. 1–5 Tage),
  Bollinger-z, IBS (Lage des Schlusskurses in der Tagesspanne), Faktor-Residuen (PCA, Avellaneda/Lee-Stil),
  Krypto-Funding-Raten (Binance, ab 2020).
- **Regeln:** überhitzt → short, unterkühlt → long; Ausstieg, sobald sich die Einschätzung auflöst (Signal kreuzt die
  Mitte) oder nach max. 12/24/48 h bzw. 1/2 Tagen. Paare: alle Kombinationen gleichzeitig, überlappend, je Asset
  netto verrechnet; Körbe: risikogleich gewichtete Klassenkörbe gegeneinander.
- **Ausführung:** Stunden: nächste Stunde, nur bei offenem Markt, Futures-/Perp-Kosten 0,5–8 bps je Seite plus
  Stressaufschlag; Tage: Schlusskurs (MOC/Futures direkt nach Kassaschluss) und konservativ nächste Eröffnung.
- **Validierung:** Optimierung (IS) 2019–2022 bzw. 2007–2016, Test (OOS) 2023–2026 bzw. 2017–2026, Placebo-Tests
  (zufällige bzw. zeitlich verschobene Einstiege), Deflated Sharpe Ratio, Ausschlusstests, Verzögerung, doppelte Kosten.
- **Neue Datenbereinigung:** Rohstoff-CFDs von Dukascopy rollen monatlich mit großen Kurslücken (Erdgas bis ±34 %,
  z. B. 22.09.2020): entfernt wurden 35 (Erdgas), 21 (Soja), 13 (Zucker, rollt um den 7.–9.), 9 (Kakao, 10.–12.), 4 (Kaffee).
  Ohne diese Bereinigung erzeugt jeder Roll ein falsches „Überhitzt“-Signal.

## 2. Die wörtliche Idee: Tages-RSI(14) – A ≥ 70 und B ≤ 30 → A short / B long, bis ein RSI 50 kreuzt, max. 2 Tage

- Tagesdaten 2007–2026, alle 1.953 Paare: 13.449 Paar-Trades (~700/Jahr), Ø +0,17 % brutto je Paar-Trade (gleichgewichtet),
  Trefferquote 53 %, Ø Haltedauer 2,0 Tage (meist Zeitstopp).
- Portfolio (überlappend, netto verrechnet): Sharpe brutto 0,12, netto −0,05 (Schlusskurs) bzw. −0,09 (Eröffnung);
  2007–2016 +0,18, 2017–2026 −0,23.
- Strenger (80/20): ~13 Trades/Jahr, Sharpe 0,23 (Schlusskurs) / 0,09 (Eröffnung). 90/10: keine Signale.
  RSI(2) 90/10 bzw. 95/5: −0,46 bzw. −0,17.
- Stundendaten (Tages-RSI, Ausführung in der nächsten Stunde): RSI(14) 70/30 −0,14 (IS −0,41, OOS +0,40);
  80/20 −0,11; RSI(2) 90/10 −0,64.

## 3. Überblick über alle Familien

**Stunden (1.243 Varianten):** 15 % im IS positiv, 16 % im OOS, 7 % in beiden; mittlere Brutto-Sharpe −0,15.
Mittlere Netto-Sharpe IS / OOS je Familie:
- Einzelasset beide Seiten (72): −1,47 / −1,42; nur long: −0,48 / −0,19; nur short: −1,78 / −1,79
- Paare mit schnellen Signalen (RSI 14 h, z 12–48 h, Residuen; 60): −1,29 / −1,26
- Paare mit langsamem RSI (48–96 h; 24): +0,19 / +0,37
- Korb gegen Korb (63): −1,54 / −2,00 (bestes IS-Setup +0,33 → OOS −0,73)
- Querschnitt (64): −2,65 / −2,57
- Krypto-Funding-Extreme (27): −0,77 / −0,53
Je Klasse und Richtung (2019–2026): „Überverkauft kaufen“ leicht positiv nur bei Altcoins (+0,42) und Aktien (+0,19);
„Überkauft shorten“ negativ fast überall (Krypto-Majors −1,35, Altcoins −1,49, Hafen-FX −1,02); einzige Ausnahme
Anleihen (+0,13). In Stressphasen (hohe Aktienvolatilität) ist „Aktien überverkauft kaufen“ im OOS +0,98.

**Tage 2007–2026:** Einzelasset (160): 7,5 % IS > 0, 0 % OOS > 0, Mittel −0,60 / −1,18 (brutto +0,03);
nur bei US-Aktien leicht positiv (IS 0,34 / OOS 0,04; IBS IS 0,71 / OOS 0,25). Paare (88): 14 % IS > 0, 1 % OOS > 0;
Einzelpaare: IS-/OOS-Korrelation 0,09 (gute Paare der Vergangenheit sagen nichts über die Zukunft).
Korb gegen Korb: brutto +0,20, netto IS −0,46 / OOS −0,69. Querschnitt −1,3 / −1,7, klassenneutral −2,0 / −2,4.
Konditionierung: nur long + Trend- oder VIX-Filter besser (z. B. IBS nur long 0,18 → mit hohem VIX 0,44);
nur short durchweg negativ.

## 4. Kandidat A: Dip-Kauf in Aktienindizes (IBS < 0,2, nur long, ≤ 2 Tage)

- Tagesdaten 2007–2026, 15 Aktienindex-ETFs, Ausführung zum Schlusskurs: Sharpe netto 0,75 (2007–2016 0,80,
  2017–2026 0,69), brutto 1,02; Buy & Hold desselben Korbs 0,37. Auf 10 % Vol: CAGR 7,2 %, MaxDD −16 %,
  16 von 20 Jahren positiv, 2008 +0,9 %. Mit VIX-Filter 0,78. Ausführung zur nächsten Eröffnung nur 0,22 →
  ein großer Teil des Effekts ist die Erholung über Nacht; Einstieg muss zum/direkt nach dem Kassaschluss erfolgen.
- Placebo (300 zufällige Einstiege, gleiche Anzahl/Haltedauer): US-Korb (SPY/QQQ/IWM) 0,98 vs. Placebo 0,38
  (95-%-Quantil 0,64) → besser als 100 %; 15 Indizes 0,75 vs. 0,06.
- Umsetzung mit Index-Futures (Stundendaten 2019–2026, Kassasitzung je Index, Einstieg in der Stunde nach
  Kassaschluss, Futures-Kosten; IBS aus stündlichen Schlusskursen angenähert): S&P 500 0,91, Nasdaq 100 1,64,
  Russell 2000 0,56 (jeweils beide Teilperioden positiv); DAX −0,37, CAC −0,82, FTSE −0,40, Nikkei 0,12,
  ASX 0,24, Hang Seng −0,23. US-Korb: 1,21 (2019–2022 1,31; 2023–2026 1,12) vs. Buy & Hold US 0,67;
  auf 10 % Vol: CAGR 12,3 %, MaxDD −9,6 %; Jahre 2020 +27,2, 2021 +17,8, 2022 +4,1, 2023 +11,5, 2024 +5,4,
  2025 +14,5, 2026 +10,7 (2019, Halbjahr: −0,2); Trefferquote 65 %; Top-10-Tage = 32 % des Gewinns;
  1.341 aktive Tage. Korrelation zu Buy & Hold US 0,64 (trägt Aktienrisiko, nur long).
- Fazit: ein US-spezifischer Effekt (Europa negativ, Asien neutral) – passt zur Literatur (Absicherungsströme
  von Optionshändlern/gehebelten ETFs in den USA, Baltussen et al.).

## 5. Kandidat B: Relative Überhitzung zwischen Paaren (langsamer RSI, klassenübergreifend)

- Paargitter Stunden: Nur Paare auf langsamen RSI-Fenstern (48–168 h) mit hoher Mindestdifferenz sind positiv.
  Umgebungsgitter klassenübergreifend (75 Varianten): 95 % IS > 0, 69 % OOS > 0, 68 % beide.
  Positive Zone: RSI 96–168 h mit 25–35 Punkten Abstand bzw. RSI 48 h mit ≥ 40 Punkten.
- Achtung Konzentration: Das IS-beste schmale Setup (RSI 96 h, 40 Punkte, 12 h) hing an AVAX (41 % der Signale)
  und 2020 → verworfen.
- Ausschlusstests (RSI 96 h, 30 Punkte, 24 h): alle Märkte IS 0,58 / OOS 0,90; ohne AVAX+Soja 0,40 / 0,90;
  ohne Altcoins+Soja 0,67 / 1,01 (8/8 Jahre positiv); ohne Krypto 0,71 / 0,94. RSI 120 h / 30 Punkte:
  0,71 / 1,12 (alle), 0,46 / 1,18 (ohne Altcoins+Soja). RSI 168 h / 25 Punkte: 0,42 / 1,06.
- Bereinigter Kandidat (RSI 96 h, 30 Punkte, ≤ 24 h, 429 klassenübergreifende Paare, ohne Altcoins und Soja):
  ~81 Paar-Trades/Jahr; Sharpe 0,79 (IS 0,67, OOS 1,01), brutto 0,84; 1 h Verzögerung 0,78, 2 h 0,75, 4 h 0,70;
  doppelte Kosten 0,74; Placebo (60 zeitlich verschobene Varianten) Mittel −0,42, 95-%-Quantil 0,14 → besser als 100 %;
  auf 10 % Vol: CAGR 7,7 %, MaxDD −6,8 %, alle 8 Jahre positiv (2019 +8,1, 2020 +11,0, 2021 +2,9, 2022 +1,5,
  2023 +1,0, 2024 +13,9, 2025 +8,8, 2026 +12,2).
- Was gehandelt wird: am häufigsten „überhitzt“ Bund (77), Yen (56), Franken (47), BTC (47), T-Bond (43),
  Russell (43); „unterkühlt“ DAX (74), FTSE (51), CAC (49), Nikkei (49), S&P (36) → im Kern: überkaufte sichere
  Häfen short gegen überverkaufte Aktienindizes long = systematisches Gegenhalten nach mehrtägigen Fluchtbewegungen.
- Konzentration: Nur an 104 von 1.894 Tagen investiert; die 5 besten Tage liefern 94 % des Gesamtgewinns, die 10
  besten 111 % (Rest leicht negativ). Top-Tage: 09.03.2026, 06.08.2019, 10.03.2020, 07.04.2025, 05./06.08.2024,
  29.04.2024, 28.07.2021, 24.02.2020, 02.03.2020 → ein Krisen-Rebound-Trade mit rund 8 Episoden in 7 Jahren.
- Deflated Sharpe: gegen alle 218 Paar-Varianten als Versuchsmenge (inkl. sehr schlechter) nicht signifikant
  (DSR ≈ 0, weil die Streuung der Versuche groß ist); einzeln getestet PSR > 0,999.
- Unabhängiger Langzeitcheck auf Tagesdaten 2007–2026 (Tages-RSI 3–10 Tage, Schwellen auf gleiche Seltenheit
  kalibriert): brutto 0,2–0,3, netto 0,0–0,2 (Schlusskurs), ≈ 0 (Eröffnung) → der Effekt ist auf Tagesbasis schwach;
  er zeigt sich vor allem, wenn man untertägig direkt auf das Extrem reagiert.

## 6. Kombination (2019–2026, je Baustein auf 10 % Vol skaliert, gleichgewichtet)

Korrelationen der Tagesrenditen: IBS US vs. Paare 0,04; IBS US vs. Risk-on-Momentum (Studie 1) 0,11;
IBS US vs. Buy & Hold US 0,64. Ergebnisse auf 10 % Vol: IBS US allein Sharpe 1,21 (CAGR 12,3 %, MaxDD −9,6 %);
+ Paare 1,38 (14,3 %, −6,1 %); + Risk-on-Momentum 1,67 (17,6 %, −5,0 %). Buy & Hold US 0,67 (6,4 %, −16,6 %).
Vorbehalt: Alle Bausteine wurden mit Kenntnis dieses Zeitraums ausgewählt → Rückschau, optimistisch.

## 7. Eigene Interpretation

1. Die allgemeine Form der Idee (alle Assets, RSI-Extreme, beide Richtungen, ≤ 2 Tage) ist nach Kosten nicht rentabel.
   Hauptgrund: „Überkauft shorten“ verliert fast überall (Trends laufen weiter, besonders Krypto), schnelle Signale
   kosten mehr als sie bringen, und Korb- sowie Querschnittsvarianten zeigen eher Momentum als Umkehr.
2. Zwei Nischen tragen: (A) Dip-Kauf in US-Aktienindizes zum Kassaschluss – am besten belegt (19 Jahre, Placebo,
   Futures-Test, Literatur); (B) relative Überhitzung Hafen vs. Aktien auf mehrtägigen RSI-Fenstern – plausibel und
   robust gegen Ausschlüsse, aber extrem episodisch (≈ 8 Krisen), deshalb statistisch dünn.
3. Gemeinsamer Nenner: Gewinne entstehen beim Kaufen von Panik (Liquiditätsbereitstellung), nicht beim Shorten
   von Euphorie – konsistent mit Studie 1 (Gegenhalten nach Panik, Risk-on-Momentum) und der Literatur (Nagel 2012).
