# Relative-Value Mean Reversion between Assets and Baskets (pairs trading, stat arb, cross-sectional short-term reversal), holding period ≤ 2 days

Scope note: the goal is to judge whether "relative overheating" between assets or baskets (for example BTC overbought vs gold oversold, or a crypto basket vs a safe-haven basket) predicts a reversal within 1 hour to 2 days. The notes cover methods, evidence by asset class, cross-sectional short-term reversal, spurious pairs and data mining, failure modes, and professional practice. Research date: October 2026. Older results are flagged for decay.

---

## 1. Methods: which ones fit 1-hour to 2-day holding periods?

### Takeaway
Every standard framework (distance, cointegration, OU/stochastic control, copula, PCA/ETF residual s-scores, ML cross-sectional ranking) can run at hourly or daily frequency. What decides whether a 1h–2d horizon is feasible is the spread's mean-reversion speed (OU half-life) compared with the holding window, plus costs per round trip. The approaches that explicitly estimate and filter on reversion speed fit this horizon best: OU/s-score models with a κ (half-life) filter and dynamic (Kalman/rolling) hedge ratios. The classic Gatev-style distance method has 6-month trading windows and was designed for much slower convergence.

### Cited Findings
**Taxonomy and the classic results**
- Krauss's survey (Journal of Economic Surveys 2017, working paper 2015) reviews more than 90 papers. It sorts them into five groups: distance, cointegration, time-series, stochastic control and "other" approaches (PCA, copula, ML) — [Krauss review, IDEAS](https://ideas.repec.org/p/zbw/iwqwdp/092015.html); [FAU working paper PDF](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- **Distance method (Gatev, Goetzmann & Rouwenhorst, GGR 2006):** annualized excess returns of up to 11% p.a. at low exposure to systematic risk, robust to data snooping in the original study. The review notes that the SSD (sum of squared distances) selection criterion "has several deficiencies, leading to low variance" spreads. The excess returns decline over time and can partly be explained by liquidity and market frictions — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- **Three-way comparison (Rad, Low & Faff 2016, Quantitative Finance), US equities 1962–2014 with time-varying costs.** Mean monthly excess returns before costs: distance 91 bp, cointegration 85 bp, copula 43 bp. After costs: 38, 33 and 5 bp. Distance and cointegration trading opportunities fell considerably from 2009, while copula trade frequency stayed stable. Cointegration did best in turbulent markets — [Bond University abstract](https://research.bond.edu.au/en/publications/the-profitability-of-pairs-trading-strategies-distance-cointegrat/). A secondary summary says performance peaked around 1990 and fell to unattractive levels after 2000, with distance and cointegration opportunities down 40% and 35% from 2007–11 to 2012–14 — [CXO Advisory](https://cxoadvisory.com/technical-trading/best-stock-pairs-trading-method) (secondary, not verified in the paper)

**Cointegration and OU (Engle-Granger, Johansen, KSS)**
- Crypto pairs studies use Engle-Granger, Kapetanios-Snell-Shin (KSS) and Johansen tests. They calibrate the OU mean-reversion speed to get the half-life, which drives both asset selection and the look-back window — [Tadi & Kortchemski 2021, arXiv](https://arxiv.org/abs/2109.10662v1)
- OU half-life is the average time for a deviation to decay by half, computed as ln(2)/κ. Hudson & Thames' ArbitrageLab exposes it as `half_life()` — [ArbitrageLab OU model docs](https://hudson-and-thames-arbitragelab.readthedocs-hosted.com/en/latest/technical/api/arbitragelab/optimal_mean_reversion/ou_model/index.html); [LuxAlgo pairs stack](https://www.luxalgo.com/library/concept/pairs-trading-stack/) (secondary)
- **Kalman-filter hedge ratio:** estimates a dynamic hedge ratio as a generalization of a rolling regression, with spread = y − β_t·x. It typically feeds a Bollinger/z-score band rule. The implementation follows E.P. Chan's "Algorithmic Trading" — [ArbitrageLab Kalman docs](https://hudson-and-thames-arbitragelab.readthedocs-hosted.com/en/latest/other_approaches/kalman_filter.html)
- **Bertram-style OU optimal thresholds on 861 energy futures spreads, 2003–2010 (Cummins & Bucca 2012).** After Romano-Wolf data-snooping controls, the top strategies earned 0.07–0.55% per day, with Sharpe ratios "often larger than two" — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)

**PCA/ETF factor-residual s-score (Avellaneda & Lee 2010)**
- Stock residuals against 15 PCA factors or sector ETFs are modelled as OU processes on a 60-day trailing window. Only residuals with κ > 252/30 = 8.4 are traded, i.e. mean-reversion time below half the estimation window (about 30 trading days). Rules: open when |s| > 1.25, close longs at s = −0.50, close shorts at s = +0.75. If κ falls below 8.4, the model is rejected and the strategy does not open trades or closes open ones. Costs are 5 bp per trade (10 bp round trip) and leverage is "2+2", targeting about 10% volatility — [Avellaneda & Lee PDF](https://www.math.nyu.edu/faculty/avellane/AvellanedaLeeStatArb20090616.pdf)
- Results after costs: PCA Sharpe 1.44 over 1997–2007 but only 0.9 over 2003–2007; ETF-factor Sharpe 1.1 over 1997–2007, with a similar decline after 2002. Volume-weighted "trading time" signals lift the ETF Sharpe to 1.51 over 2003–2007 — [Avellaneda & Lee PDF](https://www.math.nyu.edu/faculty/avellane/AvellanedaLeeStatArb20090616.pdf)
- The Krauss review warns that the results are "not robust to data mining", because the authors tried several entry and exit thresholds — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)

**Copula**
- Hourly copula-on-cointegration trading of Binance USDT-margined perpetuals, 2021-01 to 2023-01: 20 coins, BTCUSDT as reference, 3-week formation, 1-week trading, 4 bp taker fee. Best variant: 37.1% p.a., Sharpe 0.97, max drawdown −35.6%. Over the same period BTC buy-and-hold returned −17.0% p.a. (Sharpe −0.23) — [Tadi & Witzany 2023, arXiv](https://ar5iv.labs.arxiv.org/html/2305.06961)

**ML cross-sectional ranking with 1-day holding (Krauss, Do & Huck 2017, EJOR), S&P 500 1992–2015**
- The strategy goes long the top 10 and short the bottom 10 stocks for one day. The ensemble earns 0.45% per day before costs and 0.25% per day after 5 bp per half-turn — [FAU WP PDF](https://www.iwf.rw.fau.de/files/2016/03/03-2016.pdf); [IDEAS/EJOR](https://ideas.repec.org/a/eee/ejores/v259y2017i2p689-702.html)
- Decay by sub-period, after costs: 12/1992–03/2001 more than 200% p.a. (Sharpe 6.7); 04/2001–08/2008 22% p.a. (Sharpe 0.51); 09/2008–12/2009 more than 400% p.a. (Sharpe 4.5, the GFC); 2010–10/2015 negative, −14% to −25% p.a. Returns were still positive before costs — [FAU WP PDF](https://www.iwf.rw.fau.de/files/2016/03/03-2016.pdf)

**Open-to-close / close-to-open decomposition**
- Della Corte, Kosowski & Wang, US stocks 1993–2014, gross daily returns. Buying overnight losers at the open and holding intraday (CO-OC) earns 1.68% per day (Sharpe 24.16). Conventional close-to-close reversal (CC-CC) earns 0.33% per day (Sharpe 5.52). Intraday-on-intraday (OC-OC) is negative at −0.17%, i.e. momentum. Turnover is about 100% per day, and a one-minute delay in portfolio formation sharply cuts CO-OC returns — [CXO summary](https://www.cxoadvisory.com/technical-trading/overnightintraday-return-reversal-trading/)

### Inferences
- For a ≤2-day horizon, the binding constraint is that the spread's half-life must be well below the holding cap. If the cap is 2 days, the half-life should be at most about 0.5–1 day. Avellaneda & Lee's rule (half-life below half the estimation window) scales down naturally, for example a 60–120-bar hourly window that keeps only spreads with a half-life of hours.
- The GGR distance method with 12-month formation and 6-month trading is a poor template for ≤2-day trades. Hourly OU/s-score, Kalman z-score and residual-reversal-vs-basket designs (Avellaneda-Lee style: asset vs basket residual) are the natural fits.
- A "relative RSI" of BTC vs gold is functionally a z-score of a log-price ratio with a fixed 1:1 hedge. It is a special case of the distance/cointegration family, but without a test that the ratio is stationary.

### Gaps
- I could not retrieve the average trade duration and convergence times in GGR (2006) or Do & Faff, or the exact s-score holding times in Avellaneda & Lee, so there are no numbers on typical holding days for the classic methods.
- I found no peer-reviewed head-to-head comparison of methods specifically at 1h–2d holding periods across asset classes.

---

## 2. Evidence by universe (returns, Sharpe, holding, costs, sample)

### Takeaway
- **Equity pairs and stat arb:** strongly profitable before about 2000–2003, decaying sharply afterwards, and often zero or negative after costs post-2010. The exception is crisis spikes, when liquidity provision pays.
- **Commodities:** the best evidence is for economically hard-linked spreads (crack, crush, spark, energy calendar/location spreads). Gold/silver failed.
- **FX, government bonds, cross-asset pairs:** almost no rigorous net-of-cost evidence at ≤2-day horizons.
- **Crypto:** intraday mean reversion is real but tiny and is mostly eaten by costs. Daily pairs show little. Hourly perp pair strategies show Sharpe ratios around 1 in short samples with high drawdowns.

### Cited Findings
**Equities (single-stock pairs and stat arb)**
- Do & Faff (2010, FAJ) extend GGR to 2009. Profitability keeps declining, mainly because more pairs fail to converge. Under GGR's baseline method, trading costs make pairs trading largely unprofitable. The best portfolios, combining same-industry matching (48 Fama-French industries), many zero-crossings and low SSD, stay slightly profitable after costs. But Do & Faff (2012) tested 29 selection variants, which raises data-snooping risk — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf); [CFA Institute FAJ listing](https://rpc.cfainstitute.org/research/financial-analysts-journal/2010/does-simple-pairs-trading-still-work)
- Do & Faff (2010) also find that pairs trading performed well in turbulent markets, including the GFC — [CFA Institute FAJ listing](https://rpc.cfainstitute.org/research/financial-analysts-journal/2010/does-simple-pairs-trading-still-work)
- **Hourly equity pairs, FTSE 100, 2007 (Bowen et al. 2010):** 264-hour formation and 132-hour trading windows, about 20% p.a. excess return. Costs of 15 bp plus a 60-minute execution delay eliminate the excess return completely — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- **High-frequency US equity pairs (Stübinger & Bredthauer):** the best variant reportedly earns about 50% p.a. with a Sharpe of about 8.1 after costs. Most variants show declining returns over time — [ResearchGate listing](https://www.researchgate.net/publication/338969525_Statistical_arbitrage_pairs_trading_with_high-frequency_data) (abstract-level; treat with caution)
- **REIT pairs (Mori & Ziobrowski 2011):** more profitable than common-stock pairs thanks to industry homogeneity, but the advantage disappears after 2000 — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- **Lehmann-style daily contrarian on S&P 1500 (Khandani & Lo):** average returns before 2002 are all above the full-sample average and those from 2002 on are below it. The cause cited is competition and technology — [Khandani & Lo 2008, NBER w14465](https://nber.org/system/files/working_papers/w14465/w14465.pdf). The average daily return fell to a low of 0.13% in 2006, and managers added leverage in response — [Khandani & Lo 2007 (NY Fed conference version)](https://www.newyorkfed.org/medialibrary/media/research/conference/2007/liquidity/Khandani_Lo.pdf) (figure via search summary of this paper)

**ETFs and sector baskets**
- Avellaneda & Lee's ETF-residual approach is the key evidence (Sharpe 1.1 over 1997–2007, lower after 2002) — [Avellaneda & Lee PDF](https://www.math.nyu.edu/faculty/avellane/AvellanedaLeeStatArb20090616.pdf)
- Galenko et al. (2012) applied multivariate cointegration to index ETFs and outperformed the benchmark, but with "extensive data mining" (daily and weekly data, several formation lengths, nine lag parameters) and no significance tests — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- **Contrast:** the S&P 500 ETF shows intraday *momentum*. The first half-hour return (from the prior close) predicts the last half-hour return, 1993–2013. The effect also holds for 10 other actively traded domestic and international ETFs — [Gao, Han, Li & Zhou, JFE 2018](https://profiles.wustl.edu/en/publications/market-intraday-momentum/); [Alpha Architect summary](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/)

**Commodities**
- GGR distance pairs on commodity futures, 1990–2008 (Bianchi, Drew & Zhu 2009): statistically and economically significant excess returns with low systematic exposure — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- **Crack spread, crude vs gasoline/heating oil, 1983–1994 (Girma & Paulson 1999):** stationary spread, more than 15% average annual return after USD 100 per round-turn costs, using 5–10-day moving-average bands. The review stresses the "clear fundamental reason" for the cointegration. Later work (Dunis et al. 2006; Cummins & Bucca 2012) confirms profit potential. The crush spread (soybeans vs products) and spark spread (gas vs power) were also positive — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- **Gold–silver spread (Wahab & Cohn 1994):** trading "unsuccessful" — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- **WTI vs a Brent+Dubai replication portfolio (cointegration), 2000–2005:** reports empirical evidence of statistical arbitrage in crude oil markets, at daily frequency — [MDPI Risks 2024](https://www.mdpi.com/2227-9091/12/7/106)
- **Naphtha crack (naphtha vs Brent), 2014–2024:** studies mean reversion after large daily moves, with costs included in the backtests — [Energy Economics 2025](https://www.sciencedirect.com/science/article/pii/S0140988325004475) (numbers not retrieved)
- **Intraday pairs on Chinese futures** (cointegration + Kalman + Hurst filter): 81% cumulative in-sample and 21% out-of-sample after costs — [ScienceDirect 2023](https://www.sciencedirect.com/science/article/pii/S2444569X23001257) (sample and benchmark not verified)

**Currencies**
- I found no rigorous peer-reviewed net-of-cost study of intraday or daily FX pairs/cointegration trading. Search results were practitioner pieces only (see Gaps).
- Weekly currency returns: 63 developed and emerging currencies, 1–4-week look-back and holding periods. The result is strong cross-sectional *momentum*, not reversal, and it is weakest when volatility is high — [Raza 2015 thesis, Massey](https://mro.massey.ac.nz/handle/10179/7266); [CXO summary of Raza, Marshall & Visaltanachoti](https://www.cxoadvisory.com/?p=23285)

**Government bonds and rates**
- Intraday interest-rate spread trading is studied by Dunis & Lequeux (2010), "Intraday data and hedging efficiency in interest spread trading", cited in the Krauss review's references — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf). Numbers not retrieved.
- Overnight-intraday reversal is present in interest-rate futures but much weaker than in single stocks (see Section 3) — [CXO summary of Della Corte et al.](https://www.cxoadvisory.com/technical-trading/overnightintraday-return-reversal-trading/)

**Cross-asset pairs (equity vs bond, gold vs equity, BTC vs gold)**
- I found no academic backtest of short-horizon mean reversion in cross-asset pairs such as BTC/gold or Nasdaq/Bund.
- The stock-bond correlation is regime-dependent. The 36-month correlation averaged −0.37 over 2011–2021 and +0.41 after 2022 — [State Street, Oct 2025](https://www.ssga.com/library-content/assets/pdf/global/wmu/2025/mom-20251003.pdf). It averaged about −11.5% under accommodative and +28.1% under restrictive monetary policy (Baele & Van Holle) — [Swedroe summary](https://www.evidenceinvestor.com/?p=21662)
- BTC–gold correlation rose somewhat in H2 2022 but nearly always stayed below BTC's correlation with equities, then broke down again — [Deribit Insights](https://insights.deribit.com/?p=54429) (industry note). Bitcoin's price is highly sensitive to time-varying correlations with stocks — [Yae & Tian, NUS AIDF](https://aidf.nus.edu.sg/wp-content/uploads/2022/11/Volatile-Safe-Haven-Asset-James.pdf)

**Crypto**
- **Fil & Kristoufek (2020, IEEE Access):** distance and cointegration methods on 26 liquid Binance coins at 5-minute, 1-hour and daily frequencies. The daily distance method returns −0.07% per month; at 5-minute frequency it returns 11.61% per month. Strategies underperform classical benchmarks overall, and results are highly sensitive to parameters, transaction costs and execution windows. Simple mean reversion appears in intraday prices but is missing in daily data — [IEEE Xplore](https://ieeexplore.ieee.org/document/9200323)
- **Kitron & Wengrowicz (arXiv, Aug 2026):** 183 Binance USDT pairs vs 187 US stocks/ETFs, 15-minute bars, 2025-01 to 2026-02, with a holdout to 2026-08. Next-bar sign reversal is FDR-significant in 90% of crypto pairs vs 2.7% of stocks. Mean AUC is 0.531 for crypto vs 0.499 for stocks. The signal "decays monotonically and is gone by four hours" and concentrates after aggressive taker-flow moves. In the 2026 holdout the edge attenuates but 60% of pairs stay significant, and BTC shows "a mild downward drift" per year. The gross edge peaks near 1.3 bp per trade against a ≥5 bp maker and 10–20 bp taker round trip, so the authors judge it "not exploitable under benchmark spot-cost assumptions". US funds that track crypto or metal NAVs inherit the underlying's reversal, while merely correlated controls show none (0 of 5) — [arXiv 2608.21888](https://arxiv.org/html/2608.21888v1)
- **Tadi & Witzany (2023):** hourly Binance perps, 2021–2023, results as in Section 1. Costs consumed 11.7% to 47.7% of gross P&L depending on the entry threshold. Sharpe ratio across variants ranged 0.16–0.97 — [arXiv 2305.06961](https://ar5iv.labs.arxiv.org/html/2305.06961)
- **Tadi & Kortchemski (2021):** dynamic cointegration on minute data (Bitmex) beats buy-and-hold. But the authors themselves state that "ignoring the transaction costs and having a bias selection make this paper's profitability results unreliable" — [arXiv 2109.10662](https://arxiv.org/abs/2109.10662v1)
- **Leung & Nguyen (2019):** Johansen/Engle-Granger portfolio of BTC, ETH, BCH and LTC. Strategies with stop-loss constraints were profitable in several configurations — [IDEAS](https://ideas.repec.org/a/eme/sefpps/sef-08-2018-0264.html). A later study reports their entry/exit at 1.5 standard deviations and that stop-losses reduced profit — [arXiv 2109.10662](https://arxiv.org/pdf/2109.10662v1)

### Inferences
- Across asset classes, surviving relative-value evidence clusters in spreads with a physical or contractual link (refining margins, ETF/NAV vs underlying, energy calendar/location spreads). Statistically selected pairs without such a link (gold/silver; many equity pairs after 2000) have decayed or failed.
- For crypto, the literature implies that reversal exists at minutes to hours but is below retail cost hurdles on spot. Pair strategies on perps with maker fees are the only configuration with published net Sharpe ratios near 1, and those samples are short (about 2 years) with drawdowns of 35–45%.

### Gaps
- FX pairs and crosses: I found no rigorous intraday or daily net-of-cost study, only practitioner material (e.g. [QuantInsti](https://blog.quantinsti.com/statistical-arbitrage/)). This needs a targeted SSRN/JIMF search.
- Government bond spreads (e.g. Bund–BTP, curve trades at ≤2 days): no numbers retrieved.
- Brent/WTI intraday and gold/silver post-2015: no recent peer-reviewed intraday evidence found.
- Country index futures pairs: no direct ≤2-day pairs study found. Only monthly alpha-momentum/reversal evidence (Section 3).
- Funding costs for crypto perps in pair strategies: no study found that explicitly models funding payments out-of-sample in pairs trading.

---

## 3. Cross-sectional short-term reversal (1 day to 1 week) in futures, FX, commodities, country indices and crypto vs momentum

### Takeaway
- **Single assets within a homogeneous group** (individual stocks within an industry, illiquid altcoins) show short-term reversal, consistent with liquidity provision. **Baskets and macro assets** (industries, country indices, currencies, commodities, large-cap coins, the market index intraday) mostly show short-term *momentum* or no reversal at 1 day to 1 week.
- The one robust cross-asset reversal pattern is overnight → intraday (close-to-open moves reversing open-to-close). It is much weaker in futures than in stocks and very latency-sensitive.

### Cited Findings
- **Weekly reversal in 24 US futures, 1983–2000 (Wang & Yu 2004):** going long high-volume/low-open-interest losers and short winners earns 0.57% per week gross (about 29.6% p.a. arithmetic), volatility about 31%, Sharpe 0.82, max drawdown −58.65%. Profits vanish at costs of about 0.16% per dollar traded. This is in-sample with no out-of-sample evidence — [Quantpedia](https://quantpedia.com/strategies/short-term-reversal-with-futures); [ResearchGate (paper)](https://www.researchgate.net/publication/222566966_Trading_activity_and_price_reversals_in_futures_markets)
- **Commodities, mostly no reversal:** Miffre & Rallis (2007) and Bianchi et al. (2015) find reversal strategies consistently unprofitable while momentum is often profitable. A study of 19 commodity futures over 1979–2017 finds no significant reversal profit — [White Rose eprint](https://eprints.whiterose.ac.uk/id/eprint/159905/3/Do%20momentum%20and%20reversal%20strategies%20work%20in%20commodity%20futures%20A%20comprehensive%20study%20ACCEPTED%20VERSION.pdf) (via search summary)
- "Strong short-term momentum, instead of short-term reversal, is observed in commodity futures markets" — [EFMA 2017 paper](https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2017-Athens/papers/EFMA2017_0556_fullpaper.pdf) (via search snippet; full text not retrieved)
- **Splitting commodity weekly returns (Zhao, Ding, Yu & Kang):** the component driven by speculators' net flows predicts next-week returns negatively (reversal), while the remainder predicts them positively (momentum) — [SSRN 6425598](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6425598) (via search snippet)
- **Overnight-intraday reversal "everywhere" (Della Corte, Kosowski & Wang):** in futures from July 1982 to December 2014 (equity index, interest rate, commodity, currency), the pattern is "generally consistent, though much weaker" than in stocks. Per-asset-class numbers are only in a chart. Results are gross, with about 100% daily turnover — [CXO summary](https://www.cxoadvisory.com/technical-trading/overnightintraday-return-reversal-trading/). The abstract says CO-OC beats conventional reversal for international equities and for futures on indices, rates, commodities and currencies. A search snippet of the paper says commodities show "a clear signal of daily momentum" in conventional terms — [CICF paper PDF](https://www.cicfconf.org/sites/default/files/paper_357.pdf) (could not be fetched; snippet-level)
- **Currencies (weekly):** cross-sectional momentum, not reversal, over 1–4-week horizons — [Raza thesis](https://mro.massey.ac.nz/handle/10179/7266)
- **Industries vs stocks:** industry momentum explains much of individual-stock momentum (Moskowitz & Grinblatt 1999) — [IDEAS/JF](https://ideas.repec.org/a/bla/jfinan/v54y1999i4p1249-1290.html). Winner industries outperform loser industries the next month, so the across-industry component of the 1-month reversal is negative and the stock-level reversal comes from within-industry moves — [NY Fed Staff Report 513](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr513.html)
- **Country and industry indices** (51 markets, 1973–2018): short-term past alphas *positively* predict returns (alpha momentum), while long-term alphas predict reversal — [Zaremba, Umutlu & Karathanasopoulos 2019](https://napier-repository.worktribe.com/output/3011105/alpha-momentum-and-alpha-reversal-in-country-and-industry-equity-indexes). Combining them gives monthly three-factor alphas of 1.16% (countries) and 1.44% (industries) — [Opposites Attract](https://napier-repository.worktribe.com/output/3011146/opposites-attract-combining-alpha-momentum-and-alpha-reversal-in-international-equity-markets). Monthly horizon, not ≤2 days.
- **Index intraday:** market intraday momentum in SPY and 10 other ETFs — [Gao et al. JFE 2018](https://profiles.wustl.edu/en/publications/market-intraday-momentum/)
- **Crypto daily cross-section** (more than 3,600 coins, IRFA 2021): low prior-day-return coins beat high prior-day-return coins, driven by illiquidity. The few largest and most tradeable coins show daily *momentum* instead — [Zaremba et al. 2021, IDEAS](https://ideas.repec.org/a/eee/finana/v78y2021ics1057521921002349.html); [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1057521921002349)
- A four-factor crypto model (1,160 coins, 2014–2022) reports a notable short-term reversal effect alongside size and illiquidity premia — [China Accounting & Finance Review](https://www.emerald.com/cafr/article/27/4/493/1271913/Unravelling-cross-sectional-patterns-in)
- The daily cross-sectional crypto literature attributes reversal to liquidity provision, with the premium concentrated in small, illiquid pairs — [Kitron & Wengrowicz 2026](https://arxiv.org/html/2608.21888v1)

### Inferences
- The user's idea of fading a whole asset class or basket that is overheated relative to another basket targets exactly the level where the evidence points to short-term momentum (industries, countries, currencies, commodities, large-cap crypto). Reversal appears mainly for idiosyncratic, liquidity-driven dislocations of single constituents relative to their own group.
- A basket-vs-basket fade (crypto basket vs safe-haven basket) therefore has weak prior support. A constituent-vs-own-basket residual fade (e.g. an altcoin vs a crypto-sector basket, or a single commodity vs its complex) is closer to where reversal has been documented, though it is often illiquidity-driven and cost-sensitive.

### Gaps
- No net-of-cost, post-2015 study of weekly or daily cross-sectional reversal in liquid futures (equity index, bond, FX, commodity) was found. The Della Corte futures numbers per asset class were not retrievable.
- I found no explicit study of cross-asset cross-sectional reversal pooling different asset classes (equities, bonds, commodities, FX, crypto) at 1-day horizons.

---

## 4. Do economically unrelated pairs mean-revert at short horizons? Spurious pairs and data mining

### Takeaway
The evidence favours economically or mechanically linked pairs. Industry homogeneity, shared fundamentals and NAV/contract links improve stability and convergence. Unrelated pairs selected by price statistics alone are prone to spurious cointegration and non-convergence. A direct 2026 test found that correlated but non-linked instruments did *not* inherit short-term reversal. Any search across many asset-pair combinations must be deflated for multiple testing (Deflated Sharpe Ratio, a t-stat hurdle of about 3).

### Cited Findings
- **Linkage helps:** restricting pairs to the same Fama-French industry "has a potential to identify more meaningful pairs and to reduce spurious correlations" (Do & Faff). The REIT advantage came from industry homogeneity leading to "more stable pairs with clear, long-term relationships" — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- The crack spread works because of a "clear fundamental reason for the cointegration relationship". Gold-silver trading failed — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- Chen et al. (2012) find pairs selected on common-factor correlation earn much higher excess returns than pairs selected on residual correlation — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- Declining profits mainly reflect a rising share of non-converging pairs — [Krauss review on Do & Faff](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- **Direct test of mechanical vs mere correlation (crypto/metals, 15-minute):** US funds whose NAV tracks crypto or metal prices inherit the underlying's reversal (Bitcoin family: underlying AUC 0.524 vs wrapper 0.523). Correlated but non-NAV-linked controls show nothing (0 of 5 significant) — [Kitron & Wengrowicz 2026](https://arxiv.org/html/2608.21888v1)
- Correlation is not cointegration. Correlated assets may not be cointegrated, and cointegration can break with structural shifts — [Amberdata blog](https://blog.amberdata.io/crypto-pairs-trading-why-cointegration-beats-correlation) (practitioner)
- **BTC vs gold:** the correlation is weak and regime-dependent, below BTC's correlation with equities, and broke down after H2 2022 — [Deribit Insights](https://insights.deribit.com/?p=54429)
- **Stock–bond:** the sign flipped in 2022, from −0.37 (2011–2021) to +0.41 (post-2022, 36-month) — [SSGA](https://www.ssga.com/library-content/assets/pdf/global/wmu/2025/mom-20251003.pdf); [Franklin Templeton/Brandywine](https://www.franklintempleton.com/articles/2023/brandywine-global/deconstructing-the-dynamic-duo-of-stocks-and-bonds)
- **Data mining:** Do & Faff (2012) test 29 selection combinations, raising data-snooping risk. Galenko et al. (2012) ETF results come from "extensive data mining exercises". Avellaneda & Lee are "not robust to data mining". The review recommends Romano-Wolf style controls as in Cummins & Bucca — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
- **Deflated Sharpe Ratio** (Bailey & López de Prado 2014, JPM) corrects for selection bias under multiple testing and for non-normal returns. It uses the number of trials, their effective independence, the variance of the trial Sharpe ratios, and sample length — [SSRN 2460551](https://papers.ssrn.com/abstract=2460551); [Wikipedia](https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio). A common practitioner convention treats DSR < 0.95 as a possible fluke — [endgame-ml docs](https://endgame-ml.readthedocs.io/en/latest/_modules/endgame/utils/sharpe.html) (convention, not a formal rule)
- **Harvey, Liu & Zhu (RFS 2016):** a new factor should clear a t-ratio of about 3.0 rather than 2.0, given more than 300 factors tested. "Most claimed research findings in financial economics are likely false" — [NBER w20592](https://nber.org/papers/w20592); [SSRN](https://papers.ssrn.com/abstract=2513152)
- Kitron & Wengrowicz used a walk-forward out-of-sample design, a moving-block bootstrap and Benjamini-Hochberg FDR at q = 0.05, and still found the crypto edge uneconomic after costs — [arXiv 2608.21888](https://arxiv.org/html/2608.21888v1)

### Inferences
- BTC vs gold and Nasdaq vs Bunds have no contractual or fundamental anchor, and their correlations change sign across regimes. A z-score extreme in such a ratio is more likely a trend in a common driver (risk-on/off, real yields, inflation regime) than a temporary liquidity dislocation. The literature does not support expecting reliable reversal within ≤2 days.
- Testing N assets pairwise gives N(N−1)/2 pairs: 30 assets give 435 pairs, before also varying windows, thresholds and holding caps. The DSR or an FDR procedure is essential, and the effective number of trials should include every parameter variant tried.

### Gaps
- I found no peer-reviewed study that directly compares short-horizon reversal of economically unrelated cross-asset pairs (e.g. BTC/gold, equity index/bond future) against linked pairs. The Kitron & Wengrowicz NAV-linked vs correlated control is the closest direct evidence, and it is small (5 controls).

---

## 5. Failure modes and risk controls

### Takeaway
The main ways these strategies fail:
- **Non-convergence and divergence:** structural breaks.
- **Crowded unwinds:** 2007, and repeated quant drawdowns in 2025–26.
- **Correlation-regime flips:** stock–bond in 2022.
- **Leverage:** turns small, steady edges into large losses.
- **Costs and latency:** wipe out intraday edges.

Short-horizon liquidity-providing strategies lose during forced deleveraging (prices trend intraday and for days), then earn outsized returns once liquidity returns. Survival depends on capital and leverage discipline as much as on the signal. Common practitioner controls are z-score stops, time stops, model-validity stops (re-estimated half-life or κ outside the allowed range) and leverage caps. Evidence suggests stop-losses often cut profits.

### Cited Findings
- **Quant quake, August 2007:** losses at quant long/short funds from August 6 to 9, starting with July deleveraging, followed by a temporary withdrawal of market-making capital from August 8 — [Khandani & Lo 2008, NBER](https://nber.org/system/files/working_papers/w14465/w14465.pdf)
- A 5-minute contrarian strategy (5–60-minute holds) turned sharply negative in the week of August 6, with larger losses for longer holding periods. A daily contrarian portfolio built on August 6 lost 1.47% by the close on August 7 and 1.75% by August 9. It then rebounded from August 10 for a +3.44% cumulative 5-day profit. Five-day positions opened on August 8 and 9 earned 8.20% and 8.96% unleveraged — [Khandani & Lo 2008](https://nber.org/system/files/working_papers/w14465/w14465.pdf)
- Leverage of 4:1 to 10:1 was common, the highest in high-frequency mean-reversion strategies. An 8:1-levered price-momentum factor portfolio lost about 31% in two days (August 8–9) — [Khandani & Lo 2008](https://nber.org/system/files/working_papers/w14465/w14465.pdf)
- Fund-level losses reported by the WSJ and cited in the paper: Highbridge Statistical Opportunities −18% month-to-date by August 8; Goldman Sachs Global Equity Opportunities lost more than 30% in a week — [Khandani & Lo 2008](https://nber.org/system/files/working_papers/w14465/w14465.pdf)
- **Crowding mechanism:** as AUM in long/short equity and market-neutral strategies grew, average contrarian returns fell (to 0.13% per day in 2006), so managers raised leverage — [Khandani & Lo 2007](https://www.newyorkfed.org/medialibrary/media/research/conference/2007/liquidity/Khandani_Lo.pdf) (via search summary)
- **Summer 2025 quant "wobble"** (June 1 to July 25, 2025): quant equity managers lost about 4.2% (Goldman Sachs prime-brokerage estimate) while US equities rose about 8%. The beta factor ran about +2.5% per month and cumulative factor returns were "nearly double or more" the risk-model forecasts. Heavily shorted, high-residual-volatility names lost more than linear models predicted. Tail residual correlations fell, which MSCI reads as a partial crowded unwind — [MSCI blog, Oct 2025](https://www.msci.com/research-and-insights/blog-post/unraveling-summer-2025s-quant-fund-wobble)
- **January 2026:** US quant funds reportedly fell about 2.8% in the first two weeks (UBS estimate), tied to crowded trades and short squeezes in lower-quality stocks — [Crypto Briefing](https://cryptobriefing.com/quant-funds-worst-trading-rout-january-2026/); [Hedgeweek](https://hedgeweek.com/news/quant-hedge-funds-see-worst-drawdown-since-october-as-crowded-trades-unwind) (secondary press)
- **Crises as opportunity:** liquidity-providing long/short strategies did very well in the GFC (Krauss-Do-Huck ensemble: more than 400% p.a. after costs, Sharpe 4.5, 09/2008–12/2009) — [Krauss, Do & Huck WP](https://www.iwf.rw.fau.de/files/2016/03/03-2016.pdf). Do & Faff report robustness in turbulent markets — [FAJ listing](https://rpc.cfainstitute.org/research/financial-analysts-journal/2010/does-simple-pairs-trading-still-work)
- **Regime shifts in correlation:** the 2022 stock–bond flip coincided with inflation and restrictive policy — [Swedroe/Baele & Van Holle](https://www.evidenceinvestor.com/?p=21662); [SSGA](https://www.ssga.com/library-content/assets/pdf/global/wmu/2025/mom-20251003.pdf)
- **Costs and latency:**
  - FTSE hourly pairs lose their full excess return with 15 bp costs plus a 60-minute delay — [Krauss review](https://www.iwf.rw.fau.de/files/2016/03/09-2015.pdf)
  - A one-minute delay sharply reduces CO-OC reversal returns — [CXO](https://www.cxoadvisory.com/technical-trading/overnightintraday-return-reversal-trading/)
  - The 15-minute crypto reversal earns 1.3 bp gross vs a ≥5 bp round trip — [Kitron & Wengrowicz](https://arxiv.org/html/2608.21888v1)
  - Hourly crypto perp pairs lose 12–48% of gross P&L to fees — [Tadi & Witzany](https://ar5iv.labs.arxiv.org/html/2305.06961)
- **Model-validity stop:** Avellaneda & Lee re-estimate daily. When κ falls below 8.4 (half-life too long) they do not open trades, or they close open trades — [Avellaneda & Lee](https://www.math.nyu.edu/faculty/avellane/AvellanedaLeeStatArb20090616.pdf)
- **Stop-losses:** stop-loss constraints were part of the profitable configurations in Leung & Nguyen's crypto portfolios — [IDEAS](https://ideas.repec.org/a/eme/sefpps/sef-08-2018-0264.html). A later study reports that stop-loss rules reduced profit — [arXiv 2109.10662](https://arxiv.org/pdf/2109.10662v1)
- **Practitioner cautions:** hedge ratios drift, half-lives lengthen, and a spread that tested stationary can trend further than a position can survive — [LuxAlgo](https://www.luxalgo.com/library/concept/pairs-trading-stack/) (secondary)

### Inferences
- The 2007 episode shows a mean-reversion trader's dilemma. Stopping out at the worst point locks in losses that would have reverted within 2–5 days, but leverage and margin calls force exactly that. For a retail ≤2-day strategy, a hard time stop at 2 days plus small, unlevered or lightly levered size per spread is safer than tight z-score stops.
- Overlapping trades that share a leg (BTC short vs gold, BTC short vs bonds) concentrate exposure in the shared leg. In a BTC trend move they all lose together, so position limits should be set per net asset exposure, not per pair.

### Gaps
- No quantitative studies were found comparing z-score stop levels vs time stops for ≤2-day holds across asset classes.
- No public data was found on 2020 (COVID) or 2022 drawdowns of short-horizon cross-asset relative-value strategies specifically.

---

## 6. How professionals run these strategies today and what is realistic for retail (hourly/daily)

### Takeaway
Professional stat arb runs diversified books of hundreds to thousands of weakly correlated short-horizon signals:
- Holding periods of roughly 0.6–6.4 days, with turnover not significantly related to returns.
- Leverage 4–10x historically, with factor-neutral risk models and crowding monitors.
- Per-trade costs of a few bp, plus latency in minutes or less for intraday decomposition effects.

Published edges at hourly or daily frequency are a few bp to tens of bp per trade before costs and have decayed since the early 2000s. What a retail trader can realistically still exploit:
- Linked spreads (refining/calendar/location spreads, ETF vs underlying, coin vs coin within a sector on perps with maker fees).
- Liquidity-provision moments after large dislocations.

Cross-asset "overheating" fades between unrelated baskets have little support.

### Cited Findings
- **101 real-world "alphas" (WorldQuant, Kakushadze 2016):** average holding period about 0.6–6.4 days, mean pairwise correlation 15.9%. Returns correlate strongly with volatility and show no significant dependence on turnover — [arXiv 1601.00991](https://arxiv.org/abs/1601.00991)
- An empirical study of 4,000 real US equity portfolios finds no statistically significant dependence of return on turnover (Kakushadze & Tulchinsky) — [arXiv 1509.08110](https://arxiv.org/pdf/1509.08110v2.pdf) (via search summary)
- Academic stat-arb setups assume 5 bp per trade (10 bp round trip) and 2+2 leverage at about 10% volatility (Avellaneda & Lee) — [PDF](https://www.math.nyu.edu/faculty/avellane/AvellanedaLeeStatArb20090616.pdf). Krauss-Do-Huck assume 5 bp per half-turn — [WP](https://www.iwf.rw.fau.de/files/2016/03/03-2016.pdf)
- Historical leverage of 4:1–10:1, the highest for high-frequency mean reversion — [Khandani & Lo](https://nber.org/system/files/working_papers/w14465/w14465.pdf)
- Crowding is monitored, for example by MSCI's Factor Crowding Score (residual correlation pillar), and MSCI advises watching nonlinear factor interactions — [MSCI](https://www.msci.com/research-and-insights/blog-post/unraveling-summer-2025s-quant-fund-wobble)
- Practitioner descriptions put stat-arb holding periods at hours to weeks and most signal half-lives at 1–5 days. One rule of thumb says capacity tops out around USD 1–5bn — [Quantt guide](https://www.quantt.co.uk/resources/statistical-arbitrage-guide) (low-quality/unsourced; directional only)
- For the 15-minute crypto reversal, "sophisticated participants with cheaper cost structures could capture part" of an edge that is uneconomic at retail spot fees — [Kitron & Wengrowicz](https://arxiv.org/html/2608.21888v1)
- After 2010, a publicly reproducible daily ML stat-arb strategy on the S&P 500 lost 14–25% p.a. after costs, despite positive pre-cost returns. The authors surmise profits were arbitraged away as tools became widely available — [Krauss, Do & Huck WP](https://www.iwf.rw.fau.de/files/2016/03/03-2016.pdf)
- Crypto perpetuals are about 93% of crypto futures volume. Deviations from no-arbitrage perp prices are larger in crypto than in traditional currency markets — [ResearchGate preprint on funding markets](https://www.researchgate.net/publication/399936354_The_Two-Tiered_Structure_of_Cryptocurrency_Funding_Rate_Markets); [Fundamentals of Perpetual Futures, arXiv](https://arxiv.org/html/2212.06888v7)
- Hourly perp pairs with 4 bp taker fees achieved Sharpe up to 0.97 in 2021–2023 with 200k USDT capital, 176–254 trades over about 2 years, and drawdowns of 34–44% — [Tadi & Witzany](https://ar5iv.labs.arxiv.org/html/2305.06961)

### Inferences
- **Realistic retail niche (50–250k EUR, IBKR + crypto perps, hourly/daily):**
  1. Linked spreads with fundamental anchors: crack/calendar/location energy spreads, which can trade as exchange-recognized spread contracts with lower margin and fewer legging costs.
  2. Residual reversal of one constituent against its own basket (altcoin vs crypto-sector basket; single commodity vs its complex), not basket vs basket across asset classes.
  3. Entering only after large dislocations, i.e. conditioning on volatility or dislocation size, where the liquidity premium is largest, while keeping capital to survive a 2007-style multi-day trend.
- **Hurdles:**
  - Round-trip costs of about 5–20 bp per leg-pair on crypto spot or CFD spreads.
  - Overnight financing on CFDs.
  - Perp funding.
  - The 2-day cap, which forces exits before slower reversion completes.
- **Testing design for the user's own backtests:**
  - Pre-register a small universe of linked pairs and baskets.
  - Compute half-lives on rolling windows and trade only when the half-life is below about 0.5 of the holding cap.
  - Use walk-forward selection.
  - Report DSR/FDR-adjusted results.
  - Compare against the null of momentum at the basket level, since prior evidence says baskets trend at short horizons.

### Gaps
- I found no authoritative public numbers on current (2024–2026) professional stat-arb turnover, capacity or latency from Man, AQR or Two Sigma research. The capacity figures above come from low-quality practitioner sources.
- I found no study quantifying retail-achievable net returns for cross-asset pairs at IBKR-level costs (futures commissions, CFD spreads and financing) at ≤2-day horizons.
