"""Base strategy interface."""
from abc import ABC, abstractmethod
import pandas as pd


class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Return one signal per row: -1 short, 0 flat, +1 long."""
