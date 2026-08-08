---
name: si-report
description: Query and summarize the superinvestor DB — consensus buys, conviction bets, momentum ranking, Munger/Buffett verdicts, or ad-hoc SQL questions about the data.
---

Answer questions from the superinvestor SQLite DB
(`super_investor_aug_2026/data/superinvestor.db`).

Canned views (run from `super_investor_aug_2026/`):

- `uv run python -m si report new-buys` — consensus buys by # of managers
- `uv run python -m si report conviction` — biggest %-of-portfolio bets
- `uv run python -m si report momentum` — momentum ranking with components
- `uv run python -m si report verdicts` — Munger/Buffett analysis results
- `uv run python -m si report full` — all of the above

For anything else, query directly:
`sqlite3 -header -column data/superinvestor.db "<sql>"`.
Tables: managers, holdings, activity (action ∈ buy_new/add/sell_all/reduce),
stocks, fundamentals, market_stats, momentum, analysis, runs. Latest row per
ticker = `MAX(asof)`. Full schema lives in `si/db.py`.

Present results as a short markdown table plus a 2-3 sentence takeaway; flag
anything surprising (new 10%+ position, cluster of sells in one name).
