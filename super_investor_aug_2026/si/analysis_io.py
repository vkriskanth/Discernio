"""JSON bridge between the SQLite DB and the Claude analyst agents.

`dump_pending` writes one JSON packet per ticker awaiting qualitative
analysis; `save_analysis` validates an agent's JSON and upserts it.
"""

import json
import sqlite3
from pathlib import Path

from si import db

VERDICTS = {"buy", "watch", "pass"}

ANALYSIS_FIELDS = {
    "moat": str,
    "moat_score": int,
    "management_quality": str,
    "capital_allocation": str,
    "predictability": str,
    "key_risks": str,
    "fair_value_low": (int, float),
    "fair_value_high": (int, float),
    "margin_of_safety_pct": (int, float),
    "verdict": str,
    "conviction": int,
    "checklist_json": (dict, str),
    "raw_md": str,
}


def _latest(conn: sqlite3.Connection, table: str, ticker: str) -> dict | None:
    row = conn.execute(
        f"SELECT * FROM {table} WHERE ticker = ? ORDER BY asof DESC LIMIT 1", (ticker,)
    ).fetchone()
    return dict(row) if row else None


def pending_analysis_tickers(conn: sqlite3.Connection) -> list[str]:
    """Buy/add tickers that have fundamentals but no qualitative analysis yet."""
    rows = conn.execute(
        """
        SELECT DISTINCT a.ticker FROM activity a
        WHERE a.action IN ('buy_new', 'add')
          AND a.ticker IN (SELECT ticker FROM fundamentals)
          AND a.ticker NOT IN (SELECT ticker FROM analysis)
        ORDER BY a.ticker
        """
    ).fetchall()
    return [r["ticker"] for r in rows]


def build_packet(conn: sqlite3.Connection, ticker: str) -> dict:
    """Everything an analyst agent needs about one ticker."""
    buyers = conn.execute(
        """
        SELECT a.manager_code, m.name AS manager_name, a.action,
               a.share_change_pct, a.pct_of_portfolio, a.quarter
        FROM activity a JOIN managers m ON m.code = a.manager_code
        WHERE a.ticker = ? AND a.action IN ('buy_new', 'add')
        ORDER BY a.pct_of_portfolio DESC
        """,
        (ticker,),
    ).fetchall()
    stock = conn.execute("SELECT * FROM stocks WHERE ticker = ?", (ticker,)).fetchone()
    fundamentals = _latest(conn, "fundamentals", ticker)
    if fundamentals:
        fundamentals.pop("raw_json", None)
    return {
        "ticker": ticker,
        "stock": dict(stock) if stock else {},
        "superinvestor_buys": [dict(b) for b in buyers],
        "fundamentals": fundamentals,
        "market_stats": _latest(conn, "market_stats", ticker),
        "momentum": _latest(conn, "momentum", ticker),
    }


def dump_pending(out_dir: Path, tickers: list[str] | None = None) -> list[Path]:
    conn = db.connect()
    targets = tickers or pending_analysis_tickers(conn)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for t in targets:
        path = out_dir / f"{t}.json"
        path.write_text(json.dumps(build_packet(conn, t), indent=2))
        paths.append(path)
    conn.close()
    return paths


def save_analysis(path: Path) -> str:
    """Validate and persist one agent-produced analysis JSON. Returns ticker."""
    data = json.loads(path.read_text())
    ticker = data.get("ticker")
    if not ticker:
        raise ValueError("missing 'ticker'")
    for field, typ in ANALYSIS_FIELDS.items():
        if field not in data:
            raise ValueError(f"{ticker}: missing field '{field}'")
        if not isinstance(data[field], typ):
            raise ValueError(f"{ticker}: field '{field}' has wrong type")
    if data["verdict"] not in VERDICTS:
        raise ValueError(f"{ticker}: verdict must be one of {sorted(VERDICTS)}")
    if not 1 <= data["conviction"] <= 10:
        raise ValueError(f"{ticker}: conviction must be 1-10")

    values = {f: data[f] for f in ANALYSIS_FIELDS}
    if isinstance(values["checklist_json"], dict):
        values["checklist_json"] = json.dumps(values["checklist_json"])

    conn = db.connect()
    db.upsert(conn, "analysis", {"ticker": ticker, "asof": db.today()}, values)
    # momentum thesis may ride along from the momentum-analyst agent
    thesis = data.get("momentum_thesis")
    if thesis:
        conn.execute(
            "UPDATE momentum SET thesis = ? WHERE ticker = ? "
            "AND asof = (SELECT MAX(asof) FROM momentum WHERE ticker = ?)",
            (thesis, ticker, ticker),
        )
    conn.commit()
    conn.close()
    return ticker
