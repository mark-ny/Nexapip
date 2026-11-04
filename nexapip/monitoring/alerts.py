"""Alert callback abstraction; default implementation logs warnings."""
import logging


def send_alert(message: str) -> None:
    logging.getLogger("nexapip.alerts").warning("ALERT: %s", message)
