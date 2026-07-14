# Hyperscaler bonds: parking spot or trade? (data as of 2026-07-13)

## 1. The premise, checked

The issuance number is real. Alphabet, Amazon, Meta, Microsoft and Oracle sold
~$159B of bonds in the first five months of 2026 alone — more than the prior
five years combined ([CNBC](https://www.cnbc.com/2026/02/23/big-techs-ai-bond-binge-shatters-unspoken-contract-with-investors.html),
[Yahoo Finance](https://finance.yahoo.com/news/ai-hyperscalers-drive-higher-us-225314460.html)).
Add Nvidia's $25B debut (June, spreads tightened from ~90bp guidance to ~65bp
on $85B of orders — [Bloomberg](https://www.bloomberg.com/news/articles/2026-06-15/nvidia-kicks-off-first-high-grade-bond-offering-since-2021))
and SpaceX's $25B inaugural deal (June, five tranches 5.35%–6.65%, ~$89B of
orders — [SpaceX IR](https://ir.spacex.com/updates/releases-details/2026/SpaceX-Announces-Pricing-of-25-Billion-Inaugural-Bond-Issuance-2026-33VwNgsx3O/default.aspx),
[CNBC](https://www.cnbc.com/2026/06/23/spacex-debt-bond-market-ipo.html)) and
the cohort in the hypothesis is in the $210–250B range — "~$244B" is fair.
Street estimates for the full year run $230–300B ([UBS via Yahoo](https://finance.yahoo.com/news/ai-hyperscalers-drive-higher-us-225314460.html)).

The spread ranking is roughly right too, with one correction: **Oracle, not
Meta, is the widest** — S&P cut it to BBB- citing AI capex, and its CDS traded
at levels last seen in 2009 ([Fortune](https://fortune.com/2026/03/07/big-tech-trillion-dollar-borrowing-ai-century-bonds/)).
Among the AA-ish names the order is Meta > Amazon > Alphabet, and Amazon's
July 7 deal needed 18–21bp of extra concession on weak (2.5x) books —
supply is straining even the best names ([Fortune](https://fortune.com/2026/07/08/amazons-25-billion-surprise-bond-sale-dangled-extra-yield-to-lure-in-buyers/)).

## 2. What the live data says (from `main.py`, run 2026-07-13)

**Spreads (ICE BofA OAS, FRED):**

| Bucket | Latest | Since Sep-2025 | YTD |
|---|---|---|---|
| AA (Alphabet/Amazon/Meta/Nvidia proxy) | 55bp | **+12bp** | +6bp |
| BBB (Oracle proxy) | 96bp | -1bp | -5bp |
| 10y Treasury yield | 4.56% | **+40bp** | +37bp |

The AA bucket is the one that widened since the issuance wave began — that IS
the hyperscaler supply premium showing up. But note what dominates: the 10-year
Treasury moved +40bp. **Rate moves, not credit, drive short-term P&L on these
bonds.**

**"Park $10,000 for one month, every month" — 2026 YTD total return in dollars:**

| Month | SGOV (T-bills) | VCSH (short corp) | LQD (~8.4y dur) | VCLT (~12.9y dur) |
|---|---|---|---|---|
| Jan | +29 | +40 | +34 | +47 |
| Feb | +28 | +56 | +138 | +185 |
| Mar | +29 | **-83** | **-207** | **-290** |
| Apr | +30 | +38 | +28 | +33 |
| May | +30 | +27 | +86 | +154 |
| Jun | +30 | +17 | +11 | +23 |
| Jul (MTD) | +15 | -37 | **-159** | **-253** |
| **Total** | **+$191, 0 losing months** | +$58 | **-$69** | **-$101** |

The duration that matches the new hyperscaler 10y paper (LQD) **lost money**
as a monthly parking vehicle in 2026 while plain T-bills made $191 with zero
losing months. The long tranches (VCLT) were worse.

**Friction at $10k retail size (one-month hold of an individual bond):**

| Bond | Extra carry vs T-bills | Round-trip bid-ask | Loss if spreads +10bp |
|---|---|---|---|
| Alphabet/Amazon/Meta/Nvidia 10y area (~4.9%) | ~$9/mo | $20–50 | ~-$80 |
| Oracle 10y (~5.6%) | ~$15/mo | $20–50 | ~-$75 |
| SpaceX 2036 (~5.9%) | ~$17/mo | $20–50 | ~-$77 |

One month of extra carry does not even cover the retail bid-ask. Breakeven on
transaction costs alone is 3–6 months, and a routine 10bp adverse move erases
5–9 months of carry. **Monthly in-and-out of individual hyperscaler bonds is
structurally negative expected value at $10k size.**

## 3. Verdict

- **As a monthly parking spot: no.** "Parking" means capital preservation +
  liquidity. These are 8–40 year duration instruments; in 2026 they've been
  4–10x more volatile than T-bills for ~100bp of extra yield. T-bills/SGOV at
  ~3.9% are the correct parking vehicle and won every single month YTD.
- **As a trade: legitimate, but it's a different bet.** You'd be betting that
  (a) the AA supply premium (+12bp) compresses once issuance slows, and/or
  (b) 10y Treasury yields fall. That pays on a 6–24 month horizon, not monthly.
  The Amazon July concession (18–21bp) shows new issues price cheap — the
  institutional edge is buying new deals and flipping; retail rarely gets
  allocations on these deals.
- **Risk worth naming:** the whole cohort is levering up simultaneously for
  the same bet (AI capex, ~$770B in 2026). Correlated downgrades (Oracle
  already BBB-) would widen everything at once — exactly when you'd want out.

## 4. How an individual actually buys/sells these bonds

1. **Individual bonds** — Fidelity, Schwab, E*TRADE, Vanguard, IBKR bond desks.
   Search by issuer or CUSIP, $1,000 face minimums, live dealer quotes
   ([Fidelity](https://www.fidelity.com/fixed-income-bonds/individual-bonds/corporate-bonds/overview),
   [Schwab](https://www.schwab.com/bonds/individual-bonds/corporate-bonds)).
   Expect 0.2–0.5pt round-trip bid-ask at $10k size; check the same CUSIP's
   institutional prints on [FINRA TRACE](https://www.finra.org/finra-data/fixed-income)
   before accepting a quote.
2. **ETFs** — no way to buy a pure "hyperscaler bond" basket, but LQD/VCIT
   (these issuers are now ~4% of the IG index and rising) give the exposure
   with penny-wide spreads and instant exit.
3. **Taxes matter**: coupon income is ordinary income; T-bill/SGOV income is
   state-tax-exempt, corporate coupons are not — the after-tax pickup is even
   smaller than the pre-tax $9–17/month.

## 5. The $10k test plan (6 months, falsifiable)

Split the stake so the experiment measures what actually matters — realized
retail friction and relative performance:

| Sleeve | $ | What it tests |
|---|---|---|
| SGOV | $4,000 | Control: the null hypothesis ("just park in T-bills") |
| One individual bond, e.g. SpaceX 5.875% 2036 or Meta 10y (2 bonds, $2k face) | $2,000 | Realized bid-ask: record quoted bid AND ask at purchase; get an indicative bid monthly |
| LQD or VCIT | $2,000 | The liquid version of the same bet |
| Cash reserve | $2,000 | Add to the individual bond only if AA OAS widens >15bp (buy the dip test) |

Rules: log month-end values of each sleeve for 6 months (re-run `main.py` for
the benchmark data); the hypothesis survives only if a corporate sleeve beats
SGOV **after** measured transaction costs. Pre-registered prediction from the
data above: SGOV wins unless 10y Treasury yields fall >25bp over the window.

## 6. ADOPTED PLAN — parking $10,000 for one year (as of 2026-07-13)

The horizon changed from "monthly" to "one year", which changes the answer:
with a known 12-month horizon, **maturity-match instead of rolling short**.

Rate landscape at adoption:

| Vehicle | Rate | Notes |
|---|---|---|
| Rolling 3-mo T-bills / SGOV | ~3.85% | Floats down if the Fed cuts |
| 1-year Treasury bill (DGS1) | **4.06%** | Locked, state-tax-exempt, zero credit risk |
| Best 12-month CDs | 4.10–4.55% | FDIC-insured; state-taxable, early-withdrawal penalty ([CD Valet](https://www.cdvalet.com/best-12-month-cd-rates), [CNBC Select](https://www.cnbc.com/select/best-certificates-of-deposits/)) |
| Short IG corporate maturing ~mid-2027 | ~4.4–4.6% | Amazon/Alphabet/Apple-type 2027 paper, held to maturity |

The curve is upward-sloping (1-mo 3.71% → 1-y 4.06%): the market pays extra to
commit for a year, and a lock also wins if the Fed cuts. Rationale for the
corporate sleeve: a bond that **matures at the horizon** exits at par — no
bid-ask on the way out, no duration risk — the only version of the hyperscaler
thesis that survived the friction math in section 2.

**Allocation:**

| Sleeve | $ | Instrument | Why |
|---|---|---|---|
| Core lock | 6,000 | 1-year T-bill at auction (~4.06%) | State-tax-exempt (~4.3–4.5% CD-equivalent in a 6–9% tax state); no penalty if sold early |
| Credit pickup | 2,000 | One IG note maturing ~mid-2027 (Amazon/Alphabet 2027, ~4.4–4.6%) | Held to maturity → keeps the spread with zero exit friction |
| Liquidity | 2,000 | SGOV or money-market fund | Never be forced to sell the other sleeves early |

Expected outcome: **~$410–440** on $10,000 over the year, vs ~$385 rolling
bills, with no principal risk to the horizon. Simpler alternative: 100% into
the 1-year T-bill (~$406, state-tax-free). Explicitly excluded: any bond with
duration beyond the horizon — the new 10–40y hyperscaler paper moves 2–8% on
a 40bp Treasury move and is a trade, not a parking spot.

**Review checkpoint:** re-run `main.py` at month-ends; the plan is wrong if
rolling 3-mo bills out-earn the 1-y lock (i.e., the Fed hikes instead of
cutting) or the corporate note's issuer is downgraded below single-A.
