"""Market data source interfaces."""
from typing import Protocol
import pandas as pd


class DataSource(Protocol):
    def load(self) -> pd.DataFrame: ...
