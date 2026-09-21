"""
Database repository layer for the Valuation System.
Implements SQLite schema as defined in Section 13 of the documentation.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "valuation.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. company_master
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS company_master (
        company_id TEXT PRIMARY KEY,
        legal_name TEXT,
        common_name TEXT,
        isin TEXT,
        bse_code TEXT,
        listing_status TEXT,
        sector TEXT,
        subsector TEXT,
        market_cap_class TEXT,
        financial_nature TEXT,
        lifecycle TEXT,
        business_model TEXT,
        asset_intensity TEXT,
        structure_type TEXT,
        regulatory_model TEXT,
        primary_methods TEXT,
        veto_methods TEXT,
        classification_as_of TEXT,
        classification_source TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. financials
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id TEXT,
        period_end TEXT,
        period_type TEXT,
        filing_date TEXT,
        revenue REAL,
        ebitda REAL,
        ebit REAL,
        pat REAL,
        eps REAL,
        total_assets REAL,
        equity REAL,
        cash REAL,
        debt REAL,
        capex REAL,
        operating_cash_flow REAL,
        free_cash_flow REAL,
        shares_outstanding REAL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(company_id, period_end, period_type)
    )
    """)

    # 3. market_data
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id TEXT,
        as_of_date TEXT,
        close_price REAL,
        adjusted_close REAL,
        volume INTEGER,
        market_cap REAL,
        pe_ratio REAL,
        pb_ratio REAL,
        eps REAL,
        dividend_yield REAL,
        fifty_two_week_high REAL,
        fifty_two_week_low REAL,
        is_stale INTEGER DEFAULT 0,
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(company_id, as_of_date)
    )
    """)

    # 4. sector_metrics
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sector_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id TEXT,
        as_of_date TEXT,
        nim REAL,
        gnpa REAL,
        nnpa REAL,
        casa_ratio REAL,
        cet1_ratio REAL,
        roe REAL,
        roa REAL,
        cost_to_income REAL,
        constant_currency_growth REAL,
        utilisation REAL,
        attrition REAL,
        volume_growth REAL,
        gross_margin REAL,
        order_book REAL,
        us_revenue_share REAL,
        rd_expense_ratio REAL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(company_id, as_of_date)
    )
    """)

    # 5. valuation_inputs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS valuation_inputs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id TEXT,
        as_of_date TEXT,
        method TEXT,
        scenario TEXT,
        revenue_growth REAL,
        margin REAL,
        tax_rate REAL,
        capex_ratio REAL,
        wacc REAL,
        cost_of_equity REAL,
        terminal_growth REAL,
        target_multiple REAL,
        input_source TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(company_id, as_of_date, method, scenario)
    )
    """)

    # 6. valuation_output
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS valuation_output (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id TEXT,
        as_of_date TEXT,
        method TEXT,
        scenario TEXT,
        enterprise_value REAL,
        equity_value REAL,
        value_per_share REAL,
        weight REAL,
        method_confidence REAL,
        is_vetoed INTEGER DEFAULT 0,
        veto_reason TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(company_id, as_of_date, method, scenario)
    )
    """)

    # 7. final_valuation
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS final_valuation (
        company_id TEXT PRIMARY KEY,
        as_of_date TEXT,
        market_price REAL,
        q10 REAL,
        q25 REAL,
        q50 REAL,
        q75 REAL,
        q90 REAL,
        mispricing REAL,
        classification TEXT,
        confidence_score REAL,
        status TEXT,
        rationale TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 8. source_ledger
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS source_ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id TEXT,
        metric TEXT,
        value REAL,
        period_end TEXT,
        filing_date TEXT,
        source_type TEXT,
        source_reference TEXT,
        extraction_method TEXT,
        confidence TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def save_company_master(company: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO company_master (
        company_id, legal_name, common_name, isin, bse_code, listing_status, sector,
        subsector, market_cap_class, financial_nature, lifecycle, business_model,
        asset_intensity, structure_type, regulatory_model, primary_methods, veto_methods,
        classification_as_of, classification_source
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(company_id) DO UPDATE SET
        legal_name=excluded.legal_name,
        common_name=excluded.common_name,
        market_cap_class=excluded.market_cap_class,
        sector=excluded.sector,
        subsector=excluded.subsector,
        primary_methods=excluded.primary_methods,
        veto_methods=excluded.veto_methods,
        updated_at=CURRENT_TIMESTAMP
    """, (
        company["symbol"], company["legal_name"], company["common_name"],
        company.get("isin", ""), company.get("bse_code", ""), company["listing_status"],
        company["sector"], company["subsector"], company["market_cap_class"],
        company["financial_nature"], company["lifecycle"], company["business_model"],
        company["asset_intensity"], company["structure_type"], company["regulatory_model"],
        json.dumps(company.get("primary_methods", [])),
        json.dumps(company.get("veto_methods", [])),
        datetime.now().strftime("%Y-%m-%d"), "Rule-Based Deterministic Engine"
    ))
    conn.commit()
    conn.close()

def save_market_data(data: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO market_data (
        company_id, as_of_date, close_price, adjusted_close, volume, market_cap,
        pe_ratio, pb_ratio, eps, dividend_yield, fifty_two_week_high, fifty_two_week_low, is_stale, fetched_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(company_id, as_of_date) DO UPDATE SET
        close_price=excluded.close_price,
        adjusted_close=excluded.adjusted_close,
        volume=excluded.volume,
        market_cap=excluded.market_cap,
        pe_ratio=excluded.pe_ratio,
        pb_ratio=excluded.pb_ratio,
        eps=excluded.eps,
        dividend_yield=excluded.dividend_yield,
        fifty_two_week_high=excluded.fifty_two_week_high,
        fifty_two_week_low=excluded.fifty_two_week_low,
        is_stale=0,
        fetched_at=CURRENT_TIMESTAMP
    """, (
        data["company_id"], data["as_of_date"], data.get("close_price", 0.0),
        data.get("adjusted_close", 0.0), data.get("volume", 0), data.get("market_cap", 0.0),
        data.get("pe_ratio", 0.0), data.get("pb_ratio", 0.0), data.get("eps", 0.0),
        data.get("dividend_yield", 0.0), data.get("fifty_two_week_high", 0.0),
        data.get("fifty_two_week_low", 0.0), 0
    ))
    conn.commit()
    conn.close()

def save_financials(fin: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO financials (
        company_id, period_end, period_type, filing_date, revenue, ebitda, ebit, pat, eps,
        total_assets, equity, cash, debt, capex, operating_cash_flow, free_cash_flow, shares_outstanding
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(company_id, period_end, period_type) DO UPDATE SET
        revenue=excluded.revenue, ebitda=excluded.ebitda, ebit=excluded.ebit, pat=excluded.pat,
        eps=excluded.eps, total_assets=excluded.total_assets, equity=excluded.equity, cash=excluded.cash,
        debt=excluded.debt, capex=excluded.capex, operating_cash_flow=excluded.operating_cash_flow,
        free_cash_flow=excluded.free_cash_flow, shares_outstanding=excluded.shares_outstanding,
        updated_at=CURRENT_TIMESTAMP
    """, (
        fin["company_id"], fin["period_end"], fin.get("period_type", "Annual"),
        fin.get("filing_date", ""), fin.get("revenue", 0.0), fin.get("ebitda", 0.0),
        fin.get("ebit", 0.0), fin.get("pat", 0.0), fin.get("eps", 0.0),
        fin.get("total_assets", 0.0), fin.get("equity", 0.0), fin.get("cash", 0.0),
        fin.get("debt", 0.0), fin.get("capex", 0.0), fin.get("operating_cash_flow", 0.0),
        fin.get("free_cash_flow", 0.0), fin.get("shares_outstanding", 0.0)
    ))
    conn.commit()
    conn.close()

def save_sector_metrics(sm: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO sector_metrics (
        company_id, as_of_date, nim, gnpa, nnpa, casa_ratio, cet1_ratio, roe, roa, cost_to_income,
        constant_currency_growth, utilisation, attrition, volume_growth, gross_margin, order_book,
        us_revenue_share, rd_expense_ratio
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(company_id, as_of_date) DO UPDATE SET
        nim=excluded.nim, gnpa=excluded.gnpa, nnpa=excluded.nnpa, casa_ratio=excluded.casa_ratio,
        cet1_ratio=excluded.cet1_ratio, roe=excluded.roe, roa=excluded.roa, cost_to_income=excluded.cost_to_income,
        constant_currency_growth=excluded.constant_currency_growth, utilisation=excluded.utilisation,
        attrition=excluded.attrition, volume_growth=excluded.volume_growth, gross_margin=excluded.gross_margin,
        order_book=excluded.order_book, us_revenue_share=excluded.us_revenue_share, rd_expense_ratio=excluded.rd_expense_ratio,
        updated_at=CURRENT_TIMESTAMP
    """, (
        sm["company_id"], sm["as_of_date"], sm.get("nim"), sm.get("gnpa"), sm.get("nnpa"),
        sm.get("casa_ratio"), sm.get("cet1_ratio"), sm.get("roe"), sm.get("roa"), sm.get("cost_to_income"),
        sm.get("constant_currency_growth"), sm.get("utilisation"), sm.get("attrition"),
        sm.get("volume_growth"), sm.get("gross_margin"), sm.get("order_book"),
        sm.get("us_revenue_share"), sm.get("rd_expense_ratio")
    ))
    conn.commit()
    conn.close()

def save_final_valuation(val: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO final_valuation (
        company_id, as_of_date, market_price, q10, q25, q50, q75, q90, mispricing,
        classification, confidence_score, status, rationale
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(company_id) DO UPDATE SET
        as_of_date=excluded.as_of_date,
        market_price=excluded.market_price,
        q10=excluded.q10, q25=excluded.q25, q50=excluded.q50, q75=excluded.q75, q90=excluded.q90,
        mispricing=excluded.mispricing, classification=excluded.classification,
        confidence_score=excluded.confidence_score, status=excluded.status, rationale=excluded.rationale,
        updated_at=CURRENT_TIMESTAMP
    """, (
        val["company_id"], val["as_of_date"], val["market_price"],
        val["q10"], val["q25"], val["q50"], val["q75"], val["q90"],
        val["mispricing"], val["classification"], val["confidence_score"],
        val["status"], val["rationale"]
    ))
    conn.commit()
    conn.close()

def get_latest_market_data(company_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM market_data WHERE company_id = ? ORDER BY fetched_at DESC LIMIT 1", (company_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_latest_financials(company_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM financials WHERE company_id = ? ORDER BY period_end DESC LIMIT 1", (company_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_company_full_record(company_id: str) -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM company_master WHERE company_id = ?", (company_id,))
    cm = cursor.fetchone()
    cm_dict = dict(cm) if cm else {}
    if cm_dict:
        cm_dict["primary_methods"] = json.loads(cm_dict.get("primary_methods") or "[]")
        cm_dict["veto_methods"] = json.loads(cm_dict.get("veto_methods") or "[]")

    cursor.execute("SELECT * FROM market_data WHERE company_id = ? ORDER BY fetched_at DESC LIMIT 1", (company_id,))
    md = cursor.fetchone()
    md_dict = dict(md) if md else {}

    cursor.execute("SELECT * FROM financials WHERE company_id = ? ORDER BY period_end DESC LIMIT 1", (company_id,))
    fin = cursor.fetchone()
    fin_dict = dict(fin) if fin else {}

    cursor.execute("SELECT * FROM sector_metrics WHERE company_id = ? ORDER BY as_of_date DESC LIMIT 1", (company_id,))
    sm = cursor.fetchone()
    sm_dict = dict(sm) if sm else {}

    cursor.execute("SELECT * FROM final_valuation WHERE company_id = ?", (company_id,))
    fv = cursor.fetchone()
    fv_dict = dict(fv) if fv else {}

    conn.close()

    return {
        "master": cm_dict,
        "market": md_dict,
        "financials": fin_dict,
        "sector_metrics": sm_dict,
        "valuation": fv_dict
    }

def get_all_company_summaries() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        cm.company_id, cm.common_name, cm.sector, cm.market_cap_class, cm.financial_nature,
        md.close_price, md.market_cap, md.pe_ratio, md.pb_ratio, md.fetched_at, md.is_stale,
        fv.q10, fv.q25, fv.q50, fv.q75, fv.q90, fv.mispricing, fv.classification, fv.confidence_score, fv.status
    FROM company_master cm
    LEFT JOIN market_data md ON cm.company_id = md.company_id
    LEFT JOIN final_valuation fv ON cm.company_id = fv.company_id
    ORDER BY cm.sector, cm.common_name
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def log_source(company_id: str, metric: str, value: float, period_end: str, source_type: str, reference: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO source_ledger (company_id, metric, value, period_end, source_type, source_reference, extraction_method, confidence)
    VALUES (?, ?, ?, ?, ?, ?, 'Automated Live Fetcher', 'High')
    """, (company_id, metric, value, period_end, source_type, reference))
    conn.commit()
    conn.close()
