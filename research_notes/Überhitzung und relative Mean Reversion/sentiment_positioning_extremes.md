# Sentiment, Positioning & Leverage Extremes as "Overheated / Undercooled" Signals — Short-Horizon (1h–2d) Reversal Evidence Across Asset Classes

Scope note (read first): Every claim below carries a URL. Items marked **[OWN CALC]** are quick in-sample computations I ran on free primary data (sources linked). They are naive (no costs, no out-of-sample split beyond a two-period comparison, crude overlap adjustment of t-stats: t_adj = (mean_bucket − mean_all)/(sd_bucket/√(n·8h/h))). Treat them as descriptive sanity checks, not as tradable evidence. Items marked **[SECONDARY]** come from press or vendor reposts of proprietary research and were not verifiable against the original. "Decay" means the effect is reported weaker in recent subsamples.

---

## 1. Crypto leverage/sentiment (funding, OI, basis, long/short ratios, liquidations, Coinbase premium, stablecoins, Fear & Greed, 25Δ RR, DVOL): which predict next-hours/next-day returns or reversals?

### Takeaway
I found no peer-reviewed paper showing that any single crypto positioning or sentiment gauge reliably predicts BTC/ETH reversals within ≤2 days out of sample. The robust academic findings are slower. High carry/basis predicts crashes and liquidations (BIS), and perp–spot deviations mean-revert, which supports an arbitrage strategy rather than a directional one. My own check on free Binance data finds a squeeze-type effect: very negative funding was followed by positive 8–48h BTC returns in 2020–22 (t≈2), but the effect largely disappeared in 2023–26. Extreme positive funding and "Extreme Greed" showed no reliable short-horizon reversal.

### Cited Findings
**Funding rate / futures basis ("carry")**
- BIS WP 1087 (Schmeling, Schrimpf, Todorov, Apr 2023): crypto carry (the futures–spot basis) averages "above 10% annually" and reaches "up to 60% p.a.". It is driven by a volatile convenience yield from trend-chasing small investors seeking leveraged upside, against scarce arbitrage capital. Interest-rate differentials explain very little. **"High carry predicts future price crashes"**, and rising carry coincides with rising prices of crash insurance. Arbitrage is risky because margins spike and positions get liquidated in drawdowns. — [BIS WP 1087](https://www.bis.org/publ/work1087.pdf). *Caveat: I could only access the abstract and landing page, not the regression horizons or coefficients.*
- He, Manela, Ross, von Wachter, "Fundamentals of Perpetual Futures" (hourly Binance data, Jan 2020–Mar 2024; BTC, ETH, BNB, DOGE, ADA): the mean absolute perp–spot deviation is about 60–90% p.a. The mean deviation is near zero, and deviations shrink about 11% per year. Past 120-day spot returns are positively and significantly related to the deviation, which the authors read as extrapolative or sentiment-driven futures demand. A convergence arbitrage (enter when the deviation exceeds the cost bound, exit at zero) earns Sharpe ratios of 1.80 for BTC (high-fee tier), 2.55 for ETH, 4.84 for BNB, and 3.53 for BTC with no fees. For BTC, 8.64 pp of the 13.70% return comes from price convergence and 5.06 pp from funding. **The paper does not test whether deviations predict spot returns.** — [arXiv 2212.06888v5](https://arxiv.org/html/2212.06888v5)
- The funding rate itself is persistent and forecastable: double-autoregressive models beat a no-change forecast for the next-period BTC funding rate on Binance and Bybit. — [Inan, SSRN 5576424](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5576424)
- An older practitioner regression of 8-hour BTC returns on BitMEX funding found R² = 0.003 (essentially no predictive power). — [Fulgur Ventures, Medium](https://medium.com/@fulgur.ventures/bitcoin-funding-rates-and-price-predictability-27ce95535af1)
- Funding was positive in more than 92% of Q3 2025 periods. BitMEX describes the formula's built-in positive anchor (interest component) as structural, so "high funding" must be defined relative to the 0.01%/8h baseline, not relative to zero. — [BitMEX Q3 2025 derivatives report](https://testnet.bitmex.com/blog/2025q3-derivatives-report)
- A cross-sectional seven-factor crypto model includes a "funding sentiment" factor and reports regime-dependent premia: reversal earns most in fearful markets. — [Babayev & Aliyev, SSRN 6818558](https://papers.ssrn.com/sol3/Delivery.cfm/6818558.pdf?abstractid=6818558&mirid=1)
- **[OWN CALC]** Binance BTCUSDT 8h funding (7,395 observations, Jan 2020–Sep 2026) against forward BTC log returns measured from the funding timestamp. Data: [Binance fundingRate monthly files](https://data.binance.vision/?prefix=data/futures/um/monthly/fundingRate/BTCUSDT/) and [8h klines](https://data.binance.vision/?prefix=data/futures/um/monthly/klines/BTCUSDT/8h/).
  - Full sample. Unconditional mean: +0.033% (8h), +0.099% (24h), +0.199% (48h). After funding at or below the 10th percentile (≈ −0.002%/8h): +0.22% (8h, t_adj≈2.2), +0.60% (24h, t≈2.2), +0.97% (48h, t≈1.9). After funding at or above the 95th percentile (≈ +0.046%/8h): −0.04% / −0.11% / −0.19% (all t≈−0.5). Correlation of funding with the forward 24h return: −0.04.
  - 2020–2022. Funding ≤ p5: +0.57% (8h), +1.61% (24h), +2.58% (48h), t≈2.0–2.2. Funding ≥ p95: −0.26% (8h, t≈−1.5).
  - **2023–2026 (decay).** Funding ≤ p5: +0.04% (8h), +0.36% (24h), +0.73% (48h), all t<1. Funding ≥ p95/p99 was followed by positive, not negative, returns (t<0.5). Correlation of funding with the forward 24h return fell to −0.008.
  - Interpretation: there was a short-squeeze asymmetry (negative funding is the useful extreme) in the 2020–22 leverage era, and it has since weakened sharply.

**Open interest (OI), long/short ratios, liquidations**
- Glassnode's "Leverage Position Openings and Closures" infers positioning from the signs of price and OI changes: long openings (price↑ OI↑), short openings (price↓ OI↑), long closures (price↓ OI↓), short closures (price↑ OI↓). Glassnode says long closures "often mark local bottoms after downward price movements" and that long-opening ramps occur near tops. **It gives no hit rates, horizons or average returns; the evidence is visual chart inspection only.** — [Glassnode Research](https://research.glassnode.com/leverage-position-openings-and-closures/)
- Coinglass publishes two long/short ratios: an account-based one (number of accounts) and a volume- or position-based one ("top traders"). Long positions include hedgers, market makers and arbitrageurs, so the ratio is not a clean sentiment measure. I found no rigorous test of extreme L/S ratios as a contrarian signal. — [Coinglass Learn](https://www.coinglass.com/fr/learn/what-is-the-bitcoin-long-short-ratio-and-crypto-futures-longs-vs-shorts)
- October 10, 2025 cascade: about $19bn of leveraged positions were unwound across futures and perps, and nearly 90% of liquidations were longs. — [21Shares](https://www.21shares.com//research/record-crypto-liquidations-amid-tariff-shock); [WisdomTree](https://www.wisdomtree.com/onchain/insights/blog/whats-hot-leverage-liquidity-and-panic). A minute-level study of the same crash describes it as futures-led, with BTC down 12.6% in ten minutes on Binance after the tariff headline and the basis swinging within minutes. — [Lim, SSRN 6579278](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6579278) *(abstract seen only via search snippet; page returned 403)*
- Seven BTC liquidation cascades (2022–2025): price showed "critical slowing down" early-warning signatures before five endogenous build-ups but not before the two sudden-news (tariff) shocks. Early warnings are event-heterogeneous. — [arXiv 2607.27070](https://arxiv.org/abs/2607.27070) (preprint)
- A Glassnode/Bybit report on a sharp BTC short squeeze (date not verified) found that about 64k BTC of OI was closed out and shorts supplied 89% of liquidated dollars; the authors called it a one-off event rather than a regime change. — [Decrypt](https://decrypt.co/378686/bitcoin-sharpest-rally-two-years-short-liquidations) [SECONDARY]
- Intraday order flow on Binance perps: opening order imbalance predicts returns over the next 4–12 hours, with much weaker effects at finer frequencies. — [arXiv 2607.09426 "The Quarter-Hour Effect"](https://arxiv.org/html/2607.09426v2) *(seen via search summary only)*

**Coinbase premium / venue premia**
- Deeply negative Coinbase premium readings occurred near local bottoms (Nov 2022, Aug 2023), according to CryptoQuant and FalconX commentary. This is anecdotal, with no statistical test. — [CoinDesk 2024](https://coindesk.com/markets/2024/07/01/bitcoins-bottom-in-price-could-be-near-or-already-in-the-coinbase-premium-index-suggests); [FalconX via newsletter](https://theinformerpost.beehiiv.com/p/coinbase-premium-discount-could-signal-splendid-six-to-12-months-for-bitcoin-says-falconx-analyst)
- The closest academic analogue: **changes in the Grayscale GBTC premium were the single most significant predictor of Bitcoin's daily return.** The predictability holds on the most liquid exchanges and is strongest when sentiment variation is high. — [SMU working paper 2023](https://ink.library.smu.edu.sg/lkcsb_research/7447)

**Crypto Fear & Greed Index (alternative.me)**
- Wavelet coherence and VAR on the five largest coins: sentiment is a "robust leading indicator" at a **one-week to one-month** horizon, not at intraday or 1–2 day horizons. — [Albrecht, Pastorek, Maňoušek, Czech J. Econ. Finance 2025](https://journal.fsv.cuni.cz/mag/article/show/id/1548)
- Weekly BTC/ETH data (Jul 2022–Jun 2023), using Granger causality and quantile regression, tests whether the index predicts shifts in returns. — [Cavalheiro et al., Rev. Behavioral Finance 2024](https://ideas.repec.org/a/eme/rbfpps/rbf-08-2023-0224.html)
- A contrarian scaling rule since Feb 2018 (buy 1% of capital when the index is ≤20, sell 1% when ≥80) returned 1,145% against 1,046% for buy-and-hold, with no fees, no trade count, and macro-cycle holding periods. — [Bitcoin Magazine, Dec 2024](https://bitcoinmagazine.com/markets/how-a-bitcoin-fear-and-greed-index-trading-strategy-beats-buy-and-hold-investing)
- **[OWN CALC]** alternative.me F&G (daily, [API](https://api.alternative.me/fng/?limit=0)) against forward BTC returns from 00:00 UTC, 2020–2026 (2,464 days).
  - Unconditional mean: +0.10% (24h), +0.20% (48h).
  - F&G ≤10: +1.07% (24h, n=65, t≈1.7); F&G ≤20: +0.10% (24h, n=309, t≈0). No edge at "Fear ≤20".
  - F&G ≥80: +0.54% (24h) and +1.24% (48h), n=151, t≈1.4–1.6. **"Extreme Greed" was followed by continuation, not reversal.**
  - 2023–2026: all extremes have t<0.7.
  - Conclusion: no evidence for a ≤2-day contrarian F&G signal.

**Options: 25-delta risk reversal (skew), DVOL**
- A dissertation (SMU, May 2026) on daily Deribit data from Apr 2021 to Dec 2025 finds the 25Δ 90-day risk reversal coefficient significant at 1% with Newey-West errors. The t-stat rises from 1.91 (univariate) to 3.73 (full controls), and the effect is significant across most delta/tenor specifications, concentrated in **30–180-day tenors**. It is an unreviewed thesis; I could not verify the return horizon or the out-of-sample results. — [SMU etd_coll/887](https://ink.library.smu.edu.sg/etd_coll/887)
- Practitioner view: research is "mixed". RR extremes are better read as crowding or event pricing than as a directional signal. Sign conventions differ across sources (call−put vs put−call). — [LuxAlgo](https://www.luxalgo.com/library/concept/risk-reversals.md); Anchorage describes RR percentiles (e.g., 84th percentile of Deribit's five-year history) descriptively. — [Anchorage Digital](https://www.anchorage.com/research/the-anchorage-digital-prime-signal-what-skew-wings-and-the-term-structure-are-telling-us-about-bitcoin-and-its-adjacent-markets)
- GARCH-type conditional skewness predicts BTC returns, but **the sign flips by regime**: negative in 2018–2020, positive in 2021–2022. — [Atance & Serna, QREF 2024](https://ideas.repec.org/a/eee/quaeco/v96y2024ics1062976924000747.html)
- DVOL: I found no peer-reviewed short-horizon return test.

### Inferences
- The only crypto extreme with an (in-sample) ≤2-day reversal signature in my check is **deeply negative funding → upside squeeze**. Positive-funding extremes are the "overheated" case, and they did not reliably mean-revert within 2 days. This matches the BIS finding that high carry predicts crashes at unspecified (likely longer) horizons, combined with momentum in the short run.
- For a relative-value book, funding, basis and OI are better used as **conditioning or sizing filters**: they mark fragile, crash-prone states and potential liquidation fuel. They are weak entry triggers. Combining them with a price-based reversal trigger (e.g., a large move plus an OI drop, meaning a liquidation flush) is more consistent with Glassnode's long-closure observation than either signal alone. That remains untested here.
- Perp–spot and funding effects are decaying (deviations −11%/yr per He et al.; my funding check shows near-zero effect in 2023–26), which is consistent with growing arbitrage capital, including ETF-era basis traders.
- Cross-sectionally, funding or basis spreads across many perps on one exchange (Binance has more than 300) may work better than BTC time-series extremes. The SSRN factor paper hints at regime-dependent reversal premia, but I found no clean ≤2-day test.

### Gaps
- No primary Kaiko, Amberdata, CryptoQuant or Coinglass study with quantified ≤2-day hit rates for funding, OI or L/S extremes was found. Their public pages are commentary or paywalled.
- No rigorous test found for stablecoin flows (exchange netflows, mint/burn) as a ≤2-day predictor.
- No verified short-horizon evidence for DVOL spikes or the Coinbase premium (only anecdotes).
- BIS WP 1087's exact predictive horizons and coefficients were not accessible (PDF blocked by a JS challenge).

---

## 2. Equity/volatility (VIX level and spikes, VIX term structure, VVIX, SKEW, put/call, GEX, breadth/TRIN, AAII/II surveys, CNN F&G): evidence at 1–5 day horizons?

### Takeaway
At 1–5 days, the most robust non-price effects in equity indices are **mechanical hedging-flow effects**: dealer gamma and leveraged-ETF rebalancing produce end-of-day momentum that reverses over the next day(s). The second is a small positive drift after VIX extremes (VIX at a 2-year high; backwardation). Classic sentiment gauges (put/call, TRIN, AAII, SKEW, CNN F&G) have weak, inconsistent or decaying short-horizon power. My own check of VIX/VIX3M finds backwardation is a volatility-regime flag, not a reliable 1–5 day direction signal.

### Cited Findings
**VIX level/spikes**
- Bandelli & Wang (2018), Dec 1991–Nov 2017: S&P 500 returns at 1, 5 and 20 days rise with implied-volatility rank versus the past 2 years. The effect is concentrated in "rank 11" (VIX at a new 2-year high), about 54 of roughly 6,000 days. It is **statistically significant at 1 and 5 days but economically small**. CXO notes overlapping windows inflate significance and that no portfolio test was done. — [CXO Advisory summary](https://cxoadvisory.com/equity-premium/revisiting-vix-as-stock-return-predictor)
- 1990–2024: the highest average forward S&P returns (1-week, 1-month, 3-month) followed VIX readings above 25. The VIX predicts higher volatility but not losses. — [New Frontier via Advisor Perspectives](https://www.advisorperspectives.com/commentaries/2024/08/13/leaving-volatile-markets-can-result-missed-upside)

**VIX term structure (VIX/VIX3M, VIX futures curve)**
- Backwardation occurred less than 20% of the time since 2010. Outside the biggest selloffs it has not reliably preceded further declines, and some of the best periods followed big selloffs. — [Cboe Inside Volatility Trading](https://www.cboe.com/insights/posts/inside-volatility-trading-is-vix-backwardation-necessarily-a-sign-of-a-future-down-market)
- 2010–2017: an inverted VIX futures curve had a significant positive relation with subsequent S&P 500 returns, while the normal-curve coefficient was insignificant. — [Macrosynergy](https://macrosynergy.com/?p=41000) *(page returned 403 to me; claim from search excerpt)*
- Fassas & Hourvouliades (JRFM 2019): the VIX futures term structure works as a **contrarian** market-timing indicator. A steep contango marks complacency late in bull phases, and backwardation marks capitulation lows. — [JRFM 12(3):113](https://mdpi-res.com/d_attachment/jrfm/jrfm-12-00113/article_deploy/jrfm-12-00113-v2.pdf). An earlier Fassas sample (2004–2010) found only a weak negative relation between term-structure changes and future S&P returns, in-sample. — [CXO](https://cxoadvisory.com/volatility-effects/change-in-vix-futures-term-structure-as-stock-market-return-predictor)
- The VIX futures basis predicts VIX *futures* returns (Simon & Campasano), so the strategy is to buy VIX futures in backwardation, hedged with S&P futures. — [Quantpedia](https://quantpedia.com/strategies/exploiting-term-structure-of-vix-futures)
- **[OWN CALC]** Cboe [VIX](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv), [VIX3M](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv) and [SPX](https://cdn.cboe.com/api/global/us_indices/daily_prices/SPX_History.csv) closes, Sep 2009–Oct 2026 (4,291 days). Unconditional SPX mean: +0.046% (1d), +0.093% (2d), +0.23% (5d).
  - VIX/VIX3M > 1.0 (n=324): +0.10% (1d), +0.30% (2d), +0.77% (5d), t≈0.4–1.0, with daily sd 2.4% (vs ~1% normally).
  - Ratio > 1.1 (n=69): **+1.84% (5d) in 2009–16 (n=20) but −1.37% (5d) in 2017–26 (n=49)**. The sign flipped, driven by Feb 2018, Mar 2020 and Apr 2025-type crashes.
  - Ratio < 0.80 ("complacent" contango, n=281): slightly below-average returns (5d +0.04%, t≈−1.3).
  - Conclusion: no statistically reliable 1–5 day directional edge; the ratio's main value is as a volatility/regime filter.

**VVIX, SKEW**
- SKEW: Elyasiani, Gambarelli & Muzzioli (Applied Economics 2021) find SKEW acts as a measure of *greed* rather than fear in US and Italian data, and that SKEW changes Granger-cause returns but not the reverse. — [IRIS Unimore](https://iris.unimore.it/handle/11380/1240639). A practitioner decade-by-decade analysis finds SKEW extremes "NOT a reliable directional signal", with the sign flipping by decade. — [thetrading.tools](https://www.thetrading.tools/skew-index) [SECONDARY]
- VVIX: no peer-reviewed 1–5 day return study found (see Gaps).

**Put/call ratios**
- Single stocks: in Pan & Poteshman (2006), stocks with low put/call ratios outperform high put/call stocks by **more than 40 bp the next day and more than 1% over the next week**. The authors attribute this to non-public information of option traders, not to contrarian sentiment. — [NBER w10925](https://www.nber.org/papers/w10925)
- Blau & Brough (2015): the daily put/call ratio of stock options is negatively related to the next day's return. — cited in [MDPI Economies 7(1):24](https://mdpi-res.com/d_attachment/economies/economies-07-00024/article_deploy/economies-07-00024.pdf)
- Index level (CXO, 1995–Feb 2013; Cboe/ISE total, index and equity ratios; 5, 10, 21 and 63-day horizons): correlations with future SPY returns are "very small" and sometimes of the "wrong" sign. The relative CBOE equity put/call ratio has R² = 0.006 at 21 days. A put/call-versus-250-day-SMA strategy made about 19% against about 50% for buy-and-hold (68 trades) and loses money above 0.25% round-trip friction. Conclusion: the evidence "mostly does not support" the ratio's predictive use. — [CXO Advisory](https://www.cxoadvisory.com/sentiment-indicators/predictive-power-of-put-call-ratios)
- **Decay:** the indicator "has lost predictive power lately", partly because early exercise of in-the-money puts inflates the ratio without bearish intent. — [BNN Bloomberg](https://www.bnnbloomberg.ca/this-contrarian-stock-market-signal-is-losing-predictive-power-1.1865641)

**Dealer gamma (GEX) and hedging flows: the strongest ≤2-day mechanism**
- Baltussen, Da, Lammers & Martens (JFE 2021; more than 60 futures across equities, bonds, commodities and FX, 1974–2020): the **last 30 minutes' return is positively predicted by the rest-of-day return**, the effect **reverts over the next days**, and it is linked to net short-gamma hedging. — [Erasmus repository](https://repub.eur.nl/pub/131621); [author PDF](https://www3.nd.edu/~zda/intramom.pdf)
- Barbon & Buraschi, "Gamma Fragility": a **negative dealer gamma imbalance → intraday momentum; positive → intraday reversal**. The effect is stronger in less liquid underlyings, and gamma imbalance is related to the frequency and magnitude of flash crashes. — [Barbon, Gamma Fragility](https://abarbon.com/papers/gamma-fragility)
- Barbon, Beckmeyer, Buraschi & Moerke: a large negative (positive) aggregate gamma imbalance, combining leveraged-ETF rebalancing and option hedging and scaled by dollar volume, produces **end-of-day momentum (reversal)**. The price pressure **dissipates within the next trading day**. LETF flows are more predictable than option-hedger flows, and **LETF effects have weakened over time** (decay). — [SSRN 3925725](https://papers.ssrn.com/abstract=3925725); [paper page](https://abarbon.com/papers/liquidity-provision-to-leveraged-etfs-and-equity-options-rebalancing-flows)
- Vendor framing: GEX describes the volatility regime (positive gamma dampens, negative amplifies) and "does not predict direction". — [SpotGamma](https://spotgamma.com/gamma-exposure-explained/)

**Breadth / TRIN**
- One-, two-, five- and 10-day TRIN show near-zero correlations with S&P 500 moves over the next 1, 5 and 10 days. Colby & Meyers (1928–1987) found "relatively limited forecasting value". — [Daily Speculations](https://dailyspeculations.com/about%20us/archives/archieve/An%20investing%20tool%20you%20can%20do%20without.htm)
- TRIN's predictive power "has weakened considerably since the 2000s" (decay). — [AAII Journal](https://www.aaii.com/journal/article/322803-using-the-arms-index-trin-for-market-breadth-analysis)

**Surveys (AAII, Investors Intelligence)**
- The AAII survey has run weekly since 1987. When bearishness is 2 or more standard deviations above its mean, the S&P 500 has tended to post above-average 6–12 month returns. — [AAII](https://aaii.com/sentimentsurvey)
- Short horizon: a 2009 Active Trader study (data from 1988) found stocks fell a median 1.45% within two weeks of extreme bearish readings, which is continuation, not reversal. After bullish extremes the market performed in line with its benchmark. — [Fidelity/Active Trader PDF](https://www.fidelity.com/bin-public/060_www_fidelity_com/documents/TradingMarketsMood_06_2009_V2.pdf)
- After extreme bearish spreads, 3-month, 6-month and 1-year returns were only +0.3, +0.7 and +0.6 pp above average. — [LPL Research](https://qa65.lpl.com/research/blog/investor-sentiment-hits-extremely-bearish-levels.html)

**CNN Fear & Greed**
- Farrell & O'Connor (Finance Research Letters 72, 2025): CNN F&G Granger-causes S&P 500, Nasdaq Composite and Russell 3000 returns in 2011–2020, but not gold. In 2021–2024 the link is "considerably weaker" (decay), and the stronger relation may have been concentrated before 2014. The working-paper version found no significant VIX relation. The data were hand-collected (GitHub, Wayback Machine). — [RePEc](https://ideas.repec.org/a/eee/finlet/v72y2025ics1544612324015216.html); [UCC](https://research.ucc.ie/en/publications/the-cnn-fear-and-greed-index-as-a-predictor-of-us-equity-index-re/); [CXO summary](https://cxoadvisory.com/sentiment-indicators/cnn-fear-and-greed-index-as-return-predictor)

### Inferences
- For a ≤2-day reversal system, **gamma and LETF flow state** (sign and size of aggregate dealer gamma relative to volume, plus the day's move) is the best-supported equity input. It predicts *whether* intraday moves extend into the close and then partially revert the next day. A free daily GEX proxy exists (SqueezeMetrics, Section 8).
- VIX-based extremes (2-year-high VIX, backwardation) are better used for **position sizing and permission** (expect larger moves, mildly positive drift) than as contrarian triggers. The 2017–26 sign flip at VIX/VIX3M > 1.1 is a warning against hard-coding "backwardation = buy".
- Survey and put/call "overheating" signals operate, if at all, at weeks to months. They can serve as slow regime overlays, not as ≤2-day entries.

### Gaps
- No peer-reviewed 1–5 day study found for VVIX extremes, VIX9D/VIX ratio extremes, or % of stocks above 20/50-day moving averages.
- No independent study of commercial GEX (SpotGamma, SqueezeMetrics) as a predictor of next-day index returns, as opposed to intraday momentum, was found.
- Investors Intelligence data are paid; no short-horizon study was found.

---

## 3. Futures positioning (CFTC COT non-commercial/leveraged-fund percentiles): reversal evidence, and why weekly data with a 3-day lag only works as a filter

### Takeaway
Academic evidence is consistent: speculator COT positions are strongly *contemporaneously* correlated with prices (trend-following), but positions have little or no power to forecast next-week returns. The exception is the *change* in speculator positions in commodities, which negatively predicts next-week returns (a liquidity-provision reversal). Tuesday positions are released Friday at 15:30 ET, so a ≤2-day strategy can only use COT as a slow "crowding" filter. Crowding extremes can persist for months (JPY 2024 and 2026) before a catalyst (BoJ, MoF intervention) triggers the unwind.

### Cited Findings
- COT reports are "generally published each Friday at 3:30 pm Eastern Time" and "typically based upon data calculated as of the close of business of Tuesday". There are four report types: Legacy, Supplemental, Disaggregated and Traders in Financial Futures (TFF). — [CFTC](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)
- Klitgaard & Weir (NY Fed EPR 2004; six CME currencies, 1993–2003): the direction of the weekly change in speculators' net position matches the exchange rate's direction about 75% of the time, and position changes track 30–45% of weekly FX moves. However, **"net positions do not appear to be useful for anticipating exchange rate moves over the following week."** — [NY Fed EPR](https://www.newyorkfed.org/research/epr/04v10n1/0405klit/0405klit.html)
- Sanders, Irwin & Merrin (JARE 2009; 10 agricultural futures): "very little evidence that traders' positions are useful in forecasting (leading) returns". Non-commercials are trend-followers. — [AgEcon Search PDF](https://ageconsearch.umn.edu/record/54547/files/JARE_Aug09__04R_pp276-296.pdf)
- Kang, Rouwenhorst & Tang (JF 2020): short-run changes in non-commercial positions are driven by speculators' liquidity needs, and long-run variation by hedgers' needs. The two components push expected futures returns in opposite directions. — [RePEc](https://ideas.repec.org/a/bla/jfinan/v75y2020i1p377-417.html)
- A follow-up by Kang and co-authors (2026 seminar): speculators' net trading (Q) **negatively forecasts next-week commodity futures returns** ("short-term trading-based reversal"), while the return component orthogonal to Q shows next-week momentum. With granular position data, short-term reversal is better explained by past speculator *trading* than by past returns. — [Lingnan College seminar abstract](https://lingnan.sysu.edu.cn/en/event/3656) *(no effect sizes published on the page)*
- Practitioner extreme definitions: more than 2 SD above the trailing 1-year and 3-year averages ([FXStreet](https://www.fxstreet.com/amp/analysis/cot-report-speculators-buy-the-euro-and-sell-the-us-dollar-201804142005)), or a 52-week "COT Index" percentile near 0 or 100 ([Bookmap](https://bookmap.com/blog/cot-and-price-reversals-how-to-interpret-speculator-positions)). FXStreet stresses that crowded positions "do not suggest an imminent reversal" but are a risk factor.
- **[OWN DATA PULL — JPY illustration]** CFTC Legacy futures-only, JPY (CME), non-commercial net position, from the [CFTC Socrata API](https://publicreporting.cftc.gov/resource/6dca-aqww.json):
  - **2024:** −143k (2 Apr) → −180k (23 Apr) → **−184,223 on 2 Jul 2024** (most extreme since 2024-01) → −107k (23 Jul) → −73k (30 Jul) → −11k (6 Aug) → +23k (13 Aug). The record short persisted for about 3 months, through MoF intervention in late Apr/May 2024, before the July–August unwind.
  - **2026:** −155k (30 Jun) → **−163,412 (28 Jul 2026)** → −45k (4 Aug) → +120k (15 Sep) → +62k (6 Oct 2026).
- 2026 context: MoF confirmed about ¥11.7tn of intervention between 28 Apr and 27 May 2026, including a record ¥6.28tn on 30 Apr, surpassing the ¥5.92tn record of 29 Apr 2024. — [NST/Bernama](https://www.nst.com.my/amp/business/economy/2026/05/1431231/japan-spends-more-us30bil-prop-yen); [Business Today MY](https://www.businesstoday.com.my/2026/08/07/japans-yen-intervention-hit-record-us40-billion-in-april/). AFP reported ¥15.4tn (~$96bn) spent from late July to late August 2026, including the first joint US–Japan intervention in 28 years on 31 Jul. — [Qatar Tribune/AFP](https://www.qatar-tribune.com/article/251049/business/japan-spent-record-96-billion-in-yen-interventions-ministry) *(single wire source)*
- After the Aug 2024 carry unwind, hedge funds turned net long the yen. — [BNN Bloomberg](https://bnnbloomberg.ca/business/international/2024/08/16/hedge-funds-turn-bullish-on-yen-after-carry-trade-blow-up)

### Inferences
- COT data arrive with a 3-day lag (Tuesday → Friday release) and weekly granularity. For a ≤2-day holding period, COT can only (a) define which assets are "crowded" (percentile extremes) and (b) scale up reversal trades in the crowded direction when a fast trigger fires: a price shock, an intervention headline, a funding spike, or a risk-reversal move. Positions alone do not time reversals (Klitgaard & Weir; Sanders et al.).
- The JPY episodes show the asymmetry: crowded shorts unwind violently, by 170–300k contracts within 1–5 weeks, but only after a catalyst. Waiting for a fast trigger is essential.
- For commodities, the *weekly change* in speculator net positions (not the level) is the academically supported short-term reversal variable (Kang et al.). Even so, its next-week horizon only partly overlaps a ≤2-day hold.

### Gaps
- No public out-of-sample study of TFF leveraged-fund percentile extremes versus next 1–5 day FX or index returns was found.
- I did not run a full COT-extreme backtest; that would need futures price series. Daily open interest by exchange (CME daily volume/OI reports) as a higher-frequency proxy was not researched.

---

## 4. Systematic positioning estimates (CTA trend-follower positioning, vol-control funds, leveraged ETF rebalancing, options expiration): do max-long CTA positions predict short-term reversals?

### Takeaway
There is **no public, rigorous evidence** that sell-side "CTA max long" estimates predict ≤2-day reversals. These estimates are scenario models of *conditional* flows: who must sell if price breaks level X. Mechanical rebalancing flows with academic support are leveraged-ETF and option-hedging flows (end-of-day momentum, next-day reversal) and, in narrative evidence, vol-control deleveraging after volatility spikes. OPEX effects are anecdotal.

### Cited Findings
- Nomura's McElligott (2019) described CTAs flipping to "max long" US equities but said they could "just as likely" flip back to short after a short-term selloff. This is a caveat about reversibility, not a predictive test. — [BloombergQuint](https://www.bloombergquint.com/markets/nomura-s-mcelligott-sees-quants-pivoting-to-max-long-stocks)
- Goldman Sachs scenario modelling (2 Sep 2025): in a down-market scenario CTAs would sell $22.25bn of global equities over 1 week ($4.84bn US), and up to $217.92bn over 1 month ($73.69bn US) in a deep decline. Goldman judged that pullbacks would be "mild and brief" absent shocks. — [Tiger Brokers repost](https://www.itiger.com/news/1161473555) [SECONDARY]
- Citi publishes CTA trigger levels (index levels at which models cut longs). — [Tickmill repost](https://www.tickmill.com/blog/institutional-insights-citi-cta-update-positioning-key-levels) [SECONDARY]
- Crowding: managed-futures AUM relative to total futures ADV doubled from pre- to post-GFC (0.16 → 0.27). — [Babbedge & Kerson, CME-hosted 2019](https://www.cmegroup.com/education/files/trends-not-dead-babbedge-kerson-2019.pdf)
- Vendor daily CTA flow estimates exist (e.g., Kpler "Financial Flows"). — [Kpler](https://www.kpler.com/solutions/decision-tools/financial-flows)
- Vol-control funds: Barclays (2018) estimated about $225bn of equity selling by volatility-targeting funds after a vol spike, with about $500bn AUM, two-thirds of it algorithmic. — [Gulf News via PressReader](https://pressreader.com/uae/gulf-news/20180207/282355450194602). The MSCI USA 10% Risk Control index uses 20- and 60-day vol windows, so the Aug 2015 spike would have forced more than 50% deleveraging within days. Sell-side estimates of vol-target AUM ranged from $50bn to $300bn, implying up to $180bn of selling. — [Acadian](https://www.acadian-asset.com/investment-insights/managing-risk/defensive-investing-strategies-feedback-loops-and-echoes-of-1987). The S&P 500 fell 11.2% in under 10 days in Aug 2015, which managed-vol trading is argued to have amplified. — [The Actuary](https://www.theactuarymagazine.org/the-volatility-regime/)
- Leveraged ETF rebalancing: end-of-day momentum that dissipates within the next trading day, with the effect weakening over time (see Section 2). — [SSRN 3925725](https://papers.ssrn.com/abstract=3925725)
- Option expiration: an unvetted advisor analysis claims that holding the S&P 500 only in the 4 days around each monthly OPEX since 2020 returned −23%, against +39% for buy-and-hold. — [The Reformed Broker](https://thereformedbroker.com/?p=85655) [SECONDARY]. Gamma commentators note that the Dec 2018 and Mar 2020 selloffs climaxed shortly after quarterly expirations (n=2). — [SpotGamma](https://spotgamma.com/sp-remains-resilient-but-for-how-long/) [SECONDARY]
- A 2026 arXiv paper offers a microstructural account of the "demise of short-term trend-following". — [arXiv 2607.01550](https://arxiv.org/pdf/2607.01550) *(only references seen)*

### Inferences
- CTA estimates are useful to a retail system mainly as **flow asymmetry maps**. When CTAs are near max long, the upside flow is exhausted and the downside is convex (forced selling if trigger levels break). That favours *downside follow-through after a break*, not an immediate fade of strength. A retail trader can approximate CTA positioning with a multi-lookback trend model (e.g., 20/60/120/250-day signals, vol-scaled) on IB futures data. This is an inference; I did not validate it.
- Vol-control deleveraging is mechanically lagged by 1–20 days after a vol spike, so selling pressure may persist for days after a shock. It supports *not* fading the first day of a vol spike in equity indices and waiting for the vol peak instead.

### Gaps
- No published hit-rate or backtest of GS, Nomura or Citi CTA-positioning extremes against forward 1–5 day returns was found.
- No academic OPEX-week study after 2018 (0DTE era) was found.

---

## 5. FX: risk reversals, carry positioning, intervention risk (JPY), "overbought" currencies

### Takeaway
Academic FX evidence links risk reversals and speculator carry positioning to *crash risk* (the conditional distribution), not to clean short-horizon return forecasts. Jurek finds that option-implied skew does not forecast excess returns. For JPY, positioning extremes combined with intervention thresholds are the archetypal "overheated" setup, but the timing comes from the policy catalyst.

### Cited Findings
- Brunnermeier, Nagel & Pedersen: FX crash risk increases with the interest-rate differential, past carry returns and **speculators' carry futures positions**, and decreases with the price of crash insurance (risk reversals). — [Princeton slides](https://www.princeton.edu/~markus/research/papers/carry_trades_currency_crashes_slides_old.pdf); [paper page](https://markus.scholar.princeton.edu/document/99)
- Jurek: risk-neutral skewness from FX options **does not forecast** excess currency returns, and implied and realized skewness respond in opposite directions to lagged returns. — [Jurek PDF](https://www.johnhcochrane.com/s/jurek_currency.pdf)
- Kütük & van Wijnbergen (2025, USD/TRY): risk reversals and option-implied crash probabilities raise expected returns, which they read as compensation for risk rather than mispricing. — [Tinbergen DP 25-058](https://papers.tinbergen.nl/25058.pdf)
- JPY: in mid-2024 analysts warned that record net shorts were "not necessarily a sign that a sharp reversal is imminent", since intervention could matter more. — [City Index COT 2024-07-01](https://cityindex.com/en-uk/news-and-analysis/jpy-eur-cad-aud-crude-oil-analysis-cot-report-2024-07-01). The 2024 and 2026 positioning paths and intervention amounts are in Section 3. — [CFTC API](https://publicreporting.cftc.gov/resource/6dca-aqww.json); [NST](https://www.nst.com.my/amp/business/economy/2026/05/1431231/japan-spends-more-us30bil-prop-yen)
- The 5 Aug 2024 unwind is described as clearing most speculative yen shorts while leaving the structural carry trade intact. — [LambdaFin](https://www.lambdafin.com/articles/yen-carry-trade-unwind) [SECONDARY, loosely sourced]

### Inferences
- A practical FX "overheating" score for a ≤2-day system could combine: (1) COT leveraged-fund percentile (slow), (2) 1-month 25Δ RR z-score (crash-insurance price, available through IB option chains on CME FX futures; feasibility not verified), (3) distance to known intervention zones (e.g., USD/JPY 155–162 in 2024–26), and (4) a fast trigger. The research supports using (1) and (2) for *crash-risk asymmetry*, not for direction alone.

### Gaps
- No study found testing daily FX risk-reversal changes against next 1–2 day spot returns.
- No public free daily history of FX risk reversals was found. Retail would need to construct it from CME FX options via IB; I did not verify feasibility.

---

## 6. Commodities/gold: ETF holdings changes, futures curve extremes, gold/silver ratio extremes

### Takeaway
Gold ETF flows mostly *chase* price. The one short-horizon study found 1–2 day flow-to-return continuation followed by 3–5 day reversal, which is a price-pressure pattern. Gold/silver ratio mean reversion is supported only by practitioner material, with long and regime-dependent half-lives. I found no ≤2-day evidence for curve (backwardation/contango) extremes.

### Cited Findings
- Daily SPDR Gold Shares flows against the London PM fix (VAR): **positive relation from 1–2 day lagged flows to returns, negative from 3–5 day lags**, read as price pressure followed by reversal. Returns also lead flows (1-day lag strongest). — [NDLTD Taiwan thesis](https://ndltd.ncl.edu.tw/handle/79415745161990386644)
- Short-term gold price moves "remain rather unpredictable", and explanations such as physical-ETF flows are "unreliable or unstable over time". — [Klement 2015, MPRA 64590](https://mpra.ub.uni-muenchen.de/64590)
- Gold ETP flows are positively correlated with price, buying strength and selling weakness (Société Générale). — [ETF Strategy](https://etfstrategy.com/etp-flows-have-measurable-effect-on-commodity-prices-according-to-societe-generale-46525). Baur (84 gold ETFs): the gold price and ETF holdings moved almost in lockstep, without establishing causality. — [Advisor Perspectives](https://www.advisorperspectives.com/articles/2013/09/03/the-hidden-risk-in-gold)
- For precious-metal ETFs, *unexpected* flows matter more than expected flows. — [Polish VAR study](https://czasopisma.mazowiecka.edu.pl/index.php/ne/article/download/949/855)
- Gold/silver ratio: a historical mean of about 60:1, reversal tendencies when about 20% above average, and a record of about 123:1 in 2020 before falling back to about 60 (Silver Institute via a broker). — [VT Markets](https://www.vtmarkets.com/en-ca/live-updates/gold-silver-ratio-signals-potential-mean-reversion-as-silver-institute-highlights-underpriced-silver-and-demand-drivers/) [SECONDARY]. The ratio can stay elevated for years, and structural shifts move the equilibrium. — [Metalcharts](https://us2.metalcharts.org/gold-to-silver-ratio); detecting regime changes is critical. — [Mining.com](https://www.mining.com/?p=9612)

### Inferences
- In commodities, the most promising ≤2-day "overheating" input is probably *flow-pressure reversal*: large unexpected ETF flows (GLD/SLV/USO share-count changes, published daily) fading over 3–5 days. This sits at the edge of the ≤2-day window and is supported by a single thesis.
- The gold/silver ratio is a multi-week to multi-month relative-value gauge, not a ≤2-day signal.

### Gaps
- No study found linking futures-curve extremes (e.g., front-spread z-scores in crude or nat gas) to 1–2 day reversals. The academic basis/carry literature works at monthly horizons; I did not research it further here.
- I did not verify the history availability of free GLD/SLV daily holdings files.

---

## 7. Cross-asset "overheating" composites (GS Risk Appetite, BofA Bull & Bear, Citi Panic/Euphoria): evidence and availability

### Takeaway
All three are proprietary and available only through press coverage, with weekly or irregular latency. Their published track records refer to **2–12 month** horizons with small samples (about 16–18 BofA sell signals since 2002). They are useless as ≤2-day triggers, but they can serve as top-level regime labels.

### Cited Findings
- BofA Bull & Bear: the sell signal (indicator > 8) fired 16 times since 2002. Global equities (MSCI ACWI) averaged −2.4% afterwards, with a maximum average drawdown of 8.5% about 3 months later, and the signal was "right" 63% of the time. — [Fortune, 19 Dec 2025](https://fortune.com/2025/12/19/stocks-bank-of-america-warns-contrarian-sell-signal). By May 2026 it had fired for about the 17th or 18th time (8.0 → 8.5). — [StockWireX](https://stockwirex.com/news/bofa-sell-signal-bull-bear-indicator-may-2026/) [SECONDARY]. After a sell signal *ends* (32 occasions since 2002), SPX and ACWI averaged only +1% over 3 months. — [Ugebrev](https://ugebrev.dk/?p=4580725) [SECONDARY]
- GS Risk Appetite Indicator (RAI): above 1.1 in May 2026, the 99th percentile since 1991. Of 8 comparable high-risk-appetite plus high-momentum episodes since 1962, 3 were followed by a bear market within 2 years, and Goldman warned against reading too much into the timing. — [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/goldman-sachs-doubles-down-stock-171700289.html) [SECONDARY]. A 2021 Goldman note said sentiment and positioning are "seldom a catalyst for reversal" on their own. — [Ugebrev repost](https://ugebrev.dk/?p=1531571) [SECONDARY]
- Citi Panic/Euphoria: euphoric readings imply an 83% historical probability of losses over the next 12 months (Citi's own claim). — [Livewire](https://www.livewiremarkets.com/wires/citi-s-stock-market-sentiment-gauge-the-panic-euphoria-model-has-delivered-consecutive-weeks-of-euphoric-readings-for-the-market). The Dec 2018 "panic" reading was historically followed by an average +18% over 12 months. — [CNBC](https://www.cnbc.com/2019/01/02/investors-are-officially-panicking-citigroup-says.html). SentimenTrader's proxy has been "inconsistent after registering euphoric readings". — [SentimenTrader, Jun 2020](https://sentimentrader.com/blog/it-looks-like-investors-are-becoming-euphoric/). The index is published weekly via Barron's.

### Inferences
- A retail system can build its own transparent composite from free daily inputs: VIX percentile, VIX/VIX3M, HY spread (FRED), SqueezeMetrics GEX, put/call sub-indices (CNN components), crypto funding, F&G, and COT percentiles. Given the evidence above, such a composite should be used as a *regime/sizing* layer, with fast price, flow and liquidation triggers doing the timing.

### Gaps
- No independent out-of-sample evaluation of any of the three bank composites was found. Inputs and weights are not public.

---

## 8. Free or cheap machine-readable data, with history length and latency (verified by direct API/CSV pulls on 2026-10-12)

### Takeaway
Most of the catalogue can be built for free. Crypto funding (from 2019–2020), Binance 5-minute OI and long/short metrics (from Sep 2020), Deribit DVOL (from Mar 2021), alternative.me F&G (from Feb 2018), Cboe VIX-family CSVs (from 1990/2006/2009/2011), FRED VIX (from 1990), the CFTC COT API (from 1986 legacy, 2006 TFF), SqueezeMetrics DIX/GEX (from May 2011) and DefiLlama stablecoin supply (from Nov 2017) are all directly downloadable. The main gaps are free put/call history after Oct 2019, CNN F&G before 2021, and historical crypto options skew.

### Cited Findings
**Crypto**
- **Binance funding rate REST:** `GET /fapi/v1/fundingRate` returns up to 1,000 rows per call (default: the most recent 200), in ascending order, sharing a 500/5min/IP limit. — [Binance API docs](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History)
- **Binance bulk files:** monthly funding files for BTCUSDT start 2020-01 (verified listing). — [data.binance.vision fundingRate](https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix=data/futures/um/monthly/fundingRate/BTCUSDT/)
- **Binance daily "metrics" files (BTCUSDT from 2020-09-01):** 5-minute rows (288/day) with `sum_open_interest`, `sum_open_interest_value`, `count_toptrader_long_short_ratio`, `sum_toptrader_long_short_ratio`, `count_long_short_ratio`, `sum_taker_long_short_vol_ratio`. The earliest files contain duplicate rows, so clean them first. Other USD-M daily datasets: aggTrades, bookDepth, bookTicker, indexPriceKlines, klines, markPriceKlines, premiumIndexKlines, trades. — [data.binance.vision metrics listing](https://s3-ap-northeast-1.amazonaws.com/data.binance.vision?delimiter=/&prefix=data/futures/um/daily/metrics/BTCUSDT/); [sample file](https://data.binance.vision/data/futures/um/daily/metrics/BTCUSDT/BTCUSDT-metrics-2026-10-01.zip)
- **Binance REST OI history:** `GET /futures/data/openInterestHist` (5m–1d periods, max 500 rows) serves **"Only the data of the latest 1 month"**. For history, use the metrics files above. — [Binance API docs](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest-Statistics)
- **Deribit (free public API):** BTC DVOL daily OHLC via `public/get_volatility_index_data` starts 2021-03-24 (verified). BTC-PERPETUAL funding history via `public/get_funding_rate_history` returned data for 2019-04-30. — [Deribit DVOL endpoint](https://www.deribit.com/api/v2/public/get_volatility_index_data?currency=BTC&start_timestamp=1577836800000&end_timestamp=1640995200000&resolution=1D); [Deribit funding endpoint](https://www.deribit.com/api/v2/public/get_funding_rate_history?instrument_name=BTC-PERPETUAL&start_timestamp=1546300800000&end_timestamp=1556668800000)
- **alternative.me Crypto Fear & Greed:** `?limit=0` returns the full history, 3,172 daily values from 2018-02-01 to 2026-10-12, updated daily at 00:00 UTC. — [alternative.me API](https://api.alternative.me/fng/?limit=0)
- **DefiLlama stablecoin supply (USDT):** daily history from 2017-11-29 (3,240 points). — [DefiLlama stablecoins API](https://stablecoins.llama.fi/stablecoincharts/all?stablecoin=1)

**Equity/vol**
- **Cboe free CSVs** (verified through 2026-10-09): VIX from 1990-01-02, VIX9D from 2011-01-04, VIX3M from 2009-09-18, VVIX from 2006-03-06, SKEW from 1990-01-02, SPX from 1975. — [VIX](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv), [VIX9D](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX9D_History.csv), [VIX3M](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv), [VVIX](https://cdn.cboe.com/api/global/us_indices/daily_prices/VVIX_History.csv), [SKEW](https://cdn.cboe.com/api/global/us_indices/daily_prices/SKEW_History.csv)
- **Cboe put/call free CSVs** (total, equity, index) cover only **2006-11-01 to 2019-10-04**. — [totalpc.csv](https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/totalpc.csv), [equitypc.csv](https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/equitypc.csv), [indexpc.csv](https://cdn.cboe.com/resources/options/volume_and_call_put_ratios/indexpc.csv)
- **FRED:** VIXCLS from 1990-01-02 and VXVCLS (VIX3M) from 2007-12-04, both to 2026-10-08, keyless CSV. — [FRED VIXCLS](https://fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS); [FRED VXVCLS](https://fred.stlouisfed.org/graph/fredgraph.csv?id=VXVCLS)
- **SqueezeMetrics free daily DIX (dark-pool index) and GEX (dollar gamma estimate)** for SPX: 3,884 rows from 2011-05-02 to 2026-10-09. — [DIX.csv](https://squeezemetrics.com/monitor/static/DIX.csv)
- **CNN Fear & Greed (unofficial JSON endpoint):** works for start dates from 2021-01-01 (1,449 daily rows, 2021-01-04 to 2026-10-09). An earlier start returned HTTP 500. The JSON includes sub-components (market_momentum_sp500/sp125, stock_price_strength, stock_price_breadth, put_call_options, market_volatility_vix, junk_bond_demand, safe_haven_demand). This gives a free daily put/call proxy after 2019. — [CNN dataviz endpoint](https://production.dataviz.cnn.io/index/fearandgreed/graphdata/2021-01-01). Pre-2021 history must be reconstructed; Farrell & O'Connor used GitHub and the Wayback Machine. — [CXO](https://cxoadvisory.com/sentiment-indicators/cnn-fear-and-greed-index-as-return-predictor)
- **AAII sentiment:** weekly since 1987. — [AAII](https://aaii.com/sentimentsurvey)

**Positioning**
- **CFTC public reporting API (Socrata):** Legacy futures-only from 1986-01-15 and TFF futures-only from 2006-06-13, both to 2026-10-06. Released Friday 15:30 ET for Tuesday positions. — [Legacy API](https://publicreporting.cftc.gov/resource/6dca-aqww.json); [TFF API](https://publicreporting.cftc.gov/resource/gpe5-46if.json); [CFTC schedule](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)

**Catalogue summary (indicator → free source → history → latency → best-supported ≤2d use)**

| Indicator | Free source | History | Latency | ≤2d evidence (strength) |
|---|---|---|---|---|
| Perp funding (BTC/alts) | Binance REST + bulk | 2019/2020– | 8h (real-time premium index) | Negative-funding squeeze 2020–22 (in-sample, decayed); positive extremes none |
| OI, top-trader/global L/S, taker ratio | Binance metrics files | 2020-09– (5-min) | ~real-time (REST: 30d only) | No rigorous test; Glassnode qualitative |
| Liquidations | Binance WS forceOrder (not verified here) / Coinglass (paid) | — | real-time | Event studies only; heterogeneous |
| Basis/carry | Binance/Deribit/CME futures | 2019– | real-time | High carry → crash risk (BIS), horizon unclear |
| DVOL / 25Δ RR | Deribit API (DVOL); RR must be built from chains | DVOL 2021-03– | real-time | RR: one thesis (30–180d tenors); DVOL none |
| Crypto F&G | alternative.me | 2018-02– | daily 00:00 UTC | None at ≤2d (own calc); 1w–1m leading (paper) |
| VIX level / 2y-high | Cboe CSV, FRED, IB | 1990– | real-time | Small positive drift 1–5d (Bandelli & Wang) |
| VIX/VIX3M, VIX9D | Cboe CSV, FRED | 2009/2011– | real-time | Mixed; sign unstable (own calc) |
| GEX / dealer gamma | SqueezeMetrics CSV | 2011-05– | daily | Intraday momentum/reversal; next-day reversal of EOD pressure (JFE 2021; Barbon et al.) |
| Put/call | Cboe CSV (to 2019), CNN component | 2006–2019; 2021– | daily | Index-level weak; single-stock strong (non-public data) |
| CNN F&G | unofficial endpoint | 2021– (free) | daily | Granger-causality, weakening post-2021 |
| AAII | aaii.com | 1987– | weekly (Thu) | Weeks–months only |
| COT | CFTC API | 1986–/2006– | weekly, 3-day lag | No next-week forecast (FX); position *changes* reverse next week (commodities) |
| BofA B&B / GS RAI / Citi P/E | press only | — | weekly/irregular | Months-horizon, small samples |

### Inferences
- A C# implementation can pull everything above with plain HTTP GET (CSV or JSON). Only historical crypto option surfaces and post-2019 Cboe put/call history need paid or reconstructed sources. Within IB, VIX, VIX3M, VVIX and the futures and options chains are available live, and archiving them daily builds a private history going forward.
- Binance's 30-day REST limit on OI and L/S means the system should use the bulk "metrics" files for backtests and then switch to REST and WebSocket for live data.

### Gaps
- I did not verify Binance's liquidation WebSocket history (it is real-time only, with no official history), Coinglass or CryptoQuant API pricing, or IB's historical availability for VIX9D, VVIX and SKEW.
- I did not verify history depth for Bybit/OKX funding and OI, or for Coinbase/Binance spot candles (needed to compute the Coinbase premium yourself).
