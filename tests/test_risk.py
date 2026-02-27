"""Tests for risk management."""

import pytest

from ai_arb_lab.risk.kill_switch import KillSwitch
from ai_arb_lab.risk.limits import RiskLimits
from ai_arb_lab.strategies.base import Signal


def test_kill_switch_allows_when_not_triggered() -> None:
    ks = KillSwitch(enabled=True)
    ok, reason = ks.check()
    assert ok is True
    assert reason == "OK"


def test_kill_switch_blocks_when_triggered() -> None:
    ks = KillSwitch(enabled=True)
    ks.trigger()
    ok, reason = ks.check()
    assert ok is False
    assert "triggered" in reason.lower()


def test_kill_switch_reset() -> None:
    ks = KillSwitch(enabled=True)
    ks.trigger()
    ks.reset()
    ok, _ = ks.check()
    assert ok is True


def test_risk_limits_check() -> None:
    limits = RiskLimits(max_exposure=10000, initial_capital=10000)
    signal = Signal(
        symbol="BTC-USD",
        side="buy",
        venue_buy="v1",
        venue_sell="v2",
        price_buy=100,
        price_sell=101,
        size=5,  # notional ~1005
        expected_profit_bps=10,
    )
    ok, reason = limits.check(signal, current_capital=9000)
    assert ok is True


def test_risk_limits_rejects_exposure() -> None:
    limits = RiskLimits(max_exposure=100, initial_capital=10000)
    signal = Signal(
        symbol="BTC-USD",
        side="buy",
        venue_buy="v1",
        venue_sell="v2",
        price_buy=100,
        price_sell=101,
        size=10,  # notional ~2000
        expected_profit_bps=10,
    )
    ok, reason = limits.check(signal, current_capital=9000)
    assert ok is False
    assert "exposure" in reason.lower()
