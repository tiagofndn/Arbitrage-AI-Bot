"""Mock market data connector for simulation. No real exchange connection."""

from typing import AsyncIterator

from ai_arb_lab.connectors.base import MarketDataConnector
from ai_arb_lab.core.events import Event


class MockMarketDataConnector(MarketDataConnector):
    """Mock connector that yields no events. For testing and simulation only."""

    def connect(self) -> None:
        """No-op. No real connection."""
        pass

    def disconnect(self) -> None:
        """No-op."""
        pass

    async def stream_events(self) -> AsyncIterator[Event]:
        """Yield no events. Override in tests to inject mock data."""
        if False:
            yield  # Makes this an async generator; never reached
