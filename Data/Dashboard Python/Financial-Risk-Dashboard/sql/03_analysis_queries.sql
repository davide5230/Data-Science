-- Daily returns

CREATE OR REPLACE VIEW daily_returns AS

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

FROM market_prices;

-- Volatility

SELECT
    ticker,
    AVG(daily_return) AS avg_daily_return,
    STDDEV_SAMP(daily_return) AS daily_volatility,
    STDDEV_SAMP(daily_return) * SQRT(252)
        AS annualized_volatility
FROM daily_returns
WHERE daily_return IS NOT NULL
GROUP BY ticker
ORDER BY annualized_volatility DESC;
