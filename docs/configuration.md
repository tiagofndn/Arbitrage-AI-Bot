# Configuration

AI Arb Lab uses environment variables and optional config files. Never commit secrets.

## Environment Variables

Copy `.env.example` to `.env` and adjust:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | `development`, `test`, `staging` |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `LOG_FORMAT` | `json` | `json` or `console` |
| `DATA_DIR` | `./data/sample` | Path to data directory |
| `SYNTHETIC_SEED` | `42` | Random seed for reproducibility |
| `SYNTHETIC_VENUES` | `2` | Number of simulated venues |
| `SYNTHETIC_DAYS` | `1` | Days of synthetic data |
| `BACKTEST_INITIAL_CAPITAL` | `100000.0` | Starting capital for backtests |
| `BACKTEST_COMMISSION_RATE` | `0.001` | Commission rate (e.g., 0.1%) |
| `PAPER_INITIAL_CAPITAL` | `100000.0` | Starting capital for paper trading |
| `PAPER_MODE` | `simulated` | Always `simulated` in this repo |

## Logging

- **structlog** for structured logging
- **Correlation IDs**: Prefix `CORRELATION_ID_PREFIX` (e.g., `arb-`) for request tracing
- **Log levels**: Set `LOG_LEVEL` to control verbosity

## Secrets Handling

- Store API keys in `.env` (never commit)
- Use `python-dotenv` to load `.env` at startup
- For production-like setups, use a secrets manager (e.g., HashiCorp Vault) — not included in this repo

## Optional Services

When using Docker Compose (`docker compose --profile optional up -d`):

| Variable | Description |
|----------|-------------|
| `POSTGRES_HOST` | PostgreSQL host |
| `POSTGRES_PORT` | PostgreSQL port |
| `POSTGRES_DB` | Database name |
| `REDIS_HOST` | Redis host |
| `REDIS_PORT` | Redis port |

These are optional; the lab runs fully without them.

## OpenTelemetry (Stubs)

For observability, stubs exist for OpenTelemetry:

| Variable | Description |
|----------|-------------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP endpoint (if configured) |
| `OTEL_SERVICE_NAME` | Service name for traces |

Traces are not enabled by default.
