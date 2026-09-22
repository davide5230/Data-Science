# Architecture

## Overview

The Financial Risk Dashboard separates data ingestion, relational analytics, Python analytics and presentation into independent layers.

```text
Yahoo Finance
     |
     v
src/data_loader.py
     |
     v
PostgreSQL
     |
     +----------------------------+
     |                            |
     v                            v
market_prices              SQL analytical views
                             ├── daily_returns
                             ├── risk_metrics
                             └── price_drawdown_series
                                      |
                                      v
                              src/database.py
                                      |
                                      v
                              src/analytics.py
                                      |
                                      v
                             app/callbacks.py
                                      |
                                      v
                              Plotly / Dash
```

## Components

### src/data_loader.py

Downloads five years of daily market data with `yfinance`, normalizes the returned DataFrame and loads rows into PostgreSQL.

The `UNIQUE (ticker, trade_date)` constraint and `ON CONFLICT DO NOTHING` make ingestion idempotent.

### sql/01_create_tables.sql

Creates the `market_prices` table and an index on `(ticker, trade_date)`.

### sql/02_data_quality.sql

Contains reproducible checks for:

- row counts and date coverage;
- missing fields;
- duplicate ticker/date combinations;
- invalid prices;
- inconsistent OHLC relationships.

### sql/03_analysis_queries.sql

Defines the analytical SQL layer.

#### daily_returns

Uses `LAG()` partitioned by ticker to calculate previous adjusted close and daily return.

#### risk_metrics

Combines CTEs, window functions and aggregate functions to calculate:

- total return;
- annualized return;
- annualized volatility;
- maximum drawdown;
- historical VaR 95%;
- historical VaR 99%;
- Sharpe ratio.

The current Sharpe ratio assumes a risk-free rate of 0.

#### price_drawdown_series

Calculates the running peak and drawdown series used by the dashboard.

### src/database.py

Creates a SQLAlchemy engine from environment configuration and exposes parameterized queries for the analytical views.

Using SQLAlchemy keeps Pandas database access on a supported connection layer.

### src/analytics.py

Calculates analytics that are convenient to perform after retrieval:

- cumulative return;
- 30-day rolling annualized volatility;
- asset versus SPY cumulative-return comparison;
- multi-asset daily-return correlation matrix.

### app/layout.py

Defines the dashboard structure, ticker selector, KPI cards and chart containers.

### app/callbacks.py

Connects ticker selection to PostgreSQL-backed metrics and Plotly visualizations.

### app/app.py

Creates and runs the Dash application.

## Data Flow

A normal refresh cycle is:

1. market data is ingested into PostgreSQL;
2. SQL views compute deterministic risk metrics;
3. SQLAlchemy retrieves the relevant data;
4. Python calculates rolling and cross-asset analytics;
5. Dash callbacks update the dashboard.

## Reliability and Security

- credentials are loaded from a local `.env` file;
- `.env` is excluded from Git;
- SQL queries use bind parameters for ticker filters;
- database connection URLs are constructed with SQLAlchemy's `URL.create`;
- `pool_pre_ping=True` validates pooled connections before reuse;
- no PostgreSQL data files or local database dumps are committed.

## Scope

The application is intended for analytics demonstration and portfolio use. It is not designed for order execution, portfolio optimization or financial advice.
