"""Basic portfolio risk limits."""


def within_position_limit(quantity: float, maximum: float) -> bool:
    return 0 <= quantity <= maximum


def within_daily_loss_limit(daily_pnl: float, equity: float, limit_fraction: float) -> bool:
    if equity <= 0 or not 0 <= limit_fraction <= 1:
        return False
    return daily_pnl > -(equity * limit_fraction)
