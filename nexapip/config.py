"""Configuration management for Nexapip trading bot."""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class AccountConfig:
    """Account and risk parameters."""
    balance: float
    currency: str
    risk_per_trade: float
    max_daily_loss: float
    max_open_positions: int
    max_exposure: float
    max_spread_pips: float
    min_stop_distance_pips: float


@dataclass
class DataConfig:
    """Market data source configuration."""
    source: str  # 'csv', 'mt5', 'api'
    symbol: str
    timeframe: str
    csv_path: Optional[str] = None
    mt5_login: Optional[int] = None
    mt5_password: Optional[str] = None
    mt5_server: Optional[str] = None


@dataclass
class StrategyConfig:
    """Strategy parameters."""
    version: str
    ema_fast: int
    ema_slow: int
    atr_period: int
    atr_multiplier: float


@dataclass
class OllamaConfig:
    """Ollama AI configuration."""
    enabled: bool
    base_url: str
    model: str
    timeout_seconds: int = 30


@dataclass
class NexapipConfig:
    """Complete application configuration."""
    trading_mode: str  # 'paper' only
    account: AccountConfig
    data: DataConfig
    strategy: StrategyConfig
    ollama: OllamaConfig
    database_path: str
    log_level: str
    log_file: str
    paper_kill_switch_enabled: bool

    @classmethod
    def from_env(cls) -> "NexapipConfig":
        """Load configuration from environment variables."""
        trading_mode = os.getenv("TRADING_MODE", "paper")
        
        if trading_mode != "paper":
            raise ValueError(f"Only 'paper' trading mode is permitted. Got: {trading_mode}")

        account = AccountConfig(
            balance=float(os.getenv("ACCOUNT_BALANCE", "10000")),
            currency=os.getenv("ACCOUNT_CURRENCY", "USD"),
            risk_per_trade=float(os.getenv("RISK_PER_TRADE", "0.02")),
            max_daily_loss=float(os.getenv("MAX_DAILY_LOSS", "0.05")),
            max_open_positions=int(os.getenv("MAX_OPEN_POSITIONS", "3")),
            max_exposure=float(os.getenv("MAX_EXPOSURE", "0.10")),
            max_spread_pips=float(os.getenv("MAX_SPREAD_PIPS", "2.0")),
            min_stop_distance_pips=float(os.getenv("MIN_STOP_DISTANCE_PIPS", "5.0")),
        )

        data = DataConfig(
            source=os.getenv("DATA_SOURCE", "csv"),
            symbol=os.getenv("SYMBOL", "EURUSD"),
            timeframe=os.getenv("TIMEFRAME", "H1"),
            csv_path=os.getenv("CSV_DATA_PATH"),
        )

        strategy = StrategyConfig(
            version=os.getenv("STRATEGY_VERSION", "ema_atr_v1"),
            ema_fast=int(os.getenv("EMA_FAST", "12")),
            ema_slow=int(os.getenv("EMA_SLOW", "26")),
            atr_period=int(os.getenv("ATR_PERIOD", "14")),
            atr_multiplier=float(os.getenv("ATR_MULTIPLIER", "1.5")),
        )

        ollama = OllamaConfig(
            enabled=os.getenv("OLLAMA_ENABLED", "false").lower() == "true",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            model=os.getenv("OLLAMA_MODEL", "llama2"),
        )

        return cls(
            trading_mode=trading_mode,
            account=account,
            data=data,
            strategy=strategy,
            ollama=ollama,
            database_path=os.getenv("DATABASE_PATH", "nexapip.db"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file=os.getenv("LOG_FILE", "nexapip.log"),
            paper_kill_switch_enabled=os.getenv("PAPER_KILL_SWITCH_ENABLED", "false").lower() == "true",
        )

    def validate(self) -> None:
        """Validate configuration on startup."""
        if self.trading_mode != "paper":
            raise ValueError(f"Only 'paper' mode allowed. Got: {self.trading_mode}")
        
        if self.account.balance <= 0:
            raise ValueError("Account balance must be positive")
        
        if not 0 < self.account.risk_per_trade < 1:
            raise ValueError("Risk per trade must be between 0 and 1")
        
        if not 0 < self.account.max_daily_loss < 1:
            raise ValueError("Max daily loss must be between 0 and 1")
        
        if self.account.max_open_positions < 1:
            raise ValueError("Max open positions must be >= 1")
        
        if self.data.source not in ("csv", "mt5", "api"):
            raise ValueError(f"Data source must be csv, mt5, or api. Got: {self.data.source}")
        
        if self.data.source == "csv" and not self.data.csv_path:
            raise ValueError("CSV path required when data source is 'csv'")
        
        if self.strategy.ema_fast >= self.strategy.ema_slow:
            raise ValueError("EMA fast must be < EMA slow")
        
        if self.strategy.atr_period < 1:
            raise ValueError("ATR period must be >= 1")
