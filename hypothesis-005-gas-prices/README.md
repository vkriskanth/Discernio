# Hypothesis 005: Refining Strain & Fuel Prices

**Hypothesis:** (1) refining capacity is strained and fuel markets have
little buffer; (2) that's tradable short-term via NYMEX futures (CL crude,
HO ULSD, RB RBOB); (3) a basket of refiners — especially diesel-levered
ones — is a good buy.

**Verdict (see [ANALYSIS.md](ANALYSIS.md)):** true / mostly-no / yes-but.

- The strain is real and quantifiable — three stacked shocks: ~1.2M b/d of
  permanent US capacity closures since 2019, Russia's total diesel-export
  ban (7/8, after strikes disabled ~40% of its refining), and the US–Iran
  Hormuz escalation (7/13). Products are +92–100% YTD vs crude +44%; every
  crack sits at the 99th–100th percentile since 2018 and the 3-2-1 ($69.4)
  is **above its 2022 peak**.
- But that means the thesis is priced. Outright NYMEX longs run ~3:1
  against on scenario math; shorts fight ~18%/yr of backwardation carry
  plus hurricane and heating seasons with distillate at 20-year lows. And
  at $10k one HO contract is 17x the stake — futures are the wrong venue
  entirely. The tradable moment is the event-decay air pocket (7/31 ban
  expiry / Hormuz de-escalation), not today.
- Refiners are the better expression because equities price *mid-cycle
  margin levels*, not spot cracks: bought on the exact day the 2022 crack
  peaked, VLO/MPC/PSX dipped only 9–12% and were +6% to +26% within 8
  months while the crack itself halved. Still: every name is at its 52-week
  high, so — quality basket (VLO/MPC/PSX or CRAK), half now, half on the
  first event-driven dip, fundamental stop on distillate inventories
  normalizing.

## Run it

```bash
uv sync
uv run python main.py
```

Pulls fresh prices (yfinance) for CL/BZ/HO/RB futures, seven refiners, and
context ETFs, then prints:

1. the tape — levels and momentum showing products outrunning crude,
2. crack spreads vs history — today's ULSD/RBOB/3-2-1 vs the 2022 spike and
   their 2018+ percentiles,
3. an event study around the 7/8 Russia diesel-ban (extension vs fade),
4. the futures strip — how much crack normalization Sep/Dec/Mar contracts
   already price,
5. refiner scorecard — YTD, distance from highs, crack beta, and $10k
   scenario P&L if cracks mean-revert / hold / spike.

Raw downloads land in `data/`.
