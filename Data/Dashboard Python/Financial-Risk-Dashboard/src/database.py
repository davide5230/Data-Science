import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_PATH
)


def _get_database_url():
    required_variables = [
        "DB_NAME",
        "DB_HOST",
        "DB_PORT",
        "DB_USER"
    ]

    missing = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing:
        raise ValueError(
            "Missing database configuration: "
            + ", ".join(missing)
        )

    return URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD") or None,
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )


ENGINE = create_engine(
    _get_database_url(),
    pool_pre_ping=True
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

    with ENGINE.connect() as connection:
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

    with ENGINE.connect() as connection:
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

    with ENGINE.connect() as connection:
        return pd.read_sql(
            query,
            connection,
            params={
                "ticker": ticker
            }
        )
