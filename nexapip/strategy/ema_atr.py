"""EMA crossover strategy filtered by ATR availability."""
import pandas as pd
from nexapip.indicators import atr, ema
from nexapip.strategy.base import Strategy


class EmaAtrStrategy(Strategy):
    def __init__(self, fast_period: int = 12, slow_period: int = 26, atr_period: int = 14):
        if min(fast_period, slow_period, atr_period) < 1 or fast_period >= slow_period:
            raise ValueError("Require positive periods and fast_period < slow_period")
        self.fast_period, self.slow_period, self.atr_period = fast_period, slow_period, atr_period

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        fast = ema(data["close"], self.fast_period)
        slow = ema(data["close"], self.slow_period)
        volatility = atr(data, self.atr_period)
        signal = (fast > slow).astype(int) - (fast < slow).astype(int)
        return signal.where(volatility.notna(), 0).rename("signal")
