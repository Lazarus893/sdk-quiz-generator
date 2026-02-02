# SDK Quiz Generator

A skill for generating test questions with standard answers from SDK documentation. It parses API docs and produces three types of natural language questions — each with verifiable answers computed from live gateway data.

## Question Types

### Unit Test
Single-point data queries. One API call, direct answer lookup.

```
Q: What is QQQ's largest country weighting?
A: United States is QQQ's largest country weighting at 94.66%.
```

### Complex QA
Multi-hop queries requiring multiple API calls and calculations. Includes solution steps explaining what financial concept is involved and how to derive the answer.

```
Q: Calculate NVIDIA's PEG ratio using FY2024→FY2025 EPS growth and December 2024 avg closing price.

Solution Steps:
1. EPS growth = (epsAvg_2025 − epsAvg_2024) / epsAvg_2024 × 100
2. Forward P/E = avg_close / epsAvg_2025
3. PEG = Forward_PE / EPS_growth_rate

A: EPS growth = 37.17%. Forward P/E = 46.53x. PEG = 1.25 — market is paying a premium above the growth rate.
```

### Trading Strategy
Real trading strategies with specific instruments, timeframes, entry/exit rules, and position management.

## Gateway Endpoints

| API | Endpoint | Key Params |
|-----|----------|------------|
| Kline (OHLCV) | `/api/v1/stocks/kline` | `ticker`, `start_time` (unix), `end_time` (unix), `interval` (1h/1d/1w), `limit` |
| Financial Estimates | `/api/v1/stocks/financial-estimates` | `symbol`, `fiscal_year`, `fiscal_quarter` (Q1/Q2/Q3/Q4/FY) |

Base URL: `https://data-gateway.prd.space.id`

## Installation

Place the skill directory under your agent's skill path:

```bash
cp -r sdk-quiz-generator /path/to/skills/
```

Or clone directly:

```bash
git clone https://github.com/Lazarus893/sdk-quiz-generator.git /path/to/skills/sdk-quiz-generator
```

## Usage

### Generate Unit Test answers

```bash
export OPENAI_API_KEY="sk-..."

python3 scripts/generate_unit_test_answer.py \
  "What is SPY's largest country weighting?" \
  "https://data-gateway.prd.space.id/api/v1/etf/country-weightings" \
  symbol=SPY
```

### Generate Complex QA answers

**Single question (LLM answer):**
```bash
export OPENAI_API_KEY="sk-..."
python3 scripts/generate_complex_qa_answer.py input.json
```

**Batch execution (programmatic answers, no LLM needed):**
```bash
python3 scripts/run_complex_qa_batch.py batch_input.json \
  > output.json
```

Input JSON format:
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

## Project Structure

```
sdk-quiz-generator/
├── SKILL.md                                      # Skill definition (question types, workflow, pipelines)
├── examples/
│   ├── unit_test_examples.md                     # 8 Unit Test examples (ETF country weightings)
│   └── complex_qa_examples.md                    # Complex QA examples with calculations
└── scripts/
    ├── PIPELINE.md                               # Pipeline architecture (Unit Test + Complex QA)
    ├── COMPLEX_QA_PIPELINE.md                    # Complex QA workflow patterns and guidelines
    ├── generate_unit_test_answer.py              # Unit Test: single question → LLM answer
    ├── generate_complex_qa_answer.py             # Complex QA: single question → LLM answer
    ├── run_complex_qa_batch.py                   # Complex QA: batch → programmatic answers
    └── sid_gateway_client.py                     # Generic gateway client
```

## Documentation

- **[SKILL.md](SKILL.md)** — Skill definition: question types, generation workflow, field reference, usage guide
- **[scripts/PIPELINE.md](scripts/PIPELINE.md)** — Pipeline architecture: Unit Test and Complex QA answer generation
- **[scripts/COMPLEX_QA_PIPELINE.md](scripts/COMPLEX_QA_PIPELINE.md)** — Complex QA workflow patterns and guidelines
- **[examples/](examples/)** — Example questions with real answers for both question types

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | For LLM scripts | OpenAI API key (GPT-5.2) |
| `SID_API_KEY` | No (has default) | Gateway authentication key |
