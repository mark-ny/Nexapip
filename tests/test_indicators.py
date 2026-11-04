import pandas as pd
from nexapip.indicators import ema, atr


def test_ema_has_expected_warmup():
    result = ema(pd.Series([1., 2., 3.]), 2)
    assert result.iloc[:1].isna().all()
    assert result.iloc[1] > 1


def test_atr_positive():
    frame = pd.DataFrame({"high": [2., 3., 4.], "low": [1., 2., 3.], "close": [1.5, 2.5, 3.5]})
    assert atr(frame, 2).dropna().gt(0).all()
