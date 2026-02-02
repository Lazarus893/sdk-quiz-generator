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
Test specific API functionality, parameter usage, and return values with focused questions.

**Example:**
```
Q: What parameters are required to fetch quarterly revenue estimates for AAPL using the Financial Estimate API?

Standard Answer: The required parameters are `symbol` (set to "AAPL"), `metrics` (set to ["revenue"]), and `periodicity` (set to "quarterly"). The API also requires at least one of `observedAtStart`/`observedAtEnd` or `fiscalYear` to define the time range.
```

### 2. Complex QA Questions
Test understanding of API combinations, data interpretation, and multi-step workflows.

**Example:**
```
Q: How would you use the Financial Estimate and Guidance APIs together to determine if a company's guidance beat analyst expectations?

Standard Answer: First, call the Guidance API with the company's symbol and fiscal period to get `guidanceMidpoint` and `meanBefore` fields. Compare these two values: if `guidanceMidpoint > meanBefore`, the guidance beat expectations. Alternatively, use the `meanSurpriseAmt` or `meanSurprisePct` fields directly, where positive values indicate guidance exceeded expectations.
```

### 3. Trading Strategy Questions
Test application of API data to real-world trading scenarios and decision-making.

**Example:**
```
Q: Design a trading strategy that identifies stocks where analyst consensus is strengthening. Which APIs and parameters would you use, and what signals would trigger a buy decision?

Standard Answer: Use the Financial Estimate API with `observedAtStart` and `observedAtEnd` to track estimate changes over time. Monitor the `up` and `down` fields to track analyst revisions. A buy signal could trigger when: (1) `up / (up + down) > 0.7` (70%+ positive revisions), (2) `mean` is increasing over consecutive periods, and (3) `standardDeviation` is decreasing (increasing consensus). Combine with the Guidance API to confirm company guidance aligns with or exceeds the strengthening consensus.
```

## Question Generation Workflow

**Step 1: Parse SDK Documentation**
- Identify API name and purpose
- Extract all parameters (name, type, required/optional, description)
- Extract return value structure and field meanings
- Note any examples or usage patterns

**Step 2: Generate Question Pool**

For each API, create a balanced mix:
- **30-40% Unit Test questions** - Focused on specific API functionality
- **30-40% Complex QA questions** - Multi-step workflows and data interpretation
- **20-30% Trading Strategy questions** - Real-world application and decision-making

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
- Use realistic parameter values and scenarios
- Questions should be open-ended, requiring natural language answers
- Provide complete standard answers with reasoning and explanation
- Focus on practical application and understanding, not memorization

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
      "standard_answer": "..."
    }
  ]
}
```

Ask the user if they need JSON format instead of Markdown.
