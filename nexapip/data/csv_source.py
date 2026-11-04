"""CSV data source for historical candles."""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import logging

from .interfaces import Candle, DataSource

logger = logging.getLogger(__name__)


class CSVDataSource(DataSource):
    """Load candle data from CSV files."""

    def __init__(self, csv_path: str):
        """
        Initialize CSV data source.
        
        Args:
            csv_path: Path to CSV file
        """
        self.csv_path = Path(csv_path)
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found:
