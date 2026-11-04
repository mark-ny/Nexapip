"""Deterministic in-memory broker for simulations; never sends live orders."""
from nexapip.execution.order_models import Fill, Order


class PaperBroker:
    def __init__(self, slippage: float = 0.0, fee_rate: float = 0.0):
        if slippage < 0 or fee_rate < 0:
            raise ValueError("slippage and fee_rate must be non-negative")
        self.slippage, self.fee_rate = slippage, fee_rate
        self.fills: list[Fill] = []

    def submit(self, order: Order, market_price: float) -> Fill:
        if market_price <= 0:
            raise ValueError("market_price must be positive")
        direction = 1 if order.side == "buy" else -1
        price = market_price * (1 + direction * self.slippage)
        fill = Fill(order_id=order.order_id, quantity=order.quantity, price=price,
                    fee=abs(order.quantity * price) * self.fee_rate)
        self.fills.append(fill)
        return fill
