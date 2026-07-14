"""Test: are 2026 hyperscaler bonds a good place to park $10k short term (monthly)?

Issuers in scope: Alphabet, Amazon, Meta, Oracle, Nvidia, SpaceX (~$210-250B issued
globally this year across the cohort).

What this script checks with real data:
  1. Credit-spread context (FRED / ICE BofA OAS by rating bucket) - the rating
     buckets proxy the issuers: AA ~ Alphabet/Amazon/Meta/Nvidia, A ~ SpaceX area,
     BBB ~ Oracle.
  2. "Park money every month" simulation - monthly total returns of bond ETFs
     (SGOV T-bills as the parking benchmark, VCSH short IG corp, LQD intermediate
     IG corp, VCLT long corp) on a $10,000 stake.
  3. Friction math for buying individual hyperscaler bonds at retail size:
     does one month of extra carry over T-bills survive the bid-ask spread?

Writes raw data to data/ and a summary to stdout.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf

DATA_DIR = Path(__file__).parent / "data"
START = "2025-07-01"
STAKE = 10_000.0

FRED_SERIES = {
    "BAMLC0A2CAA": "AA OAS (Alphabet/Amazon/Meta/Nvidia proxy)",
    "BAMLC0A3CA": "Single-A OAS",
    "BAMLC0A4CBBB": "BBB OAS (Oracle proxy)",
    "BAMLC0A0CM": "All IG corporate OAS",
    "DGS3MO": "3-month T-bill yield",
    "DGS10": "10-year Treasury yield",
}

ETFS = {
    "SGOV": ("0-3mo T-bills (the honest 'parking' vehicle)", 0.1),
    "VCSH": ("Short-term IG corporates, ~2.7y duration", 2.7),
    "LQD": ("IG corporates, ~8.4y duration (new hyperscaler 10y area)", 8.4),
    "VCLT": ("Long IG corporates, ~12.9y duration (30-40y tranches)", 12.9),
}

# Retail friction assumptions for a single corporate bond trade (points of face).
RETAIL_BID_ASK_ROUND_TRIP = (0.20, 0.50)  # optimistic .. typical for $10k lots


def fred_series(series_id: str, start: str) -> pd.Series:
    """Fetch one FRED series as a float Series (fredgraph.csv, no API key)."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={start}"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    df = pd.read_csv(io.StringIO(resp.text), parse_dates=["observation_date"])
    s = pd.to_numeric(df.set_index("observation_date")[series_id], errors="coerce")
    return s.dropna()


def spread_context() -> pd.DataFrame:
    """Latest OAS/yield levels plus change since Sep-2025 (pre-wave) and YTD."""
    rows = []
    frames = {}
    for sid, label in FRED_SERIES.items():
        s = fred_series(sid, START)
        frames[sid] = s
        latest = s.iloc[-1]
        pre_wave = s[s.index <= "2025-09-30"].iloc[-1]  # before the Meta-led wave
        ytd_base = s[s.index <= "2026-01-02"].iloc[-1]
        rows.append(
            {
                "series": sid,
                "what": label,
                "latest_%": latest,
                "date": s.index[-1].date(),
                "chg_since_Sep25_bp": round((latest - pre_wave) * 100),
                "chg_YTD_bp": round((latest - ytd_base) * 100),
            }
        )
    pd.DataFrame(frames).to_csv(DATA_DIR / "fred_spreads.csv")
    return pd.DataFrame(rows).set_index("series")


def monthly_parking_sim(prices: pd.DataFrame) -> pd.DataFrame:
    """$10k parked for one calendar month at a time, every month of 2026."""
    month_end = prices.resample("ME").last()
    monthly = month_end.pct_change().dropna(how="all")
    monthly = monthly[monthly.index >= "2026-01-01"]
    dollars = (monthly * STAKE).round(0)
    dollars.index = dollars.index.strftime("%Y-%m")
    return dollars


def friction_table(t_bill_yield: float) -> pd.DataFrame:
    """One-month economics of holding an individual hyperscaler bond vs T-bills.

    Carry uses indicative new-issue yields (July 2026): ~4.9% for the AA-ish
    10y area (Alphabet/Amazon/Meta/Nvidia), ~5.6% Oracle-ish BBB, ~5.9% SpaceX
    long tranches. Price risk uses duration x a modest 10bp spread move.
    """
    bonds = [
        ("Alphabet/Amazon/Meta/Nvidia 10y area", 4.9, 8.0),
        ("Oracle 10y area (BBB)", 5.6, 7.5),
        ("SpaceX 2036 tranche", 5.9, 7.7),
    ]
    rows = []
    for name, ytm, dur in bonds:
        extra_carry = STAKE * (ytm - t_bill_yield) / 100 / 12
        cost_lo = STAKE * RETAIL_BID_ASK_ROUND_TRIP[0] / 100
        cost_hi = STAKE * RETAIL_BID_ASK_ROUND_TRIP[1] / 100
        ten_bp_hit = STAKE * dur * 0.0010
        rows.append(
            {
                "bond": name,
                "ytm_%": ytm,
                "extra_carry_$/mo": round(extra_carry, 0),
                "bid_ask_cost_$": f"{cost_lo:.0f}-{cost_hi:.0f}",
                "loss_if_+10bp_$": round(-ten_bp_hit, 0),
                "months_to_breakeven_on_costs": round(cost_hi / extra_carry, 1)
                if extra_carry > 0
                else float("inf"),
            }
        )
    return pd.DataFrame(rows).set_index("bond")


def main() -> int:
    """Run the three checks and print a summary."""
    DATA_DIR.mkdir(exist_ok=True)

    print("=" * 78)
    print("1) CREDIT SPREAD CONTEXT (ICE BofA OAS via FRED)")
    print("=" * 78)
    spreads = spread_context()
    print(spreads.to_string())

    print()
    print("=" * 78)
    print("2) 'PARK $10,000 EVERY MONTH' SIMULATION, 2026 YTD (total return, $)")
    print("=" * 78)
    prices = yf.download(
        list(ETFS), start=START, interval="1d", auto_adjust=True, progress=False
    )["Close"]
    if prices is None or prices.empty:
        print("ERROR: no ETF price data returned", file=sys.stderr)
        return 1
    prices.to_csv(DATA_DIR / "etf_prices.csv")
    print(f"(prices through {prices.index[-1].date()}; last row is month-to-date)\n")

    sim = monthly_parking_sim(prices)
    sim = sim[[t for t in ETFS if t in sim.columns]]
    print(sim.to_string())

    print("\nPer-vehicle summary of those months:")
    summary = pd.DataFrame(
        {
            "role": [ETFS[t][0] for t in sim.columns],
            "total_$": sim.sum().round(0),
            "worst_month_$": sim.min().round(0),
            "negative_months": (sim < 0).sum(),
        }
    )
    print(summary.to_string())

    print()
    print("=" * 78)
    print("3) INDIVIDUAL-BOND FRICTION AT $10K RETAIL SIZE (one-month hold)")
    print("=" * 78)
    t_bill = spreads.loc["DGS3MO", "latest_%"]
    print(f"(vs parking in T-bills at {t_bill:.2f}%)\n")
    print(friction_table(float(t_bill)).to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
