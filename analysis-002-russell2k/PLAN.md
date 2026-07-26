# PLAN — Analysis 002: Russell 2000 "Index Graduation" Screen

This is an execution spec. Follow it top to bottom. It was written so a
fresh session (no prior context) can build the whole analysis.

## Objective

Find the Russell 2000 companies that are earning their way out of the
index — names likely to be promoted to the S&P MidCap 400 or S&P 500 —
**before** the promotion happens and passive flows follow. The edge being
exploited: ~40% of Russell 2000 constituents lose money, so index-level
profits are concentrated in a small minority; S&P membership requires
positive GAAP earnings plus a market-cap threshold, so the profitable
compounders near the cap boundary are the graduation candidates. We want
the subset of those that are also *good businesses*: real moat, able and
responsible management, sound business model, reasonable price (be LOOSE
on price — rank by valuation but do not eliminate names on price alone;
keep the full shortlist visible with valuation as one score among four).

## Where this lives / house conventions

- Work in `analysis-002-russell2k/` inside the `discernio` repo. The
  folder already has `pyproject.toml`, `.venv` (via `uv sync`),
  `uv.lock`, a stub `main.py`, and a stub `README.md`.
- Mirror the style of `analysis-001-manpower/` — READ `main.py`,
  `README.md`, and `ANALYSIS.md` there first. House style:
  - One `main.py` that runs the entire analysis top to bottom, printing
    numbered `=== N. Section title ===` blocks to stdout, each ending
    with a short indented `Read:` interpretation paragraph.
  - Raw/intermediate data cached as CSVs in `data/` (gitignored).
  - Docstring at top of `main.py` states the question and enumerates the
    checks.
  - Deps managed with `uv add` / `uv sync`; run with
    `uv run python main.py` from inside the folder.
- Lint gates (run from repo root, config in root `pyproject.toml`):
  `ruff check analysis-002-russell2k/` and
  `pylint analysis-002-russell2k/main.py` must pass clean. Line length
  88, Python 3.14. Use `# pylint: disable=broad-exception-caught` on
  necessarily-broad try/excepts around per-ticker yfinance calls.

## Step 0 — Verify current facts (do NOT hardcode from memory)

Web-search and confirm, then record the verified numbers as constants
with a source-and-date comment:

1. **S&P index market-cap thresholds** (they are rebased periodically;
   were ~$20.5B for the S&P 500 and ~$7.4B–$20.5B band for the MidCap
   400 as of 2025 — confirm the current 2026 values).
2. **S&P earnings eligibility rule**: positive GAAP earnings in the most
   recent quarter AND positive sum of the trailing four quarters
   (confirm unchanged).
3. Other eligibility gates worth encoding: US domicile, primary US
   exchange listing, float/liquidity minimums (investable weight factor
   ≥ 0.10). Committee discretion and sector balance also apply — note in
   output that this screen produces a probability tilt, not a certainty.

## Step 1 — Universe: get the actual Russell 2000 constituents

- Download the iShares IWM holdings CSV (public, updated daily). Product
  page: <https://www.ishares.com/us/products/239710/ishares-russell-2000-etf>.
  The CSV download endpoint looks like
  `.../239710/.../1467271812596.ajax?fileType=csv&fileName=IWM_holdings&dataType=fund`
  — if that exact URL fails, find the current "Download holdings" CSV
  link on the product page. Fetch with `requests` using a browser-like
  User-Agent header (iShares blocks default UAs).
- The CSV has ~9 preamble rows before the header — parse robustly (find
  the header row containing "Ticker"). Keep: Ticker, Name, Sector,
  Weight (%), Market Value, Shares.
- Filter to `Asset Class == "Equity"` and drop cash/futures/placeholder
  rows (tickers with dashes/blanks). Expect ~1,900–2,000 names.
- Normalize tickers for yfinance (e.g. `BRK.B`-style dots → dashes:
  `s.replace(".", "-")`).
- Cache to `data/universe.csv`. **On every later run, load from cache if
  the file exists and is < 7 days old** — same caching rule for every
  expensive fetch below. A `--refresh` CLI flag (argparse) forces
  refetch of everything.

## Step 2 — Profit concentration map (who earns the index's profits?)

- For ALL universe names, fetch a lightweight fundamentals snapshot.
  Use `yf.Tickers` / batched `yf.Ticker(t).info` — but 2,000 `.info`
  calls are slow and rate-limited, so:
  - Prefer `yf.Ticker(t).fast_info` where sufficient (market cap,
    last price) and fall back to `.info` only for names that pass the
    early cap filter (Step 3) — i.e., **do the cheap cap screen first**,
    then fetch full `.info` (TTM net income `netIncomeToCommon`, margins,
    ROE, etc.) only for the survivors plus enough names to build the
    concentration table.
  - For the concentration map specifically you need TTM net income for
    everyone. If per-name `.info` for 2,000 names proves too slow
    (> ~20 min) or gets rate-limited, fall back to computing the
    concentration stats on the top ~600 names by index weight (they
    dominate the earnings anyway) and say so in the output. Sleep
    ~0.2–0.5 s between calls if 429s appear; wrap each call in
    try/except and count failures; print the failure count.
  - Cache everything fetched to `data/fundamentals_raw.csv` keyed by
    ticker so a rerun never refetches.
- Output section: total TTM net income of profitable names vs total
  losses of unprofitable names; % of names unprofitable; % of aggregate
  positive earnings contributed by the top 25 / 50 / 100 earners.
  Print the top 25 earners as a table (ticker, name, sector, TTM net
  income, market cap).

## Step 3 — Graduation screen (S&P eligibility mechanics)

Filter the universe to promotion candidates:

- **Market cap**: within the verified S&P 400 band, OR ≥ ~70% of the
  S&P 500 threshold (the "500-track" cohort). Tag each survivor
  `400-ready` or `500-track` (or both).
- **GAAP profitability**: TTM net income > 0. If quarterly net income is
  available via `yf.Ticker(t).quarterly_income_stmt`, also require most
  recent quarter > 0; if the quarterly statement fetch fails for a name,
  keep the name but flag `last_q_unverified`.
- **Domicile / listing**: `.info["country"] == "United States"` and
  exchange in NYSE/NASDAQ families. Drop foreign-domiciled names.
- Names already in the S&P SmallCap 600 are *more* likely to be promoted
  (S&P prefers promoting within its own family). Getting 600 membership
  programmatically is optional — if a clean free source (e.g. Wikipedia's
  "List of S&P 600 companies" table via `pd.read_html`) works, add an
  `in_sp600` flag column; if it's flaky, skip and note it.
- Expect roughly 30–80 survivors. Cache to `data/graduation_candidates.csv`.
- Print the survivor table sorted by market cap descending.

## Step 4 — Quality screen (the moat proxy, on survivors only)

For each survivor pull annual statements (`income_stmt`, `balance_sheet`,
`cashflow` — ~4 fiscal years each) and compute:

- ROE each year and its 4-yr average and stability (std dev).
- Operating margin each year — level and trend.
- Gross margin level (a high, stable gross margin is the rawest moat
  signal).
- Revenue CAGR over the available years.
- FCF conversion: FCF / net income (average).
- Net debt / EBITDA (most recent year).

Moat score (0–10): reward high & stable ROE, high gross margin, positive
revenue growth, FCF conversion near or above 1. Keep the scoring formula
simple, explicit, and printed in the output so it can be criticized.
Cache computed metrics to `data/quality_metrics.csv`.

## Step 5 — Management screen (on survivors)

From cashflow/balance-sheet history:

- Share count trajectory over 4 yrs (dilution is the small-cap sin —
  reward flat/shrinking, penalize > ~3%/yr growth).
- Buybacks + dividends vs FCF (returning cash without over-levering).
- Debt trajectory.
- Insider ownership % (`.info["heldPercentInsiders"]`) — reward
  meaningful skin in the game (> ~5%).

Management score (0–10), formula printed.

## Step 6 — Price (LOOSE — rank, don't eliminate)

- Trailing P/E, forward P/E, EV/EBITDA, FCF yield, P/E vs the name's own
  revenue growth (crude PEG).
- Context anchor: fetch the same multiples for the S&P 400 ETF universe
  proxy — simplest robust approach is to print IJH/MDY-level valuation
  from `.info` if available, or just state the S&P 400 median P/E from a
  web search as a hardcoded, dated constant. This is the multiple a
  promoted name re-rates *toward*.
- Value score (0–10), generous: only truly egregious multiples (e.g.
  P/E > 60 with < 10% growth) should score near 0. **No name is dropped
  for valuation.**

## Step 7 — Composite shortlist

- Composite = weighted score: moat 35%, management 25%, business
  model/growth 20%, value 20% (business-model/growth can reuse revenue
  CAGR + margin trend from Step 4 — don't double-count ROE).
- Print the final ranked shortlist (~top 15) with all four sub-scores,
  the cohort tag (400-ready / 500-track), sector, market cap, and the
  headline multiples. Save to `data/shortlist.csv`.
- End with a `Read:` block: what the screen can and cannot claim
  (committee discretion, sector balance, the shrunken but real
  anticipation run-up), and that the top ~5 names each deserve a full
  analysis-001-style single-name workup as follow-ups.

## Deliverables & acceptance criteria

1. `main.py` — runs end-to-end with `uv run python main.py`; supports
   `--refresh`; survives individual ticker failures without crashing;
   prints sections 1–7 in house style; total runtime on cached data
   < 1 min.
2. `data/` CSVs as named above (gitignored; that's fine).
3. `README.md` — rewrite the stub: the question, the mechanism being
   exploited, verdict placeholder pointing at ANALYSIS.md, "Run it"
   block, and a one-line description of each numbered output section
   (mirror analysis-001's README shape).
4. `ANALYSIS.md` — after a successful full run, write up findings:
   the concentration stats, the shortlist table, 2–3 sentences on each
   of the top ~5 names (what the numbers say about moat/management/
   model/price), and honest caveats.
5. `ruff check` and `pylint` clean from repo root.
6. Do not commit anything unless explicitly asked.

## Known pitfalls

- yfinance rate limits: cache aggressively, sleep on 429s, never refetch
  what's on disk (unless `--refresh`).
- iShares CSV preamble rows and a footer/disclaimer row — parse by
  locating the header row, stop at the first all-blank row after data.
- pandas 3.x is installed (breaking changes vs 2.x: e.g. no silent
  downcasting, `Series.__getitem__` label/positional strictness) — if an
  example from analysis-001 misbehaves, prefer `.iloc`/`.loc` explicit
  forms.
- Some Russell names have no annual statements on yfinance (recent IPOs,
  banks with odd line items) — score what's available, flag `n/a` fields,
  never let one name kill the run.
- Financials/banks: EBITDA and net-debt metrics are meaningless — detect
  `sector == "Financials"` (or missing EBITDA) and skip those fields for
  them rather than scoring garbage.
