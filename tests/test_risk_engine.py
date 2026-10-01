"""
Unit Tests for Dynamic Risk-Score Engine
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.risk_calculator import RiskCalculator

def test_risk_calculator_bounds():
    calc = RiskCalculator()
    result = calc.compute_risk(1.0, 1.0, 100.0, 20, 1, 10)
    assert 0.0 <= result["risk_score"] <= 100.0
    assert result["risk_level"] == "CRITICAL (Red)"
    print("[SUCCESS] Risk Engine boundary unit test passed!")

if __name__ == "__main__":
    test_risk_calculator_bounds()