"""Tiny SQLite repository for serialized experiment records."""
import json
import sqlite3
from nexapip.storage.database import connect


class ExperimentRepository:
    def __init__(self, connection: sqlite3.Connection | None = None):
        self.connection = connection or connect()
        self.connection.execute("CREATE TABLE IF NOT EXISTS experiments (id INTEGER PRIMARY KEY, name TEXT, payload TEXT)")
        self.connection.commit()

    def add(self, name: str, payload: dict) -> None:
        self.connection.execute("INSERT INTO experiments(name, payload) VALUES (?, ?)",
                                (name, json.dumps(payload, sort_keys=True)))
        self.connection.commit()

    def list_all(self) -> list[dict]:
        rows = self.connection.execute("SELECT name, payload FROM experiments ORDER BY id").fetchall()
        return [{"name": name, **json.loads(payload)} for name, payload in rows]
