CREATE TABLE IF NOT EXISTS market_prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    trade_date DATE NOT NULL,
    open_price NUMERIC(12, 4),
    high_price NUMERIC(12, 4),
    low_price NUMERIC(12, 4),
    close_price NUMERIC(12, 4),
    adjusted_close NUMERIC(12, 4),
    volume BIGINT,

    UNIQUE (ticker, trade_date)
);


CREATE INDEX IF NOT EXISTS idx_market_prices_ticker_date
ON market_prices (
    ticker,
    trade_date
);
