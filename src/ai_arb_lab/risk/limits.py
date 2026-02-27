"""Risk limits: max exposure, drawdown, daily loss.

All signals must pass these checks before simulated execution.
"""

from dataclasses import dataclass
from typing import Optional

from ai_arb_lab.strategies.base import Signal


@dataclass
class RiskLimits:
    """Enforce position and P&L limits."""

    max_exposure: float = 100_000.0
    max_drawdown_pct: float = 0.10
    max_daily_loss: float = 5_000.0
    initial_capital: float = 100_000.0

    def __post_init__(self) -> None:
        self._current_exposure: float = 0.0
        self._peak_capital: float = self.initial_capital
        self._daily_pnl: float = 0.0

    def check(self, signal: Signal, current_capital: float) -> tuple[bool, str]:
        """Check if signal passes risk limits. Returns (approved, reason)."""
        notional = signal.price_buy * signal.size + signal.price_sell * signal.size
        new_exposure = self._current_exposure + notional

        if new_exposure > self.max_exposure:
            return False, f"Exposure {new_exposure:.0f} exceeds max {self.max_exposure:.0f}"

        drawdown = (self._peak_capital - current_capital) / self._peak_capital
        if drawdown > self.max_drawdown_pct:
            return False, f"Drawdown {drawdown:.1%} exceeds max {self.max_drawdown_pct:.1%}"

        if self._daily_pnl < -self.max_daily_loss:
            return False, f"Daily loss {abs(self._daily_pnl):.0f} exceeds max {self.max_daily_loss:.0f}"

        return True, "OK"

    def update(self, exposure: float, capital: float, daily_pnl: float) -> None:
        """Update internal state after a fill or period end."""
        self._current_exposure = exposure
        self._peak_capital = max(self._peak_capital, capital)
        self._daily_pnl = daily_pnl
