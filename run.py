"""
Startup script for the 20-Company Valuation MVP Application.
Initializes database, fetches live data for 20 companies, calculates fair values,
and launches the FastAPI web server.
"""

import uvicorn
import os
import sys
import logging

from src.database import init_db
from src.valuation_service import run_valuation_for_all

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("run")

def main():
    logger.info("Initializing SQLite database...")
    init_db()

    logger.info("Syncing live exchange data & calculating valuations for 20 target companies...")
    try:
        summaries = run_valuation_for_all(force_refresh=False)
        logger.info(f"Successfully processed {len(summaries)} companies.")
    except Exception as e:
        logger.error(f"Error during initial sync: {e}")

    logger.info("Starting Web Application Dashboard on http://127.0.0.1:8000")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)

if __name__ == "__main__":
    main()
