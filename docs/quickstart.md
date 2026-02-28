# Quickstart

Get AI Arb Lab running in under 5 minutes.

## Prerequisites

- Python 3.12 or higher
- pip or uv

## Install

```bash
git clone https://github.com/tiagofndn/Arbitrage-AI-Bot.git
cd Arbitrage-AI-Bot
pip install -e ".[dev]"
cp .env.example .env
```

## Generate Sample Data

The synthetic generator creates multi-venue orderbooks with configurable spreads and volatility. No real data required.

```bash
ai-arb-lab generate-data --output data/sample --days 1 --seed 42
```

This produces:

- `data/sample/trades.csv` — Simulated trades
- `data/sample/orderbook.csv` — Orderbook snapshots
- `data/sample/candles.parquet` — OHLCV candles

## Run a Backtest

```bash
ai-arb-lab backtest --data-dir data/sample --output reports/
```

Output: JSON metrics and an HTML/Markdown report in `reports/`.

## Run Paper Trading (Simulation)

```bash
ai-arb-lab paper-run --data-dir data/sample --duration 60
```

Runs a 60-second simulated paper trading session. No real orders.

## Generate a Report

```bash
ai-arb-lab report --input reports/backtest_*.json --output reports/summary.md
```

## Next Steps

- [Architecture](architecture.md) — Understand the system design
- [Configuration](configuration.md) — Tune via environment and config
- [Strategies](strategies.md) — Implement or customize arbitrage logic
