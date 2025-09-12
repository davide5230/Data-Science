# Wine Quality Linear Regression Analysis

This repository contains an analysis of the **Wine Quality Dataset** using **R**. The project covers the full data analysis workflow, including:

- **Data Cleaning**: Handling missing values, correcting data types, and preparing the dataset for analysis.  
- **Descriptive Analysis**: Summarizing key statistics and distributions of the variables.  
- **Exploratory Data Analysis (EDA)**: Visualizing relationships between features and wine quality.  
- **Linear Regression**: Building and evaluating linear regression models to predict wine quality.

## Summary

This report summarizes the analyses conducted on the dataset regarding the quality of two types of Portuguese wine: **red Vinho Verde** and **white Vinho Verde**. The dataset was initially subjected to descriptive analysis, followed by exploratory analysis to better understand the distribution and characteristics of the variables.

Subsequently, a **multiple linear regression** was performed to investigate the relationships between wine quality (response variable) and the other physicochemical variables. By applying data cleaning techniques and removing outliers, the model showed a significant improvement in fit. In particular, the **Multiple R-squared**, initially 0.2819, increased to 0.9006, indicating that the final model explains most of the variability in wine quality.  

**Note:** The regression results should be interpreted with caution due to the presence of heteroscedasticity.

## Getting Started

To get started with this project, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/wine_quality_lm_analysis.git
   
2. **Navigate to the project directory:
   cd wine_quality_lm_analysis

3. **Install required R packages (if not already installed):
   install.packages(c("tidyverse", "ggplot2", "fBasics","GGally","knitr","FactoMineR","factoextra","lmtest"))
