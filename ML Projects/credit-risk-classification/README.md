# Credit Risk Classification Analysis

This project applies **machine learning classification** to a credit risk dataset in order to predict loan default risk.

The workflow combines data cleaning, exploratory analysis, class-imbalance handling, multiple classification algorithms and model evaluation to compare different approaches to credit-risk prediction.

---

## Project Overview

The project covers the full machine-learning workflow:

- **Data Cleaning & Preprocessing**: handling duplicates, missing values, outliers and categorical variables.
- **Exploratory Data Analysis (EDA)**: analyzing feature distributions, correlations and target imbalance.
- **Feature Preparation**: removing irrelevant variables and preparing model-ready inputs.
- **Class Imbalance Handling**: applying SMOTE to the training data.
- **Model Training**: Decision Tree, Random Forest, Logistic Regression and XGBoost.
- **Model Evaluation**: Accuracy, Precision, Recall, F1 Score and ROC AUC.
- **ROC Analysis**: comparing classifiers through ROC curves.
- **Feature Importance**: inspecting influential variables for supported models.

---

## Problem / Objective

Credit-risk assessment is a binary classification problem where the objective is to estimate whether a loan applicant is likely to default.

The project aims to:

1. prepare a raw financial dataset for machine learning;
2. investigate class imbalance and relevant predictor patterns;
3. compare multiple classification algorithms;
4. evaluate model performance using multiple metrics;
5. inspect which features contribute most to model predictions.

Because false negatives and false positives can have different business costs in credit-risk applications, evaluation should not rely on accuracy alone.

---

## Dataset

The project uses the **Credit Risk Dataset** available on Kaggle.

Source:

**Kaggle — Credit Risk Dataset**  
https://www.kaggle.com/datasets/laotse/credit-risk-dataset

The dataset contains information on loan applicants, including demographic, financial and credit-history features together with loan status.

To reproduce the analysis, download the dataset and place the source file inside:

```text
data/
```

The dataset itself is not redistributed in this portfolio package.

---

## Methodology

### 1. Data Cleaning

The initial dataset is inspected and prepared by:

- removing duplicates;
- handling missing values;
- reviewing and treating outliers;
- encoding categorical variables;
- removing irrelevant columns.

### 2. Exploratory Data Analysis

EDA is used to understand:

- feature distributions;
- correlations;
- class balance;
- relationships between applicant characteristics and loan status.

### 3. Class Imbalance Handling

SMOTE is applied to the **training data** to increase representation of the minority class.

This step is intended to reduce bias toward the majority class and improve the classifier's ability to identify higher-risk observations.

### 4. Model Training

The following classifiers are compared:

- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

### 5. Model Evaluation

Models are evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC
- ROC Curves

Using several metrics provides a more complete picture than accuracy alone, particularly when classes are imbalanced.

### 6. Model Interpretation

Feature-importance analysis is used where supported to inspect which variables contribute most strongly to model decisions.

---

## Key Findings

The project demonstrates how different classifiers behave on the same credit-risk classification problem and highlights the importance of evaluating imbalanced datasets with metrics beyond simple accuracy.

SMOTE allows the models to train on a more balanced representation of the target classes, while ROC AUC, precision, recall and F1 score provide additional information about classifier behavior.

The analysis also shows how feature-importance methods can support interpretation of selected models.

---

## Example Output

An example visualization from the analysis is available in:

```text
outputs/credit_risk_plot.png
```

---

## Technology Stack

- **Python**
- **Pandas**
- **Matplotlib**
- **Seaborn**
- **Scikit-learn**
- **XGBoost**
- **imbalanced-learn**
- **Jupyter Notebook**

Main machine-learning techniques:

- Data Preprocessing
- Exploratory Data Analysis
- Categorical Encoding
- SMOTE Oversampling
- Logistic Regression
- Decision Trees
- Random Forest
- XGBoost
- ROC / AUC Analysis
- Feature Importance

---

## Project Structure

```text
Credit-Risk-Classification/
|
├── README.md
├── requirements.txt
├── .gitignore
|
├── notebooks/
│   └── 01_credit_risk_classification.ipynb
|
├── data/
│   └── README.md
|
└── outputs/
    └── credit_risk_plot.png
```

The notebook remains the central analytical component of the project.

A separate `src/` package is intentionally not included because the current version is an experimental machine-learning analysis rather than a reusable production pipeline.

---

## Getting Started

### 1. Clone the portfolio repository

```bash
git clone https://github.com/davide5230/Data-Science.git
```

Navigate to:

```text
ML Projects/Credit Risk Classification Analysis/
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the dataset

Download the dataset from Kaggle and place the required CSV file inside:

```text
data/
```

Update the dataset path in the notebook if necessary.

### 4. Run the analysis

Open:

```text
notebooks/01_credit_risk_classification.ipynb
```

and execute the notebook cells in sequence.

---

## Limitations

- Model performance depends on the preprocessing and train/test split used in the notebook.
- SMOTE should be applied only to training data to avoid data leakage.
- Accuracy alone is not sufficient for evaluating an imbalanced credit-risk problem.
- Feature importance does not imply causality.
- Model outputs should not be interpreted as real-world lending decisions without additional validation, calibration and fairness analysis.
- The project is an educational portfolio analysis and is not intended for production credit scoring.

---

## Future Improvements

Possible extensions include:

- cross-validation;
- hyperparameter tuning;
- threshold optimization based on business costs;
- probability calibration;
- confusion-matrix cost analysis;
- SHAP-based model explainability;
- fairness and bias evaluation;
- model persistence and reusable inference pipeline;
- automated experiment tracking.

---

## Purpose

This project demonstrates a complete machine-learning classification workflow applied to a financial-risk problem.

The focus is on combining **data preparation, imbalanced classification, model comparison and interpretation** in a clear and reproducible analysis.
