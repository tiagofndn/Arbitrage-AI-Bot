"""Tests for CLI commands."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from ai_arb_lab.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "0.1" in result.stdout


def test_generate_data(tmp_path: Path) -> None:
    result = runner.invoke(app, ["generate-data", "--output", str(tmp_path), "--days", "1", "--seed", "42"])
    assert result.exit_code == 0
    assert (tmp_path / "trades.csv").exists()
    assert (tmp_path / "orderbook.csv").exists()
    assert (tmp_path / "candles.parquet").exists()


def test_backtest(sample_data_dir: Path, tmp_path: Path) -> None:
    result = runner.invoke(app, ["backtest", "--data-dir", str(sample_data_dir), "--output", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / "backtest_report.md").exists()
    assert (tmp_path / "backtest_metrics.json").exists()


def test_paper_run(sample_data_dir: Path) -> None:
    result = runner.invoke(app, ["paper-run", "--data-dir", str(sample_data_dir), "--duration", "10"])
    assert result.exit_code == 0


def test_report(sample_data_dir: Path, tmp_path: Path) -> None:
    # First run backtest to create metrics
    runner.invoke(app, ["backtest", "--data-dir", str(sample_data_dir), "--output", str(tmp_path)])
    metrics_file = tmp_path / "backtest_metrics.json"
    assert metrics_file.exists()

    result = runner.invoke(app, ["report", str(metrics_file), "--output", str(tmp_path / "summary.md")])
    assert result.exit_code == 0
    assert (tmp_path / "summary.md").exists()
