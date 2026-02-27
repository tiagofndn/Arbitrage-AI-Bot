"""Data layer: loaders, synthetic generator, feature store."""

from ai_arb_lab.data.synthetic import SyntheticMarketGenerator
from ai_arb_lab.data.loader import load_trades_csv, load_orderbook_csv

__all__ = [
    "SyntheticMarketGenerator",
    "load_trades_csv",
    "load_orderbook_csv",
]
