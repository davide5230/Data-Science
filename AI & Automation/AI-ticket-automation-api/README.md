# AI Support Ticket Automation API

A FastAPI-based backend that automates customer-support ticket analysis, classification, prioritization, routing, and persistence.

The project combines deterministic application logic with a local LLM: the model interprets unstructured support requests, while Python validates the result, controls routing, persists tickets, and provides a rule-based fallback when the LLM is unavailable.

## Project Goal

Build a small but realistic AI-powered backend workflow:

```text
Incoming support ticket
        ↓
FastAPI / Pydantic validation
        ↓
Local LLM analysis
        ↓
Structured category + priority + summary
        ↓
Python routing logic
        ↓
SQLite persistence
        ↓
REST API response
```

If the local LLM is unavailable, the service falls back to deterministic rule-based classification so that the API remains operational.

## Key Features

- REST API built with FastAPI
- Request and response validation with Pydantic
- Local LLM classification with Ollama
- Structured AI output using a strict Pydantic schema
- Ticket categories: billing, technical, account, shipping, general
- Ticket priorities: low, medium, high, critical
- Deterministic team routing in Python
- Rule-based fallback when the LLM is unavailable
- SQLite persistence across application restarts
- Ticket retrieval through REST endpoints
- HTTP 404 handling for unknown ticket IDs
- Automatic interactive API documentation through Swagger UI

## Architecture

The system deliberately separates AI interpretation from deterministic application logic.

```text
POST /tickets
     ↓
TicketInput
     ↓
Pydantic validation
     ↓
┌───────────────────────┐
│ LLM available?        │
├───────────────────────┤
│ Yes → AI analysis     │
│ No  → rule fallback   │
└───────────────────────┘
     ↓
TicketAnalysis
     ↓
Python routing
     ↓
TicketResponse
     ↓
SQLite
```

The LLM is responsible only for:

- category interpretation;
- priority classification;
- concise ticket summarization.

Python remains responsible for:

- validation;
- ticket IDs;
- routing;
- status;
- fallback behavior;
- database persistence;
- API responses.

This follows the principle:

> **LLM interprets; Python controls application logic.**

## API Endpoints

### `GET /`

Health/status endpoint.

### `POST /tickets`

Creates, analyzes, routes, and stores a new ticket.

Example request:

```json
{
  "customer_id": "CUST-3001",
  "subject": "Order issue",
  "message": "My package arrived but the invoice contains a charge I do not recognize."
}
```

Example response:

```json
{
  "ticket_id": "TKT-18EBA976",
  "customer_id": "CUST-3001",
  "subject": "Order issue",
  "message": "My package arrived but the invoice contains a charge I do not recognize.",
  "category": "billing",
  "priority": "high",
  "summary": "The customer received their package but reports an unrecognized charge on the accompanying invoice.",
  "route_to": "billing_team",
  "analysis_source": "llm",
  "status": "routed"
}
```

### `GET /tickets`

Returns all persisted tickets.

### `GET /tickets/{ticket_id}`

Returns one ticket by ID.

An unknown ID returns HTTP `404 Not Found`.

## LLM Fallback

The application first attempts structured analysis with the local Ollama model.

If the LLM call fails, the service automatically uses deterministic rules for category and priority assignment and marks the response as:

```json
{
  "analysis_source": "rule_based_fallback"
}
```

When the LLM succeeds:

```json
{
  "analysis_source": "llm"
}
```

This provides basic fault tolerance instead of making the entire API dependent on model availability.

## Persistence

Tickets are stored locally in SQLite:

```text
data/tickets.db
```

The database file is excluded from Git so local runtime data is not committed.

Unlike an in-memory dictionary, SQLite keeps tickets available after the FastAPI/Uvicorn process is restarted.

## Project Structure

```text
AI-ticket-automation-api/
├── app/
│   └── main.py
├── data/
│   └── README.md
├── docs/
│   └── architecture.md
├── outputs/
│   └── sample_response.json
├── tests/
│   └── README.md
├── .gitignore
├── README.md
└── requirements.txt
```

For this learning-sized project, the executable implementation remains in `app/main.py` so the complete request-to-response workflow can be inspected in one place. A production-oriented version would normally separate API routes, schemas, database access, configuration, and AI services into dedicated modules.

## Setup

### 1. Create and activate an environment

```bash
conda create -n ticket-automation python=3.12
conda activate ticket-automation
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install the local Ollama model

```bash
ollama pull qwen3.5:4b
```

### 4. Start the API

From the project root:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Validation Scenarios

The completed implementation was tested for:

- successful LLM-powered ticket classification;
- semantically ambiguous ticket classification;
- operation with Ollama unavailable through rule-based fallback;
- SQLite persistence after application restart;
- retrieval of stored tickets;
- HTTP 404 responses for unknown ticket IDs.

## Tech Stack

**Python · FastAPI · Pydantic · Ollama · Qwen · SQLite · REST APIs · Uvicorn**

## Limitations and Future Improvements

This is a portfolio/learning backend rather than a production support platform. Possible future improvements include authentication, database migrations, async database access, automated tests, Docker deployment, observability, and integration with real ticketing systems.
