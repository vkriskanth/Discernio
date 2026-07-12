# Hypothesis 002: Comcast NBC Spinoff

## Hypothesis
1. Comcast decides to separate NBC Unit
2. Comcast shares are down 30% over past year
3. Google's youtube has become an entertaining behemoth
4. Subscription streaming led by netflix has become a profitable business
5. NBC Collection has Fast and Furious, Law and Order etc

Objective:
1. Why did they buy this in first place, at what price, is selling now a best option, Are they going to lose revenue?
2. Who is going to buy this?
3. What are the streams of revenue for comcast and do they have any play now competing against youtube and netflix
4. Will this be advantageous to comcast in the longer run
5. Who do you think will benefit the most buying NBC assets from comcast.

## Setup

```bash
uv sync
```

## Run

```bash
uv run python market_data.py      # live prices/valuations: CMCSA, VSNT, NFLX, GOOGL, DIS, WBD, PSKY... -> data/
uv run python sec_financials.py   # Comcast 2009-2025 annuals from SEC EDGAR -> data/cmcsa_annual.csv
uv run python deal_math.py        # acquisition-cost math, spin reaction, sum-of-parts (needs market_data.py first)
```

## Expected Outcome

Confirm or refute each premise with market/SEC data, and answer the five
objectives with sourced numbers rather than narrative.

## Notes — conclusions (full writeup in [ANALYSIS.md](ANALYSIS.md))

- **The separation is real and already underway**: Versant (cable networks) spun off
  Jan 2, 2026 (VSNT); on June 29, 2026 Comcast announced a tax-free spin of all of
  NBCUniversal + Sky, targeted mid-2027. CMCSA rose +6.0% on the announcement.
- **Premise check**: CMCSA -25.6% over 1yr (claim of -30% is close), -49% over 5yrs,
  trading at 4.6x trailing earnings. Fast & Furious / Law & Order are Universal
  IP and go with the NBCU spinco — premise directionally correct.
- **They bought well**: ~$31.9B total to GE (2011/2013). The media assets earned
  $6.5B Adjusted EBITDA in FY2025 alone — a ~20% annual yield on original cost.
- **Nobody "buys" it** — it's a spin to shareholders; a sale would trigger huge tax.
  Post-2029 the likeliest acquirer of NBCU assets is Netflix (it bid ~$72B for
  Warner and walked when Paramount Skydance won at $110.9B).
- **Sum-of-parts** on disclosed FY2025 EBITDA: media assets ≈ $42-56B ex-Sky, vs
  $84B market cap for all of Comcast — the conglomerate discount is the thesis.
- **Biggest beneficiary**: Comcast shareholders holding both pieces; biggest risk:
  RemainCo broadband competition (see Charter, -67% in a year), which no spin fixes.
