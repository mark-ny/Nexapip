import pandas as pd
import pytest
from nexapip.data.validation import validate_ohlcv


def test_valid_ohlcv():
    validate_ohlcv(pd.DataFrame({"open": [2], "high": [3], "low": [1], "close": [2], "volume": [4]}))


def test_rejects_missing_column():
    with pytest.raises(ValueError):
        validate_ohlcv(pd.DataFrame({"open": [1]}))
