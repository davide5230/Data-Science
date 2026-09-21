# AI Market Intelligence Monitor

Automated market-intelligence pipeline that collects recent news from an external API, filters and deduplicates relevant articles, analyzes them with a local LLM, generates deterministic metrics and a structured business-intelligence report, stores historical results in SQLite, and automatically delivers new reports by email.

## Key Features

- External REST API integration
- News normalization and relevance filtering
- In-run and cross-run article deduplication
- Structured LLM analysis with Ollama and Pydantic
- Deterministic market metrics in Python
- AI-generated market-intelligence reports
- SQLite report history
- Persistent application logging
- Scheduled execution
- Automated SMTP email delivery
- Environment-based credential management

## Architecture

```text
External News API
        |
        v
   collector.py
        |
        v
   processor.py
        |
        v
Cross-run deduplication
        |
        v
   analyzer.py
      /   \
     v     v
metrics.py reporter.py
     \     /
      v   v
    pipeline.py
        |
        v
    storage.py
        |
        v
    delivery.py

scheduler.py -> periodic execution
```

## Design Principle

Python handles deterministic operations such as filtering, deduplication, counting and persistence.

The LLM is used only for tasks requiring semantic interpretation, including article classification, business-impact analysis and cross-article market synthesis.

## Project Structure

```text
AI-market-intelligence-monitor/
├── src/
│   ├── analyzer.py
│   ├── collector.py
│   ├── delivery.py
│   ├── logger.py
│   ├── metrics.py
│   ├── pipeline.py
│   ├── processor.py
│   ├── reporter.py
│   ├── scheduler.py
│   ├── schemas.py
│   └── storage.py
├── data/
│   └── README.md
├── docs/
│   └── architecture.md
├── logs/
│   └── README.md
├── outputs/
│   └── sample_report.json
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Tech Stack

Python | Requests | REST APIs | Ollama | Qwen | Pydantic | SQLite | SMTP | Schedule | Logging

## Setup

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Make sure Ollama is installed and the configured model is available:

```bash
ollama pull qwen3.5:4b
```

4. Copy `.env.example` to `.env` and configure SMTP credentials.
5. Run the pipeline manually:

```bash
python src/pipeline.py
```

6. Run the scheduled monitor:

```bash
python src/scheduler.py
```

The scheduler is configured to run daily at 08:00 local system time.

## Output

Each successful run can produce:

- structured per-article intelligence;
- deterministic category and importance statistics;
- one consolidated market-intelligence report;
- a persisted SQLite history entry;
- an email containing the final report.

Previously processed articles are stored in SQLite so later runs do not repeatedly analyze the same news item.

## Security

Runtime secrets and generated data are excluded from version control:

- `.env`
- SQLite database files
- runtime log files

Use an app-specific SMTP password or equivalent provider credential rather than an account password.

## Current Limitation

The project currently uses a local Ollama model.

Scheduled execution therefore requires the machine hosting Ollama and the Python scheduler to remain available. A production deployment could replace the local model with a hosted LLM endpoint or deploy both inference and the application to persistent infrastructure.
