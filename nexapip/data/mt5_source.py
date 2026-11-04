"""Optional MetaTrader 5 historical data adapter (read-only)."""
from datetime import datetime
import pandas as pd


class MT5DataSource:
    def __init__(self, symbol: str, timeframe: int, start: datetime, end: datetime):
        self.symbol, self.timeframe, self.start, self.end = symbol, timeframe, start, end

    def load(self) -> pd.DataFrame:
        try:
            import MetaTrader5 as mt5
        except ImportError as exc:
            raise RuntimeError("Install the optional MetaTrader5 package to use this source") from exc
        if not mt5.initialize():
            raise RuntimeError(f"MetaTrader5 initialization failed: {mt5.last_error()}")
        try:
            rates = mt5.copy_rates_range(self.symbol, self.timeframe, self.start, self.end)
            if rates is None:
                raise RuntimeError(f"Could not retrieve rates: {mt5.last_error()}")
            frame = pd.DataFrame(rates)
            frame["timestamp"] = pd.to_datetime(frame.pop("time"), unit="s", utc=True)
            return frame.rename(columns={"tick_volume": "volume"})
        finally:
            mt5.shutdown()
