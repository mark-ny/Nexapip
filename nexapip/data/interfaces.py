"""Data source interfaces."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Candle:
    """OHLCV candle data."""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    symbol: str
    timeframe: str

    def validate(self) -> List[str]:
        """
        Validate candle data.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if self.open <= 0 or self.high <= 0 or self.low <= 0 or self.close <= 0:
            errors.append("All OHLC prices must be positive")
        
        if not (self.low <= self.open <= self.high):
            errors.append(f"Invalid OHLC: low({self.low}) <= open({self.open}) <= high({self.high})")
        
        if not (self.low <= self.close <= self.high):
            errors.append(f"Invalid OHLC: low({self.low}) <= close({self.close}) <= high({self.high})")
        
        if self.volume < 0:
            errors.append("Volume cannot be negative")
        
        return errors


class DataSource(ABC):
    """Abstract base for market data sources."""

    @abstractmethod
    def fetch(self, symbol: str, timeframe: str, limit: Optional[int] = None) -> List[Candle]:
        """
        Fetch candle data.
        
        Args:
            symbol: Trading pair (e.g., EURUSD)
            timeframe: Timeframe (e.g., H1, D1)
            limit: Optional limit on number of candles
        
        Returns:
            List of validated Candle objects
        
        Raises:
            ValueError: If data is invalid or fetch fails
        """
        pass
