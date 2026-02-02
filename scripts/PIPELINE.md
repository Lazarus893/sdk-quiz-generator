# SDK Quiz Generator Pipeline

Complete workflow for generating quiz questions with standard answers from SDK documentation.

## Overview

This skill generates three types of questions from SDK documentation:
1. **Unit Test** - Single-point data queries
2. **Complex QA** - Multi-hop calculations
3. **Trading Strategy** - Real trading strategies with entry/exit rules

This document covers the **Unit Test** and **Complex QA** answer generation pipelines.

---

## Unit Test Pipeline Architecture

```
┌─────────────────────────┐
│ User provides SDK doc   │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│ Generate questions + query parameters   │
│ • Vary symbols (QQQ, SPY, IWM, etc.)   │
│ • Test different fields                 │
│ • Mix query patterns                    │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────┐
│ Call SDK Gateway API    │
│ (with query params)     │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Get SDK raw response    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ GPT-5.2 generates natural language  │
│ answer from question + SDK response │
└──────────┬──────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│ Output 4-part JSON:                     │
│ • question (natural language)           │
│ • query_params (API parameters)         │
│ • sdk_response (complete raw response)  │
│ • answer (GPT-5.2 generated)           │
└─────────────────────────────────────────┘
```

---

## Components

### 1. SDK Documentation Parser
**Input:** SDK doc (markdown/text format)
**Output:** 
- API name and purpose
- Parameters (name, type, required/optional, description)
- Return value structure
- Examples

### 2. Question Generator
**Input:** Parsed SDK structure
**Output:** Natural language questions + query parameters

**Key requirements:**
- **Vary symbols/tickers** - Don't repeat the same symbol
- **Test different fields** - largest, smallest, specific lookup, count, ranking, comparison
- **Natural language only** - Never mention APIs or data sources in questions

**Example variations:**
```json
{"symbol": "QQQ"}  // Nasdaq 100
{"symbol": "SPY"}  // S&P 500
{"symbol": "IWM"}  // Russell 2000
{"symbol": "DIA"}  // Dow Jones
{"symbol": "VTI"}  // Total market
```

### 3. SDK Gateway Client
**Location:** `scripts/generate_unit_test_answer.py`

**Functionality:**
- Makes HTTP GET request to SDK gateway
- Adds authentication headers (`X-API-Key`)
- Returns complete raw JSON response

**Usage:**
```bash
export OPENAI_API_KEY="sk-..."
python3 scripts/generate_unit_test_answer.py \
  "What is SPY's largest country weighting?" \
  "https://data-gateway.prd.space.id/api/v1/etf/country-weightings" \
  symbol=SPY
```

### 4. Answer Generator (GPT-5.2)
**Model:** `gpt-5.2`
**Temperature:** 0.1 (factual, deterministic)
**Max tokens:** 500

**Prompt structure:**
```
System: You are a financial data expert who provides clear, accurate answers.
User: 
  You are answering: [question]
  Based on SDK response: [raw JSON]
  Provide clear, concise natural language answer with specific numbers.
```

**Example output:**
> "United States is QQQ's largest country weighting at 94.66%."

---

## Example End-to-End Flow

### Input: SDK Documentation
```markdown
## getETFCountryWeightings
Retrieves ETF country weightings for a given fund symbol.

Parameters:
- params.symbol (string): ETF symbol (e.g., "SPY")

Return Value:
- response.weightings: Array of country weighting records
  - country (string): Country name
  - weight_percentage (string): Weight as percentage
```

### Step 1: Generate Question
```
Question: "What is QQQ's largest country weighting?"
Query Params: {"symbol": "QQQ"}
```

### Step 2: Call SDK
```bash
curl -X GET 'https://data-gateway.prd.space.id/api/v1/etf/country-weightings?symbol=QQQ' \
  -H 'X-API-Key: ...'
```

### Step 3: Get Response
```json
{
  "success": true,
  "response": {
    "weightings": [
      {"country": "United States", "weight_percentage": "94.6600%"},
      {"country": "United Kingdom", "weight_percentage": "1.4200%"},
      ...
    ]
  }
}
```

### Step 4: Generate Answer (GPT-5.2)
```
Answer: "United States is QQQ's largest country weighting at 94.66%."
```

### Step 5: Final Output
```json
{
  "question": "What is QQQ's largest country weighting?",
  "query_params": {"symbol": "QQQ"},
  "sdk_response": {...complete response...},
  "answer": "United States is QQQ's largest country weighting at 94.66%."
}
```

---

## Question Diversity Guidelines

### Symbol Variation
Use different ETFs/stocks to avoid repetition:
- **Broad market:** SPY, VTI, VOO
- **Tech/Growth:** QQQ, ARKK, VGT
- **Small cap:** IWM, VB
- **International:** EEM, VEA, VWO
- **Sector-specific:** XLF, XLE, XLK

### Field Testing Patterns
1. **Largest value:** "What is [symbol]'s largest country weighting?"
2. **Smallest value:** "What is [symbol]'s smallest non-zero country weighting?"
3. **Specific lookup:** "What is [country]'s weight percentage in [symbol]?"
4. **Count:** "How many countries are represented in [symbol]'s holdings?"
5. **Ranking:** "What are the top N countries by weighting in [symbol]?"
6. **Comparison:** "What is the difference between [country1] and [country2] in [symbol]?"
7. **Presence check:** "Does [symbol] have exposure to [country]?"
8. **Aggregation:** "What is the combined weight of [region] countries in [symbol]?"

### Edge Cases to Test
- Zero values vs non-zero
- Excluding "Other" category
- Handling missing countries
- Percentage format parsing
- Decimal precision

---

## Configuration

### Environment Variables
```bash
# Required
export OPENAI_API_KEY="sk-..."

# Optional (has default)
export SID_API_KEY="..."
```

### Script Parameters
```bash
python3 scripts/generate_unit_test_answer.py \
  <question>      # Natural language question
  <request_url>   # Full SDK gateway endpoint URL
  <param=value>   # Query parameters (repeatable)
```

---

## Testing Checklist

- [ ] Script generates valid JSON output
- [ ] SDK response is complete and unmodified
- [ ] GPT-5.2 answer is factually correct
- [ ] Answer includes specific numbers from response
- [ ] Questions use varied symbols
- [ ] Questions test different fields
- [ ] Edge cases are covered

---

---

## Complex QA Pipeline Architecture

```
┌─────────────────────────────┐
│ User provides SDK doc(s)    │
└──────────┬──────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│ Generate question + MULTIPLE query param sets │
│ • Multi-hop: same endpoint, different params  │
│ • Cross-API: different endpoints              │
│ • Cross-metric: same endpoint, different      │
│   metrics (e.g., revenue + netIncome)         │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│ Generate solution steps                       │
│ • What to extract from each SDK response      │
│ • What formula/calculation to apply           │
│ • Financial concepts involved                 │
│   (e.g., CV, profit margin, growth rate)     │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│ Call SDK Gateway for EACH query               │
│ (sequential calls, collect all responses)     │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│ GPT-5.2 generates calculated answer           │
│ from question + solution steps + ALL responses│
│ • Extracts data points per solution steps     │
│ • Performs calculations                       │
│ • Shows work (values + formula)               │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│ Output 5-part JSON:                           │
│ • question (natural language)                │
│ • solution_steps (how to derive the answer)  │
│ • queries (all query configs)                │
│ • sdk_responses (one per query)              │
│ • answer (GPT-5.2 generated with calc)       │
└──────────────────────────────────────────────┘
```

### Key Differences from Unit Test

| Aspect | Unit Test | Complex QA |
|--------|-----------|------------|
| Queries per question | 1 | 1-N (multiple) |
| Answer type | Direct lookup | Requires calculation |
| Solution steps | Not needed | Required |
| Output fields | 4 (question, params, response, answer) | 5 (+ solution_steps) |
| Financial concepts | Basic data retrieval | Derived metrics (P/E, VWAP, margins, volatility, PEG) |

### Components

#### 1. Question Generator

Generates questions that **cannot be answered by a single data lookup**. Each question requires:
- Data from multiple queries OR multiple fields within one response
- Mathematical calculation (growth rate, ratio, comparison, etc.)
- Clear data selection criteria in the question text

**Question diversity dimensions:**
- **Calculation types:** P/E, VWAP, margin change, growth rate, volatility, ATR%, PEG ratio, range spread
- **Query patterns:** cross-API (kline + financial-estimates), cross-year, cross-quarter, cross-symbol
- **Financial concepts:** valuation multiples, institutional benchmarks, profitability margins, risk metrics

#### 2. Solution Step Generator

Produces step-by-step instructions that describe:
1. Which data to extract from which query response
2. What financial formula or calculation to apply
3. How to interpret the result

Example:
```
1. From query 1, extract `epsAvg` for Q1 2024
2. From query 2, extract `epsAvg` for Q2 2024
3. Calculate growth rate: (epsAvg_Q2 − epsAvg_Q1) / epsAvg_Q1 × 100%
```

#### 3. Multi-Query SDK Gateway Client

Executes multiple gateway calls sequentially, collecting responses in order.

**Scripts:**
- `scripts/generate_complex_qa_answer.py` — Single question, LLM answer (requires OPENAI_API_KEY)
- `scripts/run_complex_qa_batch.py` — Batch execution, programmatic answers (no LLM needed)

#### 4. Answer Generator

**Option A: GPT-5.2 (LLM)**
- Receives all SDK responses + solution steps
- Shows calculation work (extracted values + formula)
- Temperature: 0.1, max tokens: 800

**Option B: Programmatic calculation**
- Each question has a dedicated solver function
- Computes answers directly from SDK response fields
- No external API dependency

### Gateway Endpoints

| API | Endpoint | Key Params |
|-----|----------|------------|
| **Kline (OHLCV)** | `/api/v1/stocks/kline` | `ticker`, `start_time` (unix), `end_time` (unix), `interval` (1h/1d/1w), `limit` |
| **Financial Estimates** | `/api/v1/stocks/financial-estimates` | `symbol`, `fiscal_year`, `fiscal_quarter` (Q1/Q2/Q3/Q4/FY) |

### Using the Scripts

**Option A: Single question with LLM answer**
```bash
export OPENAI_API_KEY="sk-..."

# From JSON file
python3 scripts/generate_complex_qa_answer.py input.json

# From stdin
echo '{...}' | python3 scripts/generate_complex_qa_answer.py -
```

**Option B: Batch execution with programmatic answers**
```bash
# Run all questions, compute answers from real gateway data
python3 scripts/run_complex_qa_batch.py batch_input.json \
  1> output.json \
  2> run.log
```

**Input JSON format (single question):**
```json
{
  "question": "What was AAPL's consensus EPS growth rate from Q1 to Q2 2024?",
  "solution_steps": [
    "From query 1, extract epsAvg for Q1 2024",
    "From query 2, extract epsAvg for Q2 2024",
    "Calculate growth rate: (epsAvg_Q2 − epsAvg_Q1) / epsAvg_Q1 × 100%"
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

**Batch input JSON format (array of questions):**
```json
[
  {
    "id": 1,
    "type": "Complex QA",
    "difficulty": "Medium",
    "financial_concept": "Forward P/E Ratio",
    "question": "...",
    "solution_steps": ["...", "..."],
    "queries": [{"request_url": "...", "params": {...}}, ...]
  },
  ...
]
```

**Output JSON format:**
```json
{
  "id": 1,
  "type": "Complex QA",
  "difficulty": "Medium",
  "financial_concept": "Forward P/E Ratio",
  "question": "What is AVGO's forward P/E ratio ...?",
  "solution_steps": ["Extract epsAvg", "Extract price_close", "Calculate P/E"],
  "queries": [
    {"request_url": ".../stocks/financial-estimates", "params": {"symbol": "AVGO", "fiscal_year": 2025, "fiscal_quarter": "FY"}},
    {"request_url": ".../stocks/kline", "params": {"ticker": "AVGO", "start_time": 1735344000, "end_time": 1735603200, "interval": "1d", "limit": 5}}
  ],
  "sdk_responses": [{...complete response 1...}, {...complete response 2...}],
  "answer": "AVGO FY2025 epsAvg = $6.748. Most recent close: $235.58. Forward P/E = 34.91x"
}
```

### Response Field Reference

**Financial Estimates** (all metrics in a single response):
- `epsAvg`, `epsHigh`, `epsLow` — Earnings per share consensus
- `revenueAvg`, `revenueHigh`, `revenueLow` — Revenue consensus
- `ebitdaAvg`, `ebitdaHigh`, `ebitdaLow` — EBITDA consensus
- `ebitAvg`, `ebitHigh`, `ebitLow` — EBIT (operating income) consensus
- `netIncomeAvg`, `netIncomeHigh`, `netIncomeLow` — Net income consensus
- `sgaExpenseAvg`, `sgaExpenseHigh`, `sgaExpenseLow` — SGA expense consensus
- `numAnalystsRevenue`, `numAnalystsEps` — Analyst coverage count
- `calendarEndDate` — Fiscal period end date

**Kline** (per candle):
- `price_open`, `price_high`, `price_low`, `price_close` — OHLC prices
- `volume_traded` — Trading volume
- `trades_count` — Number of trades
- `time_period_start`, `time_period_end` — ISO timestamps
- `time_open`, `time_close` — Unix timestamps

### Question Diversity Guidelines

#### Calculation Types
1. **Forward P/E:** `price_close / epsAvg`
2. **VWAP:** `Σ(TP × volume) / Σ(volume)`, TP = (H+L+C)/3
3. **Operating margin:** `ebitAvg / revenueAvg × 100%`
4. **EPS growth rate:** `(epsAvg_new − epsAvg_old) / epsAvg_old × 100%`
5. **Range spread:** `(high − low) / avg × 100%`
6. **Annualized volatility:** `stdev(ln_returns) × √252`
7. **SGA ratio:** `sgaExpenseAvg / revenueAvg × 100%`
8. **Incremental margin:** `Δ_netIncome / Δ_revenue × 100%`
9. **ATR%:** `mean(price_high − price_low) / mean(price_close) × 100%`
10. **PEG ratio:** `(price / epsAvg) / EPS_growth_rate`

#### Query Patterns
1. **Cross-API** — kline + financial-estimates (e.g., Forward P/E, PEG ratio)
2. **Cross-year** — same symbol, different fiscal_year (e.g., margin YoY)
3. **Cross-quarter** — same symbol, Q1/Q2/Q3/Q4 (e.g., EPS trajectory)
4. **Cross-symbol** — different symbols, same period (e.g., AMZN vs WMT)
5. **Single query, complex derivation** — VWAP, volatility, ATR from kline

#### Symbol Variation
- **Mega-cap tech:** AAPL, MSFT, AMZN, NVDA, AVGO
- **Growth stocks:** TSLA, AMD, CRM, NFLX
- **Value/cyclical:** JPM, WMT
- **Compared pairs:** AMZN vs WMT, HD vs COST

### Testing Checklist

- [x] Batch script fetches all gateway responses
- [x] All 10 questions produce correct answers from live data
- [x] Error in one query doesn't crash the pipeline
- [x] Answers include specific numbers from responses
- [x] Solution steps match the actual calculation performed
- [x] Questions require genuine multi-step reasoning
- [ ] Single-question LLM script accepts JSON input from file/stdin

---

## Future Enhancements

1. **Batch generation** - Generate multiple questions in one script run
2. **Trading Strategy pipeline** - Backtest strategy answers
3. **Auto-grading** - Compare user answers against standard answers
4. **Question templates** - Parameterized templates for rapid generation
5. **Parallel query execution** - Run independent queries concurrently
