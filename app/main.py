"""
FastAPI Server and Web Application API Endpoints.
Provides REST APIs and serves the interactive single-page dashboard UI.
"""

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import logging

from src.database import (
    init_db, get_all_company_summaries,
    get_all_model_company_summaries, get_model_company_record,
    get_latest_training_run
)
from src.valuation_service import (
    run_valuation_for_company, run_valuation_for_all,
    run_neural_valuation_for_company, run_neural_valuation_for_all
)
from src.company_universe import COMPANIES_20, get_company_by_symbol
from src.neural_weight_engine import (
    train_neural_weights_from_csv, get_current_model_weights,
    DEFAULT_SECTOR_WEIGHTS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

app = FastAPI(
    title="Practical Valuation MVP - 20 Companies & Neural Weight Engine",
    description="Automated valuation, neural network method weighting, point-in-time data store, classification, and ensemble fair-value distribution system",
    version="2.0.0"
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
    """Original baseline valuation dashboard."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/train", response_class=HTMLResponse)
def read_train(request: Request):
    """Model training portal for neural network weight calculation."""
    return templates.TemplateResponse(request=request, name="train.html")

@app.get("/model-valuation", response_class=HTMLResponse)
@app.get("/replica", response_class=HTMLResponse)
def read_model_valuation(request: Request):
    """Replica valuation dashboard powered by Neural Network trained weights."""
    return templates.TemplateResponse(request=request, name="model_valuation.html")

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

# =========================================================================
# Model Training & Neural Network Weights APIs
# =========================================================================

SAMPLE_CSV_PATH = os.path.join(os.path.dirname(BASE_DIR), "data", "sample_sector_training_data.csv")

@app.get("/api/train/sample-csv")
def download_sample_csv():
    """
    Serves the pre-formatted sample CSV file containing multi-sector company details.
    """
    if not os.path.exists(SAMPLE_CSV_PATH):
        raise HTTPException(status_code=404, detail="Sample CSV template not found")
    return FileResponse(
        SAMPLE_CSV_PATH,
        media_type="text/csv",
        filename="sample_sector_training_data.csv"
    )

@app.post("/api/train/upload")
async def upload_and_train_model(file: UploadFile = File(...)):
    """
    Uploads a training CSV, executes Neural Network training to calculate optimal
    method weights, updates weights in SQLite, and recalculates neural valuations.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a CSV file (.csv)")

    try:
        contents = await file.read()
        csv_text = contents.decode("utf-8", errors="replace")

        # Train neural network and update stored weights
        train_result = train_neural_weights_from_csv(csv_text, epochs=70)

        # Recalculate valuations for all 20 companies with the new weights
        logger.info("Recalculating neural valuations for 20 companies with new weights...")
        run_neural_valuation_for_all(force_refresh=False)

        return train_result
    except Exception as e:
        logger.error(f"Error during model training: {e}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.get("/api/train/status")
def get_training_status():
    """
    Returns latest training run metrics and currently stored neural method weights per sector.
    """
    latest_run = get_latest_training_run()
    current_weights = get_current_model_weights()
    return {
        "status": "Ready",
        "latest_run": latest_run,
        "current_weights": current_weights,
        "default_weights": DEFAULT_SECTOR_WEIGHTS
    }

# =========================================================================
# Replica / AI Model-Weighted Valuation APIs
# =========================================================================

@app.get("/api/companies/model-valuation")
def list_model_companies(sector: str = None, status: str = None, search: str = None):
    """
    Returns summary statistics and company valuations computed using Neural Network trained weights.
    """
    summaries = get_all_model_company_summaries()

    if not summaries or all(c.get("q50") is None for c in summaries):
        # Run neural valuation if table is empty
        summaries = run_neural_valuation_for_all(force_refresh=False)

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

    # Calculate Summary Stats for Model Valuation
    total = len(summaries)
    undervalued = len([c for c in summaries if "UNDERVALUED" in (c.get("classification") or "")])
    overvalued = len([c for c in summaries if "OVERVALUED" in (c.get("classification") or "")])
    fairly_valued = len([c for c in summaries if c.get("classification") == "FAIRLY VALUED"])
    inconclusive = len([c for c in summaries if c.get("classification") == "INCONCLUSIVE"])
    stale_count = len([c for c in summaries if c.get("is_stale") == 1])

    return {
        "mode": "Neural Network Weighted",
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

@app.get("/api/company/{symbol}/model-valuation")
def get_model_company_detail(symbol: str, refresh: bool = False):
    """
    Returns full company valuation payload evaluated using Neural Network weights.
    """
    comp_config = get_company_by_symbol(symbol)
    if not comp_config:
        raise HTTPException(status_code=404, detail=f"Company {symbol} not found in universe")

    try:
        data = run_neural_valuation_for_company(comp_config["symbol"], force_refresh=refresh)
        return data
    except Exception as e:
        logger.error(f"Error evaluating {symbol} with neural weights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/company/{symbol}/model-valuation/refresh")
def refresh_model_company(symbol: str):
    """
    Refreshes single company live data and recalculates neural valuation.
    """
    comp_config = get_company_by_symbol(symbol)
    if not comp_config:
        raise HTTPException(status_code=404, detail=f"Company {symbol} not found")

    try:
        data = run_neural_valuation_for_company(comp_config["symbol"], force_refresh=True)
        return {"status": "Success", "message": f"Refreshed neural valuation for {symbol}", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/refresh-all/model-valuation")
def refresh_all_model_companies():
    """
    Forces bulk live data fetch and recalculation for all 20 companies using Neural Network weights.
    """
    try:
        summaries = run_neural_valuation_for_all(force_refresh=True)
        return {"status": "Success", "message": "Bulk neural update completed for all 20 companies", "companies": summaries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

