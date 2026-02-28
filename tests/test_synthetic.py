"""Tests for synthetic market generator."""

from datetime import datetime

import pandas as pd

from ai_arb_lab.data.synthetic import SyntheticMarketGenerator


def test_synthetic_generator_creates_trades() -> None:
    gen = SyntheticMarketGenerator(seed=42, n_venues=2)
    start = datetime(2025, 1, 1)
    trades = gen.generate_trades(start, days=1)
    assert len(trades) > 0
    assert list(trades.columns) == ["timestamp", "venue", "symbol", "price", "size", "side"]
    assert trades["side"].isin(["buy", "sell"]).all()
    assert trades["venue"].nunique() == 2


def test_synthetic_generator_creates_orderbook() -> None:
    gen = SyntheticMarketGenerator(seed=42, n_venues=2)
    start = datetime(2025, 1, 1)
    ob = gen.generate_orderbook(start, days=1)
    assert len(ob) > 0
    assert "bid_price" in ob.columns
    assert "ask_price" in ob.columns
    assert (ob["ask_price"] >= ob["bid_price"]).all()


def test_synthetic_generator_reproducible() -> None:
    gen1 = SyntheticMarketGenerator(seed=42)
    gen2 = SyntheticMarketGenerator(seed=42)
    start = datetime(2025, 1, 1)
    t1 = gen1.generate_trades(start, days=1)
    t2 = gen2.generate_trades(start, days=1)
    pd.testing.assert_frame_equal(t1, t2)


def test_synthetic_generate_all(tmp_path: str) -> None:
    gen = SyntheticMarketGenerator(seed=42)
    paths = gen.generate_all(tmp_path, days=1)
    assert "trades" in paths
    assert "orderbook" in paths
    assert "candles" in paths
    assert paths["trades"].exists()
    assert paths["orderbook"].exists()
    assert paths["candles"].exists()
