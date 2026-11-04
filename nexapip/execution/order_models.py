"""Minimal order and fill models."""
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True)
class Order:
    side: str
    quantity: float
    order_id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self):
        if self.side not in {"buy", "sell"}:
            raise ValueError("side must be 'buy' or 'sell'")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")


@dataclass(frozen=True)
class Fill:
    order_id: str
    quantity: float
    price: float
    fee: float = 0.0
