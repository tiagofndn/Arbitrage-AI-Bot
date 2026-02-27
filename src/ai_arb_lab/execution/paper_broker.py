"""Paper broker: simulate order execution without real exchange connection."""

import uuid
import logging
from typing import Optional

from ai_arb_lab.core.events import OrderEvent, FillEvent
from ai_arb_lab.core.clock import SimClock
from ai_arb_lab.execution.fill_model import FillModel
from ai_arb_lab.strategies.base import Signal

logger = logging.getLogger(__name__)


class PaperBroker:
    """Simulate order execution. No real orders are sent."""

    def __init__(
        self,
        initial_capital: float = 100_000.0,
        fill_model: Optional[FillModel] = None,
    ) -> None:
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.fill_model = fill_model or FillModel()
        self._positions: dict[str, float] = {}
        self._order_id = 0

    def _next_order_id(self) -> str:
        self._order_id += 1
        return f"ord-{self._order_id}"

    def submit_order(
        self,
        signal: Signal,
        clock: SimClock,
    ) -> tuple[Optional[OrderEvent], Optional[FillEvent]]:
        """Submit buy order on venue_buy, then sell on venue_sell. Returns order and fill events."""
        order_id = self._next_order_id()

        # Buy leg
        buy_order = OrderEvent(
            order_id=order_id,
            symbol=signal.symbol,
            side="buy",
            venue=signal.venue_buy,
            price=signal.price_buy,
            size=signal.size,
            timestamp=clock.now(),
        )
        buy_fill = self.fill_model.simulate_fill(
            order_id=order_id,
            symbol=signal.symbol,
            side="buy",
            venue=signal.venue_buy,
            price=signal.price_buy,
            size=signal.size,
            clock=clock,
        )

        if buy_fill:
            self.capital -= buy_fill.price * buy_fill.size + buy_fill.fee
            logger.info("Paper fill: %s %s @ %s", buy_fill.side, buy_fill.size, buy_fill.price)

        # Sell leg (simplified: assume we can sell immediately)
        sell_order_id = self._next_order_id()
        sell_order = OrderEvent(
            order_id=sell_order_id,
            symbol=signal.symbol,
            side="sell",
            venue=signal.venue_sell,
            price=signal.price_sell,
            size=signal.size,
            timestamp=clock.now(),
        )
        sell_fill = self.fill_model.simulate_fill(
            order_id=sell_order_id,
            symbol=signal.symbol,
            side="sell",
            venue=signal.venue_sell,
            price=signal.price_sell,
            size=signal.size,
            clock=clock,
        )

        if sell_fill:
            self.capital += sell_fill.price * sell_fill.size - sell_fill.fee
            logger.info("Paper fill: %s %s @ %s", sell_fill.side, sell_fill.size, sell_fill.price)

        # Return first order and first fill for simplicity (caller can handle both legs)
        return buy_order, buy_fill
