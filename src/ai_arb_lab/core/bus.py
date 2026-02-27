"""In-memory async event bus.

Routes events between publishers and subscribers. Used for
data -> strategy -> risk -> execution flow. No external
message queue required for core functionality.
"""

import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

from ai_arb_lab.core.events import Event

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Event)


class EventBus:
    """In-memory async event bus with type-based routing."""

    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[Callable[[Event], Awaitable[None]]]] = {}
        self._lock = asyncio.Lock()

    def subscribe(
        self,
        event_type: type[T],
        handler: Callable[[T], Awaitable[None]],
    ) -> None:
        """Register a handler for an event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        # Cast needed for contravariance; runtime type is correct
        self._handlers[event_type].append(handler)  # type: ignore[arg-type]

    async def publish(self, event: Event) -> None:
        """Publish an event to all subscribers of its type."""
        event_type = type(event)
        if event_type not in self._handlers:
            return
        for handler in self._handlers[event_type]:
            try:
                await handler(event)
            except Exception as e:
                logger.exception("Handler failed for %s: %s", event_type.__name__, e)

    async def publish_many(self, events: list[Event]) -> None:
        """Publish multiple events in order."""
        for event in events:
            await self.publish(event)
