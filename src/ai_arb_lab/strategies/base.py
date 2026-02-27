"""Base strategy interface. All strategies extend this."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from pydantic import BaseModel, Field


class Signal(BaseModel):
    """Trading signal emitted by a strategy."""

    symbol: str
    side: str  # "buy" | "sell"
    venue_buy: str
    venue_sell: str
    price_buy: float
    price_sell: float
    size: float
    expected_profit_bps: float
    rationale: str = ""


class BaseStrategy(ABC):
    """Abstract base for all strategies. Evaluates market data and emits signals."""

    strategy_id: str = "base"

    @abstractmethod
    def evaluate(self, market_data: dict[str, Any]) -> Optional[Signal]:
        """Evaluate market data and return a signal if opportunity exists."""
        ...

    def reset(self) -> None:
        """Reset strategy state for new backtest run."""
        pass
