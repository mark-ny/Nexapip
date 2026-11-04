import pytest
from nexapip.execution.order_models import Order
from nexapip.execution.paper_broker import PaperBroker


def test_paper_broker_fill():
    fill = PaperBroker(slippage=.01, fee_rate=.001).submit(Order("buy", 2), 100)
    assert fill.price == pytest.approx(101)
    assert fill.fee == pytest.approx(.202)
