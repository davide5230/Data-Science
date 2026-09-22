import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_PATH
)


def get_engine():
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if db_password:
        database_url = (
            f"postgresql+psycopg://"
            f"{db_user}:{db_password}"
            f"@{db_host}:{db_port}/{db_name}"
        )
    else:
        database_url = (
            f"postgresql+psycopg://"
            f"{db_user}"
            f"@{db_host}:{db_port}/{db_name}"
        )

    return create_engine(
        database_url
    )


def fetch_risk_metrics():
    query = text("""
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
    """)

    with get_engine().connect() as connection:
        return pd.read_sql(
            query,
            connection
        )


def fetch_price_drawdown_series(
    ticker
):
    query = text("""
        SELECT
            ticker,
            trade_date,
            adjusted_close,
            drawdown
        FROM price_drawdown_series
        WHERE ticker = :ticker
        ORDER BY trade_date;
    """)

    with get_engine().connect() as connection:
        return pd.read_sql(
            query,
            connection,
            params={
                "ticker": ticker
            }
        )


def fetch_daily_returns(
    ticker
):
    query = text("""
        SELECT
            ticker,
            trade_date,
            adjusted_close,
            previous_close,
            daily_return
        FROM daily_returns
        WHERE ticker = :ticker
        ORDER BY trade_date;
    """)

    with get_engine().connect() as connection:
        return pd.read_sql(
            query,
            connection,
            params={
                "ticker": ticker
            }
        )
