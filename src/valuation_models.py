"""
Core Valuation Calculators & Scenario Engine.
Implements FCFF DCF, P/E, P/B, Residual Income, EV/EBITDA, EV/EBIT, and DDM models.
Provides multi-scenario modeling (Downside, Base, Upside) and sensitivity matrices.
"""

from typing import Dict, Any, List
import math

class ValuationEngine:
    @staticmethod
    def calculate_dcf(
        financials: Dict[str, Any],
        market_data: Dict[str, Any],
        growth_rate: float = 0.10,
        ebit_margin: float = 0.20,
        tax_rate: float = 0.25,
        wacc: float = 0.105,
        terminal_growth: float = 0.04,
        forecast_years: int = 5
    ) -> Dict[str, Any]:
        """
        FCFF DCF Model
        """
        base_rev = financials.get("revenue", 0.0) or (market_data.get("market_cap", 0.0) * 0.3)
        shares = financials.get("shares_outstanding", 0.0) or (market_data.get("market_cap", 1.0) / max(market_data.get("close_price", 1.0), 1.0))
        net_debt = (financials.get("debt", 0.0) - financials.get("cash", 0.0))

        if base_rev <= 0 or shares <= 0:
            return {"enterprise_value": 0, "equity_value": 0, "value_per_share": 0, "status": "Invalid inputs"}

        pv_fcff_sum = 0.0
        current_rev = base_rev

        for yr in range(1, forecast_years + 1):
            current_rev *= (1 + growth_rate)
            ebit = current_rev * ebit_margin
            nopat = ebit * (1 - tax_rate)
            # Reinvestment assumption (Capex & WC ~ 25% of NOPAT)
            fcff = nopat * 0.75
            discount_factor = (1 + wacc) ** yr
            pv_fcff_sum += fcff / discount_factor

        # Terminal value
        terminal_fcff = fcff * (1 + terminal_growth)
        if wacc <= terminal_growth:
            wacc = terminal_growth + 0.02

        terminal_value = terminal_fcff / (wacc - terminal_growth)
        pv_terminal_value = terminal_value / ((1 + wacc) ** forecast_years)

        enterprise_value = pv_fcff_sum + pv_terminal_value
        equity_value = enterprise_value - net_debt
        value_per_share = max(0.0, equity_value / shares)

        return {
            "method": "FCFF DCF",
            "enterprise_value": enterprise_value,
            "equity_value": equity_value,
            "value_per_share": value_per_share,
            "inputs": {
                "growth_rate": growth_rate,
                "ebit_margin": ebit_margin,
                "wacc": wacc,
                "terminal_growth": terminal_growth
            }
        }

    @staticmethod
    def calculate_pe(
        financials: Dict[str, Any],
        market_data: Dict[str, Any],
        target_pe: float = 22.0
    ) -> Dict[str, Any]:
        """
        P/E Relative Valuation Model
        """
        eps = financials.get("eps") or market_data.get("eps")
        price = market_data.get("close_price", 0.0)
        current_pe = market_data.get("pe_ratio", 0.0)

        if not eps or eps <= 0:
            if price > 0 and current_pe > 0:
                eps = price / current_pe
            else:
                eps = (financials.get("pat", 0.0) / max(financials.get("shares_outstanding", 1.0), 1.0))

        if eps <= 0:
            return {"equity_value": 0, "value_per_share": 0, "status": "Negative EPS"}

        value_per_share = eps * target_pe
        shares = financials.get("shares_outstanding", 1.0) or (market_data.get("market_cap", 1.0) / max(price, 1.0))
        equity_value = value_per_share * shares

        return {
            "method": "P/E",
            "equity_value": equity_value,
            "value_per_share": value_per_share,
            "inputs": {"eps": eps, "target_pe": target_pe}
        }

    @staticmethod
    def calculate_pb(
        financials: Dict[str, Any],
        market_data: Dict[str, Any],
        sector_metrics: Dict[str, Any],
        cost_of_equity: float = 0.12,
        growth_rate: float = 0.08
    ) -> Dict[str, Any]:
        """
        P/B Valuation Model (Primary for Financials/Banks)
        """
        shares = financials.get("shares_outstanding", 1.0) or (market_data.get("market_cap", 1.0) / max(market_data.get("close_price", 1.0), 1.0))
        equity = financials.get("equity", 0.0)
        bvps = (equity / shares) if shares > 0 and equity > 0 else 0.0

        if bvps <= 0 and market_data.get("close_price", 0) > 0 and market_data.get("pb_ratio", 0) > 0:
            bvps = market_data["close_price"] / market_data["pb_ratio"]

        roe = sector_metrics.get("roe") or (financials.get("pat", 0.0) / max(equity, 1.0)) or 0.15
        roe = max(0.05, min(roe, 0.30))

        if cost_of_equity <= growth_rate:
            cost_of_equity = growth_rate + 0.03

        # Theoretical Justified P/B = (ROE - g) / (Ke - g)
        justified_pb = (roe - growth_rate) / (cost_of_equity - growth_rate)
        justified_pb = max(0.8, min(justified_pb, 4.5))

        value_per_share = bvps * justified_pb
        equity_value = value_per_share * shares

        return {
            "method": "P/B",
            "equity_value": equity_value,
            "value_per_share": value_per_share,
            "inputs": {"bvps": bvps, "roe": roe, "justified_pb": justified_pb, "cost_of_equity": cost_of_equity}
        }

    @staticmethod
    def calculate_residual_income(
        financials: Dict[str, Any],
        market_data: Dict[str, Any],
        sector_metrics: Dict[str, Any],
        cost_of_equity: float = 0.12,
        growth_rate: float = 0.06,
        forecast_years: int = 5
    ) -> Dict[str, Any]:
        """
        Residual Income Valuation Model (Primary for Financials/Banks)
        """
        shares = financials.get("shares_outstanding", 1.0) or (market_data.get("market_cap", 1.0) / max(market_data.get("close_price", 1.0), 1.0))
        equity = financials.get("equity", 0.0)
        if equity <= 0 and market_data.get("market_cap", 0) > 0 and market_data.get("pb_ratio", 0) > 0:
            equity = market_data["market_cap"] / market_data["pb_ratio"]

        bvps = (equity / shares) if shares > 0 else 0.0
        roe = sector_metrics.get("roe") or 0.15

        pv_ri_sum = 0.0
        curr_bvps = bvps

        for yr in range(1, forecast_years + 1):
            expected_ni = curr_bvps * roe
            equity_charge = curr_bvps * cost_of_equity
            ri = expected_ni - equity_charge
            pv_ri_sum += ri / ((1 + cost_of_equity) ** yr)
            curr_bvps += (expected_ni * (1 - 0.20)) # Retained earnings

        # Terminal Residual Income
        terminal_ri = ri * (1 + growth_rate)
        if cost_of_equity <= growth_rate:
            cost_of_equity = growth_rate + 0.03

        terminal_val = terminal_ri / (cost_of_equity - growth_rate)
        pv_terminal = terminal_val / ((1 + cost_of_equity) ** forecast_years)

        value_per_share = bvps + pv_ri_sum + pv_terminal
        equity_value = value_per_share * shares

        return {
            "method": "Residual Income",
            "equity_value": equity_value,
            "value_per_share": value_per_share,
            "inputs": {"bvps": bvps, "roe": roe, "cost_of_equity": cost_of_equity}
        }

    @staticmethod
    def calculate_ev_ebitda(
        financials: Dict[str, Any],
        market_data: Dict[str, Any],
        target_multiple: float = 14.0
    ) -> Dict[str, Any]:
        """
        EV/EBITDA Valuation Model
        """
        ebitda = financials.get("ebitda", 0.0) or (financials.get("revenue", 0.0) * 0.22)
        shares = financials.get("shares_outstanding", 1.0) or (market_data.get("market_cap", 1.0) / max(market_data.get("close_price", 1.0), 1.0))
        net_debt = (financials.get("debt", 0.0) - financials.get("cash", 0.0))

        if ebitda <= 0:
            return {"enterprise_value": 0, "equity_value": 0, "value_per_share": 0, "status": "Negative EBITDA"}

        enterprise_value = ebitda * target_multiple
        equity_value = enterprise_value - net_debt
        value_per_share = max(0.0, equity_value / shares)

        return {
            "method": "EV/EBITDA",
            "enterprise_value": enterprise_value,
            "equity_value": equity_value,
            "value_per_share": value_per_share,
            "inputs": {"ebitda": ebitda, "target_multiple": target_multiple}
        }

    @staticmethod
    def calculate_ev_ebit(
        financials: Dict[str, Any],
        market_data: Dict[str, Any],
        target_multiple: float = 18.0
    ) -> Dict[str, Any]:
        """
        EV/EBIT Valuation Model
        """
        ebit = financials.get("ebit", 0.0) or (financials.get("revenue", 0.0) * 0.18)
        shares = financials.get("shares_outstanding", 1.0) or (market_data.get("market_cap", 1.0) / max(market_data.get("close_price", 1.0), 1.0))
        net_debt = (financials.get("debt", 0.0) - financials.get("cash", 0.0))

        if ebit <= 0:
            return {"enterprise_value": 0, "equity_value": 0, "value_per_share": 0, "status": "Negative EBIT"}

        enterprise_value = ebit * target_multiple
        equity_value = enterprise_value - net_debt
        value_per_share = max(0.0, equity_value / shares)

        return {
            "method": "EV/EBIT",
            "enterprise_value": enterprise_value,
            "equity_value": equity_value,
            "value_per_share": value_per_share,
            "inputs": {"ebit": ebit, "target_multiple": target_multiple}
        }

    @staticmethod
    def calculate_ddm(
        financials: Dict[str, Any],
        market_data: Dict[str, Any],
        cost_of_equity: float = 0.12,
        dividend_growth: float = 0.07,
        payout_ratio: float = 0.35
    ) -> Dict[str, Any]:
        """
        Dividend Discount Model
        """
        eps = financials.get("eps") or market_data.get("eps") or 30.0
        dps = eps * payout_ratio

        if cost_of_equity <= dividend_growth:
            cost_of_equity = dividend_growth + 0.03

        next_dps = dps * (1 + dividend_growth)
        value_per_share = next_dps / (cost_of_equity - dividend_growth)
        shares = financials.get("shares_outstanding", 1.0) or (market_data.get("market_cap", 1.0) / max(market_data.get("close_price", 1.0), 1.0))

        return {
            "method": "DDM",
            "equity_value": value_per_share * shares,
            "value_per_share": value_per_share,
            "inputs": {"dps": dps, "cost_of_equity": cost_of_equity, "dividend_growth": dividend_growth}
        }

def run_scenarios_for_company(
    eligible_methods: List[str],
    financials: Dict[str, Any],
    market_data: Dict[str, Any],
    sector_metrics: Dict[str, Any],
    sector_name: str
) -> Dict[str, Any]:
    """
    Executes Downside, Base, and Upside scenarios for all active eligible valuation methods.
    """
    scenarios = ["Downside", "Base", "Upside"]
    results = {sc: {} for sc in scenarios}

    # Custom sector parameters
    if sector_name == "Banks & NBFCs":
        base_wacc, base_g, base_pe, base_pb, base_ev_ebitda = 0.115, 0.07, 18.0, 2.2, 12.0
    elif sector_name == "IT Services":
        base_wacc, base_g, base_pe, base_pb, base_ev_ebitda = 0.095, 0.04, 25.0, 6.0, 18.0
    elif sector_name == "FMCG / Consumer":
        base_wacc, base_g, base_pe, base_pb, base_ev_ebitda = 0.090, 0.04, 40.0, 8.0, 26.0
    elif sector_name == "Manufacturing / Auto":
        base_wacc, base_g, base_pe, base_pb, base_ev_ebitda = 0.105, 0.04, 22.0, 3.5, 14.0
    elif sector_name == "Infrastructure / EPC":
        base_wacc, base_g, base_pe, base_pb, base_ev_ebitda = 0.110, 0.04, 18.0, 2.0, 11.0
    elif sector_name == "Pharmaceuticals":
        base_wacc, base_g, base_pe, base_pb, base_ev_ebitda = 0.095, 0.04, 26.0, 4.0, 17.0
    else:
        base_wacc, base_g, base_pe, base_pb, base_ev_ebitda = 0.100, 0.04, 20.0, 3.0, 15.0

    scenario_params = {
        "Downside": {"g_mult": 0.7, "margin_mult": 0.85, "wacc_add": 0.015, "multiple_mult": 0.80},
        "Base":     {"g_mult": 1.0, "margin_mult": 1.00, "wacc_add": 0.000, "multiple_mult": 1.00},
        "Upside":   {"g_mult": 1.3, "margin_mult": 1.15, "wacc_add": -0.010, "multiple_mult": 1.20},
    }

    for sc, p in scenario_params.items():
        g = base_g * p["g_mult"]
        wacc = base_wacc + p["wacc_add"]
        ke = wacc + 0.015
        pe_mult = base_pe * p["multiple_mult"]
        ev_ebitda_mult = base_ev_ebitda * p["multiple_mult"]

        if "FCFF DCF" in eligible_methods:
            results[sc]["FCFF DCF"] = ValuationEngine.calculate_dcf(
                financials, market_data, growth_rate=g*2, ebit_margin=0.20*p["margin_mult"], wacc=wacc, terminal_growth=g
            )

        if "P/E" in eligible_methods:
            results[sc]["P/E"] = ValuationEngine.calculate_pe(financials, market_data, target_pe=pe_mult)

        if "P/B" in eligible_methods:
            results[sc]["P/B"] = ValuationEngine.calculate_pb(financials, market_data, sector_metrics, cost_of_equity=ke, growth_rate=g)

        if "Residual Income" in eligible_methods:
            results[sc]["Residual Income"] = ValuationEngine.calculate_residual_income(financials, market_data, sector_metrics, cost_of_equity=ke, growth_rate=g)

        if "EV/EBITDA" in eligible_methods:
            results[sc]["EV/EBITDA"] = ValuationEngine.calculate_ev_ebitda(financials, market_data, target_multiple=ev_ebitda_mult)

        if "EV/EBIT" in eligible_methods:
            results[sc]["EV/EBIT"] = ValuationEngine.calculate_ev_ebit(financials, market_data, target_multiple=ev_ebitda_mult*1.2)

        if "DDM" in eligible_methods:
            results[sc]["DDM"] = ValuationEngine.calculate_ddm(financials, market_data, cost_of_equity=ke, dividend_growth=g)

    return results

def generate_sensitivity_matrix(
    financials: Dict[str, Any],
    market_data: Dict[str, Any],
    base_wacc: float = 0.10,
    base_g: float = 0.04
) -> Dict[str, Any]:
    """
    Generates a 5x5 WACC vs Terminal Growth sensitivity matrix.
    """
    wacc_steps = [base_wacc - 0.01, base_wacc - 0.005, base_wacc, base_wacc + 0.005, base_wacc + 0.01]
    g_steps = [base_g - 0.01, base_g - 0.005, base_g, base_g + 0.005, base_g + 0.01]

    matrix = []
    for w in wacc_steps:
        row = []
        for g in g_steps:
            dcf_res = ValuationEngine.calculate_dcf(financials, market_data, wacc=w, terminal_growth=g)
            row.append(round(dcf_res["value_per_share"], 1))
        matrix.append(row)

    return {
        "wacc_headers": [f"{w*100:.1f}%" for w in wacc_steps],
        "g_headers": [f"{g*100:.1f}%" for g in g_steps],
        "matrix": matrix
    }
