# Comprehensive Data Sources & Valuation Methodology Guide

This document defines the complete data pipeline, data sources, collected metrics, staleness/refresh rules, and the step-by-step valuation processing engine built for the **20-Company Research Beta** in [`d:/company-valuationi`](file:///d:/company-valuationi).

---

## 1. Executive Overview & Pipeline Architecture

The system converts raw exchange and financial statement disclosures into audited, point-in-time fair-value distributions through a seven-stage deterministic pipeline:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        1. DATA SOURCES & APIs                          │
│   • NSE / BSE Exchange Feeds via yfinance API (Tickers: *.NS)          │
│   • XBRL Financial Disclosures & Company Annual Reports                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   2. EXTRACTION & NORMALISATION                        │
│   • Clean NaN/Inf values, currency scaling (INR Crores)                │
│   • Standardize consolidated financial items (Revenue, EBITDA, PAT)     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│              3. POINT-IN-TIME STORAGE & STALENESS                      │
│   • SQLite Database (valuation.db)                                     │
│   • 24-Hour TTL for Market Prices • 90-Day TTL for Financial Statements │
│   • Audit Trail logged in source_ledger                                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             4. CLASSIFICATION & METHOD ELIGIBILITY                     │
│   • Layer A: User-facing (Listing, Market Cap Class, Sector Pack)      │
│   • Layer B: Internal Attributes (Financial Nature, Lifecycle, Asset) │
│   • Method Eligibility Rules & Veto Resolver                           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  5. MULTI-SCENARIO VALUATION ENGINE                    │
│   • Models: FCFF DCF, P/E, P/B, Residual Income, EV/EBITDA, EV/EBIT, DDM│
│   • Scenarios: Downside (Bear), Base, Upside (Bull)                    │
│   • WACC & Terminal Growth Sensitivity Surfaces                        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│              6. ENSEMBLE QUANTILE & CONFIDENCE ENGINE                  │
│   • Quantiles: Q10 (10th percentile), Q25, Q50 (Median), Q75, Q90     │
│   • Mispricing % = (Q50 / Market Price) - 1                            │
│   • Confidence Score C (0–100 weighted quality index)                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             7. CLASSIFICATION OUTPUT & INCONCLUSIVE GATE               │
│   • Strongly Undervalued | Undervalued | Fairly Valued | Overvalued   │
│   • Inconclusive Gate (High method variance or missing filings)       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Sources & Extracted Metrics

Data is collected from primary market exchange interfaces, company filings, and structured financials via `yfinance` and verified exchange symbol feeds.

### 2.1 Primary Data Sources

| Source Tier | Source Name | Protocol / Feed | Purpose & Frequency |
|---|---|---|---|
| **Tier 1 (Market Data)** | National Stock Exchange (NSE) / BSE | Yahoo Finance API (`*.NS` tickers) | Live stock price, market capitalization, trailing P/E, price-to-book, 52-week high/low, trading volume (Real-time / 24h refresh). |
| **Tier 1 (Financials)** | Company Annual Reports & Financial Results | Exchange Filing DataFrames (`t.financials`, `t.balance_sheet`, `t.cashflow`) | Annual and quarterly reported financial statements: Revenue, EBITDA, EBIT, Net Profit, Equity, Debt, Cash, Capex, Operating Cash Flow, Shares Outstanding (Quarterly / 90d refresh). |
| **Tier 2 (Sector Drivers)** | Investor Presentations & Disclosures | Structured Sector Driver Mapping | Sector-specific metrics: Bank NIM, GNPA, NNPA, CASA; IT cc-growth, attrition; FMCG gross margin; EPC order book (Quarterly / Annual). |

---

### 2.2 Detailed Metric Mapping Matrix

The table below lists every data item collected, its exact source field, unit of measurement, and where it is stored in the database:

| Category | Data Field Name | Source Field / API Key | Unit | Storage Table & Column | Purpose in Valuation |
|---|---|---|---|---|---|
| **Market** | Current Stock Price | `currentPrice` / `regularMarketPrice` | INR (₹) | `market_data.close_price` | Baseline price $P$ for mispricing calculation. |
| **Market** | Market Capitalization | `marketCap` | INR (₹) | `market_data.market_cap` | Enterprise Value & Equity Value scaling. |
| **Market** | Trailing P/E Ratio | `trailingPE` / `forwardPE` | Multiple (x) | `market_data.pe_ratio` | Benchmark comparison for Relative P/E model. |
| **Market** | Price-to-Book Ratio | `priceToBook` | Multiple (x) | `market_data.pb_ratio` | Benchmark comparison for P/B model. |
| **Market** | Trailing EPS | `trailingEps` | INR (₹) | `market_data.eps` | Input for P/E valuation ($P/E \times EPS$). |
| **Market** | Dividend Yield | `dividendYield` | Percentage (%) | `market_data.dividend_yield` | Input for Dividend Discount Model (DDM). |
| **Market** | 52-Week Range | `fiftyTwoWeekHigh` / `Low` | INR (₹) | `market_data.fifty_two_week_*` | Trading range boundary context. |
| **Financials** | Total Revenue | `Total Revenue` / `totalRevenue` | INR (₹) | `financials.revenue` | Base for revenue growth forecasts in DCF. |
| **Financials** | EBITDA | `Normalized EBITDA` / `ebitda` | INR (₹) | `financials.ebitda` | Input for EV/EBITDA valuation model. |
| **Financials** | EBIT | `EBIT` / `Operating Income` | INR (₹) | `financials.ebit` | Input for EV/EBIT and DCF NOPAT calculations. |
| **Financials** | Net Profit (PAT) | `Net Income Common Stockholders` | INR (₹) | `financials.pat` | Input for ROE and Residual Income calculation. |
| **Financials** | Diluted EPS | `Diluted EPS` / `Basic EPS` | INR (₹) | `financials.eps` | Core per-share earnings variable. |
| **Financials** | Stockholders' Equity | `Stockholders Equity` | INR (₹) | `financials.equity` | Book Value Per Share ($BVPS = Equity / Shares$). |
| **Financials** | Total Debt | `Total Debt` / `Long Term Debt` | INR (₹) | `financials.debt` | Net Debt deduction ($NetDebt = Debt - Cash$). |
| **Financials** | Cash & Cash Equivalents | `Cash Cash Equivalents` | INR (₹) | `financials.cash` | Non-operating liquid assets addition. |
| **Financials** | Operating Cash Flow | `Operating Cash Flow` | INR (₹) | `financials.operating_cash_flow` | Base cash flow validation metric. |
| **Financials** | Capital Expenditure | `Capital Expenditure` | INR (₹) | `financials.capex` | Deducted from OCF to derive Free Cash Flow. |
| **Financials** | Free Cash Flow | `Free Cash Flow` | INR (₹) | `financials.free_cash_flow` | Primary cash flow input for FCFF DCF model. |
| **Financials** | Shares Outstanding | `Ordinary Shares Number` | Count | `financials.shares_outstanding` | Per-share conversion ($ValuePerShare = EquityValue / Shares$). |
| **Sector (Bank)** | Net Interest Margin (NIM)| Financial Disclosures | Percentage (%) | `sector_metrics.nim` | Bank profitability driver. |
| **Sector (Bank)** | Gross / Net NPA | Financial Disclosures | Percentage (%) | `sector_metrics.gnpa` / `nnpa` | Risk adjustment factor for bank book quality. |
| **Sector (Bank)** | CASA Ratio | Financial Disclosures | Percentage (%) | `sector_metrics.casa_ratio` | Low-cost deposit funding stability index. |
| **Sector (Bank)** | Return on Equity (ROE) | `returnOnEquity` | Percentage (%) | `sector_metrics.roe` | Core driver for Bank P/B & Residual Income models. |
| **Sector (IT)** | Constant Currency Growth| Investor Disclosures | Percentage (%) | `sector_metrics.constant_currency_growth` | Organic top-line growth indicator. |
| **Sector (IT)** | Utilisation & Attrition | Investor Disclosures | Percentage (%) | `sector_metrics.utilisation` / `attrition` | Operating margin sustainability indicators. |
| **Sector (EPC)**| Order Book Value | Filing Disclosures | INR (₹) | `sector_metrics.order_book` | Future revenue visibility driver. |

---

## 3. Data Processing, Storage & Staleness Management

### 3.1 Point-in-Time Database Storage (`data/valuation.db`)

All retrieved metrics are stored in SQLite with strict point-in-time timestamps to prevent look-ahead bias:

1. **`company_master`**: Identity, exchange codes, listing status, and classification attributes.
2. **`market_data`**: Historical closing prices, volume, market cap, and trading multiples.
3. **`financials`**: Statement line items tagged with `period_end` date and `filing_date`.
4. **`sector_metrics`**: Sector-specific operational indicators.
5. **`source_ledger`**: Complete audit log recording the metric name, extracted value, period end, filing source, and extraction timestamp.

### 3.2 Cache Policy & Staleness Rules

To ensure data remains current without exceeding API rate limits:

- **Market Data TTL (24 Hours)**: Stock price, market cap, and trading multiples are checked against the last `fetched_at` timestamp. If older than 24 hours, the system marks `is_stale = 1` and triggers an automated live fetch.
- **Financial Statements TTL (90 Days)**: Financial statement entries are refreshed quarterly.
- **Manual Force-Refresh**: Users can trigger an instant live refresh per company or in bulk via `POST /api/company/{symbol}/refresh`.

---

## 4. Two-Layer Classification & Veto Resolver

Companies are classified across two distinct layers to determine which valuation models are mathematically valid:

```text
                          ┌───────────────────────────┐
                          │   Target Company Ticker   │
                          └─────────────┬─────────────┘
                                        │
             ┌──────────────────────────┴──────────────────────────┐
             ▼                                                     ▼
┌───────────────────────────┐                       ┌───────────────────────────┐
│   LAYER A: User-Facing    │                       │   LAYER B: Internal       │
│  • Listing: Listed        │                       │  • Financial Nature       │
│  • Cap Class: Large/Mid   │                       │  • Lifecycle Phase        │
│  • Sector Pack (1 of 6)   │                       │  • Business Model Type    │
└────────────┬──────────────┘                       │  • Asset Intensity        │
             │                                      │  • Regulatory Structure   │
             │                                      └─────────────┬─────────────┘
             └──────────────────────────┬─────────────────────────┘
                                        │
                                        ▼
                        ┌───────────────────────────────┐
                        │   METHOD ELIGIBILITY RESOLVER │
                        │  - Activates Valid Calculators│
                        │  - Enforces Veto Rules        │
                        └───────────────┬───────────────┘
                                        │
                 ┌──────────────────────┴──────────────────────┐
                 ▼                                             ▼
  ┌───────────────────────────────┐             ┌───────────────────────────────┐
  │      ELIGIBLE METHODS         │             │        VETOED METHODS         │
  │  (e.g., Banks -> P/B,         │             │  (e.g., Banks -> VETO EV/EBITDA│
  │   Residual Income, DDM)       │             │   because debt is operational)│
  └───────────────────────────────┘             └───────────────────────────────┘
```

### 4.1 Sector Pack Rules & Veto Table

| Sector Pack | Target Universe | Eligible Valuation Methods | Vetoed Methods & Rationale |
|---|---|---|---|
| **Banks & NBFCs** | HDFC Bank, ICICI Bank, SBI, Bajaj Finance, Shriram Finance | **P/B**, **Residual Income**, **DDM**, **P/E** *(NBFCs)* | **EV/EBITDA & FCFF DCF VETOED**: Bank deposits and borrowings are operating financing liabilities. Enterprise Value and EBITDA are economically meaningless for financial institutions. |
| **IT Services** | TCS, Infosys, HCLTech | **FCFF DCF**, **P/E**, **EV/EBIT** | **Residual Income VETOED**: IT companies are asset-light; balance sheet book equity does not reflect human capital or IP value. |
| **FMCG / Consumer** | Hindustan Unilever, ITC, Nestlé India | **FCFF DCF**, **P/E**, **EV/EBITDA** | **Residual Income VETOED**: Brand franchise value is not captured in historical accounting equity. |
| **Manufacturing / Auto** | Maruti Suzuki, M&M, Eicher Motors, Bajaj Auto | **FCFF DCF**, **P/E**, **EV/EBITDA** | **Residual Income VETOED**: Heavy industrial capital intensity requires EV/EBITDA and DCF frameworks. |
| **Infrastructure / EPC** | Larsen & Toubro, KEC International | **FCFF DCF**, **EV/EBITDA**, **P/E**, **SOTP** | **Residual Income VETOED**: Order book project cash flows require project-level EV frameworks. |
| **Pharmaceuticals** | Sun Pharma, Dr. Reddy's, Cipla | **FCFF DCF**, **P/E**, **EV/EBITDA** | **Residual Income VETOED**: R&D pipeline value is omitted from historical book equity. |

---

## 5. Valuation Mathematical Formulas

### 5.1 FCFF Discounted Cash Flow (DCF) Model

Used for non-financial companies (IT, FMCG, Auto, EPC, Pharma):

$$\text{FCFF}_t = \text{Revenue}_t \times \text{EBIT Margin} \times (1 - \text{Tax Rate}) \times (1 - \text{Reinvestment Rate})$$

$$\text{Enterprise Value (EV)} = \sum_{t=1}^{T} \frac{\text{FCFF}_t}{(1 + \text{WACC})^t} + \frac{\text{Terminal Value}}{(1 + \text{WACC})^T}$$

$$\text{Terminal Value} = \frac{\text{FCFF}_T \times (1 + g)}{\text{WACC} - g}$$

$$\text{Equity Value} = \text{Enterprise Value} - \text{Net Debt} \quad (\text{where Net Debt} = \text{Debt} - \text{Cash})$$

$$\text{Fair Value Per Share} = \frac{\text{Equity Value}}{\text{Shares Outstanding}}$$

---

### 5.2 Price-to-Earnings (P/E) Relative Model

$$\text{Fair Value Per Share} = \text{Normalized EPS} \times \text{Target P/E Multiple}$$

---

### 5.3 Price-to-Book (P/B) Justified Model

Used for Banks and NBFCs. The justified P/B multiple is derived from the Return on Equity ($\text{ROE}$) and Cost of Equity ($K_e$):

$$\text{Justified P/B} = \frac{\text{ROE} - g}{K_e - g}$$

$$\text{Fair Value Per Share} = \text{Book Value Per Share (BVPS)} \times \text{Justified P/B}$$

---

### 5.4 Residual Income Valuation Model

Used for financial companies to value excess equity returns above the cost of capital:

$$\text{Residual Income}_t = \text{Net Income}_t - (K_e \times \text{Beginning Equity}_{t-1})$$

$$\text{Equity Value} = \text{Current Book Equity} + \sum_{t=1}^{T} \frac{\text{Residual Income}_t}{(1 + K_e)^t} + \frac{\text{Terminal Residual Income}}{(K_e - g)(1 + K_e)^T}$$

$$\text{Fair Value Per Share} = \frac{\text{Equity Value}}{\text{Shares Outstanding}}$$

---

### 5.5 EV/EBITDA & EV/EBIT Models

$$\text{Target Enterprise Value} = \text{EBITDA} \times \text{Target EV/EBITDA Multiple}$$

$$\text{Equity Value} = \text{Target Enterprise Value} - \text{Net Debt}$$

$$\text{Fair Value Per Share} = \frac{\text{Equity Value}}{\text{Shares Outstanding}}$$

---

### 5.6 Dividend Discount Model (DDM)

$$\text{Expected DPS}_{t+1} = \text{EPS} \times \text{Payout Ratio} \times (1 + g)$$

$$\text{Fair Value Per Share} = \frac{\text{Expected DPS}_{t+1}}{K_e - g}$$

---

## 6. Multi-Scenario & Sensitivity Matrix

Every active model runs across three scenario configurations:

| Scenario | Growth Rate ($g$) | Operating Margin | WACC Adjustment | Multiple Adjustment |
|---|---:|---:|---:|---:|
| **Downside (Bear)** | $0.70 \times \text{Base}$ | $0.85 \times \text{Base}$ | $+1.5\%$ | $0.80 \times \text{Base}$ |
| **Base** | $1.00 \times \text{Base}$ | $1.00 \times \text{Base}$ | $0.0\%$ | $1.00 \times \text{Base}$ |
| **Upside (Bull)** | $1.30 \times \text{Base}$ | $1.15 \times \text{Base}$ | $-1.0\%$ | $1.20 \times \text{Base}$ |

### Sensitivity Matrix Generation

For DCF models, a $5 \times 5$ matrix evaluates WACC ($\pm 1.0\%$) against Terminal Growth ($g \pm 1.0\%$) to produce a valuation surface:

$$\begin{pmatrix}
\text{WACC} \backslash g & g - 1\% & g - 0.5\% & g & g + 0.5\% & g + 1\% \\
\text{WACC} - 1\% & V_{11} & V_{12} & V_{13} & V_{14} & V_{15} \\
\text{WACC} - 0.5\% & V_{21} & V_{22} & V_{23} & V_{24} & V_{25} \\
\text{WACC} & V_{31} & V_{32} & \mathbf{V_{base}} & V_{34} & V_{35} \\
\text{WACC} + 0.5\% & V_{41} & V_{42} & V_{43} & V_{44} & V_{45} \\
\text{WACC} + 1\% & V_{51} & V_{52} & V_{53} & V_{54} & V_{55}
\end{pmatrix}$$

---

## 7. Ensemble Quantiles, Mispricing & Confidence Score

### 7.1 Quantile Distribution ($Q10$ – $Q90$)

Outputs across all active methods and scenarios are aggregated to construct a fair-value quantile distribution:

- **$Q10$ (10th Percentile)**: Conservative bear-case valuation floor.
- **$Q25$ (25th Percentile)**: Lower fair-value bound.
- **$Q50$ (50th Percentile / Median)**: Primary baseline fair value.
- **$Q75$ (75th Percentile)**: Upper fair-value bound.
- **$Q90$ (90th Percentile)**: Optimistic bull-case ceiling.

### 7.2 Mispricing Percentage ($M$)

$$M = \frac{Q50}{\text{Current Market Price}} - 1$$

---

### 7.3 Research Classification Rules

| Classification | Quantitative Rule Criteria | Action / Interpretation |
|---|---|---|
| **STRONGLY UNDERVALUED** | $\text{Price} < Q10 \quad \text{AND} \quad M \ge +30\%$ | Significant margin of safety below 10th percentile floor. |
| **UNDERVALUED** | $\text{Price} < Q25 \quad \text{AND} \quad M \ge +15\%$ | Price trades below lower quartile threshold. |
| **FAIRLY VALUED** | $Q25 \le \text{Price} \le Q75 \quad \text{OR} \quad |M| < 15\%$ | Price lies within interquartile range. |
| **OVERVALUED** | $\text{Price} > Q75 \quad \text{AND} \quad M \le -15\%$ | Price trades above 75th percentile upper bound. |
| **STRONGLY OVERVALUED** | $\text{Price} > Q90 \quad \text{AND} \quad M \le -30\%$ | Price exceeds 90th percentile bull ceiling. |
| **INCONCLUSIVE** | $Q90 / Q10 > 3.0 \quad \text{OR} \quad \text{Data Missing}$ | Model disagreement ratio exceeds safety threshold. |

---

### 7.4 Confidence Score Formula ($C$)

The overall confidence score $C \in [0, 100]$ measures empirical reliability:

$$C = 0.30 \times \text{Data Quality} + 0.25 \times \text{Method Agreement} + 0.20 \times \text{Historical Validation} + 0.15 \times \text{Forecast Stability} + 0.10 \times \text{Peer Quality}$$

Where:
- **Data Quality (30%)**: 90 points for live exchange feeds with audited financial filings.
- **Method Agreement (25%)**: $100 \times \left(1 - \frac{\sigma}{\mu}\right)$, where $\sigma/\mu$ is the coefficient of variation across model outputs.
- **Historical Validation (20%)**: 80 points based on backtesting accuracy.
- **Forecast Stability (15%)**: 75 points based on earnings variance.
- **Peer Quality (10%)**: 85 points for peer group alignment.

---

## 8. Summary File & Code Map

| File Path | Description & Purpose |
|---|---|
| [`src/company_universe.py`](file:///d:/company-valuationi/src/company_universe.py) | Master definitions of 20 companies, tickers, sector packs, and Layer A/B attributes. |
| [`src/database.py`](file:///d:/company-valuationi/src/database.py) | SQLite schema initialization, point-in-time tables, and repository functions. |
| [`src/data_fetcher.py`](file:///d:/company-valuationi/src/data_fetcher.py) | Live `yfinance` data fetcher, staleness manager, and audit log writer. |
| [`src/classification.py`](file:///d:/company-valuationi/src/classification.py) | Two-layer classification engine and method eligibility/veto resolver. |
| [`src/valuation_models.py`](file:///d:/company-valuationi/src/valuation_models.py) | Discrete calculators (DCF, P/E, P/B, RI, EV/EBITDA, DDM) and scenario engine. |
| [`src/ensemble_engine.py`](file:///d:/company-valuationi/src/ensemble_engine.py) | Quantile distribution ($Q10$–$Q90$), mispricing, classification rules, and confidence score. |
| [`src/valuation_service.py`](file:///d:/company-valuationi/src/valuation_service.py) | Master pipeline orchestrator connecting data, models, and outputs. |
| [`app/main.py`](file:///d:/company-valuationi/app/main.py) | FastAPI web server providing REST endpoints. |
| [`app/templates/index.html`](file:///d:/company-valuationi/app/templates/index.html) | Interactive single-page dashboard UI (Tailwind CSS, Chart.js). |
| [`run.py`](file:///d:/company-valuationi/run.py) | One-command launcher script. |
