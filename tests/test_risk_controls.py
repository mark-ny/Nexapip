from nexapip.risk.controls import within_daily_loss_limit, within_position_limit
from nexapip.risk.position_sizing import position_size
from nexapip.risk.circuit_breaker import CircuitBreaker


def test_risk_helpers():
    assert within_position_limit(2, 3)
    assert within_daily_loss_limit(-50, 1000, .1)
    assert position_size(1000, .01, 100, 95) == 2


def test_circuit_breaker():
    breaker = CircuitBreaker(2)
    breaker.record_result(-1)
    breaker.record_result(-1)
    assert breaker.halted
    breaker.reset()
    assert not breaker.halted
