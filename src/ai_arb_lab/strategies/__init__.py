"""Strategy layer: arbitrage detection, cost model."""

from ai_arb_lab.strategies.base import BaseStrategy, Signal
from ai_arb_lab.strategies.simple_spread import SimpleSpreadStrategy

__all__ = [
    "BaseStrategy",
    "Signal",
    "SimpleSpreadStrategy",
]
