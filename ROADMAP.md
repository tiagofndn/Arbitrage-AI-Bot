# Roadmap

This document outlines the planned evolution of AI Arb Lab. All features remain focused on **simulation, research, and education**—never on enabling exploitative or non-compliant trading.

## Current Focus (v0.1.x)

- [x] Core event-driven architecture
- [x] Synthetic market data generator
- [x] Simple spread arbitrage strategy
- [x] Paper trading engine
- [x] Risk management (limits, kill switch)
- [x] AI assistive policy (offline threshold suggestions)
- [x] Backtesting and reporting
- [x] Full documentation

## Short Term (v0.2.x)

- [ ] Additional strategy templates (triangular, statistical)
- [ ] Walk-forward optimization framework
- [ ] Monte Carlo stress testing for slippage/latency
- [ ] Optional dashboard (Node/TS) for visualizing backtest results
- [ ] More feature store indicators (RSI, MACD, order flow)
- [ ] Config-driven strategy composition (YAML/TOML)

## Medium Term (v0.3.x)

- [ ] Connector interface with reference mock implementations
- [ ] Historical replay mode (replay CSV/parquet as event stream)
- [ ] OpenTelemetry integration (traces, metrics)
- [ ] Experiment tracking (MLflow or similar) for AI policy runs
- [ ] Multi-asset support in synthetic generator
- [ ] Regime detection (volatility regimes) for strategy adaptation

## Long Term (v0.4+)

- [ ] Plugin architecture for custom strategies and connectors
- [ ] Collaborative backtest sharing (export/import experiment configs)
- [ ] Academic paper reproducibility package
- [ ] Integration with open market data sources (with ToS compliance)

## Out of Scope

- Live trading execution
- Real exchange API implementations (beyond stubbed interfaces)
- Guidance on evading rate limits or exchange rules
- Support for leveraged or margin trading in production
