# Architecture

## Overview

The AI Market Intelligence Monitor is an automated pipeline for collecting, filtering, analyzing, persisting and delivering market intelligence from external news sources.

## Data Flow

```text
External News API
        |
        v
Collector
        |
        v
Processor
  - normalization
  - missing-data filtering
  - language filtering
  - relevance filtering
  - in-run deduplication
        |
        v
SQLite cross-run deduplication
        |
        v
LLM Article Analyzer
        |
        +------------------+
        |                  |
        v                  v
Python Metrics       LLM Report Aggregation
        |                  |
        +--------+---------+
                 |
                 v
             Pipeline
                 |
                 v
         SQLite Persistence
                 |
                 v
           Email Delivery

Scheduler -> periodic pipeline execution
Logger    -> persistent operational trace
```

## Components

### collector.py

Connects to the external news API and retrieves raw JSON data. Network failures, timeouts and HTTP errors are converted into explicit runtime errors.

### processor.py

Normalizes the API response, removes incomplete records, filters by language and keyword relevance, and deduplicates articles by URL within the current run.

### schemas.py

Defines the Pydantic models used to constrain and validate structured LLM outputs.

### analyzer.py

Uses a local Ollama model to convert individual articles into structured market-intelligence objects. The LLM is restricted to information present in the title and description.

### metrics.py

Computes deterministic statistics in Python, including importance distribution, category distribution and company mention frequency.

### reporter.py

Aggregates validated article analyses into one structured executive market-intelligence report.

### storage.py

Uses SQLite for two purposes:

- storing historical generated reports;
- storing successfully analyzed article IDs for cross-run deduplication.

Only articles with a successful structured analysis are marked as seen.

### delivery.py

Formats the report as plain-text email and sends it through SMTP using credentials loaded from environment variables.

### scheduler.py

Runs the monitoring workflow on a daily schedule and records failures without crashing the long-running scheduler process.

### logger.py

Writes persistent operational events to `logs/market_monitor.log` while suppressing noisy third-party HTTP logs.

### pipeline.py

Orchestrates collection, processing, deduplication, analysis, metrics, reporting and persistence.

## Reliability Decisions

- deterministic calculations remain in Python;
- LLM responses are validated with Pydantic;
- structured Ollama calls use `think=False` for stable JSON output;
- failed article analyses are not marked as seen;
- reports are persisted before successful article IDs are recorded;
- repeat runs skip previously analyzed article IDs;
- scheduler-level exceptions are logged with stack traces.

## Runtime Limitation

The current implementation depends on a locally available Ollama server and therefore requires the host machine to remain online for scheduled execution.
