# Complete Valuation Assumptions Specification

This file is a root-level document listing all assumptions of the valuation models and engines in this project. For the full detailed specification, please refer to:
👉 [`docs/VALUATION_ASSUMPTIONS.md`](file:///d:/company-valuationi/docs/VALUATION_ASSUMPTIONS.md)

---

## Quick Summary of Methodologies & Core Assumptions

| Methodology | Applicable Sectors | Key Baseline Assumptions | Veto Conditions |
| :--- | :--- | :--- | :--- |
| **1. FCFF DCF** | Non-financial (IT, FMCG, Auto, EPC, Pharma) | 5-yr forecast, 25% NOPAT reinvestment (Capex + NWC), sector WACC (9.0%-11.0%), terminal growth $g=4\%$, $WACC > g + 2\%$ floor. | Vetoed for Banks & NBFCs (debt is operational inventory). |
| **2. DDM** | Banks & NBFCs, High Dividend Corporates | Flat 35% dividend payout ratio, single-stage Gordon growth, $K_e = WACC + 1.5\%$, $K_e > g + 3\%$ constraint. | Vetoed if Payout Ratio $< 10\%$. |
| **3. Residual Income** | Banks & NBFCs | Book equity baseline, 80% earnings retention, ROE anchor (15%), 5-yr forecast + 6% RI terminal growth. | Vetoed for asset-light sectors (IT, FMCG, Pharma). |
| **4. P/E Relative** | All positive EPS companies | Sector target multiples (18x-40x), justified P/E formula $\frac{\text{Payout} \cdot (1+g)}{K_e - g}$. | Invalidated if EPS $\le 0$. |
| **5. Justified P/B** | Banks & NBFCs | Justified P/B formula $\frac{ROE - g}{K_e - g}$, ROE clamped [5%, 30%], Multiple clamped [0.8x, 4.5x]. | Vetoed for asset-light companies. |
| **6. EV/EBITDA** | Capital-intensive / Consumer / Pharma | Target multiples (11x-26x), EBITDA proxied as 22% of revenue if missing. Net Debt bridge ($EV - Net Debt$). | Vetoed for Banks & NBFCs. |
| **7. EV/EBIT** | Asset-light services & Healthcare | Target multiple $1.2 \times$ EV/EBITDA multiple (default 18x), EBIT proxied as 18% of revenue if missing. | Vetoed for Banks & NBFCs. |

---

## Engine-Level Assumptions

1. **Multi-Scenario Parameters**:
   - **Downside (Bear)**: Revenue growth $-30\%$, Operating margin $-15\%$, WACC $+1.5\%$, Multiples $-20\%$ (**Weight: 25%**).
   - **Base Case**: Baseline parameters (**Weight: 50%**).
   - **Upside (Bull)**: Revenue growth $+30\%$, Operating margin $+15\%$, WACC $-1.0\%$, Multiples $+20\%$ (**Weight: 25%**).

2. **Sensitivity Matrix**: $5 \times 5$ surface varying WACC ($\pm 1.0\%$) vs Terminal Growth ($\pm 1.0\%$).

3. **Ensemble Quantiles & Mispricing**:
   - Percentiles: $Q10, Q25, Q50, Q75, Q90$.
   - Mispricing % = $(Q50 / \text{Market Price}) - 1$.
   - Undervalued: $M \ge +15\%$ ($< Q25$). Strongly Undervalued: $M \ge +30\%$ ($< Q10$).
   - Overvalued: $M \le -15\%$ ($> Q75$). Strongly Overvalued: $M \le -30\%$ ($> Q90$).
   - Inconclusive: $Q90/Q10 > 3.0$ or missing data.

4. **Neural Network Optimizer**: 12-dim input $\rightarrow$ 32 ReLU $\rightarrow$ 16 ReLU $\rightarrow$ 7 Softmax output with sector masking (non-eligible methods logits set to $-10^9$).

5. **Data Staleness & TTL**: 24-hour TTL for market prices; 90-day TTL for financial statement disclosures.

For full equation derivations, sector breakdown, and source code map, see [`docs/VALUATION_ASSUMPTIONS.md`](file:///d:/company-valuationi/docs/VALUATION_ASSUMPTIONS.md).
