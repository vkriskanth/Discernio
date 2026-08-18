"""SQLite schema and helpers for the superinvestor pipeline.

All writes are idempotent upserts keyed on natural keys so the pipeline
can be re-run daily without duplicating rows.
"""

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "superinvestor.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS managers (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    portfolio_date TEXT,
    last_seen_update TEXT
);

CREATE TABLE IF NOT EXISTS holdings (
    manager_code TEXT NOT NULL,
    ticker TEXT NOT NULL,
    quarter TEXT NOT NULL,
    pct_portfolio REAL,
    shares INTEGER,
    recent_activity TEXT,
    reported_price REAL,
    snapshot_date TEXT NOT NULL,
    PRIMARY KEY (manager_code, ticker, quarter)
);

CREATE TABLE IF NOT EXISTS activity (
    manager_code TEXT NOT NULL,
    ticker TEXT NOT NULL,
    quarter TEXT NOT NULL,
    action TEXT NOT NULL,             -- buy_new | add | sell_all | reduce
    share_change_pct REAL,            -- e.g. +25.3 means added 25.3% to position
    pct_of_portfolio REAL,            -- position size as % of manager portfolio
    first_seen_date TEXT NOT NULL,
    PRIMARY KEY (manager_code, ticker, quarter, action)
);

CREATE TABLE IF NOT EXISTS stocks (
    ticker TEXT PRIMARY KEY,
    name TEXT,
    sector TEXT,
    industry TEXT
);

CREATE TABLE IF NOT EXISTS fundamentals (
    ticker TEXT NOT NULL,
    asof TEXT NOT NULL,
    price REAL,
    shares_outstanding REAL,
    market_cap REAL,
    pe REAL,
    forward_pe REAL,
    ev_ebitda REAL,
    fcf_yield REAL,
    roe REAL,
    gross_margin REAL,
    op_margin REAL,
    rev_growth REAL,
    debt_to_equity REAL,
    raw_json TEXT,
    PRIMARY KEY (ticker, asof)
);

CREATE TABLE IF NOT EXISTS market_stats (
    ticker TEXT NOT NULL,
    asof TEXT NOT NULL,
    short_pct_float REAL,
    short_ratio REAL,
    putcall_oi_ratio REAL,
    avg_volume REAL,
    beta REAL,
    PRIMARY KEY (ticker, asof)
);

CREATE TABLE IF NOT EXISTS momentum (
    ticker TEXT NOT NULL,
    asof TEXT NOT NULL,
    ret_1m REAL,
    ret_3m REAL,
    ret_6m REAL,
    ret_12m REAL,
    rsi14 REAL,
    pct_vs_200dma REAL,
    score REAL,
    components_json TEXT,
    thesis TEXT,
    PRIMARY KEY (ticker, asof)
);

CREATE TABLE IF NOT EXISTS analysis (
    ticker TEXT NOT NULL,
    asof TEXT NOT NULL,
    moat TEXT,
    moat_score INTEGER,
    management_quality TEXT,
    capital_allocation TEXT,
    predictability TEXT,
    key_risks TEXT,
    fair_value_low REAL,
    fair_value_high REAL,
    margin_of_safety_pct REAL,
    verdict TEXT,                     -- buy | watch | pass
    conviction INTEGER,               -- 1-10
    checklist_json TEXT,
    raw_md TEXT,
    PRIMARY KEY (ticker, asof)
);

CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,
    notes TEXT
);
"""


def _migrate(conn: sqlite3.Connection) -> None:
    """Add columns introduced after initial release to existing DBs in place."""
    migrations = [
        ("fundamentals", "price", "REAL"),
        ("fundamentals", "shares_outstanding", "REAL"),
    ]
    for table, col, coltype in migrations:
        try:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {coltype}")
        except sqlite3.OperationalError as exc:
            if "duplicate column" not in str(exc).lower():
                raise
    conn.commit()


def connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    _migrate(conn)
    return conn


def today() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def upsert(conn: sqlite3.Connection, table: str, keys: dict, values: dict) -> None:
    """Insert or update a row identified by `keys` with `values`."""
    all_cols = {**keys, **values}
    cols = ", ".join(all_cols)
    placeholders = ", ".join("?" for _ in all_cols)
    updates = ", ".join(f"{c}=excluded.{c}" for c in values) or ", ".join(
        f"{c}=excluded.{c}" for c in keys
    )
    key_cols = ", ".join(keys)
    conn.execute(
        f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) "
        f"ON CONFLICT ({key_cols}) DO UPDATE SET {updates}",
        list(all_cols.values()),
    )


def log_run(conn: sqlite3.Connection, stage: str, status: str, notes: str = "") -> None:
    conn.execute(
        "INSERT INTO runs (started_at, stage, status, notes) VALUES (?, ?, ?, ?)",
        (datetime.now(UTC).isoformat(timespec="seconds"), stage, status, notes),
    )
    conn.commit()
