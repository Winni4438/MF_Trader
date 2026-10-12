# Time-Series Overbought/Oversold Signals and Short-Term Mean Reversion (holding period ≤ 2 days), cross-asset

Scope: single-asset (time-series) reversal and overbought/oversold signals at 1-hour to 2-day horizons. Relative/pair signals (e.g., "BTC overbought vs gold oversold") are only touched where single-leg evidence bears on them. Research date: October 2026. Many sources are pre-2015; these are marked "[old]", and decay evidence is listed explicitly.

Source-quality legend: **[peer-rev]** journal article; **[WP]** working paper/preprint; **[pract]** practitioner/vendor blog (usually no out-of-sample test); **[snippet]** = only abstract/search snippet seen, numbers not verified in full text.

---

## 1. Indicator-level evidence: RSI / RSI(2), IBS, Bollinger z-score, Williams %R, stochastics, streaks, distance from MA, Connors rules — academic, practitioner, decay

### Takeaway
Rigorous, cost-adjusted academic evidence for named oscillators (RSI, %R, stochastics) at ≤2-day horizons is thin and old. The best-documented "overbought/oversold" effect is Internal Bar Strength (IBS) on **US equity index ETFs**: roughly +0.35% next-day after a close near the low vs −0.13% near the high (1993–2013). It is US-centric, works only on high-volume days, and its post-2013 out-of-sample record is poorly documented. Connors-style RSI(2) with a 200-day filter is a practitioner rule. Its long-run SPY backtests show a high hit rate (~80%) but modest Sharpe (~0.6), and the average hold (~3–4 days) is above the 2-day limit. Evidence points to substantial decay since the 1990s/2000s.

### Cited Findings
**Academic reviews / technical-rule tests [old]**
- Park & Irwin's review of 92 "modern" technical-analysis studies (through Aug 2004) finds 58 positive, 24 negative and 10 mixed. Technical rules "consistently generated economic profits … at least until the early 1990s." Most studies suffer from data snooping, ex-post rule selection and poor cost/risk estimates. Early studies found profits in FX and futures but not stocks before the 1980s. RSI is one of the standard rules tested. — [Park & Irwin 2004, AgMAS report](https://farmdoc.illinois.edu/assets/marketing/agmas/AgMAS04_04.pdf)
- In a data-snooping-corrected test of US futures (1985–2004, $75 round-trip cost per contract), the best technical rules were significantly profitable in only 2 of 17 futures markets. — [Park & Irwin, "Profitability of Technical Trading Rules in US Futures Markets: A Data Snooping Free Test"](https://www.researchgate.net/publication/23517440_The_Profitability_of_Technical_Trading_Rules_in_US_Futures_Markets_A_Data_Snooping_Free_Test) [snippet]
- Technical trading rules earned annual net returns of ~2–10% in major currency futures from the late 1970s to the early 1990s. Trend-following profitability in major currencies eroded around the mid-1990s. — [farmdoc review, via search summary](https://farmdoc.illinois.edu/assets/marketing/agmas/AgMAS04_04.pdf) [snippet; refers to trend rules, not oscillators]

**IBS (Internal Bar Strength = (Close−Low)/(High−Low))**
- Pagonidis (NAAIM 2013/14) [WP, old] covers 30+ US-listed equity index ETFs, 1993–Dec 2013:
  - Next-day close-to-close return is +0.35% when IBS < 0.2 and −0.13% when IBS > 0.8. The top-minus-bottom bucket spread averages 0.476%.
  - SPY: bottom bucket +0.177%, top bucket −0.022%, spread 0.199%. QQQ spread 0.330%, IWM 0.256%.
  - Probability of an up day after bottom vs top bucket, on average: 56.8% vs 46.2%. SPY: 58.2% vs 50.5%.
  - The effect is stronger in high volatility, after large-range days, in bear markets and on Mondays, and by far the weakest on Fridays.
  - For US ETFs it "completely disappears on low volume days". SPY spread on high-volume days is 0.240% vs 0.085% on low-volume days.
  - Returns after low-IBS days have skewness of +0.65.
  - Local (non-US-listed) ETFs mostly show no effect. For the German DAX ETF it is inverted. The author calls it "a U.S.-centric phenomenon."
  - An IBS-only strategy earned ">30% p.a. before trading costs" over 19 years, but "commissions will greatly decrease the returns."
  - Used as a filter on an RSI(3)<10 entry / RSI(3)≤40 hold strategy, IBS ≤ 0.5 cut market days by ~43% and raised total returns by 9.6 percentage points on average.
  - Source: [Pagonidis, "The IBS Effect: Mean Reversion in Equity ETFs"](https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf)
- Pandey & Joshi (2023) find IBS "can be a useful technical indicator" for short-term moves in a basket of country ETFs over 10 years. — [arXiv 2306.12434](https://arxiv.org/abs/2306.12434) [WP, snippet]
- One secondary summary notes stronger past performance and "recent deterioration" for the S&P 500 and Singapore indices. — [ResearchGate listing of "The IBS Effect: Daily Mean Reversion of Equity Indices"](https://www.researchgate.net/publication/256065291_The_IBS_Effect_Daily_Mean_Reversion_of_Equity_Indices) [snippet]

**RSI(2) / ConnorsRSI (practitioner)**
- An independent SPY backtest, Oct 2000–~Sep 2026, follows Connors rules:
  - Rules: price above 200-day MA, RSI(2) < 10 entry, exit at RSI(2) > 70 or after 10 days, no stop.
  - 181 trades (~7/yr), 82% win rate, average hold 3.7 trading days, 10.2% time in market.
  - Sharpe 0.62 vs 0.53 for buy-and-hold. Max drawdown −13.8% vs −55.2%. Ending value $2.49 vs $8.68 per $1.
  - The author calls it "a capital-preservation tool, not a return-maximizer". The out-of-sample/decay split is paywalled.
  - Source: [gurufinanceinsights Substack](https://gurufinanceinsights.substack.com/p/i-backtested-the-classic-rsi2-mean) [pract]
- Reported RSI(2)-on-SPY max drawdowns vary from −13.8% to −33% across vendor backtests, depending on period, costs and filters. — [search summary of QuantifiedStrategies / TraderVPS pages](https://www.quantifiedstrategies.com/rsi2-on-spy/) [pract; vendor pages blocked by bot-check, numbers unverified]
- A forum user's RSI(2) backtest over 1965–1995 showed a 66% win rate but an overall net loss. This suggests the edge is regime/period-specific (strong post-~1997, absent before). — [Trade2Win thread](https://www.trade2win.com/threads/backtest-results-for-connors-rsi2-strategy.242688/) [pract, anecdotal]
- ConnorsRSI decay (Concretum Research) [pract, snippet]:
  - US stocks with CRSI < 5 averaged ~1.5% next-week returns in 1990–2000 vs ~0.3% in 2015–2025 (rolling 10-year windows).
  - The overbought side decayed less. Concretum says CRSI still has "some capacity".
  - Source: [Concretum Research on X](https://x.com/ConcretumR/status/1879572346362593308)
- An early ConnorsRSI test on the Dow 30 with 5-day holds reported 54.7% winners and +0.24% average gain, vs 48.4% winners for standard RSI. The article itself calls the chart a "well-selected example." — [Technical Analysis of Stocks & Commodities](https://technical.traders.com/tradersonline/display.asp?art=7175) [pract, old]
- QuantifiedStrategies claims walk-forward analysis with RSI thresholds of 4–12 confirms the RSI(2) edge is not curve-fit. — [QuantifiedStrategies RSI-2 page](https://www.quantifiedstrategies.com/rsi-2-strategy/) [pract; could not verify, page bot-blocked]

**General post-publication decay**
- Published equity predictors decay substantially after publication, roughly 50–60% in the literature, but not 100%. — [Chen, Lopez-Lira & Zimmermann, arXiv 2212.10317](https://arxiv.org/pdf/2212.10317) [WP, snippet]
- In a 2019 study of mean-reversion portfolio strategies, benchmark datasets favour mean reversion, but the strategies "may fail even in favorable market conditions, especially when there exist explicit or implicit transaction costs." — [arXiv 1909.04327](https://arxiv.org/pdf/1909.04327) [WP, snippet]

### Inferences
- IBS, RSI(2)/(3), Bollinger z-scores, %R and stochastics at 2-day lookbacks are all closely related transforms of "the last 1–3 closes relative to the recent range." Expect them to capture the same underlying effect, namely negative short-lag autocorrelation in **equity indices**, rather than independent edges. Pagonidis's finding that IBS and RSI(3) only partly overlap suggests that combining an intraday-range measure with a multi-day oscillator adds some information.
- The Connors-style evidence relies on hold periods of ~3–4 days on average (exit on RSI>70 or 10-day max). Under a hard 2-day time stop, part of the per-trade edge would be cut off. This must be re-tested rather than assumed.
- The hit rate (~80%) is not the metric to optimise. The Sharpe of ~0.6 at ~10% exposure is what matters, and it is concentrated in one asset class (US equity indices).

### Gaps
- No rigorous, recent (2015–2026), cost-adjusted academic study was found that isolates Williams %R, stochastics, consecutive-down-day streaks or "distance from MA in volatility units" at ≤2-day horizons across asset classes.
- Wong, Manzur & Chew (2003, RSI/MA on Singapore) and Brock, Lakonishok & LeBaron (1992) were not retrieved; only Park & Irwin's review is cited.
- Alvarez Quant Trading, Robot Wealth and Connors Research primary posts could not be retrieved, and QuantifiedStrategies pages were bot-blocked, so their numbers are unverified.
- Price Action Lab's "Mean-Reversion Is Waning" (Sep 2021) is paywalled. A search snippet states the S&P 500 1-lag 252-day autocorrelation turned negative after a late-1997 regime change and that mean reversion "started waning" after Dec 2020. — [Price Action Lab](https://www.priceactionlab.com/Blog/2021/09/mean-reversion-waning/) [snippet only]

---

## 2. Short-term reversal by asset class: equity indices/index futures, government bonds, commodities, FX, crypto

### Takeaway
**Equity indices** are the one asset class with robust, multi-country evidence. Daily/weekly index serial correlation flipped from positive (pre-1990s) to **negative since ~2000**, which the authors link to indexing/ETF arbitrage. A contrarian MAC(5) strategy earned a gross Sharpe of ~0.63–0.67 after 1999. **Treasuries** show mild reversal. **Commodities, FX and crypto** are mostly random walk or **momentum** at daily horizons. Reversals there appear mainly intraday around specific microstructure events (FX fixes), in illiquid small coins, or in contract spreads. **Large-cap crypto (BTC/ETH) shows daily/weekly time-series momentum or random walk, not reliable reversal.**

### Cited Findings
**Equity indices / index futures**
- Baltussen, van Bekkum & Da (JFE 2019) [peer-rev]: Equity indices
  - Across 20 indices in 15 countries, serial dependence was positive until the 1990s and turned negative since the 2000s.
  - Daily AR(1) fluctuated around +0.05 from 1951, declined from the 1980s and switched sign in the 2000s. Weekly AR(1) switched even before 2000.
  - MAC(5) for the S&P 500 was +0.050 before Mar-1999 and −0.141 after. The panel of indices went from +0.054 to −0.062. With a one-day implementation lag the post-1999 panel value is still −0.057.
  - Futures and ETFs on these indices show negative serial dependence "ever since their inception." The panel MAC(5) is −0.047 for futures and −0.054 for ETFs.
  - Trading against MAC(5) across all indices (S&P 500 alone) gives an annualised Sharpe of 0.63 (0.67) after 2 Mar 1999, vs an average index buy-and-hold Sharpe of 0.36. It "requires frequent rebalancing" and "might not be exploitable to many investors after accounting for transaction costs."
  - Mechanism: rising indexing (futures/ETF/index-fund share) and index-arbitrage. Every 1% increase in indexing lowers serial dependence by ~0.031.
  - Source: [Baltussen, van Bekkum & Da, "Indexing and stock market serial dependence around the world"](https://academicweb.nd.edu/~zda/Indexing.pdf)
- Portnaya (arXiv, Jun 2026) [WP; single author, unreviewed, internal inconsistencies, e.g., "21 instruments" vs 25 tickers, "7.4" vs "77" standard errors]:
  - SPY lag-1 daily autocorrelation is −0.081 over 1993–2026, but a sign test is not significant (p=0.11). The paper concludes the predictability is in magnitude, not direction, so a pure "buy after down day" sign rule is "essentially without statistical warrant."
  - SPY VR(2) by period: 0.944 (1993–99), 0.928 (2000–09), 0.959 (2010–19, weakest), 0.851 (2020–present, strongest).
  - QQQ VR(2) = 0.943, IWM 0.933.
  - SPY lag-3 directional edge is ~0.02% per trade, "unlikely exploitable after costs." Institutional round-trip SPY cost is 2–5 bp.
  - Source: [arXiv 2606.29591](https://arxiv.org/html/2606.29591v1)
- The weekly contrarian effect across 7 European equity index futures earned 29.6% annualised in 1993–2002, significant in every region except the US. — [The Idea Farm summary](https://theideafarm.com/alternative-investment/short-term-reversal-in-equity-index-futures/) [snippet, old]
- Overnight→intraday reversal (Della Corte, Kosowski & Wang 2015) [WP, via CXO summary]:
  - US stocks 1993–2014: betting against the overnight (close-to-open) return and holding intraday earns 1.68%/day gross, Sharpe 24 (cross-sectional, ~100% daily turnover). Close-to-close earns 0.33%/day.
  - Results are "generally consistent, though much weaker," across index, interest-rate, commodity and currency futures (1982–2014).
  - The effect is larger after big overnight VIX changes, "especially in futures." A one-minute formation delay "dramatically" reduces returns.
  - Source: [CXOadvisory summary](https://www.cxoadvisory.com/technical-trading/overnightintraday-return-reversal-trading/)
- Intraday index-futures reversals [peer-rev, old]:
  - Grant, Wolf & Yu (JBF 2005): highly significant intraday reversals in US stock index futures, Nov 1987–Sep 2002. Significance is "sharply reduced" after a bid-ask cost proxy. — [Montclair](https://researchwith.montclair.edu/en/publications/intraday-price-reversals-in-the-us-stock-index-futures-market-a-1/)
  - Fung, Mok & Lam (JBF 2000): reversals after large opening moves in S&P 500 and HSI futures, exploitable after costs "even though these may not be very significant." — [HKBU](https://scholars.hkbu.edu.hk/en/publications/intraday-price-reversals-for-index-futures-in-the-us-and-hong-kon/)
  - NASDAQ-100 futures: last night's return is predominantly followed by intraday reversal, while yesterday's return shows both momentum and reversal. — [JOIM](https://joim.com/downloads/nasdaq-100-index-futures-intraday-momentum-reversal)
- A rescaled-range (Hurst) analysis of S&P 500 found it close to a random walk, with mean reversion not strongly established. — [CFA Institute Enterprising Investor 2013](https://blogs.cfainstitute.org/investor/2013/02/18/is-the-sp-500-mean-reverting-rescaled-range-analysis-provides-answers/) [pract, old]

**Government bonds**
- TLT VR(5) = 0.874 and IEF = 0.905 (reversion), but 0/4 fixed-income ETFs reject the random walk at Bonferroni 5%. Credit (LQD, HYG) behaves as a random walk. — [Portnaya, arXiv 2606.29591](https://arxiv.org/html/2606.29591v1) [WP]
- US Treasury note futures show significantly negative intraday serial correlation throughout the day. It has "declined considerably over time." A trading strategy earned excess profits (Banking & Finance Review 2009). — [Penn State listing](https://pure.psu.edu/en/publications/intraday-serial-correlation-and-the-predictability-of-returns-in-/) [snippet, old]
- Lewellen (2022, 1960–2019): daily autocorrelations of stock portfolios and Treasury bonds switched from significantly positive in the first half of the sample. The later sign was not confirmed (snippet truncated; PDF now returns 404). Individual-stock daily autocorrelations became less negative recently. — [Lewellen, Tuck](https://faculty.tuck.dartmouth.edu/images/uploads/faculty/jonathan-lewellen/Autocorrelations.pdf) [snippet]

**Commodities**
- Wang [peer-rev, old] studied 24 US futures (4 currency, 5 financial, 8 agricultural, 7 other commodities), 1983–2000:
  - Weekly reversal: long losers / short winners, restricted to high-volume, low-open-interest contracts, earned 0.57%/week (~29.6% p.a. arithmetic), Sharpe ~0.82, gross.
  - The basic strategy stays profitable up to ~0.10% one-way cost and is wiped out at ~0.16%.
  - Quantpedia notes reversal is effectively short volatility.
  - Source: [Quantpedia: Short Term Reversal with Futures](https://quantpedia.com/strategies/short-term-reversal-with-futures)
- GLD, SLV and DBC behave as random walks at daily horizons, and USO shows mild momentum (VR(5)=1.040). — [Portnaya, arXiv 2606.29591](https://arxiv.org/html/2606.29591v1) [WP]
- Across 1800–2018 and multiple asset classes including commodities and currencies, there is "no evidence of short-run reversal," only strong short-term momentum, at the monthly horizon. — [Short-term momentum (almost) everywhere, ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1042443119300976) [peer-rev; monthly horizon, contrast only]
- Chinese commodity futures and options show significant intraday reversal effects (2024). — [Pacific-Basin Finance Journal, ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0927538X24002865) [snippet]
- The F1–F2 calendar-spread return reverses weekly. A long-short version across global commodity and equity-index futures, 2007–2025, reported 9.68% p.a., Sharpe 0.92, max drawdown ~−17%, with no costs and no out-of-sample test. — [QuantReturns Substack, adapted from Rossi, Zhang & Zhu 2025](https://quantreturns.substack.com/p/when-futures-overreact-a-weekly-edge) [pract; spread effect, not outright-price reversal]

**FX**
- UUP and FXY show weak reversal and FXE a random walk at daily horizons. 0/3 FX ETFs reject the random walk. — [Portnaya, arXiv 2606.29591](https://arxiv.org/html/2606.29591v1) [WP]
- Krohn, Mueller & Whelan (JF 2024) [peer-rev]: G9 currencies 1999–2019. The USD systematically appreciates before the Tokyo, ECB and London fixes and depreciates thereafter. Reversals are "pervasive" and larger in high-volatility periods. The authors attribute this to dealer hedging of fix demand. — [Journal of Finance](https://onlinelibrary.wiley.com/doi/10.1111/jofi.13306); [Bank of Canada SWP 2021-48](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)
- Krohn, Mueller & Whelan, "FX Premia Around the Clock" [WP]: carry returns are earned intraday, while FX momentum strategies are most profitable overnight. Long-all-foreign-currency returns <1% p.a. close-to-close, versus ~+5% intraday and ~−4% overnight. — [WP 2018 PDF](https://acfr.aut.ac.nz/__data/assets/pdf_file/0007/190753/Krohn_Mueller_Whelan_Jun2018_FXPremiaAroundTheClock.pdf)
- A broker blog reports that fading 3-day USD streaks (1% streak filter, fixed stop/target, 6-year sample) beat momentum entries. — [tastyfx](https://www.tastyfx.com/news/fading-multi-day-dollar-moves-a-quantitative-case-for-mean-reversion/) [pract, weak]

**Crypto**
- Liu & Tsyvinski (NBER w24877 / RFS 2021) [peer-rev], BTC 2011–2018:
  - Daily: BTC mean return 0.52%, SD 5.55%.
  - Today's return positively predicts the next day's return (coefficient 0.06, t=2.96, but robust t=1.22). A 1-SD move implies +0.33% the next day. The 5- and 6-day-ahead coefficients are also positive and significant.
  - Weekly momentum is strong (coefficients 0.19–0.22 for weeks 1–3). The top-quintile weekly formation return is followed by +11.2% next week vs +2.6% for the bottom quintile.
  - Source: [Liu & Tsyvinski, NBER WP](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf)
- Caporale & Plastun [peer-rev / WP]:
  - BTC, LTC, XRP, DASH: after daily "overreactions", counter-movement (contrarian) strategies are **not profitable**. Inertia (momentum) strategies appear profitable but are not statistically different from random. — [CESifo WP 6861 / J. Econ. Studies 2019](https://cesifo.org/DocDL/cesifo1_wp6861.pdf) [snippet]
  - Hourly BTC/ETH/LTC 2017–2019: prices continue in the direction of the overreaction until day-end and the next day (momentum). Contrarian effects appear only for BTC positive and ETH negative overreactions. — [Brunel WP 1917](https://www.brunel.ac.uk/economics-finance-and-accounting/research/pdf/1917-Oct-GMC-Momentum-effect-in-the-Cryptocurrency-Market-after-One-day-Abnormal-Returns.pdf) [snippet]
- Wen, Bouri, Xu & Zhao (NAJEF 2022): high-frequency BTC, Mar 2013–May 2020, with similar patterns in ETH, LTC and XRP.
  - Both intraday momentum and intraday reversal exist. The half-hour tests found 12 momentum pairs vs 21 reversal pairs.
  - Patterns shift around large jumps, FOMC, liquidity conditions and COVID.
  - A timing strategy beat buy-and-hold, but no magnitudes were visible.
  - Sources: [IDEAS](https://ideas.repec.org/a/eee/ecofin/v62y2022ics1062940822000833.html); [ResearchGate](https://www.researchgate.net/publication/361202793_Intraday_return_predictability_in_the_cryptocurrency_markets_momentum_reversal_or_both) [snippet]
- Shen et al.: Bitcoin intraday time-series momentum. The first half-hour return predicts the last half-hour, strongest with high early volume or volatility. — [Reading repository](https://centaur.reading.ac.uk/100181/3/21Sep2021Bitcoin%20Intraday%20Time-Series%20Momentum.R2.pdf) [peer-rev, snippet]
- Wu & Pinsky (JRFM 2026): hourly Kraken data 2016–2025, day split into 12-hour sessions. BTC shows reversal in both sessions under an 08:00 UTC cutoff. ETH shows overnight drift plus daytime reversal. — [JRFM 19(9):692](https://doi.org/10.3390/jrfm19090692) [peer-rev, snippet only; full text 403, no numbers verified]
- Cross-sectional crypto reversal is concentrated in illiquid coins:
  - Across >3,600 coins, low prior-day-return coins outperform. This is attributed to illiquidity, and "the handful of largest coins exhibit daily momentum rather than reversal." — [Uni Stuttgart PUMA listing (likely Zaremba et al. 2021, "Up or down?", IRFA; attribution unverified)](https://puma.ub.uni-stuttgart.de/bibtex/25f0fef0802289c77953bdf3b8597196) [snippet]
  - Kozlowski, Puleo & Zhou: 200 coins 2015–2019, reversal at daily, weekly and monthly horizons, strongest in small and illiquid coins. — [Fairfield](https://fairfield.elsevierpure.com/en/publications/cryptocurrency-return-reversals/) [snippet]
  - Short-term reversal returns proxy liquidity provision and are larger in less active, smaller, more volatile pairs (Mar 2017–Mar 2022). — [Riksbank WP 413](https://www.riksbank.se/globalassets/media/rapporter/working-papers/2022/no.-413-trading-volume-and-liquidity-provision-in-cryptocurreny-markets.pdf)
  - Dobrynskaya: results vary widely by ranking/holding period, and the literature finds momentum, no effect or reversal depending on sample. — [HSE](https://spb.hse.ru/en/news/559533243.html) [snippet]
- BTC and ETH are "the closest to a pure random walk" among the instruments tested, at all horizons. — [Portnaya, arXiv 2606.29591](https://arxiv.org/html/2606.29591v1) [WP]
- Hudson & Urquhart tested ~15,000 rules on cryptocurrencies. They find significant predictability after data-snooping corrections, but "no predictability for Bitcoin in the out-of-sample period." — [Hudson & Urquhart, Annals of OR](https://reading-clone.eprints-hosting.org/85715) [peer-rev, snippet]
- QuantifiedStrategies concludes classic buy-the-dip / sell-strength mean reversion "doesn't work on Bitcoin," with momentum variants doing better. — [QuantifiedStrategies Bitcoin RSI](https://www.quantifiedstrategies.com/bitcoin-rsi-trading-strategy/) [pract]

### Inferences
- The proposed "BTC overbought → short; gold oversold → long" trade has two legs that, as single assets, show **no reliable daily time-series reversal**. BTC shows daily/weekly momentum or a random walk, and GLD a random walk (VR(2)=0.988, z=−0.68 in Portnaya). Any edge would have to come from the *relative* spread mean-reverting, which is a different claim requiring separate evidence (covered by other notes).
- The most promising single-asset venues for ≤2-day oversold buying are **liquid equity index futures** (ES/NQ/RTY, possibly Euro/Asian index futures) and, more weakly, **Treasury futures**. The economic driver is index-arbitrage and liquidity-provision bounce, not "overheating" in a behavioural sense.
- In crypto, contrarian signals are more plausible intraday or in small/illiquid alts. Those carry higher costs, liquidity risk and exchange risk, which conflicts with the reliability goal.

### Gaps
- No full-text numbers were obtained for Wu & Pinsky 2026, Wen et al. 2022, or the commodity short-horizon paper by Zhao, Ding, Yu & Kang (SSRN 6425598, 403 on fetch).
- No dedicated daily-horizon study of single-pair G10 FX time-series reversal after large moves was found.
- No study specifically on Bund/Bobl or other non-US government bond futures daily reversal was found.
- No rigorous study of crypto perp-specific signals was found: funding extremes, liquidation cascades, or post-liquidation returns with out-of-sample tests.

---

## 3. Conditions: volatility/liquidity stress, VIX regime, with vs against trend, news vs no-news, weekday/month-end

### Takeaway
Reversal returns are **strongly state-dependent**. They rise with VIX and liquidity stress (Nagel), after large-range/high-volume days, and after no-news moves. They weaken after news-driven moves, which tend to drift. For directional (non-hedged) dip-buying, the same high-volatility states are also when trend-following crashes occur. Trend filters (e.g., price above the 200-day MA) reduce drawdowns at the cost of skipping the highest-expected-return stress episodes.

### Cited Findings
- Nagel (RFS 2012) [peer-rev], cross-sectional reversal as a proxy for liquidity provision:
  - Sample: CRSP stocks, Jan 1998–Dec 2010.
  - A 5-day stock-reversal strategy earned 0.30%/day gross (transaction prices), annualised Sharpe 8.44. On quote-midpoints it earned 0.18%/day (Sharpe 4.50). Industry-portfolio reversal earned only 0.02%/day (Sharpe 0.56).
  - Returns were near 1%/day in the 1998 LTCM crisis and 2000/01. They declined steadily to <0.2%/day by 2007, then "exploded" in 2008.
  - VIX predicts reversal returns. +1 point in normalised VIX (≈16 points annualised) adds +0.22 percentage points per day for stock reversal and +0.07 for industry reversal (adj. R² 0.07). At VIX ~60, the fitted industry-reversal return is ~0.20%/day.
  - Conditional Sharpe also rises with VIX.
  - Source: [Nagel, "Evaporating Liquidity", NBER WP 17653](https://www.nber.org/papers/w17653.pdf)
- A later large-stock replication finds that +1 VIX point raises the next-5-day reversal return by 5.37 bp, confirming Nagel. — [Quantpedia summary](https://vvv.quantpedia.com/es/wp-json/wp/v2/posts/808) [pract summary, snippet]
- The IBS effect is stronger in high-volatility regimes, after large-range days, after high-volume days (US) and in bear markets. Long-side returns are greater in bear markets. It is strongest on Mondays ("Turnaround Tuesday") and weakest on Fridays. — [Pagonidis](https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf)
- After 2008, much of the IBS effect in international ETFs depends on SPY's IBS. If SPY IBS is low, shorting a high-IBS international ETF does not work, and vice versa. — [Pagonidis](https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf)
- The overnight-to-intraday reversal is larger when the overnight VIX change is larger, especially in futures. — [CXO on Della Corte et al.](https://www.cxoadvisory.com/technical-trading/overnightintraday-return-reversal-trading/)
- FX fix-related reversals are larger in high-volatility periods. — [Krohn et al., JF 2024](https://onlinelibrary.wiley.com/doi/10.1111/jofi.13306)
- News vs no-news:
  - Chan (JFE 2003): strong drift after bad news, and reversal after extreme moves without public news, mainly in smaller, illiquid stocks. — [Chan 2003 summary](https://academicnewsletter.sufe.edu.cn/info/357702) [peer-rev, old]
  - Savor (JFE 2012): price shocks accompanied by information (analyst reports) drift, while no-information shocks reverse. — [Savor 2012, UPenn repository](https://repository.upenn.edu/fnce_papers/387) [peer-rev]
- Crypto intraday predictability shifts with large jumps, FOMC releases, liquidity and COVID. — [Wen et al. 2022](https://ideas.repec.org/a/eee/ecofin/v62y2022ics1062940822000833.html)
- With vs against trend:
  - The RSI(2) 200-day-filter SPY backtest had a max drawdown of −13.8% largely because the filter kept it out of the 2008 and 2020 crashes. — [gurufinanceinsights](https://gurufinanceinsights.substack.com/p/i-backtested-the-classic-rsi2-mean) [pract]
  - Crypto naked mean reversion (BTC/ETH spot, RSI(2), Bollinger, distance-from-MA) averaged +16.3% in bull, −2.2% in sideways and −40.6% in bear regimes. Regimes were labelled in hindsight. — [CoinQuant 78 backtests](https://www.coinquant.ai/blog/building-a-mean-reversion-strategy-in-cryptocurrency-markets-evidence-from-78-backtests) [pract]
- Index serial dependence is linked to indexing even after controlling for volatility, TED spread and past returns. — [Baltussen et al.](https://academicweb.nd.edu/~zda/Indexing.pdf)

### Inferences
- There is a tension between the two condition findings. Liquidity-provision returns are highest when VIX spikes (Nagel; Pagonidis's bear-market finding). Directional dip-buying with a trend filter avoids exactly those periods. A plausible design is to condition position size on volatility (e.g., trade only when realised or implied vol is elevated, but scale notional by 1/vol) rather than block all below-200-day signals. This needs testing.
- "Fading panics" (the user's promising prior result) is consistent with Nagel's liquidity-provision story and with the no-news reversal literature. A practical proxy for "no news" is the absence of a scheduled macro release (FOMC/CPI/NFP) in the move window. Moves on news days are more likely to drift.
- Monday/weekend: IBS evidence favours entries Friday close → Monday, and the weakest edge is Friday. Crypto trades over weekends, so equity-market weekend gaps do not translate directly.

### Gaps
- No direct evidence was found on month-end effects for short-term reversal at index level.
- No study was found that splits single-asset index-futures reversal returns by VIX regime after 2015.
- Nagel's evidence is cross-sectional and market-neutral. Its transfer to single-asset directional trades is an inference.

---

## 4. Edge per trade vs realistic costs; surviving Sharpe ratios; where the effect has decayed

### Takeaway
Gross edges for the best-documented index signals are about 10–40 bp per trade (IBS bottom bucket, older samples), and daily index autocorrelation trades have a gross Sharpe of ~0.6. For a retail account trading **index futures**, round-trip costs (~0.5–1.5 bp incl. one tick) are small relative to this, so costs are not the binding constraint for index futures. Decay, regime dependence and execution timing (signal at the close) are the binding constraints. In **crypto perps** (≈4–10 bp round trip in fees alone, plus funding) and **CFDs** (wider spreads), costs consume much of the small daily edges. Decay is documented for stock-level reversal (to 2007), ConnorsRSI on stocks (1990s → 2015–25), Treasury-note intraday reversal, and BTC technical predictability (no OOS predictability). Index-level negative autocorrelation emerged only after ~2000. It was weaker in 2010–19 and stronger again in 2020–26 (VR).

### Cited Findings
**Gross edges**
- IBS on US equity ETFs: bottom-bucket next-day return +0.35% on average, +0.177% for SPY. The bottom-minus-top spread is 0.476% on average and 0.199% for SPY (1993–2013). — [Pagonidis](https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf)
- RSI(3)+IBS filter: average daily return in market of 0.293% across ETFs (SPY 0.297%, QQQ 0.460%), versus 0.159% unfiltered. — [Pagonidis, Table 15](https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf)
- Index MAC(5) contrarian strategy: annualised Sharpe of 0.63 across all indices and 0.67 for the S&P 500, post-1999, gross. — [Baltussen et al.](https://academicweb.nd.edu/~zda/Indexing.pdf)
- SPY daily contrarian: pre-cost Sharpe ~1.3 implied by the lag-1 autocorrelation, but direction-only edge ~0.02%/trade. Institutional round-trip cost is 2–5 bp. — [Portnaya, arXiv 2606.29591](https://arxiv.org/html/2606.29591v1) [WP]
- Weekly futures reversal (1983–2000): 0.57%/week gross for the selected version. The basic strategy breaks even at ~0.16% one-way cost. — [Quantpedia/Wang](https://quantpedia.com/strategies/short-term-reversal-with-futures)
- Stock-level reversal of 0.30%/day gross is not achievable by a retail trader. After fixed costs of technology and market access, "Sharpe ratios would likely be much less extreme." — [Nagel](https://www.nber.org/papers/w17653.pdf)

**Costs (current broker schedules)**
- IBKR US futures, ES example: IBKR fee USD 0.85 + exchange fee 1.38 + regulatory fee 0.02 = USD 2.25 per contract per side. — [IBKR futures commissions](https://interactivebrokers.ca/en/pricing/commissions-futures.php) [snippet]
- IBKR spot FX (IDEALPRO): 0.20 bp of trade value, minimum ~USD 2–2.50 per order. Tiers go down to 0.08 bp at very high volume. — [IBKR FX commissions PDF](https://www.interactivebrokers.com/download/newMark/PDFs/commissionsForex.pdf); [NerdWallet](https://www.nerdwallet.com/p/best/investing/forex-brokers)
- Binance USDⓈ-M perps, regular user: 0.02% maker / 0.05% taker on notional, with a 10% discount when fees are paid in BNB. — [Binance support](https://www.binance.com/fr/support/articles/360033544231)
- Intraday index-futures reversals lose most of their significance after a bid-ask cost proxy. — [Grant, Wolf & Yu 2005](https://researchwith.montclair.edu/en/publications/intraday-price-reversals-in-the-us-stock-index-futures-market-a-1/)
- Overnight-intraday reversal strategies have ~100% daily turnover, and costs "would dramatically reduce reported performance." — [CXO / Della Corte et al.](https://www.cxoadvisory.com/technical-trading/overnightintraday-return-reversal-trading/)
- In a crypto mean-reversion backtest, one 15-minute Bollinger variant paid >USD 2,300 in fees on a USD 10,000 account over 693 trades. Average returns were negative on every timeframe: 15m −14.4%, 1h −8.1%, 4h −9.5%, 1d −4.0%. — [CoinQuant](https://www.coinquant.ai/blog/building-a-mean-reversion-strategy-in-cryptocurrency-markets-evidence-from-78-backtests) [pract]

**Decay / sign changes**
- Index serial correlation was positive pre-1990s and negative post-2000 in most of 20 indices. The break date correlates with futures introduction. — [Baltussen et al.](https://academicweb.nd.edu/~zda/Indexing.pdf)
- SPY VR(2): 0.944 (1993–99), 0.928 (2000–09), 0.959 (2010–19, weakest reversal), 0.851 (2020–26, strongest). — [Portnaya](https://arxiv.org/html/2606.29591v1) [WP]
- The S&P 500 252-day lag-1 autocorrelation has been mostly negative since late 1997, very negative in the 2020 crash, and "waning" after Dec 2020. — [Price Action Lab](https://www.priceactionlab.com/Blog/2021/09/mean-reversion-waning/) [snippet; paywalled]
- Stock-reversal returns declined from ~1%/day (1998–2001) to <0.2%/day (2007), then spiked in the 2008 crisis. — [Nagel](https://www.nber.org/papers/w17653.pdf)
- ConnorsRSI (<5) next-week return fell from ~1.5% (1990–2000) to ~0.3% (2015–2025). — [Concretum on X](https://x.com/ConcretumR/status/1879572346362593308) [snippet]
- Treasury-note futures intraday negative correlation "declined considerably over time." — [Penn State listing](https://pure.psu.edu/en/publications/intraday-serial-correlation-and-the-predictability-of-returns-in-/) [snippet]
- There is no Bitcoin technical-rule predictability out of sample. — [Hudson & Urquhart](https://reading-clone.eprints-hosting.org/85715) [snippet]
- An Erasmus thesis on 5-minute BTC finds profitability that is "highly unstable and declines over time." — [Erasmus thesis](https://thesis.eur.nl/pub/41546/Bakker.pdf) [snippet]
- The IBS effect is absent or inverted in local European index ETFs, including the DAX ETF. — [Pagonidis](https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf)

### Inferences
- Cost arithmetic, my calculation:
  - Assumptions: S&P 500 around 6,000–7,000 (not sourced), so one ES contract (multiplier $50) is ≈ USD 300–350k notional. One tick is 0.25 points = $12.50 (standard CME spec, not separately sourced here).
  - USD 4.50 round-trip commission ≈ 0.13–0.15 bp. Crossing one tick once ≈ 0.4 bp. Realistic all-in is ≈ 0.5–1.5 bp per round trip.
  - Against a 10–20 bp gross edge, costs are small for index futures.
  - Crypto perps at taker/taker: 10 bp round trip plus funding; at maker/maker, 4 bp. This is comparable to or larger than the documented daily directional edges for BTC/ETH, which are near zero or momentum.
- Contract granularity matters for a 50–250k EUR account. One ES contract is ~1.3–6.5× account equity, so micro contracts (MES/MNQ/M2K) or CFDs would be needed. CFDs carry wider spreads and financing that would need checking per broker.
- A realistic net Sharpe for a single-asset ≤2-day index mean-reversion strategy is likely in the ~0.3–0.7 range. This rests on the gross index Sharpe of 0.6–0.7 (Baltussen) and the practitioner RSI(2) Sharpe of 0.62 (with ~10% exposure). Diversifying across several index futures (US, EU, Asia) is the main lever to raise it. The negative-serial-dependence effect is pervasive across 20 indices, but correlations between indices limit the gain.

### Gaps
- No credible post-2015 net-of-cost backtest of a ≤2-day index-futures mean-reversion rule with an explicit out-of-sample period was found.
- Per-trade bps for IBS/RSI(2) after 2013 could not be verified from primary sources.
- Typical spreads for EUR/USD and index CFDs at German retail brokers were not sourced.

---

## 5. Regime risk: catastrophic failures (2008, Mar-2020, crypto 2022, LUNA/FTX) and risk controls (time stops, vol filters, stop-losses)

### Takeaway
Market-neutral liquidity-provision reversal historically *profited* in crises: it had no losing 3-month period in 1998–2010, with August 2007 as the exception. Directional oversold buying in a single asset is different. It suffers in trending crashes (e.g., crypto 2022, where naked BTC/ETH mean reversion averaged −40% in bear regimes) and in correlation breakdowns (COVID 2020). The practitioner consensus, backed by a few explicit tests, is that **fixed tight stop-losses hurt** mean-reversion strategies (lower return, sometimes deeper drawdowns). The usual alternatives are **time stops**, **regime/trend filters**, **volatility-scaled sizing** and limiting position size.

### Cited Findings
- Nagel's market-neutral 5-day stock-reversal strategy had no losing 3-month period in 1998–2010 (gross), positive skew (3.02), and a worst day of −3.88%. The August 2007 quant crisis (Khandani & Lo) produced "substantial but largely transitory losses over a period of a few days." — [Nagel](https://www.nber.org/papers/w17653.pdf)
- During the COVID selloff, close-to-close mean-reversion strategies took large drawdowns as correlations broke down. They "reactively got loaded (doubled-down) more and more on losing trades anticipating a snap-back." — [Quant Bust 2020, arXiv 2006.05632](https://arxiv.org/pdf/2006.05632) [WP, snippet]
- Crypto 2022 bear market [pract; small samples]:
  - BTC daily Bollinger(20,2) long-only, exit at the mid-band: −38.9% (6 trades, 33% win rate). ETH: −39.3%.
  - Naked crypto mean reversion averaged −40.6% in bear regimes, and the best bull configuration (distance-from-MA) averaged −45% in bears.
  - 14 of 78 cells had win rates ≥65% and still lost money.
  - Source: [CoinQuant](https://www.coinquant.ai/blog/building-a-mean-reversion-strategy-in-cryptocurrency-markets-evidence-from-78-backtests)
- Oversold signals on BTC are close to a coin flip. Of 26 days with RSI<30 in a 705-day sample, only 12 were higher after 14 days, with a mean change of about −0.2%. Overbought days were more often followed by higher prices. — [cryptoticker.io](https://cryptoticker.io/en/bitcoin-rsi-explained/) [pract, small sample]
- Reversal strategies are effectively short volatility and "can suffer during high-volatility market stress." — [Quantpedia, Short Term Reversal with Futures](https://quantpedia.com/strategies/short-term-reversal-with-futures)
- The trend filter (price above the 200-day MA) kept an RSI(2) SPY strategy out of the 2008 and 2020 crashes. Max drawdown was −13.8% vs −55.2% for buy-and-hold. — [gurufinanceinsights](https://gurufinanceinsights.substack.com/p/i-backtested-the-classic-rsi2-mean) [pract]
- Stop-loss tests:
  - In a RealTest backtest where the stop was the only change, adding a 5% stop to a mean-reversion system cut annual return from ~8.2% to ~1%. Worst drawdown deepened from ~−19% to ~−42%, and win rate and profit factor fell. The result held under doubled costs and a one-bar delay. — [setup4alpha Substack](https://setup4alpha.substack.com/p/stop-loss-mean-reversion-backtest) [pract]
  - QuantifiedStrategies: "in almost all" its backtests, stops fail to add value for mean-reversion strategies, because the signal strengthens as price moves against the position. — [QuantifiedStrategies](https://www.quantifiedstrategies.com/mean-reversion-trading-strategy/) [pract]
  - Cesar Alvarez, ex-Connors Research, reportedly found mean-reversion strategies performed best without stops. He rotates live strategies based on recent performance. — [Algorithmic Advantage podcast summary](https://thealgorithmicadvantage.substack.com/p/episode-045-cesar-alvarez-a-novel) [pract]
  - In a stat-arb strategy, both tighter (1%, 3%) and looser (10%) stops moderately hurt returns versus the base case, though a 3% stop reduced max drawdown. — [arXiv 2406.10695](https://arxiv.org/pdf/2406.10695) [WP]
  - Counter-view: some guides recommend always using stops (testing 3/5/7%) because of "falling knife" trend risk, but provide no evidence. — [BacktestMe](https://backtestme.com/guides/mean-reversion-strategies) [pract]
- Next-day returns after low-IBS days are positively skewed (+0.65), versus +0.03 after high-IBS days. Losses on long oversold entries are thus on average less tail-heavy than gains. — [Pagonidis](https://www.naaim.org/wp-content/uploads/2014/04/00V_Alexander_Pagonidis_The-IBS-Effect-Mean-Reversion-in-Equity-ETFs-1.pdf)
- BTC has extreme daily tails. The probability of a −20% day is ≈0.5% and of a +20% day ≈1% (2011–2018), with daily kurtosis of 15.2. — [Liu & Tsyvinski](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf)

### Inferences
- For a ≤2-day horizon, the natural risk control is the **time stop** (exit after N bars, e.g., 1–2 days). It caps exposure to a trending crash without the "stop out at the worst point" problem of price stops. Combine it with **volatility-scaled sizing** (smaller notional when realised vol is high) and a **portfolio-level daily loss limit / kill switch** for crypto and exchange-event risk (LUNA/FTX-type events are also counterparty and exchange risks, not just price risk).
- Doubling down / adding to losers is the main failure mode documented in 2020. A fully automated system should forbid pyramiding into the same oversold signal, or cap aggregate exposure across correlated assets. All equity indices give oversold signals at the same time in a crash.
- Trend filters cut drawdowns in equity indices but remove the highest-expected-return stress episodes (Nagel, Pagonidis bear-market result). A compromise to test: allow below-200-day entries only with reduced size and a 1-day time stop.

### Gaps
- No primary-source year-by-year P&L was found for RSI(2)/IBS index strategies in 2008, Feb–Mar 2020 or 2022.
- No systematic study was found of contrarian/oversold signals around the LUNA (May 2022) or FTX (Nov 2022) collapses.
- No academic test was found that compares time stops vs price stops vs vol filters specifically for ≤2-day single-asset reversal.
