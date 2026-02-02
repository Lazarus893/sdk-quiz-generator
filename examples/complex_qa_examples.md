# Complex QA Question Examples

This file demonstrates diverse Complex QA questions that require multi-hop queries and calculations.

## Example 1: EPS Growth Rate (Cross-Quarter Comparison)

**Question:** What was AAPL's consensus EPS growth rate from Q1 2024 to Q2 2024?

**Queries:**
```json
[
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
    "params": {"symbol": "AAPL", "metrics": "eps", "fiscalYear": 2024, "fiscalQuarter": 1, "periodicity": "quarterly"}
  },
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
    "params": {"symbol": "AAPL", "metrics": "eps", "fiscalYear": 2024, "fiscalQuarter": 2, "periodicity": "quarterly"}
  }
]
```

**Solution Steps:**
1. From query 1, extract the `mean` EPS for AAPL Q1 2024
2. From query 2, extract the `mean` EPS for AAPL Q2 2024
3. Calculate growth rate: `(Q2_mean - Q1_mean) / Q1_mean × 100%`

**Answer:** AAPL's consensus EPS grew from $1.52 (Q1 2024) to $1.71 (Q2 2024), a growth rate of 12.5%.

---

## Example 2: Guidance vs Consensus Surprise (Beat/Miss Analysis)

**Question:** For MSFT's fiscal year 2024 Q3 revenue, did the company's guidance beat or miss analyst consensus? By how much in both absolute and percentage terms?

**Queries:**
```json
[
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/guidance",
    "params": {"symbol": "MSFT", "metrics": "revenue", "fiscalYear": 2024, "fiscalQuarter": 3}
  }
]
```

**Solution Steps:**
1. From the guidance response, extract `guidanceMidpoint` (company's guidance)
2. Extract `meanBefore` (analyst consensus before guidance was issued)
3. Calculate absolute surprise: `guidanceMidpoint - meanBefore`
4. Calculate percentage surprise: `(guidanceMidpoint - meanBefore) / meanBefore × 100%`
5. If positive → beat; if negative → miss

**Answer:** MSFT's Q3 2024 revenue guidance midpoint was $61.5B vs analyst consensus of $60.2B before guidance. The company beat consensus by $1.3B (+2.16%).

---

## Example 3: Analyst Consensus Dispersion (Agreement Strength)

**Question:** Compare the analyst consensus strength for NVDA vs INTC on fiscal year 2025 annual EPS estimates. Which stock has more analyst agreement?

**Queries:**
```json
[
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
    "params": {"symbol": "NVDA", "metrics": "eps", "fiscalYear": 2025, "periodicity": "annual"}
  },
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
    "params": {"symbol": "INTC", "metrics": "eps", "fiscalYear": 2025, "periodicity": "annual"}
  }
]
```

**Solution Steps:**
1. From query 1, extract NVDA's `mean` and `standardDeviation` for EPS
2. From query 2, extract INTC's `mean` and `standardDeviation` for EPS
3. Calculate Coefficient of Variation for each: `CV = (standardDeviation / mean) × 100%`
4. Lower CV = stronger consensus (analysts agree more closely)
5. Compare the two CV values

**Answer:** NVDA's EPS estimate has a mean of $2.85 with std dev of $0.12 (CV = 4.2%), while INTC's mean is $1.05 with std dev of $0.31 (CV = 29.5%). NVDA has much stronger analyst consensus — analysts are far more aligned on NVDA's earnings outlook than INTC's.

---

## Example 4: Guidance Revision Trend (Quarter-over-Quarter Change)

**Question:** How did TSLA's revenue guidance midpoint change from Q1 2024 to Q2 2024? Is the company raising or lowering expectations?

**Queries:**
```json
[
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/guidance",
    "params": {"symbol": "TSLA", "metrics": "revenue", "fiscalYear": 2024, "fiscalQuarter": 1}
  },
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/guidance",
    "params": {"symbol": "TSLA", "metrics": "revenue", "fiscalYear": 2024, "fiscalQuarter": 2}
  }
]
```

**Solution Steps:**
1. From query 1, extract Q1 2024 `guidanceMidpoint` for revenue
2. From query 2, extract Q2 2024 `guidanceMidpoint` for revenue
3. Calculate absolute change: `Q2_midpoint - Q1_midpoint`
4. Calculate percentage change: `(Q2_midpoint - Q1_midpoint) / Q1_midpoint × 100%`
5. Positive change = raising expectations; negative = lowering

**Answer:** TSLA's revenue guidance midpoint increased from $25.2B (Q1 2024) to $26.8B (Q2 2024), a +$1.6B increase (+6.35%). Tesla is raising revenue expectations quarter-over-quarter.

---

## Example 5: Estimate Momentum (Revision Ratio)

**Question:** What is the analyst estimate revision ratio for AMZN's fiscal year 2025 annual revenue? Are analysts becoming more bullish or bearish?

**Queries:**
```json
[
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
    "params": {"symbol": "AMZN", "metrics": "revenue", "fiscalYear": 2025, "periodicity": "annual"}
  }
]
```

**Solution Steps:**
1. From the response, extract `up` (number of upward revisions) and `down` (number of downward revisions)
2. Calculate revision ratio: `up / (up + down) × 100%`
3. Ratio > 50% → bullish momentum; ratio < 50% → bearish momentum
4. Also note total `estimateCount` for context

**Answer:** For AMZN's FY2025 revenue, 18 analysts revised upward and 4 revised downward, giving a revision ratio of 81.8% (18/22). Analysts are strongly bullish — over 4x more upgrades than downgrades.

---

## Example 6: Price Volatility vs Estimate Range (Cross-API)

**Question:** For GOOGL, compare the analyst estimate range spread for FY2025 annual EPS with the stock's recent 30-day price range. Which shows more relative uncertainty?

**Queries:**
```json
[
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
    "params": {"symbol": "GOOGL", "metrics": "eps", "fiscalYear": 2025, "periodicity": "annual"}
  },
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/ohlcv",
    "params": {"symbol": "GOOGL", "interval": "1d", "startDate": "2024-12-01", "endDate": "2024-12-31", "dataSource": "yahoo"}
  }
]
```

**Solution Steps:**
1. From query 1, extract EPS `high`, `low`, and `mean`
2. Calculate estimate range spread: `(high - low) / mean × 100%`
3. From query 2, find the highest `high` and lowest `low` across all daily candles
4. Calculate the average `close` over the period
5. Calculate price range spread: `(max_high - min_low) / avg_close × 100%`
6. Compare the two spreads — higher spread = more relative uncertainty

**Answer:** GOOGL's EPS estimate range spread is ($8.20 - $7.10) / $7.65 = 14.4%. The 30-day price range spread is ($182 - $168) / $175 = 8.0%. Analyst estimates show relatively more dispersion (14.4%) than the stock's price movement (8.0%), suggesting more uncertainty in earnings outlook than in near-term price action.

---

## Example 7: Guidance Accuracy (Guidance vs Actual Consensus Shift)

**Question:** For META's Q2 2024 EBITDA, how much did analyst consensus shift after the company issued guidance? Calculate the "guidance pull" effect.

**Queries:**
```json
[
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/guidance",
    "params": {"symbol": "META", "metrics": "ebitda", "fiscalYear": 2024, "fiscalQuarter": 2}
  }
]
```

**Solution Steps:**
1. From the response, extract `meanBefore` (consensus before guidance)
2. Extract `meanAfter` (consensus after guidance)
3. Extract `guidanceMidpoint` (the company's guidance)
4. Calculate consensus shift: `meanAfter - meanBefore`
5. Calculate "guidance pull" percentage: `(meanAfter - meanBefore) / (guidanceMidpoint - meanBefore) × 100%`
   - 100% = analysts fully converged to guidance; 0% = analysts ignored guidance

**Answer:** META's Q2 2024 EBITDA: meanBefore = $18.5B, meanAfter = $19.8B, guidanceMidpoint = $20.2B. Consensus shifted +$1.3B after guidance. Guidance pull = $1.3B / $1.7B = 76.5% — analysts moved roughly three-quarters of the way toward META's guidance, indicating strong but not complete trust in management's outlook.

---

## Example 8: Multi-Metric Profitability Ratio (Cross-Metric Calculation)

**Question:** Based on FY2025 annual consensus estimates for AAPL, what is the estimated net profit margin (net income / revenue)?

**Queries:**
```json
[
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
    "params": {"symbol": "AAPL", "metrics": "netIncome", "fiscalYear": 2025, "periodicity": "annual"}
  },
  {
    "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
    "params": {"symbol": "AAPL", "metrics": "revenue", "fiscalYear": 2025, "periodicity": "annual"}
  }
]
```

**Solution Steps:**
1. From query 1, extract the `mean` net income estimate
2. From query 2, extract the `mean` revenue estimate
3. Calculate net profit margin: `mean_netIncome / mean_revenue × 100%`

**Answer:** AAPL's FY2025 estimated net income is $105.2B and estimated revenue is $412.8B. Estimated net profit margin = $105.2B / $412.8B = 25.5%.

---

## Key Variations Demonstrated

1. **Calculation types:**
   - Growth rate (Example 1)
   - Beat/miss analysis with absolute and percentage (Example 2)
   - Coefficient of Variation / consensus strength (Example 3)
   - Quarter-over-quarter change (Example 4)
   - Revision ratio (Example 5)
   - Cross-API range comparison (Example 6)
   - Guidance pull effect (Example 7)
   - Multi-metric profitability ratio (Example 8)

2. **Query patterns:**
   - Same endpoint, different quarters (Examples 1, 4)
   - Single query with derived fields (Examples 2, 5, 7)
   - Same endpoint, different symbols (Example 3)
   - Cross-API queries (Example 6)
   - Same endpoint, different metrics (Example 8)

3. **Financial concepts:**
   - EPS growth rate
   - Guidance surprise (beat/miss)
   - Coefficient of Variation (consensus dispersion)
   - Guidance revision trend
   - Estimate momentum / revision ratio
   - Price vs estimate uncertainty
   - Guidance pull effect
   - Net profit margin

4. **Symbols used:** AAPL, MSFT, NVDA, INTC, TSLA, AMZN, GOOGL, META
