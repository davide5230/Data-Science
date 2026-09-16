# AI Document Intelligence

A lightweight Retrieval-Augmented Generation (RAG) project that answers questions about documents using semantic search, grounded context and a local LLM.

The project intentionally implements the core RAG workflow without high-level orchestration frameworks so that each step remains transparent and easy to inspect.

---

## Project Overview

The system transforms a source document into semantically searchable chunks and uses those chunks to ground LLM answers.

The pipeline covers:

- text loading from `.txt` files;
- paragraph-aware chunking;
- local embeddings with Ollama;
- cosine-similarity retrieval;
- top-k semantic search;
- context augmentation;
- grounded answer generation with a local LLM;
- relevance thresholding for out-of-scope questions;
- structured validation with Pydantic;
- source metadata and similarity scores;
- JSON export of results.

---

## Objective

The goal is to build a transparent document-question-answering pipeline in which the model does not receive an entire document blindly.

Instead, the system:

1. splits the document into smaller semantic units;
2. converts each chunk into an embedding;
3. converts the user question into an embedding;
4. compares the question against document chunks using cosine similarity;
5. retrieves the most relevant chunks;
6. augments the LLM prompt with retrieved evidence;
7. generates a grounded answer;
8. returns a structured result with retrieval metadata.

---

## RAG Architecture

```text
Document
   ↓
Text Loading
   ↓
Paragraph-aware Chunking
   ↓
Chunk Embeddings
   ↓
Semantic Index

User Question
   ↓
Question Embedding
   ↓
R — Retrieval
   ↓
Cosine Similarity + Top-k
   ↓
Relevance Threshold
   ↓
A — Augmentation
   ↓
Retrieved Context + Question
   ↓
G — Generation
   ↓
Local LLM
   ↓
Pydantic Validation
   ↓
Structured Answer + Retrieved Sources
```

A more detailed explanation is available in `docs/architecture.md`.

---

## Retrieval

The question and every document chunk are represented as embedding vectors using:

```text
nomic-embed-text
```

Cosine similarity is used to rank chunks by semantic relevance.

The retriever returns the top-k chunks together with:

- source filename;
- chunk ID;
- similarity score;
- chunk text.

This allows semantic matches even when the wording of the question differs from the wording used in the document.

---

## Augmentation

Retrieved chunks are converted into an explicit document context and added to the user prompt.

The system prompt instructs the model to:

- use only the supplied context;
- avoid unsupported claims;
- avoid external knowledge;
- explicitly state when the document does not contain enough information.

---

## Generation

The generation layer uses a local Ollama model:

```text
qwen3.5:4b
```

The LLM is responsible only for grounded language generation.

Python remains responsible for:

- retrieval;
- similarity calculations;
- source metadata;
- relevance checks;
- structured result construction;
- output validation.

---

## Structured Output

The final result is validated with Pydantic and contains:

```json
{
  "question": "...",
  "answer": "...",
  "answerable": true,
  "retrieved_sources": [
    {
      "source": "sample.txt",
      "chunk_id": 0,
      "score": 0.0
    }
  ]
}
```

`retrieved_sources` refers to chunks supplied to the model, not a claim that every retrieved chunk was necessarily used in the generated answer.

---

## Out-of-Scope Handling

The system uses two complementary safeguards:

1. a minimum retrieval similarity threshold;
2. an LLM grounding instruction that returns a fixed insufficient-context response when retrieved evidence does not answer the question.

This prevents `answerable=True` from being based only on retrieval score when the model determines that the available context is insufficient.

The current similarity threshold is a project-level starting value and is not presented as a universal RAG threshold.

---

## Technology Stack

- Python
- NumPy
- Ollama
- `nomic-embed-text`
- `qwen3.5:4b`
- Pydantic
- Jupyter Notebook

---

## Project Structure

```text
AI-document-intelligence/
├── README.md
├── requirements.txt
├── .gitignore
├── notebooks/
│   └── 01_document_intelligence.ipynb
├── data/
│   ├── README.md
│   └── sample.txt
├── outputs/
│   └── sample_answer.json
└── docs/
    └── architecture.md
```

The notebook remains the main implementation because this version is designed to clearly demonstrate each RAG stage rather than hide the workflow behind a framework.

---

## Getting Started

### 1. Install Ollama

Install Ollama locally and pull the required models:

```bash
ollama pull nomic-embed-text
ollama pull qwen3.5:4b
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Add a document

Place a compatible text document in:

```text
data/
```

For the included example, use `sample.txt`.

### 4. Run the notebook

Open:

```text
notebooks/01_document_intelligence.ipynb
```

and execute the cells in sequence.

---

## Current Scope

The current version deliberately supports `.txt` ingestion only.

PDF, DOCX, vector databases, APIs and user interfaces are intentionally left as future extensions so that the core RAG mechanics remain visible and understandable.

---

## Limitations

- The initial similarity threshold requires empirical calibration for different corpora.
- Character/paragraph-based chunking is simpler than token-aware or semantic chunking.
- Retrieved sources identify candidate evidence supplied to the LLM, not guaranteed causal attribution for every generated sentence.
- The current implementation keeps embeddings in memory rather than using a persistent vector database.
- Answer quality depends on the embedding model, chunking strategy and local LLM.
- The current version is an educational portfolio implementation rather than a production document-intelligence service.

---

## Future Improvements

Possible extensions include:

- PDF and DOCX ingestion;
- token-aware or semantic chunking;
- persistent vector storage;
- retrieval evaluation datasets;
- threshold calibration;
- reranking;
- multiple-document collections;
- FastAPI endpoint;
- automated tests;
- document-level source citations;
- interactive interface.

---

## Purpose

This project demonstrates the core mechanics of Retrieval-Augmented Generation by implementing the workflow explicitly:

**Documents → Chunks → Embeddings → Retrieval → Augmentation → Generation → Structured Output**
