# Question Generation Guidelines

Guidelines for generating diverse, high-quality quiz questions.

---

## Unit Test Guidelines

### Symbol Variation

Use different ETFs/stocks to avoid repetition:

| Category | Symbols |
|----------|---------|
| Broad market | SPY, VTI, VOO |
| Tech/Growth | QQQ, ARKK, VGT |
| Small cap | IWM, VB |
| International | EEM, VEA, VWO |
| Sector-specific | XLF, XLE, XLK |

### Field Testing Patterns

1. **Largest value:** "What is [symbol]'s largest country weighting?"
2. **Smallest value:** "What is [symbol]'s smallest non-zero country weighting?"
3. **Specific lookup:** "What is [country]'s weight percentage in [symbol]?"
4. **Count:** "How many countries are represented in [symbol]'s holdings?"
5. **Ranking:** "What are the top N countries by weighting in [symbol]?"
6. **Comparison:** "What is the difference between [country1] and [country2] in [symbol]?"
7. **Presence check:** "Does [symbol] have exposure to [country]?"
8. **Aggregation:** "What is the combined weight of [region] countries in [symbol]?"

### Edge Cases

- Zero values vs non-zero
- Excluding "Other" category
- Handling missing countries
- Percentage format parsing
- Decimal precision

---

## Complex QA Guidelines

### Calculation Types

| # | Calculation | Formula |
|---|-------------|---------|
| 1 | Forward P/E | `price_close / epsAvg` |
| 2 | VWAP | `Σ(TP × volume) / Σ(volume)`, TP = (H+L+C)/3 |
| 3 | Operating margin | `ebitAvg / revenueAvg × 100%` |
| 4 | EPS growth rate | `(epsAvg_new − epsAvg_old) / epsAvg_old × 100%` |
| 5 | Range spread | `(high − low) / avg × 100%` |
| 6 | Annualized volatility | `stdev(ln_returns) × √252` |
| 7 | SGA ratio | `sgaExpenseAvg / revenueAvg × 100%` |
| 8 | Incremental margin | `Δ_netIncome / Δ_revenue × 100%` |
| 9 | ATR% | `mean(price_high − price_low) / mean(price_close) × 100%` |
| 10 | PEG ratio | `(price / epsAvg) / EPS_growth_rate` |

### Query Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| Cross-API | kline + financial-estimates | Forward P/E, PEG ratio |
| Cross-year | same symbol, different fiscal_year | margin YoY |
| Cross-quarter | same symbol, Q1/Q2/Q3/Q4 | EPS trajectory |
| Cross-symbol | different symbols, same period | AMZN vs WMT |
| Single query complex | VWAP, volatility, ATR from kline | — |

### Symbol Variation

| Category | Symbols |
|----------|---------|
| Mega-cap tech | AAPL, MSFT, AMZN, NVDA, AVGO |
| Growth stocks | TSLA, AMD, CRM, NFLX |
| Value/cyclical | JPM, WMT |
| Compared pairs | AMZN vs WMT, HD vs COST |

---

## Complex QA Patterns

### Pattern 1: Ratio Calculation

```
Q: What is [company]'s [ratio] for [period]?
   Use [numerator source] and [denominator source].

Steps:
1. Get numerator value
2. Get denominator value
3. Calculate: numerator / denominator
```

**Example:**
```
Q: What was Apple's Free Cash Flow per Share for fiscal year 2025?
   Outstanding shares count should use the closest to its fiscal year-end date (September 30, 2025).

Steps:
1. Get Free Cash Flow for FY 2025
2. Get outstanding shares as of 2025-09-30
3. Calculate: FCF / shares
```

### Pattern 2: Year-over-Year Change

```
Q: How did [metric] change from [period1] to [period2] for [entity]?

Steps:
1. Get metric value for period1
2. Get metric value for period2
3. Calculate: (period2 - period1) / period1 * 100%
```

### Pattern 3: Weighted Average

```
Q: What is the weighted average [metric] of [entities] weighted by [weight_field]?

Steps:
1. Get metric value for each entity
2. Get weight for each entity
3. Calculate: Σ(metric × weight) / Σ(weight)
```

### Pattern 4: Multi-Entity Comparison

```
Q: Among [list of entities], which has the highest/lowest [metric]?

Steps:
1. Get metric for each entity
2. Compare and rank
```

### Pattern 5: Time-Series Trend

```
Q: What is the trend in [metric] from [start_period] to [end_period] for [entity]?

Steps:
1. Get metric for each period
2. Calculate period-over-period changes
3. Analyze trend (increasing/decreasing/stable)
```

---

## Data Selection Criteria

Complex QA questions must clearly specify:

### Date Selection
- "Use the closest to [date]"
- "As of [date]"
- "For the period ending [date]"
- "Between [start_date] and [end_date]"

### Entity Selection
- "Top N by [metric]"
- "Bottom N by [metric]"
- "Among [list of entities]"
- "Excluding [category]"

### Field Selection
- "Use [specific_field] for calculation"
- "Adjust for [adjustment] (e.g., stock split)"
- "In [currency] terms"
- "Annualized basis"

---

## Answer Structure

### 1. Final Result
```
Answer: [Entity]'s [metric] was [value] for [period].
```

### 2. Calculation Steps
```
Step 1: [Data point 1] = [value]
Step 2: [Data point 2] = [value]
Step 3: [Calculation] = [result]
```

### 3. Methodology (optional)
```
[Data selection criteria used]
[Adjustments applied]
```
