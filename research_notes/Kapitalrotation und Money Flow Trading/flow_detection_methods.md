# Methods and Data Sources for Detecting Cross-Asset Capital Flows ("Money Flow") in Real Time, with a Focus on Intraday Retail Use

Research date: 11 Oct 2026. Scope: cross-asset macro rotation (equities, government bonds, gold/commodities, FX, crypto). Audience: a retail trader in Germany (EUR 50-250k) with Interactive Brokers (IBKR) market data plus free data sources. Main holding period is intraday, with daily/weekly data used as a regime filter.
Latency legend used throughout: **RT** = real-time/streaming; **ID** = intraday snapshots; **D+0/D+1** = published same evening / next day; **W** = weekly; **M** = monthly. Evidence older than about 2022 is flagged as such.

---

## 1. Direct flow data (ETF/fund flows, COT, TIC, bank flow reports, crypto exchange/on-chain/derivatives flows): latency and retail availability

### Takeaway
Almost every "true" flow statistic (ETF creations/redemptions, fund flows, COT, TIC, bank flow research) arrives with a delay of T+1 evening up to 2 months, so none of it can trigger an intraday entry. These are regime/confirmation inputs only. The exception is crypto: exchange-native derivatives data (taker buy/sell volume, open interest, funding, liquidations) is streamed free in real time by the exchanges, and on-chain/stablecoin flows come at hourly to daily resolution, often paid.

### Cited Findings

**Spot crypto ETF flows (Farside and others)**
- Farside publishes daily flow tables in US$ millions for the US spot Bitcoin ETFs (separate tables for Ethereum and Solana ETFs). Its site says the data is "updated in real time" but that "updates typically occur in the evening and night (US time)". — [Farside homepage](https://farside.co.uk/); [BTC table](https://farside.co.uk/?p=997); [ETH table](https://farside.co.uk/ethereum-etf-flow/); [SOL table](https://farside.co.uk/sol/)
- Farside states its tables are generated automatically, favor speed over accuracy and may contain errors. Issuer cells (e.g. BlackRock ETH) are sometimes blank, which makes the latest daily/weekly totals provisional. — [Farside ETH table](https://farside.co.uk/?cat=7); [crypto.news on blank BlackRock entries](https://crypto.news/crypto-etf-flows-split-bitcoin-gains-ethereum-bleeds/)
- Settlement timing: ETF shares and spot BTC trade on T, while creation/redemption and the movement of cash happen on T+1. Market makers send create/redeem orders to an Authorized Participant before a cutoff time. — [NYDIG, "Predicting Bitcoin ETF fund flows"](https://nydig.com:443/research/predicting-bitcoin-etf-fund-flows)
- Day-one numbers are often incomplete. At launch in 2024, Bloomberg Intelligence's Eric Balchunas said "It's typical for only half of the actual flows to be reported on day one" (2024 quote). — [Bloomberg Law](https://news.bloomberglaw.com/crypto/first-look-at-spot-bitcoin-etf-flows-points-to-organic-demand)
- Data vendor Newhedge now shows each fund's number as it is reported, flags the day total as partial until all funds have reported, and can revise the last seven US trading days. — [Newhedge changelog](https://newhedge.io/changelog/spot-etf-flows-live-pending.md)
- Glassnode also carries aggregated US spot ETF flows. — [Glassnode Studio chart](https://studio.glassnode.com/charts/institutions.UsSpotEtfFlowsAll)
- The evidence on ETF flows and BTC price is mixed:
  - FalconX ran a Granger test (non-peer-reviewed) and reported that prior-day ETF inflows predict price (F=8.48, p=0.004; VAR coefficient 0.027). FalconX itself notes that Granger causality is not true causation. — [FalconX](https://falconx.io/newsroom/what-can-spot-etf-flows-tell-us-about-the-trajectory-of-bitcoin-prices-a-preliminary-statistical-investigation)
  - A cointegration study on daily data from Jan 2024 to May 2025 finds a long-run positive relation between ETF net assets and price, significant only at the 10% level. — [Ledger (Pitt)](https://ledger.pitt.edu/ojs/ledger/article/view/393)
  - K33 reports R²≈0.80 between 30-day flows and 30-day BTC returns. That is a contemporaneous fit, not a predictive one. — [The Block](https://www.theblock.co/amp/post/359560/analyst-explains-why-etf-flows-continue-to-drive-bitcoins-price-while-treasury-companies-have-muted-impact)
  - For the futures-ETF era (2021-24), a Granger study finds that BTC prices lead ETF prices, not the reverse. — [VJOL](https://vjol.vista.gov.vn/due/article/view/125157)

**Mutual fund / ETF flow aggregates (ICI, EPFR)**
- ICI publishes weekly estimated long-term mutual fund flows. Example: the release dated 15 July 2026 covered the week ended 8 July, so the lag is about one week. Combined long-term flows plus ETF net issuance are published separately. Actual figures are collected monthly, and the weekly estimates can differ from them. — [ICI flows page](https://www.ici.org/research/stats/flows)
- EPFR (paid, institutional) offers daily and weekly fund flows at T+1 and monthly allocations at T+16. — [CEIBS library guide](https://ceibs.libguides.com/az/epfr-data)
  - A 2014 EPFR presentation said weekly data was released on Thursdays at 5pm EST and daily data at 5pm EST for the previous day. This is old and should be re-verified. — [NBER slides (2014)](https://www.nber.org/sites/default/files/2020-11/CurcuruSlides.pdf)

**CFTC Commitments of Traders (COT)**
- COT positions are as of Tuesday close and released Friday 3:30pm ET, a three-day processing lag. Holidays can delay release by one or two days. October 2026 release dates: 2, 9, 16, 23 and 30 Oct. — [CFTC COT descriptions](https://www.cftc.gov/MarketReports/CommitmentsOfTraders/index.htm); [CFTC release schedule](https://cftc.gov/MarketReports/CommitmentsofTraders/ReleaseSchedule/index.htm)
- Institutions build positioning proxies from COT. JPMorgan's Flows & Liquidity team has proxied equity beta and momentum-trader positioning with the z-score of net CFTC positions of asset managers and leveraged funds as a percentage of open interest (2024 note, reported second-hand). — [Tickmill summary of JPM](https://www.tickmill.com/blog/institutional-insights-jpmorgan-flows-positioning-130125)

**TIC (Treasury International Capital)**
- TIC is monthly, released mid-month about 1.5-2 months after the reference month. Example: August 2026 data is scheduled for 16 Oct 2026. Releases in January, April, July and October carry annual revisions. — [US Treasury TIC release dates](https://home.treasury.gov/data/treasury-international-capital-tic-system/release-dates-of-tic-data); [archived Treasury guidance (2008-09, possibly outdated)](https://webarchive.library.unt.edu/eot2008/20090109114328mp_/http://treasury.gov/tic/using-tic.shtml)

**Bank / prime-broker flow research**
- JPMorgan "Flows & Liquidity" (Panigirtzoglou), BofA "Systematic Flows Monitor" and JPM Delta-One CTA notes are client-only. Retail traders mostly see them second-hand through broker blogs, e.g. Tickmill's "Institutional Insights" recaps of BofA and JPM notes. — [Tickmill/BofA 11 Aug 2026](https://www.tickmill.com/blog/institutional-insights-bofa-systematic-flows-monitor-11826); [Tickmill/JPM Delta-One](https://try.tickmill.com/blog/institutional-insights-jpmorgan-delta-one-flows-positioning-cta-signals); [JPM Flows & Liquidity (login)](https://markets.jpmorgan.com/research/email/scx/qqk5r318/10HsEb4xefF8EZWNPbDZ-Q/GPS-4740924-0)

**Crypto exchange-native derivatives flow data (free, real time)**
- **Binance USDⓈ-M taker buy/sell volume:** `GET /futures/data/takerlongshortRatio`.
  - Periods: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d.
  - History limited to the last 30 days; rate limit 1000 requests per 5 minutes.
  - The COIN-M equivalent is `/futures/data/takerBuySellVol`.
  - [Binance docs USDⓈ-M](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Taker-BuySell-Volume); [COIN-M](https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/Taker-Buy-Sell-Volume)
- **Binance spot klines:** every kline carries "Taker buy base asset volume" and "Taker buy quote asset volume" (fields 9-10). Intervals run from 1s to 1M. The aggTrades `m` field ("Was the buyer the maker?") gives trade-level aggressor side. Together these allow a free, exact cumulative volume delta (CVD) in real time and historically. — [Binance spot market-data endpoints](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints)
- **Funding rate and open interest:** `/fapi/v1/fundingRate` and `/fapi/v1/openInterest`. — [NautilusTrader Binance client docs](https://nautilustrader.io/docs/core-latest/nautilus_binance/futures/http/client/index.html)
- **Global long/short account ratios:** available at 5m to 1d granularity (Binance-only dataset). — [Apify description](https://apify.com/ninhothedev/binance-futures-scraper)
- **Practical caveat for cloud deployments:** Binance returns HTTP 451 to many datacenter IP ranges. — [Apify page](https://apify.com/ninhothedev/binance-futures-scraper)
- **Liquidations:** WebSocket `<symbol>@forceOrder` or `!forceOrder@arr`, updated every 1000ms. Only the latest liquidation per symbol in each 1000ms window is pushed as a snapshot, and nothing is sent when no liquidation occurs. — [Binance liquidation stream docs](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams); [all-market stream](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/All-Market-Liquidation-Order-Streams)
- **Deribit DVOL (crypto implied-vol index):** free, no-auth public endpoint `public/get_volatility_index_data` returning candles for BTC/ETH. — [Deribit API reference](https://docs.deribit.com/api-reference/market-data/public-get_volatility_index_data.md); [community skill describing free no-auth use](https://skillsmp.com/creators/dongzhuoyao/finance-option-skills/plugins-option-crypto-skills-deribit-data)
- **CoinGlass (aggregated OI/funding/liquidations across venues):** the API has no free tier: Hobbyist $29/mo (30 req/min), Startup $79, Standard $299 (first tier with commercial rights), Professional $699. Dashboards are free to view. — [CoinGlass pricing](https://coinglass.com/pricing); [ComparEdge](https://comparedge.com/tools/coinglass/pricing)

**On-chain flows and stablecoins**
- **Chi, Chu & Hao (arXiv 2411.06327, v2 Sep 2025; data 2017-2023, 1-6h intervals):**
  - ETH net exchange inflows negatively predict ETH returns and volatility at all intraday intervals.
  - USDT net inflows to exchanges positively predict BTC and ETH returns at multiple intervals.
  - BTC net inflows mostly lack predictive power for BTC returns (except at 4h) but are negatively associated with volatility.
  - [arXiv abstract](https://arxiv.org/abs/2411.06327)
- Glassnode's public netflow chart is a 7-day EMA of inflows minus outflows, so the default chart is heavily smoothed. — [CostBench on Glassnode](https://costbench.com/software/onchain-analytics/glassnode)
- Glassnode Studio Advanced is reportedly $99/mo with up to 1h resolution. API access is on Professional plans priced on request. Third-party pricing figures conflict and are unverified. — [CostBench](https://www.costbench.com/software/blockchain-data-api/glassnode-api/); [cryptoactu](https://cryptoactu.com/entreprise/glassnode/)
- **Stablecoin supply:** DefiLlama's stablecoin API (stablecoins.llama.fi) is described as free, no key, updated daily, with per-chain circulating supply and 1d/7d/30d changes. These descriptions come from third-party wrappers, not official DefiLlama docs. — [eco.com on DefiLlama](https://eco.com/support/en/articles/14800367-defillama-free-tvl-and-defi-analytics); [Apify stablecoin tracker](https://apify.com/gochujang/stablecoin-supply-tracker)
- No study was found that isolates stablecoin minting as a return predictor. Large stablecoin transfers (≥$1M) show abnormal volume and returns in the surrounding hours (working paper, via search summary). — [Blockchain Research Lab](https://www.blockchainresearchlab.org/research/stablecoins/)
- **Coinbase Premium:** the Coinbase BTC/USD price minus the Binance BTC/USDT price, used by CryptoQuant as a proxy for US buyer appetite. Positive means strong US buying, negative means weak demand or selling. It was reported negative for eight straight weeks from 6 May 2026. — [Cointelegraph](https://cointelegraph.com/markets/bitcoin-coinbase-premium-hits-4-month-high-550k-btc-leaves-exchanges); [MEXC news (July 2026)](https://www.mexc.com/news/1187967)
- **Funding rates:** K33 reports that after the 30-day average funding rate flips negative, 90-day BTC returns averaged 79% (median 55%). This is only about seven episodes since 2018, so it is a contrarian, low-n, non-peer-reviewed result. — [The Block / K33 (Sept 2024)](https://www.theblock.co/post/315831/perp-signal-bitcoin-bottom-bullish-year-end-k33)
  - Coin Metrics explains funding as periodic long/short payments that keep perpetual prices anchored to spot. — [Coin Metrics docs](https://gitbook-docs.coinmetrics.io/market-data/market-data-overview/market-funding-rates-predicted)

### Inferences
- **Latency ladder:**
  - Crypto exchange derivatives data: RT (seconds).
  - On-chain exchange flows: blocks/minutes, but vendor-smoothed; usable resolution 1h on paid plans.
  - Spot ETF flows: D+0 evening (US) / D+1 (Europe morning), incomplete on day one.
  - EPFR: D+1/W (paid).
  - ICI: W with ~1-week lag.
  - COT: W with a 3-day lag.
  - TIC: M with a ~6-8 week lag.
  - **Only the first rung can drive intraday entries.**
- For a German trader, the US-evening update of Farside means the previous US session's ETF flow is known before the European open. It works as a pre-market bias / regime input for BTC and ETH, not as an intraday trigger. Mixed direction-of-causality evidence suggests flows partly chase price, so they are better as a persistence/confirmation filter.
- Because the Binance forceOrder stream only pushes the latest liquidation per symbol per second, liquidation totals built from it are lower bounds. Aggregators (CoinGlass) or full trade-stream reconstruction would be needed for exact cascade sizes.
- The 30-day history limit on `takerlongshortRatio` means the trader should log it continuously if it is to be backtested. Alternatively, rebuild taker volume from klines fields 9-10, which have long history.

### Gaps
- No primary-source statement found on the exact time of day each spot-ETF issuer publishes shares outstanding or flows. NYDIG says the prospectuses contain the workflows, but they were not checked.
- ETF.com fund-flow tool latency and terms were not verified. Bloomberg ETF flow data is paid and its latency was not researched.
- EPFR's current weekday and time of release are unverified (latest primary source is from 2014).
- No peer-reviewed study confirmed that spot-ETF flows predict next-day BTC returns out of sample.
- No academic evidence was found on open interest changes or liquidation cascades as return predictors (only practitioner commentary).
- CryptoQuant's own documentation and pricing for the Coinbase Premium and exchange netflows were not retrieved.

---

## 2. Price/volume-based flow proxies (MFI, CMF, OBV, A/D, VWAP, CVD/order-flow imbalance, taker volume, footprint, Market Profile): information content

### Takeaway
At tick/second horizons, order-flow imbalance (OFI) is the best-supported proxy. It explains most contemporaneous price change, but its forward predictability is weak and fragile. Classic bar-based "money flow" indicators (MFI, CMF, OBV, A/D) are heuristics with little peer-reviewed support. In crypto, aggressor-side data (taker buy/sell, CVD) is exact and free, while in futures/equities it requires tick data.

### Cited Findings
- **Order-flow imbalance (Cont, Kukanov & Stoikov, J. Financial Econometrics 2014; NYSE data from ~2010, so older):**
  - Over short intervals, price changes are mainly driven by OFI, i.e. the supply/demand imbalance at the best bid and ask.
  - The relation is linear, with slope inversely proportional to market depth, and it is stable across stocks and time horizons.
  - It is less noisy than the volume-based square-root impact law.
  - [arXiv 1011.6402](https://arxiv.org/abs/1011.6402); [RePEc](https://ideas.repec.org/a/oup/jfinec/v12y2014i1p47-88..html)
  - A replication on 30 Tehran stocks finds that using OFI from the first three book levels raises explanatory power. — [JFMP](https://jfmp.sbu.ac.ir/article_103073_en.html)
- **Crypto futures, "The Quarter-Hour Effect" (arXiv 2607.09426, 2026; six assets):**
  - Baseline order imbalance and imbalance at one-minute openings show little predictive association with subsequent returns.
  - Imbalance around 15-minute boundaries predicts cumulative returns over the following several hours, attributed to periodic algorithmic trading. The authors caution it is not causal price impact.
  - [arXiv 2607.09426](https://arxiv.org/pdf/2607.09426)
- **BTC jumps:** jumps tend to follow increases in trading volume and order-flow imbalance, consistent with liquidity drying up (2017 preprint, older). — [arXiv 1704.08175](https://arxiv.org/pdf/1704.08175)
- **VPIN (flow toxicity from volume-bucketed imbalance):**
  - Easley, López de Prado and O'Hara claimed it rose in the hours and days before the 2010 Flash Crash. — [SSRN 1695041](https://papers.ssrn.com/abstract=1695041)
  - Andersen and Bondarenko found it a poor predictor of short-run volatility. It peaked after, not before, the crash, and its predictive content is largely mechanical via trading intensity. — [Kellogg Insight](https://insight.kellogg.northwestern.edu/article/the_trouble_with_vpin); [Kellogg](https://www.kellogg.northwestern.edu/academics-research/research/detail/2014/vpin-and-the-flash-crash/)
  - VPIN's false-positive rate is highly parameter-dependent. The search summary attributed this to the follow-up literature; which paper says it exactly was not verified. — [Ke & Lin](https://cfr.ivo-welch.info/published/papers/ke-lin.pdf); [eScholarship VPIN study](https://escholarship.org/content/qt2sr9m6gk/qt2sr9m6gk.pdf)
- **"Money flow" as uptick minus downtick dollar volume (FAJ 2001, older):**
  - It predicts cross-sectional variation in future stock returns.
  - Predictive ability is sensitive to how money flow is measured (e.g. treatment of block trades) and to horizon.
  - [CFA Institute FAJ](https://rpc.cfainstitute.org/en/research/financial-analysts-journal/2001/can-money-flows-predict-stock-returns)
- **Chaikin Money Flow formula (StockCharts):** multiplier = [(C−L)−(H−C)]/(H−L); money flow volume = multiplier × volume; CMF(20) = Σ20 MFV / Σ20 volume.
  - StockCharts' own caveats: the multiplier ignores close-to-close changes, so CMF can disconnect from price after gaps. It is less reliable in volatile or flattening markets. Zero-line crosses whipsaw, and buffers of ±0.05 are suggested.
  - [StockCharts ChartSchool CMF](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/chaikin-money-flow-cmf)
- **Katsanos (Stocks & Commodities, July 2011)** compared seven money-flow indicators, including OBV and CMF, with two mechanical systems. The results are behind a paywall and were not retrieved. — [Traders.com](https://store.traders.com/stcov291cose.html)
- **Exchange inflows (on-chain):** ETH exchange inflows predict negative ETH returns, and USDT exchange inflows predict positive BTC/ETH returns at 1-6h horizons (2017-2023 data). — [arXiv 2411.06327](https://arxiv.org/abs/2411.06327)
- **Aggressor-side data:** taker buy/sell volume is exchange-reported per bar on Binance (exact aggressor side), at 5m+ for futures stats and down to 1s klines for spot. — [Binance taker volume](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Taker-BuySell-Volume); [Binance klines](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints)

### Inferences
- **Intraday use:** OFI/CVD is mostly a *contemporaneous* flow measure. It tells you who is aggressing *now*, which is useful to confirm that a rotation leg is being executed with real aggression (e.g. GC up with positive CVD while NQ falls with negative CVD), not as a stand-alone forecaster. The 2026 crypto paper shows that naïve 1-minute imbalance has little forward power, while specific timing structures (15-minute boundaries) do.
- MFI, CMF, OBV and A/D estimate buying/selling pressure from OHLCV bars. With exact aggressor data available free in crypto (and via tick data on IBKR futures), these bar proxies are dominated for intraday work. They may serve as cheap daily-bar confirmation filters only.
- VWAP: no evidence was gathered here. As a practitioner view (not sourced), it is mainly an execution benchmark and an intraday "fair value" anchor, so price above or below session VWAP indicates which side controlled the session.

### Gaps
- No peer-reviewed evidence was found on OBV, MFI, A/D, footprint charts or Market Profile predictive power. Katsanos's 2011 rankings were not accessible.
- No study was found on OFI predictability specifically for ES/NQ/ZN/GC futures at retail-accessible granularity.
- No study was found on CVD divergence signals in BTC spot vs perps.
- It was not verified whether IBKR's API tick-by-tick data provides trade aggressor side for futures. Many retail implementations infer side via the tick rule or a bid/ask comparison.

---

## 3. Relative-strength and rotation tools (RRG, intermarket analysis, TS/XS momentum, ratio charts)

### Takeaway
Momentum/relative strength is the best-documented "rotation" phenomenon. It is strongest at 1-12 month horizons (time-series momentum) and, intraday, as "market intraday momentum" (first half hour or rest-of-day predicts the last 30 minutes) across 60+ futures. RRG is a visualization of relative-strength trend and momentum with proprietary smoothing. Intermarket ratios (copper/gold, SPY/TLT, BTC/NDX) are regime-dependent, and several classic relationships (stock-bond negative correlation, BTC-Nasdaq coupling) have shifted recently.

### Cited Findings
- **Relative Rotation Graphs (Julius de Kempenaer):**
  - x-axis is the JdK RS-Ratio (a normalized trend of price/benchmark), y-axis the JdK RS-Momentum (rate of change of RS-Ratio). Both are centered on 100, giving four quadrants.
  - The exact smoothing and normalization are proprietary.
  - [LuxAlgo](https://www.luxalgo.com/library/concept/relative-rotation-graphs.md); [Tradejini](https://www.tradejini.com/blogs/relative-rotation-graph-rrg-explained); [TradingView RRG script](https://www.tradingview.com/script/kM0VZhlD-RK-RRG)
- **Time-series momentum (Moskowitz, Ooi & Pedersen, JFE 2012; 58 futures, 1985-2009, older):**
  - The past 12-month excess return predicts the future return.
  - Returns persist 1-12 months and then partially reverse.
  - It worked for every contract examined and performed best in extreme markets.
  - [SSRN](https://papers.ssrn.com/abstract=2089463); [AQR dataset](https://www.aqr.com/Insights/Datasets/Time-Series-Momentum-Original-Paper-Data)
- **Market intraday momentum (Gao, Han, Li & Zhou, JFE 2018; SPY 1993-2013, older):**
  - The first half-hour return (from the prior close) predicts the last half-hour return.
  - The effect is stronger on volatile days, high-volume days, recession days and macro-news days, and it also holds in 10 other ETFs.
  - In-sample R² is about 2%.
  - [Alpha Architect](https://alphaarchitect.com/2014/08/attention-prop-traders-the-first-half-hour-of-trading-predicts-the-last-half-hour/); [WUSTL profile](https://profiles.wustl.edu/en/publications/market-intraday-momentum/); [CXO Advisory](https://www.cxoadvisory.com/?p=25481)
- **Baltussen, Da, Lammers & Martens (JFE 2021):**
  - In 60+ futures across equities, bonds, commodities and FX (1974-2020), the last-30-minute return is positively predicted by the rest-of-day return. This is economically and statistically highly significant and reverts over the next days.
  - The effect is linked to short-gamma hedging by option dealers and to leveraged-ETF rebalancing.
  - [Erasmus repository](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/); [Notre Dame PDF](https://www3.nd.edu/~zda/intramom.pdf); [Alpha Architect](https://alphaarchitect.com/hot-topic-does-gamma-hedging-actually-affect-stock-prices/)
- **CTA horizon sleeves (arXiv 2510.23150, 2020-2025):** single-horizon sleeves of 20, 60, 125, 250 and 500 days were tested. The 20- and 500-day sleeves outperformed, while the 60- and 125-day sleeves whipsawed. This is one backtest window only. — [arXiv 2510.23150](https://arxiv.org/pdf/2510.23150)
- **Intermarket analysis (John Murphy):**
  - Murphy's framework covers dollar vs commodities, stocks vs commodities, stocks vs the dollar, and bonds vs stocks/commodities.
  - He applies relative-strength analysis to ETFs for global asset allocation and rotation.
  - [Wiley](https://www.wiley-vch.de/de/fachgebiete/finanzen-wirtschaft-recht/trading-with-intermarket-analysis-978-1-119-21001-6); [StockCharts bio](https://stockcharts.com/articles/bios/john-murphy.html)
  - Wikipedia lists his death as 7 Feb 2026 (single source). — [Wikipedia](https://en.wikipedia.org/wiki/John_Murphy_(technical_analyst))
- **Stock-bond correlation regime:**
  - A Markov-switching study of SPY/TLT (2007-2023) finds that in 2022 both assets were in "crisis" regimes simultaneously, so the Treasury safe-haven role fails in inflation-driven downturns. — [Šikić (2025), Hrčak](https://hrcak.srce.hr/341058)
  - Robeco (US data back to 1875) finds high inflation or real rates coincide with positive stock-bond correlation. — [Robeco 2024](https://www.robeco.com/it-it/approfondimenti/2024/05/new-research-into-the-stock-bond-correlation-shows-when-they-correlate-and-when-they-don-t)
  - Invesco claims stocks and bonds were positively correlated 98% of the time when 5-year inflation was above 3% (practitioner claim). — [Trustnet](https://www.trustnet.com/news/13441497/higher-inflation-means-bonds-no-longer-protect-investors-when-stocks-fall)
- **Copper/gold ratio:** historically tracked long-term yields and growth sentiment, but the link reportedly unraveled after the pandemic (China slowdown, inflation/deficit-driven yields). Correlation figures quoted online are undated and unverified. — [ETF Trends](https://etftrends.com/etf-strategist-channel/copper-gold-treasurys-new-world/); [Wealth Professional](https://www.wealthprofessional.ca/partner-content/coppergold-ratio/324598)
- **BTC vs Nasdaq:**
  - The short-window (20-30 day) correlation was near zero in 2025-26 snapshots, yet BTC still sells off with Nasdaq drawdowns (asymmetric, downside coupling). — [Forex.com](https://www.forex.com/en-uk/news-and-analysis/the-nasdaq-to-bitcoin-correlation-is-alive-and-well-during-risk-off/?amp=true); [Decrypt (Sept 2025)](https://decrypt.co/338795/bitcoins-tech-stock-correlation-risks-deeper-drawdowns); [Sharpe.ai tracker (May 2026)](https://www.sharpe.ai/correlation/bitcoin-vs-nasdaq)
  - Ecoinometrics found BTC lagged and then followed NDX in the Nov 2022, Aug 2024 and Apr 2025 episodes. — [Decrypt](https://decrypt.co/338795/bitcoins-tech-stock-correlation-risks-deeper-drawdowns)
- **Dollar as risk barometer (BIS):** the dollar supplanted the VIX as the variable most associated with banks' leverage appetite. A strong dollar means weak risk appetite, with wider cross-currency basis and less cross-border dollar lending (2016-17, older). — [BIS press release](https://bis.org/press/p161115.htm); [BIS addendum](https://www.bis.org/publ/work592_addendum.pdf)
  - A 2026 J. Futures Markets paper treats the stronger-dollar / wider-basis link as established. — [Essex repository](https://repository.essex.ac.uk/42654/1/2026_Journal%20of%20Futures%20Markets%20-%20The%20Dollar%20s%20Double%20Life.pdf)

### Inferences
- **For an intraday rotation system:**
  - Compute a live cross-sectional ranking of intraday returns, e.g. since the session open or the last N minutes, volatility-normalized, across a fixed basket: ES, NQ, RTY, ZN/ZB, GC, SI, HG, CL, 6J, 6S, 6E, DX, BTC, ETH.
  - Combine it with Gao/Baltussen-style intraday momentum, which is the most robust published intraday effect and exists in bonds, commodities and FX futures too. It is a late-session continuation effect, not an all-day one.
- The "safe haven" destination is regime-dependent. In an inflationary regime Treasuries may fall alongside equities, so the system should infer the destination from live relative strength (gold vs ZN vs JPY vs CHF vs USD), not hard-code risk-off = long Treasuries.
- RRG is a visualization of the same RS-trend/RS-momentum idea. An open-source approximation, e.g. a smoothed ratio plus its rate of change, can be computed on intraday bars, but there is no published evidence of RRG-specific intraday edge.

### Gaps
- No peer-reviewed out-of-sample test of RRG signals was found.
- No primary 2025-26 study on intraday lead-lag between BTC and NQ was found. Claims of "4-18 hour" leads come from low-quality blogs.
- Market intraday momentum post-2020 in the presence of 0DTE options was not specifically checked.

---

## 4. Statistical regime / risk-appetite measures (RORO indices, PCA, absorption ratio, turbulence, correlation shifts, HMM)

### Takeaway
The academically documented, free and reproducible tools are:
- the Kansas City Fed RORO index (first principal component of daily changes in credit, equity vol, funding, FX/gold; daily and weekly CSV),
- Kritzman's absorption ratio (share of variance explained by the top N/5 eigenvectors),
- the turbulence index (Mahalanobis distance; turbulence is persistent),
- Markov-switching/HMM regime models.

Bank indices (GS RAI, HSBC RORO, Citi, UBS/CS) are proprietary and not available to retail. All of these are daily-data constructs, best as a regime filter, though a retail trader can compute absorption ratio and turbulence on intraday returns themselves.

### Cited Findings
- **KC Fed RORO (Chari, Dilts Stedman & Lundblad):**
  - Built from daily US and euro-area market data in four categories: advanced-economy credit risk, equity-market volatility, funding conditions, and currencies & gold.
  - The index is the first principal component of daily changes. It shows negative skew and fat tails, is broader than the VIX, and helps with international reallocation and return prediction.
  - [NBER w31907](https://www.nber.org/papers/w31907); [KC Fed RWP 24-12](https://www.kansascityfed.org/research/research-working-papers/risk-onrisk-off-measuring-shifts-in-investor-sentiment/)
  - Data is published as roro_daily.csv and roro_weekly.csv. The page does not state update frequency or lag. — [KC Fed RORO page](https://www.kansascityfed.org/data-and-trends/risk-on-risk-off-index/); [data page](https://www.kansascityfed.org/data-and-trends/risk-on-risk-off-index-data)
- **HSBC RORO (2010-12 era, older):** an index of how closely 34 assets (stocks, bonds, commodities, currencies) move together, launched November 2010. Readings ≥0.3 are read as sentiment-dominated markets. It originated with Oxford researchers. — [Euromoney](https://www.euromoney.com/?p=71295); [REF impact case study](https://impact.ref.ac.uk/casestudies/CaseStudy.aspx?Id=20291); [Nomura glossary (JP)](https://www.nomura.co.jp/terms/japan/ri/A02552.html)
- **Goldman Sachs Risk Appetite Indicator:** no official methodology was found publicly. Retail replications (TradingView) use HY spreads, VIX and SPY/IEF and acknowledge that GS uses undisclosed proprietary elements. — [TradingView GS RAI proxy](https://de.tradingview.com/script/KEPvkE6t-Goldman-Sachs-Risk-Appetite-Proxy)
- **Absorption ratio (Kritzman, Li, Page & Rigobon, JPM 2011, older):**
  - Fraction of total variance explained by a fixed number of top eigenvectors, with K = N/5 assets.
  - High AR means tightly coupled markets where shocks propagate faster and more broadly.
  - Most significant US drawdowns were preceded by AR spikes.
  - [State Street summary](https://globalmarkets.statestreet.com/research/portal/insights/article/2a8e282a-343b-443c-b362-1634c71d2d26); [arXiv 2002.02008 restating the definition](https://arxiv.org/pdf/2002.02008); [Top1000funds](https://www.top1000funds.com/uncategorised/condition-the-condition-you%e2%80%99re-in/)
- **Turbulence index (Kritzman & Li, FAJ 2010, older):**
  - Essentially the (squared) Mahalanobis distance of the current return vector from its historical mean/covariance. It captures extreme moves, decoupling of correlated assets and convergence of uncorrelated ones.
  - Returns to risk are lower in turbulent periods, and turbulence is persistent, typically lasting weeks.
  - [Alpha Architect](https://alphaarchitect.com/skulls-financial-turbulence-and-risk-management/); [PortfolioOptimizer](https://portfoliooptimizer.io/blog/the-turbulence-index-measuring-financial-risk/); [RePEc](https://ideas.repec.org/a/taf/ufajxx/v66y2010i5p30-41.html)
  - Combining AR with turbulence yields a fragility/resilience index. — [Top1000funds](https://www.top1000funds.com/uncategorised/condition-the-condition-you%e2%80%99re-in/)
  - A 2021 extension adds VAR-based and signed turbulence for bull/bear change points. — [Hitotsubashi WP](https://www.fs.hub.hit-u.ac.jp/inc/files/staff-research/workingpaper/FS-2021-E-001.pdf)
- **Regime models / HMM (Kritzman, Page & Turkington, FAJ 2012):**
  - Markov-switching models for turbulence, inflation and growth regimes. Dynamic allocation beat static, mainly for avoiding large losses. — [RePEc](https://ideas.repec.org/a/taf/ufajxx/v68y2012i3p22-39.html)
  - Later student theses are mixed: one finds regime strategies struggle versus static benchmarks, apart from some turbulence-based alphas; another finds an HMM-overlaid risk parity lowered out-of-sample drawdowns. — [UCP thesis 2024](https://repositorio.ucp.pt/bitstreams/0c68578b-5c05-421d-9778-8006d9744279/download); [Gothenburg thesis 2024](https://gupea.ub.gu.se/items/e6c1a03d-2b35-4f5a-85ce-8fd4b0f8ba2f)
- **OFR Financial Stress Index:** 33 market variables in five categories (credit, equity valuation, funding, safe assets, volatility) with regional breakdown. It publishes with data from two business days prior, and values are not revised. — [OFR FSI](https://www.financialresearch.gov/financial-stress-index); [OFR WP 17-04](https://www.financialresearch.gov/working-papers/files/OFRwp-17-04_The-OFR-Financial-Stress-Index.pdf)

### Inferences
- The published indices (KC Fed RORO, OFR FSI) have a lag of at least a day (OFR explicitly two business days), so they are regime filters only.
- A retail trader can rebuild the *mechanics* in real time on IBKR data. Examples:
  - A rolling PCA, absorption ratio and Mahalanobis turbulence on 5- to 30-minute returns of about 10-15 futures/FX/crypto instruments.
  - A live "RORO factor" as PC1 of returns across ES, NQ, HG, CL, AUDJPY versus ZN, GC, JPY, CHF, with the sign fixed by equity loading.
  - These intraday versions are the trader's own constructions. They are not validated by the cited papers, which used daily data.
- Turbulence persistence (weeks) supports using a turbulence/AR spike as a regime switch that changes the system's behavior for days, e.g. favoring risk-off rotations and reducing long-risk exposure, rather than as a precise entry signal.

### Gaps
- No public methodology was found for GS RAI, Citi Macro Risk Index or UBS/CS Risk Appetite Index. The Citi index was not found at all.
- The KC Fed RORO update cadence and lag are not documented on its page.
- The exact AR window (often cited as 500 days) and the "standardized shift" thresholds could not be verified from primary text.

---

## 5. Stress/fear gauges usable intraday (VIX and term structure, MOVE, credit, FX vol, JPY/CHF, funding stress, put/call, GEX)

### Takeaway
Cheapest real-time gauges for a retail IBKR user:
- VIX (via IBKR's Cboe index feed) and VIX futures,
- the crypto vol index DVOL (free from Deribit),
- intraday ETF/futures proxies for credit and rates stress (e.g. HYG/LQD vs IEF/ZN price ratios),
- JPY/CHF moves in futures or spot FX.

MOVE is real time only through ICE's paid feeds (Yahoo is delayed). HY OAS on FRED is daily and now license-truncated. SOFR is next-morning. Cboe put/call is published intraday as half-hourly snapshots. GEX is daily (SqueezeMetrics) or paid real time.

### Cited Findings
- **VIX on IBKR:** IBKR's "CBOE Streaming Market Indexes" subscription provides L1 for Cboe indices (SPX, VIX). — [IBKR popular subscriptions](https://www.interactivebrokers.com/docs/general/market-data-subscriptions/popular-market-data-subscriptions/introduction); [QuantConnect IB data docs](https://www.quantconnect.com/docs/v2//cloud-platform/datasets/interactive-brokers)
  - Cboe also sells a 24/7 streaming index feed (Cboe Global Indices, Main incl. S&P, FTSE Russell, MSCI channels). — [Cboe Global Indices Feed](https://www.cboe.com/en/data/global-indices-feed/)
  - VIX3M availability via IBKR could not be confirmed. A QuantConnect thread says it is not modeled in LEAN, which is a QuantConnect limitation. — [QuantConnect forum](https://www.quantconnect.com/forum/discussion/11852/vix3m-index/)
- **VIX term structure evidence:**
  - Academic (EFMA 2013, sample 2006-2011, older): the VIX futures basis forecasts VIX futures returns but not changes in spot VIX. Trading against the basis, hedged with S&P futures, was profitable after costs. — [EFMA 2013 paper](https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2013-Reading/papers/EFMA2013_0164_fullpaper.pdf)
  - Vendor backtest (unverified): since 2010, from the first day of a backwardation episode SPY averaged +3.9% over the next quarter (75% positive). Persistent episodes (2011, 2018, 2020) coincided with real drawdowns. — [thetrading.tools](https://www.thetrading.tools/manuals/vix-term-structure)
  - Cboe indices keep updating after the 4:15pm settlement, so scraped evening values can differ from official settlements. — [thetrading.tools](https://www.thetrading.tools/manuals/vix-term-structure)
- **MOVE index:** ICE has published MOVE in near real time since 2020 via paid ICE feeds (Consolidated Feed, ICE Data API). Yahoo ^MOVE is labeled "Delayed Quote". — [ICE developer catalog](https://developer.ice.com/fixed-income-data-services/catalog/ice-data-indices-move-index); [ICE press release 2020](https://ir.theice.com/press/news-details/2020/ICE-Data-Services-Launches-Real-Time-Publication-of-Key-Fixed-Income-Indices/default.aspx); [Yahoo ^MOVE](https://finance.yahoo.com/quote/%5EMOVE)
- **HY credit spreads (FRED BAMLH0A0HYM2):** daily ICE BofA HY OAS under ICE licence terms. Secondary sources report FRED now keeps only a rolling 3 years of observations, starting April 2026. — [FRED series graph](https://fred.stlouisfed.org/graph/?g=11lXE); [eco3min dataset note](https://eco3min.fr/en/credit-spreads-recession-risk-dataset/)
- **Funding stress (SOFR):** the NY Fed publishes SOFR around 8:00am ET each business day, reflecting the previous day's transactions. It is useless intraday. — [NY Fed SOFR](https://www.newyorkfed.org/markets/reference-rates/sofr); [NY Fed SOFR averages](https://www.newyorkfed.org/markets/reference-rates/sofr-averages-and-index)
- **Cross-currency basis:** widens with dollar strength and falling risk appetite (BIS). No free real-time source was found. — [BIS](https://bis.org/press/p161115.htm)
- **Put/call ratios:**
  - Cboe's U.S. Options Market Volume Summary shows intraday half-hourly P/C snapshots (example 22 Sep 2025: 0.65 at 09:00 CT to 0.70 at 12:00 CT). — [Cboe market statistics](https://res.cboe.com/us/options/market_statistics)
  - The daily pages give total, equity, index and VIX P/C ratios. — [Cboe daily statistics](https://www.cboe.com/us/options/market_statistics/daily/)
  - Per-minute P/C data is available via Cboe DataShop (paid). — [Cboe insights](https://www.cboe.com/insights/posts/how-early-exercise-order-flow-impacts-equity-option-put-call-ratios)
- **Dealer gamma (GEX):**
  - SqueezeMetrics introduced GEX in a December 2017 white paper. The dealer-sign assumption is a simplifying heuristic. — [abouttrading substack](https://abouttrading.substack.com/p/the-gamma-exposure-trading-strategy)
  - SqueezeMetrics publishes DIX/GEX as a daily series. A free CSV download was reported in 2020-era tutorials, and current terms are unverified. Paid real-time GEX vendors include SpotGamma, FlashAlpha, Unusual Whales and SqueezeMetrics. Price claims conflict: roughly $200-1,000/mo vs $720/mo. — [FlashAlpha comparison](https://flashalpha.com/articles/best-gex-api-2026-flashalpha-vs-spotgamma-vs-unusual-whales); [NexusFi](https://nexusfi.com/d/data-providers/squeezemetrics-prior-analytics-llc)
  - The mechanism is documented: dealer short-gamma hedging produces intraday momentum into the close. — [Baltussen et al. 2021](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/)
- **Crypto implied vol:** Deribit DVOL candles are free via the public API. — [Deribit API](https://docs.deribit.com/api-reference/market-data/public-get_volatility_index_data.md)
- **Daily composite stress:** the OFR FSI (two-business-day lag) is the official free composite. — [OFR FSI](https://www.financialresearch.gov/financial-stress-index)

### Inferences
- **Real-time stress dashboard feasible with IBKR plus free sources:**
  - VIX level and change (Cboe indices sub).
  - VIX futures front-vs-second-month spread as a term-structure proxy, if CFE data is subscribed. CFE availability and price were not verified.
  - HYG/IEF or LQD/IEF price ratio (US equity/ETF data) as an intraday credit-stress proxy.
  - ZN/ZB futures and 6J/6S futures for flight-to-quality.
  - USDJPY/USDCHF spot from IBKR's free IDEALPRO FX quotes. This is my understanding, not verified here.
  - BTC DVOL, perp funding and liquidations from the free crypto APIs.
- MOVE intraday can only be approximated, e.g. via realized volatility of ZN futures or Treasury option implieds if subscribed. FRA-OIS, cross-currency basis and SOFR are not available intraday for free.
- Treat put/call and GEX as daily context. A GEX regime (positive vs negative dealer gamma) indicates whether intraday moves are likely damped or amplified (mechanism per Baltussen et al.), but real-time GEX is paid.

### Gaps
- Not verified: whether IBKR's Cboe index subscription includes VIX3M, VIX9D, VVIX or MOVE, and the current CFE (VIX futures) data fee.
- No free real-time source for FX implied volatility (e.g. CVIX or JPY vol) was found.
- No current (2026) peer-reviewed evidence on VIX/VIX3M ratio thresholds for intraday timing was found.

---

## 6. Positioning / forced-flow models (CTA triggers, vol-targeting, risk parity, leveraged ETFs, month-/quarter-end rebalancing, options expiry/gamma)

### Takeaway
Forced or mechanical flows are the most "predictable" capital flows. The sell-side estimates them with models of the rule-based strategies (CTA trend signals with multiple lookbacks, vol-control funds keyed to realized vol, leveraged-ETF rebalancing into the close, calendar rebalancing by pensions). A retail trader can approximate the mechanics using public price data, but the AUM/positioning inputs are unobservable and estimates differ widely. Commercial products (Kpler Financial Flows, bank notes) are paid.

### Cited Findings
- **CTA trend followers:**
  - BofA's Systematic Flows Monitor models 12 trend-following strategies by speed. In the August 2026 note, faster CTAs were less bullish than slower ones after a mid-July drawdown, and meaningful CTA equity selling would generally need declines of more than 4% from spot. — [Tickmill/BofA 11 Aug 2026](https://www.tickmill.com/blog/institutional-insights-bofa-systematic-flows-monitor-11826)
  - BofA's June 2025 note reported five of 12 models stopped out on one day. — [Tickmill/BofA 16 Jun 2025](https://www.tickmill.com/blog/institutional-insights-bofa-systematic-flow-monitor-160625)
  - TD Securities' CTA tracker defines a "nearest trigger" as one within 1 standard deviation of price. — [substack PDF](https://vblgoldfix.substack.com/api/v1/file/248a88bb-5cbc-415f-a85d-07a9a3efa6bc.pdf)
  - JPM Delta-One notes report e.g. "US large-cap equities within ~1-2% of critical short-term CTA signals" (second-hand). — [Tickmill/JPM](https://try.tickmill.com/blog/institutional-insights-jpmorgan-delta-one-flows-positioning-cta-signals)
  - Kpler Financial Flows models the systematic strategies themselves to estimate positioning, execution levels and potential future order flow. Kpler reports 0.901 correlation to major CTA benchmarks over the past quarter (~0.89 full history). It does not publish lookbacks. — [Kpler blog Aug 2026](https://www.kpler.com/blog/the-hidden-layer-of-commodity-markets-understanding-systematic-cta-flows); [Kpler product](https://www.kpler.com/product/commodities/kpler-financial-flows-vs-other-providers)
  - JPM's Panigirtzoglou describes CTAs as largely price-momentum-based. — [Globe and Mail](https://beta.theglobeandmail.com/globe-investor/inside-the-market/bullishness-in-silver-supports-near-term-commodity-downside-says-analyst/article34290435/)
- **Volatility-control / vol-targeting funds:**
  - They react to realized, not implied, volatility. They often use exponential smoothing of short and long windows to de-lever fast and re-lever slowly, e.g. the maximum of 20-day and 60-day vol with a 10% target. — [Acadian](https://www.acadian-asset.com/-/media/files/commentary-pdfs/acadian--defensive-investing-strategies-feedback-loops-and-echoes-of-1987.pdf); [Macro Manv / MacroTourist](https://manveersahota.substack.com/p/the-vol-control-playbook-a-macro)
  - Flow estimates vary widely. Barclays estimated $225bn of possible equity sales in Feb 2018 (older). — [Gulf News/PressReader](https://pressreader.com/uae/gulf-news/20180207/282355450194602)
  - Tier1 Alpha estimated about $15bn sold in one day (April 2024). — [Hedgeye](https://app.hedgeye.com/insights/149510-april-24th-2024-an-uptick-in-realized-volatility?type=%2C)
  - Nomura (April 2026) puts the vol-control universe at about $1.3tn and said the most aggressive de-risking may have passed. — [Invezz](https://invezz.com/en-ae/news/2026/04/08/volatility-funds-near-end-of-selling-spree-nomura-sees-stock-bounce/)
  - Milliman argues the flows are trivial versus total market volume. — [Milliman](https://milliman.com/-/media/milliman/importedfiles/ektron/vol_control_funds.ashx)
- **Leveraged/inverse ETF rebalancing:**
  - Funds must buy after up days and sell after down days near the close, in proportion to the day's move. Estimates for 13 Sept 2022 were about $15.5bn (Nomura) to over $20bn of equities sold.
  - The price impact is disputed: one study finds close-of-day effects that revert at the next open, and a 2024 survey calls most evidence methodologically weak and economically insignificant.
  - [AMRO](https://amro-asia.org/do-leveraged-etfs-make-markets-more-volatile); [Bank Underground (BoE)](https://bankunderground.co.uk/2023/08/31/leveraged-and-inverse-etfs-the-exotic-side-of-exchange-traded-funds/); [St. Gallen survey](https://www.alexandria.unisg.ch/server/api/core/bitstreams/5a99db31-0d37-4f86-9502-8cb0f3bff4fe/content); [Nasdaq](https://www.nasdaq.com/articles/leveraged-etfs-trigger-volatility-market-rebalancing-intensifies)
- **Pension / calendar rebalancing (Harvey, Mazzoleni & Melone, NBER w33554, 2025):**
  - When equities are overweight, funds sell stocks and buy bonds, which lowers equity returns by about 17bp over the next day.
  - It costs investors about $16bn a year.
  - Calendar (monthly/quarterly) and threshold rebalancing create predictable, front-runnable signals.
  - [NBER](https://www.nber.org/papers/w33554); [Duke Fuqua](https://www.fuqua.duke.edu/duke-fuqua-insights/what-do-pensions-lose-from-rebalancing); [EDHEC slides Feb 2026](https://www.edhec.edu/sites/default/files/2026-03/slides_EDHEC_Michele%20Mazzoleni%20%281%29.pdf)
- **Options hedging / gamma:** dealer short-gamma hedging forces with-trend trading, which drives last-30-minute momentum across 60+ futures. — [Baltussen et al. JFE 2021](https://www3.nd.edu/~zda/intramom.pdf)
- **COT-based positioning:** JPM proxies hedge-fund and momentum-trader equity positioning via z-scores of net CFTC positions as a share of open interest (weekly, three-day lag). — [Tickmill/JPM](https://www.tickmill.com/blog/institutional-insights-jpmorgan-flows-positioning-130125)

### Inferences
- **Retail approximations computable from IBKR price data:**
  - (a) A CTA proxy: an ensemble of moving-average or breakout signals at 20, 60, 125 and 250 days per futures market, vol-scaled to a risk target. Output: estimated net position and the price levels at which each sleeve flips ("trigger levels"). The 1-standard-deviation proximity rule mirrors TD's convention.
  - (b) A vol-control proxy: realized 20- and 60-day vol of ES/SPX versus a 10-12% target gives the direction and rough magnitude of equity exposure changes. A realized-vol jump implies selling over the following days.
  - (c) An LETF rebalancing estimate: sign and size are proportional to the day's index return × leverage × (leverage − 1) × LETF AUM, concentrated in the last hour. LETF AUM is available from issuers.
  - (d) A month-end/quarter-end calendar flag using the month-to-date equity-vs-bond return differential (Harvey et al.).
- These models give *anticipated* flows, the only forward-looking flow information retail can get. Validation against realized moves is essential, given the huge dispersion of published estimates.

### Gaps
- No public methodology document was found that gives the exact lookbacks and weights banks use for CTA trigger levels.
- No AUM estimates for CTAs or risk parity in 2026 were retrieved (Nomura's ~$1.3tn vol-control figure is second-hand).
- Risk-parity deleveraging mechanics were not specifically sourced.
- The Cheng & Madhavan (2009) original LETF paper was not retrieved.
- No source was found on retail-accessible daily LETF AUM aggregation.

---

## 7. What can be computed in real time from IBKR data and free crypto APIs (Binance, Coinbase, Deribit)?

### Takeaway
Everything that is *price-, volume-, aggressor- or derivatives-microstructure-based* can be computed in real time. Concretely, the system can be built on:
- cross-asset futures, FX and ETFs plus VIX from IBKR,
- free Binance/Coinbase/Deribit streams for crypto (taker flow/CVD, OI, funding, liquidations, Coinbase premium, DVOL).

Every *reported-flow* dataset (ETF flows, COT, ICI/EPFR, TIC, FRED spreads, SOFR, RORO/OFR indices) is D+0 to M lag and belongs to the regime layer.

### Cited Findings
- **IBKR data packages:**
  - The "US Securities Snapshot and Futures Value Bundle" is USD 10/month, waived with at least USD 30 monthly commissions. It provides real-time top-of-book for CBOT, CME, COMEX and NYMEX. "Futures Value PLUS" adds Level-2 depth.
  - Real-time CME data requires an annually re-affirmed non-professional questionnaire. Snapshot quotes cost USD 0.01 each (USD 1 monthly waiver).
  - The knowledge-base articles say to verify current rates.
  - [IBKR KB](https://ibkb.interactivebrokers.com/fr/node/2840); [IBKR market data pricing](https://www.interactivebrokers.com/en/pricing/research-news-marketdata.php)
- **Cboe indices (VIX) on IBKR:** via the "CBOE Streaming Market Indexes" subscription. — [IBKR](https://www.interactivebrokers.com/docs/general/market-data-subscriptions/popular-market-data-subscriptions/introduction)
- **Binance (free):**
  - Spot klines with taker buy volume (1s-1M) and aggTrades with aggressor flag. — [Binance spot API](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints)
  - Futures taker buy/sell volume (5m+, 30 days of history). — [Binance futures data](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Taker-BuySell-Volume)
  - Funding and OI. — [NautilusTrader](https://nautilustrader.io/docs/core-latest/nautilus_binance/futures/http/client/index.html)
  - Liquidation stream (1s snapshots). — [Binance](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams)
  - Possible HTTP 451 from datacenter IPs. — [Apify](https://apify.com/ninhothedev/binance-futures-scraper)
- **Deribit (free):** DVOL candles via the public API. — [Deribit](https://docs.deribit.com/api-reference/market-data/public-get_volatility_index_data.md)
- **Coinbase premium:** defined as the price difference between Coinbase BTC/USD and Binance BTC/USDT, so it can be computed from both venues' public tickers. — [Cointelegraph/CryptoQuant](https://cointelegraph.com/markets/bitcoin-coinbase-premium-hits-4-month-high-550k-btc-leaves-exchanges)
- **Not real-time / not free:**
  - CoinGlass API (paid from $29/mo). — [CoinGlass](https://coinglass.com/pricing)
  - Glassnode fine resolution (paid). — [CostBench](https://www.costbench.com/software/blockchain-data-api/glassnode-api/)
  - MOVE real time (ICE paid). — [ICE](https://developer.ice.com/fixed-income-data-services/catalog/ice-data-indices-move-index)
  - Real-time GEX (paid). — [FlashAlpha](https://flashalpha.com/articles/best-gex-api-2026-flashalpha-vs-spotgamma-vs-unusual-whales)
  - EPFR (paid). — [CEIBS](https://ceibs.libguides.com/az/epfr-data)

### Inferences

**Master catalogue (latency × cost × usefulness).** Usefulness ratings are my assessment based on the findings above.

| Method / data | What it measures | Latency | Cost / source | Intraday usefulness | Regime-filter usefulness |
|---|---|---|---|---|---|
| Cross-asset intraday return ranking (ES, NQ, ZN, GC, 6J, 6S, CL, HG, BTC…) | Where marginal capital is going *now* (relative strength) | RT | IBKR futures bundle ~$10/mo ([IBKR KB](https://ibkb.interactivebrokers.com/fr/node/2840)) | **High (core signal)** | High (daily/12m TSMOM, [MOP 2012](https://papers.ssrn.com/abstract=2089463)) |
| Market intraday momentum (rest-of-day → last 30 min) | Late-session continuation from hedging/rebalancing | RT | IBKR | **High, well documented** ([Baltussen 2021](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/); [Gao 2018](https://profiles.wustl.edu/en/publications/market-intraday-momentum/)) | n/a |
| OFI / CVD / taker buy-sell (crypto exact; futures via tick data) | Aggressor imbalance | RT | Binance free ([docs](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints)); IBKR ticks | Medium: strong contemporaneous, weak forward ([Cont 2014](https://arxiv.org/abs/1011.6402); [arXiv 2607.09426](https://arxiv.org/pdf/2607.09426)) | Low |
| Perp OI change, funding, liquidations | Leverage build-up and forced unwinds | RT (1s liquidation snapshots) | Binance free ([forceOrder](https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams)); CoinGlass paid | Medium (cascade detection) | Medium (funding extremes, contrarian, low-n per [K33](https://www.theblock.co/post/315831/perp-signal-bitcoin-bottom-bullish-year-end-k33)) |
| Coinbase premium | US vs offshore BTC demand | RT (computed) | Free (two public tickers) | Medium (confirmation) | Medium |
| DVOL (Deribit) | Crypto implied vol | RT | Free ([Deribit](https://docs.deribit.com/api-reference/market-data/public-get_volatility_index_data.md)) | Medium (stress gauge) | Medium |
| VIX level/change; VIX futures curve | Equity fear / term structure | RT | IBKR Cboe indices sub; VX futures need CFE sub (unverified) | **High as stress trigger** | High (backwardation episodes; [EFMA 2013](https://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2013-Reading/papers/EFMA2013_0164_fullpaper.pdf)) |
| Credit ETF ratios (HYG/IEF, LQD/IEF) | Intraday credit-stress proxy | RT | IBKR US equity data | Medium (my inference; no study found) | Medium |
| HY OAS (FRED) | Credit spread | D+1 | Free, 3y history only since Apr 2026 ([eco3min](https://eco3min.fr/en/credit-spreads-recession-risk-dataset/)) | None | High |
| MOVE | Rates implied vol | RT paid / delayed free | ICE paid; Yahoo delayed ([Yahoo](https://finance.yahoo.com/quote/%5EMOVE)) | Low for retail | High |
| Put/call (Cboe) | Options hedging demand | ID half-hourly snapshots / D | Free web ([Cboe](https://res.cboe.com/us/options/market_statistics)) | Low-Medium | Medium |
| GEX | Dealer gamma regime | D (free, unverified) / RT paid | SqueezeMetrics; SpotGamma etc. | Medium if paid RT | Medium |
| Spot BTC/ETH ETF flows | Real creations/redemptions | D+0 US evening, revised ([Farside](https://farside.co.uk/)) | Free | **None for entry**; pre-session bias | High for crypto regime |
| ICI fund flows | Mutual fund / ETF flows | W (~1 week lag) | Free ([ICI](https://www.ici.org/research/stats/flows)) | None | Low-Medium |
| EPFR | Global fund flows | D+1 / W | Paid institutional ([CEIBS](https://ceibs.libguides.com/az/epfr-data)) | None | High (if affordable) |
| CFTC COT | Positioning by trader type | W, Tue data → Fri 15:30 ET ([CFTC](https://www.cftc.gov/MarketReports/CommitmentsOfTraders/index.htm)) | Free | None | Medium (crowding z-scores) |
| TIC | Foreign purchases of US securities | M, ~6-8 week lag ([Treasury](https://home.treasury.gov/data/treasury-international-capital-tic-system/release-dates-of-tic-data)) | Free | None | Low (structural only) |
| KC Fed RORO | PC1 of credit/vol/funding/FX-gold | D/W CSV, lag undocumented ([KC Fed](https://www.kansascityfed.org/data-and-trends/risk-on-risk-off-index/)) | Free | None (rebuild live yourself) | High |
| OFR FSI | 33-variable stress composite | D, 2-business-day lag ([OFR](https://www.financialresearch.gov/financial-stress-index)) | Free | None | High |
| Absorption ratio / turbulence (self-computed) | Market coupling / unusualness | RT if computed on intraday returns | Free (own computation) | Medium (regime switch; persistent per [Kritzman & Li](https://alphaarchitect.com/skulls-financial-turbulence-and-risk-management/)) | High |
| HMM / Markov regimes | Latent risk regimes | Model-dependent | Free (own computation) | Low-Medium | Medium (mixed evidence: [KPT 2012](https://ideas.repec.org/a/taf/ufajxx/v68y2012i3p22-39.html)) |
| CTA / vol-control / LETF / month-end models | Anticipated mechanical flows | Levels known in advance (computed from prices) | Free proxies; paid (Kpler, bank notes) | Medium-High around trigger levels, the close and month-end | High |
| On-chain exchange netflows / stablecoin supply | Coins moving to/from exchanges; dry powder | 1h-D (vendor) | Glassnode/CryptoQuant paid; DefiLlama free daily | Low-Medium (1-6h evidence: [arXiv 2411.06327](https://arxiv.org/abs/2411.06327)) | Medium |
| MFI / CMF / OBV / A-D | Bar-based buying/selling pressure | RT on bars | Free | Low (weak evidence) | Low |

- **Suggested architecture (my synthesis, not sourced):**
  1. **Daily/weekly regime layer:** KC Fed RORO, OFR FSI, HY OAS, COT z-scores, ETF flows, the trader's own daily absorption ratio/turbulence, 12-month TSMOM, CTA/vol-control proxies, inflation regime for the stock-bond correlation sign. It decides which "rotation direction" is permitted and sets risk budget.
  2. **Intraday detection layer:** a live cross-asset relative-strength ranking plus VIX/DVOL/credit-ETF stress triggers plus a live PC1 "RORO factor". This identifies source and destination assets as the rotation starts.
  3. **Confirmation layer:** CVD/taker flow, OI and liquidations for crypto legs; tick-based OFI or volume for futures legs.
  4. **Exit:** momentum fade (RS-momentum rolling over, CVD divergence), plus Gao/Baltussen late-session continuation and next-day reversal evidence for timing.

### Gaps
- IBKR fees for CFE (VIX futures), ICE/MOVE, Cboe index add-ons, and the availability of VIX3M/VVIX for non-professionals in 2026 were not verified.
- It was not verified whether IBKR's API delivers aggressor-flagged trades for CME futures.
- Coinbase Advanced Trade and Coinbase Exchange WebSocket trade-side fields were not checked in the docs. Coinbase is assumed usable for the premium calculation via public tickers.
- No published, peer-reviewed validation exists for running PCA-based RORO, absorption ratio or turbulence on *intraday* data. This needs the trader's own backtest.
