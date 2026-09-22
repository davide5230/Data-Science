-- Total number of records
SELECT
    COUNT(*) AS total_rows
FROM market_prices;


-- Records by ticker and available date range
SELECT
    ticker,
    COUNT(*) AS observations,
    MIN(trade_date) AS first_date,
    MAX(trade_date) AS last_date
FROM market_prices
GROUP BY ticker
ORDER BY ticker;


-- Check for missing values
SELECT
    COUNT(*) FILTER (
        WHERE open_price IS NULL
    ) AS missing_open,

    COUNT(*) FILTER (
        WHERE high_price IS NULL
    ) AS missing_high,

    COUNT(*) FILTER (
        WHERE low_price IS NULL
    ) AS missing_low,

    COUNT(*) FILTER (
        WHERE close_price IS NULL
    ) AS missing_close,

    COUNT(*) FILTER (
        WHERE adjusted_close IS NULL
    ) AS missing_adjusted_close,

    COUNT(*) FILTER (
        WHERE volume IS NULL
    ) AS missing_volume

FROM market_prices;


-- Check duplicate ticker/date combinations
SELECT
    ticker,
    trade_date,
    COUNT(*) AS occurrences
FROM market_prices
GROUP BY
    ticker,
    trade_date
HAVING COUNT(*) > 1;


-- Detect invalid prices
SELECT *
FROM market_prices
WHERE
    open_price <= 0
    OR high_price <= 0
    OR low_price <= 0
    OR close_price <= 0
    OR adjusted_close <= 0;


-- Detect inconsistent OHLC values
SELECT *
FROM market_prices
WHERE
    high_price < low_price
    OR high_price < open_price
    OR high_price < close_price
    OR low_price > open_price
    OR low_price > close_price;
