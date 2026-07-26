# Analysis 001: ManpowerGroup (MAN)

**Question:** ManpowerGroup jumped 32% on its 7/16/2026 Q2 earnings beat —
viewed through a Buffett-style "business, competitors, moat, management,
price" lens, is this a wonderful company at a fair price, or a mediocre one
that got statistically cheap?

**Verdict (see [ANALYSIS.md](ANALYSIS.md)):** no durable moat, but a
cycle-tested management team and a statistically cheap-to-fair price.

- The pop is a legitimate cyclical-trough re-rating (first profitable
  quarter after a 2025 loss), not a re-rating of the franchise — MAN is
  still 49% below its 2018 all-time high and had already roughly doubled
  off its 52-week low before the print.
- MAN is the second-largest revenue base in the peer set (Robert Half,
  Randstad, Adecco, Kelly, Kforce) but trades at the cheapest multiple of
  the larger names — a function of razor-thin (~1-3%) operating margins
  that the whole industry shares.
- **Business model:** a volume-and-spread business on billed labor — ~17%
  gross margin, ~16% SG&A, all profit lives in a 1-3% sliver highly
  levered to hiring volume.
- **Moat: essentially none.** Operating margins across MAN, Randstad, and
  Adecco converged to a 1-2.4% commodity band by 2025. The one standout
  (Robert Half) earned it via a bolted-on consulting business (Protiviti),
  not staffing itself. AI-driven recruiting disintermediation is a live,
  industry-wide risk.
- **Management:** Jonas Prising, CEO since 2014, cycle-tested and
  shareholder-conscious on buybacks (correctly throttled back in the
  downturn) — but 2025 forced a real 53% dividend cut and debt nearly
  doubled, evidence the downturn actually hurt.
- **Price:** 6.5x mid-cycle earnings (15.4% earnings yield) to 13x on a
  Q2/Q3 run-rate (7.6% yield) — statistically cheap to fair for a
  moat-less, thin-margin cyclical, not a wonderful business on sale.

## Run it

```bash
uv sync
uv run python main.py
```

Pulls fresh prices (yfinance) and financial statements for MAN and its
peer set (Robert Half, Randstad, Adecco, Kelly, Kforce, SPY), then prints:

1. the pop in context — MAN's tape around the 7/16 print vs its all-time
   high, 52-week range, and 5/10-yr price CAGRs,
2. a peer scoreboard — price performance across horizons,
3. comparative fundamentals — market cap, P/E, P/S, EV/EBITDA, margins, ROE,
4. MAN's income statement by fiscal year — the staffing spread made visible,
5. a moat test — operating margin stability across the closest comps,
6. management's capital allocation — dividends, buybacks, shares, debt,
7. valuation — price against trough / run-rate / mid-cycle earnings power.

Raw downloads land in `data/`.
