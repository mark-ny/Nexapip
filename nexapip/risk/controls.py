"""Risk control checks and enforcement."""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class RiskCheckResult:
    """Result of a risk control check."""
    
    passed: bool
    reason: str
    check_name: str


class RiskControls:
    """
    Enforce mandatory risk controls.
    
    These cannot be overridden by strategy or AI.
    """

    def __init__(
        self,
        max_risk_per_trade: float,
        max_daily_loss: float,
        max_open_positions: int,
        max_exposure: float,
        max_spread_pips: float,
        min_stop_distance_pips: float,
    ):
        """
        Initialize risk controls.
        
        Args:
            max_risk_per_trade: Max risk per trade (percentage of balance)
            max_daily_loss: Max daily loss (percentage of balance)
            max_open_positions: Max simultaneous open positions
            max_exposure: Max total exposure (percentage of balance)
            max_spread_pips: Max acceptable spread in pips
            min_stop_distance_pips: Minimum stop distance in pips
        """
        self.max_risk_per_trade = max_risk_per_trade
        self.max_daily_loss = max_daily_loss
        self.max_open_positions = max_open_positions
        self.max_exposure = max_exposure
        self.max_spread_pips = max_spread_pips
        self.min_stop_distance_pips = min_stop_distance_pips

    def check_position_size(
        self,
        entry_price: float,
        stop_price: float,
        account_balance: float,
    ) -> RiskCheckResult:
        """
        Check if stop distance meets minimum.
        
        Args:
            entry_price: Entry price
            stop_price: Stop loss price
            account_balance: Current balance (for logging)
        
        Returns:
            RiskCheckResult
        """
        if entry_price <= 0 or stop_price <= 0:
            return RiskCheckResult(
                passed=False,
                reason="Invalid prices",
                check_name="position_size",
            )

        stop_distance_pips = abs(entry_price - stop_price) * 10000

        if stop_distance_pips < self.min_stop_distance_pips:
            return RiskCheckResult(
                passed=False,
                reason=(
                    f"Stop distance {stop_distance_pips:.2f} pips "
                    f"below minimum {self.min_stop_distance_pips} pips"
                ),
                check_name="position_size",
            )

        return RiskCheckResult(
            passed=True,
            reason=f"Stop distance {stop_distance_pips:.2f} pips valid",
            check_name="position_size",
        )

    def check_spread(self, bid: float, ask: float) -> RiskCheckResult:
        """
        Check if spread is acceptable.
        
        Args:
            bid: Bid price
            ask: Ask price
        
        Returns:
            RiskCheckResult
        """
        if bid <= 0 or ask <= 0:
            return RiskCheckResult(
                passed=False,
                reason="Invalid bid/ask prices",
                check_name="spread",
            )

        spread_pips = (ask - bid) * 10000

        if spread_pips > self.max_spread_pips:
            return RiskCheckResult(
                passed=False,
                reason=(
                    f"Spread {spread_pips:.2f} pips "
                    f"exceeds maximum {self.max_spread_pips} pips"
                ),
                check_name="spread",
            )

        return RiskCheckResult(
            passed=True,
            reason=f"Spread {spread_pips:.2f} pips acceptable",
            check_name="spread",
        )

    def check_open_positions(
        self,
        current_open_positions: int,
    ) -> RiskCheckResult:
        """Check if opening another position would exceed limit."""
        if current_open_positions >= self.max_open_positions:
            return
