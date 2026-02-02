# SDK Quiz Generator

**OpenClaw Skill** for generating comprehensive test questions from SDK documentation.

## 🎯 What It Does

Transforms API/SDK documentation into open-ended test questions covering:
- **Unit Test questions** - Focused API functionality testing
- **Complex QA questions** - Multi-step workflows and data interpretation
- **Trading Strategy questions** - Real-world application scenarios

All questions are natural language Q&A format with complete standard answers.

## 📦 Installation

1. Download `sdk-quiz-generator.skill` from [Releases](https://github.com/Lazarus893/sdk-quiz-generator/releases)
2. Install the skill:
   ```bash
   openclaw skill install sdk-quiz-generator.skill
   ```

Or install directly from the skill directory:
```bash
openclaw skill install /path/to/sdk-quiz-generator/
```

## 🚀 Usage

Simply ask your OpenClaw agent to generate quiz questions from SDK documentation:

```
Generate quiz questions from this SDK doc

[paste your SDK documentation]
```

**Difficulty selection:**
- Easy: Basic API usage and parameters
- Medium: Complex scenarios and error handling
- Hard: Edge cases and performance optimization
- Mixed: Balanced combination

## 📚 Example

Input: Financial Estimate API documentation

Output:
- 10 comprehensive open-ended questions
- Mix of Unit Test, Complex QA, and Trading Strategy questions
- Complete standard answers with detailed reasoning and explanations

## 🔧 Skill Structure

```
sdk-quiz-generator/
├── SKILL.md                                    # Main skill instructions
└── references/
    ├── createOHLCVProvider-example.md          # Example: OHLCV data API
    └── financial-estimate-guidance-example.md  # Example: Financial APIs
```

## 📖 Documentation

See [SKILL.md](SKILL.md) for complete documentation on:
- Question types and formats
- Generation workflow
- Best practices
- Output format options (Markdown/JSON)

## 🤝 Contributing

Contributions welcome! Feel free to:
- Add more SDK documentation examples to `references/`
- Suggest new question types
- Improve question generation patterns

## 📄 License

MIT

## 🔗 Links

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Skill Hub](https://clawhub.com)
