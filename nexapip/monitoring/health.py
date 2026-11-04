"""Basic process health status."""
from datetime import datetime, timezone


def health_status() -> dict[str, str]:
    return {"status": "ok", "checked_at": datetime.now(timezone.utc).isoformat()}
