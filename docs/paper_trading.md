# Paper Trading

Paper trading simulates execution without sending real orders. The paper broker and fill model provide realistic behavior.

## Paper Broker

- Accepts orders from the strategy (after risk approval)
- Simulates order submission and fill
- Emits fill events to the event bus
- Tracks positions and P&L

## Fill Model

The fill model determines:

- **Fill probability**: May partially fill or reject
- **Slippage**: Price movement from order to fill
- **Latency**: Delay between order and fill (simulated)

### Parameters

| Parameter | Description |
|-----------|-------------|
| `slippage_bps` | Basis points of slippage |
| `fill_probability` | Probability of full fill (0–1) |
| `latency_ms` | Simulated latency in milliseconds |

## Event Flow

```
Order → Paper Broker → Fill Model → Fill Event → Event Bus
```

## Running Paper Trading

```bash
ai-arb-lab paper-run --data-dir data/sample --duration 60
```

- Loads market data (or uses synthetic stream)
- Runs strategy in real-time (simulated clock)
- Logs fills and P&L
- No real orders are sent

## Scope

Paper trading is **simulation only**. There is no live trading mode in this repository.
