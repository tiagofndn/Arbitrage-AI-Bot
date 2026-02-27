"""Connector interfaces for market data. Mock implementations only.

Real exchange connectors must be implemented by users, with full
awareness of ToS, rate limits, and compliance. This module provides
interfaces and stubs for simulation only.
"""

from ai_arb_lab.connectors.base import MarketDataConnector
from ai_arb_lab.connectors.mock import MockMarketDataConnector

__all__ = [
    "MarketDataConnector",
    "MockMarketDataConnector",
]
