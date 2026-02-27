"""Kill switch: stop all new orders when triggered."""

from dataclasses import dataclass


@dataclass
class KillSwitch:
    """Manual or automatic kill switch to halt new orders."""

    enabled: bool = True
    _triggered: bool = False

    def trigger(self) -> None:
        """Manually trigger the kill switch."""
        self._triggered = True

    def reset(self) -> None:
        """Reset the kill switch."""
        self._triggered = False

    def is_triggered(self) -> bool:
        """Return True if kill switch is active."""
        return self.enabled and self._triggered

    def check(self) -> tuple[bool, str]:
        """Check if orders are allowed. Returns (allowed, reason)."""
        if not self.enabled:
            return True, "OK"
        if self._triggered:
            return False, "Kill switch triggered"
        return True, "OK"
