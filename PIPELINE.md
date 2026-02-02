# SDK Quiz Generator Pipeline

Complete workflow for generating quiz questions with standard answers from SDK documentation.

## Overview

This skill generates three types of questions from SDK documentation:
1. **Unit Test** - Single-point data queries
2. **Complex QA** - Multi-hop calculations
3. **Trading Strategy** - Real trading strategies with entry/exit rules

This document focuses on the **Unit Test answer generation pipeline**.

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

## Future Enhancements

1. **Batch generation** - Generate multiple questions in one script run
2. **Complex QA pipeline** - Multi-hop query support
3. **Trading Strategy validation** - Backtest strategy answers
4. **Auto-grading** - Compare user answers against standard answers
5. **Question templates** - Parameterized templates for rapid generation
