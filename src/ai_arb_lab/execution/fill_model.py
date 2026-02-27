"""Fill model: simulate realistic fills with slippage and partial fills."""

import uuid
from dataclasses import dataclass
from typing import Optional

from ai_arb_lab.core.events import FillEvent
from ai_arb_lab.core.clock import SimClock


@dataclass
class FillResult:
    """Result of a fill simulation."""

    filled: bool
    fill_id: str
    price: float
    size: float
    fee: float


class FillModel:
    """Simulate order fills with slippage, latency, and partial fills."""

    def __init__(
        self,
        slippage_bps: float = 5.0,
        fill_probability: float = 1.0,
        fee_rate: float = 0.001,
    ) -> None:
        self.slippage_bps = slippage_bps / 10000.0
        self.fill_probability = fill_probability
        self.fee_rate = fee_rate

    def simulate_fill(
        self,
        order_id: str,
        symbol: str,
        side: str,
        venue: str,
        price: float,
        size: float,
        clock: SimClock,
        fill_prob_override: Optional[float] = None,
    ) -> Optional[FillEvent]:
        """Simulate a fill. Returns FillEvent or None if not filled."""
        import random
        prob = fill_prob_override if fill_prob_override is not None else self.fill_probability
        if random.random() > prob:
            return None

        # Apply slippage: buy gets worse (higher), sell gets worse (lower)
        slippage = price * self.slippage_bps
        fill_price = price + slippage if side == "buy" else price - slippage
        fee = fill_price * size * self.fee_rate

        return FillEvent(
            order_id=order_id,
            fill_id=str(uuid.uuid4()),
            symbol=symbol,
            side=side,
            venue=venue,
            price=fill_price,
            size=size,
            fee=fee,
            timestamp=clock.now(),
        )
