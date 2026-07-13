"""Deal math for the NBCUniversal acquisition and the 2026 spin-offs.

Inputs are real, sourced figures:
  - Acquisition cost: SEC filings / press coverage of the 2011 and 2013 GE deals
  - FY2025 segment revenue & Adjusted EBITDA: Comcast FY2025 10-K (filed 2026-02-03,
    accession 0001628280-26-004994), saved in data/cmcsa_10k_2025.htm
  - Prices: data/prices.csv from market_data.py (run that first)
  - Versant EBITDA/market cap: yfinance

Outputs: acquisition return math, spin-announcement price reaction, and an
illustrative sum-of-parts range for the NBCU spinco (clearly labeled estimates).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yfinance as yf

DATA = Path(__file__).parent / "data"

# --- NBCUniversal acquisition cost (nominal $B) ---
COST_2011_51PCT = 13.8   # Jan 2011: 51% stake from GE (cash + contributed assets)
COST_2013_49PCT = 16.7   # Mar 2013: remaining 49% from GE
COST_2013_30ROCK = 1.4   # Mar 2013: 30 Rock + CNBC Englewood Cliffs real estate
TOTAL_COST = COST_2011_51PCT + COST_2013_49PCT + COST_2013_30ROCK

# --- FY2025 segment results, Comcast 10-K ($M) ---
FY25 = {
    "Residential Connectivity & Platforms": {"rev": 70_704, "ebitda": 26_653},
    "Business Services Connectivity": {"rev": 10_237, "ebitda": 5_725},
    "Media (incl. Versant until 1/2/26)": {"rev": 27_090, "ebitda": 3_196},
    "Studios": {"rev": 11_286, "ebitda": 1_099},
    "Theme Parks": {"rev": 9_836, "ebitda": 3_080},
}
CE_TOTAL_EBITDA = 6_467  # Content & Experiences incl. HQ/eliminations ($M)
CE_TOTAL_REV = 45_559


def _print_sum_of_parts(media_ex_versant: float, studios: float, parks: float) -> None:
    print("\nIllustrative sum-of-parts for NBCU spinco (EBITDA x peer multiple, $B):")
    print("  NOTE: estimates. Sky is included in the announced spinco but its EBITDA")
    print("  is reported inside Connectivity & Platforms, so it is EXCLUDED here.")
    media_label = f"Media ex-Versant (~${media_ex_versant:.1f}B EBITDA)"
    ranges = {
        media_label: (media_ex_versant, 5, 7),
        f"Studios (${studios:.1f}B EBITDA)": (studios, 9, 11),
        f"Theme Parks (${parks:.1f}B EBITDA)": (parks, 9, 12),
    }
    total_lo = total_hi = 0.0
    for label, (ebitda, mlo, mhi) in ranges.items():
        lo, hi = ebitda * mlo, ebitda * mhi
        total_lo += lo
        total_hi += hi
        print(f"  {label:46s} {mlo:>2d}-{mhi:<2d}x -> ${lo:5.1f} - ${hi:5.1f}B")
    print(f"  {'Total enterprise value (ex-Sky, ex-HQ costs)':46s}       -> "
          f"${total_lo:5.1f} - ${total_hi:5.1f}B")


def main() -> None:
    """Print NBCU acquisition return math and spin-related valuation estimates."""
    print(f"NBCU total acquisition cost 2011-2013: ${TOTAL_COST:.1f}B (nominal)")
    print(f"  = ${COST_2011_51PCT}B (51%, 2011) + ${COST_2013_49PCT}B (49%, 2013)"
          f" + ${COST_2013_30ROCK}B (30 Rock real estate)")

    ce_yield = CE_TOTAL_EBITDA / 1000 / TOTAL_COST * 100
    print(f"\nFY2025 Content & Experiences Adjusted EBITDA: "
          f"${CE_TOTAL_EBITDA / 1000:.1f}B"
          f" -> {ce_yield:.0f}% annual EBITDA yield on original cost")

    # --- Spin announcement reaction (June 29, 2026) ---
    prices = pd.read_csv(DATA / "prices.csv", index_col=0, parse_dates=True)
    cmcsa = prices["CMCSA"].dropna()
    pre = cmcsa[cmcsa.index <= "2026-06-26"].iloc[-1]
    post = cmcsa[cmcsa.index >= "2026-06-30"].iloc[0]
    latest = cmcsa.iloc[-1]
    print("\nCMCSA around June 29, 2026 spin announcement:")
    print(f"  close 2026-06-26: ${pre:.2f}   first close after: ${post:.2f} "
          f"({(post/pre-1)*100:+.1f}%)   latest: ${latest:.2f} "
          f"({(latest/pre-1)*100:+.1f}% vs pre-announcement)")

    # --- Versant: value already returned to holders ---
    vsnt = yf.Ticker("VSNT").info
    vsnt_cap = (vsnt.get("marketCap") or 0) / 1e9
    vsnt_ebitda = (vsnt.get("ebitda") or 0) / 1e9
    print(f"\nVersant (VSNT): market cap ${vsnt_cap:.1f}B, TTM EBITDA "
          f"${vsnt_ebitda:.1f}B (1 VSNT per 25 CMCSA shares)")

    # --- Illustrative sum-of-parts for the NBCU spinco (ex-Sky perimeter) ---
    # Media EBITDA ex-Versant: FY25 Media includes Versant networks (spun 1/2/26).
    media_all = FY25["Media (incl. Versant until 1/2/26)"]["ebitda"] / 1000
    media_ex_versant = media_all - vsnt_ebitda
    parks = FY25["Theme Parks"]["ebitda"] / 1000
    studios = FY25["Studios"]["ebitda"] / 1000
    _print_sum_of_parts(media_ex_versant, studios, parks)

    cmcsa_cap = (yf.Ticker("CMCSA").info.get("marketCap") or 0) / 1e9
    print(f"\nComcast market cap today: ${cmcsa_cap:.1f}B — the whole company trades"
          f" near the\nhigh end of the estimated value of its media assets alone.")


if __name__ == "__main__":
    main()
