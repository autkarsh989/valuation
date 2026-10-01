# Value Drivers and Companion Drivers Specification

This document provides a complete guide to **Value Drivers** and **Companion Drivers** (also known as *Companion Variables*) within corporate valuation, relative pricing multiples, and the calculation/attribution engines implemented in this project (`src/valuation_models.py`, `src/classification.py`, and `src/explanation_engine.py`).

---

## 🎯 1. Fundamental Definitions

- **Value Drivers**: The underlying operational and financial variables that directly determine a company's cash flow generation, top-line expansion, profit margins, capital efficiency, and discount rate in an **intrinsic valuation** model (such as FCFF Discounted Cash Flow or Residual Income).
- **Companion Drivers (Companion Variables)**: In **relative valuation multiples** (P/E, P/B, EV/EBITDA, EV/Sales), the *companion driver* is the single fundamental variable that has the strongest mathematical correlation with that specific multiple. Every valuation multiple is governed primarily by one companion driver.

---

## 🧮 2. Valuation Multiples & Their Companion Drivers

When comparing valuation multiples across peer companies or industry benchmarks, comparing the multiple in isolation leads to incomplete or misleading conclusions. Instead, every valuation multiple must be evaluated alongside its **companion driver**:

| Valuation Multiple | Primary Companion Driver | Mathematical Justification / Formula | Key Valuation Takeaway |
| :--- | :--- | :--- | :--- |
| **Price-to-Book (P/B)** | **Return on Equity (ROE)** | $$\text{Justified P/B} = \frac{\text{ROE} - g}{K_e - g}$$ | A high P/B is only justified if $\text{ROE} > K_e$ (Cost of Equity). If $\text{ROE} < K_e$, the company should trade below book value. |
| **Price-to-Earnings (P/E)** | **ROE & Expected Growth ($g$)** | $$\text{Justified P/E} = \frac{\text{Payout Ratio} \cdot (1 + g)}{K_e - g}$$ | Higher ROE enables higher growth for a given dividend payout ratio, justifying a higher P/E multiple. |
| **EV / EBITDA** | **ROIC & Reinvestment Rate** | $$\text{Justified EV/EBITDA} = \frac{(1 - t) \cdot (1 - \text{Reinvestment Rate})}{\text{WACC} - g}$$ | High Return on Invested Capital (ROIC) requires less capital reinvestment to sustain growth, expanding the EV/EBITDA multiple. |
| **EV / EBIT** | **ROIC & Tax Rate** | $$\text{Justified EV/EBIT} = \frac{(1 - t) \cdot (1 - \text{Reinvestment Rate})}{\text{WACC} - g}$$ | Accounts for capital depreciation policies; driven by tax efficiency and operating asset return. |
| **EV / Sales** | **Operating Margin (EBIT Margin)** | $$\text{EV/Sales} = \text{Operating Margin} \cdot \text{EV/EBIT}$$ | A company with a 25% operating margin should trade at a significantly higher EV/Sales multiple than one with a 5% margin. |

---

## 📊 3. Core Intrinsic Value Drivers

Across Discounted Cash Flow (DCF) and Residual Income models implemented in [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py), five primary **Value Drivers** dictate Enterprise Value and Equity Value:

1. **Revenue Growth Rate ($g_{\text{rev}}$)**: Drives top-line compounding over the 5-year explicit forecast horizon and terminal cash flows.
2. **Operating Profit Margin (EBIT / EBITDA Margin)**: Determines how much revenue converts into NOPAT ($\text{NOPAT} = \text{EBIT} \times (1 - t)$).
3. **Return on Invested Capital / Equity (ROIC / ROE)**: Measures capital allocation efficiency. High ROE/ROIC creates economic value added over cost of capital.
4. **Reinvestment & Cash Flow Conversion Rate**: The percentage of NOPAT required for Capex and Net Working Capital ($\Delta \text{NWC}$). In this system, $\text{FCFF} = \text{NOPAT} \times 0.75$ (assumes 25% reinvestment).
5. **Weighted Average Cost of Capital (WACC) / Cost of Equity ($K_e$)**: The hurdle rate used to discount future cash flows, reflecting leverage, market beta, and risk profiles.

---

## 🏢 4. Sector-Specific Value Drivers in this Project

Different business models rely on distinct sector-specific operational value drivers stored in `sector_metrics` (`src/company_universe.py`):

| Sector Pack | Primary Sector-Specific Value Drivers | Role in Valuation Pipeline |
| :--- | :--- | :--- |
| **Banks & NBFCs** | Net Interest Margin (NIM), GNPA/NNPA ratios, CASA ratio, Provision Coverage, CET1 ratio | Drives ROE in P/B and Residual Income models ($\text{RI} = \text{PAT} - K_e \cdot \text{Equity}$). |
| **IT Services** | Constant Currency (CC) Growth, Employee Utilisation, Attrition Rate, Deal Bookings | Predicts revenue growth durability and operating margin retention in FCFF DCF and EV/EBIT. |
| **FMCG / Consumer** | Volume Growth vs. Price/Mix, Gross Margin, Ad/Marketing Spend, Working Capital Days | Anchors long-term cash flow predictability and premium P/E / EV/EBITDA multiples. |
| **Manufacturing / Auto** | Sales Volume, Average Selling Price (ASP), Capacity Utilisation, Commodity Input Costs | Drives cyclical earnings normalization and EV/EBITDA target multiples. |
| **Infrastructure / EPC** | Order Book Value, Order Inflow, Order-to-Revenue Ratio, Execution Rate, Receivable Aging | Determines revenue visibility and project-level cash flow conversion. |
| **Pharmaceuticals** | R&D Spend (% of Rev), US Pipeline Approvals, Price Erosion, Regulatory Observations | Dictates terminal growth assumptions and risk-adjusted scenario probabilities. |

---

## ⚙️ 5. Attribution Engine Factor Drivers (`src/explanation_engine.py`)

In the automated narrative and attribution engine, the platform quantifies fair-value impact ($\pm\%$) across **6 quantified factor drivers**:

1. **Neural Sector Weight Priority**: Explains why the system favors DCF for industrials or P/B for banks ($\text{Impact}_{\text{Method}} = \min(25\%, W_{\text{top}} \times 40\%)$).
2. **ROE Impact Driver**: Quantifies equity value creation above baseline ($\text{Impact}_{\text{ROE}} = (\text{ROE} - 14\%) \times 0.8$).
3. **Revenue Growth Rate Driver**: Quantifies top-line expansion contribution ($\text{Impact}_{\text{Growth}} = (g_{\text{rev}} - 8\%) \times 0.7$).
4. **Operating Profit Margin Driver**: Quantifies operational efficiency ($\text{Impact}_{\text{Margin}} = (\text{Margin}_{\text{op}} - 15\%) \times 0.5$).
5. **Capital Structure / Leverage Driver**: Penalizes excessive debt-to-equity ($D/E > 0.5$) or evaluates bank CET1 ratios.
6. **Market Valuation Gap Driver**: Measures current market mispricing vs. median target fair value ($Q_{50}$).

---

## 📍 6. Codebase Mapping

| System Component | File Reference | Primary Functions / Classes |
| :--- | :--- | :--- |
| **Valuation Models & Multiples** | [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py) | `ValuationEngine.calculate_dcf`, `calculate_pb`, `calculate_pe`, `calculate_residual_income` |
| **Two-Layer Veto Resolver** | [`src/classification.py`](file:///d:/company-valuationi/src/classification.py) | `resolve_method_eligibility` |
| **Attribution & Narrative Engine** | [`src/explanation_engine.py`](file:///d:/company-valuationi/src/explanation_engine.py) | `generate_valuation_explanation`, `compute_attribution_factors` |
| **Neural Method Weighting** | [`src/neural_weight_engine.py`](file:///d:/company-valuationi/src/neural_weight_engine.py) | `NeuralWeightOptimizer`, `DEFAULT_SECTOR_WEIGHTS` |
