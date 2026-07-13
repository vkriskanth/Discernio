# Trade Plan: $10K Defensive Dividend Collar on CMCSA

*Prepared 2026-07-13. Stock and Treasury data through Friday 2026-07-10 close;
option prices are last-trade (markets closed Sunday — re-quote live before entering,
bids/asks will differ). Companion to [VALUE-OR-TRAP.md](VALUE-OR-TRAP.md).
Educational analysis, not investment advice.*

## Mandate

- $10,000, primary goal: collect the dividend
- Hard floor: max loss ~5%
- Sell a call for side income
- Beat Treasuries (13-week bill = **3.69%**) intelligently

One terminology fix: the loss-limiting leg is a **bought put** (the right to sell at
a floor price). The **sold call** is the income leg. Long stock + long put + short
call = a **collar**.

## Market inputs (as of 2026-07-10 close)

- CMCSA $23.57 · dividend $1.32/yr ($0.33/qtr, 5.65% yield)
- Ex-div dates ~Oct 1, 2026 and ~Jan 2, 2027 fall inside the structure (last one
  was Jul 1 — just missed)
- Jan 15, 2027 options (187 days): $22.50 put last $2.02 · $25 call last $1.83 ·
  $24 call last $1.90
- Earnings July 23, 2026 — inside the structure, so the floor protects through it

## The trade (primary): Jan 2027 22.5/25 collar

| Leg | Qty | Price | Cash flow |
|---|---:|---:|---:|
| Buy CMCSA shares | 400 | $23.57 | -$9,428 |
| Buy Jan-15-2027 $22.50 puts | 4 | ~$2.02 | -$808 |
| Sell Jan-15-2027 $25.00 calls | 4 | ~$1.83 | +$732 |
| Net options cost | | | **-$76** |
| Residual cash → money market @3.7% | | | $496 |

Expected dividends: 2 payments × $0.33 × 400 = **$264** (Oct + Jan ex-div).

### Outcomes at Jan 15, 2027 expiry (~6.2 months)

| Scenario | Stock P&L | Options | Dividends | Total | Return on $10K |
|---|---:|---:|---:|---:|---:|
| Stock ≤ $22.50 (**worst case**) | -$428 | -$76 | +$264 | **-$240** | **-2.4%** |
| Flat at $23.57 | $0 | -$76 | +$264 | +$188 | +1.9% (~3.7% ann.) |
| Stock ≥ $25 (called away) | +$572 | -$76 | +$264 | **+$760** | **+7.6% (~15% ann.)** |

Read the three rows against the mandate:

- **Max loss -2.4%** — half the 5% budget, and it's a *hard* floor (the put is a
  contract, not a stop order that can gap through). The floor holds even if the
  July 23 earnings print is a disaster.
- **Flat = Treasury**. If CMCSA goes nowhere for six months you earn ~3.7%
  annualized — the T-bill rate. You give up nothing to make this bet.
- **The edge is the upside band.** The stock only needs to drift back to $25 —
  still 22% below its 52-week high of $31.99, still ~5x earnings — to return ~15%
  annualized. Per VALUE-OR-TRAP.md, consensus targets sit at $40+ and the
  sum-of-parts says $36; you're not paying for any of that, just harvesting the
  first $1.43 of it.

So the intelligent-vs-Treasury framing: **you risk 2.4 points to own a 6-month
window where flat matches the bill and any drift upward multiples it.**

### Income-tilted variant (higher odds, lower cap)

Sell the **$24 call** ($1.90) instead of the $25: net options cost drops to $48,
max loss improves to **-2.1%**, cap falls to $24 → max total +$388 = **+3.9%
in 6.2 months (~7.7% annualized)**. The stock needs only +1.8% for you to double
the T-bill. Pick this if you want probability over magnitude.

### Why Jan 2027 expiry specifically

- **Dec 18, 2026** is more liquid (open interest: 22.5P 3,285 / 25C 3,990 / 26C
  2,189) but expires before the ~Jan 2 ex-div — you'd capture only one dividend
  ($132) and the static return falls *below* the T-bill. Rejected.
- **Beyond March 2027** runs into the mid-2027 NBCU+Sky spin: OCC will adjust any
  options that span the distribution (deliverable becomes CMCSA + spinco shares),
  the post-split dividend policy is unannounced, and adjusted options trade wide.
  Keep every leg expiring **before the spin**.
- Jan strikes showed thin weekend open interest — enter with **limit orders at
  mid**, legs as one collar ticket if the broker supports it, and don't chase.

## Execution and management rules

1. **Enter as a package** (buy-write + put, or stock then collar ticket) with limit
   orders. Re-quote Monday; if the net collar cost exceeds ~$0.40/share, widen the
   call strike or pass — the math above assumes ≈$0.19.
2. **Early-assignment watch.** If CMCSA trades above the short-call strike just
   before an ex-div date and the call's remaining time value is under $0.33, you
   will likely be assigned the day before ex-div and lose that dividend. Response:
   roll the call up/out *before* the ex-div date (Oct 1 is the first checkpoint).
3. **At expiry:** below $25, the shares are yours with the dividend banked — roll
   into a new collar (Apr/Jun 2027, still pre-spin) and repeat. Above $25, you're
   called away at +7.6%; that's a win, not a problem.
4. **Thesis check, not price check:** per VALUE-OR-TRAP.md the falsifier is
   broadband. If July 23 shows broadband losses re-accelerating or the Peacock
   profitability guide slips, let the collar run to the floor and don't roll.

## Honest costs of the structure

- **Tax:** a collar generally suspends the qualified-dividend holding period —
  dividends received while collared are taxed as **ordinary income**, and straddle
  rules defer loss recognition on the legs. In an IRA none of this matters; in a
  taxable account it shaves the edge.
- **Capped upside:** if the spinoff thesis reprices the stock to $30+ this year,
  you make 7.6%, not 30%. This structure monetizes *waiting*, not conviction. If
  you believe VALUE-OR-TRAP.md's bull case strongly, the collar is the wrong tool —
  plain stock is.
- **Dividend risk is deferred, not eliminated:** the $1.32 payout is well covered
  by connectivity EBITDA today, but post-split policy is unknown — one more reason
  every expiry here lands before mid-2027.

## Bottom line

Buy 400 CMCSA at ~$23.57, buy the Jan-2027 $22.50 puts, sell the Jan-2027 $25
calls, park the change in a money market. Worst case -2.4% (even through a bad
earnings print), flat case ≈ T-bill, drift-to-$25 case ≈ 15% annualized with two
dividends banked. That is the defensive, better-than-Treasuries expression of
"cheap stock, known risks, paid to wait."
