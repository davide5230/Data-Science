# Architecture

## Overview

The service is designed as a small AI-assisted automation backend.

```text
Client
  ↓
POST /tickets
  ↓
Pydantic request validation
  ↓
Ticket analysis
  ├─ Local LLM (primary path)
  └─ Rule-based fallback
  ↓
Structured TicketAnalysis
  ↓
Deterministic Python routing
  ↓
TicketResponse
  ↓
SQLite persistence
```

## Responsibility Boundaries

### FastAPI

Provides HTTP endpoints, request handling, response models, and automatic OpenAPI/Swagger documentation.

### Pydantic

Validates both external API data and structured LLM output.

### LLM

Interprets unstructured ticket text and returns only:

- category;
- priority;
- summary.

The LLM does not control persistence, IDs, routing, or HTTP behavior.

### Deterministic Python Logic

Controls:

- ticket ID creation;
- category-to-team routing;
- application status;
- fallback behavior;
- persistence;
- API responses.

### SQLite

Provides lightweight local persistence so tickets remain available after application restarts.

## Reliability Strategy

The LLM is treated as a replaceable interpretation component rather than a single point of failure.

If Ollama is unavailable or structured output validation fails, the application falls back to deterministic keyword/rule analysis and records the origin in `analysis_source`.

## Why `main.py` Contains the Implementation

The current project is intentionally small and educational. Keeping the complete workflow in one executable module makes the end-to-end behavior easy to inspect.

In a larger production codebase, the same responsibilities would normally be separated approximately as follows:

```text
app/
├── main.py          # FastAPI application / route registration
├── models.py        # Pydantic schemas
├── database.py      # SQLite/database access
├── services.py      # LLM + fallback analysis
├── routing.py       # deterministic routing logic
└── config.py        # configuration
```

This refactor is not technically required for the current project; it becomes useful when the codebase grows, when multiple developers contribute, or when components need independent testing and reuse.
