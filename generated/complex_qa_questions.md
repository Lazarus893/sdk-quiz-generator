# Complex QA Questions — Kline + Financial Estimates

Generated from SDK docs:
- `@arrays/data/ohlcv-provider/v1.0.0` → Gateway: `/api/v1/stocks/kline`
- `@arrays/data/stock/financial-estimates/v1.0.0` → Gateway: `/api/v1/stocks/financial-estimates`

---

## Q1: Forward P/E Ratio [Medium]

**Financial Concept:** Forward Price-to-Earnings Ratio — a valuation multiple that compares stock price to expected future earnings. The most widely used equity valuation metric.

**Question:**
What is Broadcom's (AVGO) forward P/E ratio, calculated using the FY2025 full-year consensus EPS estimate and the most recent closing price from the last trading days of December 2024?

**Queries:**
| # | Endpoint | Params |
|---|----------|--------|
| 1 | `/stocks/financial-estimates` | symbol=AVGO, fiscal_year=2025, fiscal_quarter=FY |
| 2 | `/stocks/kline` | ticker=AVGO, start_time=1735344000, end_time=1735603200, interval=1d, limit=5 |

**Solution Steps:**
1. From query 1, extract `epsAvg` for AVGO FY2025
2. From query 2, find the most recent daily candle and extract its `price_close`
3. **Forward P/E = price_close / epsAvg**
4. Higher P/E → market expects higher growth; lower P/E → lower expectations or undervaluation

---

## Q2: Volume-Weighted Average Price (VWAP) [Hard]

**Financial Concept:** VWAP — the benchmark price institutional traders use to evaluate trade execution quality. A trade executed below VWAP is considered a "good buy."

**Question:**
What was AMD's volume-weighted average price (VWAP) on January 15, 2025, using hourly candle data? Use the typical price — the average of high, low, and close — for each candle.

**Queries:**
| # | Endpoint | Params |
|---|----------|--------|
| 1 | `/stocks/kline` | ticker=AMD, start_time=1736899200, end_time=1736985600, interval=1h, limit=50 |

**Solution Steps:**
1. Collect all hourly candles for the trading day
2. For each candle: `TP = (price_high + price_low + price_close) / 3`
3. For each candle: compute `TP × volume_traded`
4. **VWAP = Σ(TP × volume_traded) / Σ(volume_traded)**

---

## Q3: Operating Margin Year-over-Year Change [Medium]

**Financial Concept:** Operating margin expansion/contraction — measures whether a company is becoming more or less efficient at converting revenue to operating profit. EBIT (Earnings Before Interest & Taxes) is used as the proxy for operating income.

**Question:**
Compare Salesforce's (CRM) estimated operating margin for FY2024 vs FY2025 using full-year consensus estimates. By how many percentage points did the operating margin expand or contract year-over-year? (Use EBIT as the proxy for operating income.)

**Queries:**
| # | Endpoint | Params |
|---|----------|--------|
| 1 | `/stocks/financial-estimates` | symbol=CRM, fiscal_year=2024, fiscal_quarter=FY |
| 2 | `/stocks/financial-estimates` | symbol=CRM, fiscal_year=2025, fiscal_quarter=FY |

**Solution Steps:**
1. FY2024 operating margin = `ebitAvg / revenueAvg × 100%`
2. FY2025 operating margin = `ebitAvg / revenueAvg × 100%`
3. **Margin change = FY2025_margin − FY2024_margin** (percentage points)
4. Positive = expansion; Negative = contraction

---

## Q4: EPS Estimate Dispersion vs Price Volatility [Hard]

**Financial Concept:** Comparing fundamental uncertainty (analyst disagreement) with market uncertainty (price volatility). When estimate dispersion exceeds price dispersion, it suggests the market hasn't fully priced in the uncertainty.

**Question:**
For Netflix (NFLX), compare the analyst EPS estimate range spread for FY2025 with the stock's price range spread during January 2025. Which shows more relative uncertainty — analyst disagreement on earnings, or the market's price action?

**Queries:**
| # | Endpoint | Params |
|---|----------|--------|
| 1 | `/stocks/financial-estimates` | symbol=NFLX, fiscal_year=2025, fiscal_quarter=FY |
| 2 | `/stocks/kline` | ticker=NFLX, start_time=1735689600, end_time=1738281600, interval=1d, limit=31 |

**Solution Steps:**
1. From financial-estimates: `EPS spread = (epsHigh − epsLow) / epsAvg × 100%`
2. From kline: find max(`price_high`) and min(`price_low`) across all candles
3. Calculate avg `price_close` over the period
4. `Price spread = (max_high − min_low) / avg_close × 100%`
5. **Compare**: higher spread = more relative uncertainty

---

## Q5: Quarterly EPS Growth Trajectory [Hard]

**Financial Concept:** Earnings growth acceleration/deceleration — tracking whether sequential quarter-over-quarter growth rates are increasing or decreasing reveals the trajectory of a company's profitability, not just its level.

**Question:**
Calculate Apple's (AAPL) quarter-over-quarter consensus EPS growth rate for each consecutive quarter in fiscal year 2024 (Q1→Q2, Q2→Q3, Q3→Q4). Is EPS growth accelerating or decelerating through the year?

**Queries:**
| # | Endpoint | Params |
|---|----------|--------|
| 1 | `/stocks/financial-estimates` | symbol=AAPL, fiscal_year=2024, fiscal_quarter=Q1 |
| 2 | `/stocks/financial-estimates` | symbol=AAPL, fiscal_year=2024, fiscal_quarter=Q2 |
| 3 | `/stocks/financial-estimates` | symbol=AAPL, fiscal_year=2024, fiscal_quarter=Q3 |
| 4 | `/stocks/financial-estimates` | symbol=AAPL, fiscal_year=2024, fiscal_quarter=Q4 |

**Solution Steps:**
1. Extract `epsAvg` from each quarterly response
2. Q1→Q2 growth = `(epsAvg_Q2 − epsAvg_Q1) / epsAvg_Q1 × 100%`
3. Q2→Q3 growth = `(epsAvg_Q3 − epsAvg_Q2) / epsAvg_Q2 × 100%`
4. Q3→Q4 growth = `(epsAvg_Q4 − epsAvg_Q3) / epsAvg_Q3 × 100%`
5. **If each rate > previous → accelerating; each < previous → decelerating; mixed → uneven**

---

## Q6: Annualized Historical Volatility [Hard]

**Financial Concept:** Historical (realized) volatility — the standard deviation of logarithmic returns, annualized to a yearly basis. Used in options pricing (Black-Scholes model), risk management, and portfolio construction. √252 accounts for ~252 trading days per year.

**Question:**
Calculate the annualized historical volatility for JPMorgan Chase (JPM) using daily closing prices from November 2024. Use the standard deviation of daily logarithmic returns, annualized by multiplying by √252.

**Queries:**
| # | Endpoint | Params |
|---|----------|--------|
| 1 | `/stocks/kline` | ticker=JPM, start_time=1730419200, end_time=1732924800, interval=1d, limit=30 |

**Solution Steps:**
1. Extract all `price_close` values ordered by `time_period_start` ascending
2. Daily log returns: `r_i = ln(price_close_i / price_close_{i-1})`
3. Mean: `mean_r = Σ(r_i) / N`
4. Sample standard deviation: `σ = √(Σ(r_i − mean_r)² / (N − 1))`
5. **Annualized volatility = σ × √252**, expressed as percentage

---

## Q7: SGA Efficiency Comparison [Medium]

**Financial Concept:** SGA-to-Revenue ratio — measures how much a company spends on selling, general, and administrative costs per dollar of revenue. Lower is more efficient. Useful for comparing operational efficiency between competitors in the same industry.

**Question:**
Compare the selling, general & administrative expense ratio (SGA/Revenue) for Amazon (AMZN) vs. Walmart (WMT) based on FY2025 full-year consensus estimates. Which company is expected to be more efficient in controlling overhead costs, and by how many percentage points?

**Queries:**
| # | Endpoint | Params |
|---|----------|--------|
| 1 | `/stocks/financial-estimates` | symbol=AMZN, fiscal_year=2025, fiscal_quarter=FY |
| 2 | `/stocks/financial-estimates` | symbol=WMT, fiscal_year=2025, fiscal_quarter=FY |

**Solution Steps:**
1. AMZN SGA ratio = `sgaExpenseAvg / revenueAvg × 100%`
2. WMT SGA ratio = `sgaExpenseAvg / revenueAvg × 100%`
3. **Efficiency gap = AMZN_ratio − WMT_ratio**
4. Lower ratio = more efficient overhead control

---

## Q8: Incremental Margin (Revenue Drop-Through Rate) [Hard]

**Financial Concept:** Incremental margin — measures what percentage of each additional dollar of revenue converts to net income. When incremental margin exceeds overall margin, the business has positive operating leverage (fixed costs being spread over more revenue). This is a key metric for growth investors.

**Question:**
For Microsoft (MSFT), calculate the incremental net income margin from FY2024 to FY2025 — that is, what percentage of the additional revenue is expected to convert into additional net income? This measures how efficiently marginal revenue translates to bottom-line profit.

**Queries:**
| # | Endpoint | Params |
|---|----------|--------|
| 1 | `/stocks/financial-estimates` | symbol=MSFT, fiscal_year=2024, fiscal_quarter=FY |
| 2 | `/stocks/financial-estimates` | symbol=MSFT, fiscal_year=2025, fiscal_quarter=FY |

**Solution Steps:**
1. Incremental revenue = `revenueAvg_2025 − revenueAvg_2024`
2. Incremental net income = `netIncomeAvg_2025 − netIncomeAvg_2024`
3. **Incremental margin = incremental_netIncome / incremental_revenue × 100%**
4. Also calculate FY2024 overall margin = `netIncomeAvg_2024 / revenueAvg_2024 × 100%`
5. If incremental margin > overall margin → positive operating leverage; if lower → diminishing returns

---

## Q9: Average True Range % (Weekly) [Medium]

**Financial Concept:** ATR% (Average True Range as a percentage of price) — a normalized, range-based volatility measure. Unlike return-based volatility, ATR captures intra-period price swings. Commonly used in position sizing — traders size positions inversely to ATR% to normalize risk.

**Question:**
What was the average weekly true range for Tesla (TSLA) during Q4 2024, expressed as a percentage of the average weekly closing price? This measures Tesla's typical weekly price swing relative to its stock price.

**Queries:**
| # | Endpoint | Params |
|---|----------|--------|
| 1 | `/stocks/kline` | ticker=TSLA, start_time=1727740800, end_time=1735603200, interval=1w, limit=14 |

**Solution Steps:**
1. For each weekly candle: `TR = price_high − price_low`
2. `ATR = Σ(TR) / count(candles)`
3. `avg_close = Σ(price_close) / count(candles)`
4. **ATR% = ATR / avg_close × 100%**

---

## Q10: PEG Ratio (Price/Earnings-to-Growth) [Hard]

**Financial Concept:** PEG Ratio — normalizes the P/E ratio by the earnings growth rate. A PEG of 1.0 means the stock is "fairly valued" for its growth rate; < 1.0 suggests undervaluation relative to growth; > 1.0 suggests the market is paying a premium above the growth rate. Popularized by Peter Lynch.

**Question:**
Calculate NVIDIA's (NVDA) PEG ratio using: (1) the FY2025 consensus EPS estimate, (2) the EPS growth rate from FY2024 to FY2025, and (3) the average daily closing price during December 2024. A PEG ratio below 1.0 is generally considered undervalued relative to earnings growth.

**Queries:**
| # | Endpoint | Params |
|---|----------|--------|
| 1 | `/stocks/financial-estimates` | symbol=NVDA, fiscal_year=2024, fiscal_quarter=FY |
| 2 | `/stocks/financial-estimates` | symbol=NVDA, fiscal_year=2025, fiscal_quarter=FY |
| 3 | `/stocks/kline` | ticker=NVDA, start_time=1733011200, end_time=1735603200, interval=1d, limit=31 |

**Solution Steps:**
1. EPS growth rate = `(epsAvg_2025 − epsAvg_2024) / epsAvg_2024 × 100`
2. Average close = `Σ(price_close) / count(candles)` from December 2024 kline
3. Forward P/E = `avg_close / epsAvg_2025`
4. **PEG = Forward_PE / EPS_growth_rate**
5. PEG < 1 → undervalued for growth; PEG > 1 → premium above growth rate

---

## Diversity Summary

| # | Financial Concept | APIs Used | Symbol(s) | Queries | Difficulty |
|---|-------------------|-----------|-----------|---------|------------|
| 1 | Forward P/E | FE + Kline | AVGO | 2 | Medium |
| 2 | VWAP | Kline (hourly) | AMD | 1 | Hard |
| 3 | Op. Margin YoY | FE × 2 | CRM | 2 | Medium |
| 4 | EPS Spread vs Price Spread | FE + Kline | NFLX | 2 | Hard |
| 5 | QoQ EPS Trajectory | FE × 4 | AAPL | 4 | Hard |
| 6 | Annualized Volatility | Kline (daily) | JPM | 1 | Hard |
| 7 | SGA Efficiency | FE × 2 | AMZN vs WMT | 2 | Medium |
| 8 | Incremental Margin | FE × 2 | MSFT | 2 | Hard |
| 9 | ATR% | Kline (weekly) | TSLA | 1 | Medium |
| 10 | PEG Ratio | FE × 2 + Kline | NVDA | 3 | Hard |

**API Coverage:**
- `financial-estimates`: Q1, Q3, Q4, Q5, Q7, Q8, Q10 (7 questions)
- `kline`: Q1, Q2, Q4, Q6, Q9, Q10 (6 questions)
- Cross-API: Q1, Q4, Q10 (3 questions)

**Unique Symbols (11):** AVGO, AMD, CRM, NFLX, AAPL, JPM, AMZN, WMT, MSFT, TSLA, NVDA

**Difficulty:** 4 Medium / 6 Hard

**Kline Intervals Used:** 1h (Q2), 1d (Q1, Q4, Q6, Q10), 1w (Q9)

**Financial Estimate Fields Exercised:**
- `epsAvg/High/Low` (Q1, Q4, Q5, Q10)
- `revenueAvg` (Q3, Q7, Q8)
- `ebitAvg` (Q3)
- `ebitdaAvg` — not used in these 10, available for future questions
- `netIncomeAvg` (Q8)
- `sgaExpenseAvg` (Q7)
- `numAnalystsRevenue/Eps` — not used in these 10, available for future questions
