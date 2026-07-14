# Hypothesis 003 — Hyperscaler bonds as a short-term parking spot

**Hypothesis:** Alphabet, Amazon, Meta, Oracle, Nvidia and SpaceX have issued
~$244B of bonds this year at yield premiums over Treasuries (Meta/Oracle widest).
Buying these bonds is a good way for an individual investor to park $10,000
short term — roughly month by month — and sell later for a profit.

**Verdict: REJECTED for "parking"; viable only as a multi-year hold or a
deliberate spread/duration trade.** See [ANALYSIS.md](ANALYSIS.md) for
sourcing and full detail.

## Why it's rejected

**Spreads (ICE BofA OAS, FRED, as of 2026-07-13):**

| Bucket | Latest | Since Sep-2025 | YTD |
|---|---|---|---|
| AA (Alphabet/Amazon/Meta/Nvidia proxy) | 55bp | **+12bp** | +6bp |
| BBB (Oracle proxy) | 96bp | -1bp | -5bp |
| 10y Treasury yield | 4.56% | **+40bp** | +37bp |

The AA bucket did widen as issuance ramped — that's the real supply premium.
But the 10-year Treasury moved +40bp, 3x that — rate moves, not credit,
dominate short-term P&L on these bonds.

**"Park $10,000 for one month, every month" — 2026 YTD total return:**

| Vehicle | Duration | Total $ | Worst month |
|---|---|---|---|
| SGOV (T-bills) | 0.1y | **+$191** | +$15, 0 losing months |
| VCSH (short corp) | 2.7y | +$58 | -$83 |
| LQD (~10y area, matches new hyperscaler paper) | 8.4y | **-$69** | -$207 |
| VCLT (30-40y tranches) | 12.9y | **-$101** | -$253 |

The duration bucket that matches the new hyperscaler paper *lost* money as a
monthly parking vehicle in 2026 while T-bills made $191 with zero losing
months.

**Retail friction on an individual $10k bond (one-month hold):**

| Bond | Extra carry vs T-bills | Round-trip bid-ask | Loss if spreads +10bp |
|---|---|---|---|
| Alphabet/Amazon/Meta/Nvidia 10y (~4.9%) | ~$9/mo | $20–50 | ~-$80 |
| Oracle 10y (~5.6%) | ~$15/mo | $20–50 | ~-$75 |
| SpaceX 2036 (~5.9%) | ~$17/mo | $20–50 | ~-$77 |

One month of extra carry doesn't cover the bid-ask; breakeven is 3–6 months,
and a routine 10bp spread move erases 5–9 months of it. Monthly in-and-out at
$10k size is structurally negative EV.

## Adopted plan (1-year horizon, §6 of ANALYSIS.md)

With a known 12-month horizon the answer flips: maturity-match instead of
rolling short, so the position exits at par with no bid-ask and no duration
risk.

| Sleeve | $ | Instrument | Why |
|---|---|---|---|
| Core lock | 6,000 | 1-year T-bill at auction (~4.06%) | State-tax-exempt; no penalty if sold early |
| Credit pickup | 2,000 | One IG note maturing ~mid-2027 (~4.4–4.6%) | Held to maturity → keeps the spread, zero exit friction |
| Liquidity | 2,000 | SGOV / money-market | Never forced to sell the other sleeves early |

Expected ~$410–440 on $10k, vs ~$385 rolling bills, with no principal risk at
the horizon. Wrong if rolling 3-mo bills out-earn the lock (Fed hikes) or the
IG note's issuer is downgraded below single-A — review at month-ends.

## Run it

```bash
uv sync
uv run python main.py
```

`main.py` pulls, live:

- ICE BofA option-adjusted spreads by rating bucket (FRED) — AA proxies
  Alphabet/Amazon/Meta/Nvidia, BBB proxies Oracle
- Treasury yields (3-month, 10-year)
- Total-return ETF prices (SGOV, VCSH, LQD, VCLT) and simulates parking
  $10,000 for one month at a time through 2026
- Friction math: extra carry vs. retail bid-ask cost vs. a 10bp spread move
  on an individual bond at $10k size

Raw data lands in `data/`.
