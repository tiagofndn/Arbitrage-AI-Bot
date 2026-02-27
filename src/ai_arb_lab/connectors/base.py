"""Base connector interface. Real implementations are out of scope."""

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

from ai_arb_lab.core.events import Event


class MarketDataConnector(ABC):
    """Interface for market data. Implementations must comply with exchange ToS and rate limits."""

    @abstractmethod
    async def stream_events(self) -> AsyncIterator[Event]:
        """Stream market data events. Not implemented for live exchanges in this repo."""
        ...

    @abstractmethod
    def connect(self) -> None:
        """Establish connection. Stub only."""
        ...

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection. Stub only."""
        ...
