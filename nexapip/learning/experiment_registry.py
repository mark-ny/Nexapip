"""Append-only local JSON experiment registry."""
import json
from datetime import datetime, timezone
from pathlib import Path


class ExperimentRegistry:
    def __init__(self, path: str | Path = "experiments.jsonl"):
        self.path = Path(path)

    def record(self, name: str, parameters: dict, metrics: dict) -> None:
        entry = {"name": name, "parameters": parameters, "metrics": metrics,
                 "created_at": datetime.now(timezone.utc).isoformat()}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(entry, sort_keys=True) + "\n")
