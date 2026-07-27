# TRADE PLAN — $10,000 on the Russell 2000 Graduation Screen

*Built 2026-07-27 from `data/shortlist.csv` (screen run of 2026-07-26,
336 scored candidates). Research exercise, not personalized financial
advice. Prices/caps move; rerun `main.py` before acting.*

## Structure: the backtest dictates the zones, not the scores

The one-year hindcast (`backtest.py`, see ANALYSIS.md) found that names
already inside the $8.0–22.7B S&P 400 addition band returned +11% on
average over the year they were added — while IWM did +31%. The
promotion is priced by the time a name crosses $8B. The $4–8B
"approaching" cohort averaged +95% (selection-bias caveat below), and
the <$4B tail paid even more on a longer clock. Allocation follows:

| Zone | Allocation | Rationale |
|---|---|---|
| In-band ($8B+) | **$0** | catalyst spent; +11% vs IWM +31% in the hindcast |
| Approaching ($4–8B) | **$6,400** | the +95% cohort's zone, ~12-month runway |
| Far-below ($1.5–4B) | **$2,500** | 2+ year clock, so smaller |
| Cash | **$1,100** | deployed only after single-name workups |

## Rules applied on top of the composite ranking

1. **No names already in the S&P 400** (IDCC, QLYS, ANF, LNTH, IBOC,
   SIGI score well but their graduation catalyst is gone).
2. **Financials capped at ~40% of the book.** They are 8 of the top 20
   approaching names, their scores rest on fewer metric legs (FCF
   components skipped), and they share rate/credit-cycle risk.
3. **Score-integrity exclusions:**
   - CALM (7.75) — 6.3x P/E is peak egg-cycle earnings; the value
     score is an illusion.
   - MCY (7.04) — composite carried by value/mgmt while moat is 2.9;
     catastrophe-exposed insurer priced off one good year.
4. **Prefer S&P 600 members** — S&P promotes from within its family;
   7 of the 9 positions are 600 members (SKWD and PFSI narrowly missed
   the book partly for this reason).

## The book

| # | Ticker | Name | Zone | Sector | $ | Composite | Thesis in one line |
|---|--------|------|------|--------|---|-----------|--------------------|
| 1 | AX | Axos Financial | approaching | Financials | 1,400 | 8.87 | best strategy-zone score; 21% growth, 16.6% ROE, 11.7x |
| 2 | VCTR | Victory Capital | approaching | Financials | 1,200 | 8.34 | mgmt 10/10, relentless buybacks |
| 3 | YOU | Clear Secure | approaching | Info Tech | 1,200 | 7.66 | 34% ROE, network effects; paying 42x for it |
| 4 | ENVA | Enova | approaching | Financials | 900 | 7.95 | 22% growth at 17.6x |
| 5 | FTDR | Frontdoor | approaching | Cons. Disc. | 900 | 7.06 | home-warranty moat, value 8.2 |
| 6 | FSS | Federal Signal | approaching | Industrials | 800 | 6.68 | industrials diversifier, moat 7.1 |
| 7 | IPAR | Inter Parfums | far-below | Cons. Staples | 900 | 7.56 | moat 8.3, real brand economics |
| 8 | TBBK | Bancorp Inc | far-below | Financials | 800 | 8.96 | highest composite in the entire screen |
| 9 | BMI | Badger Meter | far-below | Info Tech | 800 | 7.24 | moat 8.3, water-metering niche |
| — | cash | — | — | — | 1,100 | — | deploy after AX and YOU workups |

Totals: $8,900 invested + $1,100 cash. Financials $4,300 (43%, at the
cap). Approaching $6,400 / far-below $2,500.

## Exit / review discipline

- **Promotion event:** if a name is added to the S&P 400, the
  graduation thesis is complete — reassess as a pure
  business/valuation hold within ~1 quarter (the hindcast says
  post-add returns are ordinary).
- **Thesis break:** exit on a GAAP loss quarter (breaks S&P
  eligibility) or dilution > 3%/yr (breaks the management score).
- **Rebalance check:** rerun `main.py` quarterly (caps and the S&P
  bands both move); re-run `backtest.py` annually to re-validate the
  zone structure.

## Caveats (do not skip)

- The +95% zone return is **selection-biased**: it is the return of
  names that *did* graduate, known only in hindsight. The honest
  expectation for buying the whole quality-filtered zone is lower —
  the non-promotions dilute it.
- All metrics are yfinance screen-level data (~4 fiscal years, no
  filings read). The plan's own discipline: **no position before an
  analysis-001-style single-name workup** — AX and YOU first.
- S&P additions are committee decisions (sector balance, float,
  seasoning); nothing here is a promotion guarantee.
