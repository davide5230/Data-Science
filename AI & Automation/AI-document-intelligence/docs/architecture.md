# Architecture

## Overview

AI Document Intelligence implements a transparent Retrieval-Augmented Generation pipeline without relying on a high-level RAG framework.

```text
Source Document
      ↓
Text Loading
      ↓
Paragraph-aware Chunking
      ↓
Chunk Embeddings (nomic-embed-text)
      ↓
In-memory semantic index

User Question
      ↓
Question Embedding
      ↓
Cosine Similarity
      ↓
Top-k Retrieval
      ↓
Relevance Threshold
      ↓
Context Augmentation
      ↓
qwen3.5:4b
      ↓
Pydantic Validation
      ↓
Structured Answer + Retrieved Sources
```

## Component Responsibilities

### Python

Python is responsible for deterministic operations:

- loading documents;
- chunk construction;
- embedding orchestration;
- cosine-similarity calculations;
- ranking and retrieval;
- relevance checks;
- source metadata;
- structured output construction;
- JSON serialization.

### Embedding Model

`nomic-embed-text` converts both document chunks and user questions into vector representations used for semantic retrieval.

### Local LLM

`qwen3.5:4b` receives only the retrieved document context together with the user question. It is instructed to avoid unsupported information and explicitly report insufficient context when necessary.

### Pydantic

Pydantic validates the final application-level response structure, including answerability and retrieved source metadata.

## Design Decisions

The first version deliberately avoids LangChain, persistent vector databases and a user interface. This keeps the mechanics of retrieval, augmentation and generation visible and makes the project easier to reason about.

The retrieval similarity threshold is treated as an initial project parameter rather than a universal confidence value. Future versions should calibrate it empirically against a representative evaluation set.
