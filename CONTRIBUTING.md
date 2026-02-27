# Contributing to AI Arb Lab

Thank you for your interest in contributing! This project is educational and research-focused. We welcome contributions that align with our goals: simulation, backtesting, paper trading, and learning about market microstructure.

## Getting Started

1. **Fork** the repository and clone your fork.
2. **Create a branch**: `git checkout -b feature/your-feature-name` or `fix/your-fix`.
3. **Set up the environment**:
   ```bash
   make install-dev
   cp .env.example .env
   ```
4. **Run the test suite**: `make test` (must pass before submitting).

## Development Workflow

### Code Style

- **Formatting**: Black + Ruff. Run `make format` before committing.
- **Linting**: `make lint` must pass.
- **Type checking**: `make typecheck` (mypy) must pass.
- **Tests**: `make test` or `make test-cov` for coverage.

### Commit Messages

Use clear, descriptive messages. Prefer present tense:

- `Add Monte Carlo slippage simulation`
- `Fix fill model for partial fills`
- `Docs: clarify risk limits section`

### Pull Request Process

1. Ensure all checks pass locally (`make lint format typecheck test`).
2. Update documentation if you change behavior or add features.
3. Add tests for new functionality.
4. Fill out the PR template completely.
5. Request review from maintainers.

### What We Accept

- **Bug fixes** for simulation, backtesting, or paper trading logic
- **New strategies** (simulation-only, with tests)
- **Documentation** improvements
- **Tests** and test coverage improvements
- **Performance** optimizations that don't compromise correctness
- **AI/explainability** enhancements that remain assistive and transparent

### What We Don't Accept

- Code that enables or encourages live trading without explicit user opt-in
- Real exchange API implementations (we provide interfaces and mocks only)
- Guidance on evading rate limits or exchange rules
- Changes that reduce safety or compliance documentation

## Project Structure

```
src/ai_arb_lab/
├── core/       # Events, bus, clock
├── data/       # Loaders, synthetic generator
├── strategies/ # Strategy base and implementations
├── risk/       # Limits, kill switch
├── execution/  # Fill model, paper broker
├── ai/         # Policy, explainability
└── reporting/  # Metrics, report rendering
```

## Testing

- Place tests in `tests/` mirroring `src/ai_arb_lab/`.
- Use `pytest` and `pytest-asyncio` for async tests.
- Mock external dependencies; use synthetic data for integration tests.

## Documentation

- Docs live in `docs/` and use MkDocs Material.
- Run `make docs` to serve locally.
- Add new pages to `mkdocs.yml` nav.

## Questions?

Open a [Discussion](https://github.com/your-org/ai-arb-lab/discussions) or an [Issue](https://github.com/your-org/ai-arb-lab/issues) for questions.

For security concerns, see [SECURITY.md](SECURITY.md).
