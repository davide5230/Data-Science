import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_PATH
)


def get_connection():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def fetch_risk_metrics():
    query = """
        SELECT
            ticker,
            total_return,
            annualized_return,
            annualized_volatility,
            max_drawdown,
            var_95,
            var_99,
            sharpe_ratio
        FROM risk_metrics
        ORDER BY ticker;
    """

    with get_connection() as connection:
        return pd.read_sql(
            query,
            connection
        )


def fetch_price_drawdown_series(
    ticker
):
    query = """
        SELECT
            ticker,
            trade_date,
            adjusted_close,
            drawdown
        FROM price_drawdown_series
        WHERE ticker = %s
        ORDER BY trade_date;
    """

    with get_connection() as connection:
        return pd.read_sql(
            query,
            connection,
            params=(ticker,)
        )


def fetch_daily_returns(
    ticker
):
    query = """
        SELECT
            ticker,
            trade_date,
            adjusted_close,
            previous_close,
            daily_return
        FROM daily_returns
        WHERE ticker = %s
        ORDER BY trade_date;
    """

    with get_connection() as connection:
        return pd.read_sql(
            query,
            connection,
            params=(ticker,)
        )
