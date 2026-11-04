"""Summarize closed trade outcomes."""


def analyze_trades(trades: list[dict]) -> dict[str, float]:
    pnls = [float(trade.get("pnl", 0.0)) for trade in trades]
    wins = [pnl for pnl in pnls if pnl > 0]
    losses = [pnl for pnl in pnls if pnl < 0]
    return {"count": float(len(pnls)), "win_rate": len(wins) / len(pnls) if pnls else 0.0,
            "net_pnl": sum(pnls), "average_win": sum(wins) / len(wins) if wins else 0.0,
            "average_loss": sum(losses) / len(losses) if losses else 0.0}
