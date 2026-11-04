"""Simple candidate acceptance gate based on explicit metric thresholds."""


def evaluate_candidate(candidate: dict[str, float], baseline: dict[str, float],
                       min_return_improvement: float = 0.0) -> bool:
    return (candidate.get("total_return", float("-inf")) >=
            baseline.get("total_return", float("inf")) + min_return_improvement and
            candidate.get("max_drawdown", float("-inf")) >= baseline.get("max_drawdown", float("-inf")))
