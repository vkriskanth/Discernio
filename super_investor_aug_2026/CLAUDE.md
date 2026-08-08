# super_investor_aug_2026

Tracks what Dataroma's ~83 superinvestors are buying/selling during the
Aug 2026 13F season (Q2-2026 filings land ~Aug 1-20), enriches new buys with
yfinance data, and layers on momentum + Munger/Buffett analysis. Everything
lives in SQLite at `data/superinvestor.db`.

## Daily workflow

1. `/si-daily` — scrape Dataroma, enrich, compute momentum, summarize what's new
2. `/si-analyze` — Sonnet analyst agents (momentum-analyst, value-analyst)
   write structured analysis for pending buy/add tickers
3. `/si-report` — query digests (or ad-hoc SQL)

## CLI (run from this folder, uses uv)

```
uv run python -m si scrape [--managers SAM,BRK] [--limit N]
uv run python -m si enrich [--tickers T1,T2]      # default: pending buy/adds
uv run python -m si momentum [--tickers T1,T2]
uv run python -m si pending [--tickers T1,T2]     # JSON packets -> data/pending/
uv run python -m si save-analysis <file.json>     # validate + upsert agent output
uv run python -m si report [new-buys|conviction|momentum|verdicts|full]
```

## Layout

- `si/db.py` — schema (source of truth) + idempotent upsert helpers
- `si/scrape.py` — Dataroma parsers (home, holdings, activity pages); raw HTML
  cached per-day under `data/raw/<date>/` so re-runs are free; 1.5s throttle
- `si/enrich.py`, `si/momentum.py` — yfinance; per-ticker failures are logged
  to `runs` and non-fatal
- `si/analysis_io.py` — JSON bridge to the analyst agents (validation lives here)
- `.claude/agents/` — momentum-analyst, value-analyst (both `model: sonnet`)

## Notes

- `activity.pct_of_portfolio` is Dataroma's "% change to portfolio"; for
  `buy_new` rows it equals the position's size as % of the portfolio
- Scrape is idempotent: re-running a day never duplicates rows and only prints
  activity not previously seen (`first_seen_date` is preserved)
- Managers file on different dates; expect activity to trickle in until ~Aug 20
- Lint: `ruff check .` from repo root (shared config in root pyproject.toml)
