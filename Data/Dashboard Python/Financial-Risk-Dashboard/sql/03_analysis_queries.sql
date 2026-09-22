-- Daily returns

SELECT
    ticker,
    trade_date,
    adjusted_close,

    LAG(adjusted_close) OVER (
        PARTITION BY ticker
        ORDER BY trade_date
    ) AS previous_close,

    (
        adjusted_close
        /
        LAG(adjusted_close) OVER (
            PARTITION BY ticker
            ORDER BY trade_date
        )
        - 1
    ) AS daily_return

FROM market_prices

ORDER BY
    ticker,
    trade_date;
