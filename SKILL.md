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

**Key rules:**
- Never mention APIs, endpoints, or data sources in the question text
- One API call is enough to answer
- Answer is a direct lookup or simple extraction from the response
- Vary symbols/tickers (QQQ, SPY, AAPL, MSFT, TSLA, etc.)
- Vary query patterns: single value lookup, comparisons, counts, rankings, aggregations

### 2. Complex QA Questions
Multi-hop queries requiring multiple data points and calculations. Include specific requirements for data selection.

**Example:**
```
Q: What was Apple's Free Cash Flow per Share for fiscal year 2025? Outstanding shares count should use the closest to its fiscal year-end date (September 30, 2025).

Standard Answer: Apple's Free Cash Flow per Share for fiscal year 2025 was $6.82. This is calculated by dividing the Free Cash Flow of $108.5B by the outstanding shares count of 15.9B as of September 30, 2025 (the closest date to fiscal year-end).
```

**Key rules:**
- Requires 2+ API calls or combining multiple fields from one response
- Answer requires calculation (growth rate, ratio, comparison, etc.)
- Must include solution steps: what to extract and what formula to apply
- Specify data selection criteria clearly (e.g., "use closest date to...", "top N by...")
- Cover diverse financial concepts: P/E, VWAP, margins, volatility, PEG, ATR, etc.

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

**Key rules:**
- Specify exact instrument, exchange, and timezone
- Define clear entry signal, position size, and exit rule
- Include concrete timeframe with start/end dates
- Answer must list each trade with entry/exit prices and P&L

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

## Output Format

**Default format:** Markdown with question and standard answer pairs

**Alternative format:** JSON (for integration with quiz platforms or automated grading systems)

> 💡 **No OPENAI_API_KEY?** Scripts will still output `question`, `query_params`/`queries`, `sdk_response(s)` with `answer: ""`. Use any LLM to generate answers from the returned data.

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
    },
    {
      "id": 2,
      "type": "Complex QA",
      "question": "...",
      "solution_steps": ["Step 1: ...", "Step 2: ...", "Step 3: ..."],
      "queries": [{"request_url": "...", "params": {...}}, ...],
      "sdk_responses": [{...}, ...],
      "answer": "..."
    }
  ]
}
```

Ask the user if they need JSON format instead of Markdown.

## Reference Materials

**Examples** (in `examples/`):
- `unit_test_examples.md` - Unit Test examples
- `complex_qa_examples.md` - Complex QA examples

**Pipelines** (in `scripts/`):
- `PIPELINE.md` - Pipeline architecture, JSON formats, field reference
- `GUIDELINES.md` - Question generation guidelines and patterns
