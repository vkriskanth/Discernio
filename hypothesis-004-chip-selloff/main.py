"""Test: could a normal investor have identified the July 2026 chip sell-off
in time to make money on a hypothetical $10k?

The sell-off the hypothesis is about: 2026-07-13, when NVDA -3.5%, SNDK -13%,
MU -4.3%, MRVL -7.8%, INTC -6.1%, AMD -4.1% in one session.

What this script checks with real data:
  1. Timeline reconstruction - daily moves of the sold-off names, SOXX, and the
     Asian memory bellwethers (SK Hynix Seoul, Samsung Seoul) from mid-June on.
     Did 7/13 start the sell-off, or was it just the loudest day of one already
     in progress?
  2. Leading-indicator scorecard - signals a retail investor could have seen
     for free, and the date each one fired: NVDA rolling over from its 5/14
     peak, SK Hynix Seoul cracking after 6/25, SOXX losing its 50-day moving
     average, and the "sold on great news" tells (Micron 6/25 vs Samsung 7/7).
  3. Reaction-speed P&L - $10k moved into SOXS (3x inverse semis ETF) at the
     open after each realistic detection date, held to the 7/13 close, vs the
     honest alternatives: just stepping aside (selling SOXX), or doing nothing.
  4. Seoul-signal study - the Korean session ends ~2:30am ET, so a Hynix crash
     is knowable before the US open. On every >5% Hynix down day: how much of
     the US memory move was gapped away by the open (untradeable) vs how much
     followed through open-to-close (tradeable)?
  5. Rebound study - 7/14 bounced hard (MU +4.9%, INTC +4.5%, AMD +2.6%,
     MRVL +2.3%). Same questions in reverse: which free signals marked the
     turn, how much of the bounce was gapped away by the 9:30 open, and what
     each realistic $10k long entry (overnight session, open chase, pre-set
     limit ladder, earlier dip-buys) was worth at the 7/14 close.

Writes raw data to data/ and a summary to stdout.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yfinance as yf

DATA_DIR = Path(__file__).parent / "data"
START = "2026-04-01"
STAKE = 10_000.0
SELLOFF_DAY = "2026-07-13"
REBOUND_DAY = "2026-07-14"
HYNIX_CRASH = -5.0  # Seoul daily % move that counts as an overnight signal
LADDER = (-15, -22, -30)  # capitulation limit-order triggers, % below 2026 high
LADDER_PLACED = "2026-07-01"  # shopping list written the day the narrative broke

TICKERS = {
    "NVDA": "Nvidia",
    "AMD": "AMD",
    "MU": "Micron",
    "SNDK": "Sandisk",
    "MRVL": "Marvell",
    "INTC": "Intel",
    "SOXX": "iShares Semiconductor ETF",
    "SOXS": "Direxion Semis Bear 3X",
    "SPY": "S&P 500 (context)",
    "000660.KS": "SK Hynix (Seoul)",
    "005930.KS": "Samsung Electronics (Seoul)",
}

# Publicly reported events a retail investor could have read the same day.
EVENTS = {
    "2026-05-14": "NVDA all-time high (peak of the AI leadership)",
    "2026-06-25": "Micron +15% on blowout earnings; SK Hynix Seoul record high",
    "2026-07-01": "Report: Meta to resell idle AI compute (oversupply signal)",
    "2026-07-07": "Samsung prelim Q2: 19x profit jump SOLD 7-10% (sell-the-news tell)",
    "2026-07-08": "Sell-off deepens; memory supply-glut headlines",
    "2026-07-10": "SK Hynix $26.5B Nasdaq debut, +13% (biggest foreign US listing)",
    "2026-07-13": "SK Hynix Seoul plunges on resumption; US memory rout",
}

# (label, signal date visible to retail, first tradable US open after it)
ENTRY_SCENARIOS = [
    ("Tape reader: SOXX loses 50dma / NVDA downtrend", "2026-07-01", "2026-07-02"),
    ("News reader: Meta compute-resale headline", "2026-07-01", "2026-07-02"),
    ("News reader: Samsung sold on great news", "2026-07-07", "2026-07-07"),
    ("Slow news reader: next morning after Samsung", "2026-07-07", "2026-07-08"),
    ("Weekend reader: saw it Monday morning", "2026-07-13", "2026-07-13"),
]


def _repair_missing_day(
    close: pd.DataFrame, opens: pd.DataFrame, lows: pd.DataFrame, day: str
) -> None:
    """Rebuild a US session Yahoo's daily bars haven't posted yet from hourly bars.

    (As of 7/15 the daily endpoint still returns NaN for most US names on 7/14
    while the 60-minute bars are complete.)
    """
    ts = pd.Timestamp(day)
    if ts in close.index and not pd.isna(close.loc[ts, "SOXX"]):
        return
    us = [t for t in TICKERS if not t.endswith(".KS")]
    end = (ts + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    hourly = yf.download(
        us, start=day, end=end, interval="60m",
        auto_adjust=True, progress=False, group_by="column",
    )
    if hourly is None or hourly.empty:
        return
    fills = (
        (close, hourly["Close"].iloc[-1]),
        (opens, hourly["Open"].iloc[0]),
        (lows, hourly["Low"].min()),
    )
    for frame, row in fills:
        for tkr, val in row.items():
            frame.loc[ts, tkr] = val
        frame.sort_index(inplace=True)


def fetch_prices() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Daily close, open, low, and pct-change frames for all tickers."""
    raw = yf.download(
        list(TICKERS), start=START, auto_adjust=True, progress=False, group_by="column"
    )
    if raw is None or raw.empty:
        sys.exit("yfinance returned no data - check network")
    close = raw["Close"].dropna(how="all")
    opens = raw["Open"].dropna(how="all")
    lows = raw["Low"].dropna(how="all")
    _repair_missing_day(close, opens, lows, REBOUND_DAY)
    pct = close.pct_change() * 100
    DATA_DIR.mkdir(exist_ok=True)
    close.to_csv(DATA_DIR / "close.csv")
    opens.to_csv(DATA_DIR / "open.csv")
    lows.to_csv(DATA_DIR / "low.csv")
    return close, opens, lows, pct


def timeline(close: pd.DataFrame, pct: pd.DataFrame) -> None:
    """Daily % moves since mid-June: when did the sell-off actually start?"""
    us = ["NVDA", "AMD", "MU", "SNDK", "MRVL", "INTC", "SOXX"]
    seoul = ["000660.KS", "005930.KS"]
    window = pct.loc["2026-06-22":, us + seoul].round(1)
    window.index = [d.strftime("%m-%d %a") for d in window.index]
    print("\n=== 1. Daily % moves (US names + Seoul bellwethers) ===")
    print(window.to_string())

    print("\nEvent tape a retail investor could read the same day:")
    for day, what in EVENTS.items():
        print(f"  {day}: {what}")

    print("\nDrawdown from each name's 2026 high, as of key dates:")
    highs = close.loc["2026-01-01":].cummax()
    dd = (close / highs - 1) * 100
    checkpoints = ["2026-06-30", "2026-07-07", "2026-07-10", SELLOFF_DAY]
    rows = {}
    for c in checkpoints:
        idx = dd.index[dd.index <= c]
        if len(idx):
            rows[c] = dd.loc[idx[-1], us + seoul].round(1)
    print(pd.DataFrame(rows).to_string())


def indicator_scorecard(close: pd.DataFrame) -> None:
    """When did each free, public signal fire relative to 7/13?"""
    print("\n=== 2. Leading-indicator scorecard (all free/public) ===")
    selloff = pd.Timestamp(SELLOFF_DAY)
    rows = []

    nvda = close["NVDA"].dropna()
    peak_day = nvda.loc["2026-01-01":].idxmax()
    rows.append(
        (
            "NVDA below its 2026 peak (leadership rolling over)",
            peak_day,
            f"peaked {peak_day.date()}, "
            f"-{(1 - nvda.loc[:selloff].iloc[-1] / nvda.max()) * 100:.0f}% by 7/13",
        )
    )

    hynix = close["000660.KS"].dropna()
    hy_peak = hynix.loc["2026-01-01":].idxmax()
    hy_trigger = hynix[(hynix.index > hy_peak) & (hynix / hynix.max() < 0.90)]
    if not hy_trigger.empty:
        rows.append(
            (
                "SK Hynix Seoul -10% from record (memory bellwether cracks)",
                hy_trigger.index[0],
                f"peak {hy_peak.date()}, -10% crossed {hy_trigger.index[0].date()}, "
                f"{(hynix.loc[:selloff].iloc[-1] / hynix.max() - 1) * 100:.0f}%"
                " by 7/13",
            )
        )

    soxx = close["SOXX"].dropna()
    ma50 = soxx.rolling(50).mean()
    below = soxx[(soxx < ma50) & (soxx.index >= "2026-06-15")]
    if not below.empty:
        rows.append(
            (
                "SOXX closes below 50-day moving average",
                below.index[0],
                f"first close below on {below.index[0].date()}",
            )
        )

    rows.append(
        (
            "Meta compute-resale report (oversupply narrative)",
            pd.Timestamp("2026-07-01"),
            "public headline, same-day",
        )
    )
    rows.append(
        (
            "Samsung 19x profit jump sold 7-10% (positioning saturated)",
            pd.Timestamp("2026-07-07"),
            "the classic 'sold on great news' top signal",
        )
    )
    rows.append(
        (
            "SK Hynix $26.5B mega-listing (record supply of paper at the top)",
            pd.Timestamp("2026-07-10"),
            "biggest foreign US share sale ever; Alibaba 2014 echo",
        )
    )

    for name, fired, note in sorted(rows, key=lambda r: r[1]):
        lead = (selloff - fired).days
        print(f"  [{fired.date()}] {lead:>3}d before 7/13 | {name}")
        print(f"               {note}")


def reaction_pnl(close: pd.DataFrame, opens: pd.DataFrame) -> None:
    """$10k into SOXS at the open after each detection date, out at 7/13 close."""
    print("\n=== 3. Reaction-speed P&L on $10k (exit: 7/13 close) ===")
    exit_soxs = close.loc[SELLOFF_DAY, "SOXS"]
    exit_soxx = close.loc[SELLOFF_DAY, "SOXX"]
    print(
        f"{'scenario':52} {'entry':>10} {'SOXS 3x short':>14} {'stayed in SOXX':>15}"
    )
    for label, _seen, entry_day in ENTRY_SCENARIOS:
        idx = opens.index[opens.index >= entry_day]
        if idx.empty:
            continue
        entry = opens.loc[idx[0]]
        short_pnl = STAKE * (exit_soxs / entry["SOXS"] - 1)
        hold_pnl = STAKE * (exit_soxx / entry["SOXX"] - 1)
        print(
            f"{label:52} {idx[0].strftime('%m-%d'):>10}"
            f" {short_pnl:>+13,.0f}$ {hold_pnl:>+14,.0f}$"
        )
    print(
        "\n  'stayed in SOXX' = what doing nothing cost from that date; the gap"
        "\n  between columns is the value of stepping aside vs actively shorting."
    )

    us_close = close["SOXX"].dropna()
    last = us_close.index[-1]
    if last > pd.Timestamp(SELLOFF_DAY):
        after = (close.loc[last] / close.loc[SELLOFF_DAY] - 1) * 100
        cols = ["NVDA", "MU", "SNDK", "SOXX", "SOXS"]
        print(f"\nSince the 7/13 close (through {last.date()}):")
        print(after[cols].round(1).to_string())
    else:
        print("\n(No US close after 7/13 yet - rerun after today's close.)")


def seoul_signal_study(close: pd.DataFrame, opens: pd.DataFrame) -> None:
    """On >5% Hynix down days in Seoul: US gap at open vs open-to-close.

    The gap is the part of the move a US investor cannot trade (it prints in
    futures/pre-market while Seoul trades, 8pm-2:30am ET); open-to-close is
    what was still capturable by shorting at the 9:30am open.
    """
    print("\n=== 4. Seoul signal: what's left by the US open? ===")
    hynix_pct = close["000660.KS"].dropna().pct_change() * 100
    crash_days = hynix_pct[hynix_pct < HYNIX_CRASH]

    rows = []
    for day, hy_move in crash_days.items():
        if day not in close.index or pd.isna(close.loc[day, "SOXX"]):
            continue  # US market closed that day
        prev = close.index[close.index.get_loc(day) - 1]
        for tkr in ["MU", "SNDK", "SOXX"]:
            rows.append(
                {
                    "date": day.date(),
                    "hynix_%": round(hy_move, 1),
                    "ticker": tkr,
                    "gap_at_open_%": round(
                        (opens.loc[day, tkr] / close.loc[prev, tkr] - 1) * 100, 1
                    ),
                    "open_to_close_%": round(
                        (close.loc[day, tkr] / opens.loc[day, tkr] - 1) * 100, 1
                    ),
                }
            )
    study = pd.DataFrame(rows)
    print(f"\nUS session on days Hynix fell >{-HYNIX_CRASH:.0f}% in Seoul:")
    print(study.to_string(index=False))

    print("\nAverage: gap (lost to you) vs open-to-close (still capturable):")
    avg = study.groupby("ticker")[["gap_at_open_%", "open_to_close_%"]].mean()
    print(avg.round(1).to_string())
    print(
        "\n  Read: the gap eats the move; shorting at the open is ~zero-edge"
        "\n  on average. Exception: days the US open did NOT price the Seoul"
        "\n  crash (gap ~flat while Hynix down double digits, e.g. 7/2) - the"
        "\n  residual then resolved sharply lower intraday."
    )


def ladder_pnl(close: pd.DataFrame, lows: pd.DataFrame) -> None:
    """P&L of the pre-set capitulation limit ladder, marked at the 7/14 close."""
    print(
        f"\nPre-set capitulation ladder: 3 x ${STAKE / 3:,.0f} limit orders at"
        f" {'/'.join(f'{d}%' for d in LADDER)} below the 2026 high,"
        f" placed {LADDER_PLACED} (the narrative-break day):"
    )
    c14 = close.loc[REBOUND_DAY]
    for tkr in ["SOXX", "NVDA", "MU", "INTC", "MRVL", "AMD"]:
        high = close.loc["2026-01-01":"2026-06-30", tkr].max()
        total, legs = 0.0, []
        for depth in LADDER:
            trigger = high * (1 + depth / 100)
            touched = lows.index[(lows[tkr] <= trigger) & (lows.index >= LADDER_PLACED)]
            if touched.empty:
                legs.append(f"{depth}% unfilled")
                continue
            pnl = (STAKE / 3) * (c14[tkr] / trigger - 1)
            total += pnl
            legs.append(f"{depth}% filled {touched[0].strftime('%m-%d')} {pnl:+,.0f}$")
        print(f"  {tkr:5} {total:>+7,.0f}$ | " + " | ".join(legs))


def rebound_study(close: pd.DataFrame, opens: pd.DataFrame, lows: pd.DataFrame) -> None:
    """7/14 rebound: which $10k long entry actually captured the bounce?"""
    print("\n=== 5. Rebound study: catching the 7/14 bounce with $10k ===")
    if REBOUND_DAY not in close.index or pd.isna(close.loc[REBOUND_DAY, "SOXX"]):
        print("(No 7/14 US data available yet - rerun later.)")
        return

    print("\nSeoul tape around the turn (the free overnight signal, both ways):")
    seoul = close[["000660.KS", "005930.KS"]].dropna().pct_change() * 100
    window = seoul.loc["2026-07-08":].round(1)
    window.index = [d.strftime("%m-%d %a") for d in window.index]
    print(window.to_string())

    print("\nBounce-day decomposition - gap at open vs open-to-close (mirror of #4):")
    prev, o14, c14 = close.loc[SELLOFF_DAY], opens.loc[REBOUND_DAY], close.loc[REBOUND_DAY]
    decomp = pd.DataFrame(
        {
            "day_%": (c14 / prev - 1) * 100,
            "gap_at_open_%": (o14 / prev - 1) * 100,
            "open_to_close_%": (c14 / o14 - 1) * 100,
        }
    )
    print(
        decomp.loc[["MU", "INTC", "AMD", "MRVL", "NVDA", "SNDK", "SOXX", "SPY"]]
        .round(1)
        .to_string()
    )
    print(
        "\n  Read: the overnight gap ate MORE than the whole headline move -"
        "\n  buying the 9:30 open on the rebound news lost money intraday in"
        "\n  every name except NVDA. Same lesson as #4, in reverse."
    )

    print(f"\n$10k long entries valued at the {REBOUND_DAY} close:")
    entries = [
        ("Dip-buyer after the 7/8 bounce (7/9 open)", opens, "2026-07-09"),
        ("Dip-buyer on Hynix IPO pop (7/10 open)", opens, "2026-07-10"),
        ("Overnight-session buy while Seoul bounced (~7/13 close px)", close, SELLOFF_DAY),
        ("Chased the 7/14 9:30 open on the Seoul signal", opens, REBOUND_DAY),
    ]
    cols = ["SOXX", "MU", "INTC", "NVDA"]
    print(f"{'entry':60} " + " ".join(f"{t:>8}" for t in cols))
    for label, frame, day in entries:
        pnl = STAKE * (c14[cols] / frame.loc[day, cols] - 1)
        print(f"{label:60} " + " ".join(f"{v:>+7,.0f}$" for v in pnl))

    ladder_pnl(close, lows)
    print(
        "\n  Read: the ladder only made day-one money on the index and the"
        "\n  quality leader; -15% triggers on the high-beta names filled 7/2,"
        "\n  a week and one to two more down-legs before the bottom."
    )


def main() -> None:
    """Run all five checks against fresh market data."""
    close, opens, lows, pct = fetch_prices()
    timeline(close, pct)
    indicator_scorecard(close)
    reaction_pnl(close, opens)
    seoul_signal_study(close, opens)
    rebound_study(close, opens, lows)


if __name__ == "__main__":
    main()
