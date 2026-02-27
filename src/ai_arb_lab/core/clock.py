"""Simulation clock for reproducible, time-controlled execution.

Supports replay mode (replay historical timestamps) and speed-up
for faster backtesting. All components use this clock for consistency.
"""

from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Field


class SimClock(BaseModel):
    """Simulation clock with configurable speed and start time."""

    current_time: datetime = Field(default_factory=datetime.utcnow)
    speed_multiplier: float = 1.0  # 1.0 = real-time, 10.0 = 10x faster
    initial_time: Optional[datetime] = None

    def start(self, start_time: Optional[datetime] = None) -> None:
        """Start the clock. Optionally set initial time for replay."""
        self.initial_time = start_time or datetime.utcnow()
        self.current_time = self.initial_time

    def advance(self, delta: timedelta) -> datetime:
        """Advance clock by delta (scaled by speed_multiplier)."""
        scaled = timedelta(
            seconds=delta.total_seconds() * self.speed_multiplier
        )
        self.current_time = self.current_time + scaled
        return self.current_time

    def advance_seconds(self, seconds: float) -> datetime:
        """Advance clock by N seconds (scaled)."""
        return self.advance(timedelta(seconds=seconds))

    def now(self) -> datetime:
        """Return current simulation time."""
        return self.current_time
