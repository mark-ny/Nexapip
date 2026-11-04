"""Application configuration loaded from environment variables."""
from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    starting_cash: float = 10_000.0
    max_risk_fraction: float = 0.01
    data_path: str = "data/prices.csv"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            starting_cash=float(os.getenv("NEXAPIP_STARTING_CASH", "10000")),
            max_risk_fraction=float(os.getenv("NEXAPIP_MAX_RISK_FRACTION", "0.01")),
            data_path=os.getenv("NEXAPIP_DATA_PATH", "data/prices.csv"),
            log_level=os.getenv("NEXAPIP_LOG_LEVEL", "INFO").upper(),
        )
