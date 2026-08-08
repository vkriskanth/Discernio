---
name: si-daily
description: Daily superinvestor pipeline — scrape Dataroma, enrich new buys with fundamentals, compute momentum, and summarize what's new. Run every day through ~Aug 20 2026 as Q2-2026 13F filings land.
---

Run the daily data collection for the superinvestor tracker. All commands run
from `super_investor_aug_2026/` (use `uv run`).

1. **Scrape** — `uv run python -m si scrape`
   (~170 throttled requests, takes a few minutes; run in background if long).
   Note the "NEW activity" lines it prints — that is today's story.
2. **Enrich** — `uv run python -m si enrich` (fundamentals for new buy/add
   tickers). Then **momentum** — `uv run python -m si momentum`.
   Failures on individual tickers are logged and non-fatal; mention them.
3. **Summarize for the user**:
   - Which managers filed today (new activity by manager)
   - Notable new positions: biggest `pct_of_portfolio` first — a 10%+ position
     is a conviction bet, call it out
   - Consensus: tickers bought by 2+ managers (`uv run python -m si report new-buys`)
   - Notable exits (sell_all rows)
4. If there are new buy/add tickers without qualitative analysis, tell the
   user how many are pending and suggest running `/si-analyze`.

Keep the summary tight: a few bullet groups, tickers bolded, no table dumps
unless asked.
