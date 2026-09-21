"""
FastAPI Server and Web Application API Endpoints.
Provides REST APIs and serves the interactive single-page dashboard UI.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import logging

from src.database import init_db, get_all_company_summaries
from src.valuation_service import run_valuation_for_company, run_valuation_for_all
from src.company_universe import COMPANIES_20, get_company_by_symbol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

app = FastAPI(
    title="Practical Valuation MVP - 20 Companies",
    description="Automated valuation, point-in-time data store, classification, and ensemble fair-value distribution system",
    version="1.0.0"
)

# Setup template engine
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.on_event("startup")
def startup_event():
    logger.info("Initializing database and loading initial universe...")
    init_db()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/companies")
def list_companies(sector: str = None, status: str = None, search: str = None):
    """
    Returns summary statistics and company list for the 20-company research universe.
    """
    summaries = get_all_company_summaries()

    if not summaries:
        # Run initial valuation if database is empty
        summaries = run_valuation_for_all(force_refresh=False)

    filtered = summaries
    if sector and sector != "All":
        filtered = [c for c in filtered if c.get("sector") == sector]
    if status and status != "All":
        filtered = [c for c in filtered if c.get("classification") == status]
    if search:
        s = search.lower()
        filtered = [
            c for c in filtered
            if s in c.get("company_id", "").lower() or s in c.get("common_name", "").lower()
        ]

    # Calculate Summary Stats
    total = len(summaries)
    undervalued = len([c for c in summaries if "UNDERVALUED" in (c.get("classification") or "")])
    overvalued = len([c for c in summaries if "OVERVALUED" in (c.get("classification") or "")])
    fairly_valued = len([c for c in summaries if c.get("classification") == "FAIRLY VALUED"])
    inconclusive = len([c for c in summaries if c.get("classification") == "INCONCLUSIVE"])
    stale_count = len([c for c in summaries if c.get("is_stale") == 1])

    return {
        "stats": {
            "total": total,
            "undervalued": undervalued,
            "overvalued": overvalued,
            "fairly_valued": fairly_valued,
            "inconclusive": inconclusive,
            "stale_count": stale_count
        },
        "companies": filtered
    }

@app.get("/api/company/{symbol}")
def get_company_detail(symbol: str, refresh: bool = False):
    """
    Returns full detailed valuation payload for a specific company.
    """
    comp_config = get_company_by_symbol(symbol)
    if not comp_config:
        raise HTTPException(status_code=404, detail=f"Company {symbol} not found in universe")

    try:
        data = run_valuation_for_company(comp_config["symbol"], force_refresh=refresh)
        return data
    except Exception as e:
        logger.error(f"Error evaluating {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/company/{symbol}/refresh")
def refresh_company(symbol: str):
    """
    Forces live yfinance data fetch, updates SQLite DB, and recalculates valuation.
    """
    comp_config = get_company_by_symbol(symbol)
    if not comp_config:
        raise HTTPException(status_code=404, detail=f"Company {symbol} not found")

    try:
        data = run_valuation_for_company(comp_config["symbol"], force_refresh=True)
        return {"status": "Success", "message": f"Refreshed live data and recalculated valuation for {symbol}", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/refresh-all")
def refresh_all_companies():
    """
    Forces bulk live data fetch and recalculation for all 20 companies.
    """
    try:
        summaries = run_valuation_for_all(force_refresh=True)
        return {"status": "Success", "message": "Bulk live update completed for all 20 companies", "companies": summaries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
