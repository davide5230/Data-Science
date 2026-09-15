# Wine Quality Linear Regression Analysis

This project analyzes the **Wine Quality Dataset** using **R**, combining data cleaning, exploratory analysis and multiple linear regression to investigate the relationship between wine quality and physicochemical wine characteristics.

The objective is to build a clear statistical workflow that moves from raw observations to an interpretable predictive model while explicitly considering model diagnostics and limitations.

---

## Project Overview

The analysis covers:

- **Data Cleaning**: handling missing values, checking data types and preparing variables for analysis.
- **Descriptive Analysis**: summarizing the distribution and main characteristics of the dataset.
- **Exploratory Data Analysis (EDA)**: visualizing relationships between physicochemical variables and wine quality.
- **Outlier Analysis**: identifying influential observations and evaluating their effect on model fit.
- **Multiple Linear Regression**: estimating the relationship between wine quality and explanatory variables.
- **Model Diagnostics**: evaluating residual behavior, heteroscedasticity and overall model assumptions.

---

## Problem / Objective

Wine quality can be influenced by several measurable physicochemical characteristics.

The goal of this project is to evaluate whether those characteristics can explain variation in wine quality and to assess how well a multiple linear regression model performs after data preparation and diagnostic analysis.

The workflow focuses on:

1. understanding the structure and distribution of the dataset;
2. identifying relevant relationships between variables;
3. fitting a multiple linear regression model;
4. evaluating model quality and assumptions;
5. interpreting the final results with appropriate statistical caution.

---

## Dataset

The analysis uses the **Wine Quality Dataset**, containing physicochemical measurements and quality scores for Portuguese Vinho Verde wines.

Source:

**Kaggle — Wine Quality Dataset**  
https://www.kaggle.com/datasets/yasserh/wine-quality-dataset

To reproduce the analysis, download the dataset and place the source file inside:

```text
data/
```

The dataset itself is not redistributed in this portfolio package.

---

## Methodology

### 1. Data Preparation

The dataset is inspected and prepared before modeling.

The workflow includes:

- checking missing values;
- verifying variable types;
- reviewing distributions;
- identifying unusual or influential observations.

### 2. Exploratory Data Analysis

Exploratory analysis is used to understand:

- variable distributions;
- correlations between physicochemical features;
- relationships between predictors and wine quality;
- potential multicollinearity or anomalous patterns.

### 3. Multiple Linear Regression

A multiple linear regression model is fitted with wine quality as the response variable and physicochemical characteristics as explanatory variables.

The analysis compares model behavior before and after data-cleaning and outlier-management steps.

### 4. Model Diagnostics

The fitted model is evaluated through diagnostic analysis.

Particular attention is given to:

- goodness of fit;
- residual behavior;
- heteroscedasticity;
- influential observations;
- limitations of the linear-model assumptions.

---

## Results

The initial multiple linear regression achieved a **Multiple R-squared of 0.2819**.

After the data-cleaning and outlier-treatment steps used in the notebook, the reported model fit increased to a **Multiple R-squared of 0.9006**.

This indicates a substantially stronger fit on the processed sample.

However, this result must be interpreted carefully. The analysis identifies **heteroscedasticity**, meaning that one of the assumptions of ordinary least squares regression is not fully satisfied.

The large increase in R-squared after removing observations should also be treated cautiously because aggressive outlier removal can improve in-sample fit without necessarily improving generalization.

---

## Key Findings

- Physicochemical variables contain measurable information related to wine-quality scores.
- Data preparation and influential observations have a strong effect on model fit.
- The final model achieves a high in-sample R-squared after preprocessing.
- Regression diagnostics indicate heteroscedasticity, limiting the strength of statistical conclusions.
- Model fit alone is not sufficient to establish predictive reliability or causal relationships.

---

## Example Output

An example visualization produced during the exploratory analysis is available in:

```text
outputs/wine_plot.png
```

---

## Technology Stack

- **R**
- **Jupyter Notebook**
- **tidyverse**
- **ggplot2**
- **dplyr**
- **GGally**
- **FactoMineR**
- **factoextra**
- **lmtest**
- **knitr**

Main analytical techniques:

- Data Cleaning
- Exploratory Data Analysis
- Correlation Analysis
- Multiple Linear Regression
- Outlier Analysis
- Regression Diagnostics

---

## Project Structure

```text
Wine-Quality-Analysis/
|
├── README.md
├── requirements.R
├── .gitignore
|
├── notebooks/
│   └── 01_wine_quality_analysis.ipynb
|
├── data/
│   └── README.md
|
└── outputs/
    └── wine_plot.png
```

The notebook remains the central analytical component of the project.  
A separate `src/` package is intentionally not included because the project is a statistical analysis rather than a reusable software application.

---

## Getting Started

### 1. Clone the portfolio repository

```bash
git clone https://github.com/davide5230/Data-Science.git
```

Navigate to:

```text
Data/Dataset Analysis/Wine Quality LM Analysis R/
```

### 2. Install the required R packages

From R, run:

```r
source("requirements.R")
```

### 3. Add the dataset

Download the Wine Quality Dataset from Kaggle and place the required file inside:

```text
data/
```

Update the dataset path in the notebook if necessary.

### 4. Run the analysis

Open:

```text
notebooks/01_wine_quality_analysis.ipynb
```

and execute the notebook cells in sequence.

---

## Limitations

- The reported R-squared values describe in-sample model fit and should not automatically be interpreted as out-of-sample predictive performance.
- The final model shows evidence of heteroscedasticity.
- Outlier removal can materially affect regression results and should be justified analytically rather than used only to maximize model fit.
- Linear regression assumes relationships that may not fully capture the structure of wine-quality scores.
- The analysis does not establish causal relationships between physicochemical variables and wine quality.

---

## Future Improvements

Possible extensions include:

- train/test or cross-validation evaluation;
- robust standard errors for heteroscedasticity;
- robust regression methods;
- regularized regression such as Ridge or Lasso;
- comparison with nonlinear regression or machine-learning models;
- systematic influence analysis;
- reproducible dataset-download instructions;
- additional model-performance metrics beyond R-squared.

---

## Purpose

This project demonstrates a complete statistical-analysis workflow in **R**, combining exploratory data analysis, multiple linear regression and model diagnostics.

The focus is not only on obtaining a strong model fit, but also on understanding the assumptions and limitations that determine whether the results are statistically reliable.
