"""Report rendering: Markdown and HTML."""

from pathlib import Path
from typing import Any

from ai_arb_lab.reporting.metrics import BacktestMetrics


def render_markdown_report(metrics: BacktestMetrics, title: str = "Backtest Report") -> str:
    """Render metrics as Markdown."""
    lines = [
        f"# {title}",
        "",
        "## Summary",
        "",
        f"- **Initial Capital**: {metrics.initial_capital:,.2f}",
        f"- **Final Capital**: {metrics.final_capital:,.2f}",
        f"- **Total Return**: {metrics.total_return:,.2f} ({metrics.total_return_pct:.2%})",
        f"- **Trade Count**: {metrics.trade_count}",
        f"- **Win Count**: {metrics.win_count}",
        f"- **Max Drawdown**: {metrics.max_drawdown_pct:.2%}",
    ]
    if metrics.sharpe_ratio is not None:
        lines.append(f"- **Sharpe Ratio**: {metrics.sharpe_ratio:.2f}")
    lines.append("")
    return "\n".join(lines)


def save_report(content: str, path: Path | str) -> Path:
    """Save report to file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path
