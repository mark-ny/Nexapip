"""Small bar-by-bar signal backtest for research and education."""
import pandas as pd
from nexapip.backtesting.costs import transaction_cost


def run_backtest(data: pd.DataFrame, signals: pd.Series, initial_cash: float = 10_000.0,
                 fee_rate: float = 0.0) -> pd.DataFrame:
    if len(data) != len(signals):
        raise ValueError("data and signals must have equal length")
    if initial_cash <= 0:
        raise ValueError("initial_cash must be positive")
    position = signals.shift(1).fillna(0).clip(-1, 1)
    returns = data["close"].pct_change().fillna(0)
    turnover = position.diff().abs().fillna(position.abs())
    costs = turnover * fee_rate
    result = data.copy()
    result["signal"] = signals
    result["position"] = position
    result["strategy_return"] = position * returns - costs
    result["equity"] = initial_cash * (1 + result["strategy_return"]).cumprod()
    return result
