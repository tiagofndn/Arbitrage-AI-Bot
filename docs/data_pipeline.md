# Data Pipeline

The data layer provides market data (trades, orderbooks, candles) from synthetic generation or file ingestion.

## Schema

### Trades

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | datetime | Trade time |
| `venue` | str | Venue identifier |
| `symbol` | str | Asset symbol |
| `price` | float | Trade price |
| `size` | float | Trade size |
| `side` | str | `buy` or `sell` |

### Orderbook

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | datetime | Snapshot time |
| `venue` | str | Venue identifier |
| `symbol` | str | Asset symbol |
| `bid_price` | float | Best bid |
| `ask_price` | float | Best ask |
| `bid_size` | float | Best bid size |
| `ask_size` | float | Best ask size |
| `depth` | int | Levels of depth (optional) |

### Candles (OHLCV)

| Column | Type | Description |
|--------|------|-------------|
| `timestamp` | datetime | Candle open time |
| `venue` | str | Venue identifier |
| `symbol` | str | Asset symbol |
| `open` | float | Open price |
| `high` | float | High price |
| `low` | float | Low price |
| `close` | float | Close price |
| `volume` | float | Volume |

## Ingest Pipeline

### Synthetic Generator

Generates multi-venue data with configurable:

- Number of venues
- Base price, volatility, drift
- Spread and depth
- Seed for reproducibility

```bash
ai-arb-lab generate-data --output data/sample --days 1 --venues 2 --seed 42
```

### CSV / Parquet Loader

Load from files:

- `trades_*.csv` — Trade data
- `orderbook_*.csv` — Orderbook snapshots
- `candles_*.parquet` — OHLCV candles

Column names must match the schema above.

## Feature Store

Rolling features are computed from raw data for strategy inputs:

| Feature | Description |
|---------|-------------|
| `spread` | Ask - Bid |
| `mid_price` | (Bid + Ask) / 2 |
| `imbalance` | (Bid size - Ask size) / (Bid size + Ask size) |
| `volatility` | Rolling std of returns |
| `depth` | Total size at best levels |

Used by strategies for signal generation.
