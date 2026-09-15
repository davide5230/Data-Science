# Architecture

The project separates deterministic analytics from generative AI interpretation.

```text
Data Generation
      |
      v
Economic Metrics
      |
      v
Business Aggregations
      |
      +--> Product Performance
      +--> Regional Performance
      +--> Monthly Performance
      |
      v
Anomaly Detection
      |
      v
Structured Analytics Payload
      |
      +-------------------------+
      |                         |
      v                         v
Rule-Based Insights         Local LLM
                                |
                                v
                         Pydantic Validation
                                |
                                v
                       Structured Business Report
```

## Design Principle

Python is responsible for financial calculations, aggregation, anomaly detection and deterministic business rules.

The LLM is responsible for summarization, interpretation, risk identification, opportunity identification and recommendation generation.

This separation reduces the risk of hallucinated numerical analysis.
