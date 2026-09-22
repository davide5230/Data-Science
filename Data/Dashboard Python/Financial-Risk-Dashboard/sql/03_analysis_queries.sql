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

-- Drawdown over time

WITH running_peak AS (

    SELECT
        ticker,
        trade_date,
        adjusted_close,

        MAX(adjusted_close) OVER (
            PARTITION BY ticker
            ORDER BY trade_date
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS running_max

    FROM market_prices
)

SELECT
    ticker,
    trade_date,
    adjusted_close,
    running_max,

    (
        adjusted_close
        /
        running_max
        - 1
    ) AS drawdown

FROM running_peak

ORDER BY
    ticker,
    trade_date;

-- Maximum drawdown by ticker

WITH running_peak AS (

    SELECT
        ticker,
        trade_date,
        adjusted_close,

        MAX(adjusted_close) OVER (
            PARTITION BY ticker
            ORDER BY trade_date
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ) AS running_max

    FROM market_prices
),

drawdowns AS (

    SELECT
        ticker,
        trade_date,

        (
            adjusted_close
            /
            running_max
            - 1
        ) AS drawdown

    FROM running_peak
)

SELECT
    ticker,
    MIN(drawdown) AS max_drawdown

FROM drawdowns

GROUP BY ticker

ORDER BY max_drawdown;

-- Historical Value at Risk at 95%

SELECT
    ticker,

    PERCENTILE_CONT(0.05)
    WITHIN GROUP (
        ORDER BY daily_return
    ) AS var_95

FROM daily_returns

WHERE daily_return IS NOT NULL

GROUP BY ticker

ORDER BY var_95;
