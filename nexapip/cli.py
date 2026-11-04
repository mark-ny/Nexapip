"""Command-line entry point for basic data validation."""
import argparse
import logging

from nexapip.config import Settings
from nexapip.data.csv_source import CsvDataSource
from nexapip.data.validation import validate_ohlcv


def main() -> int:
    parser = argparse.ArgumentParser(description="Nexapip research and paper-trading tools")
    parser.add_argument("--data", help="OHLCV CSV path (overrides NEXAPIP_DATA_PATH)")
    parser.add_argument("--validate", action="store_true", help="Validate the configured CSV")
    args = parser.parse_args()
    settings = Settings.from_env()
    logging.basicConfig(level=settings.log_level)
    if args.validate:
        frame = CsvDataSource(args.data or settings.data_path).load()
        validate_ohlcv(frame)
        print(f"Validated {len(frame)} OHLCV rows")
    else:
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
