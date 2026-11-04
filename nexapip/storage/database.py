"""SQLite connection helper."""
import sqlite3
from pathlib import Path


def connect(path: str | Path = "nexapip.sqlite3") -> sqlite3.Connection:
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)
