# Hypothesis 003 — Hyperscaler bonds as a short-term parking spot

**Hypothesis:** Alphabet, Amazon, Meta, Oracle, Nvidia and SpaceX have issued
~$244B of bonds this year at yield premiums over Treasuries (Meta/Oracle widest).
Buying these bonds is a good way for an individual investor to park $10,000
short term — roughly month by month — and sell later for a profit.

**Verdict: REJECTED for "parking"; viable only as a multi-year hold or a
deliberate spread/duration trade.** See [ANALYSIS.md](ANALYSIS.md).

**Adopted plan (1-year horizon, §6 of ANALYSIS.md):** $6k 1-year T-bill
(~4.06%, state-tax-exempt) + $2k IG note maturing ~mid-2027 (held to
maturity) + $2k SGOV/money-market for liquidity. Expected ~$410–440 on
$10k with no principal risk at the horizon.

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
