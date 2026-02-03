# SDK Quiz Generator Pipeline

Answer generation pipelines for Unit Test and Complex QA questions.

> 📖 For question diversity guidelines and patterns, see **[GUIDELINES.md](GUIDELINES.md)**

---

## Unit Test Pipeline

```
User provides SDK doc
        ↓
Generate question + query params
        ↓
Call SDK Gateway API
        ↓
GPT-5.2 generates answer from response
        ↓
Output JSON: question, query_params, sdk_response, answer
```

### Usage

```bash
export OPENAI_API_KEY="sk-..."

python3 scripts/generate_unit_test_answer.py \
  "What is SPY's largest country weighting?" \
  "https://data-gateway.prd.space.id/api/v1/etf/country-weightings" \
  symbol=SPY
```

### Output

```json
{
  "question": "What is QQQ's largest country weighting?",
  "query_params": {"symbol": "QQQ"},
  "sdk_response": {...},
  "answer": "United States is QQQ's largest country weighting at 94.66%."
}
```

---

## Complex QA Pipeline

```
User provides SDK doc(s)
        ↓
Generate question + MULTIPLE query param sets
        ↓
Generate solution steps (extract → calculate)
        ↓
Call SDK Gateway for EACH query
        ↓
GPT-5.2 / programmatic calculation
        ↓
Output JSON: question, solution_steps, queries, sdk_responses, answer
```

### Key Differences from Unit Test

| Aspect | Unit Test | Complex QA |
|--------|-----------|------------|
| Queries per question | 1 | 1-N (multiple) |
| Answer type | Direct lookup | Calculation required |
| Solution steps | Not needed | Required |

### Usage

```bash
# Single question (LLM)
export OPENAI_API_KEY="sk-..."
python3 scripts/generate_complex_qa_answer.py input.json

# Batch (LLM)
python3 scripts/generate_complex_qa_answer.py batch.json --batch

# Batch (programmatic, no LLM)
python3 scripts/generate_complex_qa_answer.py batch.json --batch --no-llm
```

### Input JSON

```json
{
  "question": "What was AAPL's consensus EPS growth rate from Q1 to Q2 2024?",
  "solution_steps": [
    "From query 1, extract epsAvg for Q1 2024",
    "From query 2, extract epsAvg for Q2 2024",
    "Calculate: (epsAvg_Q2 − epsAvg_Q1) / epsAvg_Q1 × 100%"
  ],
  "queries": [
    {
      "request_url": "https://data-gateway.prd.space.id/api/v1/stocks/financial-estimates",
      "params": {"symbol": "AAPL", "fiscal_year": 2024, "fiscal_quarter": "Q1"}
    },
    {
      "request_url": "https://data-gateway.prd.space.id/api/v1/stocks/financial-estimates",
      "params": {"symbol": "AAPL", "fiscal_year": 2024, "fiscal_quarter": "Q2"}
    }
  ]
}
```

### Output JSON

```json
{
  "id": 1,
  "type": "Complex QA",
  "question": "What is AVGO's forward P/E ratio ...?",
  "solution_steps": ["Extract epsAvg", "Extract price_close", "Calculate P/E"],
  "queries": [...],
  "sdk_responses": [{...}, {...}],
  "answer": "AVGO FY2025 epsAvg = $6.748. Most recent close: $235.58. Forward P/E = 34.91x"
}
```

---

## Response Field Reference

### Financial Estimates

| Field | Description |
|-------|-------------|
| `epsAvg`, `epsHigh`, `epsLow` | Earnings per share consensus |
| `revenueAvg`, `revenueHigh`, `revenueLow` | Revenue consensus |
| `ebitdaAvg`, `ebitdaHigh`, `ebitdaLow` | EBITDA consensus |
| `ebitAvg`, `ebitHigh`, `ebitLow` | EBIT (operating income) consensus |
| `netIncomeAvg`, `netIncomeHigh`, `netIncomeLow` | Net income consensus |
| `sgaExpenseAvg`, `sgaExpenseHigh`, `sgaExpenseLow` | SGA expense consensus |
| `numAnalystsRevenue`, `numAnalystsEps` | Analyst coverage count |
| `calendarEndDate` | Fiscal period end date |

### Kline (per candle)

| Field | Description |
|-------|-------------|
| `price_open`, `price_high`, `price_low`, `price_close` | OHLC prices |
| `volume_traded` | Trading volume |
| `trades_count` | Number of trades |
| `time_period_start`, `time_period_end` | ISO timestamps |
| `time_open`, `time_close` | Unix timestamps |

---

## Configuration

```bash
# Required
export OPENAI_API_KEY="sk-..."

# Optional (has default)
export SID_API_KEY="..."
```
