# Question Generation Guidelines

Guidelines for generating diverse, high-quality quiz questions.

---

## ⚠️ Core Principles (MUST Follow)

### 1. 题目必须像真实的金融问题，而非接口测试

**❌ 错误示例（像在测试接口）：**
- "getStockKline 返回的 price_close 字段值是多少？"
- "AAPL 的 epsAvg 字段是什么？"
- "API 返回的 data 数组第一个元素是什么？"

**✅ 正确示例（真实金融问题）：**
- "2024年12月31日收盘时，苹果公司的股价是多少？"
- "英伟达 2024 财年的每股收益预期是多少？"
- "2024年第三季度，特斯拉的营业利润率是多少？"

**原则：** 问的是金融指标（股价、PE、利润率、增长率等），不是字段名或数据结构。

### 2. 时间点必须固定且稳定

**使用 2024-2025 年及之前的历史数据**，这些数据已经确定，不会再变化。

**❌ 错误示例：**
- "苹果公司最新的股价是多少？"（会随时间变化）
- "当前的比特币价格是多少？"（实时变化）
- "2026年预测的EPS是多少？"（可能还在更新）

**✅ 正确示例：**
- "2024年6月30日收盘时，苹果公司的股价是多少？"
- "2024年1月15日 UTC 00:00 时，比特币的价格是多少？"
- "根据2024年9月发布的预测，英伟达2025财年的EPS预期是多少？"

**原则：** 每道题必须有明确的、固定的时间点，确保答案有且仅有一个。

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

1. **Date-specific value:** "2024年8月12日 UTC 00:00，以太坊的开盘价是多少？"
2. **Financial ratio:** "根据苹果公司 2024 财年第二季度财报，其毛利率是多少？"
3. **Multi-metric:** "微软 2024 财年第二季度的营业利润率和净利润率分别是多少？"
4. **Yes/No check:** "美国是否在 2024年8月14日 公布了 CPI 数据？"
5. **Existence:** "特斯拉在 2024年9月11日 是否有内部人士交易记录？"
6. **Period aggregate:** "2024年第三季度，参议员 X 共购买了多少股英伟达股票？"

**注意：** 所有题目都使用 2024-2025 年的历史数据，确保答案唯一且稳定。

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
Q: 苹果公司 2024 财年的每股自由现金流是多少？
   流通股数量使用最接近其财年结束日（2024年9月30日）的数据。

Steps:
1. 获取 2024 财年的自由现金流
2. 获取截至 2024-09-30 的流通股数量
3. 计算: FCF / shares
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

**⚠️ 重要：只使用 2024-2025 年及之前的历史数据！**

- "Use the closest to [date]" → 使用 2024 年或更早的日期
- "As of [date]" → 指定具体的历史日期（如 2024-06-30）
- "For the period ending [date]" → 使用已结束的财务期间
- "Between [start_date] and [end_date]" → 使用历史时间范围

**示例：**
- ✅ "截至 2024年12月31日"
- ✅ "2024财年第三季度"
- ✅ "2024年1月1日至2024年6月30日"
- ❌ "最新数据"、"当前"、"实时"

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
