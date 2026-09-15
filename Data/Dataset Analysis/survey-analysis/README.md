# Survey Data Analysis and Clustering

This project analyzes a structured survey dataset using **Python**, combining exploratory data analysis, gap analysis, clustering and logistic regression to identify respondent profiles and behavioral patterns.

The objective is to transform raw survey responses into **interpretable segments and actionable insights**, following a complete data-analysis workflow from cleaning to statistical and predictive analysis.

---

## Project Overview

The analysis covers:

- **Data Cleaning**: handling missing values, inconsistent fields and data types.
- **Descriptive Analysis**: summarizing response distributions and key survey variables.
- **Exploratory Data Analysis (EDA)**: examining patterns and relationships across survey responses.
- **Gap Analysis**: comparing expectations and perceptions to identify areas requiring attention.
- **Clustering**: segmenting respondents into groups with similar behaviors and characteristics.
- **PCA**: supporting dimensionality reduction and cluster interpretation.
- **Logistic Regression**: modeling and evaluating membership in selected respondent groups.
- **Model Evaluation**: using classification metrics to assess predictive performance.

---

## Problem / Objective

Survey datasets often contain a mixture of categorical responses, multi-choice fields, missing values and behavioral indicators.

The goal of this project is to build an analytical workflow capable of:

1. cleaning and preparing survey data;
2. exploring response patterns;
3. identifying meaningful respondent segments;
4. characterizing those segments statistically;
5. evaluating whether group membership can be predicted from available features.

---

## Dataset

The dataset contains responses collected through a structured interview survey.

Each record represents one respondent and includes multiple survey fields covering usage, perceptions, behaviors and respondent characteristics.

The original dataset is **not included in this repository due to licensing and privacy restrictions**.

To reproduce the analysis, place a compatible CSV file inside:

```text
data/
```

and update the dataset path in the notebook if necessary.

---

## Methodology

### 1. Data Preparation

The raw survey data is inspected and cleaned before analysis.

The workflow includes:

- missing-value handling;
- data-type correction;
- removal or treatment of non-analytical metadata;
- preparation of survey variables for modeling.

### 2. Exploratory Data Analysis

Descriptive statistics and visual exploration are used to identify:

- response distributions;
- differences between respondent groups;
- behavioral patterns;
- potentially relevant variables.

### 3. Gap Analysis

Where applicable, expectation and perception measures are compared to highlight differences between what respondents expect and what they report experiencing.

### 4. Respondent Segmentation

**K-Means clustering** is used to identify groups of respondents with similar characteristics.

The workflow includes:

- feature scaling;
- cluster evaluation;
- silhouette analysis;
- PCA-based visualization and interpretation.

### 5. Predictive Analysis

Logistic regression is used to further characterize selected groups and evaluate whether cluster membership can be predicted from respondent features.

Classification metrics are used to assess model performance.

---

## Key Findings

The analysis demonstrates how survey responses can be transformed into structured respondent profiles rather than interpreted only through aggregate percentages.

The clustering stage highlights distinct behavioral patterns among respondents, while the regression analysis provides an additional way to understand which features are most associated with selected groups.

The project therefore combines **descriptive analytics, segmentation and predictive modeling** within a single survey-analysis workflow.

---

## Example Output

An example visualization generated during the analysis is available in:

```text
outputs/survey_plot.png
```

---

## Technology Stack

- **Python**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **Scikit-learn**
- **Statsmodels**
- **Jupyter Notebook**

Main analytical techniques:

- Exploratory Data Analysis
- Missing-value treatment
- Standardization
- K-Means Clustering
- Silhouette Analysis
- Principal Component Analysis
- Logistic Regression
- Classification Metrics

---

## Project Structure

```text
Survey-Analysis/
|
├── README.md
├── requirements.txt
├── .gitignore
|
├── notebooks/
│   └── 01_survey_analysis.ipynb
|
├── data/
│   └── README.md
|
└── outputs/
    └── survey_plot.png
```

The notebook remains the central analytical component of the project.  
A separate `src/` package is intentionally not used because the project is an exploratory and statistical analysis rather than a reusable application.

---

## Getting Started

### 1. Clone the portfolio repository

```bash
git clone https://github.com/davide5230/Data-Science.git
```

Navigate to:

```text
Data/Dataset Analysis/Survey Analysis/
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the dataset

Place the required CSV file inside:

```text
data/
```

The original dataset is not distributed with the project.

### 4. Run the analysis

Open:

```text
notebooks/01_survey_analysis.ipynb
```

and execute the notebook cells in sequence.

---

## Limitations

- The original survey dataset cannot be publicly distributed.
- Results depend on the structure and quality of the source survey.
- Cluster interpretation is exploratory and should not automatically be treated as causal.
- K-Means results depend on the selected variables, scaling procedure and chosen number of clusters.
- Predictive performance should be interpreted in the context of the available sample rather than generalized automatically to other populations.

---

## Future Improvements

Possible extensions include:

- automated preprocessing for new survey exports;
- reusable survey-variable mapping;
- additional cluster-validation techniques;
- comparison with alternative clustering algorithms;
- interactive segmentation dashboards;
- explainability analysis for predictive models;
- automated generation of survey insight reports.

---

## Purpose

This project demonstrates a complete survey-analysis workflow combining **data cleaning, exploratory analysis, segmentation and predictive modeling**.

It is designed as a portfolio project showing how raw survey responses can be transformed into structured analytical insights using Python.
