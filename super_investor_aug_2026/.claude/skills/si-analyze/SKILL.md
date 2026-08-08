---
name: si-analyze
description: Run the Sonnet analyst agents (momentum-analyst + value-analyst) over superinvestor buys that lack qualitative analysis, and persist their structured output to SQLite. Optionally pass tickers as arguments.
---

Dispatch the analyst agents over pending tickers. All commands run from
`super_investor_aug_2026/`.

1. **Get packets** — `uv run python -m si pending` (or with
   `--tickers T1,T2` if the user named tickers). It writes one JSON packet per
   ticker to `data/pending/` and prints the paths. If empty, say so and stop.
2. **Batch** — take up to 5 tickers per invocation (tell the user if more
   remain). For each ticker, spawn BOTH agents in parallel via the Agent tool:
   - `momentum-analyst` with the packet path — writes `<TICKER>.momentum.md`
   - `value-analyst` with the packet path — writes `<TICKER>.analysis.json`
   Independent tickers' agents can all run concurrently.
3. **Merge & persist** — for each ticker, add the momentum-analyst's thesis
   paragraph into the value-analyst's `<TICKER>.analysis.json` under the key
   `"momentum_thesis"`, then run:
   `uv run python -m si save-analysis data/pending/<TICKER>.analysis.json`
   If validation fails, fix the JSON shape (see the error) and retry once.
4. **Report back** — one line per ticker: verdict, conviction, fair-value
   range vs price, and the momentum adjusted score. Close with
   `uv run python -m si report verdicts` if 3+ tickers were analyzed.
