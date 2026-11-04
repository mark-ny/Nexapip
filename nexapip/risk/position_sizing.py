"""Position sizing and risk calculations."""

from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class PositionSizer:
    """
    Calculate position size based on risk management rules.
    
    Conservative approach: always rounds down, never up.
    """

    @staticmethod
    def calculate_lot_size(
        account_balance: float,
        risk_amount: float,
        entry_price: float,
        stop_price: float,
        instrument_pip_value: float = 10.0,
        account_currency: str = "USD",
    ) -> float:
        """
        Calculate position size in lots.
        
        Args:
            account_balance: Current account balance
            risk_amount: Amount willing to risk per trade (e.g., 200 USD)
            entry_price: Entry price
            stop_price: Stop loss price
            instrument_pip_value: Pip value (e.g., 10 USD per pip for EURUSD 1.0 lot)
            account_currency: Account base currency
        
        Returns:
            Position size in lots (rounded down)
        
        Raises:
            ValueError: If parameters are invalid
        """
        if account_balance <= 0:
            raise ValueError("Account balance must be positive")

        if risk_amount <= 0:
            raise ValueError("Risk amount must be positive")

        if entry_price <= 0 or stop_price <= 0:
            raise ValueError("Prices must be positive")

        if entry_price == stop_price:
            raise ValueError("Entry and stop prices cannot be equal")

        if instrument_pip_value <= 0:
            raise ValueError("Instrument pip value must be positive")

        # Calculate risk in pips
        risk_pips = abs(entry_price - stop_price) * 10000  # Convert to pips

        if risk_pips == 0:
            raise ValueError("Risk in pips cannot be zero")

        # Calculate lot size: risk_amount / (risk_pips * pip_value_per_lot)
        lot_size = risk_amount / (risk_pips * instrument_pip_value)

        # Conservative: round down
        lot_size = int(lot_size * 100) / 100

        if lot_size < 0.01:
            lot_size = 0.0

        logger.debug(
            f"Calculated lot size: {lot_size} "
            f"(balance={account_balance}, risk={risk_amount}, "
            f"risk_pips={risk_pips})"
        )

        return lot_size

    @staticmethod
    def calculate_risk_amount(
        account_balance: float,
        risk_percentage: float,
    ) -> float:
        """
        Calculate risk amount from percentage.
        
        Args:
            account_balance: Current account balance
            risk_percentage: Risk as percentage (e.g., 0.02 for 2%)
        
        Returns:
            Risk amount in account currency
        
        Raises:
            ValueError: If parameters invalid
        """
        if account_balance <= 0:
            raise ValueError("Account balance must be positive")

        if not 0 < risk_percentage < 1:
            raise ValueError("Risk percentage must be between 0 and 1")

        return account_balance * risk_percentage

    @staticmethod
    def calculate_position_value(
        lot_size: float,
        entry_price: float,
        pip_value: float = 10.0,
    ) -> float:
        """
        Calculate notional value of position.
        
        Args:
            lot_size: Position size in lots
            entry_price: Entry price
            pip_value: Pip value per lot
        
        Returns:
            Position value in account currency
        """
        # For Forex: 1 standard lot = 100,000 units
        # Notional value = lot_size * 100,000 * entry_price
        return lot_size * 100000 * entry_price
