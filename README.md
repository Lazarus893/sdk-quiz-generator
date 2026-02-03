# SDK Quiz Generator

A skill for generating test questions with standard answers from SDK documentation. Produces three question types: **Unit Test**, **Complex QA**, and **Trading Strategy**.

> 📖 For question types, examples, generation workflow, and best practices, see **[SKILL.md](SKILL.md)**

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

```bash
# Single question (LLM)
export OPENAI_API_KEY="sk-..."
python3 scripts/generate_complex_qa_answer.py input.json

# Batch (LLM)
python3 scripts/generate_complex_qa_answer.py batch.json --batch

# Batch (programmatic, no LLM)
python3 scripts/generate_complex_qa_answer.py batch.json --batch --no-llm
```

See `scripts/PIPELINE.md` for input JSON format.

## Project Structure

```
sdk-quiz-generator/
├── SKILL.md                           # Skill definition (question types, workflow)
├── examples/
│   ├── unit_test_examples.md          # Unit Test examples
│   └── complex_qa_examples.md         # Complex QA examples
└── scripts/
    ├── PIPELINE.md                    # Pipeline architecture + JSON formats
    ├── GUIDELINES.md                  # Question generation guidelines
    ├── generate_unit_test_answer.py   # Unit Test answer (LLM)
    ├── generate_complex_qa_answer.py  # Complex QA (single/batch, LLM/programmatic)
    └── sid_gateway_client.py          # Gateway client
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Optional | OpenAI API key (GPT-5.2). If not set, `answer` will be empty |
| `SID_API_KEY` | No (has default) | Gateway authentication key |

> 💡 **No API Key?** Scripts will still fetch SDK data and output `question`, `query_params`, `sdk_response` — just with `answer: ""`. You can then use any LLM to generate the answer from the returned data.
