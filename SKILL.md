---
name: sdk-quiz-generator
description: Generate comprehensive open-ended test questions from SDK documentation. Use when the user asks to create test questions, quiz problems, or assessment materials based on API documentation. Generates three types of natural language questions - Unit Test (specific API functionality), Complex QA (multi-step workflows), and Trading Strategy (real-world application scenarios).
---

# SDK Quiz Generator

## Overview

This skill transforms SDK documentation into structured test questions and quizzes. It analyzes API documentation to generate comprehensive assessment materials covering API usage, parameters, return values, and real-world scenarios.

## Quick Start

**Basic usage:**
```
User: "Generate quiz questions from this SDK doc"
→ Read the SDK documentation
→ Analyze structure (API name, parameters, return values, examples)
→ Ask user for difficulty level (easy/medium/hard/mixed)
→ Generate 5-10 questions across the three types: Unit Test, Complex QA, Trading Strategy
```

**With specific focus:**
```
User: "Create Trading Strategy questions for the Financial Estimate API"
→ Focus on real-world trading scenarios
→ Generate questions about using the API for investment decisions
→ Include standard answers with detailed reasoning
```

## Question Types

Generate open-ended natural language questions in **three categories only**:

### 1. Unit Test Questions
Single-point data queries asking for specific metrics or values. Do NOT mention APIs or data sources in the question.

**Example:**
```
Q: What is BA's debt-to-asset ratio based on 2025 Q2 earnings?

Standard Answer: BA's debt-to-asset ratio for 2025 Q2 was 0.73, calculated from total debt of $58.2B divided by total assets of $79.8B as reported in their Q2 2025 earnings.
```

### 2. Complex QA Questions
Multi-hop queries requiring multiple data points and calculations. Include specific requirements for data selection.

**Example:**
```
Q: What was Apple's Free Cash Flow per Share for fiscal year 2025? Outstanding shares count should use the closest to its fiscal year-end date (September 30, 2025).

Standard Answer: Apple's Free Cash Flow per Share for fiscal year 2025 was $6.82. This is calculated by dividing the Free Cash Flow of $108.5B by the outstanding shares count of 15.9B as of September 30, 2025 (the closest date to fiscal year-end).
```

### 3. Trading Strategy Questions
Real trading strategies with specific instruments, timeframes, entry/exit rules, and position management. Focus on signal identification, position sizing, and exit timing.

**Example:**
```
Q: Using BTCUSDT Perpetual Futures (Binance, UTC, 2025-11-10 to 2025-11-20): identify all days where Binance's BTCUSDT long/short ratio closes above 2. At the daily close of such days, open a 100% short position. Exit after 24 hours.

Standard Answer: During the specified period, the long/short ratio closed above 2 on 2025-11-12 (2.15), 2025-11-15 (2.31), and 2025-11-18 (2.08). 
- Trade 1: Short at daily close 2025-11-12 23:59 UTC ($89,432), exit 2025-11-13 23:59 UTC ($87,210), profit: +2.48%
- Trade 2: Short at daily close 2025-11-15 23:59 UTC ($91,820), exit 2025-11-16 23:59 UTC ($90,105), profit: +1.87%
- Trade 3: Short at daily close 2025-11-18 23:59 UTC ($93,015), exit 2025-11-19 23:59 UTC ($94,330), loss: -1.41%
Total strategy return: +2.94% over 3 trades.
```

## Question Generation Workflow

**Step 1: Parse SDK Documentation**
- Identify API name and purpose
- Extract all parameters (name, type, required/optional, description)
- Extract return value structure and field meanings
- Note any examples or usage patterns

**Step 2: Generate Question Pool**

For each API, create a balanced mix:
- **30-40% Unit Test questions** - Single-point data queries (DO NOT mention APIs in question text)
- **30-40% Complex QA questions** - Multi-hop calculations with specific data requirements
- **20-30% Trading Strategy questions** - Concrete trading strategies with instruments, timeframes, signals, position sizing, and exit rules

**Important for Unit Test questions:**
- **Vary the symbols/tickers** - Use different stocks/ETFs (e.g., QQQ, SPY, AAPL, MSFT, TSLA)
- **Test different fields** - Don't just ask for the largest value; test specific countries, comparisons, counts, rankings
- **Mix query patterns** - Single value lookup, comparisons, aggregations, edge cases

**Step 3: Format Output**

Present questions in clear, numbered format with standard answers:

```markdown
## Quiz: [API Name]

**Total Questions: 10**

### Question 1: [Unit Test / Complex QA / Trading Strategy]
[Question text in natural language]

**Standard Answer:**
[Complete answer explaining the approach, required parameters, expected results, and reasoning]

---

### Question 2: [Type]
[Question text]

**Standard Answer:**
[Answer text]

---
```

## Best Practices

**Question Quality:**
- **Unit Test**: Ask for specific metrics/values directly. Never mention APIs or data sources.
- **Complex QA**: Require multiple data points and calculations. Specify data selection criteria (e.g., "use closest date to...")
- **Trading Strategy**: Include specific instruments, exchanges, timeframes, entry signals, position size, and exit rules
- Provide complete standard answers with concrete numbers and step-by-step calculations
- Use realistic data and actual market scenarios

**Difficulty Levels:**

Ask the user to choose difficulty level or mix:
- **Easy**: Basic API usage, single-API workflows, straightforward parameter combinations
- **Medium**: Multi-API workflows, data interpretation, comparing results across timeframes
- **Hard**: Complex trading strategies, edge case handling, performance optimization, multi-step decision trees

**Example prompt:** "What difficulty level do you want? (easy/medium/hard/mixed)"

If user chooses "mixed", ask for ratio (e.g., "40% easy, 40% medium, 20% hard") or use default balanced mix

**Coverage:**
- Test all required parameters across Unit Test questions
- Combine multiple APIs in Complex QA questions
- Include realistic market scenarios in Trading Strategy questions
- Cover edge cases and error handling

## Reference Materials

See `references/` directory for example SDK documentation:
- `createOHLCVProvider-example.md` - Data provider API example
- `financial-estimate-guidance-example.md` - Financial data API examples

Load these references to understand documentation format and generate similar questions for new SDK docs.

## Unit Test Answer Generation Pipeline

For **Unit Test questions**, we generate standard answers by calling the actual SDK:

### Pipeline Steps

```
1. User provides SDK documentation
   ↓
2. Generate question + query parameters
   Example: 
   - Question: "What is SPY's largest country weighting?"
   - Parameters: {"symbol": "SPY"}
   ↓
3. Call SDK gateway with parameters
   (request_url provided by user, e.g., https://data-gateway.prd.space.id/api/v1/etf/country-weightings)
   ↓
4. Get SDK raw response
   ↓
5. Question + SDK response → GPT-5.2 → Natural language answer
   ↓
Final output:
{
  "question": "What is SPY's largest country weighting?",
  "query_params": {"symbol": "SPY"},
  "sdk_response": {...complete SDK response...},
  "answer": "United States is SPY's largest country weighting at 97.38%."
}
```

### Using the Script

```bash
# Set OpenAI API key (required)
export OPENAI_API_KEY="sk-..."

# Generate a single Unit Test with answer
python3 scripts/generate_unit_test_answer.py \
  "What is SPY's largest country weighting?" \
  "https://data-gateway.prd.space.id/api/v1/etf/country-weightings" \
  symbol=SPY
```

The script (`scripts/generate_unit_test_answer.py`) handles:
- SDK gateway API calls with authentication
- GPT-5.2 answer generation
- Complete JSON output with all 4 components

### Example Variations

**Different tickers:**
```bash
symbol=QQQ  # Nasdaq 100
symbol=SPY  # S&P 500
symbol=IWM  # Russell 2000
```

**Different fields to test:**
- Largest/smallest value: "What is QQQ's largest country weighting?"
- Specific lookup: "What is the United Kingdom's weight percentage in SPY?"
- Counting: "How many countries are represented in IWM's holdings?"
- Ranking: "What are the top three countries by weighting in QQQ?"
- Comparison: "What is the difference in weight percentage between Canada and Ireland in QQQ?"

## Output Format

**Default format:** Markdown with question and standard answer pairs

**Alternative format:**
- JSON (for integration with quiz platforms or automated grading systems)

Structure:
```json
{
  "quiz_name": "Financial Estimate API",
  "questions": [
    {
      "id": 1,
      "type": "Unit Test",
      "question": "...",
      "query_params": {...},
      "sdk_response": {...},
      "answer": "..."
    }
  ]
}
```

Ask the user if they need JSON format instead of Markdown.
