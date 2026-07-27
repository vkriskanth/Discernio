"""Hindcast: rerun the graduation screen as of one year ago (2025-07-25).

Would the screen have flagged the right names a year early, and what did
buying them return vs just holding IWM? Approach:

  1. Approximate each name's July-2025 market cap: close on 2025-07-25
     (adjusted) x current shares outstanding. Approximation - buybacks/
     dilution over the year skew it slightly; noted in output.
  2. Apply the same graduation screen with the same $8.0-22.7B band
     (effective 2025-07-01), requiring the last fiscal year ending on or
     before mid-2025 (FY<=2024) to be GAAP-profitable.
  3. Score with main.py's exact formulas, statements truncated to
     FY<=2024 - only the data a July-2025 analyst had.
  4. Outcomes: 1-yr total return per name vs IWM, current S&P 400/600
     membership, and the S&P 400 additions of the past 12 months from
     Wikipedia's changes table (which also catches winners that already
     left the Russell 2000 - today's universe is survivorship-biased).

Requires a prior `python main.py` run (uses its cached fundamentals).
Run: uv run python backtest.py
"""

from __future__ import annotations

import io
import sys
import time

import pandas as pd
import requests
import yfinance as yf
from main import (
    DATA_DIR,
    SP400_MAX_CAP,
    SP400_MIN_CAP,
    SP400_WIKI_URL,
    SP600_WIKI_URL,
    UA,
    US_EXCHANGES,
    growth_score,
    mgmt_score,
    moat_score,
    sp_members,
    statement_metrics,
    value_score,
)

AS_OF = "2025-07-25"
CUTOFF_FY = 2024  # last fiscal year a July-2025 analyst had in hand


def load_cached() -> pd.DataFrame:
    """Universe + fundamentals from the main run's cache."""
    uni_path = DATA_DIR / "universe.csv"
    fun_path = DATA_DIR / "fundamentals_raw.csv"
    if not (uni_path.exists() and fun_path.exists()):
        sys.exit("run `python main.py` first - backtest reuses its cache")
    universe = pd.read_csv(uni_path)
    funda = pd.read_csv(fun_path)
    meta = universe[["yf_ticker", "Ticker", "Name", "Sector", "weight_pct"]]
    return funda.merge(meta, on="yf_ticker", how="left")


def fetch_closes(tickers: list[str]) -> pd.DataFrame:
    """Adjusted closes from just before AS_OF to now, cached."""
    path = DATA_DIR / "backtest_close.csv"
    if path.exists():
        return pd.read_csv(path, index_col=0, parse_dates=True)
    raw = yf.download(
        tickers + ["IWM"], start="2025-07-18", auto_adjust=True,
        progress=False, group_by="column",
    )
    if raw is None or raw.empty:
        sys.exit("yfinance returned no price data")
    close = raw["Close"].dropna(how="all")
    close.to_csv(path)
    return close


def hindcast_screen(funda: pd.DataFrame, close: pd.DataFrame) -> pd.DataFrame:
    """The graduation screen as a July-2025 analyst would have run it."""
    print(f"\n=== 1. Hindcast screen as of {AS_OF} ===")
    asof_px = close.loc[:AS_OF].iloc[-1]
    now_px = close.ffill().iloc[-1]
    cand = funda.dropna(subset=["shares_out"]).copy()
    cand["px_asof"] = cand["yf_ticker"].map(asof_px)
    cand["px_now"] = cand["yf_ticker"].map(now_px)
    cand = cand.dropna(subset=["px_asof"])  # drops post-2025 IPOs correctly
    cand["cap_asof"] = cand["px_asof"] * cand["shares_out"]
    cand = cand[
        (cand["cap_asof"] >= SP400_MIN_CAP) & (cand["cap_asof"] <= SP400_MAX_CAP)
    ]
    cand = cand[cand["country"] == "United States"]
    cand = cand[cand["exchange"].isin(US_EXCHANGES)]
    print(f"cap band survivors (${SP400_MIN_CAP / 1e9:.1f}-"
          f"{SP400_MAX_CAP / 1e9:.1f}B est. as of {AS_OF}): {len(cand)}")
    print(
        "  (market cap = 2025-07-25 close x TODAY's share count -"
        "\n   approximation; and today's Russell membership is the universe,"
        "\n   so names promoted out of the Russell 2000 since are invisible"
        "\n   here - section 3 catches them via the S&P changes list)"
    )
    return cand


def score_cutoff(cand: pd.DataFrame) -> pd.DataFrame:
    """Score survivors on FY<=CUTOFF_FY statements only, cached."""
    path = DATA_DIR / "backtest_metrics.csv"
    if path.exists():
        metrics = pd.read_csv(path)
    else:
        print(f"(pulling FY<={CUTOFF_FY} statements for {len(cand)} names...)")
        rows = []
        for tkr in cand["yf_ticker"]:
            met = statement_metrics(tkr, until=CUTOFF_FY)
            met["yf_ticker"] = tkr
            rows.append(met)
            time.sleep(0.15)
        metrics = pd.DataFrame(rows)
        metrics.to_csv(path, index=False)
    full = cand.merge(metrics, on="yf_ticker", how="left")

    # FY2024 profitability gate (the GAAP screen a 2025 analyst ran)
    prof_path = DATA_DIR / "backtest_ni2024.csv"
    if prof_path.exists():
        ni2024 = pd.read_csv(prof_path)
    else:
        rows = []
        for tkr in full["yf_ticker"]:
            try:
                inc = yf.Ticker(tkr).income_stmt
                cols = [c for c in inc.columns if c.year <= CUTOFF_FY]
                val = inc.loc["Net Income", cols[0]] if cols else None
            except Exception:  # pylint: disable=broad-exception-caught
                val = None
            rows.append({"yf_ticker": tkr, "ni_fy2024": val})
            time.sleep(0.1)
        ni2024 = pd.DataFrame(rows)
        ni2024.to_csv(prof_path, index=False)
    full = full.merge(ni2024, on="yf_ticker", how="left")
    full = full[full["ni_fy2024"] > 0]
    print(f"FY{CUTOFF_FY} GAAP-profitable survivors: {len(full)}")

    # value inputs as-of 2025: trailing P/E on FY2024 EPS, FCF yield on
    # FY-2024-era FCF vs the as-of cap; insider % is today's (approx)
    full["insider_pct_x100"] = full["insider_pct"] * 100
    full["pe_ttm"] = full["cap_asof"] / full["ni_fy2024"]
    full["fcf_yield_pct"] = full["fcf"] / full["cap_asof"] * 100
    full["moat"] = full.apply(moat_score, axis=1)
    full["mgmt"] = full.apply(mgmt_score, axis=1)
    full["growth_s"] = full.apply(growth_score, axis=1)
    full["value"] = full.apply(value_score, axis=1)
    full["composite"] = (
        full["moat"] * 0.35 + full["mgmt"] * 0.25
        + full["growth_s"] * 0.20 + full["value"] * 0.20
    ).round(2)
    return full.sort_values("composite", ascending=False)


def outcomes(scored: pd.DataFrame, close: pd.DataFrame) -> None:
    """1-yr returns, current index membership, and actual S&P 400 adds."""
    # pylint: disable=too-many-locals
    print("\n=== 2. What the July-2025 shortlist did over the year ===")
    scored = scored.copy()
    scored["ret_1y_pct"] = (scored["px_now"] / scored["px_asof"] - 1) * 100
    in400 = sp_members(SP400_WIKI_URL)
    in600 = sp_members(SP600_WIKI_URL)
    scored["now_sp400"] = scored["Ticker"].isin(in400)
    scored["now_sp600"] = scored["Ticker"].isin(in600)

    show = scored.head(15)[
        ["Ticker", "Name", "Sector", "cap_asof", "composite",
         "ret_1y_pct", "now_sp400", "now_sp600"]
    ].copy()
    show["cap_2025_$B"] = (show.pop("cap_asof") / 1e9).round(1)
    show["ret_1y_pct"] = show["ret_1y_pct"].round(1)
    print(show.to_string(index=False))

    iwm = close["IWM"].dropna()
    iwm_ret = (iwm.iloc[-1] / iwm.loc[:AS_OF].iloc[-1] - 1) * 100
    for top_n in (5, 10, 15):
        cohort = scored.head(top_n)["ret_1y_pct"].mean()
        print(f"top-{top_n:>2} equal-weight 1-yr return: {cohort:+.1f}%"
              f"  vs IWM {iwm_ret:+.1f}%  (alpha {cohort - iwm_ret:+.1f}pp)")
    promoted = scored[scored["now_sp400"]]
    print(f"\nhindcast names now in the S&P 400: {len(promoted)}"
          f" of {len(scored)} screened"
          f" ({', '.join(promoted.head(15)['Ticker'])})")
    print(
        "\n  Read: names in the 400 now but absent from section 3's"
        "\n  additions window were ALREADY members in July 2025 - today's"
        "\n  Russell holdings simply contain almost no unpromoted $8B+"
        "\n  profitable names from a year ago. The zone empties fast."
    )


def sp400_additions_window() -> list[str]:
    """Tickers added to the S&P 400 between AS_OF and today (Wikipedia)."""
    resp = requests.get(SP400_WIKI_URL, headers=UA, timeout=60)
    resp.raise_for_status()
    tables = pd.read_html(io.StringIO(resp.text))
    changes = next(
        tab for tab in tables
        if any("Added" in str(col) for col in tab.columns)
    )
    changes.columns = [
        "_".join(str(part) for part in col).lower() if isinstance(col, tuple)
        else str(col).lower()
        for col in changes.columns
    ]
    date_col = next(col for col in changes.columns if "date" in col)
    add_col = next(
        col for col in changes.columns if "added" in col and "ticker" in col
    )
    changes["when"] = pd.to_datetime(
        changes[date_col], format="mixed", errors="coerce"
    )
    window = changes[
        (changes["when"] >= AS_OF) & (changes["when"] <= pd.Timestamp.now())
    ].dropna(subset=[add_col])
    return sorted(set(window[add_col].astype(str)))


def additions_section(scored: pd.DataFrame) -> None:
    """Where were the year's actual S&P 400 additions a year ago?"""
    # pylint: disable=too-many-locals
    print("\n=== 3. The year's actual S&P 400 additions, seen from 2025 ===")
    try:
        added = sp400_additions_window()
    except Exception:  # pylint: disable=broad-exception-caught
        print("(could not parse the Wikipedia changes table - skipped)")
        return
    print(f"additions Jul 2025 - Jul 2026: {len(added)}")
    flagged = sorted(set(added) & set(scored["Ticker"]))
    print(f"flagged by the strict hindcast screen: {len(flagged) or 'none'}")

    path = DATA_DIR / "backtest_additions.csv"
    if path.exists():
        table = pd.read_csv(path)
    else:
        yf_tkrs = [t.replace(".", "-") for t in added]
        raw = yf.download(
            yf_tkrs, start="2025-07-18", auto_adjust=True,
            progress=False, group_by="column",
        )
        close = raw["Close"].dropna(how="all")
        rows = []
        for tkr, yf_tkr in zip(added, yf_tkrs):
            row: dict[str, object] = {"Ticker": tkr}
            px = close.get(yf_tkr)
            if px is not None and not px.dropna().empty:
                px = px.dropna()
                asof = px.loc[:AS_OF]
                row["px_asof"] = asof.iloc[-1] if len(asof) else None
                row["px_now"] = px.iloc[-1]
            try:
                row["shares_out"] = yf.Ticker(yf_tkr).info.get("sharesOutstanding")
            except Exception:  # pylint: disable=broad-exception-caught
                row["shares_out"] = None
            rows.append(row)
            time.sleep(0.1)
        table = pd.DataFrame(rows)
        table.to_csv(path, index=False)

    table["cap_2025_$B"] = table["px_asof"] * table["shares_out"] / 1e9
    table["ret_1y_pct"] = (table["px_now"] / table["px_asof"] - 1) * 100

    def zone(cap: float) -> str:
        if pd.isna(cap):
            return "no 2025 data (IPO/spin-off)"
        if cap >= SP400_MIN_CAP / 1e9:
            return "in band already"
        if cap >= 4.0:
            return "approaching (4-8B)"
        return "far below (<4B)"

    table["zone_2025"] = table["cap_2025_$B"].apply(zone)
    table = table.sort_values("cap_2025_$B", ascending=False)
    show = table[["Ticker", "cap_2025_$B", "ret_1y_pct", "zone_2025"]].round(1)
    print(show.to_string(index=False))
    print("\nby zone a year before their S&P 400 add:")
    for name, grp in table.groupby("zone_2025"):
        ret = grp["ret_1y_pct"].mean()
        ret_txt = f"{ret:+.0f}%" if pd.notna(ret) else "n/a"
        print(f"  {name:28} {len(grp):>2} names, avg 1-yr return {ret_txt}")
    print(
        "\n  Read: the 'approaching (4-8B)' zone is where today's 400-ready"
        "\n  shortlist (ZWS, EAT, SNEX...) sat a year before promotion -"
        "\n  their average return is what catching graduation early paid."
        "\n  'In band already' names were promoted within months, so the"
        "\n  strict screen's window is roughly 0-2 quarters, not 12 months."
    )


def main() -> None:
    """Run the one-year hindcast."""
    funda = load_cached()
    close = fetch_closes(list(funda["yf_ticker"].dropna()))
    cand = hindcast_screen(funda, close)
    scored = score_cutoff(cand)
    scored.to_csv(DATA_DIR / "backtest_shortlist.csv", index=False)
    outcomes(scored, close)
    additions_section(scored)


if __name__ == "__main__":
    main()
