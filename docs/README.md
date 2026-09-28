# Practical 20-Company Valuation & AI Neural Network Engine OS

Welcome to the **Practical 20-Company Valuation OS**, a production-grade automated enterprise valuation platform, point-in-time financial database, multi-scenario calculator, and Deep Learning Neural Weight Optimization Engine designed for the National Stock Exchange (NSE) research universe.

---

## 🌟 Overview & Key Features

The system bridges classical financial engineering (Discounted Cash Flow, Residual Income, Dividend Discount Models, Multiples) with modern Deep Learning (MLP Neural Networks) to provide defensible fair value estimates, quantile distributions ($Q_{10}, Q_{25}, Q_{50}, Q_{75}, Q_{90}$), factor impact attributions, and plain-English narratives.

### Core Capabilities
1. **20-Company Target Research Universe**:
   - Spans 6 critical sector packs: *Banks & NBFCs*, *IT Services*, *FMCG / Consumer*, *Manufacturing / Auto*, *Infrastructure / EPC*, and *Pharmaceuticals*.
2. **Dual Valuation Dashboards**:
   - **Standard Valuation OS (`/`)**: Equal/Heuristic weighted ensemble quantile valuation.
   - **AI Model Valuation OS (`/model-valuation`)**: Sector-weighted valuation powered by trained Neural Network weights.
3. **Neural Weight Optimization Engine (`/train`)**:
   - Multilayer Perceptron (MLP) Neural Network trained on cross-sector financial data to calculate optimal method weights ($W_{\text{DCF}}, W_{\text{PE}}, W_{\text{PB}}, W_{\text{EBITDA}}$, etc.) per sector pack.
4. **Point-In-Time SQLite Financial Data Store**:
   - Deduplicated point-in-time market data store preventing duplicate joins across snapshot dates.
5. **AI Explanation & Factor Attribution Engine**:
   - Plain-English valuation thesis generation, quantified metric impact extents ($\pm\%$ impact), standalone method share breakdowns, and Layer A veto rationale.
6. **Disagreement Ratio Circuit Breaker**:
   - Flags companies as **`INCONCLUSIVE`** when the spread between Bull ($Q_{90}$) and Bear ($Q_{10}$) scenarios exceeds a safety threshold ($Q_{90}/Q_{10} > 3.0x$).
7. **Interactive Glassmorphic Frontend**:
   - Grid View vs. Table View toggle, live Chart.js sector breakdown, click-to-filter KPI summary cards, price-vs-quantile range bars, and 1-click Markdown research report exporter.

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python**: 3.9+ or 3.10+
- **Database**: SQLite3 (bundled with Python)
- **Dependencies**: `fastapi`, `uvicorn`, `yfinance`, `torch` / `scikit-learn` or NumPy MLP, `jinja2`, `pytest`

### Installation

```bash
# 1. Clone or navigate to project directory
cd d:\company-valuationi

# 2. Install Python dependencies
pip install fastapi uvicorn yfinance jinja2 pytest numpy pandas
```

### Running the Web Server

Start the FastAPI application with auto-reload:

```bash
python run.py
```
The application will launch on **`http://127.0.0.1:8000`**.

### Application Routes

- **Standard Valuation Dashboard**: [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/)
- **AI Model Valuation Dashboard**: [`http://127.0.0.1:8000/model-valuation`](http://127.0.0.1:8000/model-valuation)
- **Neural Weight Training Portal**: [`http://127.0.0.1:8000/train`](http://127.0.0.1:8000/train)

### Running Unit Tests

```bash
python -m pytest
```

---

## 📂 Documentation Sitemap

Detailed documentation is available in the `docs/` directory:

| Document | Description |
| :--- | :--- |
| [**System Architecture & Flow**](file:///d:/company-valuationi/docs/SYSTEM_ARCHITECTURE_AND_FLOW.md) | End-to-end execution pipeline, data acquisition flow, neural network weight optimizer lifecycle, and system diagrams. |
| [**Valuation Methods & Models**](file:///d:/company-valuationi/docs/VALUATION_METHODS_AND_MODELS.md) | Detailed mathematical formulations for all 7 valuation models, Layer A veto rules, Layer B qualitative attributes, and WACC sensitivity matrices. |
| [**Explanation & Attribution Engine**](file:///d:/company-valuationi/docs/EXPLANATION_AND_ATTRIBUTION_ENGINE.md) | How plain-English AI explanations are generated, factor impact extents ($\pm\%$), method contribution shares, and the $Q_{90}/Q_{10}$ disagreement circuit breaker. |
| [**API & Database Reference**](file:///d:/company-valuationi/docs/API_AND_DATABASE_REFERENCE.md) | Complete OpenAPI REST endpoints spec, SQLite database schema definitions, sample JSON payloads, and CLI sync scripts. |
| [**How to Add New Companies Guide**](file:///d:/company-valuationi/docs/ADDING_COMPANIES_GUIDE.md) | Step-by-step instructions on expanding the universe, registering ticker metadata, training dataset updates, database sync, and verification. |

---

## 💻 Tech Stack Summary

- **Backend**: FastAPI (Python), Uvicorn ASGI Web Server
- **Database**: SQLite3 (`data/valuation.db`) with Point-In-Time deduplicated joins
- **Data Ingestion**: Yahoo Finance (`yfinance`) with fallback static financials
- **Data Science & Modeling**: NumPy, Scipy, MLP Neural Weight Engine
- **Frontend**: HTML5, Tailwind CSS, FontAwesome 6, Chart.js, Vanilla JavaScript (ES6+)
- **Testing**: Pytest & FastAPI TestClient
