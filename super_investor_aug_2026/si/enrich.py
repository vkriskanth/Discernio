"""Fundamentals enrichment via yfinance for tickers with new buy/add activity."""

import json
import sqlite3

import yfinance as yf

from si import db


def pending_tickers(conn: sqlite3.Connection, table: str) -> list[str]:
    """Tickers with buy_new/add activity lacking a row in `table` for today."""
    rows = conn.execute(
        f"""
        SELECT DISTINCT a.ticker FROM activity a
        WHERE a.action IN ('buy_new', 'add')
          AND a.ticker NOT IN (SELECT ticker FROM {table} WHERE asof = ?)
        ORDER BY a.ticker
        """,
        (db.today(),),
    ).fetchall()
    return [r["ticker"] for r in rows]


def yf_symbol(ticker: str) -> str:
    """Dataroma uses dot share-class suffixes (BRK.B); yfinance wants a dash."""
    return ticker.replace(".", "-")


def _get(info: dict, *keys: str) -> float | None:
    for k in keys:
        v = info.get(k)
        if isinstance(v, (int, float)):
            return float(v)
    return None


def enrich_ticker(conn: sqlite3.Connection, ticker: str) -> bool:
    """Fetch fundamentals for one ticker; returns False on failure."""
    try:
        info = yf.Ticker(yf_symbol(ticker)).info or {}
    except Exception as exc:  # yfinance raises many ad-hoc types
        db.log_run(conn, "enrich", "error", f"{ticker}: {exc}")
        return False
    if not info.get("symbol"):
        db.log_run(conn, "enrich", "error", f"{ticker}: no data")
        return False

    market_cap = _get(info, "marketCap")
    fcf = _get(info, "freeCashflow")
    fcf_yield = (fcf / market_cap) if fcf and market_cap else None
    price = _get(info, "currentPrice", "regularMarketPrice", "previousClose")
    shares_outstanding = _get(info, "sharesOutstanding")

    db.upsert(
        conn,
        "stocks",
        {"ticker": ticker},
        {
            "name": info.get("shortName") or info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
        },
    )
    db.upsert(
        conn,
        "fundamentals",
        {"ticker": ticker, "asof": db.today()},
        {
            "price": price,
            "shares_outstanding": shares_outstanding,
            "market_cap": market_cap,
            "pe": _get(info, "trailingPE"),
            "forward_pe": _get(info, "forwardPE"),
            "ev_ebitda": _get(info, "enterpriseToEbitda"),
            "fcf_yield": fcf_yield,
            "roe": _get(info, "returnOnEquity"),
            "gross_margin": _get(info, "grossMargins"),
            "op_margin": _get(info, "operatingMargins"),
            "rev_growth": _get(info, "revenueGrowth"),
            "debt_to_equity": _get(info, "debtToEquity"),
            "raw_json": json.dumps(
                {k: v for k, v in info.items() if isinstance(v, (int, float, str))}
            ),
        },
    )
    conn.commit()
    return True


def enrich(tickers: list[str] | None = None) -> dict:
    conn = db.connect()
    targets = tickers or pending_tickers(conn, "fundamentals")
    done, failed = [], []
    for t in targets:
        (done if enrich_ticker(conn, t) else failed).append(t)
    db.log_run(conn, "enrich", "ok", f"{len(done)} enriched, {len(failed)} failed")
    conn.close()
    return {"enriched": done, "failed": failed}
