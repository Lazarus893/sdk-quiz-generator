# SDK Quiz Generator

**OpenClaw Skill** for generating comprehensive test questions from SDK documentation.

## 🎯 What It Does

Transforms API/SDK documentation into structured test questions covering:
- Multiple-choice questions (概念题)
- Code completion questions (代码填空)
- Scenario-based problems (场景题)
- Parameter validation questions (参数校验题)
- Output interpretation questions (返回值理解题)

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
- 10 comprehensive questions covering all API aspects
- Multiple question types for complete understanding
- Answers with explanations for learning

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
- Output format options (Markdown/JSON/CSV/HTML)

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
