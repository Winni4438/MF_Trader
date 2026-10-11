# Practitioners and Retail Feasibility of Cross-Asset Capital-Flow / Rotation Trading (status: October 2026)

Research notes for a German retail trader (50–250k EUR, IBKR as data source, fully automated execution, holding periods of hours to 1 day, risk-on/risk-off rotation between Nasdaq/BTC and gold/Treasuries/JPY/CHF).
Method note: The web-search budget ran out partway through, so some items below are marked as gaps rather than filled from memory. IBKR price lists were pulled directly from interactivebrokers.com on 2026-10-11.

---

## 1. Which professional strategy families trade "flows" or rotation, and how do they do it?

### Takeaway
No major professional category trades a discretionary "money flow" signal intraday the way the user describes. Close relatives exist in three forms: (a) systematic managed futures/CTAs, which follow price trends across about 50–100+ futures and react to rotation after it shows up in prices, with short-term CTAs at holding periods of about 1–10 days; (b) bank flow and positioning desks (JPM, Goldman, Nomura), which model other players' mechanical flows (CTA triggers, vol-control) and publish them as research; (c) academic and bank RORO indices, which describe the regime but are used for allocation and research rather than as intraday trading signals. Exploiting cross-asset lead-lag at sub-second horizons is HFT territory.

### Cited Findings
**Managed futures / CTA (long-term trend)**
- SG Trend Index = the 10 largest trend-following CTAs. Constituents for 2026 (per search-engine summary of the SG constituent PDF; the PDF itself could not be fetched directly): AlphaSimplex, AQR, Aspect, Graham, iSAM Vector, Lynx, Man Group, PIMCO, Transtrend, Winton — [SG Trend Index Constituents (PDF)](https://wholesale.banking.societegenerale.com/fileadmin/indices_feeds/SG_Trend_Index_Constituents.pdf); [Hedgeweek: SG releases 2026 constituents](https://www.hedgeweek.com/sg-prime-services-releases-the-cta-indices-constituents-for-2026/)
- Changes for 2026: AFBI Multi-Strategy and Crabel Advanced Trend join the SG CTA Index, and CFM ISTrends returns — [Alternative Fund Insight](https://alternativefundinsight.com/societe-generale-updates-membership-of-cta-indices/)
- Man AHL describes trend "speed" as the trend-length sensitivity of the signal (double-EWMA crossovers). Its universe is the 50 most liquid futures/FX forwards, with 25% risk each in equities, fixed income, FX and commodities. The backtest runs 1995–Aug 2022 — [Man Group, "The Need for Speed in Trend-Following Strategies"](https://www.man.com/insights/need-for-speed-trend-following)
- Man's dispersion study (data through Dec 2024): differences in speed, market set and carry explain most of the 10–20% annual return spread among SG Trend Index constituents. Faster systems and those tilted to alternative markets did better in crises such as 2008 and 2022 — [The Idea Farm / Man "Dynamics of Dispersion"](https://theideafarm.com/alternative-investment/trend-following/a-trend-following-deep-dive-the-dynamics-of-dispersion/)

**Short-term CTAs (closest professional analogue to hours-to-1-day holding)**
- The SG Short-Term Traders Index (STTI) "is designed to track the daily performance of a portfolio of short term CTAs" — [BarclayHedge STTI page](https://portal.barclayhedge.com/cgi-bin/indices/displayHfIndex.cgi?indexCat=SG-Prime-Services-Indices&indexName=SG-Short-Term-Traders-Index)
- Crabel (2019 profile): the flagship Multi-Product holds positions about **1 day on average**. Contra holds about 7 days and Gemini about 10 days, and Gemini excludes timeframes under 2 days. Turnover is about 15,000 round turns per USD 1m of capital per year for the flagship, 5–6k for Contra and ~4k for Gemini. Execution has been fully automated since 2009, with co-location in Chicago/NY since 2011 and Hong Kong/Frankfurt since 2013. About 99% of orders go direct to the exchange at **~15 µs latency**. Crabel trades about 60 million futures/FX contracts a year through 30 FX liquidity providers — [The Hedge Fund Journal, "Crabel Contra" (Oct 2019)](https://thehedgefundjournal.com/crabel-contra/)
- Crabel Contra was built because clients wanted a faster product after trend following failed in the abrupt reversals of February and October 2018. It targets an average equity beta of −0.4, 10% volatility and a 2.5% daily portfolio stop. Its "portfolio protection" sleeve reacts to intraday drawdowns and "produces false alarms, which typically cause modest losses" — [HFJ (2019)](https://thehedgefundjournal.com/crabel-contra/)
- Crabel Multi-Product: "the majority of the price-driven strategies can be classified as short-term momentum or mean-reversion trades." A third-party report lists AUM of about USD 1.39bn and a 2025 return of −6.24% (max DD −8.25%). This is secondary data and should be verified with the manager — [Autumn Gold CTA report](https://www.autumngold.com/ascent/gold_report.php?id=113230)

**Bank flow and positioning desks**
- JPMorgan Flows & Liquidity (Panigirtzoglou) / Delta-One: the desks estimate CTA positioning from "key momentum indicators" and project where signals flip. Example from early 2025: CTAs long US equities, short US/EU rates, long metals and USD — [Tickmill summary of JPM Delta-One (Jan/Feb 2025)](https://www.tickmill.com/blog/institutional-insights-jpmorgan-flows-positioning-130125); [Tickmill, CTA signals](https://try.tickmill.com/blog/institutional-insights-jpmorgan-delta-one-flows-positioning-cta-signals)
- In a 2024 JPM note, net longs of asset managers and leveraged funds as a percentage of open interest reached a decade high. Together with elevated momentum-trader positioning, JPM said this left equities vulnerable — [Tickmill/JPM summary, as above](https://www.tickmill.com/blog/institutional-insights-jpmorgan-delta-one-flows-positioning-050225)
- In a momentum-to-value rotation, JPM put CTA losses at about one third of the February 2018 "quant quake," with CTA positioning extreme only in bonds — [BloombergQuint](https://www.bloombergquint.com/markets/jpmorgan-says-the-momentum-rotation-isn-t-a-quant-quake-yet)
- Goldman Sachs (Cullen Morgan, equity derivatives/flows) publishes scenario tables for CTA selling. Examples from Feb 2026: about USD 33bn of selling in a week if stocks fell again, and about USD 80bn over a month if the S&P 500 dropped below 6,707. Elsewhere, CTAs were estimated about USD 129bn long, with modelled selling of USD 10bn in a rising and up to USD 42bn in a falling market over one week. These figures come from secondary or syndicated copies with inconsistent dates — [Longport/Jinshi](https://longportapp.cn/topics/38598301); [MEXC news](https://www.mexc.com/news/666746); [The Wealth Advisor](https://www.thewealthadvisor.com/article/goldman-says-momentum-traders-sell-stocks-every-scenario)
- BofA (Mar 2025): before the 2 April 2025 tariff deadline, trend-following CTAs held their largest S&P 500 short since February 2016 — [roic.ai/BofA](https://www.roic.ai/news/bofa-warns-of-growing-cta-short-positions-in-us-equities-ahead-of-tariff-deadline-03-31-2025)

**RORO indices / products**
- HSBC built a "RORO Index" from the variance of daily returns across 34 asset categories. Around 2010, HSBC analysts considered RORO "a new structural reality" — [Institutional Investor, "Examining the Contradictions of RORO" (old, ~2016/17)](https://www.institutionalinvestor.com/article/b14zb96hrjdqzs/examining-the-contradictions-of-roro); [New Statesman (2012)](https://www.newstatesman.com/business/economics/2012/04/roro-risk-risk)
- Academic RORO index (Chari, Dilts Stedman, Lundblad; KC Fed RWP 24-12, Nov 2024): the first principal component of daily changes in advanced-economy credit risk, equity volatility, funding conditions, and currencies and gold. It shows risk-off skewness and fat tails, with sharp risk-off moves in the GFC, the euro crisis, the taper tantrum and COVID. **Daily and weekly data are public** at anushachari.weebly.com/roro.html and updated monthly — [KC Fed working paper](https://www.kansascityfed.org/documents/10594/rwp24-12charistedmanlundblad.pdf)

**Cross-asset HFT lead-lag**
- ES futures and SPY are almost perfectly correlated at minute, hour and day horizons, but the correlation "breaks down completely" at millisecond horizons. Budish et al. estimate about 1,000 ES–SPY arbitrage opportunities per day, worth about USD 75m a year, all captured by the fastest traders — [Budish, Cramton, Shim (NBER/QJE 2015)](https://conference.nber.org/conf_papers/f69665.pdf); [Chicago Booth Review](https://www.chicagobooth.edu/review/alternative-high-frequency-trading)
- Aquilina, Budish and O'Neill plot median latency-arbitrage race durations in milliseconds (axis up to ~250 ms) for 2005–2011 — [Budish slides, NBER 2023](https://conference.nber.org/confer/2023/MDs23/BudishSlides.pdf)

### Inferences
- The user's concept ("detect rotation as it happens, hold hours to 1 day") falls between short-term CTAs (STTI universe, Crabel-type momentum/mean-reversion at 1–10 days) and HFT lead-lag. The HFT end is unreachable for retail. The short-term CTA end is reachable only with careful cost control.
- What bank flow desks offer is mostly a forecast of other systematic players' mechanical flows (CTA trigger levels, vol-control rebalancing). A retail system could treat these published levels as context, but they reach retail via secondary channels, often late and inconsistent.
- RORO is better used as a regime filter (risk-on/off state, daily) than as an intraday trigger, since the public index is daily/weekly and updated monthly.

### Gaps
- No primary 2025–2026 documents from HSBC or Citi on still-live RORO-linked investable indices were found. Whether HSBC's RORO index is still published is unknown.
- No Nomura (McElligott) primary or secondary source was found within budget.
- No performance data for discretionary global macro or tactical asset allocation (HFR Macro etc.) was collected for 2024–2026.
- Risk parity and vol-targeting overlays (e.g., 2022 drawdowns, August 2024 deleveraging) have no sourced numbers. The August 2024 yen-carry unwind is documented only generically (yen +~6% within days) — [WisdomTree (Dec 2025)](https://www.wisdomtree.eu/de-lu/blog/2025-12-05/positioning-for-a-stronger-yen); [Block Scholes (Aug 2024)](https://blockscholes.com/premium-research/carry-trade-collapse)

---

## 2. How did these strategies perform? SG indices 2015–2026, short-term vs long-term trend

### Takeaway
Long-term trend (SG Trend) has a CAGR of about 5.3% since 2000, with a max drawdown of about 21%. It had a weak 2023–H1 2025 (13-month drawdown, a −9.3% YTD trough in April 2025) and then a strong 2026 (SG CTA about +15.7% for the nine months to September; about +16% YTD by 11 Oct 2026). Short-term traders (STTI) were much more stable in the 2025 whipsaw (about −0.9% YTD in April 2025 vs −9.3% for SG Trend). But they lag heavily in strong trend years (2026 YTD +5.3% vs +16.1%). Short-term is a diversifier, not a better trend strategy.

### Cited Findings
**Current status (estimated, 11 Oct 2026)**
- SG CTA Index: MTD +0.42%, **YTD +16.15%** — [BarclayHedge SG CTA](https://portal.barclayhedge.com/cgi-bin/indices/displayHfIndex.cgi?indexCat=SG-Prime-Services-Indices&indexName=SG-CTA-Index)
- SG Trend Index: MTD +0.28%, **YTD +16.14%** — [BarclayHedge SG Trend](https://portal.barclayhedge.com/cgi-bin/indices/displayHfIndex.cgi?indexCat=SG-Prime-Services-Indices&indexName=SG-Trend-Index)
- SG Short-Term Traders Index: MTD −0.92%, **YTD +5.32%** — [BarclayHedge STTI](https://portal.barclayhedge.com/cgi-bin/indices/displayHfIndex.cgi?indexCat=SG-Prime-Services-Indices&indexName=SG-Short-Term-Traders-Index)
- SG CTA Index +15.7% for the nine months to end Q3 2026, vs S&P 500 +11.7%. Drivers: short US Treasuries going into the September bond sell-off, long USD, and long crude since January 2026 ahead of the Iran war (started 28 Feb 2026). Andrew Beer (DBi) described CTA positioning as "early, contrarian and right" (CNBC 6 Oct 2026, via secondary reports) — [HedgeCo](https://hedgeco.net/news/?p=92151); [Political.org](https://political.org/2026/10/05/quant-hedge-funds-outpace-sp-500-in-2026-by-betting-early-against-bonds-and-on-oil/); [Pluang](https://pluang.com/en/news-feed/indeks-sg-cta-naik-157-persen-sembilan-bulan)
- SG Trend as of 11 Sep 2026: September +2.79% MTD and +14.18% YTD. Gains came from energy (WTI +9.4% in the week), short bonds, and JPY +1.58% — [TTU Week in Review 11 Sep 2026](https://www.toptradersunplugged.com/trend-following-week-in-review-september-11-2026/)

**2025 (whipsaw year)**
- SG Trend −4.89% in April 2025 and −9.33% YTD after April. The SG Trend trailing max DD was 20.61% — [content.sgmarkets / TTU April 2025](https://www.toptradersunplugged.com/trend-following-performance-report-april-2025/); [SG CTA Update 2025](https://content.sgmarkets.com/CTA_UPDATE_KEEPING_UP_WITH_THE_TRENDFOLLOWERS_2025)
- STTI after April 2025: about −0.9% for the month and YTD, versus SG Trend −9.3% YTD. After March 2025, STTI was −0.11% YTD (March +1.11%) — [SG CTA Update 2025](https://content.sgmarkets.com/CTA_UPDATE_KEEPING_UP_WITH_THE_TRENDFOLLOWERS_2025); [The Full FX](https://thefullfx.com/ctas-tough-start-to-2025-continues/)
- Full year 2025: SG Trend +2.39% (Dec +1.92%), BTOP50 +2.81%, S&P 500 TR +17.89%. Long-term figures: SG Trend CAGR 5.33% since 2000 (max DD 20.61%), BTOP50 4.08% (max DD 15.94%), S&P 500 TR 7.98% since 2000 (max DD 50.95%) — [TTU Performance Report Dec 2025](https://www.toptradersunplugged.com/trend-following-performance-report-december-2025/)
- SG CTA Index full year 2025 about −0.2% (secondary, unverified) — [Aussie Turtles, Battle of the Trend Indexes Dec 2025](https://www.aussieturtles.com/battle-of-the-trend-following-indexes-december-2025/)
- April 2025 single-manager figures ("Liberation Day"): Mulvaney −40.67% (YTD −39.22%), Tulip Trend −8.1% (YTD −28.5%), Aspect Diversified −9.6% (YTD −13.5%), DUNN WMA −3.18%, Quantedge about −10%, QMS Diversified Global Macro +5.38% (YTD +20.2%). Tulip reported "three days of extreme losses" and recovered about half of them — [Institutional Investor](https://www.institutionalinvestor.com/index.php/article/top-managed-futures-funds-are-down-sharply-liberation-day)
- With Intelligence: "short-term CTAs have been better positioned to handle the day-to-day market volatility due to their shorter holding periods." V-shaped tariff reversals hurt large trend followers, who were in a "deep, 13-month drawdown" — [With Intelligence CTA report](https://www.withintelligence.com/insights/cta-hedge-fund-report/)
- IASG on April 2025: "massive moves up and down, many of which were against the current trends." The S&P fell from about 6,147 to about 4,802 by 4 April before the sharp rally on 9 April — [IASG](https://www.iasg.com/?p=11317)

**2024 and older (marked as older)**
- STTI 2024: April +2.2% (YTD +3.28%), May −0.77% (YTD +4.51%). No full-year figure was found — [The Full FX (2024)](https://thefullfx.com/ctas-suffer-first-negative-month-in-2024/)
- 2016 (old): STTI −1.15% YTD through November and the best SG CTA index of the year, versus SG Trend −6.79% and SG CTA −3.38%. SG's Tom Wrobel: short-term traders do better when trends are absent — [Hedgeweek (Dec 2016)](https://www.hedgeweek.com/short-term-ctas-show-improved-performance/)
- Crabel (2019): the flagship and Gemini had outperformed the STTI "by a large margin." Contra returned about 6% from May to August 2019 while equities were flat — [HFJ (2019)](https://thehedgefundjournal.com/crabel-contra/)
- Crabel Gemini: about a 10-day average hold, 10% vol target, peak-to-valley DD −10.95% from Dec 2024 to May 2025 (secondary) — [Autumn Gold](https://www.autumngold.com/ascent/leaf_report.php?id=113230)

### Inferences
- STTI and SG Trend behave as complements. STTI held up better in reversal regimes (2016, H1 2025) and lagged in persistent macro trends (2026). A system designed to "ride rotation for hours" will likely look like the STTI profile: lower drawdowns in whipsaw, but no large payoff in multi-month trends.
- The 2026 gains came from multi-week to multi-month macro trends (bonds short, oil long, USD long), not from intraday rotations. That supports adding at least a daily or weekly trend component alongside any intraday layer.

### Gaps
- No annual STTI returns for 2015–2025 could be retrieved; BarclayHedge offers them only as a download. Full-year STTI 2024 and 2025 figures are therefore missing.
- No 2025/2026 figures were found for Man AHL, Winton, Quantica or Crabel at single-fund level, apart from the secondary Crabel figures above.
- One secondary source claims the SG CTA Index returned under 2% a year over ten years with about a 22% max DD. It could not be verified and is not used.

---

## 3. Intraday vs daily/weekly: speed, costs, capacity, crowding, alpha decay (practitioner view)

### Takeaway
Practitioners largely agree on three points. Faster trend signals offer better crisis protection (crisis alpha, positive skew) but a materially lower Sharpe after costs. Short horizons reduce capacity and demand top execution. Intraday models suffer alpha decay and model turnover (Crabel: 10–15% of models replaced each year). Intraday cross-asset effects do exist (e.g., intraday momentum), but they are small (R² of about 2%) and depend on news days.

### Cited Findings
- Man AHL: all speeds have a positive gross Sharpe, and slower speeds have higher risk-adjusted returns. **After costs, Sharpe is "materially lower for faster speeds over the long-term"**, because higher turnover means crossing the spread more often. Skewness stays positive and is higher for fast systems. Fast systems did best in the worst S&P quintile ("crisis alpha"), even after costs. Correlation between the fastest and slowest speed is **0.17**. The cost model assumes a USD 5bn portfolio. AHL says its execution costs are about half those of bank algos (company claim). The study does not cover intraday — [Man Group](https://www.man.com/insights/need-for-speed-trend-following)
- Crabel: shorter holding periods and more intraday trading reduce capacity. Contra (about 7-day hold) has capacity of about USD 3bn, and the 1-day flagship has less. Crabel believes its trend-following execution is "five to ten times better than the average trend follower." Alpha decay is handled with stop-losses at position, market and strategy level, with expected model turnover of 10–15% per year — [HFJ (2019)](https://thehedgefundjournal.com/crabel-contra/)
- Older Newedge research argued that asset growth has only a "muted impact" on CTA performance (date unclear, paywalled) — [Risk.net](https://www.risk.net/node/2290596)
- Market intraday momentum (Gao, Han, Li, Zhou, JFE 2018): the first half-hour SPY return (measured from the previous close) predicts the last half-hour return, with data from 1993–2013. The effect is stronger on volatile, high-volume, recession and macro-news days, and also appears in 10 other liquid ETFs. In the working-paper version, R² is about 0.02 — [WUSTL profile](https://profiles.wustl.edu/en/publications/market-intraday-momentum/); [Alpha Architect](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/)
- A follow-up on Chinese commodity futures (copper, steel, soy, soymeal) finds the same first-to-last half-hour momentum, strongest on high-volume or high-volatility sessions — [Hull repository](https://hull-repository.worktribe.com/OutputFile/3303156)
- Crowding: JPM in a 2024 note on equity futures; BofA in March 2025 on the largest CTA S&P short since 2016. In April 2025 the crowded CTA positions were hit by V-shaped reversals — [Tickmill/JPM](https://www.tickmill.com/blog/institutional-insights-jpmorgan-delta-one-flows-positioning-050225); [roic.ai/BofA](https://www.roic.ai/news/bofa-warns-of-growing-cta-short-positions-in-us-equities-ahead-of-tariff-deadline-03-31-2025); [Institutional Investor](https://www.institutionalinvestor.com/index.php/article/top-managed-futures-funds-are-down-sharply-liberation-day)
- Clients asked for faster CTAs after trend following failed in the abrupt reversals of February and October 2018. Fast "protection" sleeves produce false alarms with small losses — [HFJ (2019)](https://thehedgefundjournal.com/crabel-contra/)

### Inferences
- For a retail system at hours to 1 day, cost per round turn is the main lever. Even AHL, at institutional cost levels, sees fast signals lose after costs. A retail trader pays more than AHL per unit of turnover (no co-location, no in-house execution algos), so an intraday rotation strategy needs a clearly higher gross edge than a daily one.
- Faster signals do serve as a "crash hedge" (positive skew in equity sell-offs). A sensible design goal is therefore a risk-off hedge or crisis-alpha sleeve on top of a slower core strategy, not a stand-alone return engine.
- Known intraday effects (intraday momentum around macro news days) are weak (R² of about 2%), so they need many independent bets. With 5–10 macro futures and 1-day holding, statistical significance takes a long time to build.

### Gaps
- No quotes or blog articles from Robot Wealth, Quantpedia or Ernie Chan specifically on intraday cross-asset systems were retrieved. The search budget was exhausted. Quantpedia lists only a monthly "Asset Class Trend-Following" (indicative 11.27% p.a., 6.87% vol) and "Time Series Momentum" (20.7%/15.74%) with unclear periods — [Quantpedia](https://quantpedia.com/an-analysis-of-expected-returns-of-trend-following-strategies/)
- No quantitative alpha-decay data (half-life) for intraday macro signals was found.

---

## 4. What has been discarded or criticised?

### Takeaway
Several "flow" ideas have been empirically discredited or became regime-dependent: (1) RORO as a single-factor trade lost its strength after 2012/13 as correlations fell; (2) the stock-bond hedge (bonds as a risk-off haven) broke in 2022 under inflation; (3) following fund flows (EPFR/mutual-fund/ETF flows) is contrarian over long horizons ("dumb money"), and flows tend to lag prices; (4) business-cycle sector rotation works only with perfect foresight; (5) CTA trigger estimates from bank desks are model-dependent, inconsistent across banks and only available secondhand.

### Cited Findings
**RORO after 2012/13**
- Putnam: in H2 2012, correlations across sectors, countries and individual securities "were easing" after enabling RORO trading — [Putnam](https://www.putnam.com/institutional/content/perspectives/3502)
- Euromoney: correlation across USD currency pairs fell to its lowest level since the Lehman collapse. JPM's John Normand said FX moves were now driven by local rather than global factors — [Euromoney](https://www.euromoney.com/article/27bjsstsqxhkmh0tqp18m/foreign-exchange/currency-managers-rejoice-as-foreign-exchange-correlation-hits-lowest-level-since-lehman-collapse/)
- "Risk on risk off regime heads for the exit" (2013); Liz Ann Sonders expected falling correlations to be a key theme of 2013 — [Markets Media](https://www.marketsmedia.com/risk-on-risk-off-regime-heads-for-the-exit)
- Shane Oliver (AMP, 2013): the relationship of growth assets moving together and inversely to safe-haven bonds was "breaking down" — [AMP Oliver's Insights 2013 (PDF)](https://adviservoice.com.au/wp-content/uploads/2013/05/Risk-on-risk-off-OI-_18-2013.pdf)
- RORO did not disappear entirely: HSBC described G10 FX in the COVID sell-off of 2020 as "simply RORO playing out" — [FXStreet/HSBC (2020)](https://www.fxstreet.com/amp/news/sp-500-and-usd-an-inverse-relationship-hsbc-202006160719). Risk-off spikes cluster in crises (GFC, euro crisis, taper tantrum, COVID) — [KC Fed RWP 24-12](https://www.kansascityfed.org/documents/10594/rwp24-12charistedmanlundblad.pdf)

**Stock-bond hedge 2022**
- In 2022, stock-bond correlation rose to 50-year highs and became positive for the first time in more than 20 years — [PGIM](https://www.pgim.com:443/research/negative-correlation-dead-long-live-6040-portfolio)
- The 60/40 portfolio lost 17.5% in 2022, its worst result since 1937 — [Morgan Stanley IM](https://www.morganstanley.com/im/publication/insights/articles/article_bigpicturereturnofthe6040_A4.pdf)
- State Street (Oct 2025): the shift happened as inflation became the dominant macro variable — [SSGA](https://www.ssga.com/library-content/assets/pdf/global/wmu/2025/mom-20251003.pdf)
- AQR (May 2022, via secondary source): inflation uncertainty is the swing factor for the sign of stock-bond correlation — [Advisor Perspectives](https://www.advisorperspectives.com/articles/2024/06/17/positive-stock-bond-correlations-joseph-burns)
- 2026 example of Treasuries not acting as a haven: in September 2026 the bond sell-off coincided with falling equity indices (all 7 equity contracts down, 30Y bond −1.78% in the week to 11 Sep 2026). CTAs profited from short bond positions — [TTU 11 Sep 2026](https://www.toptradersunplugged.com/trend-following-week-in-review-september-11-2026/); [HedgeCo](https://hedgeco.net/news/?p=92151)

**Following fund flows**
- Frazzini & Lamont (JFE 2008, data 1980–2003): high fund inflows predict low returns at long horizons ("dumb money"). The "smart money" effect is limited to about one quarter — [NBER w11526](https://nber.org/papers/w11526); [AQR](https://www.aqr.com/library/journal-articles/dumb-money-mutual-fund-flows-and-the-crosssection-of-stock-returns)
- An ETF study (FT-reported) found that shorting the ETFs with the highest inflows and buying those with the highest outflows earned excess returns, especially among leveraged ETFs. The paper itself was not reviewed — [Wealth Professional](https://www.wealthprofessional.ca/investments/alternative-investments/are-fools-rushing-into-the-most-popular-etfs/370179)

**Sector rotation over the business cycle**
- Stangl/Jacobsen/Visaltanachoti: with perfect foresight of NBER phases, about +2.3% p.a. (1948–2007). Realistic timing errors and costs largely erase this. Molchanov & Stangl (2023) find "no evidence of systematic sector performance where popular belief anticipates it" — [CXO Advisory](https://www.cxoadvisory.com/economic-indicators/perfect-sector-rotation); [Massey Univ., "The myth of business cycle sector rotation"](https://mro.massey.ac.nz/handle/10179/69590)

**Bank flow and CTA trigger estimates**
- Goldman's CTA trigger and selling figures vary across reports for the same period (e.g., 6,707 vs 6,725 S&P triggers; USD 33bn/80bn vs USD 40bn vs >USD 100bn). Some copies are of questionable origin — [MEXC](https://www.mexc.com/news/666746); [Stockwirex](https://stockwirex.com/?p=26818); [The Wealth Advisor](https://www.thewealthadvisor.com/article/goldman-says-momentum-traders-sell-stocks-every-scenario)
- A June 2026 note on a "CTA selling trigger at USD 4,470" for gold was AI-assisted and cites no Goldman source — [VT Markets](https://www.vtmarkets.com/en-mena/?p=49614)

### Inferences
- A pure "RORO single-factor" model (everything risk-on vs everything risk-off) is fragile because correlations are regime-dependent: high in 2008–2012 and in crises, low in calm phases, and the stock-bond sign flipped in 2022 and again in 2026. The system should estimate rolling correlations and allow for "safe-haven failure" (gold/USD/CHF instead of Treasuries in inflationary risk-off).
- Fund-flow data (EPFR, ETF flows) are useless as intraday triggers. They are published with a lag, they follow prices, and over long horizons they are contrarian.
- Technical "money flow" indicators (MFI, Chaikin MF, OBV) are not found in professional CTA or macro practice.

### Gaps
- No robust academic study on the Money Flow Index (MFI), Chaikin Money Flow or OBV in futures was found within budget, so there is no source for their (lack of) efficacy.
- 2022 performance of risk parity (e.g., Bridgewater All Weather) was not collected.

---

## 5. Retail data and API access (IBKR, CME/Eurex data, crypto, free sources)

### Takeaway
Real-time top-of-book data for CME, CBOT, COMEX and NYMEX costs non-professionals at IBKR only **USD 1.55/month per exchange** (L1), and Eurex Core L1 is free, so data cost is not a bottleneck. The bottlenecks are the API: IBKR streams **250 ms snapshots** (not tick-by-tick) for US/EU futures, a 50 requests/s pacing limit, strict historical-data pacing, weekly re-authentication, and the C# API being officially Windows-only.

### Cited Findings
**IBKR market data prices (non-professional, monthly, as of 11 Oct 2026)**
- CME, CBOT and COMEX Real-Time L1: **USD 1.55 each** (Pro: N/A in this row); L2 USD 12.10; L1+L2 USD 145 (column assignment ambiguous in the HTML table, probably the Pro/combined price). NYMEX is listed in the same way — [IBKR Market Data Pricing](https://www.interactivebrokers.com/en/pricing/market-data-pricing.php)
- "US Securities Snapshot and Futures Value Bundle": USD 10/month, **waived from USD 30 in monthly commissions**, plus USD 0.01 per snapshot. "US Futures Value Bundle PLUS": USD 5 (non-pro) — [IBKR Market Data Pricing](https://www.interactivebrokers.com/en/pricing/market-data-pricing.php). The bundle gives top-of-book for CBOT/CME/COMEX/NYMEX, and the PLUS bundle adds depth (L2) — [IBKR KB](https://ibkb.interactivebrokers.com/fr/node/2840)
- Eurex Core L1: fee waived (non-pro); Eurex Core L2 EUR 13.00 (Pro EUR 67.50); Eurex Retail Europe L1 waived. ICE Futures US (NYBOT) L1+L2 USD 142; CFE Enhanced L1 USD 4.50 (non-pro). Snapshot quotes outside US equities cost USD 0.03 each — [IBKR Market Data Pricing](https://www.interactivebrokers.com/en/pricing/market-data-pricing.php)
- CME and other US data require the annual non-professional questionnaire — [IBKR KB (US market data, non-pro)](https://ibkb.interactivebrokers.com/fr/node/2840)

**IBKR TWS API limits**
- Pacing: maximum requests per second = market data lines / 2. The default is 100 lines, so **50 requests/s**; FIX via IB Gateway allows 250 msg/s — [TWS API: Pacing Limitations](https://www.interactivebrokers.com/docs/tws-api/doc/pacing-limitations/introduction)
- **L1 streaming is snapshot-based: US stocks, futures, bonds and indices every 250 ms; Forex 5 ms; Europe and Asia all products 250 ms** — [TWS API: Market Data Update Frequency](https://www.interactivebrokers.com/docs/tws-api/doc/market-data-live/top-of-book-l-1/market-data-update-frequency)
- Historical data pacing: no identical requests within 15 s, no 6+ requests for the same contract/exchange/tick type within 2 s, **max 60 requests per 10 minutes** (BID_ASK counts double). IBKR says it "is not a specialised market data provider" — [TWS API: Historical Pacing](https://www.interactivebrokers.com/docs/tws-api/doc/market-data-historical/historical-data-limitations/pacing-violations-for-small-bars-30-secs-or-less)
- "The TWS API C# source files are not available through the Mac and Unix distribution" because they are DLL-based. Paper trading uses more simulation than live, so fills can differ — [TWS API Limitations](https://www.interactivebrokers.com/docs/tws-api/doc/notes-limitations/tws-api-limitations)
- Daily: "Never lock Trader Workstation" plus "Auto restart". Weekly re-authentication begins every Monday, and an error message means manual login is needed — [TWS API: Daily & Weekly Reauthentication](https://www.interactivebrokers.com/docs/tws-api/doc/tws-settings/daily-weekly-reauthentication)

**Free and other data**
- Daily and weekly RORO index (Chari et al.) is publicly available and updated monthly — [KC Fed RWP 24-12](https://www.kansascityfed.org/documents/10594/rwp24-12charistedmanlundblad.pdf)
- The QuantConnect data provider is free during live trading and covers US equities, futures, Forex, CFDs, SPX/VIX — [QuantConnect IB docs](https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/interactive-brokers)

**Crypto exchanges (example Kraken, fees as of Oct 2026)**
- Kraken Pro spot, Tier 1 (USD 0+ 30-day volume): maker 0.40% / taker 0.80% (notably higher than earlier Kraken tiers; check before use). Futures Tier 1: maker 0.02% / taker 0.05%. Margin rollover for BTC 0.01–0.02% per 4 h; liquidation fee 2%. EU availability of futures is not stated on the page — [Kraken Fee Schedule](https://www.kraken.com/features/fee-schedule)

### Inferences
- With 250 ms snapshots, "detecting a rotation as it happens" is feasible at minute-to-hour resolution, not sub-second. Lead-lag signals between ES and NQ, ZN, GC and 6J at millisecond scale are not usable with IBKR data, consistent with the Budish ES–SPY evidence.
- For intraday backtesting, IBKR historical pacing (60 requests per 10 min) is too tight to bulk-download years of minute data across many contracts. A dedicated data vendor or QuantConnect data is needed (no costs for third-party vendors were researched).
- Cost per round trip for crypto spot at Kraken (0.80% taker on each leg) is prohibitive for intraday rotation. Futures or perps (5 bps taker) or CME MBT via IBKR are more viable.

### Gaps
- No prices were collected for alternative futures data vendors (Databento, Polygon/Massive, CQG, Rithmic).
- Fees and API limits of other exchanges (Binance, Bybit, Deribit, Coinbase International) and the MiCA rules on perpetuals for EU retail were not researched.

---

## 6. Execution costs, latency, margins, trading hours, weekend gaps

### Takeaway
At IBKR, full-size contracts are cheaper in bps than micros (ES about 0.13 bps commission per round trip vs MBT about 2.2 bps). For intraday rotation the bid-ask spread (1 tick) usually matters more than commission. Retail latency (250 ms data snapshots, ms to tens of ms to the exchange) is 4–5 orders of magnitude slower than Crabel (15 µs). Overnight margin rises before the close, and IBKR liquidates rather than issuing margin calls. Weekend gaps remain for all non-crypto futures. CME crypto has traded 24/7 since 29 May 2026.

### Cited Findings
**IBKR futures commissions (per contract per side, monthly volume ≤1,000; pulled 11 Oct 2026)**
- US standard futures: USD 0.85 (tiers: 0.65 / 0.45 / 0.25 above 1k / 10k / 20k contracts), plus exchange and regulatory fees — [IBKR Commissions Futures](https://www.interactivebrokers.com/en/pricing/commissions-futures.php)
- **ES worked example: USD 0.85 commission + USD 1.38 exchange + USD 0.01 regulatory = USD 2.24 per side.** E7 (E-mini EUR): 0.50 + 0.85 + 0.01 = USD 1.36 — [IBKR](https://www.interactivebrokers.com/en/pricing/commissions-futures.php)
- E-micro (MES, MNQ, M2K, MYM, MCL, MGC, 10Y yield futures, etc.): **USD 0.25** (tiered 0.20 / 0.15 / 0.10), plus exchange fees — [IBKR](https://www.interactivebrokers.com/en/pricing/commissions-futures.php). Micro FX: USD 0.05–0.15 — [IBKR Micro Futures](https://www.interactivebrokers.com/en/trading/micro-futures-comparison.php)
- CME Bitcoin (BTC): **USD 5.00** (tiers down to 2.60). Micro Bitcoin (MBT): **USD 0.85** (down to 0.43). Bitcoin Friday Futures (BFF): USD 0.25. Coinbase Nano BTC/ETH: USD 0.20 — [IBKR](https://www.interactivebrokers.com/en/pricing/commissions-futures.php)
- Eurex (Germany): tiered EUR 0.90 per contract (fixed EUR 2.00, i.e. EUR 4.00 round turn). **FDAX worked example: 0.90 + 1.25 exchange + 0.01 = EUR 2.16 per side. Mini-DAX EUR 0.75; Micro-DAX EUR 0.38** — [IBKR](https://www.interactivebrokers.com/en/pricing/commissions-futures.php)
- The micro products IBKR lists include Micro EUR/USD, AUD/USD and GBP/USD, Micro Gold/Silver/Copper, Micro WTI, Micro 10Y, Micro Ultra T-Bond and yield futures. No Micro JPY is listed — [IBKR Micro Futures](https://www.interactivebrokers.com/en/trading/micro-futures-comparison.php)

**Contract specs and hours**
- MES: tick 0.25 = USD 1.25 (USD 5/point). ES: tick 0.25 = USD 12.50 (USD 50/point). MNQ about USD 2/point (USD 0.50/tick). Trading hours Sunday 17:00 CT to Friday 16:00 CT with a daily 60-minute break (16:00–17:00 CT) — [QuantVPS (updated Oct 2026)](https://www.quantvps.com/blog/mes-tick-value)
- **CME crypto futures and options 24/7 since 29 May 2026** (start Friday 16:00 CT). There is a weekly maintenance window of at least 2 h, and weekend trades get the next business day as trade date. The first weekend saw about 7,200 contracts (about USD 50m notional). 2025 was a record year with USD 3tn notional in crypto derivatives — [Markets Media](https://www.marketsmedia.com/cme-launches-24-7-crypto-futures-options-trading/); [Crowdfund Insider](https://www.crowdfundinsider.com/2026/02/263656-cme-group-to-roll-out-24-7-cryptocurrency-futures-and-options-trading-starting-may-29/); [CME press release PDF (search summary)](https://cmegroupinc.gcs-web.com/node/55391/pdf)

**Margin**
- IBKR has four margin levels: intraday initial and maintenance, and overnight initial and maintenance. "Once the intraday end time approaches … the margin requirement will increase to the overnight maintenance." Cut-off times vary by contract. If the overnight requirement is not met, the position is **force-closed** — [IBKR Campus: TWS Margin for Futures](https://www.interactivebrokers.com/campus/trading-lessons/tws-margin-for-futures/); [IBKR KB](https://ibkb.interactivebrokers.com/de/node/2882)
- A 2014 forum report says IBKR switches to overnight margin about 15 minutes before the regular close (old, possibly outdated) — [NexusFi](https://nexusfi.com/showthread.php?p=390827)
- Published maintenance margins for micros conflict (undated): MES USD 1,460 / MNQ USD 2,220 at AMP; MES USD 2,455 at QuantVPS; MES 2,729/2,481, MNQ 4,062/3,693, MGC 3,399/3,090 at uSMART (columns unlabelled) — [AMP Futures](https://ampfutures.com/trading-info); [QuantVPS](https://www.quantvps.com/blog/mes-tick-value); [uSMART](https://www.usmartsecurities.com/en/help-centre/343/detail/12215)

**Latency**
- Crabel: about 15 µs to the exchange, co-located. IBKR API: 250 ms snapshot intervals for futures data — [HFJ (2019)](https://thehedgefundjournal.com/crabel-contra/); [IBKR API docs](https://www.interactivebrokers.com/docs/tws-api/doc/market-data-live/top-of-book-l-1/market-data-update-frequency)
- VPS vendor claims: Chicago VPS "CME 0.52 ms", New York "NYSE 0–2 ms", London "FX 0–10 ms" (marketing figures) — [QuantVPS](https://www.quantvps.com/blog/mes-tick-value)

### Inferences (worked examples; prices are assumptions, not sourced quotes)
- **ES** at an assumed S&P level of about 6,700 (the order of the Goldman trigger cited in Feb 2026) gives notional of about USD 335k. Commission round trip 2 × 2.24 = USD 4.48, about 0.13 bps. One tick of spread (USD 12.50) is about 0.37 bps, so the total is **≈0.5 bps per round trip** without slippage.
- **MES** has notional of about USD 33.5k. IBKR commission is USD 0.50 per round trip, about 0.15 bps plus CME exchange fees (not sourced). One tick (USD 1.25) is about 0.37 bps, so MES is roughly ES cost plus exchange fee. MES is suitable for 50–250k EUR accounts because of position-sizing granularity.
- **MBT** (0.1 BTC) at BTC ≈ USD 77,330 (11 Sep 2026, TTU) has notional of about USD 7.7k. IBKR commission alone is USD 1.70 per round trip, about **2.2 bps**. **BTC** (5 BTC, about USD 387k): USD 10 per round trip, about 0.26 bps. Micro crypto is 8–9× more expensive in bps than the full contract.
- **FDAX**: EUR 4.32 per round trip all-in (tiered). Micro-DAX EUR 0.76 per round trip.
- **Kraken spot** taker: 0.80% per side, i.e. 160 bps per round trip, unsuitable for intraday. Kraken futures taker: 5 bps per side.
- **JPY/CHF exposure**: with no micro JPY on the IBKR list, the options are full-size 6J, IBKR spot FX (IdealPro, 5 ms snapshots) or CFDs. CHF was not researched.
- 1-day holding periods that cross the close trigger overnight margin. A system that holds through the CME daily break (16:00–17:00 CT) or a weekend must hold full overnight margin and accept gap risk. On weekends, only crypto (CME crypto 24/7 since May 2026, or spot/perps) can react, which makes crypto a weekend risk-sentiment indicator and also a weekend gap risk for the other legs.

### Gaps
- No sourced typical bid-ask spreads (in ticks) or slippage figures for NQ/MNQ, GC/MGC, ZN/ZB, 6J/6E, CL/MCL, FESX were found. Spreads should be measured from your own IBKR data.
- CME exchange fees per micro contract and current official CME/IBKR margin figures were not retrievable (CME and IBKR margin pages load dynamically or block bots).
- No measured retail round-trip latency (VPS → IB Gateway → IBKR server → exchange) is documented.

---

## 7. Infrastructure for a solo C# developer

### Takeaway
A realistic setup: IBKR Pro account; IB Gateway with auto-restart on a Windows VPS (because of the official C# DLL), or LEAN (C#, open source) with the Interactive Brokers brokerage plugin, run either in the cloud (QuantConnect, optionally FIX with no weekly re-login) or locally; a separate data source for backtests; and monitoring for disconnects and re-authentication. Main operational risks: weekly 2FA, only one API session per user, paper-trading fills that differ from live, and API outages.

### Cited Findings
- The TWS API ships official sample projects in Java, VB, C#, C++ and Python — [IBKR TWS API Doc](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/)
- The C# API is officially DLL-based and not in the Mac/Unix distribution — [TWS API Limitations](https://www.interactivebrokers.com/docs/tws-api/doc/notes-limitations/tws-api-limitations)
- IB Gateway and TWS auto-restart (from version 974) can run Sunday to Sunday without re-authentication. Credentials must be re-entered after the weekend server reset. Windows sleep mode disconnects the API — [IBKR: The IB Gateway](https://www.interactivebrokers.com/docs/tws-api/doc/architecture/the-trader-workstation/the-ib-gateway); [IBKR Campus: Third-party connections](https://www.interactivebrokers.com/campus/ibkr-api-page/third-party-connections/)
- QuantConnect/LEAN with IB requires **IBKR Pro (not Lite)** and IB Key 2FA. The **weekly re-authentication notification arrives on Sundays**; if not confirmed, the algorithm stops before market open. Only one connection per IB user is allowed, so a second user is needed for TWS and a subaccount for each additional algorithm. SMS 2FA and third-party authenticators are not supported — [QuantConnect: IB Brokerage](https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/interactive-brokers)
- QuantConnect–IBKR FIX integration "remains up forever, and prevents the need for weekly re-logins," routed over a dedicated VPN. It is not available for paper accounts (DU…) — [QuantConnect](https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/interactive-brokers)
- LEAN supports US Equities, Equity Options, Forex, Futures, Future Options, Indices, Index Options and CFDs with IB. "If you live in the EU, you can't trade US ETFs. You can trade the CFD equivalent." — [QuantConnect](https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/interactive-brokers)
- A newer QuantConnect approach starts 2FA earlier to keep the algorithm online as long as possible (LEAN ≥ v17339, cloud) — [QuantConnect announcement](https://www.quantconnect.com/announcements/19751/new-approach-to-authentication-refresh/); typical error: "IBGateway soft restart timed out" — [QC Forum](https://www.quantconnect.com/forum/discussion/16028/the-ibgateway-soft-restart-timed-out/)
- IBC (IB Controller) automates TWS/Gateway login and restart. Disabling 2FA to automate logins is described as a risky workaround — [IBC User Guide (Scribd copy)](https://www.scribd.com/document/973259048/User-Guide); [MultiCharts forum](https://www.multicharts.com/discussion/viewtopic.php?p=97786); [Elite Trader 2FA thread](https://elitetrader.com/et/threads/2-factor-auth-with-automated-trading.368494/)
- Paper trading at IBKR "relies on more simulated technologies," so execution can differ from live — [TWS API Limitations](https://www.interactivebrokers.com/docs/tws-api/doc/notes-limitations/tws-api-limitations)

### Inferences
- For a C# developer, the most direct route is LEAN (C#) plus the IB brokerage. Local/self-hosted LEAN means handling IB Gateway and 2FA yourself; QuantConnect cloud with FIX avoids the weekly re-login (QuantConnect subscription costs were not researched).
- A home-grown .NET bot with the TWS API should run on a Windows VPS close to IBKR servers, with a watchdog for reconnects, idempotent order management (orderId/permId) and a kill switch (e.g., a daily stop as at Crabel: 2.5%).
- Crypto legs (exchange API) and IBKR futures legs in one system need a common clock and risk layer, and must handle weekends (crypto 24/7, CME 24/7 crypto only, everything else closed).

### Gaps
- No pricing for QuantConnect live nodes or data, and no comparison of other .NET frameworks (e.g., StockSharp, NinjaTrader/NinjaScript C#) or VPS costs.
- The IBKR Client Portal Web API (REST) was not researched in detail (session timeouts, rate limits).

---

## 8. German/EU regulation and tax relevant to strategy design

### Takeaway
Three design rules follow. (1) US ETFs (e.g., QQQ, TLT, GLD) cannot be bought by EU retail clients without a KID (PRIIPs), so use futures, UCITS ETFs or CFDs. (2) The 20,000 EUR loss-offset cap for derivatives (Termingeschäfte, § 20 Abs. 6 S. 5 EStG) was **abolished** by the Jahressteuergesetz 2024 (in force 6 Dec 2024, for all open cases), so futures/CFD losses are again fully offsettable against capital income (25% Abgeltungsteuer + Soli). (3) Crypto spot gains fall under § 23 EStG (1-year holding period, 1,000 EUR exemption limit, losses offsettable only against private sale gains). CFDs are capped at 30:1 to 2:1 leverage for retail and come with negative balance protection.

### Cited Findings
**PRIIPs/KID**
- IBKR: a broker may not let retail clients buy PRIIPs products without a KID, and US ETF issuers generally do not produce KIDs, so EEA/UK retail clients cannot buy them. Workarounds: European UCITS equivalents, **CFDs on large US ETFs** (issued by IBKR's European entities with KIDs), or reclassification as a professional client — [IBKR KB: PRIIPs Overview](https://ibkb.interactivebrokers.com/de/node/3324)
- Individual US stocks are not affected. Options on ETFs may remain available (anecdotal) — [QuantConnect forum](https://www.quantconnect.com/forum/discussion/4153/uk-retail-investors/)

**Tax on derivatives (Termingeschäfte)**
- JStG 2024: the 20,000 EUR cap on Termingeschäft losses (§ 20 Abs. 6 S. 5 EStG, in force since 2021) and the separate loss pool for Termingeschäfte were removed without replacement, along with the cap on losses from bad debts (S. 6). The trigger was the BFH decision of June 2024 (VIII B 113/23, AdV) expressing constitutional doubts. Bundestag 18 Oct 2024, Bundesrat 22 Nov 2024, in force 6 Dec 2024 — [VLH](https://www.vlh.de/kaufen-investieren/geldanlage/verluste-aus-termingeschaeften-das-aendert-sich.html); [GTKP](https://www.gtkp.de/aktuelles/2024-12-11-bundesrat-ermoeglicht-vollstaendige-verlustverrechnung-bei-termingeschaeften-676.html); [Winheller](https://winheller.com/blog/jahressteuergesetz-2024-krypto-anleger/)
- Applies to "all open cases": existing loss carryforwards from Termingeschäfte can be offset without limit against all capital income. Final (bestandskräftig) assessments cannot be reopened — [Ruge Fehsenfeld (26 Nov 2024)](https://www.rugefehsenfeld.de/blog/steuerrecht/aufhebung-des-besonderen-verlustverrechnungskreises-bei-termingeschaeften-und-der-betragsmaessigen-beschraenkung-der-verrechenbarkeit-von-verlusten-aus-forderungsausfaellen-im-privatvermoegen-jahres)
- Sources disagree on how far back it applies: "for 2024 and all open cases" vs "retroactive from 2020". One source says banks must implement it in the withholding-tax procedure only from 1 Jan 2026 — [search summary of VLH/Lohnsteuer-kompakt/Steuernsteuern](https://www.steuernsteuern.de/blog/artikel/verlustverrechnungsbeschraenkung); [Lohnsteuer-kompakt](https://www.lohnsteuer-kompakt.de/steuerwissen/verluste-aus-termingeschaeften-steuererleichterung-fuer-anleger/)
- Futures, options and CFDs are taxed as capital income at 25% Abgeltungsteuer + Soli (+ church tax if applicable) — [Ruge Fehsenfeld](https://www.rugefehsenfeld.de/blog/steuerrecht/aufhebung-des-besonderen-verlustverrechnungskreises-bei-termingeschaeften-und-der-betragsmaessigen-beschraenkung-der-verrechenbarkeit-von-verlusten-aus-forderungsausfaellen-im-privatvermoegen-jahres)

**Crypto (§ 23 EStG)**
- Private sales of "other assets" are taxable if held for 1 year or less (10 years if the asset was used to earn income). Exemption limit (Freigrenze, not an allowance): total annual gain under 1,000 EUR. Losses offset only gains from private sales, with carry-back and carry-forward under § 10d rules — [gesetze-im-internet.de, § 23 EStG](https://www.gesetze-im-internet.de/estg/__23.html)

**CFD/ESMA/BaFin**
- ESMA (2018): leverage caps for retail of 30:1 (major FX pairs) down to 2:1 (crypto); individual equities 5:1. Margin close-out at 50% of minimum margin, negative balance protection per account, standardised risk warning — [ESMA](https://www.esma.europa.eu/node/84933); [ESMA final measures](https://www.esma.europa.eu/es/press-news/esma-news/esma-adopts-final-product-intervention-measures-cfds-and-binary-options); [Mondaq](https://webiis06.mondaq.com/Article/687554); [Finadium](https://finadium.com/?p=79743)
- BaFin: since 8 May 2017, a general order bans selling CFDs with a margin-call obligation (Nachschusspflicht) to retail clients. Unlike ESMA's 3-month measures, it applies indefinitely — [beck-aktuell](https://www.beck-aktuell.de/heute-im-recht/rechtspolitik-gesetzgebung/bafin-verbietet-cfds-mit-nachschusspflicht-im-privatkundengeschaeft-2017-05-09); [Börsen-Zeitung](https://www.boersen-zeitung.de/banken-finanzen/grenze-fur-hebelpapiere-weckt-kritik)
- BaFin planned to adopt the ESMA emergency measures (30:1 FX majors, 5:1 equities, 2:1 crypto) permanently, consulting from late 2018 — [stock3](https://stock3.com/news/bafin-moechte-esma-notfallmassnahmen-fuer-cfds-und-forex-dauerhaft-implementieren-6778671)

### Inferences
- Design consequence: the "risk-off target" legs (Treasuries, gold, Nasdaq short) should be built from **CME/Eurex futures** (ZN/ZB/MGC/MNQ/FDAX etc.) or UCITS ETFs/CFDs, not US ETFs.
- Since the cap was abolished, frequent intraday futures trading with many small losses is no longer a tax-structural problem (gross losses are fully offsettable). The tax environment for derivatives is now neutral for strategy choice.
- Crypto spot with holding periods under 1 year is fully taxable, and losses go into the separate § 23 pool. CME crypto futures (MBT/BTC via IBKR) should, by the derivative logic, count as Termingeschäfte under § 20 (Abgeltungsteuer, offsettable with other capital income). This is an inference and should be checked with a tax adviser.
- CFDs are possible (negative balance protection, leverage caps) but carry spread and financing costs, and the counterparty is the broker. For overnight positions, futures are usually cheaper (CFD financing not researched).

### Gaps
- The exact current text of § 20 Abs. 6 EStG could not be fetched (gesetze-im-internet.de returned HTTP 503). The BGBl reference for JStG 2024 and the application rule (§ 52 EStG) were not verified at primary level.
- No primary BaFin source was found on the current status of the permanent CFD leverage limits (BaFin general order from 2019).
- The BMF letter on crypto taxation (2025) and the tax treatment of crypto perpetuals and crypto CFDs were not researched.
- MiCA/MiFID status of crypto perpetuals for German retail clients (Binance/Bybit/Kraken EU) was not researched.
