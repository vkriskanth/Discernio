# ANALYSIS — Russell 2000 Index Graduation Screen

*Data as of 2026-07-23 (IWM holdings) / 2026-07-26 (fundamentals run).
All numbers from the first full run of `main.py`; rerun for fresh data.*

## The concentration thesis holds

Of the top 600 Russell 2000 names by weight (598 with data), **30% are
unprofitable**, with a combined $57.9B of TTM losses against $90.0B of
profits earned by the other 421. The positive earnings are themselves
concentrated: the top 25 earners produce 22% of all positive TTM income,
the top 50 produce 34%, the top 100 produce 52%. The index's profit
engine is a thin slice — which is exactly why screening that slice for
S&P graduation candidates is tractable.

The single biggest earner (StoneCo, $3.6B TTM) is Brazilian and
correctly falls out on the US-domicile gate — a reminder that raw
earnings rank alone is not a candidate list.

## The graduation screen: 15 candidates, but two different trades

Sixteen names cleared cap ≥ $8.0B (the S&P 400 floor, verified July
2026); one fell out on a most-recent-quarter GAAP loss. Of the 15
survivors, the S&P family membership check split them into two very
different groups:

**Already in the S&P MidCap 400 — only the 500 jump remains (6):**
BrightSpring (BTSG), UMB Financial (UMBF), CareTrust REIT (CTRE), Old
National (ONB), Krystal Biotech (KRYS), FirstCash (FCFS). The market has
already had its 400-inclusion event; the next catalyst is the $22.7B
S&P 500 threshold, 1.6–2.8x away from their current caps. Slow burners.

**True 400-graduation candidates (9):** Zurn Elkay (ZWS), Brinker (EAT),
StoneX (SNEX), TG Therapeutics (TGTX), Life Time (LTH), Ryman (RHP),
ESCO (ESE), Legence (LGN), Compass (COMP). Seven of the nine are already
S&P 600 members — and S&P promotes from within its family far more often
than from outside. LGN (Sept-2025 IPO, still seasoning) and COMP are the
outsiders.

## The composite shortlist (moat 35 / mgmt 25 / growth 20 / value 20)

| # | Ticker | Composite | Cohort | Read |
|---|--------|-----------|--------|------|
| 1 | FCFS | 7.75 | in-400 | best all-rounder, but catalyst is distant |
| 2 | UMBF | 6.78 | in-400 | cheap (12.4x) but M&A-inflated growth |
| 3 | ZWS | 6.70 | **400-ready** | top true graduation candidate |
| 4 | CTRE | 6.62 | in-400 | REIT; dilution penalty overstated |
| 5 | EAT | 6.19 | **400-ready** | turnaround momentum, 18x, at the floor |

**FirstCash (FCFS, 7.75)** — pawn + retail-POS lending. The best
balanced scorecard: moat 7.2 (ROE ~13% on a genuinely differentiated
lending niche), management 9.4 (steady buybacks, minimal dilution,
insider ownership), value 7.8 at 22x with ~10% revenue growth. But it is
already in the S&P 400, so the only index catalyst left is a 500 add at
~2.6x its current cap — own it for the business, not the flow.

**UMB Financial (UMBF, 6.78)** — regional bank at 12.4x with a 21%
revenue CAGR, but both numbers carry the all-stock Heartland Financial
acquisition: the share issuance craters the management score (1.6) and
inflates growth. Already in the 400. The value score (10) is real, the
graduation angle is not.

**Zurn Elkay (ZWS, 6.70)** — clean-water products; **the screen's top
actionable name**. In the S&P 600, cap $8.1B right at the 400 floor,
management 9.5 (buybacks, deleveraging, disciplined post-merger
integration), stable margins. The catch is price: 39x trailing with
~10% growth (value 4.4) — you are paying up for quality plus catalyst.

**CareTrust REIT (CTRE, 6.62)** — skilled-nursing REIT compounding via
acquisitions, 25% revenue CAGR. Already in the 400. Its management score
(3.4) is unfairly low: REITs must issue shares to grow, and the dilution
penalty in the formula doesn't know that. Read REIT scores with that
caveat.

**Brinker (EAT, 6.19)** — Chili's turnaround, 18x with 12% growth and
huge momentum; in the S&P 600 at exactly the $8.0B floor. The 95.6% ROE
is an artifact of years of near-zero book equity, so the moat score
leans on distorted inputs. The truest near-term 400 candidate on
fundamentals-plus-catalyst after ZWS.

Also notable among true candidates: **StoneX (SNEX, 6.02)** — 19.9x,
26% revenue CAGR, in the 600, but financial-conglomerate accounting
makes its screen metrics the least trustworthy of the group.

## Verdict

The mechanism is real but narrower than the raw screen suggests: after
removing names the S&P 400 already holds, the front-runnable set is ~9
names, led by **ZWS and EAT** (quality + in-family + at the cap floor),
with **SNEX, LTH, RHP** behind them. The in-400 quality names (FCFS
above all) are still interesting — as businesses, not as flow trades.

## Caveats (honest ones)

- yfinance gives only ~4 fiscal years; "stability" measured on 4 points
  is weak evidence of a moat.
- ROE distortions: EAT and RHP run tiny/negative book equity; TGTX's
  505% revenue CAGR is off a near-zero base (its growth score of 10 is
  a base effect, not a franchise).
- The dilution penalty misreads REITs (CTRE, RHP) and all-stock
  acquirers (UMBF); the FCF metrics are skipped for financials, so their
  scores rest on fewer legs.
- S&P additions are committee calls (sector balance, float, seasoning);
  this is a probability tilt. The inclusion-day pop has shrunk over the
  years — the anticipation run-up is the actual target.
- Missing-data renormalization means a name scored on fewer components
  can look artificially clean (LGN's 4 quarters of history, for one).
- Next step before any position: full analysis-001-style single-name
  workups on ZWS, EAT, and FCFS.
