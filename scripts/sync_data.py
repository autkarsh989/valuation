"""
Initial Live Data Collection and Valuation Script.
"""

from src.database import init_db
from src.valuation_service import run_valuation_for_all

def main():
    print("Initializing database...")
    init_db()
    print("Fetching live market & financial data for all 20 companies...")
    summaries = run_valuation_for_all(force_refresh=True)
    print(f"\nSuccessfully processed {len(summaries)} companies:\n")
    for c in summaries:
        price = f"₹{c.get('close_price', 0):,.1f}"
        q50 = f"₹{c.get('q50', 0):,.1f}"
        status = c.get('classification', 'N/A')
        comp_id = c.get('company_id', '')
        print(f"  {comp_id:<15} | Price: {price:>10} | Q50 Fair Value: {q50:>10} | Status: {status}")

if __name__ == "__main__":
    main()
