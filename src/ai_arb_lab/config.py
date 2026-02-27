"""Configuration management. Load from env and defaults."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def get_env(key: str, default: str = "") -> str:
    """Get env var with default."""
    return os.getenv(key, default)


def get_env_float(key: str, default: float = 0.0) -> float:
    """Get env var as float."""
    try:
        return float(os.getenv(key, str(default)))
    except ValueError:
        return default


def get_env_int(key: str, default: int = 0) -> int:
    """Get env var as int."""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default


# Application
APP_ENV = get_env("APP_ENV", "development")
LOG_LEVEL = get_env("LOG_LEVEL", "INFO")
LOG_FORMAT = get_env("LOG_FORMAT", "json")
CORRELATION_ID_PREFIX = get_env("CORRELATION_ID_PREFIX", "arb")

# Data
DATA_DIR = Path(get_env("DATA_DIR", "./data/sample"))
SYNTHETIC_SEED = get_env_int("SYNTHETIC_SEED", 42)
SYNTHETIC_VENUES = get_env_int("SYNTHETIC_VENUES", 2)
SYNTHETIC_DAYS = get_env_int("SYNTHETIC_DAYS", 1)

# Backtest
BACKTEST_INITIAL_CAPITAL = get_env_float("BACKTEST_INITIAL_CAPITAL", 100_000.0)
BACKTEST_COMMISSION_RATE = get_env_float("BACKTEST_COMMISSION_RATE", 0.001)

# Paper
PAPER_INITIAL_CAPITAL = get_env_float("PAPER_INITIAL_CAPITAL", 100_000.0)
PAPER_MODE = get_env("PAPER_MODE", "simulated")
