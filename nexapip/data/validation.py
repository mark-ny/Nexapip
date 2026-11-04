"""Data validation utilities."""

from typing import List, Tuple
from datetime import datetime, timedelta
import logging

from .interfaces import Candle

logger = logging.getLogger(__name__)


class DataValidator:
    """Validate market data integrity."""

    @staticmethod
    def detect_gaps(
        candles: List[Candle],
        expected_interval_minutes: int,
    ) -> List[Tuple[Candle, Candle]]:
        """
        Detect missing candles based on expected interval.
        
        Args:
            candles: Sorted list of candles
            expected_interval_minutes: Expected minutes between candles
        
        Returns:
            List of (prev_candle, next_candle) tuples with gaps
        """
        gaps = []
        expected_delta = timedelta(minutes=expected_interval_minutes)

        for i in range(len(candles) - 1):
            current = candles[i]
            next_candle = candles[i + 1]
            actual_delta = next_candle.timestamp - current.timestamp

            if actual_delta > expected_delta:
                gaps.append((current, next_candle))

        return gaps

    @staticmethod
    def detect_stale_data(
        candles: List[Candle],
        max_age_hours: int = 24,
    ) -> List[Candle]:
        """
        Detect stale candles (old data).
        
        Args:
            candles: List of candles
            max_age_hours: Maximum acceptable age in hours
        
        Returns:
            List of stale candles
        """
        cutoff = datetime.utcnow().replace(tzinfo=None)
        stale = []

        for candle in candles:
            candle_time = candle.timestamp.replace(tzinfo=None)
            age = cutoff - candle_time
            if age > timedelta(hours=max_age_hours):
                stale.append(candle)

        return stale

    @staticmethod
    def detect_outliers(
        candles: List[Candle],
        std_dev_threshold: float = 5.0,
    ) -> List[Candle]:
        """
        Detect price outliers using simple std dev check.
        
        Args:
            candles: List of candles
            std_dev_threshold: Number of std devs to flag as outlier
        
        Returns:
            List of suspicious candles
        """
        import numpy as np

        if len(candles) < 10:
            return []

        closes = np.array([c.close for c in candles])
        mean = np.mean(closes)
        std = np.std(closes)

        outliers = []
        for candle in candles:
            z_score = abs((candle.close - mean) / std) if std > 0 else 0
            if z_score > std_dev_threshold:
                outliers.append(candle)

        return outliers

    @staticmethod
    def report_quality(candles: List[Candle], timeframe: str = "H1") -> dict:
        """
        Generate data quality report.
        
        Args:
            candles: List of candles to check
            timeframe: Expected timeframe (for gap detection)
        
        Returns:
            Dictionary with quality metrics
        """
        timeframe_minutes = {
            "M1": 1,
            "M5": 5,
            "M15": 15,
            "M30": 30,
            "H1": 60,
            "H4": 240,
            "D1": 1440,
        }

        expected_minutes = timeframe_minutes.get(timeframe, 60)

        gaps = DataValidator.detect_gaps(candles, expected_minutes)
        stale = DataValidator.detect_stale_data(candles)
        outliers = DataValidator.detect_outliers(candles)

        return {
            "total_candles": len(candles),
            "gaps_detected": len(gaps),
            "stale_candles": len(stale),
            "outliers_detected": len(outliers),
            "date_range": (
                f"{candles[0].timestamp} to {candles[-1].timestamp}"
                if candles
                else "No data"
            ),
            "quality_score": max(0, 100 - len(gaps) * 5 - len(outliers) * 10),
        }
