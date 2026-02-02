# Complex QA Question Examples

This file demonstrates diverse Complex QA questions that require multi-hop queries and calculations.
All answers are computed from live gateway data.

**Gateway endpoints used:**
- Kline: `https://data-gateway.prd.space.id/api/v1/stocks/kline`
- Financial Estimates: `https://data-gateway.prd.space.id/api/v1/stocks/financial-estimates`

---

## Example 1: Forward P/E Ratio (AVGO) — Cross-API

**Question:** What is Broadcom's (AVGO) forward P/E ratio, calculated using the FY2025 full-year consensus EPS estimate and the most recent closing price from the last trading days of December 2024?

**Queries:**
```json
[
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "AVGO", "fiscal_year": 2025, "fiscal_quarter": "FY"}},
  {"request_url": ".../stocks/kline", "params": {"ticker": "AVGO", "start_time": 1735344000, "end_time": 1735603200, "interval": "1d", "limit": 5}}
]
```

**Solution Steps:**
1. From financial-estimates, extract `epsAvg` for AVGO FY2025
2. From kline, find the most recent candle's `price_close`
3. Calculate: Forward P/E = price_close / epsAvg

**Answer:** AVGO FY2025 consensus epsAvg = $6.74825. Most recent closing price (2024-12-30): $235.58. Forward P/E = $235.58 / $6.74825 = **34.91x**.

---

## Example 2: Volume-Weighted Average Price (AMD) — Hourly Kline

**Question:** What was AMD's volume-weighted average price (VWAP) on January 15, 2025, using hourly candle data? Use the typical price — the average of high, low, and close — for each candle.

**Queries:**
```json
[
  {"request_url": ".../stocks/kline", "params": {"ticker": "AMD", "start_time": 1736899200, "end_time": 1736985600, "interval": "1h", "limit": 50}}
]
```

**Solution Steps:**
1. For each hourly candle: TP = (price_high + price_low + price_close) / 3
2. For each candle: compute TP × volume_traded
3. VWAP = Σ(TP × volume_traded) / Σ(volume_traded)

**Answer:** AMD hourly candles: 17 candles, total volume 33,572,182. VWAP = **$119.1549**.

---

## Example 3: Operating Margin YoY Change (CRM) — Cross-Year

**Question:** Compare Salesforce's (CRM) estimated operating margin for FY2024 vs FY2025 using full-year consensus estimates. By how many percentage points did the operating margin expand or contract year-over-year? (Use EBIT as proxy for operating income.)

**Queries:**
```json
[
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "CRM", "fiscal_year": 2024, "fiscal_quarter": "FY"}},
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "CRM", "fiscal_year": 2025, "fiscal_quarter": "FY"}}
]
```

**Solution Steps:**
1. FY2024 operating margin = ebitAvg / revenueAvg × 100%
2. FY2025 operating margin = ebitAvg / revenueAvg × 100%
3. Margin change = FY2025_margin − FY2024_margin

**Answer:** CRM FY2024: ebitAvg=$3.47B, revenueAvg=$36.47B, margin=9.52%. FY2025: ebitAvg=$3.61B, revenueAvg=$37.96B, margin=9.52%. Year-over-year margin change: **-0.00 percentage points** (flat).

---

## Example 4: EPS Dispersion vs Price Volatility (NFLX) — Cross-API

**Question:** For Netflix (NFLX), compare the analyst EPS estimate range spread for FY2025 with the stock's price range spread during January 2025. Which shows more relative uncertainty?

**Queries:**
```json
[
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "NFLX", "fiscal_year": 2025, "fiscal_quarter": "FY"}},
  {"request_url": ".../stocks/kline", "params": {"ticker": "NFLX", "start_time": 1735689600, "end_time": 1738281600, "interval": "1d", "limit": 31}}
]
```

**Solution Steps:**
1. EPS spread = (epsHigh − epsLow) / epsAvg × 100%
2. Price spread = (max price_high − min price_low) / avg price_close × 100%
3. Compare the two spreads

**Answer:** NFLX EPS range spread = (2.695 − 2.543) / 2.563 = **5.93%**. Price range spread = (99.90 − 82.35) / 90.16 = **19.46%**. Market price action shows more relative uncertainty.

---

## Example 5: Quarterly EPS Growth Trajectory (AAPL) — 4 Quarters

**Question:** Calculate Apple's (AAPL) quarter-over-quarter consensus EPS growth rate for each consecutive quarter in fiscal year 2024 (Q1→Q2, Q2→Q3, Q3→Q4). Is EPS growth accelerating or decelerating through the year?

**Queries:**
```json
[
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "AAPL", "fiscal_year": 2024, "fiscal_quarter": "Q1"}},
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "AAPL", "fiscal_year": 2024, "fiscal_quarter": "Q2"}},
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "AAPL", "fiscal_year": 2024, "fiscal_quarter": "Q3"}},
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "AAPL", "fiscal_year": 2024, "fiscal_quarter": "Q4"}}
]
```

**Solution Steps:**
1. Extract epsAvg from each quarter
2. Calculate Q1→Q2, Q2→Q3, Q3→Q4 growth rates
3. If each rate > previous → accelerating; each < previous → decelerating

**Answer:** Q1=$2.101, Q2=$1.505, Q3=$1.346, Q4=$1.600. Q1→Q2: **-28.35%**, Q2→Q3: **-10.60%**, Q3→Q4: **+18.94%**. EPS growth is accelerating (decline narrowing, then turning positive).

---

## Example 6: Annualized Historical Volatility (JPM) — Daily Log Returns

**Question:** Calculate the annualized historical volatility for JPMorgan Chase (JPM) using daily closing prices from November 2024. Use the standard deviation of daily logarithmic returns, annualized by multiplying by √252.

**Queries:**
```json
[
  {"request_url": ".../stocks/kline", "params": {"ticker": "JPM", "start_time": 1730419200, "end_time": 1732924800, "interval": "1d", "limit": 30}}
]
```

**Solution Steps:**
1. Extract price_close from each daily candle (ascending order)
2. Calculate daily log returns: r_i = ln(close_i / close_{i-1})
3. Calculate sample standard deviation: σ = √(Σ(r_i − mean)² / (N−1))
4. Annualize: σ × √252

**Answer:** JPM November 2024: 21 trading days, 20 daily log returns. Mean daily log return: 0.005901. Daily σ = 0.027666. **Annualized volatility = 43.92%**.

---

## Example 7: SGA Efficiency Comparison (AMZN vs WMT) — Cross-Symbol

**Question:** Compare the selling, general & administrative expense ratio (SGA/Revenue) for Amazon (AMZN) vs. Walmart (WMT) based on FY2025 full-year consensus estimates. Which company is expected to be more efficient in controlling overhead costs, and by how many percentage points?

**Queries:**
```json
[
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "AMZN", "fiscal_year": 2025, "fiscal_quarter": "FY"}},
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "WMT", "fiscal_year": 2025, "fiscal_quarter": "FY"}}
]
```

**Solution Steps:**
1. AMZN SGA ratio = sgaExpenseAvg / revenueAvg × 100%
2. WMT SGA ratio = sgaExpenseAvg / revenueAvg × 100%
3. Compare: lower ratio = more efficient

**Answer:** AMZN SGA ratio = $64.6B / $714.7B = **9.04%**. WMT SGA ratio = $140.1B / $680.5B = **20.58%**. AMZN is more efficient by **11.54 percentage points**.

---

## Example 8: Incremental Margin / Drop-Through Rate (MSFT) — Cross-Year

**Question:** For Microsoft (MSFT), calculate the incremental net income margin from FY2024 to FY2025 — what percentage of the additional revenue is expected to convert into additional net income?

**Queries:**
```json
[
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "MSFT", "fiscal_year": 2024, "fiscal_quarter": "FY"}},
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "MSFT", "fiscal_year": 2025, "fiscal_quarter": "FY"}}
]
```

**Solution Steps:**
1. Incremental revenue = revenueAvg_2025 − revenueAvg_2024
2. Incremental net income = netIncomeAvg_2025 − netIncomeAvg_2024
3. Incremental margin = incremental_NI / incremental_rev × 100%
4. Compare with FY2024 overall margin to assess operating leverage

**Answer:** FY2024 revenue=$244.9B, NI=$90.5B (margin 36.95%). FY2025 revenue=$279.2B, NI=$100.2B. Incremental rev=$34.3B, incremental NI=$9.7B. **Incremental margin = 28.39%** — below the 36.95% overall margin, indicating diminishing returns on incremental revenue.

---

## Example 9: Weekly ATR% (TSLA) — Weekly Kline

**Question:** What was the average weekly true range for Tesla (TSLA) during Q4 2024, expressed as a percentage of the average weekly closing price?

**Queries:**
```json
[
  {"request_url": ".../stocks/kline", "params": {"ticker": "TSLA", "start_time": 1727740800, "end_time": 1735603200, "interval": "1w", "limit": 14}}
]
```

**Solution Steps:**
1. For each weekly candle: TR = price_high − price_low
2. ATR = Σ(TR) / count(candles)
3. avg_close = Σ(price_close) / count(candles)
4. ATR% = ATR / avg_close × 100%

**Answer:** TSLA Q4 2024: 14 weekly candles. ATR = $45.62. Average weekly close = $331.07. **ATR% = 13.78%**.

---

## Example 10: PEG Ratio (NVDA) — Cross-API + Cross-Year

**Question:** Calculate NVIDIA's (NVDA) PEG ratio using: (1) the FY2025 consensus EPS estimate, (2) the EPS growth rate from FY2024 to FY2025, and (3) the average daily closing price during December 2024. A PEG below 1.0 is generally considered undervalued relative to earnings growth.

**Queries:**
```json
[
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "NVDA", "fiscal_year": 2024, "fiscal_quarter": "FY"}},
  {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "NVDA", "fiscal_year": 2025, "fiscal_quarter": "FY"}},
  {"request_url": ".../stocks/kline", "params": {"ticker": "NVDA", "start_time": 1733011200, "end_time": 1735603200, "interval": "1d", "limit": 31}}
]
```

**Solution Steps:**
1. EPS growth = (epsAvg_2025 − epsAvg_2024) / epsAvg_2024 × 100
2. avg_close from December 2024 kline
3. Forward P/E = avg_close / epsAvg_2025
4. PEG = Forward_PE / EPS_growth_rate

**Answer:** FY2024 epsAvg=$2.152, FY2025 epsAvg=$2.952. EPS growth = **37.17%**. Dec 2024 avg close = $137.37 (20 days). Forward P/E = 46.53x. **PEG = 1.25** — market is paying a premium above the growth rate.

---

## Key Variations Demonstrated

1. **Calculation types:** Forward P/E, VWAP, operating margin change, range spread comparison, sequential growth trajectory, annualized volatility, SGA efficiency ratio, incremental margin, ATR%, PEG ratio
2. **Query patterns:**
   - Cross-API: kline + financial-estimates (Examples 1, 4, 10)
   - Cross-year: same symbol, different fiscal_year (Examples 3, 8)
   - Cross-symbol: different symbols, same period (Example 7)
   - Cross-quarter: 4 quarters in one fiscal year (Example 5)
   - Single-query complex derivation (Examples 2, 6, 9)
3. **Kline intervals used:** 1h (Example 2), 1d (Examples 1, 4, 6, 10), 1w (Example 9)
4. **Financial estimate fields used:** epsAvg/High/Low, revenueAvg, ebitAvg, netIncomeAvg, sgaExpenseAvg
5. **Symbols used:** AVGO, AMD, CRM, NFLX, AAPL, JPM, AMZN, WMT, MSFT, TSLA, NVDA
6. **Difficulty:** 4 Medium / 6 Hard
