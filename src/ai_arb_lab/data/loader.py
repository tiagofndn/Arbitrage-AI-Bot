"""Load market data from CSV and Parquet files."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def load_trades_csv(path: Path | str) -> pd.DataFrame:
    """Load trades from CSV. Expected columns: timestamp, venue, symbol, price, size, side."""
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def load_orderbook_csv(path: Path | str) -> pd.DataFrame:
    """Load orderbook snapshots from CSV."""
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def load_candles_parquet(path: Path | str) -> pd.DataFrame:
    """Load OHLCV candles from Parquet."""
    df = pd.read_parquet(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def load_data_dir(data_dir: Path | str) -> dict[str, pd.DataFrame]:
    """Load all available data from a directory."""
    data_dir = Path(data_dir)
    result: dict[str, pd.DataFrame] = {}

    trades_path = data_dir / "trades.csv"
    if trades_path.exists():
        result["trades"] = load_trades_csv(trades_path)

    orderbook_path = data_dir / "orderbook.csv"
    if orderbook_path.exists():
        result["orderbook"] = load_orderbook_csv(orderbook_path)

    candles_path = data_dir / "candles.parquet"
    if candles_path.exists():
        result["candles"] = load_candles_parquet(candles_path)

    return result
