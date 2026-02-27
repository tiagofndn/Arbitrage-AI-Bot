# AI Arb Lab - Common Commands
# Use `make help` for usage

.PHONY: help install install-dev lint format typecheck test test-cov docs clean docker-up docker-down

help:
	@echo "AI Arb Lab - Available targets:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install with dev dependencies"
	@echo "  lint         - Run ruff linter"
	@echo "  format       - Run black + ruff format"
	@echo "  typecheck    - Run mypy"
	@echo "  test         - Run pytest"
	@echo "  test-cov     - Run pytest with coverage"
	@echo "  docs         - Serve mkdocs locally"
	@echo "  docs-build   - Build docs to site/"
	@echo "  clean        - Remove build artifacts"
	@echo "  docker-up    - Start optional services (Postgres, Redis)"
	@echo "  docker-down  - Stop optional services"
	@echo "  generate     - Generate synthetic sample data"
	@echo "  backtest     - Run example backtest"
	@echo "  paper-run    - Run paper trading simulation"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,docs]"

lint:
	ruff check src tests examples

format:
	black src tests examples
	ruff format src tests examples

typecheck:
	mypy src

test:
	pytest tests/

test-cov:
	pytest tests/ --cov=src/ai_arb_lab --cov-report=term-missing --cov-report=html

docs:
	mkdocs serve

docs-build:
	mkdocs build

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

docker-up:
	docker compose --profile optional up -d

docker-down:
	docker compose --profile optional down

generate:
	ai-arb-lab generate-data --output data/sample --days 1 --seed 42

backtest:
	ai-arb-lab backtest --data-dir data/sample --output reports/

paper-run:
	ai-arb-lab paper-run --data-dir data/sample --duration 60
