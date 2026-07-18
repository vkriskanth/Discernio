"""Test: refining capacity is strained and fuel markets have little buffer.

Is that (a) true, (b) tradable short-term via NYMEX futures (CL crude,
HO ULSD, RB RBOB gasoline), and (c) a reason to buy a basket of refiners,
especially diesel-levered ones?

Context being tested (July 2026): Russia banned all diesel exports on 7/8
after Ukrainian strikes disabled ~40% of its refining capacity; the US has
permanently closed ~550 kb/d of capacity in 18 months (P66 Wilmington,
Valero Benicia); distillate inventories sit ~11% below the 5-yr average.

What this script checks with real data:
  1. The tape - futures levels and momentum (1w/1m/3m/YTD) for CL, BZ, HO,
     RB, plus refiner equities and context ETFs. Products vs crude divergence.
  2. Crack spreads - daily ULSD crack, RBOB crack, and 3-2-1 since 2018;
     where today sits vs the 2022 spike and its own history (percentiles).
  3. Event study - day-by-day moves around the 7/8 Russia diesel-export ban:
     what repriced, how fast, and the follow-through since.
  4. Term structure - the futures strip for HO/RB/CL a few months out: how
     much crack normalization is already priced into deferred contracts.
  5. What refiners price in - each stock's distance from its 52-week high,
     its sensitivity (beta) to the 3-2-1 crack, and scenario P&L on $10k
     notional if cracks mean-revert vs stay elevated vs spike further.

Writes raw data to data/ and a summary to stdout.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yfinance as yf

DATA_DIR = Path(__file__).parent / "data"
START = "2018-01-01"  # covers the 2022 crack blowout for percentile context
BAN_DAY = "2026-07-08"  # Russia announces total diesel-export ban
STAKE = 10_000.0
BBL_GAL = 42

FUTURES = {
    "CL=F": "WTI crude (NYMEX)",
    "BZ=F": "Brent crude (ICE)",
    "HO=F": "NY Harbor ULSD (NYMEX)",
    "RB=F": "RBOB gasoline (NYMEX)",
}
REFINERS = {
    "VLO": "Valero",
    "MPC": "Marathon Petroleum",
    "PSX": "Phillips 66",
    "PBF": "PBF Energy",
    "DINO": "HF Sinclair",
    "DK": "Delek US",
    "CVI": "CVR Energy",
}
CONTEXT = {
    "CRAK": "VanEck Oil Refiners ETF",
    "XLE": "Energy Select SPDR",
    "SPY": "S&P 500",
}
ALL = {**FUTURES, **REFINERS, **CONTEXT}

# Deferred NYMEX contracts for the strip (Sep'26, Dec'26, Mar'27).
STRIP = {
    "CL": ["CLU26.NYM", "CLZ26.NYM", "CLH27.NYM"],
    "HO": ["HOU26.NYM", "HOZ26.NYM", "HOH27.NYM"],
    "RB": ["RBU26.NYM", "RBZ26.NYM", "RBH27.NYM"],
}
STRIP_LABELS = ["Sep26", "Dec26", "Mar27"]

# Publicly reported events a retail investor could have read the same day.
EVENTS = {
    "2025-12-31": "Phillips 66 permanently closes Wilmington CA (139 kb/d)",
    "2026-04-30": "Valero closes Benicia CA (170 kb/d)",
    "2026-07-03": "EIA week: distillate -5.0M bbl to 103.6M (~12% under 5-yr avg)",
    "2026-07-08": "RUSSIA BANS ALL DIESEL EXPORTS (drone strikes; ~40% capacity down)."
    " NYMEX 3-2-1 prints record $64.58/bbl",
    "2026-07-10": "EIA week: distillate +4.6M bbl build (still ~11% under 5-yr avg)",
}


def fetch_prices() -> pd.DataFrame:
    """Daily closes for futures, refiners, and context tickers."""
    raw = yf.download(
        list(ALL), start=START, auto_adjust=True, progress=False, group_by="column"
    )
    if raw is None or raw.empty:
        sys.exit("yfinance returned no data - check network")
    close = raw["Close"].dropna(how="all")
    missing = [t for t in ALL if t not in close or close[t].dropna().empty]
    for tkr in missing:  # transient yfinance cache-lock failures - retry singly
        retry = yf.download(tkr, start=START, auto_adjust=True, progress=False)
        if retry is not None and not retry.empty:
            close[tkr] = retry["Close"].iloc[:, 0]
    DATA_DIR.mkdir(exist_ok=True)
    close.to_csv(DATA_DIR / "close.csv")
    return close


def crack_frame(close: pd.DataFrame) -> pd.DataFrame:
    """Daily crack spreads in $/bbl from front-month futures closes."""
    cl, ho, rb = close["CL=F"], close["HO=F"], close["RB=F"]
    cracks = pd.DataFrame(
        {
            "ulsd_crack": ho * BBL_GAL - cl,
            "rbob_crack": rb * BBL_GAL - cl,
            "crack_321": (2 * rb * BBL_GAL + ho * BBL_GAL - 3 * cl) / 3,
        }
    ).dropna()
    cracks.to_csv(DATA_DIR / "cracks.csv")
    return cracks


def tape(close: pd.DataFrame) -> None:
    """Levels and momentum: is the strain visible in the tape?"""
    print("\n=== 1. The tape: levels and momentum ===")
    last = close.index[-1]
    rows = []
    for tkr, name in ALL.items():
        px = close[tkr].dropna()
        if px.empty:
            continue
        now = px.iloc[-1]

        def back(days: int, series: pd.Series = px, ref: float = now) -> float:
            cutoff = series.index[-1] - pd.Timedelta(days=days)
            base = series[series.index <= cutoff]
            return (ref / base.iloc[-1] - 1) * 100 if len(base) else float("nan")

        ytd = px[px.index >= "2026-01-01"]
        rows.append(
            {
                "ticker": tkr,
                "name": name,
                "last": round(now, 2),
                "1w_%": round(back(7), 1),
                "1m_%": round(back(30), 1),
                "3m_%": round(back(91), 1),
                "ytd_%": round((now / ytd.iloc[0] - 1) * 100, 1) if len(ytd) else None,
            }
        )
    print(f"(as of {last.date()})")
    print(pd.DataFrame(rows).to_string(index=False))
    print(
        "\n  Read: if products (HO, RB) are far ahead of crude (CL, BZ) on"
        "\n  every horizon, the market is paying for refining, not for oil -"
        "\n  the capacity-strain premise in one line."
    )


def crack_history(cracks: pd.DataFrame) -> None:
    """Where do today's cracks sit vs their own history?"""
    print("\n=== 2. Crack spreads vs history (front-month, $/bbl) ===")
    now = cracks.iloc[-1]
    stats = pd.DataFrame(
        {
            "today": now.round(1),
            "5yr_avg": cracks.loc["2021-07-01":].mean().round(1),
            "2022_peak": cracks.loc["2022"].max().round(1),
            "2026_high": cracks.loc["2026"].max().round(1),
            "pctile_since_2018": (cracks < now).mean().mul(100).round(0),
        }
    )
    print(stats.to_string())

    print("\nEvent tape a retail investor could read the same day:")
    for day, what in EVENTS.items():
        print(f"  {day}: {what}")
    print(
        "\n  Read: percentile near 100 means cracks are at/near record - the"
        "\n  strain is real AND already in the price. The 2022 column shows"
        "\n  the only precedent (post-Ukraine-invasion) and how it resolved."
    )


def event_study(close: pd.DataFrame, cracks: pd.DataFrame) -> None:
    """Day-by-day reaction to the 7/8 Russia diesel-export ban."""
    print("\n=== 3. Event study: the 7/8 Russia diesel-export ban ===")
    cols = ["CL=F", "HO=F", "RB=F", "VLO", "MPC", "PSX", "CRAK", "SPY"]
    pct = close[cols].pct_change() * 100
    window = pct.loc["2026-07-01":].round(1)
    window.index = [d.strftime("%m-%d %a") for d in window.index]
    print("\nDaily % moves since 7/1:")
    print(window.to_string())

    print("\nCrack levels ($/bbl) since 7/1:")
    cw = cracks.loc["2026-07-01":].round(1)
    cw.index = [d.strftime("%m-%d %a") for d in cw.index]
    print(cw.to_string())

    ban = pd.Timestamp(BAN_DAY)
    pre = close.index[close.index < ban][-1]
    lastd = close.index[-1]
    since = (close.loc[lastd, cols] / close.loc[pre, cols] - 1) * 100
    print(f"\nCumulative move {pre.date()} -> {lastd.date()} (pre-ban to now):")
    print(since.round(1).to_string())
    print(
        "\n  Read: did the ban-day pop hold, extend, or fade? Faded pops mean"
        "\n  the market judges the ban short-lived (it expires 7/31);"
        "\n  extension means physical tightness is doing the pricing."
    )


def term_structure() -> None:
    """Deferred contracts: how much normalization does the strip price?"""
    print("\n=== 4. Term structure: what the strip already prices ===")
    tickers = [t for chain in STRIP.values() for t in chain]
    raw = yf.download(
        tickers, period="5d", auto_adjust=True, progress=False, group_by="column"
    )
    if raw is None or raw.empty:
        print("(deferred-contract data unavailable from yfinance - skipping)")
        return
    closes = raw["Close"].ffill().iloc[-1]

    rows = []
    for label, (cl_t, ho_t, rb_t) in zip(
        STRIP_LABELS, zip(STRIP["CL"], STRIP["HO"], STRIP["RB"])
    ):
        cl, ho, rb = closes.get(cl_t), closes.get(ho_t), closes.get(rb_t)
        if pd.isna(cl) or pd.isna(ho):
            continue
        row = {
            "month": label,
            "CL_$": round(cl, 2),
            "HO_$gal": round(ho, 3),
            "ulsd_crack": round(ho * BBL_GAL - cl, 1),
        }
        if not pd.isna(rb):
            row["RB_$gal"] = round(rb, 3)
            row["rbob_crack"] = round(rb * BBL_GAL - cl, 1)
        rows.append(row)
    if not rows:
        print("(no deferred contracts returned - skipping)")
        return
    print(pd.DataFrame(rows).to_string(index=False))
    print(
        "\n  Read: a steeply backwardated HO strip = the market ALREADY prices"
        "\n  cracks normalizing; buying deferred tightness is not on offer."
        "\n  A flat strip = the market pays you to hold the tightness view."
    )


def refiner_beta(close: pd.DataFrame, cracks: pd.DataFrame) -> pd.Series:
    """%-move in each refiner per $1/bbl change in the 3-2-1 (weekly, 2024+)."""
    wk_crack = cracks["crack_321"].resample("W").last().diff().loc["2024":]
    betas = {}
    for tkr in list(REFINERS) + ["CRAK"]:
        wk_ret = close[tkr].resample("W").last().pct_change().loc["2024":] * 100
        joined = pd.concat([wk_ret, wk_crack], axis=1).dropna()
        if len(joined) > 30:
            x, y = joined.iloc[:, 1], joined.iloc[:, 0]
            betas[tkr] = x.cov(y) / x.var()
    return pd.Series(betas)


def priced_in(close: pd.DataFrame, cracks: pd.DataFrame) -> None:
    """Refiners: how much of the crack rally is already in the stocks?"""
    print("\n=== 5. Refiners: what's already priced, and scenario P&L ===")
    betas = refiner_beta(close, cracks)
    rows = []
    for tkr in list(REFINERS) + ["CRAK"]:
        px = close[tkr].dropna()
        if px.empty:
            continue
        hi52 = px[px.index >= px.index[-1] - pd.Timedelta(days=365)].max()
        ytd = px[px.index >= "2026-01-01"]
        rows.append(
            {
                "ticker": tkr,
                "ytd_%": round((px.iloc[-1] / ytd.iloc[0] - 1) * 100, 1),
                "off_52w_high_%": round((px.iloc[-1] / hi52 - 1) * 100, 1),
                "beta_%_per_$1_crack": round(betas.get(tkr, float("nan")), 2),
            }
        )
    print(pd.DataFrame(rows).to_string(index=False))

    now = cracks["crack_321"].iloc[-1]
    avg5 = cracks.loc["2021-07-01":, "crack_321"].mean()
    scenarios = {
        "cracks mean-revert to 5yr avg": avg5,
        "halfway back to normal": (now + avg5) / 2,
        "cracks hold here": now,
        "winter tightness: +20%": now * 1.2,
    }
    print(
        f"\n$10k notional P&L if the 3-2-1 (now ${now:.0f}) moves by year-end"
        " (stock move = beta x crack change; HO leg = crack change"
        " passed into the ULSD price at flat crude):"
    )
    cl_now, ho_now = close["CL=F"].iloc[-1], close["HO=F"].iloc[-1]
    picks = ["VLO", "MPC", "PSX", "PBF", "CRAK"]
    header = f"{'scenario':38} {'3-2-1':>6} {'long HO':>9} " + " ".join(
        f"{t:>7}" for t in picks
    )
    print(header)
    for label, target in scenarios.items():
        d_crack = target - now
        ho_target = cl_now + (ho_now * BBL_GAL - cl_now) + d_crack
        ho_pnl = STAKE * (ho_target / (ho_now * BBL_GAL) - 1)
        stock_pnls = [STAKE * betas.get(t, 0) * d_crack / 100 for t in picks]
        print(
            f"{label:38} {target:>5.0f}$ {ho_pnl:>+8,.0f}$ "
            + " ".join(f"{v:>+6,.0f}$" for v in stock_pnls)
        )
    print(
        "\n  Read: the asymmetry IS the trade decision. If mean reversion"
        "\n  costs 3-4x what further tightening earns, the long is late even"
        "\n  when the fundamental story is true (see hypothesis-004)."
    )


def main() -> None:
    """Run all five checks against fresh market data."""
    close = fetch_prices()
    cracks = crack_frame(close)
    tape(close)
    crack_history(cracks)
    event_study(close, cracks)
    term_structure()
    priced_in(close, cracks)


if __name__ == "__main__":
    main()
