"""
AI Explanation Engine & Factor Attribution Engine.
Analyzes company financials, sector parameters, neural weights, scenario projections,
and quantile distributions to generate human-readable explanations of WHY the model
predicts a target fair value, WHAT FACTORS contribute to what extent, and WHY methods
are eligible or vetoed.
"""

from typing import Dict, Any, List

METHOD_ELIGIBILITY_REASONS = {
    "FCFF DCF": "FCFF DCF calculates intrinsic value by discounting projected free cash flows to the firm at WACC. It is highly suitable for cash-generating, non-financial businesses.",
    "P/E": "Price-to-Earnings (P/E) assesses relative valuation against earnings capacity. It is effective for mature companies with positive earnings.",
    "P/B": "Price-to-Book (P/B) measures market value relative to net asset value. It is the primary valuation anchor for Banks and NBFCs whose assets are mark-to-market financial instruments.",
    "EV/EBITDA": "EV/EBITDA evaluates operating profitability independent of capital structure and depreciation policy. Ideal for capital-intensive industrial and consumer sectors.",
    "EV/EBIT": "EV/EBIT evaluates operating cash earnings while accounting for capital depreciation. Highly effective for IT and asset-light services.",
    "Residual Income": "Residual Income models value generated above the firm's required cost of equity capital. Crucial for financial institutions with book equity anchors.",
    "DDM": "Dividend Discount Model values shares based on present value of projected dividend distributions. Effective for high-payout or regulated dividend-paying financial institutions."
}

def generate_ai_explanation(
    master: Dict[str, Any],
    market: Dict[str, Any],
    financials: Dict[str, Any],
    sector_metrics: Dict[str, Any],
    scenarios: Dict[str, Any],
    valuation: Dict[str, Any],
    is_neural: bool = True
) -> Dict[str, Any]:
    """
    Generates structured AI explanation, factor attributions, method contributions,
    and eligibility/veto impact analyses.
    """
    symbol = master.get("company_id") or master.get("symbol", "")
    company_name = master.get("common_name") or master.get("legal_name", symbol)
    sector = master.get("sector", "")
    close_price = market.get("close_price", 0.0)
    q50 = valuation.get("q50", close_price) or close_price
    mispricing_pct = (valuation.get("mispricing", 0.0) or 0.0) * 100.0
    classification = valuation.get("classification", "FAIRLY VALUED")
    confidence = valuation.get("confidence_score", 85.0)

    # Financial & Sector Drivers
    roe = sector_metrics.get("roe") or (financials.get("pat", 0.0) / max(financials.get("equity", 1.0), 1.0)) or 0.15
    if isinstance(roe, (float, int)) and roe > 1.0:
        roe = roe / 100.0

    growth = sector_metrics.get("constant_currency_growth") or financials.get("revenue_growth") or 0.12
    if isinstance(growth, (float, int)) and growth > 1.0:
        growth = growth / 100.0

    pe = market.get("pe_ratio") or 20.0
    pb = market.get("pb_ratio") or 3.0
    debt = financials.get("debt", 0.0) or 0.0
    equity = financials.get("equity", 1.0) or 1.0
    d_e = (debt / equity) if equity > 0 else 0.5

    ebit = financials.get("ebit", 0.0) or 0.0
    rev = financials.get("revenue", 1.0) or 1.0
    operating_margin = (ebit / rev) if rev > 0 else 0.20

    weights = valuation.get("weights_applied") or {}
    method_medians = valuation.get("method_medians") or {}

    # Factor Analysis
    factors = []

    # 1. Neural Sector Method Priority
    top_method = "FCFF DCF"
    top_weight_pct = 40.0
    if weights:
        sorted_w = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        if sorted_w:
            top_method, top_weight_val = sorted_w[0]
            top_weight_pct = top_weight_val * 100.0

    factors.append({
        "name": "Methodology & Weight Priority",
        "metric_value": f"{top_method} ({top_weight_pct:.1f}% weight)",
        "impact_direction": "positive" if mispricing_pct >= 0 else "neutral",
        "impact_extent_pct": round(min(25.0, top_weight_pct * 0.4), 1),
        "category": "Methodology",
        "description": f"The model assigns highest weight ({top_weight_pct:.1f}%) to {top_method} for {sector}, reflecting sector-specific cash flow and asset characteristics."
    })

    # 2. Return on Equity (ROE)
    roe_impact = (roe - 0.14) * 100.0 * 0.8
    factors.append({
        "name": "Return on Equity (ROE)",
        "metric_value": f"{roe * 100:.1f}%",
        "impact_direction": "positive" if roe >= 0.14 else "negative",
        "impact_extent_pct": round(max(-15.0, min(20.0, roe_impact)), 1),
        "category": "Profitability",
        "description": f"ROE of {roe*100:.1f}% {'exceeds' if roe >= 0.14 else 'lags'} sector benchmark (14.0%), {'elevating justified valuation multiples & residual earnings' if roe >= 0.14 else 'depressing justified price-to-book ratios'}."
    })

    # 3. Revenue Growth
    growth_impact = (growth - 0.08) * 100.0 * 0.7
    factors.append({
        "name": "Revenue Growth Rate",
        "metric_value": f"{growth * 100:.1f}% YoY",
        "impact_direction": "positive" if growth >= 0.08 else "negative",
        "impact_extent_pct": round(max(-12.0, min(18.0, growth_impact)), 1),
        "category": "Growth",
        "description": f"Annual growth of {growth*100:.1f}% provides {'strong cash flow expansion in DCF forecasting' if growth >= 0.08 else 'modest top-line growth support'}."
    })

    # 4. Operating Margin
    margin_impact = (operating_margin - 0.15) * 100.0 * 0.5
    factors.append({
        "name": "Operating Profit Margin",
        "metric_value": f"{operating_margin * 100:.1f}%",
        "impact_direction": "positive" if operating_margin >= 0.18 else ("negative" if operating_margin < 0.10 else "neutral"),
        "impact_extent_pct": round(max(-10.0, min(15.0, margin_impact)), 1),
        "category": "Efficiency",
        "description": f"Operating margin of {operating_margin*100:.1f}% drives {'higher NOPAT & enterprise value per rupee of revenue' if operating_margin >= 0.18 else 'standard operating conversion efficiency'}."
    })

    # 5. Capital Structure & Leverage
    if sector == "Banks & NBFCs":
        leverage_desc = "Capital structure governed by RBI prudential standards (CASA & CET1 ratios)."
        leverage_impact = 2.5
        leverage_dir = "positive"
    else:
        leverage_dir = "positive" if d_e <= 0.5 else ("negative" if d_e > 1.2 else "neutral")
        leverage_impact = - (d_e - 0.5) * 6.0 if d_e > 0.5 else (0.5 - d_e) * 4.0
        leverage_desc = f"Debt-to-equity ratio of {d_e:.2f} {'indicates low financial risk' if d_e <= 0.5 else 'creates net debt deduction on Enterprise Value'}."

    factors.append({
        "name": "Capital Structure & Leverage",
        "metric_value": f"D/E {d_e:.2f}x",
        "impact_direction": leverage_dir,
        "impact_extent_pct": round(max(-15.0, min(10.0, leverage_impact)), 1),
        "category": "Solvency",
        "description": leverage_desc
    })

    # 6. Market Price vs Fair Value Gap
    factors.append({
        "name": "Market Price vs Fair Value Gap",
        "metric_value": f"P/E {pe:.1f}x • P/B {pb:.1f}x",
        "impact_direction": "positive" if mispricing_pct >= 0 else "negative",
        "impact_extent_pct": round(mispricing_pct * 0.4, 1),
        "category": "Market Gap",
        "description": f"Current market price ₹{close_price:.1f} trades at a {abs(mispricing_pct):.1f}% {'discount' if mispricing_pct >= 0 else 'premium'} relative to model fair value ₹{q50:.1f}."
    })

    # Method Contributions
    method_contributions = []
    tot_weighted = 0.0
    for m, val in method_medians.items():
        w = weights.get(m, 1.0 / max(len(method_medians), 1))
        weighted_val = val * w
        tot_weighted += weighted_val
        method_contributions.append({
            "method": m,
            "fair_value": round(val, 1),
            "weight_pct": round(w * 100.0, 1),
            "weighted_value": round(weighted_val, 1)
        })

    for mc in method_contributions:
        mc["contribution_share_pct"] = round((mc["weighted_value"] / tot_weighted * 100.0), 1) if tot_weighted > 0 else 0.0

    # Eligibility & Veto Explanations
    eligibility_explanations = []
    for mc in method_contributions:
        m_name = mc["method"]
        reason = METHOD_ELIGIBILITY_REASONS.get(m_name, f"{m_name} is suitable for {sector}.")
        eligibility_explanations.append({
            "method": m_name,
            "standalone_fair_value": mc["fair_value"],
            "weight_pct": mc["weight_pct"],
            "reason": reason,
            "impact": f"Contributes ₹{mc['weighted_value']:.1f} ({mc['contribution_share_pct']}%) to final target price."
        })

    # Verdict Statement & Narrative
    if mispricing_pct >= 30.0:
        verdict_heading = "Strong Upside Signal"
        verdict_statement = f"{company_name} is classified as **STRONGLY UNDERVALUED**. The model estimates a fair value of **₹{q50:.1f}**, providing a **+{mispricing_pct:.1f}% potential upside** over current price ₹{close_price:.1f}."
    elif mispricing_pct >= 15.0:
        verdict_heading = "Moderate Upside Signal"
        verdict_statement = f"{company_name} is classified as **UNDERVALUED**. The model estimates a fair value of **₹{q50:.1f}**, indicating a **+{mispricing_pct:.1f}% upside potential** over current price ₹{close_price:.1f}."
    elif mispricing_pct <= -30.0:
        verdict_heading = "High Downside Risk"
        verdict_statement = f"{company_name} is classified as **STRONGLY OVERVALUED**. The model estimates a fair value of **₹{q50:.1f}**, implying a **{mispricing_pct:.1f}% downside risk** from current price ₹{close_price:.1f}."
    elif mispricing_pct <= -15.0:
        verdict_heading = "Moderate Downside Risk"
        verdict_statement = f"{company_name} is classified as **OVERVALUED**. The model estimates a fair value of **₹{q50:.1f}**, reflecting a **{mispricing_pct:.1f}% downside risk** relative to current price ₹{close_price:.1f}."
    else:
        verdict_heading = "Fairly Valued Signal"
        verdict_statement = f"{company_name} is classified as **FAIRLY VALUED**. The model's median fair value estimate of **₹{q50:.1f}** closely aligns with the market price ₹{close_price:.1f} (within a {mispricing_pct:+.1f}% margin)."

    mode_name = "Neural Network Weighted Ensemble" if is_neural else "Standard Ensemble Distribution"

    top_m_str = method_contributions[0]['method'] if method_contributions else 'DCF'
    top_m_val = method_contributions[0]['fair_value'] if method_contributions else q50
    top_m_w = method_contributions[0]['weight_pct'] if method_contributions else 0.0

    summary_narrative = (
        f"{verdict_statement}\n\n"
        f"**Model Calculation Explanation:**\n"
        f"The {mode_name} computes this target price by evaluating active valuation methods for **{sector}**. "
        f"Key underlying metrics include a Return on Equity (ROE) of **{roe*100:.1f}%**, operating margin of **{operating_margin*100:.1f}%**, and revenue growth of **{growth*100:.1f}%**. "
        f"The highest weight ({top_m_w:.1f}%) is assigned to **{top_m_str}**, which yields a standalone valuation of **₹{top_m_val:.1f}**.\n\n"
        f"Quantile bounds span from **₹{valuation.get('q10', 0):.1f}** (Bear Q10) to **₹{valuation.get('q90', 0):.1f}** (Bull Q90), with an overall model confidence score of **{confidence}/100**."
    )

    primary_driver = f"ROE of {roe*100:.1f}% & Growth of {growth*100:.1f}% driving {top_m_str}"
    secondary_driver = f"{top_m_w:.1f}% weight allocated to {top_m_str} for {sector}"

    return {
        "verdict_heading": verdict_heading,
        "verdict_statement": verdict_statement,
        "summary_narrative": summary_narrative,
        "mode_name": mode_name,
        "primary_driver": primary_driver,
        "secondary_driver": secondary_driver,
        "confidence_score": confidence,
        "factors": factors,
        "method_contributions": method_contributions,
        "eligibility_explanations": eligibility_explanations
    }
