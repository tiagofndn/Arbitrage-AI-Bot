# Troubleshooting

## Common Issues

### "No module named 'ai_arb_lab'"

Install the package in editable mode:

```bash
pip install -e .
```

### "No data found" when running backtest

Ensure you have generated sample data:

```bash
ai-arb-lab generate-data --output data/sample --days 1 --seed 42
```

Then run backtest with `--data-dir data/sample`.

### Tests fail with "FileNotFoundError"

Tests expect `data/sample` to exist. Run:

```bash
ai-arb-lab generate-data --output data/sample --days 1 --seed 42
```

Or add a pytest fixture that generates data on demand.

### Mypy errors

Ensure you're on Python 3.12+ and run:

```bash
make typecheck
```

Fix type annotations as suggested. For tests, `disallow_untyped_defs` is relaxed.

### Docker Compose fails

Ensure Docker is running. Use the `optional` profile:

```bash
docker compose --profile optional up -d
```

### Logs are too verbose

Set `LOG_LEVEL=WARNING` in `.env` to reduce output.

## Getting Help

- Open an [Issue](https://github.com/tiagofndn/Arbitrage-AI-Bot/issues)
- Check [CONTRIBUTING.md](https://github.com/tiagofndn/Arbitrage-AI-Bot/blob/main/CONTRIBUTING.md)
