# Hypothesis 004: The July 2026 Chip Sell-Off

**Hypothesis:** the 7/13/2026 chip rout (NVDA -3.5%, SNDK -13%, MU -4.3%,
MRVL -7.8%, INTC -6.1%, AMD -4.1%) was identifiable in advance by a normal
retail investor using only free, public signals — early enough to make money
on a hypothetical $10k.

**Verdict (see [ANALYSIS.md](ANALYSIS.md)):** partially true.

- 7/13 was **not the start** — it was the fourth down-leg of a rout that began
  6/23. The identification problem was solvable 6–12 days early with free data
  (Seoul memory tape, the Meta compute-resale headline, Samsung's
  "sold-on-great-news" reaction).
- Making money on the **short side** was much harder than identifying it:
  only the earliest entry (7/2, day after the Meta headline) made real money
  (+$2,109 on $10k in SOXS). Entries on 7/7 or 7/8 — still six days "early" —
  **lost** money because of the 7/8–7/10 bounce and 3x-ETF decay.
- The reliable retail edge was **defensive** (stepping aside saved ~$790 per
  $10k of SOXX exposure) plus a planned **buy-the-capitulation** list, not
  fast shorting.
- The Seoul overnight tape (SK Hynix, Samsung) is a real leading signal, but
  **not** a short-at-the-open signal: on the 12 days Hynix fell >5% this year,
  US memory names gapped down ~4% before the open and averaged ~0% open-to-
  close. The move is priced before a US investor can click. Exception: the
  rare complacent open (7/2 — Hynix -14.6%, US opened flat, then fell 6-15%
  intraday).
- The **7/14 rebound** (MU +4.9%, INTC +4.5%, AMD +2.6%, MRVL +2.3%) proved
  the same lesson in reverse: Seoul's overnight bounce (Hynix +3.7%) flagged
  the turn by 2:30am ET, but the US open gapped up 4.7–7.9% — more than the
  entire day's move — so chasing the 9:30 open **lost** money in everything
  but NVDA. The entries that captured the uptick were an overnight-session
  buy at ~7/13-close prices (+$260 to +$488 per $10k in one day) or an
  index/leader-grade limit ladder already filled; single-name ladders on
  high-beta names (MRVL -$882) filled a week before the bottom.

## Run it

```bash
uv sync
uv run python main.py
```

Pulls fresh prices (yfinance) for the sold-off names, SOXX/SOXS, and the Seoul
bellwethers (SK Hynix, Samsung), then prints:

1. the daily tape since 6/22 — when the sell-off actually started,
2. a leading-indicator scorecard — the date each free signal fired vs 7/13,
3. reaction-speed P&L — $10k into SOXS at each realistic detection date,
4. the Seoul-signal study — on >5% Hynix down days, how much of the US move
   was gapped away by the open vs still capturable intraday,
5. the rebound study — the 7/14 bounce decomposed into gap vs open-to-close,
   $10k long-entry P&L per route (overnight session, open chase, earlier
   dip-buys), and the pre-set capitulation ladder marked to market.

Raw downloads land in `data/`.
