"""Fixed-fractional position sizing."""


def position_size(equity: float, risk_fraction: float, entry: float, stop: float) -> float:
    if equity <= 0 or not 0 <= risk_fraction <= 1 or entry <= 0 or stop <= 0:
        return 0.0
    distance = abs(entry - stop)
    return 0.0 if distance == 0 else (equity * risk_fraction) / distance
