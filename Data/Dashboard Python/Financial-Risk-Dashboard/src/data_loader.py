import os
import pandas as pd
import psycopg
import yfinance as yf
from dotenv import load_dotenv
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_PATH
)

TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "SPY"
]


def get_connection():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def download_market_data(
    ticker,
    period="5y"
):
    data = yf.download(
        ticker,
        period=period,
        auto_adjust=False,
        progress=False
    )

    if data.empty:
        raise ValueError(
            f"No data downloaded for {ticker}"
        )

    data = data.reset_index()

    return data


def prepare_market_data(
    data,
    ticker
):
    prepared = data.copy()

    # yfinance can return MultiIndex columns.
    if isinstance(
        prepared.columns,
        pd.MultiIndex
    ):
        prepared.columns = [
            column[0]
            for column in prepared.columns
        ]

    prepared = prepared.rename(
        columns={
            "Date": "trade_date",
            "Open": "open_price",
            "High": "high_price",
            "Low": "low_price",
            "Close": "close_price",
            "Adj Close": "adjusted_close",
            "Volume": "volume"
        }
    )

    prepared["ticker"] = ticker

    columns = [
        "ticker",
        "trade_date",
        "open_price",
        "high_price",
        "low_price",
        "close_price",
        "adjusted_close",
        "volume"
    ]

    return prepared[columns]


def insert_market_data(
    connection,
    data
):
    query = """
        INSERT INTO market_prices (
            ticker,
            trade_date,
            open_price,
            high_price,
            low_price,
            close_price,
            adjusted_close,
            volume
        )
        VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        ON CONFLICT (
            ticker,
            trade_date
        )
        DO NOTHING
    """

    records = [
        (
            row.ticker,
            row.trade_date,
            row.open_price,
            row.high_price,
            row.low_price,
            row.close_price,
            row.adjusted_close,
            int(row.volume)
        )
        for row in data.itertuples(
            index=False
        )
    ]

    with connection.cursor() as cursor:
        cursor.executemany(
            query,
            records
        )


def load_all_tickers():
    with get_connection() as connection:

        for ticker in TICKERS:
            print(
                f"Downloading {ticker}..."
            )

            raw_data = download_market_data(
                ticker
            )

            prepared_data = prepare_market_data(
                raw_data,
                ticker
            )

            insert_market_data(
                connection,
                prepared_data
            )

            print(
                f"{ticker}: "
                f"{len(prepared_data)} rows processed."
            )


if __name__ == "__main__":
    load_all_tickers()
