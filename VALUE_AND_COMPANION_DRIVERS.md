# Value Drivers and Companion Drivers Specification

This file provides a root-level reference for **Value Drivers** and **Companion Drivers** in this project. For the full detailed specification document, see:
👉 [`docs/VALUE_AND_COMPANION_DRIVERS.md`](file:///d:/company-valuationi/docs/VALUE_AND_COMPANION_DRIVERS.md)

---

## Quick Summary

- **Value Drivers**: The underlying financial and operational metrics (e.g., Revenue Growth, Operating Margin, ROE, ROIC, WACC) that directly drive cash flows and intrinsic value in DCF and Residual Income models.
- **Companion Drivers**: The single fundamental financial metric that mathematically dictates a specific relative valuation multiple:
  - **P/B Multiple** $\rightarrow$ Companion Driver: **Return on Equity (ROE)** ($\text{Justified P/B} = \frac{\text{ROE} - g}{K_e - g}$)
  - **P/E Multiple** $\rightarrow$ Companion Driver: **ROE & Earnings Growth ($g$)** ($\text{Justified P/E} = \frac{\text{Payout} \cdot (1+g)}{K_e - g}$)
  - **EV/EBITDA Multiple** $\rightarrow$ Companion Driver: **ROIC & Reinvestment Rate**
  - **EV/Sales Multiple** $\rightarrow$ Companion Driver: **Operating Margin** ($\text{EV/Sales} = \text{Operating Margin} \cdot \text{EV/EBIT}$)

For sector-specific driver mappings and factor attribution formulas, see [`docs/VALUE_AND_COMPANION_DRIVERS.md`](file:///d:/company-valuationi/docs/VALUE_AND_COMPANION_DRIVERS.md).
