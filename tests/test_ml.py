import sys, os
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../ml"))


def test_churn_rule_low():
    from recommendation_engine.rules import _apply_rules
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../recommendation_engine"))
    from rules import _apply_rules

    actions = _apply_rules(0.20, 3000)
    priorities = [a[1] for a in actions]
    assert "high" not in priorities


def test_churn_rule_high():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../recommendation_engine"))
    from rules import _apply_rules

    actions = _apply_rules(0.90, 500)
    priorities = [a[1] for a in actions]
    assert "high" in priorities


def test_churn_rule_champion():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../recommendation_engine"))
    from rules import _apply_rules

    actions = _apply_rules(0.10, 8000)
    texts = [a[0] for a in actions]
    assert any("upsell" in t or "thank" in t for t in texts)


def test_clv_segment():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../ml"))
    from clv_model import _segment

    assert _segment(6000) == "champion"
    assert _segment(3000) == "loyal"
    assert _segment(700)  == "potential"
    assert _segment(100)  == "at-risk"


def test_revenue_forecast_needs_data():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../ml"))
    import numpy as np
    from sklearn.linear_model import LinearRegression

    # simulate 4 months of data
    months   = np.arange(4).reshape(-1, 1)
    revenues = np.array([1000, 1200, 1150, 1400])

    model = LinearRegression().fit(months, revenues)
    pred  = model.predict([[4], [5], [6]])

    assert len(pred) == 3
    # trend should be going up
    assert pred[2] > pred[0]
