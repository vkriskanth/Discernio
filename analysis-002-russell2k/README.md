# Analysis 002: Russell 2000 "Index Graduation" Screen

**Question:** Which Russell 2000 companies are earning their way out of
the index — likely promotions to the S&P MidCap 400 or S&P 500 — and
which of those are genuinely good businesses (moat, management, model,
price) worth catching before passive flows make it official?

**The mechanism:** ~40% of Russell 2000 constituents lose money, so the
index's profits concentrate in a small minority of names. S&P membership
requires positive GAAP earnings (latest quarter and trailing four
quarters) plus an unadjusted market cap of $8.0–22.7B for the MidCap 400
or ≥ $22.7B for the S&P 500 (thresholds verified July 2026). Profitable
compounders near those boundaries are graduation candidates; promotion
brings index-fund buying, and the anticipation run-up starts before the
committee announcement.

**Verdict (see [ANALYSIS.md](ANALYSIS.md)):** the concentration thesis
holds — 30% of the top-600 weights are unprofitable and the top 100
earners produce 52% of all positive earnings. Fifteen names clear the
mechanical screen, but six are already in the S&P 400; the true
front-runnable set is ~9 names, led by **Zurn Elkay (ZWS)** and
**Brinker (EAT)** — quality businesses, already inside the S&P 600
family, sitting right at the $8B MidCap 400 floor. FirstCash (FCFS) is
the best pure scorecard but its 400-inclusion has already happened.

## Run it

```bash
uv sync
uv run python main.py            # cached data reused if < 7 days old
uv run python main.py --refresh  # force refetch of everything
```

First run fetches fundamentals for the top 600 index weights (~15 min,
rate-limit friendly, checkpointed); cached reruns finish in seconds.
Then prints:

1. the universe — actual Russell 2000 constituents via the iShares IWM
   holdings CSV,
2. the profit concentration map — % unprofitable, and how much of the
   index's positive earnings the top 25/50/100 earners produce,
3. the graduation screen — GAAP profitability, US domicile/listing,
   cap ≥ $1.5B, tagged into three zones: **in-band** ($8.0–22.7B, the
   MidCap 400 addition range), **approaching** ($4–8B — the backtest's
   +95% cohort), and **far-below** ($1.5–4B, requires TTM NI ≥ $50M),
   with S&P 400/600 membership flags,
4. the moat test — ROE level and stability, gross margin, growth, FCF
   conversion over ~4 fiscal years, scored 0–10,
5. the management test — dilution, cash returned vs FCF, debt
   discipline, insider ownership, scored 0–10,
6. price, scored loosely — FCF yield, P/E, crude PEG vs the S&P 400
   multiple a promoted name re-rates toward; ranks but never eliminates,
7. the composite shortlist — moat 35% + management 25% + model/growth
   20% + value 20%, ranked per zone, full table in `data/shortlist.csv`.

Raw downloads and intermediates land in `data/` (gitignored).

## Backtest

```bash
uv run python backtest.py   # requires a prior main.py run (reuses cache)
```

Reruns the screen as of 2025-07-25 (caps rebuilt from that day's closes,
scoring restricted to FY≤2024 statements) and autopsies the year's 45
actual S&P 400 additions by where they sat a year earlier. Headline:
the $8B+ screen catches promotions only 0–2 quarters out (+11% avg for
names already in band); the +95%-avg payoff zone was the **$4–8B
"approaching" cohort** — see ANALYSIS.md for the selection-bias caveat.

## Caveats

S&P additions are committee decisions weighing sector balance, float,
and seasoning — this screen is a probability tilt, not a promotion list.
The index-inclusion pop has shrunk over the years; the anticipation
run-up is the actual target. Top names deserve a full analysis-001-style
single-name workup before any position.
