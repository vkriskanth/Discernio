# ManpowerGroup (NYSE: MAN): A Value-Investor's Read on the +32% Day

*Written 2026-07-20, four days after the print. All market/financial
figures from `main.py` (yfinance daily prices + statements, run against the
7/17 close); news items sourced at the bottom. Framed as a Buffett-style
"business, moat, management, price" walkthrough — not advice.*

## Q1. What actually happened, and does 32% mean anything?

On **7/16/2026** ManpowerGroup reported Q2 results that beat on both lines:
revenue $4.9B (+7.5–8% y/y, ~$170M above consensus) and adjusted EPS $0.99
(vs. $0.95 expected) — the headline swing was **net income of $53.5M versus
a $67.1M loss** in the year-ago quarter. Management raised Q3 guidance to
$0.96–$1.06 (midpoint $1.01, implying ~6% constant-currency organic growth)
and described the core Manpower brand as having "moved from stabilization
into a recovery" after five straight quarters of improving trends. The stock
opened up as much as 32% and closed the week +27–32% depending on the print
used.

**But altitude matters more than velocity.** Pulling the full tape:

- MAN's last close is **$52.34** — still **49% below its all-time peak of
  $102.66** set in January 2018.
- The 52-week range is $25.16–$52.34: the stock had already **doubled off
  its 52-week low** before the earnings pop even printed.
- **5-year price CAGR: −10.9%/yr. 10-year CAGR: +0.5%/yr.** An investor who
  bought and held MAN a decade ago has made essentially nothing on price.

So: 32% in one day is real, but it's a re-rating of a *cyclical trough*, not
a re-rating of the franchise. The Q2 print was the first hard evidence that
2023–2025 (three years of shrinking revenue and a near-loss in 2025) was the
bottom of the staffing cycle, not a permanent impairment. That distinction —
cyclical recovery vs. structural improvement — is the question the rest of
this analysis has to answer.

## Q2. Competitors — how does MAN stack up?

The peer set: **Robert Half (RHI)**, **Randstad (RAND.AS, Amsterdam)** —
the global #1 by revenue — **Adecco (ADEN.SW, Zurich)**, **Kelly Services
(KELYA)**, and **Kforce (KFRC)**. (Allegis, cited as the largest *US*
staffing firm, is privately held and not investable.)

**Price performance** tells a industry-first, company-second story:

| | YTD | 1y | 3y | 5y |
|---|----:|---:|---:|---:|
| MAN | +78% | +24% | −32% | −44% |
| RHI | +60% | +8% | −43% | −41% |
| Randstad | +8% | −17% | −25% | −27% |
| Adecco | −8% | −16% | −28% | −54% |
| Kelly | +80% | +26% | −13% | −22% |
| Kforce | +91% | +43% | −2% | +12% |
| S&P 500 | +9% | +20% | +70% | +84% |

Every staffing name has trailed SPY badly over 3–5 years — this is a
*sector* that's been through a real winter, not a MAN-specific problem.
2026 is a broad staffing re-rating (MAN, Kelly, and Kforce all up 78–91%
YTD), which is itself informative: the market is pricing a **cyclical
turn in hiring**, across the board, not a MAN-specific fix.

**Fundamentals** put MAN squarely mid-pack on quality, cheap on multiple:

| | Mkt cap | Rev | P/E ttm | P/E fwd | EV/EBITDA | Op margin | Net margin | ROE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| MAN | $2.4B | $18.7B | 23.6x | **10.8x** | 8.8x | 2.3% | 0.6% | 5.1% |
| RHI | $4.3B | $5.3B | 32.2x | 20.3x | 33.3x | **2.8%** | **2.4%** | **10.2%** |
| Randstad | $5.7B | $22.9B | 20.8x | 11.3x | 12.0x | 1.9% | 1.2% | 7.4% |
| Adecco | $3.6B | $23.2B | 12.3x | 8.4x | 8.7x | 2.0% | 1.3% | 8.6% |
| Kelly | $0.5B | $4.1B | n/m | 9.0x | 8.8x | 0.4% | −6.4% | −24.1% |
| Kforce | $1.0B | $1.3B | 29.7x | 20.0x | 20.5x | 3.6% | 2.6% | 27.1% |

Two things jump out. **First, MAN is the second-largest revenue base
($18.7B) trading at the second-smallest market cap ($2.4B)** among this
group — a function of razor-thin net margins (0.6%) turning modest revenue
swings into large earnings swings, which is exactly what a 32%-in-a-day
move looks like mechanically. **Second, Kforce and RHI post the best
margins/ROE in the group** by specializing (Kforce: pure-play tech/finance
staffing; RHI: see Q4 below) rather than competing as a diversified
generalist the way MAN, Randstad, and Adecco do.

## Q3. What is the business model?

MAN is not one business — it's a portfolio of staffing brands sold through
four geographic segments (Americas, Northern Europe, Southern Europe, Asia
Pacific Middle East), with Europe historically the largest base (France is
~71% of Southern Europe revenue alone):

- **Manpower** — the core brand: temporary/contract staffing, blue- and
  grey-collar heavy. This is the brand management flagged as driving the
  Q2 beat.
- **Experis** — professional/IT staffing (higher skill, higher bill rate).
- **Talent Solutions** — RPO (recruitment process outsourcing), TAPFIN
  (managed service provider for a client's entire contingent workforce),
  and Right Management (career transition/outplacement consulting).

The economics, laid bare in the P&L (`main.py` section 4):

| FY | Revenue | Gross margin | Operating margin | Net margin | Net income |
|----|--------:|--------------:|------------------:|-----------:|-----------:|
| 2022 | $19.8B | 18.0% | 3.2% | 1.9% | $374M |
| 2023 | $18.9B | 17.8% | 1.6% | 0.5% | $89M |
| 2024 | $17.9B | 17.3% | 1.7% | 0.8% | $145M |
| 2025 | $18.0B | 16.7% | 1.3% | −0.1% | −$13M |

MAN keeps roughly **17 cents of gross profit per revenue dollar** — the
markup on billed labor after paying the worker — and runs **~16 cents of
SG&A** (recruiters, branch offices, back office) against it. **The entire
operating profit lives in the 1–3 cent sliver left over**, which is why a
7.5% revenue swing (like Q2's) can flip net income from −$67M to +$54M:
this is an operating-leverage business, not a high-margin one. It is,
in Buffett's vocabulary, closer to **a labor-intensive distribution
business** than a business with pricing power — you are selling *access to
workers*, a service that is genuinely useful but structurally hard to mark
up.

## Q4. Moat — does MAN have one?

Run the numeric test across the closest comps (operating margin by year):

| | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|
| MAN | 3.2% | 1.6% | 1.7% | 1.3% |
| RHI | **13.5%** | 7.3% | 4.2% | 1.4% |
| Randstad | 4.1% | 3.5% | 2.1% | 2.4% |
| Adecco | 2.2% | 2.5% | 2.2% | 2.3% |
| Kelly | 1.4% | 0.6% | 1.5% | 0.6% |

**Buffett's moat test is simple: does anyone sustain a margin the rest of
the industry can't compete away?** By 2025 the answer across this table is
mostly no — everyone has converged to a 0.6%–2.4% band as the downturn
squeezed pricing. The one name that stood apart, RHI, only did so on the
back of **Protiviti**, its risk/consulting/technology-advisory arm — a
genuinely different business bolted onto a staffing shell, not a staffing
moat. Protiviti now represents more than a quarter of RHI's revenue,
carries multi-quarter engagements (unlike temp placements, which can be
cancelled with a week's notice), and lets RHI redeploy Talent Solutions
contractors into Protiviti projects — a real structural advantage
"ManpowerGroup or Randstad... lack."

**MAN's own candidate moats are weak by comparison:**
- *Scale/brand* — real (Manpower is one of the most recognized staffing
  brands globally, 70+ countries) but scale hasn't produced a durable
  margin edge versus Randstad, which is larger still.
- *Switching costs via TAPFIN/RPO* — the strongest candidate. Managed
  service provider contracts are multi-year, embedded in a client's HR
  ops, and genuinely sticky. But this is a small slice of total revenue,
  not the core Manpower brand that drove the Q2 beat.
- *AI transformation ($200M in targeted permanent cost savings by 2028,
  IBM/SoundHound partnerships)* — this is a cost-out and product initiative,
  not a moat; it may restore margin to 2022 levels but doesn't change the
  competitive structure.

**The honest verdict: MAN operates in a commodity-service industry with no
durable pricing moat.** It is a decent-to-good operator of a bad-economics
business, and the current re-rating is the market pricing "less bad," not
"structurally advantaged." That said, staffing is also genuinely useful and
non-obsolete (someone has to match temp labor to seasonal demand), so this
is a "no moat, but not going away" verdict — closer to an airline or a
commodity producer than to a business Buffett would call a "wonderful
company at a fair price."

## Q5. How is management?

CEO **Jonas Prising** has run MAN since 2014 (Chairman since 2015) — over a
decade of tenure through two full cycles (2015–2019 expansion, 2020 COVID
crash, 2022–2025 downturn, now a 2026 recovery), which is itself a data
point in a industry known for shorter CEO tenures.

**Capital allocation record** (`main.py` section 6, $M):

| FY | FCF | Dividends paid | Buybacks | Shares out | Total debt |
|----|----:|----:|----:|----:|----:|
| 2022 | $348 | $140 | $270 | 51.3M | $1,253 |
| 2023 | $270 | $144 | $180 | 48.3M | $1,326 |
| 2024 | $258 | $146 | $140 | 47.4M | $1,330 |
| 2025 | −$161 | $67 | $38 | 46.1M | $2,089 |

Two reads, one favorable and one that should be a flag:

- **Favorable:** the share count has shrunk every year (51.3M → 46.1M,
  ~10% over 4 years) and buybacks were heaviest in the good years (2022–23)
  and cut hardest as conditions worsened (2024–25) — the textbook *correct*
  sequencing (buy less when cash flow is scarce and the stock's cheapness
  is uncertain), not the common sin of buying back stock at cycle highs on
  autopilot.
- **The flag:** FCF went **negative (−$161M) in 2025** while total debt
  nearly doubled (**$1.33B → $2.09B**) and, in **May 2025, the board cut
  the semiannual dividend 53%** (to $0.72/share) — a genuine, admitted
  capital-allocation stress point, not managed around. The dividend was
  held flat (not cut further) at the May 2026 declaration, consistent with
  the Q2 recovery narrative, but a 33-year-plus dividend streak (paid since
  1994) being cut at all is a material data point for anyone using dividend
  continuity as a management-quality proxy.

**On strategy:** the $200M-by-2028 cost program (with $20M of back-office
savings flagged for 2026 and $80M of front-office redesign beginning 2027)
and AI tooling reportedly scaling to ~70% of revenue by year-end reads as
a sensible, incremental response to a genuine industry threat (see Q4) —
management is not denying the AI-disintermediation risk, it's restructuring
around it. That is more credible than a management team promising the
downturn was purely macro and nothing will change.

**Verdict: competent, cycle-tested, shareholder-conscious management that
hit a real air pocket in 2025** — buybacks throttled back appropriately,
but the debt increase and dividend cut mean this was not a business that
sailed through the downturn on its balance sheet strength; it needed the
board to act.

## Q6. Price — is MAN fairly valued?

The valuation table (`main.py` section 7) is the whole ballgame for a
cyclical, because the "right" P/E depends entirely on which year's earnings
you annualize:

| Earnings basis | EPS | P/E | Earnings yield |
|---|---:|---:|---:|
| TTM (still includes 2025's loss quarters) | $2.22 | 23.6x | 4.2% |
| Q2-26 adjusted, annualized (4 × $0.99) | $3.96 | 13.2x | 7.6% |
| Q3-26 guide midpoint, annualized (4 × $1.01) | $4.04 | 13.0x | 7.7% |
| Mid-cycle (2022's $374M net income ÷ shares) | $8.04 | **6.5x** | **15.4%** |

The spread from 23.6x to 6.5x on the *same stock, same day* is the entire
lesson of valuing a cyclical: **the P/E you compute depends on which
earnings you believe are "normal."**

- If you believe **2025 was the trough and 2026 is the new steady state**
  (Q2/Q3 run-rate, ~$4/share), MAN at 13x with a 7.6% earnings yield is
  reasonably priced for a no-moat, low-margin business — neither obviously
  cheap nor expensive.
- If you believe **2022's $374M/8.04-EPS year is closer to mid-cycle**
  (pre-downturn, but also pre-AI-disruption), MAN at **6.5x / 15.4% earnings
  yield** is statistically cheap — the kind of multiple that shows up on
  cyclicals right as the market fears the trough is structural.
- The **forward P/E of 10.8x** (consensus-based, section 3) sits between
  these two anchors, implying Wall Street currently expects something
  closer to the Q2/Q3 run-rate than a full 2022-style recovery — a
  reasonable, non-euphoric expectation.

**The Buffett-style read:** paying 6–13x for a business with no durable
moat, 0.6–2% net margins, and a live structural risk (AI disintermediating
recruiting — the exact thing hitting RHI, MAN, and Randstad per multiple
2026 analyst downgrades) is not "wonderful company, fair price" — it's
"fair-to-mediocre company, statistically cheap price, real balance-sheet
stress evidenced by the 2025 dividend cut." That can still be a sound value
bet (cyclical low-multiple recoveries are a legitimate value strategy — see
Adecco at an even cheaper 8.4x forward and 12.3x trailing) but it is a bet
on cycle-timing and AI-risk resolution, not on a durable competitive
advantage compounding for decades. The 32% pop was the market moving from
pricing "2025 repeats forever" toward "2022 partially returns" — reasonable
given the data, but it used up the easiest re-rating; the multiple's
remaining discount at 13x reflects real, still-unresolved AI risk rather
than pure mispricing.

## Verdict on the hypothesis

1. **The 32% pop** is a legitimate cyclical-trough re-rating (first
   profitable quarter after a loss, guidance raised) on a stock still 49%
   below its 2018 high and already roughly double its 52-week low set
   *before* the print — momentum, not a re-rating of the underlying
   franchise.
2. **Competitors:** MAN is the second-biggest revenue base in a
   commodity-margin industry, trading at the cheapest multiple of the
   group's larger names; RHI and Kforce show the only real differentiation
   (specialization/consulting), and the whole sector has trailed the S&P by
   50–100 points over five years.
3. **Business model:** a volume-and-spread business on billed labor — ~17%
   gross margin, ~16% SG&A, profit lives in a 1–3% sliver highly levered to
   hiring volume.
4. **Moat:** effectively none. Operating margins across MAN, Randstad, and
   Adecco converged to a 1–2.4% commodity band by 2025; the one outlier
   (RHI) earned it via a bolted-on consulting business, not staffing
   itself. AI-driven recruitment disintermediation is a live, industry-wide
   threat, not a MAN-specific weakness.
5. **Management:** decade-plus tenured, cycle-tested, and shareholder-
   conscious on buybacks (correctly throttled back in the downturn) — but
   2025 forced a genuine 53% dividend cut and a near-doubling of debt,
   evidence this cycle actually hurt, not just optics.
6. **Price:** statistically cheap on mid-cycle earnings (6.5x, 15.4%
   earnings yield) and reasonably priced on a Q2/Q3 run-rate basis (13x,
   7.6%) — fair-to-cheap for what it is, which is a moat-less, thin-margin
   cyclical facing a real structural question, not a wonderful business on
   sale.

## Sources

- [Yahoo Finance — Why ManpowerGroup (MAN) stock is trading up today](https://finance.yahoo.com/markets/stocks/articles/why-manpowergroup-man-stock-trading-203322721.html)
- [RTTNews — ManpowerGroup stock surges 32% after returning to Q2 profit](https://www.rttnews.com/story.aspx?Id=3667730)
- [GuruFocus — ManpowerGroup (MAN) stock soars 27% on strong Q2 earnings report](https://www.gurufocus.com/news/8963007/manpowergroup-man-stock-soars-27-on-strong-q2-earnings-report)
- [Investing.com — Earnings call transcript: ManpowerGroup tops Q2 2026 estimates as stock jumps](https://www.investing.com/news/transcripts/earnings-call-transcript-manpowergroup-tops-q2-2026-estimates-as-stock-jumps-93CH-4796068)
- [Investing.com — ManpowerGroup Q2 2026 slides: revenue beats as recovery broadens](https://www.investing.com/news/company-news/manpowergroup-q2-2026-slides-revenue-beats-as-recovery-broadens-93CH-4796129)
- [PR Newswire — ManpowerGroup reports 2nd quarter 2026 results](https://www.prnewswire.com/news-releases/manpowergroup-reports-2nd-quarter-2026-results-302827010.html)
- [ManpowerGroup — Jonas Prising leadership bio](https://www.manpowergroup.com/en/about/leadership/jonas-prising)
- [Investing.com SWOT — ManpowerGroup's dividend cut signals workforce stock challenges](https://www.investing.com/news/swot-analysis/manpowergroups-swot-analysis-dividend-cut-signals-workforce-stock-challenges-93CH-4063558)
- [ManpowerGroup — Declares semi-annual dividend (2026)](https://www.manpowergroup.com/en/news-releases/news/manpowergroup-declares-semi-annual-dividend)
- [American Staffing Association — Top 5 staffing trends to watch for 2026](https://americanstaffing.net/posts/2026/01/06/top-5-staffing-trends-to-watch-for-2026/)
- [Staffing Industry Analysts — Could AI disrupt staffing firms when it comes to recruiting?](https://www.staffingindustry.com/editorial/healthcare-staffing-report/could-ai-disrupt-staffing-firms-when-it-comes-to-recruiting-)
- [Bloomberg / Detroit News — AI threatens staffing industry as companies bring recruitment in-house](https://eu.detroitnews.com/story/business/2026/02/18/ai-threatens-staffing-industry-as-companies-bring-recruitment-in-house/88738387007/)
- [Umbrex — ManpowerGroup strategy and business model](https://umbrex.com/resources/company-profiles/manpowergroup/)
- [Simply Wall St — Does Robert Half (RHI) capture durable value from shifting labor-market optimism?](https://simplywall.st/stocks/us/commercial-services/nyse-rhi/robert-half/news/does-robert-half-rhi-capture-durable-value-from-shifting-lab/amp)
- [BeyondSPX — Robert Half reports Q4/FY2024 results, Protiviti continues growth](https://www.beyondspx.com/quote/RHI/news/robert-half-reports-fourth-quarter-and-full-year-2024-financial-results-protiviti-continues-growth)
