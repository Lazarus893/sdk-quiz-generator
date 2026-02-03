# Question Generation Guidelines

Guidelines for generating diverse, high-quality quiz questions.

---

## Unit Test Guidelines

### API Categories

| Category | APIs |
|----------|------|
| Financials | `getCompanyIncomeStatements`, `getCompanyBalanceStatements`, `getCompanyCashFlowStatements` |
| Price | `getStockKline`, `getCryptoKline`, `getETFKline`, `getFuturePrice` |
| Holdings | `getInsiderTrades`, `getSenatorTrades`, `getInstitutionOwnershipAnalytics` |
| Macro | `getHistoricalEconomicIndicator` (CPI, GDP, Unemployment, Fed Funds) |
| Events | `getDividendEvent`, `getSplitEvent`, `getEarningsCalendarData` |
| Crypto-specific | `getExchangeNetflow`, `getFundingRate`, `getOpenInterest`, `getLongShortRatio` |

### Question Patterns

1. **Date-specific value:** "What was ETH's opening price on Aug 12, 2025?"
2. **Financial ratio:** "What is AAPL's gross margin based on 2025 Q2 earnings?"
3. **Multi-metric:** "What is MSFT's operating margin and net margin for 2025 Q2?"
4. **Yes/No check:** "Did US announce CPI data on Aug 14, 2025?"
5. **Existence:** "Did TSLA have an insider transaction on Sep 11, 2025?"
6. **Period aggregate:** "How many shares of NVDA did Senator X purchase in Q3 2025?"

### Common Formulas

| Ratio | Formula |
|-------|---------|
| Gross Margin | `(Revenue - COGS) / Revenue` |
| Operating Margin | `Operating Income / Revenue` |
| Net Margin | `Net Income / Revenue` |
| Current Ratio | `Current Assets / Current Liabilities` |
| Debt-to-Asset | `Total Debt / Total Assets` |

---

## Complex QA Guidelines

### Calculation Categories

**Risk & Return:**
| Metric | Formula |
|--------|---------|
| Sharpe Ratio | `(Mean Return − Rf) / StdDev × √252` |
| Sortino Ratio | `(Mean Return − Rf) / Downside StdDev × √252` |
| Max Drawdown | `(Trough − Peak) / Peak` |
| CAGR | `(End/Start)^(1/n) − 1` |

**Technical:**
| Metric | Formula |
|--------|---------|
| VWAP | `Σ(TP × Vol) / Σ(Vol)`, TP = (H+L+C)/3 |
| ATR% | `mean(H−L) / mean(C) × 100%` |
| RSI | 14-day relative strength index |
| Volatility | `stdev(ln_returns) × √252` |

**Fundamental:**
| Metric | Formula |
|--------|---------|
| Forward P/E | `Price / EPS_estimate` |
| PEG | `P/E / EPS_growth_rate` |
| FCF per Share | `FCF / Outstanding Shares` |
| DuPont ROE | `Net Margin × Asset Turnover × Leverage` |

**Trading:**
| Metric | Formula |
|--------|---------|
| Position Size | `(Equity × MaxLoss%) / (Entry − StopLoss)` |
| Risk/Reward | `(Target − Entry) / (Entry − StopLoss)` |
| Margin Call | Solve `(Shares × P − Loan) / (Shares × P) = Maintenance%` |

### Query Patterns

| Pattern | Example APIs | Use Case |
|---------|--------------|----------|
| Price + Financials | `getStockKline` + `getCompanyIncomeStatements` | P/E, PEG |
| Cross-period | Same API, different `fiscal_year`/`fiscal_quarter` | YoY growth |
| Cross-symbol | Same API, different symbols | Company comparison |
| Estimate vs Actual | `getFinancialEstimates` + `getCompanyIncomeStatements` | Beat/miss |
| Macro + Asset | `getHistoricalEconomicIndicator` + `getCryptoKline` | Event study |

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
