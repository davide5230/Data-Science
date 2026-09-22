import pandas as pd

from database import (
    fetch_daily_returns,
    fetch_price_drawdown_series
)


TRADING_DAYS = 252


def calculate_cumulative_return(
    ticker
):
    data = fetch_daily_returns(
        ticker
    ).copy()

    data = data.dropna(
        subset=["daily_return"]
    )

    data["cumulative_return"] = (
        1 + data["daily_return"]
    ).cumprod() - 1

    return data


def calculate_rolling_volatility(
    ticker,
    window=30
):
    data = fetch_daily_returns(
        ticker
    ).copy()

    data["rolling_volatility"] = (
        data["daily_return"]
        .rolling(window=window)
        .std()
        * (TRADING_DAYS ** 0.5)
    )

    return data


def compare_with_benchmark(
    ticker,
    benchmark="SPY"
):
    asset = fetch_daily_returns(
        ticker
    )[
        [
            "trade_date",
            "daily_return"
        ]
    ].copy()

    benchmark_data = fetch_daily_returns(
        benchmark
    )[
        [
            "trade_date",
            "daily_return"
        ]
    ].copy()

    asset = asset.rename(
        columns={
            "daily_return":
                "asset_return"
        }
    )

    benchmark_data = benchmark_data.rename(
        columns={
            "daily_return":
                "benchmark_return"
        }
    )

    data = asset.merge(
        benchmark_data,
        on="trade_date",
        how="inner"
    )

    data = data.dropna()

    data["asset_cumulative"] = (
        1 + data["asset_return"]
    ).cumprod() - 1

    data["benchmark_cumulative"] = (
        1 + data["benchmark_return"]
    ).cumprod() - 1

    return data


def calculate_correlation_matrix(
    tickers
):
    returns = []

    for ticker in tickers:
        data = fetch_daily_returns(
            ticker
        )[
            [
                "trade_date",
                "daily_return"
            ]
        ].copy()

        data = data.rename(
            columns={
                "daily_return": ticker
            }
        )

        data = data.set_index(
            "trade_date"
        )

        returns.append(
            data
        )

    combined = pd.concat(
        returns,
        axis=1,
        join="inner"
    )

    return combined.corr()


def get_drawdown_series(
    ticker
):
    return fetch_price_drawdown_series(
        ticker
    )
