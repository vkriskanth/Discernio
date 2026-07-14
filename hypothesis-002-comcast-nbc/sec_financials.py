"""Pull Comcast's annual financials from SEC EDGAR company facts (XBRL).

Gives the 2010-2025 revenue / net income / operating cash flow trend so we can
judge what the NBCUniversal acquisition (2011/2013, ~$31.9B) produced.
Saves data/cmcsa_annual.csv.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

CIK = "0001166691"  # Comcast Corp
URL = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json"
HEADERS = {"User-Agent": "discernio research vkriskanth@gmail.com"}

TAGS = {
    "revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"],
    "net_income": ["NetIncomeLoss"],
    "op_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment"],
    "dividends_paid": ["PaymentsOfDividendsCommonStock", "PaymentsOfDividends"],
    "buybacks": ["PaymentsForRepurchaseOfCommonStock"],
}

DATA_DIR = Path(__file__).parent / "data"


def annual_series(facts: dict, tags: list[str]) -> dict[int, float]:
    """Extract full-year (FY, ~365-day duration) USD values, latest filing wins."""
    out: dict[int, float] = {}
    for tag in tags:
        units = facts.get("us-gaap", {}).get(tag, {}).get("units", {})
        for item in units.get("USD", []):
            if item.get("form") not in ("10-K", "10-K/A"):
                continue
            start, end = item.get("start"), item.get("end")
            if not start or not end:
                continue
            days = (pd.Timestamp(end) - pd.Timestamp(start)).days
            if not 350 <= days <= 380:
                continue
            year = pd.Timestamp(end).year
            out.setdefault(year, item["val"])  # first tag with data wins
        if out:
            break
    return out


def main() -> int:
    """Fetch SEC EDGAR XBRL facts, build the annual financials table, save/print it."""
    DATA_DIR.mkdir(exist_ok=True)
    resp = requests.get(URL, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    facts = resp.json()["facts"]

    table = {name: annual_series(facts, tags) for name, tags in TAGS.items()}
    df = pd.DataFrame(table).sort_index()
    # pylint's astroid can't infer pandas' dynamic __getitem__, so this reads as
    # unsubscriptable even though boolean-mask indexing is standard DataFrame usage.
    df = df[df.index >= 2009] / 1e9  # pylint: disable=unsubscriptable-object  # $B
    df["fcf"] = df["op_cash_flow"] - df["capex"]
    df = df.round(2)

    print("Comcast annual financials from SEC EDGAR ($B):")
    print(df.to_string())
    df.to_csv(DATA_DIR / "cmcsa_annual.csv")

    ni = df["net_income"].dropna()
    print(f"\nCumulative net income {int(ni.index[0])}-{int(ni.index[-1])}: "
          f"${ni.sum():,.0f}B")
    fcf = df["fcf"].dropna()
    print(f"Cumulative FCF {int(fcf.index[0])}-{int(fcf.index[-1])}: "
          f"${fcf.sum():,.0f}B")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
