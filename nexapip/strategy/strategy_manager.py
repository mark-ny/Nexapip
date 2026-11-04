"""Strategy selection and signal dispatch."""
from nexapip.strategy.base import Strategy


class StrategyManager:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def signals(self, data):
        return self.strategy.generate_signals(data)
