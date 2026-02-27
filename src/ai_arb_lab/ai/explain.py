"""Explainability: produce human-readable rationale for AI suggestions."""

from ai_arb_lab.ai.policy import PolicySuggestion


def explain_suggestion(suggestion: PolicySuggestion) -> str:
    """Produce a human-readable explanation for a policy suggestion."""
    return (
        f"Parameter: {suggestion.parameter}\n"
        f"Suggested value: {suggestion.value}\n"
        f"Rationale: {suggestion.rationale}\n"
        f"Confidence: {suggestion.confidence:.0%}"
    )
