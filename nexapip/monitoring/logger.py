"""Package logger configuration."""
import logging


def get_logger(name: str = "nexapip") -> logging.Logger:
    return logging.getLogger(name)
