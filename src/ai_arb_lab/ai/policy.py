"""Assistive policy module: suggests thresholds from offline training on synthetic data.

This is NOT predictive. It proposes parameters (e.g., min spread) based on
historical synthetic data. Humans make final decisions. Deterministic fallback
when AI is disabled.
"""

from dataclasses import dataclass


@dataclass
class PolicySuggestion:
    """A suggested parameter from the policy module."""

    parameter: str
    value: float
    rationale: str
    confidence: float = 1.0  # 0-1, 1 = deterministic


class PolicyModule:
    """Offline policy that suggests strategy parameters. Assistive only."""

    def __init__(self, enabled: bool = True, default_min_spread_bps: float = 20.0) -> None:
        self.enabled = enabled
        self.default_min_spread_bps = default_min_spread_bps

    def suggest_min_spread(
        self,
        historical_spreads: list[float] | None = None,
    ) -> PolicySuggestion:
        """Suggest min_spread_bps. Uses historical data if provided and enabled."""
        if not self.enabled or not historical_spreads:
            return PolicySuggestion(
                parameter="min_spread_bps",
                value=self.default_min_spread_bps,
                rationale="Deterministic fallback: using default threshold",
                confidence=1.0,
            )

        # Simple heuristic: use 75th percentile of historical spreads as threshold
        sorted_spreads = sorted(historical_spreads)
        idx = int(len(sorted_spreads) * 0.75)
        suggested = (
            sorted_spreads[idx] if idx < len(sorted_spreads) else self.default_min_spread_bps
        )

        return PolicySuggestion(
            parameter="min_spread_bps",
            value=float(suggested),
            rationale=f"Based on 75th percentile of {len(historical_spreads)} historical spreads",
            confidence=0.8,
        )
