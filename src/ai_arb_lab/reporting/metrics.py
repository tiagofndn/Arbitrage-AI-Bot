"""Backtest metrics computation."""

from dataclasses import dataclass


@dataclass
class BacktestMetrics:
    """Metrics from a backtest run."""

    initial_capital: float
    final_capital: float
    total_return: float
    total_return_pct: float
    trade_count: int
    win_count: int
    max_drawdown_pct: float
    sharpe_ratio: float | None = None

    def to_dict(self) -> dict[str, float | int | None]:
        """Export as dict for JSON serialization."""
        return {
            "initial_capital": self.initial_capital,
            "final_capital": self.final_capital,
            "total_return": self.total_return,
            "total_return_pct": self.total_return_pct,
            "trade_count": self.trade_count,
            "win_count": self.win_count,
            "max_drawdown_pct": self.max_drawdown_pct,
            "sharpe_ratio": self.sharpe_ratio,
        }

    @classmethod
    def from_results(
        cls,
        initial_capital: float,
        final_capital: float,
        trade_count: int,
        win_count: int,
        returns: list[float] | None = None,
    ) -> "BacktestMetrics":
        """Compute metrics from backtest results."""
        total_return = final_capital - initial_capital
        total_return_pct = total_return / initial_capital if initial_capital else 0

        # Simplified max drawdown (would need equity curve for accurate)
        max_dd = abs(min(0, total_return_pct))

        sharpe = None
        if returns and len(returns) > 1:
            import numpy as np

            arr = np.array(returns)
            if arr.std() > 0:
                sharpe = float(arr.mean() / arr.std() * (252**0.5))  # Annualized

        return cls(
            initial_capital=initial_capital,
            final_capital=final_capital,
            total_return=total_return,
            total_return_pct=total_return_pct,
            trade_count=trade_count,
            win_count=win_count,
            max_drawdown_pct=max_dd,
            sharpe_ratio=sharpe,
        )
