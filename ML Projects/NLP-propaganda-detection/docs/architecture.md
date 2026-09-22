# Architecture

## Overview

The project is organized as a notebook-driven NLP pipeline that applies multiple analytical stages to the same text corpus.

```text
Input Dataset
     |
     v
Metadata Enrichment
     |
     v
Text Cleaning and Preprocessing
     |
     +-----------------------------+
     |                             |
     v                             v
KeyBERT / Sentiment / NER      LDA Topic Modeling
     |                             |
     +-------------+---------------+
                   |
                   v
      Propaganda & Narrative Rules
                   |
                   v
          LSA Summarization
                   |
                   v
             Output Analysis
```

## Design Rationale

The pipeline deliberately combines several NLP paradigms:

- **statistical methods** for feature extraction and LSA summarization;
- **rule-based methods** for interpretability;
- **topic models** for unsupervised thematic exploration;
- **transformer models** for emotion classification and contextual keyword embeddings.

The current implementation remains notebook-driven because the project originated as an exploratory academic analysis.

A future production-oriented version could separate preprocessing, feature extraction, classification and summarization into reusable modules under a `src/` package.
