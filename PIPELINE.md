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
| Financial concepts | Basic data retrieval | Derived metrics (ratios, growth, margins) |

### Components

#### 1. Question Generator

Generates questions that **cannot be answered by a single data lookup**. Each question requires:
- Data from multiple queries OR multiple fields
- Mathematical calculation (growth rate, ratio, comparison, etc.)
- Clear data selection criteria in the question text

**Question diversity dimensions:**
- **Calculation types:** growth rate, ratio, percentage comparison, absolute difference, aggregation
- **Query patterns:** cross-quarter, cross-symbol, cross-metric, cross-API
- **Financial concepts:** profit margin, EPS growth, consensus dispersion (CV), guidance surprise, revision momentum

#### 2. Solution Step Generator

Produces step-by-step instructions that describe:
1. Which data to extract from which query response
2. What financial formula or calculation to apply
3. How to interpret the result

Example:
```
1. From query 1, extract the `mean` EPS for Q1 2024
2. From query 2, extract the `mean` EPS for Q2 2024
3. Calculate growth rate: (Q2_mean - Q1_mean) / Q1_mean × 100%
```

#### 3. Multi-Query SDK Gateway Client

Executes multiple gateway calls sequentially, collecting responses in order.

**Script location:** `scripts/generate_complex_qa_answer.py`

#### 4. Answer Generator (GPT-5.2)

Same model as Unit Test but with enhanced prompt:
- Receives all SDK responses + solution steps
- Shows calculation work (extracted values + formula)
- Temperature: 0.1 (factual)
- Max tokens: 800 (higher than Unit Test due to calculation details)

### Using the Script

Complex QA uses JSON input (file or stdin) due to the multi-query structure:

```bash
export OPENAI_API_KEY="sk-..."

# From JSON file
python3 scripts/generate_complex_qa_answer.py input.json

# From stdin
echo '{...}' | python3 scripts/generate_complex_qa_answer.py -
```

**Input JSON format:**
```json
{
  "question": "What was AAPL's consensus EPS growth rate from Q1 to Q2 2024?",
  "solution_steps": [
    "From query 1, extract the mean EPS for Q1 2024",
    "From query 2, extract the mean EPS for Q2 2024",
    "Calculate growth rate: (Q2_mean - Q1_mean) / Q1_mean × 100%"
  ],
  "queries": [
    {
      "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
      "params": {"symbol": "AAPL", "metrics": "eps", "fiscalYear": 2024, "fiscalQuarter": 1, "periodicity": "quarterly"}
    },
    {
      "request_url": "https://data-gateway.prd.space.id/api/v1/financial-estimate",
      "params": {"symbol": "AAPL", "metrics": "eps", "fiscalYear": 2024, "fiscalQuarter": 2, "periodicity": "quarterly"}
    }
  ]
}
```

**Output JSON format:**
```json
{
  "question": "What was AAPL's consensus EPS growth rate from Q1 to Q2 2024?",
  "solution_steps": [
    "From query 1, extract the mean EPS for Q1 2024",
    "From query 2, extract the mean EPS for Q2 2024",
    "Calculate growth rate: (Q2_mean - Q1_mean) / Q1_mean × 100%"
  ],
  "queries": [
    {"request_url": "...", "params": {...}},
    {"request_url": "...", "params": {...}}
  ],
  "sdk_responses": [
    {...complete response 1...},
    {...complete response 2...}
  ],
  "answer": "AAPL's consensus EPS grew from $1.52 (Q1 2024) to $1.71 (Q2 2024), a growth rate of 12.5%. Calculation: ($1.71 - $1.52) / $1.52 × 100% = 12.5%."
}
```

### Question Diversity Guidelines

#### Calculation Types
1. **Growth rate:** `(new - old) / old × 100%` (cross-quarter, cross-year)
2. **Beat/miss analysis:** `guidance - consensus` (absolute + percentage)
3. **Coefficient of Variation:** `stdDev / mean × 100%` (consensus strength)
4. **Revision ratio:** `up / (up + down) × 100%` (estimate momentum)
5. **Profitability ratio:** `netIncome / revenue × 100%` (cross-metric)
6. **Range spread:** `(high - low) / mean × 100%` (uncertainty measure)
7. **Guidance pull:** `(meanAfter - meanBefore) / (guidance - meanBefore) × 100%`

#### Query Patterns
1. **Same endpoint, different quarters** — e.g., Q1 vs Q2 EPS
2. **Same endpoint, different symbols** — e.g., NVDA vs INTC consensus
3. **Same endpoint, different metrics** — e.g., netIncome + revenue → margin
4. **Cross-API** — e.g., financial-estimate + OHLCV → price vs estimate range
5. **Single query, derived fields** — e.g., guidance response has both meanBefore and meanAfter

#### Symbol Variation
- **Mega-cap tech:** AAPL, MSFT, GOOGL, AMZN, META, NVDA
- **Growth stocks:** TSLA, AMD, CRM, NFLX
- **Value/cyclical:** JPM, BAC, XOM, CVX
- **Compared pairs:** NVDA vs INTC, AAPL vs MSFT, AMZN vs WMT

### Testing Checklist

- [ ] Script accepts JSON input from file
- [ ] Script accepts JSON input from stdin
- [ ] All queries execute and responses are collected
- [ ] Error in one query doesn't crash the pipeline
- [ ] GPT-5.2 answer shows calculation work
- [ ] Answer includes specific numbers from responses
- [ ] Solution steps match the actual calculation performed
- [ ] Questions require genuine multi-step reasoning

---

## Future Enhancements

1. **Batch generation** - Generate multiple questions in one script run
2. **Trading Strategy pipeline** - Backtest strategy answers
3. **Auto-grading** - Compare user answers against standard answers
4. **Question templates** - Parameterized templates for rapid generation
5. **Parallel query execution** - Run independent queries concurrently
