/**
 * Stock Data Tables
 */
CREATE TABLE IF NOT EXISTS stocks (
    symbol VARCHAR(16),
    timestamp BIGINT,
    high float,
    volume BIGINT,
    open float,
    close float,
    low float,
    adjclose float,
    
    PRIMARY KEY (symbol, timestamp)
);

CREATE TABLE IF NOT EXISTS s_and_p (
    timestamp BIGINT,
    high float,
    volume BIGINT,
    open float,
    close float,
    low float,
    adjclose float,
    
    PRIMARY KEY (timestamp)
);

/**
 * Caching this to optimize performance.
 *   > SELECT DISTINCT symbol FROM stocks;
 * takes a while to run.
 */
CREATE TABLE IF NOT EXISTS symbols (
    symbol VARCHAR(16)
);

CREATE TABLE IF NOT EXISTS stock_metadata (
    symbol VARCHAR(16),
    name VARCHAR(128),
    sector VARCHAR(64),
    industry VARCHAR(64),
    description VARCHAR(4096),

    PRIMARY KEY (symbol)
);


/**
 * NLP Tables
 */

CREATE TABLE IF NOT EXISTS words(
    symbol VARCHAR(16),
    word VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS periodly_ratios(
    symbol VARCHAR(16),
    period INTEGER,
    ratio double precision,

    PRIMARY KEY (symbol, period)
);

CREATE TABLE IF NOT EXISTS word_scores(
    word VARCHAR(32),
    period INTEGER,
    total INTEGER,
    win_percent double precision,
    mean_ratio double precision,
    median_ratio double precision,

    PRIMARY KEY (word, period)
);
