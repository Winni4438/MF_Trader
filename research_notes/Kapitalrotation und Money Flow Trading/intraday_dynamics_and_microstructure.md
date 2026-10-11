# Intraday Anatomy of Cross-Asset Rotations and Market Shocks: Dynamics, Sequencing, Microstructure and Backtesting Implications

Scope note: research conducted 2026-10-11. The web-search budget for this session ran out before 2026 episodes (especially the Iran-conflict shock that began 28 Feb 2026) could be researched in detail. Gaps are listed explicitly under each question. Where only secondary sources were available, this is flagged.

---

## 1. Sequencing and lead–lag: which markets move first in risk-off/risk-on shocks, and how long does the lead last?

### Takeaway
At the microstructure level, futures (ES, ZN and similar) are where most price discovery happens. Cross-market leads between liquid futures, cash markets and FX last seconds to a few minutes, not hours. Scheduled news is priced within about 1–2 minutes. In macro shocks, the market that moves "first" is mostly whichever venue is open and liquid when the news hits: Asian equity/FX on Monday mornings, CME Globex futures on Sunday evenings, crypto on weekends. The safe-haven responses of JPY/CHF and Treasuries are fast but regime-dependent. In "dash for cash" (March 2020) and "sell America" (April 2025) regimes, Treasuries, gold and the USD can be sold together with equities, so a fixed risk-off map is unreliable.

### Cited Findings
**Price discovery and lead–lag at high frequency**
- In US Treasuries, futures usually lead cash, but the reverse is also often true. From a price-discovery point of view the two can be treated as one market. Near-simultaneous cash/futures cross-market trading made up as much as 20% of cash-market activity on many days. — [NY Fed Liberty Street (2015)](https://libertystreeteconomics.newyorkfed.org/2015/08/high-frequency-cross-market-trading-in-us-treasury-markets)
- Dobrev & Schaumburg find that price discovery in both US Treasury and US equity markets happens mostly in futures rather than cash. Cross-market (equity–Treasury) high-frequency activity tracks volatility even after controlling for volume and trade counts. The paper contrasts the 2010 equity flash crash with the 2014 Treasury flash rally. — [Dobrev & Schaumburg, AEA 2018 paper page](https://benny.aeaweb.org/conference/2018/preliminary/paper/QdkHkBSZ)
- A tick-data study of S&P 500 index futures vs. the cash index finds a bidirectional lead–lag of up to 3–4 one-minute lags. Leadership is two-way at sub-minute to few-minute horizons. (Attribution from search summary; full text not opened.) — [Inderscience study](https://www.inderscience.com/filter.php?aid=73790)
- In crypto, prices on some exchanges trail others by up to about 15 seconds (2018 tick data). Even within one asset, lead–lag across venues is measured in seconds. — [CBS thesis, "High Frequency Lead-Lag Relationships in the Bitcoin Market"](https://research-api.cbs.dk/ws/portalfiles/portal/59795067/612646_High_Frequency_Lead_Lag_Relationships_in_The_Bitcoin_Market.pdf)

**Speed of reaction to scheduled news**
- In the Treasury market, a major macro announcement first produces a sharp, nearly instantaneous price change with lower volume and sharply wider spreads. A second stage follows in which volume surges, volatility persists and spreads stay moderately wide while investors reconcile differing views. — [Fleming & Remolona (1999, JF)](https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1901-1915.html)
- Most of the price response to scheduled macroeconomic announcements is completed within 1–2 minutes. — [Fleming & Remolona, BIS Working Paper 71](https://www.bis.org/publ/work71.pdf)
- In FX (USD vs DEM/EUR, GBP, JPY, CHF), announcement surprises cause immediate jumps in the conditional mean. The response is asymmetric: bad news moves prices more than good news. — [Andersen, Bollerslev, Diebold & Vega (2003, AER), NBER WP](https://www.nber.org/system/files/working_papers/w8959/w8959.pdf)

**Safe-haven FX sequencing**
- High-frequency data from 1993–2008 show the CHF and JPY appreciating against the USD when US stocks fall, US bond prices rise and FX volatility rises. The effect appears at horizons from a few hours to several days, is non-linear in volatility, and is stronger in crises. Safe-haven moves equal losses for carry traders. — [Ranaldo & Söderlind, SNB WP 2007/17 (Review of Finance 2010)](https://www.snb.ch/en/publications/research/working-papers/2007/working_paper_2007_17)

**Regime breaks: when "safe havens" are sold**
- March 2020: the FSB divides the turmoil into a "flight to safety" phase (about 21 Feb–11 Mar), in which risky assets were sold and safe ones bought, and a "dash for cash" phase (about 11–23 Mar). In the second phase, government bonds and gold were also sold, stocks and bonds fell together, and the USD appreciated strongly. Stress ended only with central-bank interventions, and equities bottomed between 18 Mar (Europe) and 23 Mar (US). — [FSB Holistic Review of the March Market Turmoil (Nov 2020)](https://www.fsb.org/uploads/P171120-2.pdf)
- During the dash for cash, US Treasury bid-offer spreads widened by a factor of 10 and gold fell 12%. — [Jon Cunliffe speech, Bank of England (via BIS)](https://www.bis.org/review/r220210f.htm)
- April 2025: the USD depreciated strongly while US Treasury yields rose, the reverse of the usual risk-off pattern. — [ECB Financial Stability Review special feature (Nov 2025)](https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202511_01~fdf147a04a.en.html). The dollar fell about 2.8% against the euro within two days. — [Bundesbank Monthly Report May 2025](https://publikationen.bundesbank.de/content/957530)
- On 9 Apr 2025, Deutsche Bank described US assets, including the dollar, falling together. Investors reportedly moved into gold, CHF and German Bunds. — [Wikipedia: 2025 stock market crash](https://en.wikipedia.org/wiki/2025_stock_market_crash)

**Who moves first in actual episodes (details in Q4)**
- Aug 2024: crypto weakened over the weekend (sell-off "worsened on Sunday", 4 Aug). The rout deepened early Monday during Asian trading as the yen hit seven-month highs and Japanese equities crashed, before US markets opened. — [CoinDesk, 5 Aug 2024](https://coindesk.com/markets/2024/08/05/crypto-futures-witness-840m-in-liquidations-as-bitcoin-nosedives-ether-records-biggest-fall-since-2021)
- The VIX spike on 5 Aug 2024 (to almost 66, +180%) happened before the US cash open. It was driven mainly by wider option bid-ask quotes rather than trades, with puts accounting for more than 85% of the spike. — [BIS Bulletin 95 summary via Finadium](https://finadium.com/?p=145021); [BIS Bulletin 95](https://www.bis.org/publ/bisbull95.htm)
- April 2025: after the "Liberation Day" tariffs were announced on the afternoon of 2 Apr, futures fell immediately: S&P futures −3.9%, Nasdaq-100 futures −4.7%. On Monday 7 Apr, Asian markets priced the weekend first: the Nikkei fell 7.83% with a trading curb, and the ASX 200 fell about 6% within 30 minutes. — [Wikipedia: 2025 stock market crash](https://en.wikipedia.org/wiki/2025_stock_market_crash)
- In April 2025, the dollar's largest declines occurred during Asian trading hours, which suggests an important role for Asian investors' FX hedging. — [BIS Bulletin 105 (June 2025)](https://www.bis.org/publ/bisbull105.htm)
- On 10 Oct 2025, US equities sold off during cash hours after a Trump post. The largest crypto liquidation wave came hours later (20:50–21:30 UTC, i.e. after the US cash close). Crypto lagged equities in this episode. — [bit.com timeline](https://www.bit.com/knowledge-hub/october-10-crypto-crash-binance-usde); [Barron's via Tiger](https://www.itiger.com/news/2574702483)

### Inferences
- For a retail bot reacting in minutes, true informational lead–lag between liquid futures (ES/NQ/ZN/6J/GC) cannot be exploited. It lasts seconds and is captured by HFT/cross-market arbitrage. The usable "lead" comes from session asymmetry: a venue that is open (Globex Sunday evening, Tokyo/Sydney Monday morning, crypto on weekends) prices a shock hours before a closed venue (Xetra, NYSE cash) can.
- The direction of safe-haven flows depends on the regime. JPY/CHF/Treasuries/gold as risk-off "sinks" worked in Aug 2024 (carry unwind, JPY up). They failed for the USD and Treasuries in April 2025 and for Treasuries and gold in the March 2020 dash for cash. A system should infer the regime from live co-movement (e.g. whether stocks and bonds are falling together) rather than hard-code "risk-off → long ZN".
- Rotations also run at several speeds: an immediate jump (minutes), a hedging or deleveraging flow over hours to days (e.g. FX hedging in Asian hours in April 2025, carry unwind over days in Aug 2024), and a policy-driven reversal (days).

### Gaps
- No peer-reviewed intraday lead–lag study specifically on ES vs ZN vs USDJPY vs gold vs BTC during 2020–2026 shocks was found. The Dobrev–Schaumburg full text (with millisecond-scale statistics) could not be retrieved; the Atlanta Fed PDF link returned 404.
- No source quantified how many minutes USDJPY led or lagged NQ on 5 Aug 2024 or in April 2025.
- VIX futures (VX) lead–lag vs ES was not found in any source. Note that spot VIX can be an artefact of quote widening (see Q5).

---

## 2. Trading sessions, overnight vs intraday returns, and macro news as rotation triggers

### Takeaway
Session structure matters a great deal. Historically, much of the US equity premium was earned overnight, concentrated at the European open (02:00–03:00 ET). That "overnight drift" has averaged roughly zero since 2021, so it is a decayed, regime-dependent pattern. Momentum-type returns accrue overnight and reverse intraday. Scheduled macro news is priced within 1–2 minutes, with volatility persisting afterwards. The well-documented pre-FOMC drift happens before the announcement, not after it. Asian hours have recently been the locus of key FX moves (USD in April 2025, JPY in Aug 2024).

### Cited Findings
**Overnight vs intraday decomposition**
- Boyarchenko, Larsen & Whelan: almost 100% of the US equity premium was earned in a one-hour window, 02:00–03:00 ET (the European open), the "overnight drift". They link it to dealer inventory risk from end-of-day order imbalances. — [NY Fed Staff Report 917](https://www.newyorkfed.org/research/staff_reports/sr917)
- Update (July 2026): the 02:00–03:00 ET window earned about 3.7% p.a. and over 60% of the E-mini's 5.9% annualized close-to-close return from 1998 to 2020. It has averaged close to zero since 2021, including in E-mini Nasdaq-100 and Dow.
  - Main driver: the dispersion of closing order imbalances fell from 6.5% to 2.9%. VIX was little changed (mean 20.4 → 19.4), and the overnight share of E-mini volume was little changed (15% → 16%).
  - NightShares overnight ETFs (NSPY, NIWM) closed after about 14 months.
  - The authors' charts also show an opening reversal at 08:30–10:00 ET.
  - — [Liberty Street Economics, "The Disappearing Overnight Drift" (Jul 2026)](https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/)
- Lou, Polk & Skouras (JFE 2019): momentum profits are earned almost entirely overnight, while profits of most other strategies arise intraday, often with opposite signs across the two components. Institutions prefer to trade during the day and against momentum. — [Lou, Polk & Skouras, "A Tug of War"](https://personal.lse.ac.uk/polk/research/TugOfWar.pdf)
- Cliff, Cooper & Gulen report that essentially all stock returns accrue from holding overnight risk (as summarized by Alpha Architect). — [Alpha Architect summary](https://alphaarchitect.com/2015/02/overnight-momentum-vs-intraday-momentum/)

**Asian / European / US sessions**
- April 2025: the dollar's largest declines occurred during Asian trading hours, pointing to Asian investors' hedging of USD assets. — [BIS Bulletin 105](https://www.bis.org/publ/bisbull105.htm)
- Global FX turnover averaged $9.5 trillion per day in April 2025, up 27% from April 2022, driven by volatility and a rush to hedge dollar exposures after the tariff announcements. There were no signs of dollar-funding strains. — [BIS Quarterly Review Dec 2025, "Global FX markets when hedging takes centre stage"](https://www.bis.org/publ/qtrpdf/r_qt2512b.htm)
- Eurex reports that during the early-August 2024 volatility spike (STOXX Europe 600), its Asian-hours trading session "remained robust and provided investors access to liquidity to meet hedging needs". — [Eurex Trading Hours Extension presentation](https://eurex.com/resource/blob/2845114/27b6a6c653c3d047f57d88f706be26fe/data/Trading%20Hours%20Extension%20(presentation).pdf)

**Macro news (CPI, NFP, FOMC) as triggers and post-announcement behaviour**
- Treasury prices adjust to scheduled announcements within 1–2 minutes. Spreads widen dramatically at the release, and volatility and volume stay elevated for some time afterwards. — [Fleming & Remolona, BIS WP 71](https://www.bis.org/publ/work71.pdf); [JF 1999](https://ideas.repec.org/a/bla/jfinan/v54y1999i5p1901-1915.html)
- FX conditional means jump on announcement surprises, and bad news has larger effects. — [Andersen et al. (2003)](https://www.nber.org/system/files/working_papers/w8959/w8959.pdf)
- Pre-FOMC drift: the S&P 500 rose an average of 49 bp in the 24 hours before scheduled FOMC announcements, accounting for more than 80% of the equity premium over the sample. Returns after the decision are not systematically positive or negative. There is no such effect in Treasuries. — [Lucca & Moench via VoxEU](https://voxeu.org/article/predictable-movements-asset-prices-around-fomc-meetings); [NBER conference paper](https://conference.nber.org/conf_papers/f66717.pdf)
- Market intraday momentum (first half-hour predicts last half-hour) is stronger on days with major macroeconomic news releases. — [Gao, Han, Li & Zhou, "Market Intraday Momentum" (JFE 2018), summary](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/)
- Aug 2024 trigger chain: the BoJ hike (31 Jul) and a weak US jobs report (2 Aug; +114k) preceded the 5 Aug crash. — [Substack summary (secondary)](https://moneybycj.substack.com/p/the-yen-carry-trade-that-crashed-the-markets). The BIS describes leveraged unwinds amplifying the reaction to "a negative macro release in the United States". — [BIS Bulletin 90](https://www.bis.org/publ/bisbull90.htm)
- 2026: Treasury volatility rose around the 11 Feb 2026 employment report and the 13 Feb CPI release, but not around the 20 Feb Supreme Court ruling striking down the emergency tariffs. — [Liberty Street Economics (Apr 2026)](https://libertystreeteconomics.newyorkfed.org/2026/04/treasury-market-liquidity-since-april-2025/)

### Inferences
- A rotation bot should not build in an overnight-drift or pre-FOMC long bias without out-of-sample checks after 2021. The overnight drift's disappearance shows that published intraday seasonalities can decay.
- Scheduled releases are poor entry triggers for a minutes-latency retail system: the first move is complete in 1–2 minutes, while spreads are widest. A more realistic approach is to treat the post-release state (direction plus persistent volatility) as a filter and to enter on confirmation, e.g. after 15–30 minutes, accepting that the first leg is gone.
- Monday Asian open and Sunday Globex reopen are the natural "first look" windows for weekend shocks (tariff weekends in April 2025, the weekend of 4 Aug 2024). The 02:00–03:00 ET European open is a second key liquidity transition.

### Gaps
- No source quantifying post-announcement drift length (in minutes or hours) specifically for CPI/NFP in ES/ZN/FX for 2020–2026 was retrieved.
- Ranaldo (2009) and Breedon & Ranaldo (2013) on FX time-of-day patterns (home currency depreciating in home hours) were not retrieved, so the specific numbers are missing.
- No source was found on gold's session pattern (Asia vs London fix vs NY).

---

## 3. 24/7 crypto as a leading indicator for weekend/overnight risk; BTC–Nasdaq correlation and lead–lag 2020–2026

### Takeaway
BTC is the only liquid risk asset trading on weekends, but weekend crypto liquidity has thinned markedly: about 13% of volume in early 2024, down from 24% in 2018, with spreads reported to more than double on weekends. Weekend BTC moves are therefore noisy and liquidity-driven. Daily BTC–Nasdaq correlation peaked at about 0.87 in 2024 and fell to about 0.3 by March 2026. No rigorous intraday lead–lag study of BTC vs NQ was found. The case evidence is mixed:
- Aug 2024: crypto weakened on the weekend before the Monday Asian crash, consistent with leading.
- Oct 2025: crypto crashed after the equity sell-off, and equities rebounded on Monday regardless, so crypto lagged and the weekend move was a false Monday signal.

### Cited Findings
- Kaiko data: the weekend share of BTC volume fell to 13% (early 2024 YTD, a record low) from 24% in 2018. US exchanges were at 11% and offshore venues at 15%. Kaiko says this "suggests worsening liquidity conditions during weekends" and expects the weekday/weekend gap to deepen because spot ETFs trade Monday–Friday. — [The Block, 27 Feb 2024](https://www.theblock.co/news/markets/2024-02-27-bitcoin-weekend-trading-279353); [Decrypt](https://decrypt.co/219288/bitcoin-crypto-weekend-trading-liquidity-kaiko)
- A more recent Kaiko analysis cited by CryptoSlate puts about 47% of volume in US weekday hours, with weekday volumes about double weekend levels. 1%-depth is about $30M on Binance and $16–20M on Coinbase. (Date of the underlying data not confirmed.) — [CryptoSlate](https://cryptoslate.com/how-institutions-made-bitcoin-a-weekday-market-so-retail-takes-on-all-the-weekend-risk/)
- Commentary citing Kaiko: weekend BTC bid-ask spreads more than double. Weekend BTC moves should be treated as a possible, not confirmed, signal for the Monday equity/FX open, because much of the swing reflects thin liquidity. — [investingLive](https://investinglive.com/cryptocurrency/bitcoin-isn-t-a-weekend-hedge-it-s-just-the-only-market-still-open/)
- Rolling daily correlation between BTC and the Nasdaq-100 (2018–2025) rose after institutional milestones such as ETF approvals, peaking at 0.87 in 2024, and varies by regime. — [Wu (2025), arXiv 2501.09911](https://arxiv.org/abs/2501.09911v1)
- S&P Global (as cited) put BTC–Nasdaq correlation near 0.3 by March 2026, well below the 2024 peak. (Secondary.) — [eco3min](https://eco3min.fr/en/bitcoin-vs-nasdaq/)
- An informal test found no significant correlation when lagging Nasdaq by one day to predict BTC. (Blog, not peer-reviewed.) — [Ecoinometrics](https://ecoinometrics.substack.com/p/ecoinometrics-bitcoin-and-tech-stocks?s=r)
- Aug 2024 case: the crypto sell-off worsened on Sunday 4 Aug and again early Monday as the yen hit seven-month highs on carry-unwind expectations.
  - BTC fell more than 11% in 24h; ETH fell as much as 25% intraday, its worst day since May 2021.
  - More than $1bn of crypto futures were liquidated in 24h, about 87% of them longs.
  - Rumours of Jump Trading liquidating crypto holdings added to the Sunday pressure.
  - — [CoinDesk](https://coindesk.com/markets/2024/08/05/crypto-futures-witness-840m-in-liquidations-as-bitcoin-nosedives-ether-records-biggest-fall-since-2021); [CoinDesk headline "Bitcoin Tumbles to $53K"](https://coindesk.com/markets/2024/08/05/bitcoin-tumbles-to-53k-ether-turns-negative-for-2024-as-panic-grips-markets)
- Oct 2025 case: the US stock sell-off on Fri 10 Oct (Nasdaq Composite −3.6%, S&P 500 −2.7%) preceded the crypto liquidation cascade, which peaked about 20:50–21:30 UTC. Crypto then traded through the weekend at depressed levels. On Monday 13 Oct, US stocks closed higher on easing trade tensions after Trump's softer weekend comments. — [Barron's via Tiger](https://www.itiger.com/news/2574702483); [bit.com](https://www.bit.com/knowledge-hub/october-10-crypto-crash-binance-usde); [Anadolu Agency](https://www.aa.com.tr/en/economy/us-stocks-close-with-gains-on-possible-easing-trade-tensions/3716362)

### Inferences
- Weekend BTC can serve as a sentiment proxy only when the move is clearly news-driven and confirmed by other weekend-open venues (Sunday 17:00 CT Globex reopen, Monday Wellington/Sydney/Tokyo FX/equities). A weekend BTC drop driven by crypto-specific leverage (Oct 2025) or by ETH/staking/fund-specific selling (Aug 2024 Jump rumours) can mislead.
- Because ETF flows now concentrate BTC liquidity in US weekday hours, weekend BTC moves are more likely to overshoot and partly revert when US liquidity returns. This is an inference from the Kaiko volume/spread data, not a tested result.
- Correlation regimes shift: 0.87 in 2024 versus about 0.3 in early 2026. Any BTC→NQ signal must be conditioned on a rolling correlation estimate.

### Gaps
- No academic, high-frequency (minute-level) lead–lag study of BTC vs NQ/ES futures for 2020–2026 was found.
- No systematic study of "weekend BTC return → Monday ES/NQ gap" predictive power was found. This is a clear candidate for the user's own backtest, which requires careful time alignment (Globex reopens Sunday 17:00 CT).
- CME Bitcoin futures "weekend gap" behaviour was not researched.

---

## 4. Intraday timelines of specific episodes

### Takeaway
Episodes differ in sequencing:
- **Aug 2024**: began in the yen and Asian equities, with crypto on the weekend; reversed within one day.
- **March 2020**: alternating ±9–12% days with circuit breakers; safe havens sold in the dash for cash; lasted about two weeks until Fed action.
- **April 2025**: a news-driven (headline) sequence with minute-scale reversals, simultaneous selling of US equities, Treasuries and the USD (USD weakness concentrated in Asian hours), and a policy reversal after a week.
- **SVB 2023**: a Treasury-led rotation (2y yield −97 bp over 3 days).
- **Oct 2025**: equity sell-off during US hours, then a crypto liquidity cascade after the US close, and a Monday rebound.

### Cited Findings
**August 2024 (yen carry unwind)**
- Trigger chain: BoJ hike on 31 Jul, then a weak US payrolls report on 2 Aug (+114k), then the 5 Aug crash. — [Substack summary (secondary)](https://moneybycj.substack.com/p/the-yen-carry-trade-that-crashed-the-markets)
- The BIS says leveraged positions in equity and FX markets unwound and amplified the reaction to a weak US release, after which markets stabilised quickly. The peak was 5 Aug, when TOPIX lost 12% in one day and the VIX briefly hit levels not seen since Covid. FX carry trades are estimated at about ¥40tn ($250bn), probably an underestimate. Fragility was visible from early July, when the yen began reversing from multi-decade lows. — [BIS Bulletin 90](https://www.bis.org/publ/bisbull90.htm); [Global Trading summary](https://globaltrading.net/?p=36090)
- The Nikkei 225 fell 12.4% on 5 Aug 2024, its worst day since 1987, and the S&P 500 fell about 3% the same day. — [CS Monitor/AP](https://csmonitor.com/World/2024/0806/stock-market-recession-carry-trade). Japanese shares soared in early trading on Tuesday 6 Aug, clawing back most of the previous day's losses. — [AP via WXOW](https://www.wxow.com/news/japan-stocks-rebound-sharply-after-worst-rout-in-history-in-boost-to-asia-markets/article_d5827838-2c44-54f1-9590-3969ed3eca84.html)
- The yen moved from about ¥146 to just below ¥142 per USD around the event, and from about 162 to 142 over three weeks peak-to-trough. (Secondary; levels not verified against wire data.) — [Substack summary](https://moneybycj.substack.com/p/the-yen-carry-trade-that-crashed-the-markets)
- The VIX spiked about 180% to almost 66 before the US open. This was the biggest one-day VIX spike ever, exceeding 2008 and March 2020, and was driven mainly by market makers widening SPX option quotes, especially puts (more than 85% of the spike), not by trades. — [BIS Bulletin 95](https://www.bis.org/publ/bisbull95.htm); [Finadium](https://finadium.com/?p=145021). The SEC DERA working paper reaches a similar conclusion: more OTM puts entered the VIX calculation and their mid-quotes surged. — [SEC DERA WP](https://sec.gov/files/dera-vix-working-paper-2504.pdf)
- Crypto timeline: the sell-off worsened on Sunday 4 Aug and early Monday 5 Aug (Asian hours). ETH fell as much as 25% intraday and BTC more than 11% over 24h, with more than $1bn liquidated. — [CoinDesk](https://coindesk.com/markets/2024/08/05/crypto-futures-witness-840m-in-liquidations-as-bitcoin-nosedives-ether-records-biggest-fall-since-2021)
- The Fed's Nov 2024 FSR (per secondary summaries) attributes part of the August volatility to leveraged investors. Institutions sold to meet internal volatility targets rather than because of extra margin calls. Liquidity in Treasuries and other markets deteriorated significantly but improved rapidly after favourable data the following week. — [American Banker](https://www.americanbanker.com/news/fed-flags-overheated-markets-as-top-stability-risk); [Longport summary](https://longportapp.cn/news/220507206)

**March 2020 (COVID crash, dash for cash)**
- Phases: flight to safety (about 21 Feb–11 Mar), dash for cash (about 11–23 Mar), easing after 23 Mar. On 16 Mar the S&P 500 lost 12%, its worst day since 1987, and the VIX hit an all-time peak of 83. Market depth in US equities and Treasuries fell to the worst levels of 2008. ETF prices and NAVs, and cash Treasuries and futures, dislocated. — [FSB Holistic Review](https://www.fsb.org/uploads/P171120-2.pdf)
- Daily path:
  - 9 Mar: S&P −7.6%; futures fell sharply pre-open, then a 15-minute circuit-breaker halt at the open.
  - 12 Mar: S&P −9.5%; trading halted after a 7.2% drop within 15 minutes of the open.
  - 13 Mar: about +9%.
  - 16 Mar: −12% to −13%, curb at the open; VIX close 82.69, the record.
  - 17 Mar: +6%. 18 Mar: −5%, fourth curb.
  - 24 Mar: S&P +9%.
  - The 10-year yield went from about 0.40% on 9 Mar to 1.23% on 18 Mar during the dash for cash.
  - — [Wikipedia: 2020 stock market crash](https://en.wikipedia.org/wiki/2020_stock_market_crash)
- Four market-wide circuit-breaker halts occurred in March 2020 (9, 12, 16, 18 Mar). — [SEC-filed working group report](https://www.sec.gov/file/exhibit-3-148); [StockAlarm summary](https://pro.stockalarm.io/blog/stock-market-circuit-breakers)
- Sunday-evening futures: on Sun 8 Mar, futures fell 4.89% overnight, triggering limit rules; on Sun 15 Mar (after the emergency Fed cut), Dow futures were limit-down at 5% by early evening. Under the 2020 rules the overnight limit was 5%. — [Fortune 16 Mar 2020](https://fortune.com/2020/03/16/wall-street-circuit-breakers-sp-500-coronavirus-covid-19-monday); search summary of Bloomberg reporting (not directly opened)

**April 2025 (tariff shock, "sell America")**
- 2 Apr (after the US close): tariffs announced; S&P futures −3.9%, NQ futures −4.7% immediately.
- 3 Apr: S&P −4.84%, Nasdaq −5.97%. 4 Apr: S&P −5.97%, VIX close 45.31, 10-year yield to 3.86%.
- 7 Apr: Nikkei −7.83% (curb), ASX −6% within 30 minutes, STOXX 600 −6% intraday. A false "90-day pause" headline caused a huge swing that reversed within about an hour.
- 9 Apr: after a pause was announced in the afternoon, S&P +9.52%, Nasdaq +12.16%, Dow +7.87%. 10 Apr: S&P −3.46%.
- 30-year yield +54 bp to 4.92%, the biggest three-day jump since 1982.
- — [Wikipedia: 2025 stock market crash](https://en.wikipedia.org/wiki/2025_stock_market_crash)
- 7 Apr false headline: the S&P fell as much as 4.7% at the open, then briefly gained up to 3.4%, adding about $3.6tn in value, before reversing. — [AOL/Yahoo Finance](https://www.aol.com/fake-news-4-trillion-swing-160048240.html). Risk.net: a surge of more than 6% shortly after the open, reversed an hour later. — [Risk.net](https://www.risk.net/node/7961352)
- Treasury microstructure (Fed FEDS Note, Nov 2025): 10-year Treasury futures volume spiked to nearly 10x normal for the time of day at 10:10–10:20 ET on 7 Apr and 13:20–13:30 ET on 9 Apr. On 7 Apr, cumulative sell imbalance exceeded $2bn shortly after 10:10 and dissipated over about 10 minutes. 9 Apr imbalances were two-way and below $1bn. — [Federal Reserve FEDS Note](https://www.federalreserve.gov/econres/notes/feds-notes/order-flow-imbalances-and-amplification-of-price-movements-evidence-from-u-s-treasury-markets-20251103.html)
- The 10-year yield fell from about 4.2% to 3.9% after 2 Apr, then rose about 60 bp to roughly 4.5%. Realized volatility peaked 7–9 Apr. — [Liberty Street (Apr 2026)](https://libertystreeteconomics.newyorkfed.org/2026/04/treasury-market-liquidity-since-april-2025/). The 10-year was above 4.51% intraday on 9 Apr before falling after the pause. — [NBC/CNBC](https://nbcmiami.com/news/business/money-report/10-year-treasury-yields-fall-after-trumps-tariff-reprieve/3588188). Long yields reversed from spike highs near 4.5% (10y) and 5.0% (30y), while short-dated yields rose after the pause. — [Saxo](https://home.saxo/en-gb/content/articles/macro/market-quick-take---10-april-2025-10042025)
- USD: the largest declines came in Asian hours, driven by non-US investors' hedging. — [BIS Bulletin 105](https://www.bis.org/publ/bisbull105.htm). A BIS working paper (Aug 2025) concludes that tariffs alone do not fully explain the later yield and dollar moves. — [Central Banking](https://www.centralbanking.com/central-banks/economics/7973496/tariffs-only-partly-explain-april%E2%80%99s-volatility-%E2%80%93-bis-paper)

**March 2023 (SVB)**
- On Monday 13 Mar 2023 (after the SVB failure on 10 Mar and the Sunday backstop), the 2-year Treasury yield fell below 4% intraday and was down about 48–53 bp during the session. This was the biggest one-day drop since 2008 and the biggest three-day drop (about 97 bp) since Black Monday 1987. Goldman forecast no Fed hike. — [Reuters via Kitco](https://www.kitco.com/news/off-the-wire/2023-03-13/treasuries-us-2-year-yield-plunges-most-2008-after-svb-collapse); [Kitco/Reuters](https://www.kitco.com/news/off-the-wire/2023-03-13/treasuries-us-two-year-yields-crash-wake-svb-collapse-yield-curve); [CNBC](https://www.cnbc.com/2023/03/13/us-treasury-yields-investors-assess-the-state-of-the-economy.html)
- Treasury bid-ask spreads widened more in March 2023 than in April 2025. — [Liberty Street (Nov 2025)](https://libertystreeteconomics.newyorkfed.org/2025/11/how-has-treasury-market-liquidity-fared-in-2025/)

**10–11 October 2025 (crypto liquidation cascade)**
- 14:57 UTC (10:57 ET): Trump post on Truth Social.
  - Sources conflict on content. bit.com says the post announced 100% tariffs. Barron's says the intraday post concerned China's rare-earth controls, and the explicit 100% tariff from 1 Nov was posted shortly after the US close.
  - Stocks opened higher and then reversed: Nasdaq Composite −3.6%, its worst day since 10 Apr; S&P 500 −2.7%.
  - VIX above 20 for the first time since April.
  - — [bit.com](https://www.bit.com/knowledge-hub/october-10-crypto-crash-binance-usde); [Barron's via Tiger](https://www.itiger.com/news/2574702483); [Motilal Oswal](https://www.motilaloswal.com/news/stocks/106729)
- Crypto sequence (UTC):
  - BTC held near $122.5k for hours after the post, and the sell-off accelerated after about 20:20.
  - 20:50–21:30: about $6.9bn liquidated, including $3.2bn in a single minute.
  - 21:36–22:15: Binance-internal depegs (USDe about $0.66, wBETH and BNSOL −80% to −88%).
  - BTC ended about −14.5% (≈$105k), ETH −12.2%, altcoins about −47% on average.
  - Perp open interest −43% ($217bn → $123bn); Hyperliquid OI −57%.
  - About $19bn and 1.6M accounts liquidated.
  - — [bit.com](https://www.bit.com/knowledge-hub/october-10-crypto-crash-binance-usde)
- Binance says about 75% of industry liquidations had occurred before 21:36 UTC, when two localized technical issues affected parts of its platform. — [Yahoo Finance](https://finance.yahoo.com/news/binance-pins-cryptos-worst-ever-085054129.html)
- Funding rates rose from about 10% to nearly 30% annualized by 6 Oct (pre-crash leverage build-up). Top-of-book depth fell more than 90% and spreads widened from single-digit bps to double-digit percentages at the extremes. Frozen interfaces stopped some traders managing risk. — [FTI Consulting](https://fticonsulting.com/insights/articles/crypto-crash-october-2025-leverage-met-liquidity)
- Monday 13 Oct: US stocks closed higher after Trump softened his stance. — [Anadolu Agency](https://www.aa.com.tr/en/economy/us-stocks-close-with-gains-on-possible-easing-trade-tensions/3716362)

**2026**
- The conflict with Iran began on 28 Feb 2026, after the sample of the NY Fed liquidity study. The authors note that economic uncertainty and rate volatility have risen since. — [Liberty Street (Apr 2026)](https://libertystreeteconomics.newyorkfed.org/2026/04/treasury-market-liquidity-since-april-2025/). BTC was near $65k in February 2026. — [bit.com](https://www.bit.com/knowledge-hub/october-10-crypto-crash-binance-usde)

### Inferences
- Duration differs by mechanism:
  - Leverage/carry unwinds (Aug 2024, Oct 2025 crypto) are violent for hours and largely reverse within 1–3 sessions.
  - Fundamental or policy regime shifts (March 2020; SVB rate repricing) persist for days to weeks until a policy backstop arrives.
  - Headline-driven shocks (April 2025) produce minute-scale whipsaws, and the dominant risk is reversal on the next headline.
- For "ride for hours, exit on fading momentum", the most favourable pattern is the persistent repricing seen in SVB 2y yields and in the 3–4 Apr 2025 consecutive down days. The least favourable are 7 Apr and 9 Apr 2025 and the March 2020 alternating days.
- Crypto can lag equities (Oct 2025) or lead them on weekends (Aug 2024). A cross-asset system needs explicit rules for which venue's signal counts at which hour.

### Gaps
- Minute-by-minute USDJPY/NQ/ES/BTC/gold timestamps for 5 Aug 2024 were not retrieved; Wikipedia page lookups returned 404 and the BIS PDF was blocked by a bot challenge.
- The exact time of the 9 Apr 2025 pause post is not confirmed by a fetched source. The Fed note's 13:20–13:30 ET volume spike is consistent with an early-afternoon post.
- Gold and BTC intraday paths for April 2025 and SVB were not retrieved.
- The 2026 Iran-conflict shock (and any later 2026 episodes) could not be researched because the search budget was exhausted.

---

## 5. Liquidity in stress: spreads, depth, slippage, circuit breakers, gaps, outages, API limits

### Takeaway
In major shocks, top-of-book depth in ES and crypto typically collapses by about 90%. Treasury spreads widen several-fold (up to about 6–10x in March 2020, much less in April 2025). Quote-based indicators (VIX, mid-prices) can be distorted by spread widening. CME equity futures have hard price limits and dynamic pauses that can freeze exits. Crypto venues throttle APIs, freeze UIs and trigger ADL exactly when they are needed most. A retail bot must assume worse fills, partial non-execution and connectivity loss in the very states it targets.

### Cited Findings
**Equity index futures (ES/NQ)**
- Week of 16 Mar 2020: E-mini S&P volume was 85% higher while order-book depth was about 90% lower than in the week of 20 Jan 2020. Fill-quality degradation was at most about 7.5 ticks for a 275-contract order, and it improved in April 2020. ES average daily volume rose about 166% (24 Feb–13 Mar vs Nov 2019–Jan 2020). Cost-to-trade rose much less than the daily true range. (CME-published, interested party.) — [CME "Assessing Liquidity"](https://www.cmegroup.com/education/articles-and-reports/assessing-liquidity.html); [CME "Holistic liquidity measures during COVID-19"](https://www.cmegroup.com/education/articles-and-reports/holistic-liquidity-measures-during-covid-19-supply-demand-and-market-conditions)
- April 2025: S&P 500 futures liquidity reportedly declined about 90% at the height of the tariff turmoil, as depth collapsed and liquidity providers fled. (Paywalled; headline/lede only.) — [Global Trading, 15 Apr 2025](https://www.globaltrading.net/?p=38057)
- CME US equity index futures price limits:
  - Overnight: ±7% plus a 3.5% dynamic circuit breaker, effective 12 Oct 2020; previously ±5%. Overnight, the market stays open but cannot trade beyond the limit. A move of more than 3.5% within an hour triggers a 2-minute pause.
  - Daytime: 7%/13%/20% levels coordinated with equity market-wide circuit breakers; 20% ends trading for the day.
  - Limits are referenced to a VWAP fixing taken between 14:59:30 and 15:00:00 CT.
  - Whether all parameters are still unchanged in 2026 is unverified.
  - — [CME Price Limits FAQ](https://www.cmegroup.com/trading/equity-index/faq-us-based-equity-index-price-limits.html.html); [CME "Understanding Price Limits and Circuit Breakers"](https://www.cmegroup.com/education/articles-and-reports/understanding-price-limits-and-circuit-breakers.html)
- NYSE market-wide circuit breakers: Level 1 = 7% (15-minute halt), Level 2 = 13%, Level 3 = 20%. — [FXStreet](https://fxstreet.com/education/what-are-stock-market-circuit-breaker-rules-202003201942)

**VIX / options**
- On 5 Aug 2024 the VIX rose about 180% pre-market to almost 66, mostly because of quote widening, not trades. VIX is computed from mid-quotes, so dealer quote widening mechanically raises it. Less-liquid puts drove more than 85% of the spike. — [BIS Bulletin 95](https://www.bis.org/publ/bisbull95.htm); [Finadium](https://finadium.com/?p=145021); [SEC DERA](https://sec.gov/files/dera-vix-working-paper-2504.pdf)

**Treasuries**
- March 2020:
  - 30-year bid-ask went from about 1/32 (28 Feb) to more than 5/32 (11–13 Mar), over 6x its post-crisis average. The 10-year spread about doubled and the 5-year widened about 50%.
  - 5- and 10-year depth fell to as low as 10% of the post-crisis average; 30-year to 38%.
  - Price impact reached about 5–6x average.
  - The worst window was 9–24 Mar.
  - — [Liberty Street (Apr 2020)](https://libertystreeteconomics.newyorkfed.org/2020/04/treasury-market-liquidity-during-the-covid-19-crisis)
- 10-year depth fell 93% from its February average to the lowest in history, and 30-year depth fell 76% (IMF GMM, cited by the FSB). — [FSB](https://www.fsb.org/uploads/P171120-2.pdf)
- April 2025:
  - Spreads widened after 2 Apr, but much less than in March 2020 and somewhat less than in March 2023.
  - Depth fell to its lowest since March 2023. Price impact jumped on 2 Apr and quickly reverted.
  - All measures normalised after 9 Apr; by early 2026 price impact was the lowest since 2021.
  - — [Liberty Street (Nov 2025)](https://libertystreeteconomics.newyorkfed.org/2025/11/how-has-treasury-market-liquidity-fared-in-2025/); [Liberty Street (Apr 2026)](https://libertystreeteconomics.newyorkfed.org/2026/04/treasury-market-liquidity-since-april-2025/)
- Order-flow imbalances amplify price moves when depth is thin: the 7 Apr 2025 sell imbalance of more than $2bn in ZN futures dissipated in about 10 minutes. — [Fed FEDS Note](https://www.federalreserve.gov/econres/notes/feds-notes/order-flow-imbalances-and-amplification-of-price-movements-evidence-from-u-s-treasury-markets-20251103.html)

**FX**
- April 2025 FX turnover was $9.5tn/day (+27% vs 2022) with no dollar-funding strains, so FX liquidity held up in volume terms. — [BIS QR Dec 2025](https://www.bis.org/publ/qtrpdf/r_qt2512b.htm). In March 2020, by contrast, offshore dollar funding was severely strained (large cross-currency basis dislocations). — [FSB](https://www.fsb.org/uploads/P171120-2.pdf)

**Gold**
- Gold fell 12% during the March 2020 dash for cash, and gold volatility rose as investors sold winners for cash. — [Cunliffe/BoE](https://www.bis.org/review/r220210f.htm); [FSB](https://www.fsb.org/uploads/P171120-2.pdf)

**Crypto**
- On 10 Oct 2025, BTC top-of-book depth fell more than 90% on key venues and spreads went from single-digit bps to double-digit % at the extremes. Market makers widened spreads or withdrew. Frozen interfaces blocked risk management. ADL closed profitable shorts. — [FTI Consulting](https://fticonsulting.com/insights/articles/crypto-crash-october-2025-leverage-met-liquidity)
- A secondary memo claims a 98% depth collapse ($1.2M → $27k) between 20:40 and 21:20 UTC. (Unverified.) — [tianpan.co memo](https://tianpan.co/investment-memo/2025-10-16-the-1011-crypto-storm)
- Binance:
  - Secondary post-mortems report intermittent Binance web/API outages around 20:50–22:00 UTC, API throttling, and users unable to cancel orders or adjust margin. Binance disputes the scope, saying core matching and APIs held. — [Insights4VC](https://insights4vc.substack.com/p/inside-the-19b-flash-crash); [The Defiant](https://thedefiant.io/newsletter/defi-daily/the-ultimate-10-10-crash-autopsy)
  - Binance's own account: localized issues before 21:36 UTC; about 75% of liquidations occurred before then. — [Yahoo Finance](https://finance.yahoo.com/news/binance-pins-cryptos-worst-ever-085054129.html)
  - A competitor alleged a 33-minute database processing delay. — [bit.com](https://www.bit.com/knowledge-hub/october-10-crypto-crash-binance-usde)
- BitMEX (a competitor) says numerous platforms suffered API overloads and system-wide lag. Hyperliquid processed about $10.3bn in liquidations, and its ADL was activated. — [BitMEX post-mortem](https://blog.bitmex.com/the-october-11-flash-crash)
- Binance Unified Account priced collateral (USDe, wBETH, BNSOL) from its own thin order books, causing venue-specific depegs (USDe about $0.66 vs $0.90–0.95 elsewhere). — [bit.com](https://www.bit.com/knowledge-hub/october-10-crypto-crash-binance-usde)

**Broker API limits (IBKR)**
- TWS API:
  - The default limit is 50 messages per second. Exceeding it returns error 100, and TWS will likely disconnect the client. With "reject" pacing, three violations terminate the session; otherwise TWS auto-paces (queues) requests.
  - Above 50 requests/s, orders may be queued and delayed, and IBKR suggests FIX.
  - The limit scales with market-data lines (lines ÷ 2 per second). FIX via IB Gateway allows 250 messages per second.
  - — [IBKR TWS API pacing](https://www.interactivebrokers.com/docs/tws-api/doc/pacing-limitations/introduction); [IBKR error codes](https://www.interactivebrokers.com/docs/tws-api/ref/error-codes); [IBKR pacing behaviour](https://www.interactivebrokers.com/docs/tws-api/doc/pacing-limitations/pacing-behavior); [IBKR Web API pacing](https://www.interactivebrokers.com/docs/web-api/trading/usage-and-availability/pacing-limitations)

### Inferences
- Backtest fills in stress should model the observed depth collapse: assume about 10% of normal top-of-book size and several ticks of slippage on ES/NQ market orders. For a 1–10-lot retail ES order the CME 7.5-tick figure (275 lots) is an upper bound, but 1–3 ticks in fast markets seems plausible. This is an inference; no retail-size source was found.
- Overnight equity index futures can lock at ±7% (with 2-minute pauses at ±3.5% per hour). A short in NQ is not automatically exitable in a limit-up reversal; this is a gap risk for "short the source asset" ideas.
- Do not use spot VIX (quote-based) as a real-time trigger in pre-market or other illiquid windows without spread filters. On 5 Aug 2024 it overstated actual volatility.
- For crypto legs, assume API degradation in the very minutes of peak opportunity. Use exchange-side stop/TP orders placed in advance rather than client-side logic, and avoid cross-margin with exotic collateral.
- At the bot's likely message rates (a handful of orders per minute) the IBKR 50 msg/s limit is not binding. The binding constraint is market-data subscription and historical-data pacing.

### Gaps
- No measured round-trip order latency for the IBKR TWS/Gateway API was found. Users should measure it themselves (timestamp at placeOrder vs. orderStatus/execDetails callbacks), especially from Germany to IBKR's US/EU servers.
- No source on gold futures (GC) or FX futures (6J/6S) depth and spreads during 5 Aug 2024 or April 2025 was found.
- No CME data on ZN/ZB futures (rather than cash) bid-ask in ticks during stress was found, and current CME interest-rate and metals dynamic circuit breaker parameters were not retrieved.
- No source on IBKR platform outages during the stress days was found.

---

## 6. Intraday momentum vs mean reversion: do moves persist after large shocks, and how much is left after the first hour?

### Takeaway
There is robust evidence of market intraday momentum. The return from the prior close to 30 minutes before the close predicts the last 30 minutes across 60+ futures in all asset classes (Sharpe 0.87–1.73 before costs), and the effect is stronger when option dealers are short gamma, on volatile, high-volume and news days, and in recessions. The predictability is small (R² about 2–3%), and the momentum reverts over the following days. Opening moves after large overnight returns tend to reverse partly, while multi-day momentum accrues overnight. For a rotation system this argues for holding with a shock into the close on volatile days but not overnight by default.

### Cited Findings
- Gao, Han, Li & Zhou (JFE 2018), SPY 1993–2013:
  - The first half-hour return (from the previous close) predicts the last half-hour return. The effect is stronger on volatile, high-volume, recession and macro-news days and also holds in 10 other ETFs.
  - A timing strategy earned 6.67% p.a. at Sharpe 1.08, vs 6.04% at Sharpe 0.29 for buy-and-hold.
  - — [Alpha Architect summary](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/); [WUSTL profile](https://profiles.wustl.edu/en/publications/market-intraday-momentum/)
  - Criticism: R² is about 0.02 and frictions are ignored. — [CXO Advisory](https://www.cxoadvisory.com/?p=25481)
- Baltussen, Da, Lammers & Martens (JFE 2021), 60+ futures (equity indices, 16 government bond futures, 21 commodities, 8 currencies), 1974–2020:
  - The rest-of-day return (prior close up to the last 30 minutes) positively predicts the last 30 minutes, with Sharpe ratios of 0.87–1.73 before costs.
  - Out-of-sample R² is 2.88% for pooled equity index futures and 0.60% for bond futures. In bonds, 11 of 16 contracts had positive, significant OOS R². Results are weaker for commodities and currencies.
  - Predictability reverts over the next days.
  - The mechanism is short-gamma hedging by option market makers and leveraged ETFs: momentum is present when net gamma exposure is negative and stronger the more negative it is.
  - S&P 500 futures remain net-profitable with a one-tick cost assumption.
  - The pattern was strong in Feb–May 2020; JPMorgan estimated more than $100bn of hedging-driven selling in two days in late Feb 2020.
  - — [Baltussen et al., JFE 142 (2021)](https://academicweb.nd.edu/~zda/intramom.pdf?utm_campaign=redirect&utm_medium=web&utm_source=www3.nd.edu); [EUR repository](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/)
- Nasdaq-100 futures show both momentum and reversal, depending on the signs of yesterday's and last night's returns and on whether it is Monday. Last night's return is mostly associated with intraday reversal. — [Yu, Rentzler & Wolf, JOIM](https://joim.com/downloads/nasdaq-100-index-futures-intraday-momentum-reversal)
- S&P 500: an opening reversal turns into closing momentum, and the opening reversal is concentrated on days with negative overnight returns. — [Southampton thesis](https://eprints.soton.ac.uk/452387)
- Older US index-futures evidence (1987–2002): highly significant intraday reversals after large opening moves, more pronounced after large positive opens. Significance drops sharply after a bid-ask cost proxy. (Attribution from search summary; full text not opened.) — [Montclair repository](https://digitalcommons.montclair.edu/acctg-finance-facpubs/70)
- In commodity futures, high-frequency realized semivariance helps predict time-series momentum reversals and improves on standard TSMOM out of sample. — [Liu et al., Reading repository](https://centaur.reading.ac.uk/111035/1/Anonymized%20manuscript-R1.pdf)
- Momentum profits accrue overnight and tend to reverse intraday at the stock level. — [Lou, Polk & Skouras](https://personal.lse.ac.uk/polk/research/TugOfWar.pdf)
- How long the price pressure lasts in stress episodes:
  - April 2025 ZN: a $2bn+ sell imbalance dissipated in about 10 minutes. — [Fed FEDS Note](https://www.federalreserve.gov/econres/notes/feds-notes/order-flow-imbalances-and-amplification-of-price-movements-evidence-from-u-s-treasury-markets-20251103.html)
  - Aug 2024: the Nikkei recovered most of its −12.4% the next morning. — [AP via WXOW](https://www.wxow.com/news/japan-stocks-rebound-sharply-after-worst-rout-in-history-in-boost-to-asia-markets/article_d5827838-2c44-54f1-9590-3969ed3eca84.html)
  - March 2020: daily S&P moves alternated between about −10% and +9%. — [Wikipedia 2020 crash](https://en.wikipedia.org/wiki/2020_stock_market_crash)
  - SVB: the 2-year yield fell about 97 bp over 3 days, a persistent move. — [Kitco/Reuters](https://www.kitco.com/news/off-the-wire/2023-03-13/treasuries-us-two-year-yields-crash-wake-svb-collapse-yield-curve)
  - April 2025: S&P −4.84% and −5.97% on consecutive days (3–4 Apr), then a policy reversal of +9.52% on 9 Apr. — [Wikipedia 2025 crash](https://en.wikipedia.org/wiki/2025_stock_market_crash)

### Inferences
- How much of a move is left after the first hour: no source quantifies it directly. The combined evidence suggests that, on high-volatility, short-gamma days, the direction of the day's move up to mid-afternoon tends to extend into the final 30 minutes. That supports "join and hold to the close" over "fade" for equity index and bond futures on shock days.
  - The expected extension is small relative to the day's range (low R²).
  - Next-day reversal risk is material (Baltussen; Aug 2024; March 2020).
  - A realistic design is to enter after confirmation (e.g. 30–90 minutes into a shock), exit into the close, and re-assess overnight rather than carry by default.
- Momentum appears strongest when it is mechanically forced (dealer short gamma, vol-targeting deleveraging, margin-driven liquidations). Proxies for these (SPX dealer gamma estimates, realized vol jumps, crypto funding/OI) could serve as continuation filters.
- After large overnight gaps, especially negative ones, the first 1–1.5 hours of US cash trading are prone to reversal, so a bot should not chase the open.

### Gaps
- No study directly measures the "fraction of the eventual daily or multi-day move remaining after the first hour" for unscheduled cross-asset shocks.
- No intraday momentum evidence specific to crypto or to FX safe havens (JPY/CHF) on shock days was retrieved.
- Post-2020 out-of-sample performance of the Gao et al./Baltussen et al. effects was not verified.

---

## 7. Practical backtesting pitfalls for intraday cross-asset systems

### Takeaway
The main risks to a cross-asset intraday backtest are:
- Timestamp misalignment across venues with different sessions and daily cut-offs.
- Quote-based or stale indicators (VIX mid-quotes, ETF vs NAV, futures vs cash dislocations).
- Assuming normal-day spreads and depth in exactly the stressed states the strategy targets.
- Ignoring price limits, halts and exchange or API failures.
- Data-mined seasonalities that decay after publication (the overnight drift).
- Under-modelled costs: Gao-type effects have R² of about 2% and are easily consumed by a tick or two.

### Cited Findings
- Different daily cut-offs:
  - CME equity index limits use a 14:59:30–15:00:00 CT VWAP fixing. — [CME FAQ](https://www.cmegroup.com/trading/equity-index/faq-us-based-equity-index-price-limits.html.html)
  - Crypto daily candles often run 00:00–23:59 UTC (e.g. TradingView), as noted in CoinDesk's ETH daily-drop computation. — [CoinDesk](https://coindesk.com/markets/2024/08/05/crypto-futures-witness-840m-in-liquidations-as-bitcoin-nosedives-ether-records-biggest-fall-since-2021)
  - Baltussen et al. define each futures market's day by its own pit/day-session hours (e.g. US 30-year T-bond futures 08:20–15:00 CT; Japanese 10-year JGB futures 08:45–15:00 local). — [Baltussen et al.](https://academicweb.nd.edu/~zda/intramom.pdf?utm_campaign=redirect&utm_medium=web&utm_source=www3.nd.edu)
- Stale and dislocated prices in stress: during March 2020, prices that usually move together dislocated (on-the-run vs off-the-run Treasuries, ETF prices vs NAV, cash Treasuries vs futures). — [FSB](https://www.fsb.org/uploads/P171120-2.pdf)
- Quote-based index artefacts: the VIX pre-market spike on 5 Aug 2024 reflected widening option quotes, not trades. — [BIS Bulletin 95](https://www.bis.org/publ/bisbull95.htm)
- Venue-specific prices: on 10 Oct 2025, USDe traded at about $0.66 on Binance vs $0.90–0.95 elsewhere. Some BTC exchange prices lag others by up to 15 seconds. — [bit.com](https://www.bit.com/knowledge-hub/october-10-crypto-crash-binance-usde); [CBS thesis](https://research-api.cbs.dk/ws/portalfiles/portal/59795067/612646_High_Frequency_Lead_Lag_Relationships_in_The_Bitcoin_Market.pdf)
- Liquidity costs in stress: ES depth −90% and fill degradation up to about 7.5 ticks (275 lots) in March 2020 [CME](https://www.cmegroup.com/education/articles-and-reports/assessing-liquidity.html). Treasury spreads widened by up to 6x (30-year) [Liberty Street 2020](https://libertystreeteconomics.newyorkfed.org/2020/04/treasury-market-liquidity-during-the-covid-19-crisis) or 10x [Cunliffe](https://www.bis.org/review/r220210f.htm). Crypto spreads reached double-digit % at the extremes [FTI](https://fticonsulting.com/insights/articles/crypto-crash-october-2025-leverage-met-liquidity). Weekend BTC spreads are more than 2x weekday [investingLive/Kaiko](https://investinglive.com/cryptocurrency/bitcoin-isn-t-a-weekend-hedge-it-s-just-the-only-market-still-open/).
- Transaction costs vs edge:
  - Intraday-momentum results are reported without costs. Exploiting them requires frequent rebalancing, so they may not survive costs for many investors. — [Baltussen et al.](https://academicweb.nd.edu/~zda/intramom.pdf?utm_campaign=redirect&utm_medium=web&utm_source=www3.nd.edu)
  - R² for SPY first-half-hour predictability is about 0.02. — [CXO Advisory](https://www.cxoadvisory.com/?p=25481)
  - Older intraday-reversal profits shrink sharply after bid-ask costs. — [Montclair repository](https://digitalcommons.montclair.edu/acctg-finance-facpubs/70)
- Pattern decay (look-ahead or data-snooping risk): the 02:00–03:00 ET overnight drift (about 3.7% p.a., 1998–2020) averaged about zero after 2021, and products built to harvest it closed within about 14 months. — [Liberty Street (Jul 2026)](https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/)
- Regime-dependent correlations: BTC–Nasdaq correlation went from 0.87 (2024) to about 0.3 (March 2026). — [arXiv](https://arxiv.org/abs/2501.09911v1); [eco3min](https://eco3min.fr/en/bitcoin-vs-nasdaq/). Stock–bond correlation turned positive during the March 2020 dash for cash. — [FSB](https://www.fsb.org/uploads/P171120-2.pdf)
- Halts and limits: four NYSE market-wide halts in March 2020 [SEC report](https://www.sec.gov/file/exhibit-3-148). Overnight futures limits were ±5% in 2020 and ±7% plus a 3.5% DCB since Oct 2020 [CME FAQ](https://www.cmegroup.com/trading/equity-index/faq-us-based-equity-index-price-limits.html.html). Backtests on limit-locked bars assume fills that were impossible.
- Infrastructure failures: crypto API throttling and outages and ADL on 10 Oct 2025. — [FTI](https://fticonsulting.com/insights/articles/crypto-crash-october-2025-leverage-met-liquidity); [BitMEX](https://blog.bitmex.com/the-october-11-flash-crash). IBKR API pacing: error 100 and possible disconnect above 50 msg/s, queued orders. — [IBKR](https://www.interactivebrokers.com/docs/tws-api/doc/pacing-limitations/introduction)

### Inferences (design and backtest checklist derived from the findings)
1. **Time alignment**: store all data in UTC with exchange-session calendars. Compute cross-asset signals only from bars where every input market is actually trading. Otherwise the "lead" is just a stale price, e.g. Xetra/NYSE closed while Globex/crypto trade, or a JGB futures close vs a US afternoon.
2. **Bid/ask, not mid**: simulate entries and exits at the touch (ask for buys, bid for sells) plus stress-dependent slippage scaled by realized volatility or depth proxies. Mid-price backtests overstate profits most in exactly the shock windows a rotation system targets.
3. **Limits and halts**: flag limit-locked and halted intervals (CME ±7% overnight, 3.5% DCB pauses, 7/13/20% daytime) and disallow fills there.
4. **Futures rolls**: use back-adjusted continuous series for signals but trade the actual contract with roll dates matching IBKR availability. Avoid signals around roll weeks when the front contract's liquidity drains. This is standard practice; no specific source was retrieved.
5. **Latency**: model a realistic decision-to-fill delay for a retail IBKR bot, likely seconds rather than milliseconds once data-arrival, computation, and order-routing/acknowledgement delays are included. This is an inference; no measured figure was found. Do not assume entries at the bar close that triggered the signal; use the next bar's open or later.
6. **Survivorship and look-ahead**: use only information available at that time, e.g. Wikipedia-style closing data must not inform intraday decisions. Be wary of event-study selection, where testing only on famous crashes overfits. Include "false alarm" days, such as headline whipsaws like 7 Apr 2025.
7. **Out-of-sample by regime**: test separately on flight-to-safety, dash-for-cash and sell-America regimes, and on pre/post-2021 data (overnight drift decay, post-ETF crypto microstructure).
8. **Crypto venue risk**: model exchange-specific prices (no global mid), API unavailability windows and ADL. Prefer the most liquid venue or CME crypto futures for signals.

### Gaps
- No primary source was retrieved on futures roll methodology pitfalls, stale-price bias in asynchronous correlation estimation (e.g. Burns–Engle–Mezrich), or quantified IBKR order-routing latency from Europe.
- Typical IBKR commission and exchange fees per ES/MES/ZN/6J/GC/MBT contract were not researched here (likely covered by another workstream).
- No independent measurements of retail-size (1–10 lot) slippage in ES/NQ during 5 Aug 2024 or April 2025 were found.
