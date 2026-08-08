"""Canned queries over the superinvestor DB, printed as aligned tables."""

import sqlite3

from si import db


def _print_table(rows: list[sqlite3.Row], title: str) -> None:
    print(f"\n## {title}")
    if not rows:
        print("(no rows)")
        return
    cols = rows[0].keys()
    widths = {
        c: max(len(c), *(len(f"{r[c]}" if r[c] is not None else "-") for r in rows))
        for c in cols
    }
    print("  ".join(c.ljust(widths[c]) for c in cols))
    for r in rows:
        print(
            "  ".join(
                (f"{r[c]}" if r[c] is not None else "-").ljust(widths[c]) for c in cols
            )
        )


def new_buys(conn: sqlite3.Connection) -> None:
    _print_table(
        conn.execute(
            """
            SELECT a.ticker, s.name,
                   COUNT(*) AS buyers,
                   SUM(a.action = 'buy_new') AS new_positions,
                   ROUND(MAX(a.pct_of_portfolio), 2) AS max_pct_portfolio,
                   MAX(a.first_seen_date) AS latest_seen
            FROM activity a LEFT JOIN stocks s ON s.ticker = a.ticker
            WHERE a.action IN ('buy_new', 'add')
            GROUP BY a.ticker
            ORDER BY buyers DESC, max_pct_portfolio DESC
            LIMIT 30
            """
        ).fetchall(),
        "Consensus buys this quarter (by number of superinvestors)",
    )


def conviction(conn: sqlite3.Connection) -> None:
    _print_table(
        conn.execute(
            """
            SELECT a.ticker, m.name AS manager, a.action,
                   ROUND(a.pct_of_portfolio, 2) AS pct_of_portfolio,
                   a.quarter, a.first_seen_date
            FROM activity a JOIN managers m ON m.code = a.manager_code
            WHERE a.action IN ('buy_new', 'add') AND a.pct_of_portfolio IS NOT NULL
            ORDER BY a.pct_of_portfolio DESC
            LIMIT 30
            """
        ).fetchall(),
        "Highest-conviction buys (% of manager's portfolio)",
    )


def momentum_top(conn: sqlite3.Connection) -> None:
    _print_table(
        conn.execute(
            """
            SELECT mo.ticker, s.name, mo.score,
                   ROUND(mo.ret_3m, 1) AS ret_3m, ROUND(mo.ret_12m, 1) AS ret_12m,
                   ROUND(mo.rsi14, 0) AS rsi14,
                   ROUND(mo.pct_vs_200dma, 1) AS vs_200dma,
                   ROUND(ms.short_pct_float * 100, 1) AS short_pct,
                   ROUND(ms.putcall_oi_ratio, 2) AS put_call
            FROM momentum mo
            LEFT JOIN stocks s ON s.ticker = mo.ticker
            LEFT JOIN market_stats ms
                   ON ms.ticker = mo.ticker AND ms.asof = mo.asof
            WHERE mo.asof = (SELECT MAX(asof) FROM momentum WHERE ticker = mo.ticker)
            ORDER BY mo.score DESC
            LIMIT 30
            """
        ).fetchall(),
        "Momentum ranking",
    )


def verdicts(conn: sqlite3.Connection) -> None:
    _print_table(
        conn.execute(
            """
            SELECT an.ticker, s.name, an.verdict, an.conviction, an.moat_score,
                   an.fair_value_low, an.fair_value_high,
                   ROUND(an.margin_of_safety_pct, 1) AS mos_pct, an.asof
            FROM analysis an LEFT JOIN stocks s ON s.ticker = an.ticker
            WHERE an.asof = (SELECT MAX(asof) FROM analysis WHERE ticker = an.ticker)
            ORDER BY an.conviction DESC, an.moat_score DESC
            """
        ).fetchall(),
        "Munger/Buffett verdicts",
    )


def report(kind: str) -> None:
    conn = db.connect()
    sections = {
        "new-buys": [new_buys],
        "conviction": [conviction],
        "momentum": [momentum_top],
        "verdicts": [verdicts],
        "full": [new_buys, conviction, momentum_top, verdicts],
    }
    for fn in sections.get(kind, sections["full"]):
        fn(conn)
    conn.close()
