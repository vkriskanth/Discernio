# Refining Strain, July 2026: Is the Tightness Still Tradable?

*Written 2026-07-18. All market numbers from `main.py` (yfinance daily data,
run 7/18 against the 7/17 close); news items sourced at the bottom. Framed,
per this repo's convention, as a hypothetical $10k exercise — not advice.*

## Q1. Is refining capacity strained with no fuel-market buffer? Yes — three stacked shocks

The premise is not just true, it is quantifiable, and it comes in three layers
moving at three speeds:

**Layer 1 — structural (years):** the US has permanently closed more than
1.2M b/d of refining capacity since 2019, including ~550k b/d in the last 18
months alone (Phillips 66 Wilmington, 139k b/d, closed end-2025; Valero
Benicia, 170k b/d, closed April 2026). The EIA forecasts gasoline + distillate
+ jet inventories ending 2026 at ~375M bbl — the lowest since 2000. Distillate
stocks sat 11–12% below their 5-year seasonal average through early July
(103.6M bbl week of 7/3).

**Layer 2 — war (months):** Ukrainian drone strikes have disabled ~40% of
Russia's designed refining capacity; the IEA estimates the war cut global
refinery output by ~4.5M b/d last quarter. On **7/8 Russia banned all diesel
exports** (nominally through 7/31) — Russia supplied ~11% of the world's
diesel last year, and its June product exports were already the lowest since
2016. European diesel margins printed a record $60/bbl on the announcement.

**Layer 3 — chokepoint (days):** over the weekend of 7/11–12, US and Iranian
forces exchanged strikes and Iran claimed closure of the Strait of Hormuz
(~20% of world oil + LNG). Kpler counted six tanker transits on 7/12, a
five-week low. WTI rose 9.4% on Monday 7/13 alone.

### The tape agrees — this is a refining shock, not an oil shock

YTD through 7/17: **ULSD +92%, RBOB +100%, vs WTI +44%** — products have
outrun crude two-to-one on every horizon. That ratio is the capacity-strain
premise in one line: the market is paying for refining, not for molecules of
crude. In spread terms (front-month, $/bbl):

| Crack | Today | 5-yr avg | 2022 peak | Percentile since 2018 |
|-------|------:|---------:|----------:|----------------------:|
| ULSD (HO−CL) | **$88.2** | $38.9 | $110.3 | 99th |
| RBOB (RB−CL) | **$60.0** | $25.7 | $59.7 | **100th — all-time high** |
| 3-2-1 | **$69.4** | $30.1 | $64.6 | **100th — above the 2022 peak** |

And the post-ban action **extended rather than faded** — the 3-2-1 went $58.9
(7/1) → $64.6 (ban day 7/8) → dipped to $61.9 → $69.4 (7/17) as Hormuz
stacked on top. Cumulative from the 7/7 pre-ban close: HO +23%, CL +17%,
VLO/MPC/PSX +16–17%, SPY −0.6%. When an event pop extends for seven sessions,
physical tightness — not headlines — is doing the pricing.

**Verdict on Q1: true, verified, and — critically for Q2/Q3 — priced at the
100th percentile.**

## Q2. Short-term bets on NYMEX CL / HO / RB?

A desk rule worth its weight: *when the fundamental story is at its most
obviously true, check what percentile you're being asked to pay.* Here it is
the 100th. That doesn't mean short it — it means the easy directional money
is gone, and what's left is structure.

### Decompose the price before betting on it

Today's HO at $4.06/gal = crude ($82.5, carrying a Hormuz war premium — WTI
was ~$71 on 7/7) + crack ($88, carrying a Russia-ban premium against a ban
that nominally **expires 7/31**). An outright long is a bet on both premiums
persisting; an outright short fights both physical scarcity and the calendar
below.

### What the strip already prices

| Contract | CL | ULSD crack | RBOB crack |
|----------|---:|-----------:|-----------:|
| Spot (7/17) | $82.5 | $88.2 | $60.0 |
| Sep 26 | $81.78 | $83.6 | $52.3 |
| Dec 26 | $77.65 | $69.9 | $31.0* |
| Mar 27 | $74.87 | $61.9 | $29.0* |

*\*winter-grade RBOB trades at a seasonal discount — the gasoline
backwardation overstates true normalization.*

Two readings:

1. **The market already prices partial normalization** — the Dec ULSD crack
   sits $18 under spot. You cannot "discover" the tightness thesis; it's on
   the screen.
2. **But only partial** — Dec at $70 is still ~80% above the $39 5-yr
   average. The strip is betting tightness persists into winter. If you hold
   the structural view, the *deferred* crack is the honest instrument (it
   carries the structure premium without the expiring event premiums).

### Why the "obvious" short is a trap

Mean reversion screams from the table above, but three things stand between
a short and the money:

- **Carry is against you.** Backwardation (HO spot $4.06 vs Sep $3.937) pays
  a rolling long ~3%/2 months if the curve merely stands still; a short pays
  that away — roughly 18%/yr of negative carry to fight.
- **The 2022 winter re-spike.** In the only precedent, the ULSD crack fell
  from $110 (April 2022) to $50 by September — and then re-spiked to $103 on
  10/28 as heating season hit low inventories. Shorts who were right for five
  months were carried out in week twenty-four.
- **Seasonal steamrollers ahead.** Hurricane season (August–September; the
  Gulf Coast is ~half of US refining) and the heating season both sit between
  now and year-end, with distillate stocks at 20-year lows as the buffer.

### The venue problem at $10k

One HO contract is 42,000 gal ≈ **$170k notional — 17x the stake**; there is
no micro ULSD contract and no US-listed ULSD ETP (UGA exists for gasoline,
USO for crude). At $10k, NYMEX futures are the wrong venue entirely — undersized
accounts express this trade through refiner equities (Q3) or not at all.
This repo's hypothesis-004 lesson was that identification ≠ monetization
because of *timing*; here the same gap opens because of *instrument size*.

### The short-term playbook (if one insists)

| Bet | Verdict |
|-----|---------|
| Outright long HO/RB/CL here | Late. Scenario math (below) runs ~3:1 against. |
| Naked short the crack | Fighting carry + two seasonal tails at 20-yr-low inventories. No. |
| Long Dec-26 ULSD crack (structure without event premium) | The defensible long — but you pay 80% over normal for it. Small. |
| Wait for event decay | **The desk trade.** 7/31 ban expiry or a Hormuz de-escalation headline should retrace cracks 15–30% (2022 analog: −30% in ~10 weeks). That air pocket — not today — is the entry for the winter-tightness trade. |

The event calendar to trade around: **7/31** Russia ban expiry/renewal;
**Wednesdays** EIA weeklies (the 7/10 report built distillate +4.6M bbl when
analysts expected −0.9M — the first crack in the bull tape, and cracks still
shrugged it off); **late July** refiner Q2 earnings; **Aug–Sep** hurricanes;
**October** heating season.

## Q3. Buy a group of refiners, especially diesel-levered? Yes-but — quality, half-size, and know what you're paying for

### What's already in the stocks

Every refiner but CVI closed 7/17 at its **exact 52-week high**:

| Ticker | YTD | Off 52-wk high | β (% move per $1 of 3-2-1) |
|--------|----:|---------------:|---------------------------:|
| VLO | +89% | 0% | 0.47 |
| MPC | +91% | 0% | 0.35 |
| PSX | +61% | 0% | 0.32 |
| PBF | +123% | 0% | 1.08 |
| DINO | +92% | 0% | 0.51 |
| DK | +115% | 0% | 0.46 |
| CVI | +40% | −12% | 0.74 |
| CRAK (ETF) | +43% | 0% | 0.21 |

Scenario P&L on $10k, using each stock's observed crack beta (3-2-1 now $69):

| Scenario (year-end) | 3-2-1 | Long HO | VLO | MPC | PSX | PBF | CRAK |
|--------------------|------:|--------:|----:|----:|----:|----:|-----:|
| Mean-revert to 5-yr avg | $30 | −$2,304 | −$1,842 | −$1,374 | −$1,275 | −$4,241 | −$818 |
| Halfway back | $50 | −$1,152 | −$921 | −$687 | −$638 | −$2,120 | −$409 |
| Hold here | $69 | $0 | $0 | $0 | $0 | $0 | $0 |
| Winter +20% | $83 | +$813 | +$650 | +$485 | +$450 | +$1,497 | +$289 |

The asymmetry is ~3:1 against fresh longs *if stocks track cracks*.

### But refiners are not cracks — the 2022 analog

Here is the nuance that changes the answer from "no" to "yes-but." Buying
refiners **on the exact day the 2022 crack peaked** (4/28/22, 3-2-1 at
$64.6):

| From 4/28/22 entry | Worst dip | ~4.5 mo later | ~7.5 mo | ~13 mo |
|--------------------|----------:|--------------:|--------:|-------:|
| 3-2-1 crack itself | — | **−57%** ($28) | $31 | $38 |
| VLO | −12% | −7% | **+6%** | +3% |
| MPC | −11% | +8% | **+26%** | +31% |
| PSX | −9% | −4% | **+20%** | +17% |
| CRAK | −12% | −8% | +1% | +4% |

The crack *halved* and the equities went *up* over any 6-month-plus horizon.
Why: the market never capitalizes spot cracks (that's what betas of 0.3–0.5
mean — CRAK is +43% YTD against a crack +130%), so when cracks normalize,
the stocks give back a dip, not the rally. What the equities actually price
is the **level** of mid-cycle margins — and permanently closed capacity
raises that level. Equity is the venue where the *structural* layer of Q1
pays, while futures are the venue where the *event* layers (which expire)
get priced. That is the deepest reason the answer to Q2 is "mostly no" and
Q3 is "yes-but."

### The diesel question specifically

Diesel is the right molecule for the structural leg: Russia's ban is a diesel
ban, distillate inventories are the tightest, heating season is the next
demand wave, and gasoline's all-time-high crack faces demand destruction and
its seasonal cliff (Dec RBOB crack: $31). Ranked as diesel expressions:

- **VLO** — the cleanest large-cap play: largest merchant refiner, Gulf
  Coast distillate skew (Q1-26 USGC distillate margin $27.60/bbl vs $16.69 a
  year prior), β 0.47.
- **MPC** — biggest system + the buyback machine; lowest drawdown risk in
  the 2022 analog (+26% at 7.5 mo). β 0.35.
- **PSX** — most diversified (midstream/chem cushion), management explicitly
  pitching distillate-heavy operations and export capability. β 0.32.
- **PBF (β 1.08) / DK (0.46 but small)** — pure torque: the +20% scenario
  pays +$1,497 on $10k, mean reversion costs −$4,241. That's a sleeve, not a
  position.
- **CVI** — the only name not at its high (−12%); cheapness here has
  historically come with RIN/small-refinery idiosyncrasies. Pass.

### The playbook

1. **Basket, not single name; quality, not torque.** VLO + MPC + PSX (or
   simply CRAK) — hypothesis-004's lesson transfers exactly: quality
   absorbed a mistimed entry, high-beta punished it.
2. **Half now, half on the air pocket.** Entry at the 52-week high into Q2
   earnings pays full headline price. The 2022 analog says a −9% to −12% dip
   arrived within three months of the crack peak; the 7/31 ban expiry and
   any Hormuz de-escalation are the likely triggers. Stage the second half
   there.
3. **The stop is fundamental, not technical:** two consecutive EIA weeks of
   distillate builds toward the 5-yr average (the 7/10 report was the first)
   plus a lapsed Russia ban = the thesis expiring; the remaining tightness
   is then hurricane/winter optionality you're overpaying for.
4. **What would make this a table-pounding buy:** cracks retrace 20–30%
   while distillate stays >8% below average into September — structure
   intact, event premium flushed. That's the 2022 September setup that
   preceded the October re-spike.

## Verdict on the hypothesis

1. **Strained capacity, no buffer — TRUE**, three stacked shocks
   (structural closures + Russia's refining war-loss + Hormuz), verified in
   a tape where products doubled crude's move and every crack sits at the
   99th–100th percentile.
2. **Short-term NYMEX bets — mostly no.** The tightness is on the screen at
   record levels; outright longs run ~3:1 against, shorts fight 18%/yr of
   carry plus two seasonal tails, and at $10k the contracts are 17x the
   stake anyway. The tradable moment is the *event-decay air pocket* (7/31
   ban expiry / Hormuz de-escalation), not today.
3. **Refiner basket, diesel-levered — yes-but.** Equities are the correct
   venue for the structural (persistent) layer of the thesis — 2022 proved
   they keep their gains through a crack collapse — but at 52-week highs the
   entry is half-size in quality names (VLO/MPC/PSX or CRAK), completed on
   the first event-driven dip, with a fundamental stop on inventory
   normalization.

## Sources

- [EIA — Refinery closures and rising consumption will reduce US petroleum inventories in 2026](https://www.eia.gov/todayinenergy/detail.php?id=64644)
- [EIA — US total distillate inventories forecast to end 2025 and 2026 at multiyear lows](https://www.eia.gov/todayinenergy/detail.php?id=66124)
- [EIA — Short-Term Energy Outlook, July 2026](https://www.eia.gov/outlooks/steo/report/petro_prod.php)
- [BIC Magazine — Refinery closures and their impact on US fuel supply in 2026](https://www.bicmagazine.com/industry/refining-petrochem/refinery-closures-and-their-impact-on-us-fuel-supply/)
- [IndexBox — Refining margins for gasoline and diesel hit record highs in July 2026](https://www.indexbox.io/blog/refining-margins-for-gasoline-and-diesel-hit-record-highs-in-july-2026/)
- [CME Group — Fresh from the Trading Room, 7/14/26: Papering over the cracks](https://www.cmegroup.com/newsletters/fresh-from-the-trading-room/2026-07-14.html)
- [Bloomberg — Russia bans diesel exports after Ukraine's refinery attacks (7/8)](https://www.bloomberg.com/news/articles/2026-07-08/russia-bans-diesel-exports-after-ukraine-s-refinery-attacks)
- [OilPrice — Russia bans diesel exports amid heavy Ukraine attacks on refineries](https://oilprice.com/Latest-Energy-News/World-News/Russia-Bans-Diesel-Exports-Amid-Heavy-Ukraine-Attacks-On-Refineries.html)
- [Moscow Times — Russia bans diesel exports to ensure domestic supply](https://www.themoscowtimes.com/2026/07/08/russia-bans-diesel-exports-to-ensure-domestic-supply-after-targeted-ukrainian-drone-strikes-a93202)
- [IndexBox — Russia's fuel export ban and Ukraine attacks reshape clean tanker markets](https://www.indexbox.io/blog/russias-fuel-export-ban-and-ukraine-attacks-reshape-clean-tanker-markets/)
- [DiscoveryAlert — Russia's diesel export ban and the 2026 global supply crunch](https://discoveryalert.com.au/russia-diesel-export-ban-global-supply-crunch-2026/)
- [Al Jazeera — Oil prices jump as US and Iran trade attacks over Strait of Hormuz (7/13)](https://www.aljazeera.com/economy/2026/7/13/oil-prices-jump-as-us-and-iran-trade-attacks-over-strait-of-hormuz)
- [Yahoo Finance — Oil prices rise more than 3% amid new US–Iran strikes near Hormuz](https://finance.yahoo.com/energy/articles/oil-prices-rise-more-3-105659641.html)
- [Tank Transport — Fuel supply crunch: 7 critical warning signs as crude cools](https://tanktransport.com/2026/07/fuel-supply-crunch/)
- [Yahoo Finance — Marathon Petroleum rallies 52% in 6 months](https://finance.yahoo.com/markets/stocks/articles/marathon-petroleum-rallies-52-6-143100068.html)
- [Yahoo Finance — Refiners are quiet winners in 2026](https://finance.yahoo.com/news/refiners-quiet-winners-2026-wall-152554757.html)
- [Simply Wall St — 3 refining stocks with strong diesel exposure after Russia export ban](https://simplywall.st/stocks/us/energy/nyse-psx/phillips-66/news/3-refining-stocks-with-strong-diesel-exposure-after-russia-e)
- [24/7 Wall St — Forget oil prices: this one refining number explains why these stocks are on fire](https://247wallst.com/investing/2026/07/15/forget-oil-prices-this-1-refining-number-explains-why-these-energy-stocks-are-on-fire/)
- [EnergyNow — US refiners' Q1 profits expected to jump as war lifts fuel margins](https://energynow.com/2026/04/us-refiners-first-quarter-profits-expected-to-jump-as-war-lifts-fuel-margins/)
- [FreightWaves — As prices fall, crack spread signals a split in oil markets](https://www.freightwaves.com/news/as-prices-fall-crack-spread-signals-a-split-in-oil-markets)
- [Commodity Board — Oil forward curve flattens as geopolitics clash with softening demand](https://commodity-board.com/oil-forward-curve-flattens-as-geopolitics-clash-with-softening-demand)
