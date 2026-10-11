# Eigene Simulation: Intraday-Kapitalrotation (2019–2026) – Ergebnisse

Quelle: eigene Berechnungen im Repo `MF_Trader` (Code: `mf_trader/`, `scripts/run_hourly.py`, `scripts/run_daily.py`,
`scripts/run_extra_equity_momentum.py`; Rohergebnisse: `results/hourly/*.csv|json`, `results/daily/*.csv|json`;
Grafiken: `results/charts/*.png`). Alle Zahlen nach Kosten, sofern nicht „brutto“ angegeben.

## 1. Setup

**Daten (frei verfügbar):**
- histdata.com 1-Minuten-Daten → Stundenkerzen: S&P 500 (SPX), Nasdaq 100 (NDX), DAX (ab 06/2020–12/2023 liefert der Feed
  fälschlich Euro-Stoxx-50-Niveaus; als „Aktien Europa“ verkettet), Nikkei (NKY), Gold, Silber, Brent, USDJPY, USDCHF,
  AUDJPY, USDMXN, US-Dollar-Index.
- Dukascopy (Stundenkerzen): US-T-Bond-Future (ZB-Front-Month), Bund-Future (FGBL), Kupfer.
- Binance: BTC/USDT, ETH/USDT stündlich inkl. Taker-Buy-Volumen (echter Orderflow).
- Yahoo (Kontrolle/Tagesdaten), FRED (Makro/Stress). IBKR wurde geprüft, aber die historische API ist auf
  ~60 Abfragen/10 min limitiert und damit für mehrjährige Stundenhistorien ungeeignet → IBKR ist die
  natürliche Live-Daten-/Ausführungsquelle, nicht die Backtest-Quelle.
- Universum: 17 Instrumente. Rollen: Risiko = SPX, NDX, DAX, NKY, BTC, ETH, AUDJPY, MXN, Kupfer;
  Häfen = US-T-Bond, Bund, Gold, JPY, CHF; ohne feste Rolle = USD, Öl, Silber.
- Zeitraum: 2019-07-01 bis 2026-09-30 (Stunden). In-Sample (IS) 2019-07 bis 2022-12, Out-of-Sample (OOS) 2023-01 bis 2026-09.

**Gefundene und behobene Datenfehler (wichtig für jeden, der so etwas selbst baut):**
1. HistData-Zeitstempel sind entgegen der Doku New Yorker Ortszeit *mit* Sommerzeit (verifiziert gegen Yahoo-Futures und
   Dukascopy für 2019, 2021, 2023–2026). Unkorrigiert entstand ein Schein-Effekt „BTC führt Nasdaq um 1 h“
   (Korrelation 0,23); korrigiert: 0,02.
2. Roll-Sprünge der Anleihe-Futures (0,7–1,8 % Kurslücke beim Kontraktwechsel; 10 beim T-Bond, 22 beim Bund) per
   Back-Adjustment entfernt.
3. Look-ahead im ersten Tages-Backtest (100 % Trefferquote) entdeckt und korrigiert.
4. Fehlerhafte Niveaubrüche (DAX-Feed ±136 %) und Einzel-Asset-News (Kupferzoll Juli 2025: +12,6 % / −18,8 % in einer
   Stunde) dürfen keine „Rotation“ auslösen → Flow-Scores werden vor der Mittelung auf ±4 begrenzt.

**Flow-Messung:**
- Saisonal normierte Rendite: Stundenrendite / erwartete Volatilität derselben Tagesstunde (letzte 60 Tage) –
  berücksichtigt, dass z. B. die US-Eröffnung volatiler ist als die Asien-Nacht und geschlossene Märkte.
- Flow-Score F(L) je Asset: kumulierte L-Stunden-Rendite / erwartete L-Stunden-Volatilität.
- RORO-Score: (Mittel F der Risikoassets − Mittel F der Häfen)/√2, rollierend standardisiert (z-Wert, 1 Jahr).
  z ≤ −2,5 = Risk-off-Rotation, z ≥ +2,5 = Risk-on-Rotation (bei L = 4 h).
- Häufigkeit (L=4h, |z|≥2,5, erstes Überschreiten): ~55–85 Risk-off- und ~33–75 Risk-on-Signale pro Jahr
  (2026 bis Sept.: 44 / 19).

**Ausführung & Kosten:**
- Signal am Schluss der Stunde t, Ausführung zu Beginn von t+1 (vollautomatischer Bot), nur wenn der jeweilige Markt
  offen ist; über Wochenenden/Sitzungspausen wird die Lücke mitgetragen.
- Kosten je Seite (Spread/2 + Kommission + Slippage, IBKR-Futures bzw. Krypto-Perps): Aktienindex-Futures 1,0–2,0 bps,
  Gold 1,0, T-Bond 1,5, Bund 1,0, JPY/CHF 0,7, Öl 1,5, Kupfer/Silber 2,0, BTC 5,0, ETH 6,0 bps.
  Stressaufschlag: × √(aktuelle/normale Volatilität), max. × 3.
- Positionsgröße: inverse Volatilität, 5 % annualisiertes Risikobudget je Bein (Sharpe ist skalierungsunabhängig).

## 2. Ereignisstudie: Wie viel der Bewegung ist nach der Erkennung noch übrig?

(L=4h, z=2,5; 528 Risk-off- / 382 Risk-on-Ereignisse 2019-07–2026-09; Überrenditen ggü. normaler Drift)

**Vor dem Risk-off-Signal (letzte 4 h) – die Rotation ist bereits gelaufen:**
Nasdaq −89 bps, S&P −73, Nikkei −92, BTC −104, ETH −149, AUDJPY −50, Kupfer −48, Öl −54;
T-Bond +37, Bund +17, Gold +26, JPY +35, CHF +18 bps.

**Nach dem Risk-off-Signal (Überrendite, bps; 1 h / 4 h / 8 h / 24 h):**
- Nasdaq: −1,0 / +0,6 / −0,1 / +3,5; S&P: −0,5 / −1,4 / −1,7 / +0,4; BTC: −8,1 / −3,3 / +2,0 / +9,2
- T-Bond: +1,4 / 0,0 / −1,6 / −4,9; Gold: −0,3 / +0,7 / +1,5 / −4,1; JPY: +0,7 / −1,5 / −1,1 / −1,9; CHF: +1,1 / +0,8 / +2,9 / +4,6
- → Nach der Erkennung bleiben typischerweise 0–3 bps Fortsetzung, also weniger als die Kosten eines Round-Trips
  (2–3 bps je Bein). Über 24 h kehren Häfen eher um (T-Bond −4,9, Gold −4,1), Risikoassets erholen sich.
- Starke Signale (z≥3, n=239): Gold +6,0 bps in 4 h (t=2,0), Bund +4,0 (t=2,1), Aktien kaum Fortsetzung;
  z≥4 (n=110): Bund +6,3 (t=2,3), Öl −60 bps (Ölschocks), Gold 0.
- Nach Sitzung: In Asien-Stunden ausgelöste Risk-off-Signale zeigen anschließend eher Erholung; in US-Stunden leicht
  weiter fallende Kurse (S&P −3 bps in 4 h, t=−0,7) – statistisch nicht belastbar.
- Nach Regime: Wenn die 60-Tage-Korrelation Aktien/Anleihen ≥ 0 ist (Inflationsregime wie 2022–2026), funktionieren
  Anleihen als Ziel nicht; Gold und CHF etwas besser.

**Nach dem Risk-on-Signal (z≥3, n=165) – hier gibt es Fortsetzung:**
S&P +5,0 / +12,5 / +5,9 / +15,1 bps (1/4/8/24 h), Nasdaq +5,9 / +17,0 (t=3,1 bei 4 h) / +9,3 / +18,1, DAX +13,0 (4 h),
BTC +24,4 (4 h); Anleihen fallen weiter (Bund −3,6, t=−2,5).
→ Asymmetrie: Panik-Rotationen (Risk-off) sind bei Erkennung „verbraucht“ und kehren eher um; Erleichterungs-
Rotationen (Risk-on) laufen bei Aktienindizes noch Stunden weiter.

## 3. Handelsstrategien (Intraday)

| Strategie | Sharpe IS | Sharpe OOS | Sharpe gesamt | Trades/Jahr | Ø Trade (bps netto) | Trefferquote |
|---|---|---|---|---|---|---|
| Rotation Follower Basis (long Ziel-Assets mit Zufluss, 4h-Flow, z≥2,5, max 8h, Ausstieg bei nachlassendem Momentum/US-Schluss) | −1,18 | −0,28 | −0,71 | 104 | −0,6 | 43 % |
| … + Short der Quell-Assets | −1,43 | −0,45 | −0,96 | 104 | −2,1 | 38 % |
| … nur Risk-off | −0,99 | −0,25 | −0,61 | 59 | −0,8 | 40 % |
| … nur Risk-on | −0,62 | −0,25 | −0,42 | 46 | −0,4 | 48 % |
| **Nutzer-Idee: bei Risk-off Gold + T-Bonds long, BTC + Nasdaq short** | −0,58 | −0,45 | −0,51 | 60 | −0,3 | 40 % |
| … + Tages-RORO-Trend-Filter | −1,08 | −0,08 | −0,57 | 51 | −0,9 | 43 % |
| … + Hafen-Trendfilter | −1,42 | −0,37 | −0,88 | 90 | −1,3 | 43 % |
| … + Aktien-Anleihe-Korrelationsfilter | −0,84 | −0,26 | −0,56 | 103 | −0,2 | 43 % |
| … nur US-Sitzung (Risk-off) | −1,45 | −1,50 | −1,47 | 23 | −6,1 | 37 % |
| Bestes von 900 Gitter-Setups (IS-Optimum) | −0,29 | −0,40 | −0,34 | 55 | +1,0 | 46 % |
| **Gegenhalten** (z≥3: 2 h warten, stärkste Verlierer der Quellseite kaufen, 24 h halten) | +0,86 | +0,36 | +0,63 | 28 | +11,5 | 59 % |
| **Risk-on-Momentum Aktienindex** (z≥3: S&P+Nasdaq-Futures 4 h long) | +0,36 | +1,62 | +1,02 | 25 | +9,0 | – |

- Parametergitter Rotation Follower: 900 Kombinationen (Fenster 2/4/8 h, Schwelle z 2/2,5/3, Haltedauer 4/8/24 h,
  Ausstiegsfenster, mit/ohne Short-Bein, mit/ohne Glattstellung vor US-Schluss, 5 Filter). **Alle 900 haben im
  In-Sample eine negative Sharpe** (Mittel −1,72; bestes −0,29); OOS-Mittel −0,46. Die Kosten betragen im Mittel ein
  Vielfaches des Bruttogewinns.
- Brutto (ohne Kosten) hat der Basis-Follower Sharpe +0,39 (Ø +1,2 bps/Trade) → Signal ist real, aber kleiner als die
  Transaktionskosten.
- Reaktionszeit: 1–2 h Verzögerung verschlechtern brutto auf ~0,05–0,08; netto −1,1.
  Doppelte Kosten: −1,8 (ohne Verzögerung).
- Placebo-Test (200 zufällige Einstiegszeitpunkte, gleiche Logik): Folger Risk-off US-Sitzung −1,47 vs. Placebo-Mittel
  −0,64 (schlechter als 99 % der Zufallsvarianten) → das Signal schadet sogar, weil es nach Überreaktionen einsteigt.
- Gegenhalten: Placebo-Mittel −0,02, echte Sharpe 0,63 → besser als 94,5 % der Zufallsvarianten (p≈0,055).
  Aber: über das 144er-Gitter gemittelt nur −0,29 IS / −0,09 OOS; robust nur die Familie „24 h halten, ohne Hedge“
  (IS +0,33, OOS +0,31 im Mittel). Jahres-P&L (5 % Risikobudget je Bein): 2019 +2,9 %, 2020 −4,1 %, 2021 +13,2 %,
  2022 +4,0 %, 2023 +0,1 %, 2024 +0,8 %, 2025 +1,6 %, 2026 +2,8 %; Top-5-Trades = 46 % des Gewinns → konzentriert,
  vorsichtig interpretieren. Gekauft werden v. a. AUDJPY, S&P, Nikkei, DAX, Nasdaq.
- Risk-on-Momentum Aktienindex (nach Ereignisstudie formuliert → Out-of-Sample nicht „blind“): alle 9 Varianten
  mit z≥3 positiv in IS und OOS (Haltedauer 2/4/8 h; z 3,0/3,5); z≥3,5/4h: IS 0,88, OOS 1,50. Placebo (300 zufällige
  Einstiege long S&P+Nasdaq, gleiche Anzahl/Haltedauer): Mittel −0,16, 95-%-Quantil 0,47; echte Sharpe 1,02 →
  besser als 100 % der Zufallsvarianten. Jahres-P&L: 2019 −0,2 %, 2020 +0,3 %, 2021 +1,9 %, 2022 +0,4 %, 2023 +3,5 %,
  2024 +5,7 %, 2025 +0,4 %, 2026 +2,9 % (bei 5 % Risikobudget je Bein; nur ~100 Stunden/Jahr investiert).
  Auf 10 % Jahresvolatilität skaliert (≈ 5-facher Hebel ggü. Basis): CAGR ~10 %, MaxDD −14 %.
  Gegenhalten auf 10 % Vol: CAGR ~6 %, MaxDD −21 %. Nutzer-Idee auf 10 % Vol: CAGR −5,5 %, MaxDD −36 %.
  Rotation Follower Basis auf 10 % Vol: CAGR −7,3 %, MaxDD −49 %.

## 4. Weitere Intraday-Tests

- **Querschnitts-Flow-Momentum** (stündlich die Assets mit stärkstem Zufluss long, stärkstem Abfluss short):
  1-Stunden-Fenster brutto Sharpe ≈ −2 (starke kurzfristige Umkehr), 24-h-Fenster brutto bis +0,69, netto aber
  durchweg negativ (IS −1,7 bis −5).
- **Paar-Matrix** (136 Paare, „folge dem Flow von B nach A“, 4 h bzw. 8 h): netto nur 1 % (4 h) bzw. 10 % (8 h) der
  Paare positiv; kein Paar ist bei 4 h in IS und OOS positiv, bei 8 h nur 5 von 136. Beste: Gold vs. JPY (8 h,
  netto 0,41; OOS 0,73), JPY vs. Silber, AUDJPY vs. JPY. Schlechteste: Bund vs. T-Bond (−2,5), MXN-Paare.
  Die Rangfolge ist stabil (IS/OOS-Korrelation 0,48–0,66): Paare mit Yen/Franken als Hafen funktionieren relativ am
  besten, Anleihe-gegen-Anleihe und EM-FX am schlechtesten.
- **Intraday-Momentum letzte Stunde** (Gao et al. / Baltussen et al.: Rendite Vortagsschluss→15:00 NY sagt
  15–16 Uhr voraus): 2019–2026 brutto nur schwach (Nasdaq 0,43, Gold 0,79, S&P 0,13), netto überall negativ; OOS negativ.
- **Krypto als Frühindikator:** BTC-Wochenendrendite korreliert 0,20 mit der Nasdaq-Eröffnungslücke am Sonntagabend
  (nicht handelbar, da Futures erst dann öffnen) und −0,13 mit dem Rest des Montags (leichte Umkehr). BTC→Nasdaq
  nächste Stunde: 0,02 (nach DST-Korrektur; vorher scheinbar 0,23). Binance-Taker-Imbalance erklärt die gleiche Stunde
  (Korrelation 0,44), sagt aber die nächste Stunde nicht voraus (−0,005).

## 5. Tagesdaten-Referenz (Swing, ETF-Daten 2007–2026)

**Rotations-Taxonomie (Tage pro Jahr, Klassifikation nach z-Renditen SPY/TLT/GLD/UUP/FXY):**
- „Klassisches Risk-off“ (Aktien ↓, Anleihen ↑, Gold/Yen ↑): 2008: 35, 2011: 20, 2014: 23 … seit 2021 nur 3–11/Jahr
  (2024: 6, 2025: 11, 2026 bis Okt.: 3) → seltener geworden.
- „Zins-/Inflationsschock“ (Aktien ↓, Anleihen ↓): früher 0–3/Jahr, 2021: 6, 2022: 10, 2023: 9, 2025: 7.
- „Liquidation / Dash for Cash“ (alles ↓, USD ↑): 2021: 7, 2022: 5, 2024: 8, 2026: 7.
- „Sell America“ (Aktien ↓, Anleihen ↓, USD ↓): selten (25 Tage seit 2007; 2017: 5, 2025: 5).
- „Liquiditätsrally“ (Aktien ↑, Anleihen ↑, USD ↓): von 1–10/Jahr (2007–2016) auf 11–25/Jahr (2021–2026) gestiegen.
- „Reflations-Risk-on“ (Aktien ↑, Anleihen ↓): 2011: 29 … 2025: 8, 2026: 1.
→ Die Rollen der Anlageklassen haben sich seit 2021 verschoben: Aktien und Anleihen bewegen sich häufiger gemeinsam.

**Was passiert am Folgetag (Mittel, t-Wert)?**
- Nach klassischem Risk-off (n=282): S&P +0,19 % (t=1,9), T-Bonds −0,15 % (t=−2,2), Yen −0,10 % (t=−2,2) → Umkehr.
- Nach Zins-/Inflationsschock (n=57): USD +0,14 % (t=2,7; 5 Tage t=2,3), BTC −0,98 % (5 Tage −2,5 %), Aktien weiter
  schwach (t≈−1) → Fortsetzung.
- Nach Liquidation (n=44): USD +0,16 % (t=1,9), Gold −0,38 % (t=−1,7).
- Nach Liquiditätsrally (n=187): Gold +0,20 % (t=2,8).
- Nach „Sell America“ (n=25): Aktien +0,9–1,2 % (t≈2) → starke Erholung (z. B. 9. April 2025).

**Swing-Strategien:**
- Rotation Follower auf Tagesbasis (480 Varianten, 1–20 Tage Haltedauer): Mittel Sharpe IS −0,29, OOS −0,03; Einstieg
  einen Tag später besser als am Signaltag (Umkehr am ersten Tag). Kein robustes Setup.
- Klassisches Cross-Asset-Momentum (Rangfolge nach 60–250-Tage-Rendite, Top-3/5 long, wöchentlich/monatlich):
  Sharpe IS 0,63–0,72, OOS 0,70–0,78, CAGR 10–12 %, MaxDD −32 bis −35 % (long-only); Long/Short 0,3–0,4.
  Zum Vergleich Buy & Hold 2007–2026: SPY Sharpe 0,62 (CAGR 10,8 %, MaxDD −55 %), QQQ 0,79, GLD 0,59, TLT 0,25.
- Paar-Flows Swing (20–60 Tage): robusteste Paare = BTC gegen sichere Häfen (BTC vs. IEF/TLT/GLD/JPY/USD: netto
  Sharpe 0,6–0,8, IS und OOS positiv) und Anleihen gegen Rohstoffe (IEF vs. Öl/DBC: ~0,5–0,6) – also langsame Trends,
  keine schnellen Rotationen. 5-Tage-Paare: nur 26 % positiv.

## 6. Interpretation (eigene Schlussfolgerungen)

1. Die Rotation ist messbar und in Echtzeit erkennbar – aber zum Zeitpunkt der Erkennung (2,5 σ) sind ~90–100 % der
   Bewegung bereits gelaufen. Bei Risk-off folgt im Mittel keine verwertbare Fortsetzung, eher Umkehr.
2. „Aufspringen“ (Folgen) ist nach Kosten in allen 900 getesteten Varianten unprofitabel; Reaktionsverzögerung und
   Stresskosten verschärfen das.
3. Die profitableren Richtungen sind (a) Gegenhalten nach Panik (Verlierer kaufen, 24 h) und (b) Mitlaufen bei
   Erleichterungsrallys in liquiden Aktienindex-Futures (4–8 h). Beide sind statistisch nur moderat abgesichert
   (Data-Snooping-Risiko, wenige große Ereignisse), (b) besteht den Placebo-Test deutlich.
4. Die Wahl des „sicheren Hafens“ ist regimeabhängig; seit 2022 und erneut 2026 versagen lange Anleihen häufig.
5. Auf Tages-/Wochenbasis funktioniert langsames Cross-Asset-Momentum (Trendfolge) robust – das ist die
   „professionelle“ Form des Money-Flow-Tradings.
