# Sample Data

This directory contains minimal synthetic market data for quick testing.

## Files

- `trades.csv` — Sample trades (timestamp, venue, symbol, price, size, side)
- `orderbook.csv` — Sample orderbook snapshots (timestamp, venue, symbol, bid_price, ask_price, bid_size, ask_size)

## Generating More Data

For full backtests, generate more data:

```bash
ai-arb-lab generate-data --output data/sample --days 1 --seed 42
```

This adds `candles.parquet` and expands trades/orderbook.
