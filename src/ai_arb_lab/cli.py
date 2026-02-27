"""CLI entry point using Typer."""

import json
import logging
from datetime import datetime
from pathlib import Path

import typer

from ai_arb_lab import __version__
from ai_arb_lab.config import (
    BACKTEST_INITIAL_CAPITAL,
    DATA_DIR,
    SYNTHETIC_DAYS,
    SYNTHETIC_SEED,
    SYNTHETIC_VENUES,
)
from ai_arb_lab.data.loader import load_data_dir
from ai_arb_lab.data.synthetic import SyntheticMarketGenerator
from ai_arb_lab.execution.fill_model import FillModel
from ai_arb_lab.execution.paper_broker import PaperBroker
from ai_arb_lab.logging_config import setup_logging
from ai_arb_lab.reporting.metrics import BacktestMetrics
from ai_arb_lab.reporting.render import render_markdown_report, save_report
from ai_arb_lab.risk.kill_switch import KillSwitch
from ai_arb_lab.risk.limits import RiskLimits
from ai_arb_lab.strategies.simple_spread import SimpleSpreadStrategy

app = typer.Typer(
    name="ai-arb-lab",
    help="AI-assisted arbitrage research lab (simulated execution, paper trading)",
)
logger = logging.getLogger(__name__)


def _run_backtest_engine(
    data_dir: Path,
    output_dir: Path,
    initial_capital: float,
) -> BacktestMetrics:
    """Run backtest on loaded data."""
    setup_logging()
    data = load_data_dir(data_dir)
    if "orderbook" not in data:
        raise typer.BadParameter("No orderbook data found. Run generate-data first.")

    orderbook = data["orderbook"]
    strategy = SimpleSpreadStrategy(min_spread_bps=15.0)
    risk_limits = RiskLimits(
        max_exposure=initial_capital * 0.5,
        initial_capital=initial_capital,
    )
    kill_switch = KillSwitch(enabled=True)
    broker = PaperBroker(initial_capital=initial_capital, fill_model=FillModel())

    trade_count = 0
    win_count = 0
    capital = initial_capital

    # Sample orderbook by time windows (e.g., per minute)
    orderbook = orderbook.copy()
    orderbook["minute"] = orderbook["timestamp"].dt.floor("min")
    groups = list(orderbook.groupby("minute"))
    max_iterations = 500  # Limit for reasonable backtest duration
    for minute, group in groups[:max_iterations]:
        market_data = {"orderbook": group, "symbol": "BTC-USD"}
        signal = strategy.evaluate(market_data)
        if signal is None:
            continue

        ok, reason = risk_limits.check(signal, capital)
        if not ok:
            continue
        ok, reason = kill_switch.check()
        if not ok:
            continue

        from ai_arb_lab.core.clock import SimClock
        clock = SimClock()
        clock.start(datetime.fromisoformat(str(minute)))
        _, fill = broker.submit_order(signal, clock)
        if fill:
            trade_count += 1
            # Simplified: assume profit if we got a fill
            win_count += 1
        capital = broker.capital

    metrics = BacktestMetrics.from_results(
        initial_capital=initial_capital,
        final_capital=capital,
        trade_count=trade_count,
        win_count=win_count,
    )

    # Save report
    output_dir.mkdir(parents=True, exist_ok=True)
    md = render_markdown_report(metrics)
    save_report(md, output_dir / "backtest_report.md")
    (output_dir / "backtest_metrics.json").write_text(json.dumps(metrics.to_dict(), indent=2))

    return metrics


@app.callback()
def main() -> None:
    """AI Arb Lab - Simulation-first arbitrage research."""


@app.command()
def version() -> None:
    """Show version."""
    typer.echo(__version__)


@app.command()
def generate_data(
    output: Path = typer.Option("./data/sample", "--output", "-o", path_type=Path),
    days: int = typer.Option(1, "--days", "-d"),
    seed: int = typer.Option(42, "--seed", "-s"),
    venues: int = typer.Option(2, "--venues", "-v"),
) -> None:
    """Generate synthetic market data."""
    setup_logging()
    gen = SyntheticMarketGenerator(seed=seed, n_venues=venues)
    paths = gen.generate_all(output, days=days)
    typer.echo(f"Generated: {list(paths.values())}")


@app.command()
def backtest(
    data_dir: Path = typer.Option(None, "--data-dir", "-d", path_type=Path),
    output: Path = typer.Option("./reports", "--output", "-o", path_type=Path),
    initial_capital: float = typer.Option(BACKTEST_INITIAL_CAPITAL, "--capital", "-c"),
) -> None:
    """Run backtest on data directory."""
    data_dir = data_dir or DATA_DIR
    metrics = _run_backtest_engine(data_dir, output, initial_capital)
    typer.echo(f"Backtest complete. Return: {metrics.total_return_pct:.2%}, Trades: {metrics.trade_count}")
    typer.echo(f"Report saved to {output / 'backtest_report.md'}")


@app.command()
def paper_run(
    data_dir: Path = typer.Option(None, "--data-dir", "-d", path_type=Path),
    duration: int = typer.Option(60, "--duration", help="Seconds to run (simulated)"),
) -> None:
    """Run paper trading simulation."""
    setup_logging()
    data_dir = data_dir or DATA_DIR
    data = load_data_dir(data_dir)
    if "orderbook" not in data:
        raise typer.BadParameter("No orderbook data. Run generate-data first.")

    typer.echo(f"Paper run for {duration}s (simulated). No real orders.")
    # Simplified: just run a few iterations
    strategy = SimpleSpreadStrategy()
    orderbook = data["orderbook"]
    signals = 0
    for _, group in orderbook.head(100).groupby(orderbook["timestamp"].dt.floor("min")):
        s = strategy.evaluate({"orderbook": group, "symbol": "BTC-USD"})
        if s:
            signals += 1
    typer.echo(f"Detected {signals} potential signals (simulation only)")


@app.command()
def report(
    input_path: str = typer.Argument(..., help="Path to metrics JSON (e.g. reports/backtest_metrics.json)"),
    output: Path = typer.Option("./reports/summary.md", "--output", "-o", path_type=Path),
) -> None:
    """Generate report from backtest metrics JSON."""
    setup_logging()
    path = Path(input_path)
    if "*" in input_path:
        parent = path.parent
        pattern = path.name
        files = list(parent.glob(pattern)) if parent.exists() else []
    else:
        files = [path] if path.exists() else []

    if not files:
        typer.echo("No input files found")
        raise typer.Exit(1)

    all_metrics = []
    for f in files:
        data = json.loads(f.read_text())
        m = BacktestMetrics(
            initial_capital=data["initial_capital"],
            final_capital=data["final_capital"],
            total_return=data["total_return"],
            total_return_pct=data["total_return_pct"],
            trade_count=data["trade_count"],
            win_count=data["win_count"],
            max_drawdown_pct=data["max_drawdown_pct"],
            sharpe_ratio=data.get("sharpe_ratio"),
        )
        all_metrics.append(m)

    # Aggregate or use first
    m = all_metrics[0]
    content = render_markdown_report(m, title="Backtest Summary")
    save_report(content, output)
    typer.echo(f"Report saved to {output}")
