# NLP Propaganda Detection and Analysis

This repository contains an **NLP-based analysis pipeline** for detecting propaganda techniques in textual data.  
The project integrates **data preprocessing, feature extraction, topic modeling, and machine learning** to explore the structure and rhetorical strategies of texts.

## Project Workflow

The workflow includes the following main steps:

- **Metadata Extraction**: Scraping biographical metadata (e.g., author, birth/death dates, occasion) from Britannica.  
- **Data Preprocessing**: Text cleaning, tokenization, lemmatization, and stopword removal using **spaCy** and **NLTK**.  
- **Feature Engineering**:  
  - Readability metrics  
  - Keyword extraction (TF-IDF, TextRank, YAKE)  
  - Sentiment and emotion analysis  
  - Named entity recognition  
- **Topic Modeling**: Using **Latent Dirichlet Allocation (LDA)** to uncover latent semantic structures.  
- **Propaganda Detection**:  
  - Rule-based detection of propaganda techniques (emotional language, exaggeration, scapegoating, etc.)  
  - Narrative schemes classification (hero vs. enemy, utopia/dystopia, appeal to tradition…)  
- **Summarization**: Automatic abstractive summarization with Hugging Face transformers.

## Dataset
The project was developed for academic purposes on a **custom dataset of historical and political speeches**.  
Due to licensing restrictions, the dataset is not publicly included. To reproduce the pipeline, provide your own dataset in `.csv` format under a `data/` directory.

## Summary

This project provides a **comprehensive NLP workflow** that combines both **statistical methods** and **rule-based approaches** for analyzing propaganda.  

Key outcomes include:
- Extraction of linguistic and stylistic features of texts.  
- Identification of recurring propaganda techniques and narrative schemes.  
- Topic modeling for thematic structure discovery.  
- Sentiment and emotion profiling of speeches.  

While the rule-based classifiers provide interpretability, they could be enhanced with supervised models for higher accuracy.

## Getting Started

To get started with this project, follow these steps:

1. **Clone the repository:**
   
   ```bash
   git clone https://github.com/your-username/nlp_propaganda_analysis.git

2. **Navigate to the project directory:**

   cd nlp_propaganda_analysis

3. **Install required Python packages** (Python 3.9+ recommended):

   pip install -r requirements.txt

##Usage

1. Place your dataset in the data/ directory (CSV format).

2. Run the main analysis script step by step:

- Data preprocessing
- Feature extraction
- Topic modeling
- Propaganda and narrative detection
- Summarization
  
3. Results and processed outputs are saved under the results/ directory.

This project demonstrates skills in data preprocessing, natural language processing, and applied machine learning, with a focus on analyzing propaganda techniques and rhetorical structures in texts.
