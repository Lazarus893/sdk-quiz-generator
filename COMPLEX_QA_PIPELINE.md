# Complex QA Generation Pipeline

Complete workflow for generating Complex QA questions with multi-hop queries and calculations.

## Overview

**Complex QA questions** test the ability to:
- Combine data from multiple API calls
- Perform calculations across different fields
- Apply data selection criteria
- Analyze trends and comparisons

Unlike Unit Test (single-point queries), Complex QA requires **multi-step workflows** and **computational reasoning**.

---

## Pipeline Architecture

```
┌─────────────────────────┐
│ User provides SDK doc   │
└──────────┬──────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ Identify multi-step query opportunities  │
│ • Cross-field calculations               │
│ • Time-series comparisons                │
│ • Multi-entity analysis                  │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ Generate question + data requirements    │
│ • Specify calculation steps              │
│ • Define data selection criteria         │
│ • Include time/entity constraints        │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ Execute multi-hop query plan             │
│ Step 1: Call SDK for first data point   │
│ Step 2: Call SDK for second data point  │
│ Step N: Call SDK for final data point   │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ Perform calculations                     │
│ • Apply formulas                         │
│ • Aggregate data                         │
│ • Compare values                         │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│ Generate natural language answer         │
│ • Show step-by-step calculation          │
│ • Cite specific numbers                  │
│ • Explain methodology                    │
└──────────────────────────────────────────┘
```

---

## Complex QA Patterns

### Pattern 1: Ratio Calculation

**Structure:**
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

**Structure:**
```
Q: How did [metric] change from [period1] to [period2] for [entity]?

Steps:
1. Get metric value for period1
2. Get metric value for period2
3. Calculate: (period2 - period1) / period1 * 100%
```

**Example:**
```
Q: What is the revenue growth rate between Q3 2024 and Q4 2024 for Microsoft?

Steps:
1. Get Q3 2024 revenue
2. Get Q4 2024 revenue
3. Calculate: (Q4 - Q3) / Q3 * 100%
```

### Pattern 3: Weighted Average

**Structure:**
```
Q: What is the weighted average [metric] of [entities] weighted by [weight_field]?

Steps:
1. Get metric value for each entity
2. Get weight for each entity
3. Calculate: Σ(metric × weight) / Σ(weight)
```

**Example:**
```
Q: What is the weighted average P/E ratio of the top 5 holdings in QQQ by market cap?

Steps:
1. Get P/E ratio for top 5 holdings
2. Get market cap weight of each holding
3. Calculate: Σ(P/E × weight)
```

### Pattern 4: Multi-Entity Comparison

**Structure:**
```
Q: Among [list of entities], which has the highest/lowest [metric]?

Steps:
1. Get metric for entity1
2. Get metric for entity2
...
N. Compare and rank
```

**Example:**
```
Q: Among the "Magnificent 7" tech stocks, which had the highest earnings growth rate in 2025?

Steps:
1. Get 2024 and 2025 earnings for each company
2. Calculate growth rate for each
3. Rank and identify highest
```

### Pattern 5: Time-Series Trend

**Structure:**
```
Q: What is the trend in [metric] from [start_period] to [end_period] for [entity]?

Steps:
1. Get metric for each period
2. Calculate period-over-period changes
3. Analyze trend (increasing/decreasing/stable)
```

**Example:**
```
Q: What is the trend in Amazon's debt-to-equity ratio from Q1 2025 to Q4 2025?

Steps:
1. Get debt and equity for Q1, Q2, Q3, Q4
2. Calculate D/E for each quarter
3. Analyze trend direction
```

---

## Data Requirements Specification

Complex QA questions must clearly specify **data selection criteria**:

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

Complex QA answers should follow this format:

### 1. Final Result (Clear Statement)
```
Answer: [Entity]'s [metric] was [value] for [period].
```

### 2. Calculation Steps (Show Work)
```
This is calculated as:
Step 1: [Data point 1] = [value]
Step 2: [Data point 2] = [value]
Step 3: [Calculation] = [result]
```

### 3. Methodology (When Needed)
```
[Data selection criteria used]
[Adjustments applied]
[Assumptions made]
```

### Example Answer:
```
Answer: Apple's Free Cash Flow per Share for fiscal year 2025 was $6.82.

Calculation:
Step 1: Free Cash Flow (FY 2025) = $108.5B
Step 2: Outstanding Shares (as of 2025-09-30) = 15.9B shares
Step 3: FCF per Share = $108.5B / 15.9B = $6.82

Methodology: Outstanding shares count uses the closest available date to Apple's 
fiscal year-end (September 30, 2025).
```

---

## Implementation Approach

### Current Status
Complex QA answer generation is **not yet automated** (unlike Unit Test which has the `generate_unit_test_answer.py` script).

### Manual Generation Process

1. **Question Design**
   - Identify multi-hop opportunity in SDK doc
   - Define calculation formula
   - Specify data selection criteria

2. **Query Plan**
   - List all required API calls
   - Document query parameters for each call
   - Define calculation steps

3. **Data Collection**
   - Execute each API call
   - Store intermediate results
   - Verify data quality

4. **Calculation**
   - Apply formulas
   - Show step-by-step work
   - Format results with appropriate precision

5. **Answer Generation**
   - Write clear final statement
   - Include calculation steps
   - Explain methodology

### Future Automation (Roadmap)

To automate Complex QA answer generation:

1. **Query Planner**
   - Parse question to identify required data points
   - Generate API call sequence
   - Handle dependencies between calls

2. **Data Collector**
   - Execute multi-hop queries
   - Cache intermediate results
   - Handle errors and retries

3. **Calculator Engine**
   - Parse calculation formulas
   - Execute computations
   - Validate results

4. **Answer Formatter**
   - Generate step-by-step explanation
   - Format numbers and units
   - Create natural language output

---

## Example Workflow

### Question:
"What was Apple's Free Cash Flow per Share for fiscal year 2025? Outstanding shares count should use the closest to its fiscal year-end date (September 30, 2025)."

### Query Plan:
```json
{
  "step1": {
    "api": "getFinancialMetrics",
    "params": {
      "symbol": "AAPL",
      "metric": "free_cash_flow",
      "fiscal_year": 2025
    }
  },
  "step2": {
    "api": "getSharesOutstanding",
    "params": {
      "symbol": "AAPL",
      "date": "2025-09-30"
    }
  },
  "calculation": {
    "formula": "free_cash_flow / shares_outstanding",
    "result_unit": "dollars per share"
  }
}
```

### Execution:
```bash
# Step 1: Get Free Cash Flow
curl "https://api.example.com/financial-metrics?symbol=AAPL&metric=free_cash_flow&fiscal_year=2025"
# Result: {"free_cash_flow": 108500000000}

# Step 2: Get Shares Outstanding
curl "https://api.example.com/shares-outstanding?symbol=AAPL&date=2025-09-30"
# Result: {"shares_outstanding": 15900000000}

# Step 3: Calculate
# 108500000000 / 15900000000 = 6.82
```

### Answer:
```
Answer: Apple's Free Cash Flow per Share for fiscal year 2025 was $6.82.

Calculation:
Step 1: Free Cash Flow (FY 2025) = $108.5B
Step 2: Outstanding Shares (as of 2025-09-30) = 15.9B shares
Step 3: FCF per Share = $108.5B / 15.9B = $6.82

Methodology: Outstanding shares count uses the closest available date to 
Apple's fiscal year-end (September 30, 2025).
```

---

## Validation Checklist

For each Complex QA question and answer:

- [ ] Question clearly specifies data requirements
- [ ] All API calls are documented
- [ ] Calculation formula is explicit
- [ ] Step-by-step work is shown
- [ ] Units are included (%, $, shares, etc.)
- [ ] Dates are specified when relevant
- [ ] Methodology is explained
- [ ] Final answer is clear and concise
- [ ] Numbers can be verified from source data

---

## Best Practices

### Question Design
- **Be specific** - Define exact calculation and data sources
- **Include constraints** - Specify date ranges, entity lists, exclusions
- **Test real scenarios** - Use realistic business analysis questions
- **Vary difficulty** - Mix simple ratios with complex multi-step problems

### Answer Quality
- **Show all work** - Don't skip calculation steps
- **Cite sources** - Reference which API/field provided each number
- **Explain choices** - Why use "closest date" or "top 5"
- **Check precision** - Use appropriate decimal places for context

### Common Pitfalls
- ❌ Ambiguous data selection ("recent data" - how recent?)
- ❌ Missing calculation steps (jumping to result)
- ❌ Inconsistent units ($B vs $M)
- ❌ Unrealistic scenarios (data not available in SDK)
- ❌ Overly complex questions (5+ API calls)

---

## Tools and Resources

- **Query Planner Tool** (Coming soon) - Generates API call sequence from question
- **Calculator Helper** - Validates formulas and unit conversions
- **Example Library** - 8 diverse Complex QA examples in `examples/complex_qa_examples.md`

---

For more patterns and examples, see **[examples/complex_qa_examples.md](examples/complex_qa_examples.md)**.
