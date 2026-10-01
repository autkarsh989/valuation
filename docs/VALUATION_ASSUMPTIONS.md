# Complete Valuation Assumptions Specification

This document provides a comprehensive, itemized list of all empirical, mathematical, operational, and structural assumptions used across all valuation methodologies and calculation engines implemented in this project (`src/valuation_models.py`, `src/classification.py`, `src/ensemble_engine.py`, and `src/neural_weight_engine.py`).

---

## 📋 1. Methodological Overview & Sector Eligibility Matrix

The valuation platform enforces a **Two-Layer Classification and Veto Resolver** (`src/classification.py`). Not all valuation methodologies are applicable to every sector. The table below lists the active vs. vetoed status and key governing assumptions for each methodology across sector packs:

| Valuation Methodology | Applicable Sectors | Vetoed Sectors | Primary Anchor / Core Rule |
| :--- | :--- | :--- | :--- |
| **1. FCFF DCF** | IT Services, FMCG, Manufacturing/Auto, Infrastructure/EPC, Pharma | Banks & NBFCs | Vetoed for Financials; Debt is operational inventory. Reinvestment assumed at 25% of NOPAT. |
| **2. Dividend Discount Model (DDM)** | Banks & NBFCs, High Dividend Corporates | Payout < 10% | Assumes stable payout ratio (35%) and perpetual dividend growth. |
| **3. Residual Income (RI)** | Banks & NBFCs | Asset-Light Sectors (IT, FMCG, Pharma) | Primary anchor for Financials where Book Value represents earning capacity; 80% earnings retained. |
| **4. P/E Relative Multiple** | All sectors with positive EPS | Negative EPS companies | Relies on sector target multiples or justified P/E derived from growth and Cost of Equity. |
| **5. P/B Justified Multiple** | Banks & NBFCs | Asset-Light Sectors (IT, SaaS) | Driven by Return on Equity (ROE) vs Cost of Equity ($K_e$); multiple clamped between 0.8x and 4.5x. |
| **6. EV/EBITDA Multiple** | FMCG, Manufacturing/Auto, Infrastructure/EPC, Pharma | Banks & NBFCs | Enterprise Value multiple independent of leverage; EBITDA proxied as 22% of revenue if missing. |
| **7. EV/EBIT Multiple** | IT Services, Healthcare, Asset-Light Services | Banks & NBFCs | EBIT multiple accounting for depreciation; target multiple set at $1.2 \times$ EV/EBITDA multiple. |

---

## 🧮 2. Methodology-Specific Valuation Assumptions

### 2.1 Free Cash Flow to Firm (FCFF) DCF Model
*Source File: [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py#L12-L67)*

- **Explicit Forecast Horizon**: Fixed **5-year projection window** ($t = 1, 2, 3, 4, 5$).
- **Revenue Growth Rate ($g_{\text{rev}}$)**: Sector baseline growth rate (default 4.0% to 14.0% depending on sector and scenario).
- **Operating Margin (EBIT Margin)**: Assumed fixed percentage of revenue (default **20.0%**, adjusted by scenario multipliers).
- **Corporate Tax Rate**: Flat tax rate assumption of **25.0%** ($0.25$).
- **Reinvestment Rate (Capex + Working Capital)**:
  - Reinvestment in Capital Expenditure ($\text{Capex}$) and Net Working Capital ($\Delta \text{NWC}$) is assumed to be **25.0% of NOPAT**.
  - **FCFF Formula Assumption**: $\text{FCFF}_t = \text{NOPAT}_t \times (1 - 0.25) = \text{NOPAT}_t \times 0.75$.
- **Cost of Capital (WACC)**: Baseline WACC defined by sector profile (IT: 9.5%, FMCG: 9.0%, Manufacturing: 10.5%, EPC: 11.0%, Pharma: 9.5%, Banks: 11.5%, Default: 10.0%).
- **Terminal Growth Rate ($g_{\text{term}}$)**: Perpetual terminal growth rate between **2.0% and 4.0%** (Default: 4.0%).
- **WACC Floor / Singularity Guard**: If $\text{WACC} \le g_{\text{term}}$, WACC is automatically reset to $g_{\text{term}} + 0.02$ (+2.0%) to prevent division-by-zero or negative enterprise values.
- **Enterprise Value to Equity Value Bridge**:
  - $\text{Net Debt} = \text{Total Debt} - \text{Cash \& Cash Equivalents}$.
  - $\text{Equity Value} = \text{Enterprise Value} - \text{Net Debt}$.
- **Fallback Data Proxies**:
  - If baseline revenue is missing or $\le 0$, revenue is proxied as **30.0% of Market Capitalization**.
  - If shares outstanding is missing/zero, estimated as $\text{Market Cap} / \max(\text{Close Price}, 1.0)$.
- **Veto Condition**: Vetoed for Banks & NBFCs because interest expense is an operating item and deposits/debt constitute operational inventory.

---

### 2.2 Dividend Discount Model (DDM)
*Source File: [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py#L245-L270)*

- **Earnings Anchor**: EPS taken from reported trailing EPS or proxied at flat **₹30.0** if unavailable.
- **Target Dividend Payout Ratio**: Assumed flat dividend payout ratio of **35.0%** ($0.35$).
- **Dividend Per Share Calculation**: $\text{DPS}_0 = \text{EPS} \times 0.35$.
- **Dividend Growth Rate ($g_{\text{div}}$)**: Baseline dividend growth aligned with sector terminal growth (default 4.0% - 7.0%).
- **Cost of Equity ($K_e$)**: Baseline $K_e = \text{WACC} + 1.5\%$ (ranging 10.5% - 13.0%).
- **$K_e$ Spread Constraint**: If $K_e \le g_{\text{div}}$, $K_e$ is automatically reset to $g_{\text{div}} + 0.03$ (+3.0%).
- **Gordon Growth Model Assumption**: Assumes single-stage perpetual dividend growth:
  $$\text{Expected DPS}_1 = \text{DPS}_0 \times (1 + g_{\text{div}})$$
  $$\text{Value Per Share} = \frac{\text{Expected DPS}_1}{K_e - g_{\text{div}}}$$
- **Veto Condition**: Vetoed for companies with dividend payout ratio $< 10\%$.

---

### 2.3 Residual Income (RI) Model
*Source File: [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py#L140-L186)*

- **Book Value Per Share (BVPS)**: Derived as $\text{Stockholders' Equity} / \text{Shares Outstanding}$. If equity is non-positive, proxied as $\text{Market Cap} / \text{P/B Ratio}$.
- **Return on Equity (ROE)**: Taken from sector metrics or calculated as $\text{PAT} / \text{Equity}$ (default baseline **15.0%**).
- **Cost of Equity ($K_e$)**: Baseline $K_e = \text{WACC} + 1.5\%$ (default 12.0%).
- **Retained Earnings Reinvestment Assumption**: **80.0% of Net Income** is retained and added to Book Equity each year ($1 - 20\%$ payout assumption):
  $$\text{Expected Net Income}_t = \text{BVPS}_{t-1} \times \text{ROE}$$
  $$\text{Equity Charge}_t = \text{BVPS}_{t-1} \times K_e$$
  $$\text{Residual Income}_t = \text{Expected Net Income}_t - \text{Equity Charge}_t$$
  $$\text{BVPS}_t = \text{BVPS}_{t-1} + (\text{Expected Net Income}_t \times 0.80)$$
- **Terminal Growth Rate**: Residual income terminal growth rate assumed at **6.0%**.
- **Valuation Composition**:
  $$\text{Equity Value Per Share} = \text{BVPS}_0 + \sum_{t=1}^5 \frac{\text{RI}_t}{(1 + K_e)^t} + \frac{\text{RI}_5 \times (1 + g)}{(K_e - g)(1 + K_e)^5}$$
- **Veto Condition**: Primary anchor for Financials/Banks. VETOED for Asset-Light businesses (IT Services, FMCG, Pharma) because historical book equity fails to capture intellectual capital, brand equity, or R&D pipelines.

---

### 2.4 Price-to-Earnings (P/E) Relative Valuation Model
*Source File: [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py#L70-L100)*

- **Target P/E Multiples**: Set per sector based on historic median trading bands:
  - Banks & NBFCs: **18.0x**
  - IT Services: **25.0x**
  - FMCG / Consumer: **40.0x**
  - Manufacturing / Auto: **22.0x**
  - Infrastructure / EPC: **18.0x**
  - Pharmaceuticals: **26.0x**
  - Baseline Default: **20.0x**
- **Earnings Per Share (EPS) Fallback Hierarchy**:
  1. Reported TTM EPS / `market_data.eps`.
  2. If missing, calculated as $\text{Close Price} / \text{P/E Ratio}$.
  3. If still missing, calculated as $\text{PAT} / \text{Shares Outstanding}$.
- **Negative Earnings Assumption**: If EPS $\le 0$, model returns `value_per_share = 0` with status `"Negative EPS"`.
- **Fair Value Formula**: $\text{Value Per Share} = \text{EPS} \times \text{Target P/E}$.

---

### 2.5 Price-to-Book (P/B) Justified Valuation Model
*Source File: [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py#L103-L138)*

- **Book Value Per Share (BVPS)**: Derived from balance sheet equity or proxied via $\text{Close Price} / \text{P/B Ratio}$.
- **Return on Equity (ROE) Clamping**: ROE is bounded between **5.0%** ($0.05$) and **30.0%** ($0.30$) to prevent extreme distortion.
- **Cost of Equity ($K_e$)**: Baseline **12.0%** ($0.12$). If $K_e \le g$, reset to $g + 0.03$.
- **Justified P/B Formula**:
  $$\text{Justified P/B} = \frac{\text{ROE} - g}{K_e - g}$$
- **Multiple Hard Clamping**: Justified P/B multiple is strictly bounded between **0.8x and 4.5x**.
- **Fair Value Formula**: $\text{Value Per Share} = \text{BVPS} \times \text{Justified P/B}$.
- **Veto Condition**: Primary anchor for Banks & NBFCs. Vetoed for asset-light corporates.

---

### 2.6 EV/EBITDA Relative Multiple Model
*Source File: [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py#L189-L215)*

- **EBITDA Fallback Proxy**: Reported EBITDA. If missing or $\le 0$, proxied as **22.0% of Total Revenue**.
- **Target EV/EBITDA Multiples**:
  - Banks & NBFCs: **12.0x** *(Vetoed)*
  - IT Services: **18.0x**
  - FMCG / Consumer: **26.0x**
  - Manufacturing / Auto: **14.0x**
  - Infrastructure / EPC: **11.0x**
  - Pharmaceuticals: **17.0x**
  - Baseline Default: **15.0x**
- **Net Debt Bridge**: $\text{Implied EV} = \text{EBITDA} \times \text{Target Multiple}$; $\text{Equity Value} = \text{Implied EV} - \text{Net Debt}$.
- **Negative EBITDA Handling**: Returns `0` if EBITDA $\le 0$.

---

### 2.7 EV/EBIT Relative Multiple Model
*Source File: [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py#L218-L242)*

- **EBIT Fallback Proxy**: Reported EBIT. If missing or $\le 0$, proxied as **18.0% of Total Revenue**.
- **Target EV/EBIT Multiple**: Set at **$1.2 \times$ Base EV/EBITDA Multiple** (ranging 13.2x to 31.2x; default 18.0x).
- **Net Debt Bridge**: $\text{Implied EV} = \text{EBIT} \times \text{Target Multiple}$; $\text{Equity Value} = \text{Implied EV} - \text{Net Debt}$.

---

## 🎭 3. Multi-Scenario & Sensitivity Matrix Assumptions

### 3.1 Multi-Scenario Operational Adjustments
*Source File: [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py#L272-L337)*

Every active model executes across three operational scenarios:

| Parameter Adjustment | Downside (Bear) Case | Base Case | Upside (Bull) Case |
| :--- | :--- | :--- | :--- |
| **Scenario Probability Weight** | **25.0%** | **50.0%** | **25.0%** |
| **Revenue Growth ($g_{\text{rev}}$)** | $0.70 \times \text{Base}$ ($-30\%$) | $1.00 \times \text{Base}$ | $1.30 \times \text{Base}$ ($+30\%$) |
| **Operating Margin (EBIT Margin)** | $0.85 \times \text{Base}$ ($-15\%$) | $1.00 \times \text{Base}$ | $1.15 \times \text{Base}$ ($+15\%$) |
| **WACC Add-On** | $+1.5\%$ ($+0.015$) | $0.0\%$ | $-1.0\%$ ($-0.010$) |
| **Target Multiples (P/E, EV/EBITDA)**| $0.80 \times \text{Base}$ ($-20\%$) | $1.00 \times \text{Base}$ | $1.20 \times \text{Base}$ ($+20\%$) |

---

### 3.2 Sensitivity Matrix Grid Assumptions
*Source File: [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py#L339-L366)*

A $5 \times 5$ sensitivity surface is generated by stepping WACC and Terminal Growth ($g$) around baseline parameters:

- **WACC Row Headers**: $[\text{Base}-1.0\%, \text{Base}-0.5\%, \text{Base}, \text{Base}+0.5\%, \text{Base}+1.0\%]$
- **Terminal Growth ($g$) Column Headers**: $[\text{Base}-1.0\%, \text{Base}-0.5\%, \text{Base}, \text{Base}+0.5\%, \text{Base}+1.0\%]$
- **Highlighted Scenario Coordinates**:
  - **Normal (Base) Case**: Row 3, Column 3 $(\text{Base WACC}, \text{Base } g)$
  - **Downside Case**: Row 5, Column 1 $(\text{Base WACC}+1.0\%, \text{Base } g-1.0\%)$
  - **Upside Case**: Row 1, Column 5 $(\text{Base WACC}-1.0\%, \text{Base } g+1.0\%)$

---

## 📊 4. Ensemble Distribution, Mispricing & Classification Assumptions
*Source File: [`src/ensemble_engine.py`](file:///d:/company-valuationi/src/ensemble_engine.py)*

### 4.1 Quantile Distribution ($Q10 - Q90$)
- Outputs from all active models across Downside, Base, and Upside scenarios are pooled.
- Quantiles are calculated empirically using numpy percentiles: $Q10$ (10th percentile floor), $Q25$ (lower quartile), $Q50$ (median baseline), $Q75$ (upper quartile), and $Q90$ (90th percentile ceiling).

### 4.2 Mispricing Formula & Classification Thresholds
- **Mispricing % ($M$)**:
  $$M = \frac{Q50}{\text{Current Market Price}} - 1$$

| Classification Status | Quantitative Threshold Criteria | Actionable Meaning |
| :--- | :--- | :--- |
| **STRONGLY UNDERVALUED** | $\text{Market Price} < Q10 \quad \text{AND} \quad M \ge +30.0\%$ | Significant margin of safety below 10th percentile floor |
| **UNDERVALUED** | $\text{Market Price} < Q25 \quad \text{AND} \quad M \ge +15.0\%$ | Trading below 25th percentile fair value |
| **FAIRLY VALUED** | $Q25 \le \text{Market Price} \le Q75 \quad \text{OR} \quad \|M\| < 15.0\%$ | Price lies within interquartile fair range |
| **OVERVALUED** | $\text{Market Price} > Q75 \quad \text{AND} \quad M \le -15.0\%$ | Trading above 75th percentile fair bound |
| **STRONGLY OVERVALUED** | $\text{Market Price} > Q90 \quad \text{AND} \quad M \le -30.0\%$ | Price exceeds 90th percentile bull ceiling |
| **INCONCLUSIVE** | $Q90 / Q10 > 3.0 \quad \text{OR} \quad \text{Valid Samples} < 2$ | Model disagreement exceeds 3.0x threshold |

---

### 4.3 Confidence Score Formula ($C$)
The confidence score $C \in [0, 100]$ represents valuation reliability:

$$C = 0.30 \cdot \text{Data Quality} + 0.25 \cdot \text{Method Agreement} + 0.20 \cdot \text{Historical Validation} + 0.15 \cdot \text{Forecast Stability} + 0.10 \cdot \text{Peer Quality}$$

- **Data Quality (30%)**: Default **90.0** for live exchange feeds.
- **Method Agreement (25%)**: Calculated as $\max(20.0, \min(100.0, 100.0 \times (1.0 - \text{CV})))$, where $\text{CV} = \sigma / Q50$.
- **Historical Validation (20%)**: Fixed **80.0** baseline.
- **Forecast Stability (15%)**: Fixed **75.0** baseline.
- **Peer Quality (10%)**: Fixed **85.0** baseline.

---

## 🧠 5. Neural Network Weight Engine Assumptions
*Source File: [`src/neural_weight_engine.py`](file:///d:/company-valuationi/src/neural_weight_engine.py)*

### 5.1 Architecture & Softmax Masking
- **Architecture**: 3-layer Feedforward Multi-Layer Perceptron (MLP):
  - **Input Layer**: 12 dimensions (6-dim One-Hot Sector Encoding + 6 Normalized Financial Metrics).
  - **Hidden Layer 1**: 32 units + ReLU activation.
  - **Hidden Layer 2**: 16 units + ReLU activation.
  - **Output Layer**: 7 units (matching all 7 valuation methods) + **Softmax Sector Mask**.
- **Sector Masking Assumption**: Logits of vetoed sector methods are forced to $-1 \times 10^9$ before Softmax, guaranteeing **0.0 weight** for non-eligible methods.
- **Normalized Weight Constraint**: All active method weights sum strictly to **1.0** ($\sum w_i = 1.0$).

### 5.2 Sector Default Weights (Fallback Allocation)

| Sector Pack | FCFF DCF | P/E | P/B | EV/EBITDA | EV/EBIT | Residual Income | DDM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Banks & NBFCs** | *Vetoed* | 10% | **40%** | *Vetoed* | *Vetoed* | **35%** | 15% |
| **IT Services** | **45%** | 35% | *Vetoed* | *Vetoed* | 20% | *Vetoed* | *Vetoed* |
| **FMCG / Consumer** | **40%** | 35% | *Vetoed* | 25% | *Vetoed* | *Vetoed* | *Vetoed* |
| **Manufacturing / Auto**| **35%** | 30% | *Vetoed* | **35%** | *Vetoed* | *Vetoed* | *Vetoed* |
| **Infrastructure / EPC**| **40%** | 25% | *Vetoed* | 35% | *Vetoed* | *Vetoed* | *Vetoed* |
| **Pharmaceuticals** | **40%** | 35% | *Vetoed* | 25% | *Vetoed* | *Vetoed* | *Vetoed* |

---

## ⏱️ 6. Data Pipeline, Cache & Staleness Assumptions
*Source File: [`src/data_fetcher.py`](file:///d:/company-valuationi/src/data_fetcher.py)*

- **Market Data TTL**: **24-hour cache limit** for stock price, market cap, and trading multiples.
- **Financial Statement TTL**: **90-day refresh cycle** for quarterly/annual balance sheets and income statements.
- **Point-in-Time Integrity**: All disclosures tagged with explicit `filing_date` and `period_end` date to eliminate look-ahead bias.
- **Currency & Scale**: All financial statements stored and evaluated in **INR Crores** (or normalized raw INR).

---

## 📍 7. Summary File Map

| System Component | Primary Code File | Key Function / Class |
| :--- | :--- | :--- |
| **Valuation Calculators & Scenarios** | [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py) | `ValuationEngine`, `run_scenarios_for_company`, `generate_sensitivity_matrix` |
| **Two-Layer Veto Resolver** | [`src/classification.py`](file:///d:/company-valuationi/src/classification.py) | `resolve_method_eligibility`, `get_company_classification` |
| **Ensemble & Mispricing Engine** | [`src/ensemble_engine.py`](file:///d:/company-valuationi/src/ensemble_engine.py) | `compute_ensemble_valuation`, `compute_weighted_ensemble_valuation` |
| **Neural Weight Optimization** | [`src/neural_weight_engine.py`](file:///d:/company-valuationi/src/neural_weight_engine.py) | `NeuralWeightOptimizer`, `train_neural_weights_from_csv` |
| **Pipeline Service Orchestrator** | [`src/valuation_service.py`](file:///d:/company-valuationi/src/valuation_service.py) | `run_full_valuation_pipeline` |
