"""Pull real market data for Comcast and streaming/entertainment peers.

Verifies the hypothesis claims:
  - "Comcast shares are down 30% over past year"
  - relative positioning vs Netflix, Google (YouTube), Disney, WBD, etc.

Writes a summary table to stdout and saves raw prices to data/prices.csv.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yfinance as yf

TICKERS = {
    "CMCSA": "Comcast",
    "VSNT": "Versant (spun-off cable nets)",
    "NFLX": "Netflix",
    "GOOGL": "Alphabet (YouTube)",
    "DIS": "Disney",
    "WBD": "Warner Bros. Discovery",
    "PSKY": "Paramount Skydance",
    "FOX": "Fox Corp",
    "CHTR": "Charter (cable peer)",
    "SPY": "S&P 500 ETF",
}

DATA_DIR = Path(__file__).parent / "data"


def pct(a: float, b: float) -> float:
    return (a / b - 1.0) * 100.0


def main() -> int:
    DATA_DIR.mkdir(exist_ok=True)

    prices = yf.download(
        list(TICKERS), period="5y", interval="1d", auto_adjust=True, progress=False
    )["Close"]
    if prices is None or prices.empty:
        print("ERROR: no price data returned", file=sys.stderr)
        return 1

    prices.to_csv(DATA_DIR / "prices.csv")
    last_date = prices.index[-1]
    print(f"Price data through: {last_date.date()}\n")

    rows = []
    for tkr, name in TICKERS.items():
        if tkr not in prices.columns:
            continue
        s = prices[tkr].dropna()
        if s.empty:
            continue
        latest = s.iloc[-1]

        def trailing(
            days: int, s: pd.Series = s, latest: float = latest
        ) -> float | None:
            cutoff = s.index[-1] - pd.Timedelta(days=days)
            past = s[s.index <= cutoff]
            return pct(latest, past.iloc[-1]) if not past.empty else None

        rows.append(
            {
                "ticker": tkr,
                "name": name,
                "last": round(latest, 2),
                "1y_%": trailing(365),
                "2y_%": trailing(730),
                "5y_%": pct(latest, s.iloc[0]),
                "from_5y_high_%": pct(latest, s.max()),
                "first_data": s.index[0].date(),
            }
        )

    df = pd.DataFrame(rows).set_index("ticker")
    for col in ["1y_%", "2y_%", "5y_%", "from_5y_high_%"]:
        df[col] = df[col].map(lambda v: round(v, 1) if v is not None else None)
    print(df.to_string())

    # Market caps and valuation snapshot
    print("\n--- Valuation snapshot ---")
    vrows = []
    for tkr, name in TICKERS.items():
        if tkr == "SPY":
            continue
        try:
            info = yf.Ticker(tkr).info
        except Exception as exc:  # noqa: BLE001
            print(f"{tkr}: info fetch failed ({exc})", file=sys.stderr)
            continue
        vrows.append(
            {
                "ticker": tkr,
                "mkt_cap_$B": round((info.get("marketCap") or 0) / 1e9, 1),
                "trailing_PE": info.get("trailingPE"),
                "fwd_PE": info.get("forwardPE"),
                "EV/EBITDA": info.get("enterpriseToEbitda"),
                "div_yield_%": info.get("dividendYield"),
                "rev_ttm_$B": round((info.get("totalRevenue") or 0) / 1e9, 1),
            }
        )
    vdf = pd.DataFrame(vrows).set_index("ticker")
    print(vdf.to_string())
    vdf.to_csv(DATA_DIR / "valuation.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
