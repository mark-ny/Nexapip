import pandas as pd
from nexapip.backtesting.engine import run_backtest
from nexapip.backtesting.metrics import summarize


def test_backtest_and_metrics():
    data = pd.DataFrame({"close": [100., 110., 121.]})
    result = run_backtest(data, pd.Series([1, 1, 0]), fee_rate=0)
    assert result["equity"].iloc[-1] > result["equity"].iloc[0]
    assert summarize(result["equity"])["total_return"] > 0
