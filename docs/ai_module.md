# AI Module

The AI layer is **assistive**, not autonomous. It suggests thresholds and filters; humans make final decisions.

## Policy Module

- **Offline training**: Trained on synthetic data only
- **Output**: Suggested thresholds (e.g., min spread, max position)
- **Use case**: Propose parameters for strategies; user can accept, reject, or modify

## Explainability

Every AI suggestion includes a **human-readable rationale**:

- Which features influenced the suggestion
- Confidence or uncertainty (if available)
- Fallback to deterministic rules if AI is disabled

## Deterministic Fallback

When AI is disabled or fails:

- Use configurable default thresholds
- No "black box" behavior
- Fully reproducible

## Limitations

- **Not predictive**: Does not predict prices or returns
- **Not live**: Trained offline; no real-time adaptation
- **Not magic**: Suggestions may be wrong; always validate

## Reproducibility

- Fixed random seeds for training
- Config-driven experiments
- Export policy config with reports
