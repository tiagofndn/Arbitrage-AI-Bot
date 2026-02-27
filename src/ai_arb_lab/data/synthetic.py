"""Synthetic market data generator for reproducible experiments.

Generates multi-venue orderbooks, trades, and candles with configurable
volatility, spreads, and depth. No real exchange connection required.
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class SyntheticMarketGenerator:
    """Generate synthetic market data for backtesting and paper trading."""

    def __init__(
        self,
        seed: int = 42,
        base_price: float = 50000.0,
        volatility: float = 0.02,
        spread_bps: float = 10.0,
        n_venues: int = 2,
    ) -> None:
        self.seed = seed
        self.base_price = base_price
        self.volatility = volatility
        self.spread_bps = spread_bps / 10000.0  # Convert to decimal
        self.n_venues = n_venues
        self._rng = np.random.default_rng(seed)

    def generate_trades(
        self,
        start: datetime,
        days: int = 1,
        symbol: str = "BTC-USD",
        trades_per_minute: int = 5,
    ) -> pd.DataFrame:
        """Generate synthetic trade data for all venues."""
        n_trades = days * 24 * 60 * trades_per_minute
        timestamps = [
            start + timedelta(minutes=i / trades_per_minute)
            for i in range(n_trades)
        ]
        prices = self._random_walk(n_trades)
        sizes = self._rng.lognormal(0, 1, n_trades).clip(0.001, 10.0)
        sides = self._rng.choice(["buy", "sell"], n_trades)
        venues = [f"venue_{i % self.n_venues}" for i in range(n_trades)]

        return pd.DataFrame({
            "timestamp": timestamps,
            "venue": venues,
            "symbol": symbol,
            "price": prices,
            "size": sizes,
            "side": sides,
        })

    def generate_orderbook(
        self,
        start: datetime,
        days: int = 1,
        symbol: str = "BTC-USD",
        snapshots_per_minute: int = 1,
    ) -> pd.DataFrame:
        """Generate synthetic orderbook snapshots."""
        n_snapshots = days * 24 * 60 * snapshots_per_minute
        timestamps = [
            start + timedelta(minutes=i / snapshots_per_minute)
            for i in range(n_snapshots)
        ]
        prices = self._random_walk(n_snapshots)
        spread = prices * self.spread_bps
        bid_prices = prices - spread / 2
        ask_prices = prices + spread / 2
        bid_sizes = self._rng.uniform(1, 100, n_snapshots)
        ask_sizes = self._rng.uniform(1, 100, n_snapshots)
        venues = [f"venue_{i % self.n_venues}" for i in range(n_snapshots)]

        return pd.DataFrame({
            "timestamp": timestamps,
            "venue": venues,
            "symbol": symbol,
            "bid_price": bid_prices,
            "ask_price": ask_prices,
            "bid_size": bid_sizes,
            "ask_size": ask_sizes,
        })

    def generate_candles(
        self,
        start: datetime,
        days: int = 1,
        symbol: str = "BTC-USD",
        interval_minutes: int = 15,
    ) -> pd.DataFrame:
        """Generate OHLCV candles."""
        n_candles = (days * 24 * 60) // interval_minutes
        timestamps = [
            start + timedelta(minutes=i * interval_minutes)
            for i in range(n_candles)
        ]
        prices = self._random_walk(n_candles)
        high = prices * (1 + self._rng.uniform(0, self.volatility, n_candles))
        low = prices * (1 - self._rng.uniform(0, self.volatility, n_candles))
        volume = self._rng.lognormal(5, 2, n_candles)
        venues = [f"venue_{i % self.n_venues}" for i in range(n_candles)]

        return pd.DataFrame({
            "timestamp": timestamps,
            "venue": venues,
            "symbol": symbol,
            "open": prices,
            "high": high,
            "low": low,
            "close": prices,
            "volume": volume,
        })

    def _random_walk(self, n: int) -> np.ndarray:
        """Generate price series with random walk."""
        returns = self._rng.normal(0, self.volatility, n)
        prices = self.base_price * np.cumprod(1 + returns)
        return prices

    def generate_all(
        self,
        output_dir: Path | str,
        start: Optional[datetime] = None,
        days: int = 1,
        symbol: str = "BTC-USD",
    ) -> dict[str, Path]:
        """Generate all data types and write to output directory."""
        from datetime import datetime as dt

        start = start or dt.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        trades = self.generate_trades(start, days, symbol)
        orderbook = self.generate_orderbook(start, days, symbol)
        candles = self.generate_candles(start, days, symbol)

        trades_path = out / "trades.csv"
        orderbook_path = out / "orderbook.csv"
        candles_path = out / "candles.parquet"

        trades.to_csv(trades_path, index=False)
        orderbook.to_csv(orderbook_path, index=False)
        candles.to_parquet(candles_path, index=False)

        logger.info("Generated synthetic data: %s", out)
        return {
            "trades": trades_path,
            "orderbook": orderbook_path,
            "candles": candles_path,
        }
