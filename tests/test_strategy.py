import pandas as pd
from nexapip.strategy.ema_atr import EmaAtrStrategy


def test_strategy_signal_values():
    data = pd.DataFrame({"close": range(1, 40), "high": [x + 1 for x in range(1, 40)],
                         "low": [x - 1 for x in range(1, 40)]})
    signals = EmaAtrStrategy(3, 6, 3).generate_signals(data)
    assert set(signals.unique()) <= {-1, 0, 1}
