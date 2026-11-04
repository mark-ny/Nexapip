"""Broker interface; implementations should make execution mode explicit."""
from typing import Protocol
from nexapip.execution.order_models import Order, Fill


class Broker(Protocol):
    def submit(self, order: Order, market_price: float) -> Fill: ...
