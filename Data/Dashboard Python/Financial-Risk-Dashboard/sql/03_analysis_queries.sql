-- Daily Returns

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

-- Drawdown Over Time

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

-- Maximum Drawdown by Ticker

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

    ROUND(
        (
            PERCENTILE_CONT(0.05)
            WITHIN GROUP (
                ORDER BY daily_return
            )
        )::numeric * 100,
        2
    ) AS var_95_pct,

    ROUND(
        (
            PERCENTILE_CONT(0.01)
            WITHIN GROUP (
                ORDER BY daily_return
            )
        )::numeric * 100,
        2
    ) AS var_99_pct

FROM daily_returns

WHERE daily_return IS NOT NULL

GROUP BY ticker

ORDER BY var_95_pct;

-- Risk analysis

CREATE OR REPLACE VIEW risk_metrics AS

WITH
daily_stats AS (
    SELECT
        ticker,

        AVG(daily_return) AS avg_daily_return,

        STDDEV_SAMP(daily_return)
            AS daily_volatility,

        STDDEV_SAMP(daily_return)
            * SQRT(252)
            AS annualized_volatility,

        PERCENTILE_CONT(0.05)
        WITHIN GROUP (
            ORDER BY daily_return
        ) AS var_95,

        PERCENTILE_CONT(0.01)
        WITHIN GROUP (
            ORDER BY daily_return
        ) AS var_99

    FROM daily_returns

    WHERE daily_return IS NOT NULL

    GROUP BY ticker
),

drawdowns AS (
    SELECT
        ticker,
        MIN(drawdown) AS max_drawdown

    FROM (
        SELECT
            ticker,
            trade_date,

            adjusted_close
            /
            MAX(adjusted_close) OVER (
                PARTITION BY ticker
                ORDER BY trade_date
                ROWS BETWEEN UNBOUNDED PRECEDING
                AND CURRENT ROW
            )
            - 1 AS drawdown

        FROM market_prices
    ) AS drawdown_series

    GROUP BY ticker
),

returns AS (
    SELECT DISTINCT
        ticker,

        FIRST_VALUE(adjusted_close) OVER (
            PARTITION BY ticker
            ORDER BY trade_date
        ) AS first_price,

        LAST_VALUE(adjusted_close) OVER (
            PARTITION BY ticker
            ORDER BY trade_date
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND UNBOUNDED FOLLOWING
        ) AS last_price

    FROM market_prices
)

SELECT
    d.ticker,

    (
        r.last_price
        /
        r.first_price
        - 1
    ) AS total_return,

    d.avg_daily_return
        * 252
        AS annualized_return,

    d.annualized_volatility,

    dd.max_drawdown,

    d.var_95,

    d.var_99,

    CASE
        WHEN d.annualized_volatility = 0
        THEN NULL

        ELSE
            (
                d.avg_daily_return * 252
            )
            /
            d.annualized_volatility
    END AS sharpe_ratio

FROM daily_stats d

JOIN drawdowns dd
    ON d.ticker = dd.ticker

JOIN returns r
    ON d.ticker = r.ticker;
