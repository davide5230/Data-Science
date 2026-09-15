# NLP Propaganda Detection and Analysis

This project implements a multi-stage **Natural Language Processing (NLP) pipeline** for analyzing historical and political speeches, with a focus on propaganda techniques, rhetorical patterns and narrative structures.

The workflow combines text preprocessing, metadata enrichment, keyword extraction, sentiment analysis, named entity recognition, topic modeling, rule-based propaganda detection and transformer-based summarization.

---

## Project Overview

The project integrates several NLP techniques within a single analytical workflow:

- **Metadata Extraction**: enriching documents with biographical or contextual information from external sources.
- **Text Preprocessing**: cleaning, tokenization, lemmatization and stopword removal.
- **Keyword Extraction**: TF-IDF, TextRank and YAKE.
- **Readability Analysis**: measuring linguistic complexity and stylistic characteristics.
- **Sentiment and Emotion Analysis**: profiling the emotional tone of speeches.
- **Named Entity Recognition (NER)**: extracting people, places and organizations.
- **Topic Modeling**: discovering latent themes with Latent Dirichlet Allocation (LDA).
- **Propaganda Detection**: identifying selected rhetorical and propaganda patterns using interpretable rules.
- **Narrative Analysis**: identifying recurring narrative structures such as hero/enemy framing or utopian/dystopian themes.
- **Automatic Summarization**: generating abstractive summaries using Hugging Face transformer models.

---

## Problem / Objective

Political and historical speeches often contain multiple layers of meaning that are difficult to analyze using only basic word frequencies.

The objective of this project is to build an NLP workflow capable of:

1. cleaning and normalizing textual data;
2. extracting relevant linguistic and semantic features;
3. identifying recurring topics and entities;
4. detecting interpretable rhetorical and propaganda patterns;
5. generating compact summaries of long documents;
6. combining statistical, rule-based and transformer-based NLP methods in a single pipeline.

The project is primarily analytical and exploratory. It does not claim to provide a production-grade propaganda classifier.

---

## Dataset

The project was developed for academic purposes using a custom dataset of **historical and political speeches**.

The original dataset is not included due to licensing restrictions.

To reproduce the workflow, place a compatible CSV or spreadsheet file inside:

```text
data/
```

and update the dataset path in the notebook when necessary.

---

## NLP Pipeline

### 1. Metadata Enrichment

The workflow enriches texts with contextual metadata where available, such as:

- author information;
- birth and death dates;
- occasion or historical context.

External information is retrieved from public web sources.

### 2. Text Preprocessing

The text-processing stage includes:

- normalization;
- tokenization;
- stopword removal;
- lemmatization;
- removal of irrelevant symbols and formatting artifacts.

Tools include **NLTK** and **spaCy**.

### 3. Linguistic Feature Extraction

The pipeline extracts several types of features:

- readability indicators;
- TF-IDF keywords;
- TextRank keywords;
- YAKE keywords;
- sentiment information;
- named entities.

Using multiple keyword-extraction techniques allows comparison between statistical and graph-based approaches.

### 4. Topic Modeling

Latent Dirichlet Allocation (LDA) is used to identify recurring semantic themes across the document collection.

The workflow uses tools such as:

- Gensim
- pyLDAvis

to support topic interpretation and visualization.

### 5. Propaganda and Narrative Detection

A rule-based layer identifies selected rhetorical strategies, including patterns associated with:

- emotionally loaded language;
- exaggeration;
- scapegoating;
- hero/enemy narratives;
- appeals to tradition;
- utopian or dystopian framing.

The rule-based approach prioritizes interpretability over predictive accuracy.

### 6. Transformer-Based Summarization

Hugging Face transformer models are used to generate abstractive summaries of longer texts.

This provides a compact semantic representation that complements the statistical NLP analysis.

---

## Key Findings

The project demonstrates how multiple NLP approaches can be combined to analyze the same textual corpus from different perspectives.

The pipeline can surface:

- recurring thematic structures;
- relevant keywords;
- frequently mentioned entities;
- emotional and stylistic patterns;
- interpretable rhetorical markers;
- narrative structures;
- concise automatic summaries.

The rule-based propaganda layer is transparent and easy to inspect, but its results depend heavily on the manually defined linguistic rules.

---

## Technology Stack

- **Python**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **NLTK**
- **spaCy**
- **Transformers**
- **PyTorch**
- **TextBlob**
- **YAKE**
- **Gensim**
- **pyLDAvis**
- **Jupyter Notebook**

Main NLP techniques:

- Tokenization
- Lemmatization
- Stopword Removal
- TF-IDF
- TextRank
- YAKE
- Sentiment Analysis
- Named Entity Recognition
- Topic Modeling
- Rule-Based Classification
- Transformer Summarization

---

## Project Architecture

```text
Raw Text / Metadata
        |
        v
Text Cleaning & Normalization
        |
        v
Linguistic Feature Extraction
        |
        +-----------------------------+
        |                             |
        v                             v
Keywords / Sentiment / NER       Topic Modeling
        |                             |
        +-------------+---------------+
                      |
                      v
          Propaganda & Narrative Rules
                      |
                      v
             Transformer Summaries
                      |
                      v
             Analytical Outputs
```

A more detailed description is available in:

```text
docs/architecture.md
```

---

## Project Structure

```text
NLP-Propaganda-Detection/
|
├── README.md
├── requirements.txt
├── .gitignore
|
├── notebooks/
│   └── 01_nlp_propaganda_analysis.ipynb
|
├── data/
│   └── README.md
|
├── outputs/
│   └── README.md
|
└── docs/
    └── architecture.md
```

The notebook remains the central implementation of the current project.

A dedicated `src/` package is not introduced in this version because the existing implementation is notebook-driven and the goal is to preserve the actual project structure rather than artificially refactor it into a software package.

---

## Getting Started

### 1. Clone the portfolio repository

```bash
git clone https://github.com/davide5230/Data-Science.git
```

Navigate to:

```text
ML Projects/NLP Propaganda Detection and Analysis/
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install NLP resources

Depending on the notebook configuration, additional language resources may be required for NLTK and spaCy.

For example:

```bash
python -m spacy download en_core_web_sm
```

and download the NLTK resources used by the notebook when prompted.

### 4. Add the dataset

Place the source dataset inside:

```text
data/
```

The original academic dataset is not publicly distributed.

### 5. Run the analysis

Open:

```text
notebooks/01_nlp_propaganda_analysis.ipynb
```

and execute the notebook cells in sequence.

---

## Limitations

- The dataset is not publicly available, limiting exact reproducibility.
- Rule-based propaganda detection depends on manually defined linguistic patterns.
- Detected rhetorical patterns should not automatically be interpreted as proof of propaganda intent.
- Sentiment models can perform differently on historical or political language.
- Topic modeling depends on preprocessing choices and the selected number of topics.
- Named entity recognition may produce errors on historical names, unusual spellings or context-specific entities.
- Transformer summaries can omit details or generate imperfect abstractions.
- The current implementation is exploratory and is not a validated production propaganda-detection system.

---

## Future Improvements

Possible extensions include:

- supervised propaganda classification using labeled data;
- transformer-based sequence classification;
- sentence-level propaganda detection;
- evaluation against benchmark propaganda datasets;
- SHAP or attention-based explainability;
- stronger emotion-classification models;
- reusable preprocessing modules;
- automated experiment configuration;
- structured result export;
- interactive visualization dashboards;
- migration from notebook workflow to a modular NLP pipeline.

---

## Purpose

This project demonstrates a broad applied NLP workflow that combines **classical NLP, statistical analysis, rule-based reasoning and transformer models**.

Its main value is the integration of multiple techniques into a single interpretable analysis pipeline for historical and political text.
