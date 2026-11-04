"""Simple loss-streak circuit breaker."""


class CircuitBreaker:
    def __init__(self, max_consecutive_losses: int = 3):
        if max_consecutive_losses < 1:
            raise ValueError("max_consecutive_losses must be positive")
        self.max_consecutive_losses = max_consecutive_losses
        self.consecutive_losses = 0

    @property
    def halted(self) -> bool:
        return self.consecutive_losses >= self.max_consecutive_losses

    def record_result(self, pnl: float) -> None:
        self.consecutive_losses = self.consecutive_losses + 1 if pnl < 0 else 0

    def reset(self) -> None:
        self.consecutive_losses = 0
