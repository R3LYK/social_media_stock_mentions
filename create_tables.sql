CREATE table IF NOT EXISTS ticker_match (
    stock_id INTEGER,
    dt TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    message TEXT NOT NULL,
    source TEXT NOT NULL,
    username TEXT NOT NULL,
    url TEXT NOT NULL,
    PRIMARY KEY (stock_id, dt),
    CONSTRAINT fk_match_stock FOREIGN KEY (stock_id) REFERENCES stock (id)
);

CREATE INDEX ON ticker_match (stock_id, dt DESC);

--for timestampdb
SELECT create_hypertable('ticker_match', 'dt');