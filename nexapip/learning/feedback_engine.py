"""Rule-based feedback placeholder; does not automatically alter strategies."""
from nexapip.learning.trade_analyzer import analyze_trades


def review_trades(trades: list[dict]) -> dict[str, float | str]:
    metrics = analyze_trades(trades)
    note = "Collect more paper-trading data before drawing conclusions."
    if metrics["count"] >= 20:
        note = "Review performance and risk controls; do not deploy changes without validation."
    return {**metrics, "note": note}
