"""Event definitions for the event-driven architecture.

All domain events are typed dataclasses. The event bus routes these
between data, strategy, risk, and execution layers.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Event(BaseModel):
    """Base event with timestamp and optional correlation ID."""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: str | None = None

    class Config:
        extra = "forbid"


class TradeEvent(Event):
    """A trade occurred on a venue."""

    venue: str
    symbol: str
    price: float
    size: float
    side: str  # "buy" | "sell"


class OrderbookEvent(Event):
    """Orderbook snapshot from a venue."""

    venue: str
    symbol: str
    bid_price: float
    ask_price: float
    bid_size: float
    ask_size: float
    depth: dict[str, Any] | None = None  # Optional full depth


class SignalEvent(Event):
    """Strategy emitted a trading signal (e.g., arbitrage opportunity)."""

    strategy_id: str
    symbol: str
    side: str  # "buy" | "sell"
    venue_buy: str
    venue_sell: str
    price_buy: float
    price_sell: float
    size: float
    expected_profit_bps: float
    rationale: str = ""


class OrderEvent(Event):
    """Order submitted to the paper broker."""

    order_id: str
    symbol: str
    side: str
    venue: str
    price: float
    size: float
    signal_id: str | None = None


class FillEvent(Event):
    """Order was (partially) filled."""

    order_id: str
    fill_id: str
    symbol: str
    side: str
    venue: str
    price: float
    size: float
    fee: float = 0.0
