"""Simple spread arbitrage strategy.

Detects cross-venue price discrepancies when spread (after fees/slippage)
exceeds a threshold. Used for simulation and education.
"""

from typing import Any, Optional

import pandas as pd

from ai_arb_lab.strategies.base import BaseStrategy, Signal


class SimpleSpreadStrategy(BaseStrategy):
    """Detect arbitrage when cross-venue spread exceeds min_spread_bps."""

    strategy_id: str = "simple_spread"

    def __init__(
        self,
        min_spread_bps: float = 20.0,
        fee_rate: float = 0.001,
        slippage_bps: float = 5.0,
    ) -> None:
        self.min_spread_bps = min_spread_bps
        self.fee_rate = fee_rate
        self.slippage_bps = slippage_bps / 10000.0

    def evaluate(self, market_data: dict[str, Any]) -> Optional[Signal]:
        """Check for cross-venue arbitrage opportunity.

        Compares best bid/ask across venues and emits signal if net spread
        (after fees and slippage) exceeds min_spread_bps.
        """
        orderbook = market_data.get("orderbook")
        if orderbook is None or not isinstance(orderbook, pd.DataFrame):
            return None
        if len(orderbook) < 2:
            return None

        # Group by venue, take best bid/ask per venue
        venues = orderbook["venue"].unique()
        if len(venues) < 2:
            return None

        best_bids = orderbook.groupby("venue")["bid_price"].max()
        best_asks = orderbook.groupby("venue")["ask_price"].min()

        # Find venue with lowest ask (buy there) and highest bid (sell there)
        venue_buy = best_asks.idxmin()
        venue_sell = best_bids.idxmax()
        if venue_buy == venue_sell:
            return None

        price_buy = float(best_asks[venue_buy])
        price_sell = float(best_bids[venue_sell])
        spread_bps = (price_sell - price_buy) / price_buy * 10000
        cost_bps = 2 * self.fee_rate * 10000 + 2 * self.slippage_bps * 10000
        net_spread_bps = spread_bps - cost_bps

        if net_spread_bps >= self.min_spread_bps:
            size = 0.01  # Small size for simulation
            return Signal(
                symbol=market_data.get("symbol", "BTC-USD"),
                side="buy",
                venue_buy=venue_buy,
                venue_sell=venue_sell,
                price_buy=price_buy,
                price_sell=price_sell,
                size=size,
                expected_profit_bps=net_spread_bps,
                rationale=f"Spread {spread_bps:.1f} bps > min {self.min_spread_bps} bps, net {net_spread_bps:.1f} bps after costs",
            )
        return None
