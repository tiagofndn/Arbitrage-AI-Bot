# Evaluation

Backtesting and evaluation produce metrics and reports for research and learning.

## Backtesting

1. Load historical or synthetic data
2. Replay events through the event bus
3. Strategy emits signals; risk gates them
4. Paper broker simulates fills
5. Compute metrics

```bash
ai-arb-lab backtest --data-dir data/sample --output reports/
```

## Metrics

| Metric | Description |
|--------|-------------|
| **Total return** | (Final - Initial) / Initial |
| **Sharpe ratio** | Risk-adjusted return |
| **Max drawdown** | Largest peak-to-trough decline |
| **Win rate** | % of profitable trades |
| **Profit factor** | Gross profit / Gross loss |
| **Trade count** | Number of executed trades |

## Walk-Forward Validation

- Split data into train/test windows
- Train (e.g., threshold tuning) on train window
- Test on out-of-sample test window
- Reduces overfitting

## Monte Carlo

- Run backtest with randomized slippage/latency
- Many runs to assess robustness
- Output: distribution of returns, confidence intervals

## Reports

- **HTML**: Interactive report with charts (placeholder)
- **Markdown**: Summary tables and metrics
- Stored in `reports/` directory
