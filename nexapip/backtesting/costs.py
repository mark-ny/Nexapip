"""Transaction cost helpers."""


def transaction_cost(notional: float, fee_rate: float) -> float:
    if notional < 0 or fee_rate < 0:
        raise ValueError("notional and fee_rate must be non-negative")
    return notional * fee_rate
