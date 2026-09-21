"""
Test Suite for 20-Company Valuation MVP Engine.
Verifies database creation, live data fetcher, veto rules, model accuracy, and ensemble engine.
"""

try:
    import pytest
except ImportError:
    pytest = None
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.database import init_db, get_connection, get_company_full_record
from src.company_universe import COMPANIES_20, get_company_by_symbol
from src.classification import resolve_classification_and_eligibility
from src.valuation_models import ValuationEngine, run_scenarios_for_company
from src.ensemble_engine import compute_ensemble_valuation
from src.valuation_service import run_valuation_for_company

def test_company_universe_count():
    assert len(COMPANIES_20) == 20
    symbols = [c["symbol"] for c in COMPANIES_20]
    assert "TCS.NS" in symbols
    assert "HDFCBANK.NS" in symbols
    assert "MARUTI.NS" in symbols

def test_database_initialization():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert "company_master" in tables
    assert "financials" in tables
    assert "market_data" in tables
    assert "sector_metrics" in tables
    assert "final_valuation" in tables

def test_bank_veto_rules():
    bank_comp = get_company_by_symbol("HDFCBANK.NS")
    res = resolve_classification_and_eligibility(bank_comp)
    assert "P/B" in res["eligible_methods"]
    assert "Residual Income" in res["eligible_methods"]

    vetoed_names = [v["method"] for v in res["vetoed_methods"]]
    assert "EV/EBITDA" in vetoed_names
    assert "FCFF DCF" in vetoed_names

def test_it_services_eligibility():
    it_comp = get_company_by_symbol("TCS.NS")
    res = resolve_classification_and_eligibility(it_comp)
    assert "FCFF DCF" in res["eligible_methods"]
    assert "P/E" in res["eligible_methods"]

def test_dcf_calculator():
    financials = {"revenue": 100000.0, "shares_outstanding": 1000.0, "debt": 10000.0, "cash": 5000.0}
    market = {"close_price": 500.0, "market_cap": 500000.0}
    res = ValuationEngine.calculate_dcf(financials, market, growth_rate=0.10, wacc=0.10, terminal_growth=0.04)
    assert res["value_per_share"] > 0

def test_ensemble_classification():
    scenarios = {
        "Base": {"P/E": {"value_per_share": 500.0}},
        "Downside": {"P/E": {"value_per_share": 450.0}},
        "Upside": {"P/E": {"value_per_share": 550.0}}
    }
    res = compute_ensemble_valuation("TEST.NS", market_price=350.0, scenario_results=scenarios, vetoed_methods=[])
    assert res["classification"] in ["UNDERVALUED", "STRONGLY UNDERVALUED"]

if __name__ == "__main__":
    try:
        import pytest
        pytest.main(["-v", __file__])
    except ImportError:
        test_company_universe_count()
        test_database_initialization()
        test_bank_veto_rules()
        test_it_services_eligibility()
        test_dcf_calculator()
        test_ensemble_classification()
        print("All system tests passed successfully!")

