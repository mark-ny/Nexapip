"""Common performance statistics."""
import pandas as pd


def summarize(equity: pd.Series) -> dict[str, float]:
    if equity.empty:
        return {"total_return": 0.0, "max_drawdown": 0.0}
    total_return = float(equity.iloc[-1] / equity.iloc[0] - 1) if equity.iloc[0] else 0.0
    drawdown = equity / equity.cummax() - 1
    return {"total_return": total_return, "max_drawdown": float(drawdown.min())}
