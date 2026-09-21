"""
Valuation Service Orchestrator.
Coordinates data fetching, classification, valuation models, scenarios, and ensemble outputs.
"""

from typing import Dict, Any, List
import logging
from src.company_universe import COMPANIES_20, get_company_by_symbol
from src.database import (
    get_company_full_record, get_all_company_summaries
)
from src.data_fetcher import fetch_and_store_company_data, fetch_all_companies_data
from src.classification import resolve_classification_and_eligibility
from src.valuation_models import run_scenarios_for_company, generate_sensitivity_matrix
from src.ensemble_engine import compute_ensemble_valuation

logger = logging.getLogger("valuation_service")

def run_valuation_for_company(symbol: str, force_refresh: bool = False) -> Dict[str, Any]:
    """
    Complete pipeline for a single company:
    1. Fetch live market/financial data
    2. Resolve classification & method eligibility
    3. Run scenario models
    4. Compute sensitivity matrix
    5. Compute ensemble distribution & classification
    """
    # Step 1: Data Acquisition
    fetch_and_store_company_data(symbol, force_refresh=force_refresh)
    record = get_company_full_record(symbol)

    master = record.get("master", {})
    market = record.get("market", {})
    fin = record.get("financials", {})
    sm = record.get("sector_metrics", {})

    if not master or not market:
        raise ValueError(f"Failed to retrieve database record for company {symbol}")

    # Step 2: Classification & Veto Resolution
    eligibility = resolve_classification_and_eligibility(master)
    active_methods = eligibility.get("eligible_methods", [])
    vetoed_methods = eligibility.get("vetoed_methods", [])

    # Step 3: Run Multi-Scenario Valuation Calculators
    scenarios = run_scenarios_for_company(
        eligible_methods=active_methods,
        financials=fin,
        market_data=market,
        sector_metrics=sm,
        sector_name=master.get("sector", "")
    )

    # Step 4: Sensitivity Matrix
    market_price = market.get("close_price", 0.0)
    sensitivity = generate_sensitivity_matrix(fin, market)

    # Step 5: Ensemble Quantiles & Final Valuation Status
    ensemble = compute_ensemble_valuation(
        company_id=symbol,
        market_price=market_price,
        scenario_results=scenarios,
        vetoed_methods=vetoed_methods
    )

    return {
        "company": master,
        "market": market,
        "financials": fin,
        "sector_metrics": sm,
        "classification_layers": {
            "layer_a": eligibility["layer_a"],
            "layer_b": eligibility["layer_b"],
        },
        "eligible_methods": active_methods,
        "vetoed_methods": vetoed_methods,
        "scenarios": scenarios,
        "sensitivity": sensitivity,
        "valuation": ensemble
    }

def run_valuation_for_all(force_refresh: bool = False) -> List[Dict[str, Any]]:
    """
    Runs the full valuation pipeline for all 20 companies in the universe.
    """
    logger.info("Starting bulk valuation pipeline for 20 companies...")
    for comp in COMPANIES_20:
        sym = comp["symbol"]
        try:
            run_valuation_for_company(sym, force_refresh=force_refresh)
        except Exception as e:
            logger.error(f"Error running valuation for {sym}: {e}")
    return get_all_company_summaries()
