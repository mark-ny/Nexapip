"""Validation helpers for OHLCV data."""
import pandas as pd

REQUIRED_COLUMNS = {"open", "high", "low", "close", "volume"}


def validate_ohlcv(frame: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Missing OHLCV columns: {', '.join(sorted(missing))}")
    if frame.empty:
        raise ValueError("OHLCV data is empty")
    if frame[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("OHLCV data contains missing values")
    if (frame["high"] < frame[["open", "close", "low"]].max(axis=1)).any():
        raise ValueError("High must be at least open, close, and low")
    if (frame["low"] > frame[["open", "close", "high"]].min(axis=1)).any():
        raise ValueError("Low must be at most open, close, and high")
    if (frame["volume"] < 0).any():
        raise ValueError("Volume cannot be negative")
