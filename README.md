# Nexapip

Nexapip is a Python framework scaffold for market-data validation, technical indicators, strategy research, backtesting, risk controls, and **paper trading only**. It does not provide live order execution or financial advice.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Validate a CSV

Provide columns `open, high, low, close, volume`; an optional `timestamp` column is parsed as UTC.

```bash
python -m nexapip.cli --data path/to/prices.csv --validate
```

## Tests

```bash
pytest
```

## Project layout

- `nexapip/data`: CSV and optional read-only MetaTrader 5 sources, validation.
- `nexapip/strategy`, `indicators.py`: strategy contracts and EMA/ATR example.
- `nexapip/risk`: sizing, limits, and loss-streak breaker.
- `nexapip/execution`: order models and an in-memory paper broker.
- `nexapip/backtesting`: a simple bar-based simulation, costs, metrics, and chronological splits.
- `nexapip/learning`: trade summaries and experiment review helpers.
- `nexapip/storage`, `monitoring`: local persistence and basic health/logging helpers.

This is an initial scaffold, not a production-ready trading system. Validate assumptions, avoid look-ahead bias, include realistic execution costs, and test extensively before relying on research results. Never connect this scaffold to a live brokerage account.
