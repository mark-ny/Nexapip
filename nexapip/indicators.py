"""Technical indicators for strategy signals."""

from typing import List, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)


class Indicators:
    """Calculate technical indicators."""

    @staticmethod
    def ema(prices: List[float], period: int) -> List[float]:
        """
        Calculate Exponential Moving Average.
        
        Args:
            prices: List of prices
            period: EMA period
        
        Returns:
            List of EMA values (NaN for insufficient data)
        """
        if len(prices) < period:
            return [np.nan] * len(prices)

        multiplier = 2.0 / (period + 1)
        ema_values = [np.nan] * (period - 1)
        
        # First EMA is SMA
        ema_values.append(np.mean(prices[:period]))

        # Calculate subsequent EMAs
        for i in range(period, len(prices)):
            ema = (prices[i] - ema_values[-1]) * multiplier + ema_values[-1]
            ema_values.append(ema)

        return ema_values

    @staticmethod
    def atr(
        candles: List[dict],
        period: int,
    ) -> List[float]:
        """
        Calculate Average True Range.
        
        Args:
            candles: List of dicts with high, low, close
            period: ATR period
        
        Returns:
            List of ATR values (NaN for insufficient data)
        """
        if len(candles) < period:
            return [np.nan] * len(candles)

        true_ranges = []
        for i, candle in enumerate(candles):
            high = candle["high"]
            low = candle["low"]
            close = candle.get("prev_close", candle["close"])

            tr = max(
                high - low,
                abs(high - close),
                abs(low - close),
            )
            true_ranges.append(tr)

        atr_values = [np.nan] * (period - 1)
        atr_values.append(np.mean(true_ranges[:period]))

        for i in range(period, len(true_ranges)):
            atr = (
                (atr_values[-1] * (period - 1) + true_ranges[i]) / period
            )
            atr_values.append(atr)

        return atr_values

    @staticmethod
    def sma(prices: List[float], period: int) -> List[float]:
        """
        Calculate Simple Moving Average.
        
        Args:
            prices: List of prices
            period: SMA period
        
        Returns:
            List of SMA values (NaN for insufficient data)
        """
        if len(prices) < period:
            return [np.nan] * len(prices)

        sma_values = [np.nan] * (period - 1)
        for i in range(period - 1, len(prices)):
            sma = np.mean(prices[i - period + 1 : i + 1])
            sma_values.append(sma)

        return sma_values

    @staticmethod
    def rsi(prices: List[float], period: int = 14) -> List[float]:
        """
        Calculate Relative Strength Index.
        
        Args:
            prices: List of prices
            period: RSI period
        
        Returns:
            List of RSI values (0-100, NaN for insufficient data)
        """
        if len(prices) < period + 1:
            return [np.nan] * len(prices)

        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])

        rsi_values = [np.nan] * period

        for i in range(period, len(prices)):
            avg_gain = (avg_gain * (period - 1) + gains[i - 1]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i - 1]) / period

            rs = avg_gain / avg_loss if avg_loss != 0 else 0
            rsi = 100 - (100 / (1 + rs)) if rs >= 0 else 0
            rsi_values.append(rsi)

        return rsi_values

    @staticmethod
    def validate_parameters(**params) -> List[str]:
        """
        Validate indicator parameters.
        
        Args:
            **params: Parameter name -> value pairs
        
        Returns:
            List of validation errors
        """
        errors = []

        if "period" in params and params["period"] < 1:
            errors.append("Period must be >= 1")

        if "ema_fast" in params and "ema_slow" in params:
            if params["ema_fast"] >= params["ema_slow"]:
                errors.append("EMA fast must be < EMA slow")

        return errors
