from nexapip.learning.trade_analyzer import analyze_trades
from nexapip.learning.candidate_evaluator import evaluate_candidate


def test_trade_analysis():
    result = analyze_trades([{"pnl": 10}, {"pnl": -5}])
    assert result["win_rate"] == .5
    assert result["net_pnl"] == 5


def test_candidate_gate():
    assert evaluate_candidate({"total_return": .2, "max_drawdown": -.1},
                              {"total_return": .1, "max_drawdown": -.2})
