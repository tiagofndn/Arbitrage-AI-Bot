"""Tests for strategies."""

import pandas as pd

from ai_arb_lab.strategies.simple_spread import SimpleSpreadStrategy


def test_simple_spread_no_signal_when_single_venue() -> None:
    strategy = SimpleSpreadStrategy(min_spread_bps=10.0)
    ob = pd.DataFrame(
        {
            "venue": ["venue_0", "venue_0"],
            "bid_price": [50000, 50000],
            "ask_price": [50010, 50010],
        }
    )
    signal = strategy.evaluate({"orderbook": ob, "symbol": "BTC-USD"})
    assert signal is None


def test_simple_spread_detects_opportunity() -> None:
    strategy = SimpleSpreadStrategy(min_spread_bps=5.0, fee_rate=0, slippage_bps=0)
    # Venue 0: buy at 50000, Venue 1: sell at 50100 -> 100 bps spread
    ob = pd.DataFrame(
        {
            "venue": ["venue_0", "venue_1"],
            "bid_price": [50050, 50100],  # venue_1 has higher bid
            "ask_price": [50000, 50150],  # venue_0 has lower ask
        }
    )
    signal = strategy.evaluate({"orderbook": ob, "symbol": "BTC-USD"})
    assert signal is not None
    assert signal.venue_buy == "venue_0"
    assert signal.venue_sell == "venue_1"
    assert signal.expected_profit_bps >= 5.0


def test_simple_spread_rejects_small_spread() -> None:
    strategy = SimpleSpreadStrategy(min_spread_bps=200.0, fee_rate=0, slippage_bps=0)
    # Small spread: buy 50000, sell 50050 -> 50 bps, below 200 min
    ob = pd.DataFrame(
        {
            "venue": ["venue_0", "venue_1"],
            "bid_price": [50040, 50050],
            "ask_price": [50000, 50060],
        }
    )
    signal = strategy.evaluate({"orderbook": ob, "symbol": "BTC-USD"})
    assert signal is None or signal.expected_profit_bps < 200.0
