# Strategies

Strategies detect arbitrage opportunities and produce signals. All execution is simulated.

## Base Strategy

All strategies extend `BaseStrategy` and implement:

- `evaluate(market_data) -> Optional[Signal]` — Returns a signal or None
- `reset()` — Reset state for new backtest run

## Simple Spread Strategy

The built-in `SimpleSpreadStrategy` detects cross-venue price discrepancies:

1. Compare mid prices across venues
2. Compute spread after fees
3. If spread exceeds threshold, emit a signal
4. Cost model applies: fees, slippage, latency

### Parameters

| Parameter | Description |
|-----------|-------------|
| `min_spread_bps` | Minimum spread in basis points to trigger |
| `fee_rate` | Fee rate per venue (e.g., 0.001 = 0.1%) |
| `slippage_bps` | Slippage assumption in basis points |

### Cost Model

- **Fees**: Applied per leg (buy and sell)
- **Slippage**: Configurable; can use depth-aware model
- **Latency**: Simulated delay between legs
- **Partial fills**: Fill model may partially fill orders

## Adding a Custom Strategy

```python
from ai_arb_lab.strategies.base import BaseStrategy, Signal

class MyStrategy(BaseStrategy):
    def evaluate(self, market_data: dict) -> Signal | None:
        # Your logic here
        if opportunity:
            return Signal(...)
        return None
```

Register and use in backtest config.
