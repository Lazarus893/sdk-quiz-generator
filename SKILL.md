---
name: sdk-quiz-generator
description: Generate comprehensive test questions and quizzes from SDK documentation. Use when the user asks to create test questions, quiz problems, or assessment materials based on API documentation, SDK guides, or technical reference materials. Supports multiple question types including multiple-choice, code completion, scenario-based problems, and parameter validation questions.
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
→ Generate 5-10 diverse question types
```

**With specific focus:**
```
User: "Create parameter validation questions for the Financial Estimate API"
→ Focus on input parameters and validation logic
→ Generate questions testing edge cases and required fields
```

## Question Types

Generate a mix of question types to comprehensively test understanding:

### 1. Multiple Choice Questions (概念题)
Test understanding of API purpose, parameter meanings, and return value interpretations.

**Example:**
```
Q: What does the `periodicity` parameter in Financial Estimate API control?
A) The fiscal year period
B) The frequency of data updates (annual/quarterly)
C) The number of estimates to return
D) The standard deviation calculation method

Answer: B
```

### 2. Code Completion Questions (代码填空)
Test practical API usage by providing incomplete code snippets.

**Example:**
```
Q: Complete the following API call to fetch quarterly estimates for AAPL:

const response = await financialEstimate({
  symbol: "AAPL",
  ______: "quarterly",
  observedAtStart: "2024-01-01"
});

Options: periodicity, frequency, timeframe, interval
Answer: periodicity
```

### 3. Scenario-Based Questions (场景题)
Test ability to apply API knowledge to real-world use cases.

**Example:**
```
Q: You need to compare analyst consensus estimates before and after an earnings call.
Which combination of parameters would you use?

A) observedAtStart + observedAtEnd with the same date
B) Two separate calls with different observedAt ranges
C) Single call with guidanceMidpoint comparison
D) Use prevMidpoint field in Guidance API

Answer: B (Financial Estimate doesn't provide before/after comparison in one call)
```

### 4. Parameter Validation Questions (参数校验题)
Test understanding of parameter constraints and validation rules.

**Example:**
```
Q: Which of the following API calls will fail validation?

A) { symbol: "AAPL", periodicity: "quarterly" }
B) { symbol: "AAPL", metrics: ["revenue"], limit: 0 }
C) { symbol: "AAPL", fiscalYear: 2024 }
D) { symbol: "", periodicity: "annual" }

Answer: B and D (limit must be > 0, symbol cannot be empty)
```

### 5. Output Interpretation Questions (返回值理解题)
Test understanding of response structure and field meanings.

**Example:**
```
Q: If an API returns { estimateCount: 15, up: 8, down: 3 }, what can you conclude?

A) 8 analysts revised estimates upward, 3 revised downward, 4 kept unchanged
B) There are 15 total estimates with 8 positive and 3 negative values
C) The estimate increased by 8 and decreased by 3 over time
D) 8 estimates are above mean, 3 are below mean

Answer: A
```

## Question Generation Workflow

**Step 1: Parse SDK Documentation**
- Identify API name and purpose
- Extract all parameters (name, type, required/optional, description)
- Extract return value structure and field meanings
- Note any examples or usage patterns

**Step 2: Generate Question Pool**

For each API, create at least:
- 2-3 multiple choice questions (concept understanding)
- 1-2 code completion questions (practical usage)
- 1-2 scenario questions (real-world application)
- 1-2 parameter validation questions (edge cases)
- 1-2 output interpretation questions (response understanding)

**Step 3: Format Output**

Present questions in clear, numbered format:

```markdown
## Quiz: [API Name]

**Total Questions: 10 | Time: 15 minutes**

### Question 1: [Type]
[Question text]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

**Answer:** [Correct answer with brief explanation]

---

### Question 2: [Type]
...
```

## Best Practices

**Question Quality:**
- Use realistic parameter values and scenarios
- Avoid trick questions; test genuine understanding
- Include "all of the above" / "none of the above" sparingly
- Provide brief explanations with answers for learning

**Difficulty Levels:**

Ask the user to choose difficulty level or mix:
- **Easy**: Basic API usage, required parameter understanding, simple return value interpretation
- **Medium**: Combining parameters, comparing multiple APIs, error handling scenarios
- **Hard**: Edge cases, complex multi-step scenarios, performance optimization, architecture decisions

**Example prompt:** "What difficulty level do you want? (easy/medium/hard/mixed)"

If user chooses "mixed", ask for ratio (e.g., "50% easy, 30% medium, 20% hard") or use default balanced mix

**Coverage:**
- Test all required parameters
- Test at least 2-3 optional parameters per API
- Include questions about error conditions
- Test understanding of return value structure

## Reference Materials

See `references/` directory for example SDK documentation:
- `createOHLCVProvider-example.md` - Data provider API example
- `financial-estimate-guidance-example.md` - Financial data API examples

Load these references to understand documentation format and generate similar questions for new SDK docs.

## Output Format

**Default format:** Markdown quiz with inline answers

**Alternative formats available:**
- JSON (for integration with quiz platforms)
- CSV (for spreadsheet import)
- Interactive HTML (with answer reveal on click)

Ask the user if they need a specific format.
