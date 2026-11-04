"""Strategy management and selection."""

from typing import Dict, Optional
import logging

from .base import BaseStrategy
from .ema_atr import EMAATRStrategy

logger = logging.getLogger(__name__)


class StrategyManager:
    """Manage strategy instances and versions."""

    def __init__(self):
        """Initialize strategy manager."""
        self.strategies: Dict[str, BaseStrategy] = {}
        self.active_strategy: Optional[str] = None

    def register(self, name: str, strategy: BaseStrategy) -> None:
        """
        Register a strategy.
        
        Args:
            name: Unique strategy identifier
            strategy: Strategy instance
        """
        self.strategies[name] = strategy
        logger.info(f"Registered strategy: {name}")

    def get(self, name: str) -> Optional[BaseStrategy]:
        """
        Retrieve a strategy by name.
        
        Args:
            name: Strategy identifier
        
        Returns:
            Strategy instance or None
        """
        return self.strategies.get(name)

    def set_active(self, name: str) -> bool:
        """
        Set active strategy for trading.
        
        Args:
            name: Strategy identifier
        
        Returns:
            True if set successfully
        """
        if name not in self.strategies:
            logger.error(f"Strategy not found: {name}")
            return False

        self.active_strategy = name
        logger.info(f"Active strategy set to: {name}")
        return True

    def get_active(self) -> Optional[BaseStrategy]:
        """Get currently active strategy."""
        if self.active_strategy is None:
            return None
        return self.strategies.get(self.active_strategy)

    @staticmethod
    def create_ema_atr(
        version: str = "v1",
        ema_fast: int = 12,
        ema_slow: int = 26,
        atr_period: int = 14,
        atr_multiplier: float = 1.5,
    ) -> EMAATRStrategy:
        """
        Factory method to create EMA+ATR strategy.
        
        Args:
            version: Strategy version
            ema_fast: Fast EMA period
            ema_slow: Slow EMA period
            atr_period: ATR period
            atr_multiplier: Stop distance multiplier
        
        Returns:
            Configured EMA+ATR strategy
        """
        return EMAATRStrategy(
            version=version,
            ema_fast=ema_fast,
            ema_slow=ema_slow,
            atr_period=atr_period,
            atr_multiplier=atr_multiplier,
        )
