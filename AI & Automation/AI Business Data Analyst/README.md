# AI Business Data Analyst

This project implements an **AI-assisted business analytics pipeline** built with Python, Pandas and a local Large Language Model.
The objective is to transform raw transactional data into **reliable business KPIs, anomaly detection, structured insights and management recommendations**, while keeping numerical calculations deterministic and using the LLM only for interpretation.
The project combines traditional data analysis with a local AI workflow using **Ollama and Qwen 3.5 4B**, with **Pydantic** used to validate structured model outputs.

---

## Project Overview

The pipeline covers the complete workflow:

- **Synthetic Business Data Generation**: Creation of realistic transactional sales data with product-specific prices, costs and quantities.
- **Controlled Anomaly Injection**: Introduction of realistic pricing and cost anomalies for testing.
- **Data Quality Checks**: Validation of missing values, duplicates and impossible numerical values.
- **Business KPI Analysis**: Revenue, profit, margin, units sold and average order value.
- **Product Analysis**: Revenue, profit, units and weighted margins by product.
- **Regional Analysis**: Revenue and profitability comparison across regions.
- **Monthly Trend Analysis**: Revenue and profit evolution with month-over-month growth.
- **Anomaly Detection**: Identification of loss-making transactions and weak-performing segments.
- **Rule-Based Insight Engine**: Deterministic business observations generated directly from calculated metrics.
- **LLM Business Analysis**: Local LLM interpretation of structured analytical data.
- **Structured AI Output**: Pydantic validation of executive summaries, findings, risks, opportunities and recommendations.

---

## Architecture

```text
Synthetic Business Data
        |
        v
Python / Pandas
        |
        +--> Data Quality Checks
        |
        +--> KPI Calculation
        |
        +--> Product / Region / Monthly Analysis
        |
        +--> Anomaly Detection
        |
        v
Structured Analytics JSON
        |
        +--> Rule-Based Insight Engine
        |
        v
Local LLM - Qwen 3.5 4B via Ollama
        |
        v
Pydantic Validation
        |
        v
Structured Business Report
```

A key design principle is that **Python performs numerical calculations and the LLM performs interpretation**.

---

## Dataset

The project uses a synthetic transactional dataset generated directly in Python.

Each row represents a simulated sale and contains date, product, region, units sold, unit price, unit cost, revenue, cost, profit and margin.

The dataset includes five product categories:

- Laptop
- Monitor
- Keyboard
- Mouse
- Headphones

and three geographical regions:

- North
- Center
- South

Prices, costs and quantities are generated according to product-specific business rules rather than independently random values.

Controlled anomalies are also injected into the data to simulate real analytical problems such as unusually low margins or increased supplier costs.

---

## Business Metrics

The analytical pipeline calculates:

- Total Revenue
- Total Profit
- Average Margin
- Total Units Sold
- Average Order Value
- Product Revenue and Profit
- Product Weighted Margin
- Regional Revenue and Profitability
- Monthly Revenue Growth
- Monthly Profit Growth
- Loss-Making Transactions
- Lowest-Margin Product
- Weakest Revenue Growth Month

---

## AI Layer

The aggregated analytics are converted into a structured JSON payload before being passed to the LLM.

The model does **not** receive the raw transactional dataset. Instead, Python first transforms the source data into reliable business information.

The local LLM generates:

- Executive Summary
- Key Findings
- Main Risks
- Opportunities
- Recommended Actions

The response is validated using Pydantic models to guarantee a consistent structure.

---

## Technology Stack

- **Python**
- **Pandas**
- **NumPy**
- **Pydantic**
- **Ollama**
- **Qwen 3.5 4B**
- **Jupyter Notebook**

The LLM runs locally through Ollama, allowing the AI layer to operate without external API costs.

---

## Project Structure

```text
AI-Business-Data-Analyst/
|
├── README.md
├── requirements.txt
├── .gitignore
├── pipeline.py
|
├── notebooks/
│   └── 01_business_analysis.ipynb
|
├── src/
│   ├── data_generator.py
│   ├── analytics.py
│   ├── insight_engine.py
│   ├── schemas.py
│   └── llm_report.py
|
├── outputs/
│   └── sample_business_report.json
|
└── docs/
    └── architecture.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/davide5230/Data-Science.git
```

Navigate to the project directory.

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama

Install Ollama locally and download the model used by the project:

```bash
ollama pull qwen3.5:4b
```

### 4. Run the analysis

Open:

```text
notebooks/01_business_analysis.ipynb
```

and execute the notebook cells in sequence.

Alternatively, after Ollama is running locally, execute the complete modular pipeline:

```bash
python pipeline.py
```

The validated AI report will be saved under:

```text
outputs/business_report.json
```

---

## Key Design Decisions

### Deterministic calculations first

Financial calculations are performed exclusively with Python rather than delegated to the LLM.

### Aggregated context instead of raw data

The LLM receives structured analytical summaries rather than the complete transactional table.

### Structured AI outputs

Pydantic schemas validate the LLM response before it is consumed by other parts of the application.

### Local AI model

The project uses a local model through Ollama, avoiding dependency on paid cloud APIs during development.

---

## Limitations

- The dataset is synthetic and does not represent a real company.
- Average Order Value assumes that each dataset row represents one order.
- The analysis covers one year, therefore monthly variations should not automatically be interpreted as recurring seasonality.
- The LLM provides interpretations and recommendations, not verified causal explanations.
- The current project is a prototype and does not include persistent storage or production deployment.

---

## Future Improvements

Possible future extensions include:

- Real CSV / Excel file ingestion
- Database integration
- Interactive dashboard
- Automated PDF reporting
- Email delivery
- Multiple LLM provider support
- Tool calling for deeper drill-down analysis
- Automated data-quality scoring
- Multi-year trend analysis
- Tests and CI/CD

---

## Purpose

This project demonstrates the integration of **Data Analysis, Business Analytics and Generative AI** in a practical workflow.

The focus is not simply on using an LLM, but on designing a system where deterministic analytics and AI interpretation complement each other to produce reliable, structured business insights.
