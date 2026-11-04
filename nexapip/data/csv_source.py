"""CSV-backed OHLCV data source."""
from pathlib import Path
import pandas as pd


class CsvDataSource:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> pd.DataFrame:
        frame = pd.read_csv(self.path)
        if "timestamp" in frame.columns:
            frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        return frame
