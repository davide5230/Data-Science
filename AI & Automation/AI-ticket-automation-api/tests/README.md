# Tests

The current project was manually validated through FastAPI's Swagger UI for the following scenarios:

- valid LLM-powered classification;
- ambiguous ticket classification;
- rule-based fallback with Ollama unavailable;
- SQLite persistence after application restart;
- retrieval of stored tickets;
- HTTP 404 for unknown ticket IDs.

A production-oriented extension could replace these manual checks with automated `pytest` and FastAPI `TestClient` tests.
