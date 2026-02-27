# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Expand strategy docstrings for clarity

### Added
- Initial release: simulation-first arbitrage research lab
- Synthetic market data generator
- Simple spread arbitrage strategy
- Paper trading engine with fill simulation
- Cost model (fees, slippage, latency)
- Risk management (limits, kill switch, circuit breaker)
- AI assistive policy module (offline threshold suggestions)
- Explainability layer for AI decisions
- Backtesting and walk-forward validation
- HTML/Markdown report generation
- CLI: generate-data, backtest, paper-run, report
- Docker Compose for optional services (Postgres, Redis, Grafana, Prometheus)
- Full documentation (mkdocs-material)
- CI: lint, typecheck, tests, docs build

## [0.1.0] - 2025-02-27

### Added
- First public release
- Core event-driven architecture
- Data layer: trades, orderbooks, candles schema
- Feature store: rolling features, volatility, spreads, depth, imbalance
- Monte Carlo slippage/latency simulation
- OpenTelemetry stubs for observability
- Sample synthetic data for reproducible experiments
