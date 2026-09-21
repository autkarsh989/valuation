"""
Two-Layer Classification Engine and Method Eligibility Resolver.
Implements Layer A (User-facing classification) and Layer B (Internal valuation attributes),
as well as deterministic method eligibility and veto rules.
"""

from typing import Dict, Any, List

def resolve_classification_and_eligibility(company_master: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates internal company attributes and resolves eligible valuation methods and vetoes.
    """
    sector = company_master.get("sector", "")
    financial_nature = company_master.get("financial_nature", "")
    structure_type = company_master.get("structure_type", "")

    eligible_methods = []
    vetoed_methods = []

    # Sector Pack Rules & Veto Logic
    if financial_nature == "Financial" or sector == "Banks & NBFCs":
        eligible_methods = ["P/B", "Residual Income", "DDM"]
        vetoed_methods = [
            {
                "method": "EV/EBITDA",
                "reason": "VETO: Bank/NBFC deposits & borrowings are operating liabilities, making conventional Enterprise Value and EBITDA undefined/misleading."
            },
            {
                "method": "EV/EBIT",
                "reason": "VETO: Financial company operating income includes interest margin, invalidating EV/EBIT."
            },
            {
                "method": "FCFF DCF",
                "reason": "VETO: Free Cash Flow to Firm cannot isolate operating cash flow from financial lending activities for banks."
            }
        ]
        # NBFCs can additionally support P/E if non-deposit taking
        if "NBFC" in company_master.get("subsector", ""):
            eligible_methods.append("P/E")

    elif sector == "IT Services":
        eligible_methods = ["FCFF DCF", "P/E", "EV/EBIT"]
        vetoed_methods = [
            {
                "method": "P/B",
                "reason": "VETO/LOW WEIGHT: IT services companies are asset-light; book value does not reflect intellectual property or human capital value."
            },
            {
                "method": "Residual Income",
                "reason": "VETO: Accounting equity is minimal for asset-light software services."
            }
        ]

    elif sector == "FMCG / Consumer":
        eligible_methods = ["FCFF DCF", "P/E", "EV/EBITDA"]
        if structure_type == "SOTP candidate":
            eligible_methods.append("SOTP")
        vetoed_methods = [
            {
                "method": "Residual Income",
                "reason": "VETO: Consumer brand franchise value is not reflected on balance sheet book equity."
            }
        ]

    elif sector == "Manufacturing / Auto":
        eligible_methods = ["FCFF DCF", "P/E", "EV/EBITDA"]
        if structure_type == "SOTP candidate":
            eligible_methods.append("SOTP")
        vetoed_methods = [
            {
                "method": "Residual Income",
                "reason": "VETO: Industrial capital intensity requires EV/EBITDA and DCF framework."
            }
        ]

    elif sector == "Infrastructure / EPC":
        eligible_methods = ["FCFF DCF", "EV/EBITDA", "P/E"]
        if structure_type == "SOTP candidate":
            eligible_methods.append("SOTP")
        vetoed_methods = [
            {
                "method": "Residual Income",
                "reason": "VETO: Order book cash flows and project debt require project-level EV frameworks."
            }
        ]

    elif sector == "Pharmaceuticals":
        eligible_methods = ["FCFF DCF", "P/E", "EV/EBITDA"]
        if structure_type == "SOTP candidate":
            eligible_methods.append("SOTP")
        vetoed_methods = [
            {
                "method": "Residual Income",
                "reason": "VETO: R&D pipeline value is not captured in historical accounting book equity."
            }
        ]

    else:
        # Default non-financial fallback
        eligible_methods = ["FCFF DCF", "P/E", "EV/EBITDA"]
        vetoed_methods = []

    return {
        "company_id": company_master.get("company_id"),
        "layer_a": {
            "listing_status": company_master.get("listing_status"),
            "market_cap_class": company_master.get("market_cap_class"),
            "sector": company_master.get("sector"),
            "subsector": company_master.get("subsector"),
        },
        "layer_b": {
            "financial_nature": company_master.get("financial_nature"),
            "lifecycle": company_master.get("lifecycle"),
            "business_model": company_master.get("business_model"),
            "asset_intensity": company_master.get("asset_intensity"),
            "structure_type": company_master.get("structure_type"),
            "regulatory_model": company_master.get("regulatory_model"),
        },
        "eligible_methods": eligible_methods,
        "vetoed_methods": vetoed_methods
    }
