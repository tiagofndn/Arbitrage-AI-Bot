"""Pytest fixtures."""

from pathlib import Path

import pytest

from ai_arb_lab.data.synthetic import SyntheticMarketGenerator


@pytest.fixture
def sample_data_dir(tmp_path: Path) -> Path:
    """Generate sample data in a temp directory."""
    gen = SyntheticMarketGenerator(seed=42, n_venues=2)
    gen.generate_all(tmp_path, days=1)
    return tmp_path
