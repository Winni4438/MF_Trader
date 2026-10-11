# Academic and Empirical Evidence: Is Trading Cross-Asset Capital Rotations (Momentum / Flight-to-Safety / Risk-On-Risk-Off) Profitable? (Intraday focus, daily/weekly reference)

Research date: 2026-10-11. Tag convention: **[DECAY]** = out-of-sample / post-publication weakening or failure; **[COST]** = transaction-cost evidence; **[SECONDARY]** = number taken from a summary/commentary, not the primary paper.

---

## 1. Intraday momentum and continuation (Gao et al. 2018; Baltussen et al. 2021; futures across asset classes; crypto); does it survive costs?

### Takeaway
The best-documented intraday effect is continuation into the close: the market's return up to ~30 min before the close predicts the last 30 minutes in equity-index, bond, commodity and (historically) FX futures (gross Sharpe 0.87–1.73 by asset class, 1974–2020). The edge per trade is only a few basis points. It survives tight futures/ETF costs for liquid equity index products. It partly reverses over the next 1–3 days, and it has weakened or vanished in FX since 2000.

### Cited Findings
**Gao, Han, Li & Zhou ("Market intraday momentum", JFE 2018; numbers from the Dec-2015 working-paper version)**
- Sample: SPY, 1993–2013. The first half-hour return (previous close to 10:00 ET) predicts the last half-hour return. In-sample slope significant at 1%, R² = 1.6%. Adding the 12th half-hour raises R² to 2.6%. Out-of-sample R² is 1.2% (first half-hour alone), 0.7% (12th half-hour alone) and 1.8% (both) — [Gao et al. WP PDF](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf); published as [JFE 129(2):394–414](https://ideas.repec.org/a/eee/jfinec/v129y2018i2p394-414.html)
- Timing strategy (long or short SPY in the last half-hour according to the sign of the first half-hour): 6.67% p.a., SD 6.19%, Sharpe 1.08. "Always long last half-hour" earned −1.11% p.a. (Sharpe −0.18). Buy-and-hold earned 6.04% p.a. (SD 20.57%, Sharpe 0.29). The strategy is in the market only 30 minutes per day — [Gao et al. WP](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- Predictability is stronger on high-volatility days, high-volume days, recession days and major macro-news days. It is also present in 10 other heavily traded ETFs and 2 international index futures. Out-of-sample gains are often larger in the less liquid ETFs — [Gao et al. WP](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- **[COST]** After decimalization (July 2001 onward), costs cut the r1 strategy's return to 4.46% p.a. (−2.47 pp). From 2005, with SPY proportional spreads stable around 1.2 bp, the return is 6.52% after costs vs. 7.96% before. Commissions are ignored, and the 16:00 close is assumed executable at the closing auction price without a spread — [Gao et al. WP](https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf)
- [SECONDARY] CXO Advisory's out-of-sample replication on SPY (1999–2012): out-of-sample R² 0.018. Holding SPY in the last half-hour only when the first half-hour is positive returned 6.3%/yr vs. −0.5% gross — [CXO Advisory](https://cxoadvisory.com/calendar-effects/first-and-last-half-hours-of-trading-linked)

**Baltussen, Da, Lammers & Martens ("Hedging demand and market intraday momentum", JFE 142, 2021)**
- Sample: 62 futures (17 equity index, 16 government bond, 21 commodity, 8 currency), Dec 1974–May 2020. The "rest-of-day" return (previous close to 30 min before close) predicts the last 30 minutes in every asset class. This predictor beats the first half-hour signal of Gao et al. — [Baltussen et al. PDF](https://www3.nd.edu/~zda/intramom.pdf)
- Gross strategy performance by asset class (1/N within each class; long or short the last 30 min by the sign of the rest-of-day return):

  | Asset class | Return | Volatility | Sharpe |
  |---|---|---|---|
  | Equity index | 6.86% | 3.96% | 1.73 |
  | Government bond | 2.16% | 1.33% | 1.62 |
  | Commodity | 4.34% | 3.05% | 1.42 |
  | Currency | 0.85% | 0.98% | 0.87 |

  For comparison, "Always long last half hour" in equities: Sharpe 0.11 — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf)
- **[DECAY]** Subsample regressions, 1974–1999 vs. 2000–2020:

  | Asset class | 1974–1999 slope (t), R² | 2000–2020 slope (t), R² | Change |
  |---|---|---|---|
  | Equity | 5.96 (t=4.80), R² 3.41% | 3.98 (t=6.65), R² 2.34% | Still strong |
  | Bonds | R² 1.28% | 1.53 (t=3.61), R² 0.47% | Weaker |
  | Commodities | R² 0.23% | 1.04 (t=2.86), R² 0.12% | Weak but significant |
  | Currencies | 1.31 (t=6.48) | 0.33 (t=1.45), R² 0.04% | Insignificant, effectively gone |

  Source: [Baltussen et al., Table (subsamples)](https://www3.nd.edu/~zda/intramom.pdf)
- Mechanism: hedging of short-gamma positions by option market makers and leveraged-ETF rebalancing. Momentum is present when dealers' net gamma exposure is negative and stronger the more negative it is. [SECONDARY] There is no significant intraday momentum on positive-gamma days — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf); [Alpha Architect summary](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/)
- Reversal: the last-half-hour return reverses over the next 1–3 days in all four asset classes. The reversal is highly significant for equities, bonds and commodities and not significant for FX. The authors read this as transitory price pressure, not information — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf)
- **[COST]** The paper's results are before costs. The authors say the strategy "might not be exploitable to many investors after accounting for transaction costs." S&P 500 futures still give a positive net Sharpe at a one-tick cost — [Baltussen et al.](https://www3.nd.edu/~zda/intramom.pdf)

**Other markets, recent replications and decay**
- Li, Sakkas & Urquhart (J. Financial Markets 57, 2022): intraday time-series momentum in 16 developed equity markets is economically and statistically significant in- and out-of-sample in most countries. It is stronger when liquidity is low, volatility is high and information arrives discretely — [IDEAS/RePEc](https://ideas.repec.org/a/eee/finmar/v57y2022ics138641812100001x.html)
- Elaut, Frömmel & Lampaert (J. Financial Markets 37, 2018) document intraday momentum in FX markets and separate informed trading from liquidity provision. Only the title and abstract were available, so no numbers are reported here — [IDEAS/RePEc](https://ideas.repec.org:443/a/eee/finmar/v37y2018icp35-51.html)
- Intraday momentum is also documented in VIX futures (J. Banking & Finance 148, 2023); title only — [IDEAS/RePEc](https://ideas.repec.org/a/eee/jbfina/v148y2023ics0378426622003260.html)
- Zarattini, Aziz & Barbon (SFI Research Paper 24-97, 2024): an intraday trend-following rule on SPY enters when price leaves a volatility-based "noise area" and uses dynamic trailing stops, instead of trading only the last 30 minutes. Reported for 2007–early 2024: 1,985% total return net of commissions and slippage, 19.6% p.a., Sharpe 1.33. This is a working paper with authors from a commercial firm (Concretum); it placed 4th in the Quantpedia Awards 2025 — [Concretum](https://concretumgroup.com/beat-the-market-an-effective-intraday-momentum-strategy-for-sp500-etf-spy/); [SFI](https://www.sfi.ch/de/publications/n-24-97-beat-the-market-an-effective-intraday-momentum-strategy-for-s-p500-etf-spy); [HSG news](https://fsi.unisg.ch/de/newsdetail/news/quantpedia-awards-2025-fsis-barbon-and-team-secure-4th-place-with-intraday-momentum-strategy/)
- **[DECAY]** A 2023 master's thesis (Northern Illinois Univ., high-frequency data 2007–2018) finds intraday momentum patterns, especially in earlier years, weakening over time. A predictable overnight-to-first-half-hour reversal persists. This is a non-peer-reviewed thesis — [NIU Huskie Commons](https://huskiecommons.lib.niu.edu/allgraduate-thesesdissertations/7160)
- **[DECAY] (general benchmark)** McLean & Pontiff (JF 2016; 97 predictors): average long-short returns are about 58% lower after publication. Decay is larger for predictors built only from price and trading data, which is exactly the class intraday momentum belongs to — [McLean & Pontiff PDF](https://Www.Gwern.net/doc/economics/2016-mclean.pdf)

**Crypto**
- Shen, Urquhart & Wang (Financial Review 57(2), 2022): Bitcoin's first half-hour return predicts its last half-hour return, with "market time" defined by trading volume because BTC trades 24/7. Predictability is strongest in high-volume and high-volatility sessions. The authors attribute it to liquidity provision, not late-informed trading. Momentum timing gives economic gains, especially during BTC downturns — [Birmingham research portal](https://research.birmingham.ac.uk/en/publications/bitcoin-intraday-time-series-momentum/); [accepted manuscript](https://reading-9.eprints-hosting.org/100181/3/21Sep2021Bitcoin%20Intraday%20Time-Series%20Momentum.R2.pdf)
- Wen, Bouri, Xu & Zhao (NAJEF 62, 2022): high-frequency BTC data, March 2013–May 2020. They find both intraday momentum and intraday reversal, and say the reversal is unique to crypto. The patterns change in the presence of large intraday jumps, FOMC releases, liquidity conditions and COVID-19. ETH, LTC and XRP are also predictable. Timing beats always-long and buy-and-hold. Momentum is linked to late-informed traders; reversal to overreaction to non-fundamental information — [IDEAS/RePEc abstract](https://ideas.repec.org/a/eee/ecofin/v62y2022ics1062940822000833.html)
- Daily cross-section of more than 3,600 coins: coins with low previous-day returns outperform (daily reversal). The handful of largest, most tradeable coins show daily momentum instead — ["Up or down? Short-term reversal, momentum, and liquidity effects in cryptocurrency markets"](https://earsiv.medeniyet.edu.tr/items/23a96c9f-3952-4bdf-aec5-abafb3aaab70)
- Kim & Hansen (arXiv 2607.09426, July 2026), six Binance perpetual futures: volatility and volume bursts occur at minute, 5-minute and quarter-hour marks and are attributed to algorithms. Quarter-hour opening returns are predictable out-of-sample, and opening order imbalance predicts returns 4–12 hours ahead. The abstract gives no sign, effect size or cost analysis — [arXiv](https://arxiv.org/abs/2607.09426)

### Inferences
- The gross edge per trading day is tiny: about 6.67%/252 ≈ 2.6 bp per day for the SPY signal, and about 6.86%/252 ≈ 2.7 bp for the equity-futures basket (my arithmetic from the figures above). All-in round-trip costs therefore have to stay well below ~1–1.5 bp. This is plausible only with liquid index futures or closing-auction/MOC execution, and not with CFDs or wide-spread ETFs or crypto venues.
- The effect is "continuation into the close, then reversal over 1–3 days." This argues against holding intraday rotation trades overnight or for several days if the move is flow- or hedging-driven.
- The FX leg (JPY/CHF as destination) has the weakest and most decayed intraday-momentum evidence since 2000. Equity index futures, and to a lesser extent bond futures, are where the effect is most robust.
- The negative-gamma dependence implies the signal works best on high-volatility, risk-off days, which are exactly the "rotation" days the user targets. It is weak in calm positive-gamma regimes.

### Gaps
- No peer-reviewed out-of-sample update of Baltussen et al. after May 2020, or of Gao et al. after 2013, was found. Evidence for 2020–2026 rests on the Zarattini et al. working paper and a thesis.
- No net-of-cost results were found for crypto intraday momentum, either at exchange fees or at funding/slippage levels.
- The Elaut et al. (FX) and Li et al. (16 markets) papers' effect sizes were not retrieved (paywalled).

---

## 2. Short-term reversal vs. continuation after large intraday shocks/jumps (overreaction vs. underreaction)

### Takeaway
The evidence is conditional. Shocks driven by information or news tend to continue (drift). Shocks without news, driven by liquidity or hedging, tend to revert within days. Market-level intraday moves continue into the close but revert over the next 1–3 days. Time-series momentum persists for 1–12 months and partially reverses afterwards.

### Cited Findings
- Savor (JFE 106, 2012): large stock price moves accompanied by information (analyst reports) are followed by drift. No-information moves reverse. Drift exists only when the price move and the analyst recommendation change have the same sign. The ratio of no-information to information shocks correlates with implied volatility and forecasts momentum returns — [UPenn repository](https://repository.upenn.edu/handle/20.500.14332/34495)
- Follow-up (Govindaraj, Livnat, Savor, Zhao): when analysts revise immediately after large price shocks, prices show momentum. Unrevised shocks show short-term reversals, consistent with liquidity- or noise-trader-driven moves — [Alpha Architect summary](https://alphaarchitect.com/follow-the-trend-and-the-sell-side/)
- Jiang & Zhu (JFE 124, 2017): large stock-price jumps proxy for information shocks. Buying after positive jumps and selling after negative jumps earns significantly positive returns over the next 1–3 months. Overnight jumps show the strongest underreaction, partly attributed to limited attention — [IDEAS/RePEc](https://ideas.repec.org/a/eee/jfinec/v124y2017i1p43-64.html)
- A Financial Review 2025 paper on China finds underreaction to overnight information shocks but overreaction (reversal) to intraday information shocks — [IDEAS/RePEc](https://ideas.repec.org/a/bla/finrev/v60y2025i2p623-652.html)
- At market level across futures, the last-half-hour move (hedging-driven continuation) reverses over the next 1–3 days, significantly in equities, bonds and commodities — [Baltussen et al. 2021](https://www3.nd.edu/~zda/intramom.pdf)
- Crypto: intraday momentum and reversal coexist, and the pattern changes with large intraday jumps — [Wen et al. 2022](https://ideas.repec.org/a/eee/ecofin/v62y2022ics1062940822000833.html)
- Flight-to-safety spells (stock–bond): the return effect on days after the onset is much smaller than at onset. Model estimates on subsequent FTS days are −0.13%/day for equities and +0.05%/day for bonds, vs. much larger onset jumps — [Baele et al. 2020](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/Flights%20to%20Safety.pdf)
- Monthly horizon: time-series momentum shows return persistence for 1–12 months that partially reverses over the following ~4 years, consistent with initial underreaction and delayed overreaction — [Moskowitz, Ooi & Pedersen 2012](https://fairmodel.econ.yale.edu/ec439/jpde.pdf)

### Inferences
- For a "join the rotation" system, the key filter is whether there is a fundamental or news driver (policy, macro data, credit event) versus a flow, hedging or liquidation driver (gamma, margin calls, leverage flush). The first favors holding for days to weeks. The second favors a same-day continuation trade with an exit by the close, or even fading the move on day 2–3.
- Overnight shocks (e.g., Asian-session or weekend news) are more likely to be underreacted to than intraday shocks, according to equity-level evidence. That is a possible edge for entering at the European or US open.

### Gaps
- No study was found that specifically tests continuation vs. reversal after large cross-asset rotation days (e.g., Nasdaq −3% and gold +2% on the same day) at intraday horizons. The evidence is from single-asset studies only.
- Index-futures-level jump studies with explicit next-day/next-week returns after large intraday moves (beyond Baltussen's last-half-hour regression) were not retrieved.

---

## 3. Time-series momentum / trend following across asset classes; crisis alpha; 2020–2026 performance; short-term trend

### Takeaway
Multi-month trend following across futures has more than a century of positive gross evidence: net Sharpe about 0.77 after hypothetical 2/20 fees (1880–2013), with crisis alpha in slow bear markets. However, risk-adjusted returns have fallen since 2000 (net Sharpe 0.62 for 2000–2013; SG Trend Index CAGR about 5.2–5.3% since 2000). Performance after 2022 has been weak: +27% in 2022 but only +2.4% in 2025, with a deep tariff-whipsaw drawdown. The statistical robustness of time-series predictability itself is disputed.

### Cited Findings
- Moskowitz, Ooi & Pedersen (JFE 104, 2012): 58 liquid futures (equity index, currency, commodity, bond), main sample Jan 1985–Dec 2009 with data from 1965. 12-month time-series momentum is positive for every one of the 58 contracts. A diversified portfolio has a Sharpe greater than 1, roughly 2.5 times the equity market, with little exposure to standard factors. It performs best in extreme markets. The pre-1985 period, which the authors present as out-of-sample, shows an annualized Sharpe of 1.1. Losses occur when crises end and trends sharply reverse (e.g., 2009) — [MOP PDF](https://fairmodel.econ.yale.edu/ec439/jpde.pdf); [SSRN](https://papers.ssrn.com/abstract=2089463)
- Hurst, Ooi & Pedersen ("A Century of Evidence on Trend-Following Investing", AQR; JPM 2017 version extended to 2016), 67 markets, Jan 1880–Dec 2013, after simulated transaction costs:
  - Gross 14.9% p.a.; net of 2/20 fees 11.2% p.a.; volatility 9.7%; net Sharpe 0.77; correlation 0.00 to US equities and −0.04 to US 10-year bonds.
  - Net Sharpe by decade: 1970s 1.70; 1980s 0.96; 1990s 0.98.
  - **[DECAY]** 2000–2013: 11.3% gross, 7.9% net, Sharpe 0.62.
  - Positive returns in 8 of the 10 largest 60/40 drawdowns. The paper notes most bear markets "occurred gradually over several months, rather than abruptly over a few days," which is why trend following worked in them.
  - Source: [AQR whitepaper PDF](https://www.TrendFollowing.com/whitepaper/Century_Evidence_Trend_Following.pdf)
- [SECONDARY] Net Sharpe figures for the 1880–2016 JPM version differ between summaries: 0.76 after all costs and 2/20 fees per Swedroe, vs. 0.4 average Sharpe after 2%+20% fees per CXO. The discrepancy is unresolved — [ETF.com/Swedroe](https://www.etf.com/node/93857.md); [CXO Advisory](https://www.cxoadvisory.com/momentum-investing/trend-following-with-intrinsic-momentum-over-the-very-long-run)
- Asness, Moskowitz & Pedersen ("Value and Momentum Everywhere", JF 2013): consistent momentum premia across 8 markets and asset classes (stocks in 4 regions, equity index futures, government bonds, currencies, commodities). There is a strong common factor across asset classes, and global funding liquidity risk is a partial source (negatively related to momentum) — [AQR](https://www.aqr.com/Insights/Research/Journal-Article/Value-and-Momentum-Everywhere); [ETF.com summary](https://www.etf.com/sections/index-investor-corner/swedroe-close-look-value-momentum)
- **[DECAY / critique]** Huang, Li, Wang & Zhou ("Time series momentum: Is it there?", JFE 135, 2020): asset-by-asset regressions show little evidence of time-series momentum, in- or out-of-sample. The pooled t-statistic falls below bootstrap critical values. The TSMOM strategy is profitable but performs about the same as a strategy based on the historical sample mean, i.e., without requiring predictability — [WUSTL profile](https://profiles.wustl.edu/en/publications/time-series-momentum-is-it-there/); [CXO](https://www.cxoadvisory.com/momentum-investing/intrinsic-time-series-momentum-does-not-really-exist/). Rebuttal: Alpha Architect's replication finds pooled results "fairly robust" — [Alpha Architect](https://alphaarchitect.com/are-trend-following-and-time-series-momentum-research-results-robust/)
- Speed of trend:
  - Goulding, Harvey & Mazzoleni ("Momentum Turning Points", JFE 2023): slow (12-month) and fast (1-month) signals disagree at turning points. Slow signals react late, while fast signals give false alarms. Blended intermediate speeds earn positive unconditional alpha, and dynamic speed selection beats the best static speed in most countries. Slower momentum is preferred after "Correction" months, faster after "Rebound" months — [Alpha Architect](https://alphaarchitect.com/momentum-trends/); [CXO](https://www.cxoadvisory.com/technical-trading/mitigating-impact-of-price-turning-points-on-trend-following/)
  - "Breaking Bad Trends": the more turning points an asset has, the worse its 12-month trend strategy's risk-adjusted performance — [Duke PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P167_Breaking_bad_trends.pdf)
- Recent live performance (SG Trend Index = 10 largest trend-following CTAs):
  - 2022: +27.35%, the best year since the index launched in Jan 2000 — [The Full FX](https://thefullfx.com/year-end-drop-fails-to-dampen-stellar-2022-for-trend-followers/)
  - 2024: average pairwise correlation among constituents was 0.78, but the range of returns was about 15 pp, so manager and speed choice matter — [SG CTA Update 2025](https://content.sgmarkets.com/CTA_UPDATE_KEEPING_UP_WITH_THE_TRENDFOLLOWERS_2025)
  - **[DECAY / recent]** 2025: −2.22% in May alone, and the TTU trend index was down more than −11.19% YTD by end-May after an April described as "carnage" around the tariff shock — [TTU May 2025](https://www.toptradersunplugged.com/trend-following-performance-report-may-2025/). October 2025 +1.41% (trailing 12 months +3.86%; since-inception CAGR 5.23%, max drawdown −20.61%) — [TTU Oct 2025](https://www.toptradersunplugged.com/trend-following-performance-report-october-2025/). Full-year 2025 +2.39% (December +1.92%; since-inception CAGR 5.33%) — [TTU Dec 2025 report](https://www.toptradersunplugged.com/?p=20381)

### Inferences
- Trend following earns its crisis alpha in gradual, multi-month bear markets (2008, 2022). It loses in V-shaped policy shocks: the April 2025 tariff shock and reversal, the 2009 crisis end and the March 2020 spike-and-rebound. Those V-shaped shocks are exactly the intraday or few-day "rotation" events the user wants to trade, so slow trend is not a substitute for an intraday rotation system.
- Expect much lower live Sharpe than century backtests: about 0.3–0.6 for diversified trend after costs in the 2000–2025 era, judging from the 0.62 net Sharpe for 2000–2013 and the SG index's roughly 5% CAGR with a ~20% max drawdown.

### Gaps
- Full-year SG Trend Index returns for 2023 and 2024, and 2026 YTD, were not retrieved from a reliable source. A search snippet reported SG Trend Index YTD −7.56% at end-August 2025, followed by a +5.73% September, but the exact TTU report page was not verified, so it is excluded from the findings.
- No rigorous public data was found on short-term (days–weeks lookback) trend programs' 2020–2026 performance vs. slow trend, e.g., in April 2025.
- The exact diversified Sharpe in MOP Table 3 was not extracted (only "greater than one" from the text).

---

## 4. Flight-to-quality / flight-to-safety: Baele et al. 2020; gold (Baur & Lucey; Baur & McDermott); JPY/CHF (Ranaldo & Söderlind); duration; continuation after day 1?

### Takeaway
Flight-to-safety episodes are rare (under 2% of days), large (bond-minus-equity return of about 2.7–2.8% on day 1) and short: 62% last one day and none last more than 10 days. Most of the move happens on the first day, and subsequent-day effects are much smaller. CHF and JPY reliably appreciate on FTS days (+0.33% and +0.44%). Gold's raw FTS-day return is about zero (+3 bp), and its safe-haven property lasts only about 15 trading days after a shock.

### Cited Findings
**Baele, Bekaert, Inghelbrecht & Wei ("Flights to Safety", RFS 33(2), 2020)**
- Sample: 23 countries, Jan 1980–Jun 2015, FTS days identified from stock and bond returns only. FTS days are under 2% of the sample and show an average bond-equity return differential of 2.7%. They coincide with significant flows out of equity funds into government bond and money-market funds — [Baele et al. PDF](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/Flights%20to%20Safety.pdf)
- Spell duration: 62% last 1 day, 23% last 2 days, 9% last 3 days, 6% last longer than 4 days, and none longer than 10 days. The first-day return impact is 2.79%, a 2.3-SD move — [Baele et al.](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/Flights%20to%20Safety.pdf)
- On the day before an FTS spell, equity returns are slightly but significantly positive and bond returns slightly negative, so there is no lead-in warning. Equity and bond volatility regimes last about 32 days on average — [Baele et al.](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/Flights%20to%20Safety.pdf)
- On subsequent FTS days the return effect is "much smaller": equity −0.13%/day and bonds +0.05%/day — [Baele et al.](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/Flights%20to%20Safety.pdf)
- Safe-haven FX on FTS days: CHF +0.33% (significant in 20+ countries), JPY +0.44% (20+ countries), USD +0.07% (mixed: 7 countries significant appreciation, 6 significant depreciation) — [Baele et al.](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/Flights%20to%20Safety.pdf)
- Gold on FTS days: +3 bp on average and almost never significant. After controlling for global equity exposure, it is +0.20%/day and significant in half the countries, i.e., gold hedges FTS only after removing its positive equity beta — [Baele et al.](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/Flights%20to%20Safety.pdf)
- The US TED spread rises about 5 bp on an FTS day, so FTS is not always a credit event. Emerging markets, endowments and hedge funds perform poorly during FTS — [Baele et al.](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/Flights%20to%20Safety.pdf)

**Gold**
- Baur & Lucey (Financial Review 45, 2010), daily US/UK/German data, about Nov 1995–Nov 2005: gold is a hedge against stocks on average and a safe haven in extreme stock-market conditions, but only for about 15 trading days after an extreme shock. It is not a safe haven for bonds — [TCD working paper](https://www.tcd.ie/triss/assets/PDFs/iiis/iiisdp198.pdf); [CXO summary](https://www.cxoadvisory.com/gold/gold-as-hedge-and-safe-haven/)
- Baur & McDermott (2010) find gold a safe haven and hedge for European and US stock markets, as cited in — [Baele et al.](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/Flights%20to%20Safety.pdf)

**Safe-haven currencies**
- Ranaldo & Söderlind (Review of Finance 14(3), 2010): CHF and JPY appreciate vs. USD when US stocks fall, US bonds rise and FX volatility rises. This holds at horizons from a few hours to several days, non-linearly with volatility and during crises; the yen effect was strongest in the GFC. The working-paper version links the safe-haven behavior to carry-trade losses — [SNB WP 2007/17](https://www.snb.ch/en/mmr/papers/id/working_paper_2007_17); [HSG Alexandria](https://www.alexandria.unisg.ch/id/eprint/57677); [CEPR DP7249](https://cepr.org/publications/DP7249)
- **[DECAY / regime]** The yen was a reliable safe haven from the GFC to COVID but not in 2022, when rate differentials became its dominant driver — [Man Group](https://www.man.com/insights/road-ahead-yen-behaving-badly)
- In 2022, short-term US–JP rate differentials rose from 0.3% to 4.9%, and the yen-funded carry trade hampered yen risk-off behavior — [LGIM](https://blog.lgim.com/categories/investment-strategy/does-the-yen-still-work-as-a-safe-haven-currency/)
- The yen hit its weakest level in two decades (beyond ¥130/$) in April 2022 despite the energy shock — [ADBI](https://www.asiapathways-adbi.org/2022/05/plunging-yen-hit-by-widening-interest-rate-differentials-and-rising-commodity-prices/); [AMRO note](https://amro-asia.org/wp-content/uploads/2022/09/AMRO-Analytical-Note-on-JPY_final.pdf)
- Initial COVID flight to safety (Feb 2020): US Treasury yields fell about 100 bp and gold rose about 4% before the March dash for cash reversed safe-asset gains — [BIS / Cunliffe speech](https://www.bis.org/review/r220210f.htm)

### Inferences
- Joining a flight-to-safety trade after it has visibly started captures mainly the rest of day 1. Day-2+ expected moves are small (−0.13%/day equity), and 62% of spells are already over after one day. Intraday detection plus a same-day or 1–2-day holding period is the only horizon consistent with this evidence.
- On risk-off days the stronger destination legs are long CHF and JPY vs. risk currencies (historically +0.3–0.4% on FTS days) and long Bunds/Treasuries in a negative stock–bond correlation regime. Raw gold is a weak same-day destination (+3 bp average). Gold's safe-haven window is about 15 trading days, so gold suits a multi-day hold better than a day-1 hold.
- JPY's safe-haven reliability is regime-dependent, weakening with wide rate differentials and carry positioning. The August 2024 yen-carry unwind shows JPY can spike in risk-off when the carry trade unwinds, but that is a positioning effect, not a structural one (no numeric source retrieved).

### Gaps
- Intraday (hourly) dynamics of safe-haven assets on FTS days were not found: how much of the day-1 move happens in the first hour, and how much is left by the time a signal triggers.
- Post-2015 updates of the Baele FTS classification (covering 2020, 2022, 2025) were not found.
- Baur & McDermott 2010 primary numbers were not retrieved.

---

## 5. Stock–bond correlation regimes and safe-haven failures (March 2020, 2022, April 2025): implications for "buy Treasuries on risk-off"

### Takeaway
"Buy Treasuries on risk-off" works only in a negative stock–bond correlation regime (low and stable inflation, 2000–2021). Since 2022 the correlation has been positive (about +0.4 on 36-month windows), and Treasuries failed as a hedge in three distinct ways:
- liquidity "dash for cash" (March 2020);
- inflation and rate shock (2022);
- policy-credibility shock (April 2025: long yields up about 50 bp in a week while the USD fell).

A rotation system must condition the destination asset on the regime.

### Cited Findings
- US stock–bond correlation was about +0.35 in 1970–1999 and −0.31 in 2000–2022 — [Alpha Architect](https://alphaarchitect.com/stock-bond-correlation/)
- The average 36-month stock–bond correlation was −0.37 over 2011–2021 and +0.41 after 2022, as of Sept 2025 — [State Street Global Advisors](https://www.ssga.com/library-content/assets/pdf/global/wmu/2025/mom-20251003.pdf)
- A 60/40 portfolio fell 17.5% in 2022, its worst year since 1937 and 4th worst in 200 years, as central banks fought the highest inflation in 40 years — [Morgan Stanley IM](https://www.morganstanley.com/im/publication/insights/articles/article_bigpicturereturnofthe6040_A4.pdf). SSGA puts the 2022 loss at −16.7% — [SSGA](https://www.ssga.com/library-content/assets/pdf/global/wmu/2025/mom-20251003.pdf)
- AQR (Brixton, Brooks, Hecht, Ilmanen, Maloney, McQuinn 2023), [SECONDARY]: moving the stock–bond correlation from −0.5 to +0.5 raises 60/40 volatility about 20% and 12-month VaR and max drawdown about 30%. Inflation uncertainty is the key driver of positive correlation — [WealthManagement summary](https://www.wealthmanagement.com/equities/implications-regime-shifting-stock-and-bond-correlations); [Quantpedia](https://quantpedia.com/estimating-stocks-bonds-correlation-from-long-term-data/)
- Ilmanen: the correlation is lowest in deflationary recessions and flight-to-quality episodes; inflation uncertainty raises the common discount-rate channel — [Russell Investments](https://russellinvestments.com/au/blog/is-the-stock-bond-correlation-positive-or-negative); [Vanguard](https://www.ch.vanguard/content/dam/intl/europe/documents/en/the-stock-bond-correlation-eu-en-pro.pdf)

**March 2020 "dash for cash"**
- After an initial flight to safety in February, from 9 to 18 March investors sold their most liquid assets, including safe assets, because other markets were illiquid — [BIS / Cunliffe](https://www.bis.org/review/r220210f.htm)
- The disruption hit the US Treasury market disproportionately compared with other advanced-economy sovereign markets — [NY Fed / Fed in Print](https://www.fedinprint.org/item/fednep/97451)
- A flight to safety can itself trigger a dash for cash when dealer balance sheets are constrained — [OFR blog](https://www.financialresearch.gov/the-ofr-blog/2023/04/03/ofr-models-one-theory-on-the-cause-of-march-2020s-treasury-market-fragility/)
- Gold fell about 3% on 12 March 2020 alone, linked to selling of liquid assets to meet margin calls — [WisdomTree](https://www.wisdomtree.eu/de-lu/blog/2020-03-13/gold-price-moves-on-12th-march-2020-opening-up-attractive-entry-points). [SECONDARY, window-dependent] Market commentary puts gold's March 2020 drawdown at about 10–12% — [ii.co.uk](https://ii.co.uk/analysis-commentary/why-did-safe-haven-gold-fall-value-during-market-sell-ii512586); [Market Index](https://www.marketindex.com.au/news/why-is-gold-selling-off-amid-market-turmoil)

**April 2025 tariff shock**
- The 10-year UST yield rose almost 50 bp between 4 and 11 April 2025, the third-largest weekly rise since 1986. The USD fell broadly (about 12% vs. EUR YTD, about 7 pp of that after 1 April), and the VIX hit levels exceeded only in the GFC and COVID. "The US dollar depreciated strongly while US Treasury yields rose – the opposite of what usually happens in a risk-off environment" — [ECB Financial Stability Review, Nov 2025](https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202511_01~fdf147a04a.en.html)
- Speculative net-long USD positions flipped to net short and stayed short for months. The 10y yield–USD correlation turned negative after 2 April. Foreign outflows were sizeable but short-lived, with a strong rebound in May, and the dollar stabilized from July. The ECB does not conclude that safe-haven status changed and says the next major shock will be the test — [ECB FSR Nov 2025](https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202511_01~fdf147a04a.en.html)
- The convenience yield of long-dated Treasuries fell, consistent with safe-asset investors rotating from long Treasuries into shorter-term Treasuries and gold — [NBER w34640 (Acharya & Laarits)](https://www.nber.org/papers/w34640)
- Banco de España WP 2629 (Sept 2026): the initial reaction looks like a standard safe-haven shock. Subsequent dollar and long-yield co-movement reflects distinct shocks: confidence in US institutions, Treasury-market intermediation and the convenience value of dollar safe assets — [Banco de España](https://www.bde.es/wbe/en/publicaciones/analisis-economico-investigacion/documentos-trabajo/what-volatility-reveals-agnostic-identification-of-exchange-rate-and-treasury-market-dynamics-in-inconvenient-times.html)
- The dollar also failed as a natural hedge during the March 2020 dash for cash, and its co-movement with other safe havens was negative in early 2017 — [ECB FSR Nov 2025](https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202511_01~fdf147a04a.en.html)

### Inferences
- Destination selection should be regime-aware. In positive-correlation or inflation regimes, and in US-policy-credibility shocks, prefer short-dated Treasuries/T-bills, gold, CHF and (conditionally) JPY over long Treasuries and USD. In liquidity crises (dash for cash), every asset including gold and Treasuries can fall for several days, and the safe destination is cash.
- A practical classifier: rolling 20–60-day stock–bond (e.g., ES vs. ZN/Bund) correlation, plus the sign of the same-day yield move on a risk-off day. Rising yields on an equity selloff means do not buy duration. This is my inference from the regime evidence above, not a tested rule.

### Gaps
- No academic study was found that measures intraday safe-haven returns (Treasuries, gold, JPY, CHF) on April 2–10, 2025 or on March 9–18, 2020 at hourly resolution.
- No BIS Quarterly Review piece on April 2025 was retrieved.
- No peer-reviewed source was found for gold's exact March 2020 drawdown.

---

## 6. Is Bitcoin a risk asset or a safe haven? Correlation with Nasdaq 2020–2026; BTC in risk-off; does 24/7 BTC lead equities?

### Takeaway
Since 2020 Bitcoin has behaved as a high-beta risk asset, not a safe haven. It fell with equities in March 2020, and its correlation with the Nasdaq-100 averaged 0.52 in 2025. Losses are asymmetric: larger on down days. In a risk-off rotation, BTC is a source (short or avoid) candidate, not a destination. No credible academic evidence was found that weekend BTC moves predict the Monday equity open.

### Cited Findings
- IMF: the daily correlation of BTC with the S&P 500 was 0.01 in 2017–19 and 0.36 in 2020–21. BTC–MSCI EM correlation was 0.34 in 2020–21, a 17-fold increase. The change came after the extraordinary central bank crisis responses of early 2020 — [IMF blog, Jan 2022](https://www.imf.org/en/blogs/articles/2022/01/11/crypto-prices-move-more-in-sync-with-stocks-posing-new-risks)
- LSEG data via Reuters: the average 2025 correlation of BTC with the Nasdaq-100 was 0.52 (2024: 0.23), and with the S&P 500 0.50 (2024: 0.29) — [The Globe and Mail / Reuters](https://www.theglobeandmail.com/investing/article-bitcoins-2025-rollercoaster-may-end-on-a-low)
- K33 Research: the 30-day BTC–Nasdaq correlation was 0.44 in late October 2025. BTC lagged on up days and lost more on down days — [FXStreet](https://www.fxstreet.com/amp/cryptocurrencies/news/bitcoin-underperforms-nasdaq-following-october-plunge-as-k33-predicts-rebound-on-the-horizon-202510212105)
- The 10 October 2025 crypto crash liquidated more than $19bn of leveraged positions. BTC then decoupled downward from the Nasdaq (Nasdaq-100 +0.44% vs. BTC −3.71% in the week from 15 Oct) — [The Currency Analytics](https://thecurrencyanalytics.com/bitcoin/bitcoin-decouples-from-nasdaq-amid-leverage-driven-selloff-206295)
- Conlon & McGee (Finance Research Letters 35, 2020): BTC fell in lockstep with the S&P 500 in the COVID bear market, and even small BTC allocations substantially increased portfolio downside risk. Not a safe haven — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7246008)
- Contrasting study (smooth-transition regression): BTC showed some safe-haven features during COVID, with results varying by market and horizon — [Qatar Univ. QSpace](https://qspace.qu.edu.qa/handle/10576/38546)
- Weekend lead:
  - No paper was found testing whether weekend BTC returns predict Monday equity returns.
  - Ali, Du & Majeed (Finance Research Letters 77, 2025; 72 cryptos vs. S&P 500, 2018–2024, TVP-VAR): the choice of weekend/Monday return benchmark changes both the size and direction of measured crypto–equity spillovers — [IDEAS/RePEc](https://ideas.repec.org/a/eee/finlet/v77y2025ics1544612325002806.html)
  - Binance Research (vendor), as reported by Finance Magnates: tokenized-stock weekend prices captured a median 92% of the Monday reopening move across 7 weekends. The article itself states this does not establish prediction — [Finance Magnates](https://www.financemagnates.com/thought-leadership/the-convergence-trade-nobody-planned-on-chain-fridays-to-nyse-mondays/)
- BTC has its own Monday effect, with Monday returns significantly higher in one study — [CESifo WP 6716](https://cesifo.org/DocDL/cesifo1_wp6716.pdf); other studies find no consistent day-of-week effect — [Applied Finance Letters](https://ojs.aut.ac.nz/applied-finance-letters/article/download/266/85)

### Inferences
- In a "Nasdaq/BTC → gold/Treasuries/CHF/JPY" rotation, BTC belongs on the risk (source) side. Its correlation with tech is regime-dependent (0.2–0.5 annual averages, occasionally negative on 20-day windows), and it can sell off for crypto-specific leverage reasons when equities are calm (Oct 2025).
- BTC's 24/7 trading could serve as an early risk-sentiment gauge on weekends, but this is untested academically. Any use requires the user's own out-of-sample testing, with care over how Monday returns are defined.

### Gaps
- No peer-reviewed intraday lead–lag study of BTC vs. Nasdaq futures (who leads whom at minute or hourly frequency) was retrieved.
- BTC's behavior during 2–10 April 2025 was not documented in retrieved sources.
- The source for a −0.43 20-day correlation reading in late 2025 or 2026 was undated, so it was excluded.

---

## 7. Flow-induced price pressure: do fund/ETF flows predict returns (Coval & Stafford; Gabaix & Koijen; Ben-Rephael, Kandel & Wohl; spot BTC ETF flows)? Momentum vs. reversal after flows

### Takeaway
Flows move prices strongly at the time of the flow: $1 into equities raises market value by about $5, and fire-sale selling depresses commonly held stocks. Much of that effect reverts:
- about half within 10 trading days for daily flows (Israel);
- 85% within 4 months and all within 10 months for US bond-to-equity fund switches.

So flows are a short-term continuation signal (days) and a medium-term reversal signal (weeks to months). For spot BTC ETFs there is only weak, short-sample evidence of flows leading price by a few days.

### Cited Findings
- Coval & Stafford (JFE 86(2), 2007; mutual-fund flows 1980–2004): funds with large outflows (inflows) cut (expand) existing positions, creating price pressure in commonly held stocks. Investors who trade against constrained funds earn significant returns for providing liquidity. Because flow-driven trades are predictable, there is an incentive to front-run them — [NBER w11357](https://www.nber.org/papers/w11357); impact-then-reversal pattern as characterized by later work — [Honkanen, HEC](https://hal-hec.archives-ouvertes.fr/hal-01941538)
- Gabaix & Koijen (Inelastic Markets Hypothesis; NBER w28967): using granular instrumental variables, investing $1 in the stock market raises aggregate market value by about $5. The aggregate demand elasticity is small because institutions have fixed-equity-share mandates. Sample: US flows across investor categories, 1993–2018 [SECONDARY for the sample] — [NBER w28967](https://www.nber.org/papers/w28967); [CXO summary](https://www.cxoadvisory.com/big-ideas/inelastic-markets-hypothesis/)
- Ben-Rephael, Kandel & Wohl (JFE 104, 2012; US): net exchanges between bond and equity funds (a monthly sentiment proxy) relate to contemporaneous market returns, with 1 SD corresponding to 1.95% of excess market return. 85% of that relation reverses within 4 months and all of it within 10 months, and the effect is stronger in small and growth stocks — [TAU PDF](https://en-coller.tau.ac.il/sites/nihul_en.tau.ac.il/files/RP_219_Wohl_0.pdf)
- Ben-Rephael, Kandel & Wohl (JFQA 46, 2011; Israel, daily aggregate equity-fund flows): flows cause temporary price pressure, and about half reverses within 10 trading days — [IDEAS/RePEc](https://ideas.repec.org/a/cup/jfinqa/v46y2011i02p585-603_00.html)
- FTS days coincide with significant outflows from equity funds into government-bond and money-market funds — [Baele et al. 2020](https://business.columbia.edu/sites/default/files-efs/citation_file_upload/Flights%20to%20Safety.pdf)
- Hedging flows (gamma, leveraged-ETF rebalancing) create intraday continuation that reverses over 1–3 days — [Baltussen et al. 2021](https://www3.nd.edu/~zda/intramom.pdf)
- Spot BTC ETFs:
  - FalconX (Jan–Oct 2024, VAR): the lagged daily ETF inflow coefficient on next-day BTC return is positive (0.027). The impulse response peaks at about +1.2% around day 3–4 and then fades. Granger test flows → price F = 8.48, p = 0.004. The 7-day flow–price correlation is 0.30, so flows explain under 10% of price variance — [FalconX](https://www.falconx.io/newsroom/what-can-spot-etf-flows-tell-us-about-the-trajectory-of-bitcoin-prices-a-preliminary-statistical-investigation)
  - CoinShares (2024): 45-day price changes vs. weekly flows/AuM give R² = 0.31 — [CoinShares](https://researchblog.coinshares.com/us-bitcoin-etf-launch-price-impact-d94d4ad02d93)
  - Ledger (2025; 11 Jan 2024–16 May 2025): ETF assets and BTC price are cointegrated only at the 10% level, a long-run co-movement and not a forecasting test — [Ledger](https://ledger.pitt.edu/ojs/ledger/article/view/393)

### Inferences
- Observed flow data (ETF creations/redemptions, fund-flow reports) arrive with a lag of T+1 or weekly. By the time a retail trader sees them, the contemporaneous price impact has happened. The remaining continuation is a few days at most (BTC ETF IRF peak at day 3–4). The robust trade after large, sentiment-driven flows is a reversal over weeks to months.
- Intraday "money flow" is better proxied by price action itself (rest-of-day return, cross-asset co-movement) than by published flow statistics, which are too slow for the intraday horizon.

### Gaps
- Exact abnormal-return and reversal magnitudes and horizons in Coval & Stafford were not retrieved.
- No peer-reviewed out-of-sample study of spot-BTC-ETF-flow trading strategies, with or without costs, was found; existing evidence is industry research on about 10 months of data.
- No study was found linking gold-ETF (e.g., GLD) or Treasury-ETF (e.g., TLT) daily flows to next-day returns.

---

## 8. Cross-asset lead–lag at high frequency (bond futures → equities, FX, copper/oil, crypto) and exploitability after costs

### Takeaway
High-frequency lead–lag relationships exist: futures lead cash markets in Treasuries, equities and EUR/USD, and order-book imbalance in one asset predicts another's midquote. They are exploitable mainly at milliseconds to seconds by colocated HFTs. No evidence was found that a retail-latency (seconds to minutes) cross-asset lead–lag strategy survives costs.

### Cited Findings
- Dobrev & Schaumburg (Fed/AEA 2018): price discovery in US Treasuries, equities and EUR/USD takes place primarily in futures rather than cash markets. Cross-market trading and liquidity provision are measured in (near-)arbitrage-linked markets at high frequency — [Atlanta Fed conference PDF](https://www.atlantafed.org/-/media/documents/news/conferences/2018/1018-financial-stability-implications-of-new-technology/papers/dobrev-schaumburg_high-frequency-cross-market-trading.pdf)
- Huth & Abergel ("High frequency lead/lag relationships"): tick-level cross-correlations are strongly asymmetric, especially futures leading stocks — [arXiv 1111.7103](https://www.arxiv.org/pdf/1111.7103)
- Cestonaro: transaction prices and best-quote order-book imbalance of one asset carry information on another asset's future midpoint across stocks, futures and ETPs — [eflab Frankfurt](https://www.eflab.de/events/detail/jour-fixe-lead-lag-relationships-in-market-microstructure)
- Poutré, Dionne & Yergeau (arXiv 2025; DAX-30 cross-listed stocks): an HFT can profit from lead–lag predictability even after trading costs, latency and execution risk — [arXiv 2501.03171](https://arxiv.org/abs/2501.03171v1)
- Crypto perpetuals: order imbalance at quarter-hour openings predicts returns over 4–12 hours. Effects are much weaker at finer clock-time frequencies — [Kim & Hansen 2026](https://arxiv.org/abs/2607.09426)
- Within-day cross-asset structure (Baltussen): the second-to-last half-hour return predicts the last half-hour in equities and bonds but not in commodities or currencies — [Baltussen et al. 2021](https://www3.nd.edu/~zda/intramom.pdf)

### Inferences
- For a retail API trader (IBKR latency of roughly 100 ms to seconds, non-colocated), microsecond lead–lag between ES/ZN/6E futures and cash is not capturable. A realistic use of cross-asset lead–lag is confirmation: entering a destination asset only once the source asset and a second confirming market (e.g., ES down and ZN/Bund up and JPY up) agree. This is a regime filter, not a latency arbitrage.

### Gaps
- No studies were found on minute-to-hour lead–lag between bond futures and equity futures, copper/oil vs. equities, or BTC vs. Nasdaq futures with net-of-cost strategy results for non-HFT latency. This remains a key open question that requires the user's own testing.

---

## 9. Daily/swing reference: tactical asset allocation on cross-asset momentum or risk-on/off regimes (Faber GTAA, Antonacci dual momentum, Keller DAA/canary assets, risk-appetite timing): performance and decay

### Takeaway
Monthly-rebalanced TAA (10-month moving-average filters, dual momentum, canary-based risk-off switching) mainly improves drawdowns and Sharpe relative to buy-and-hold in long crashes (2000–02, 2008). Since publication, live and out-of-sample results are modest: Faber-style GTAA had Sharpe about 0.68 and CAGR about 6% in 2006–2025 and trailed stocks in most post-2009 years. Canary or fast-switching variants are vulnerable to V-shaped crashes such as March 2020.

### Cited Findings
- Faber (JPM 2018 "Revisited 10 Years Later") [SECONDARY]: the Sharpe ratio rose from 0.45 to 0.80 with timing. The timing system beat stocks in 2008–09 but trailed them in 6 of the following 8 years — [ETF.com / Swedroe](https://www.etf.com/sections/index-investor-corner/swedroe-why-financial-trends-persist)
- Faber's 2013 update reports good real-time results: equity-like returns with bond-like volatility and drawdowns — [Quantpedia](https://quantpedia.com/strategies/asset-class-trend-following)
- **[DECAY]** An independent extension of the original GTAA rules for 2006–Mar 2025 gives Sharpe 0.68, CAGR 6.05% and max drawdown 11.7% — [Concretum](https://concretumgroup.substack.com/p/global-tactical-asset-allocation)
- Keller & Keuning (DAA, "Breadth Momentum and the Canary Universe", 2018):
  - Crash protection is triggered by breadth momentum of a two-asset canary universe (VWO and BND proxies, chosen on 1926–1970 data).
  - The average cash fraction is often less than half that of VAA, with better return/risk and lower turnover — [CXO Advisory](https://www.cxoadvisory.com/strategic-allocation/multi-class-momentum-portfolio-with-canary-crash-protection/)
  - Reported Dec 1970–Oct 2018 return/max drawdown of 16.5%/14.4% for one variant, with 0.1% costs. This is caveated as a period of mainly falling interest rates — [Alpha Architect](https://alphaarchitect.com/?p=43813)
- **[DECAY]** A QuantConnect replication of the related HAA (canary TIP) strategy found results "not as good as in the paper," mainly due to the March 2020 crash — [QuantConnect forum](https://www.quantconnect.com/forum/discussion/14842/hybrid-asset-allocation/)
- Antonacci GEM: 12-month relative momentum between US and foreign stocks plus an absolute-momentum filter vs. T-bills, switching to bonds. The original test used 1974–2011; the author-claimed out-of-sample periods are 1950–1973 and 2012–2018. ReSolve replicated the backtest closely — [Advisor Perspectives / ReSolve](https://files.advisorperspectives.com/articles/2019/05/06/global-equity-momentum-a-craftsmans-perspective); [Hedge Fund Alpha](https://hedgefundalpha.com/strategies/is-gary-antonaccis-global-equity-momentum-strategy-robust/)
- The diversified trend-following comparison (2000–2013 net Sharpe 0.62 vs. 0.77 since 1880) is in Section 3 — [AQR / Hurst et al.](https://www.TrendFollowing.com/whitepaper/Century_Evidence_Trend_Following.pdf)

### Inferences
- At daily or weekly horizons, regime-switching between risk assets and safe assets is a drawdown-control tool with Sharpe of roughly 0.6–0.8, not a high-alpha engine. Post-publication returns are clearly below backtests, and fast switching suffers in V-shaped shocks (2020, April 2025).
- Combining a slow regime layer (e.g., monthly canary or trend filter, or the sign of stock–bond correlation) with a fast intraday continuation layer (Section 1) is consistent with the evidence. The slow layer picks which destination assets are valid; the fast layer harvests same-day continuation and exits by the close. This is an inference, not a tested combination in the literature.

### Gaps
- No independent post-2018 live performance numbers for GEM or DAA were retrieved.
- No academic study of "risk appetite index" timing (e.g., Credit Suisse/UBS/GS risk-appetite indicators) with out-of-sample results was retrieved.
- Faber's 2018 paper itself was not accessed; its numbers are from Swedroe's summary.
