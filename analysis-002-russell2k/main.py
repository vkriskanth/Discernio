"""Analysis 002: Russell 2000 "index graduation" screen.

Which Russell 2000 companies are earning their way out of the index -
likely promotions to the S&P MidCap 400 or S&P 500 - before the S&P
committee makes it official and passive flows follow? The edge: ~40% of
Russell 2000 constituents lose money, so index profits concentrate in a
small minority; S&P membership requires positive GAAP earnings plus a
market-cap threshold, so profitable compounders near the cap boundary
are the graduation candidates. We then keep only the *good businesses*:
moat, management, business model, price (price scored loosely - it
ranks, it never eliminates).

What this script does with real data:
  1. Universe - the actual Russell 2000 constituent list via the iShares
     IWM holdings CSV (public, daily).
  2. Profit concentration map - who actually earns the index's profits;
     % unprofitable; top-25/50/100 earner concentration.
  3. Graduation screen - S&P eligibility mechanics: positive TTM GAAP
     earnings, US domicile and listing, market cap >= $1.5B, tagged into
     three zones: in-band ($8.0-22.7B, the MidCap 400 addition range),
     approaching ($4-8B - the backtest's +95% cohort), and far-below
     ($1.5-4B, needs TTM NI >= $50M). In-band cohorts: 400-ready,
     500-track, in-400.
  4. Moat test - ROE level/stability, gross margin, revenue growth, FCF
     conversion across ~4 fiscal years -> moat score 0-10.
  5. Management test - dilution, cash returned vs FCF, debt trajectory,
     insider ownership -> management score 0-10.
  6. Price (loose) - FCF yield, trailing P/E, crude PEG vs the S&P 400
     multiple it would re-rate toward -> value score 0-10; no name is
     dropped on price.
  7. Composite shortlist - moat 35%, management 25%, model/growth 20%,
     value 20%; ranked per zone, full table saved to data/shortlist.csv.

Caching: every expensive fetch lands in data/ and is reused if < 7 days
old. --refresh forces a refetch of everything. Run:
    uv run python main.py
"""

from __future__ import annotations

import argparse
import io
import sys
import time
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf

DATA_DIR = Path(__file__).parent / "data"
CACHE_DAYS = 7

# S&P eligibility, verified 2026-07-26 (spglobal.com press release
# 2025-07-01 "Update to S&P Composite 1500 Market Cap Guidelines",
# reaffirmed by the 2026-06-04 megacap consultation results; July 2026
# U.S. Indices methodology). Ranges are for additions, reviewed
# quarterly. Float-adjusted cap must be >= 50% of the index minimum.
SP500_MIN_CAP = 22.7e9
SP400_MIN_CAP = 8.0e9
SP400_MAX_CAP = 22.7e9
SP500_TRACK_FRAC = 0.70  # >= 70% of the 500 threshold = "500-track"
# Zones below the S&P 400 floor, from the backtest.py autopsy: names
# $4-8B a year before their 400 add averaged +95%; the in-band cohort
# only +11% (promotion already priced). Smallest graduate was ~$1.6B.
APPROACH_MIN = 4.0e9
FARBELOW_MIN = 1.5e9
FARBELOW_MIN_NI = 50e6  # <$4B names must show real earnings power
# GAAP earnings rule (unchanged): positive earnings in the most recent
# quarter AND positive sum of the trailing four quarters.

# S&P 400 forward P/E ~17x (Feb 2026, investsnips.com survey) - the
# multiple a promoted name re-rates toward; refreshed from IJH at
# runtime when available.
SP400_PE_ANCHOR = 17.0

IWM_HOLDINGS_URL = (
    "https://www.ishares.com/us/products/239710/"
    "ishares-russell-2000-etf/latest-holdings.csv"
)
SP600_WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_600_companies"
SP400_WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/126.0"}

# How many names (by index weight) get a full fundamentals snapshot.
# They dominate index earnings and contain every plausible graduate.
TOP_N_FUNDAMENTALS = 600

US_EXCHANGES = {"NYQ", "NMS", "NGM", "NCM", "ASE", "PCX", "BTS"}

INFO_FIELDS = {
    "marketCap": "mkt_cap",
    "totalRevenue": "revenue",
    "netIncomeToCommon": "ni_ttm",
    "trailingPE": "pe_ttm",
    "forwardPE": "pe_fwd",
    "enterpriseToEbitda": "ev_ebitda",
    "ebitda": "ebitda",
    "grossMargins": "gross_margin",
    "operatingMargins": "op_margin",
    "profitMargins": "net_margin",
    "returnOnEquity": "roe",
    "heldPercentInsiders": "insider_pct",
    "freeCashflow": "fcf",
    "totalDebt": "total_debt",
    "totalCash": "total_cash",
    "sharesOutstanding": "shares_out",
    "country": "country",
    "exchange": "exchange",
}


def cache_ok(path: Path, refresh: bool) -> bool:
    """True when a cached file exists, is fresh, and --refresh is off."""
    if refresh or not path.exists():
        return False
    age_days = (time.time() - path.stat().st_mtime) / 86400
    return age_days < CACHE_DAYS


def fetch_universe(refresh: bool) -> pd.DataFrame:
    """Step 1: the Russell 2000 constituents from the IWM holdings CSV."""
    path = DATA_DIR / "universe.csv"
    if cache_ok(path, refresh):
        return pd.read_csv(path)
    resp = requests.get(IWM_HOLDINGS_URL, headers=UA, timeout=60)
    resp.raise_for_status()
    lines = resp.text.splitlines()
    header_row = next(i for i, ln in enumerate(lines) if ln.startswith("Ticker,"))
    table = pd.read_csv(io.StringIO("\n".join(lines[header_row:])), thousands=",")
    table = table[table["Asset Class"] == "Equity"].copy()
    table = table[table["Ticker"].str.fullmatch(r"[A-Z][A-Z.]*", na=False)]
    table["yf_ticker"] = table["Ticker"].str.replace(".", "-", regex=False)
    table = table[
        ["Ticker", "yf_ticker", "Name", "Sector", "Weight (%)", "Market Value"]
    ].rename(
        columns={"Weight (%)": "weight_pct", "Market Value": "mkt_value"}
    )
    DATA_DIR.mkdir(exist_ok=True)
    table.to_csv(path, index=False)
    return table


def universe_section(universe: pd.DataFrame) -> None:
    """Print the universe summary."""
    print("\n=== 1. Universe: Russell 2000 via IWM holdings ===")
    print(f"equity constituents: {len(universe)}")
    by_sector = universe.groupby("Sector")["weight_pct"].sum().sort_values(
        ascending=False
    )
    print("\nindex weight by sector (%):")
    print(by_sector.round(1).to_string())
    print(
        "\n  Read: the working universe. Fundamentals below cover the top"
        f"\n  {TOP_N_FUNDAMENTALS} names by weight - they dominate index"
        "\n  earnings and contain every plausible S&P graduate."
    )


def fetch_fundamentals(universe: pd.DataFrame, refresh: bool) -> pd.DataFrame:
    """Snapshot .info fields for the top names by weight, cached per ticker."""
    # pylint: disable=too-many-locals
    path = DATA_DIR / "fundamentals_raw.csv"
    have = pd.DataFrame()
    if path.exists() and not refresh:
        have = pd.read_csv(path)
    top = universe.nlargest(TOP_N_FUNDAMENTALS, "weight_pct")
    todo = top[~top["yf_ticker"].isin(set(have.get("yf_ticker", [])))]
    if len(todo):
        print(f"(fetching fundamentals for {len(todo)} names - cached after)")
    DATA_DIR.mkdir(exist_ok=True)
    rows, failures = [], 0
    for count, uni_row in enumerate(todo.itertuples(), 1):
        tkr = uni_row.yf_ticker
        try:
            info = yf.Ticker(tkr).info
        except Exception:  # pylint: disable=broad-exception-caught
            failures += 1
            time.sleep(0.5)
            continue
        row = {"yf_ticker": tkr}
        for key, label in INFO_FIELDS.items():
            row[label] = info.get(key)
        rows.append(row)
        if count % 25 == 0:  # checkpoint so a crash never loses the batch
            pd.concat([have, pd.DataFrame(rows)], ignore_index=True).to_csv(
                path, index=False
            )
        time.sleep(0.15)
    if failures:
        print(f"(fundamentals fetch failures: {failures})")
    fresh = pd.DataFrame(rows)
    table = pd.concat([have, fresh], ignore_index=True) if len(fresh) else have
    table.to_csv(path, index=False)
    meta = universe[["yf_ticker", "Ticker", "Name", "Sector", "weight_pct"]]
    return table.merge(meta, on="yf_ticker", how="left")


def concentration_section(funda: pd.DataFrame) -> None:
    """Step 2: who earns the Russell 2000's profits."""
    print("\n=== 2. Profit concentration map ===")
    known = funda.dropna(subset=["ni_ttm"]).copy()
    profitable = known[known["ni_ttm"] > 0]
    losers = known[known["ni_ttm"] <= 0]
    total_profit = profitable["ni_ttm"].sum()
    total_loss = losers["ni_ttm"].sum()
    print(
        f"names with TTM net income data: {len(known)}"
        f" (top {TOP_N_FUNDAMENTALS} by weight)"
    )
    print(f"unprofitable: {len(losers)} ({len(losers) / len(known) * 100:.0f}%)"
          f", combined loss ${total_loss / 1e9:,.1f}B")
    print(f"profitable:   {len(profitable)},"
          f" combined profit ${total_profit / 1e9:,.1f}B")
    ranked = profitable.sort_values("ni_ttm", ascending=False)
    for n in (25, 50, 100):
        share = ranked.head(n)["ni_ttm"].sum() / total_profit * 100
        print(f"top {n:>3} earners contribute {share:.0f}% of all positive earnings")
    top25 = ranked.head(25)[["Ticker", "Name", "Sector", "ni_ttm", "mkt_cap"]].copy()
    top25["ni_ttm_$M"] = (top25.pop("ni_ttm") / 1e6).round(0)
    top25["mkt_cap_$B"] = (top25.pop("mkt_cap") / 1e9).round(1)
    print("\ntop 25 earners:")
    print(top25.to_string(index=False))
    print(
        "\n  Read: the index's profits belong to a thin slice of names."
        "\n  Everything below hunts inside that slice - concentration is"
        "\n  why a graduation screen on the Russell 2000 can work at all."
    )


def sp_members(url: str) -> set[str]:
    """Current S&P index tickers from a Wikipedia list page (best effort)."""
    try:
        resp = requests.get(url, headers=UA, timeout=60)
        resp.raise_for_status()
        tables = pd.read_html(io.StringIO(resp.text))
        for table in tables:
            if "Symbol" in table.columns:
                return set(table["Symbol"].astype(str))
    except Exception:  # pylint: disable=broad-exception-caught
        pass
    return set()


def last_quarter_positive(tkr: str) -> bool | None:
    """Most recent quarterly GAAP net income > 0, or None when unavailable."""
    try:
        inc = yf.Ticker(tkr).quarterly_income_stmt
        if inc is None or inc.empty or "Net Income" not in inc.index:
            return None
        latest = inc.loc["Net Income"].dropna()
        if latest.empty:
            return None
        return bool(latest.iloc[0] > 0)
    except Exception:  # pylint: disable=broad-exception-caught
        return None


def graduation_screen(funda: pd.DataFrame, refresh: bool) -> pd.DataFrame:
    """Step 3: filter to S&P promotion candidates, tag cohorts."""
    print("\n=== 3. Graduation screen: S&P eligibility mechanics ===")
    path = DATA_DIR / "graduation_candidates.csv"
    if cache_ok(path, refresh):
        table = pd.read_csv(path)
        print(f"(cached) candidates: {len(table)}")
        return table
    cand = funda.dropna(subset=["mkt_cap", "ni_ttm"]).copy()
    cand = cand[cand["ni_ttm"] > 0]
    cand = cand[cand["mkt_cap"] >= FARBELOW_MIN]
    cand = cand[cand["country"] == "United States"]
    cand = cand[cand["exchange"].isin(US_EXCHANGES)]
    # the far-below tail must show real earnings power, or the list
    # would swallow half the index
    far = cand["mkt_cap"] < APPROACH_MIN
    cand = cand[~far | (cand["ni_ttm"] >= FARBELOW_MIN_NI)]

    cand["zone"] = "far-below (1.5-4B)"
    cand.loc[cand["mkt_cap"] >= APPROACH_MIN, "zone"] = "approaching (4-8B)"
    cand.loc[cand["mkt_cap"] >= SP400_MIN_CAP, "zone"] = "in-band (8B+)"

    cand["cohort"] = cand["zone"]
    in_band = cand["mkt_cap"] >= SP400_MIN_CAP
    cand.loc[in_band, "cohort"] = "400-ready"
    on_track = cand["mkt_cap"] >= SP500_MIN_CAP * SP500_TRACK_FRAC
    cand.loc[on_track, "cohort"] = "400-ready+500-track"
    cand.loc[cand["mkt_cap"] >= SP500_MIN_CAP, "cohort"] = "500-eligible"

    in600 = sp_members(SP600_WIKI_URL)
    in400 = sp_members(SP400_WIKI_URL)
    cand["in_sp600"] = cand["Ticker"].isin(in600) if in600 else None
    cand["in_sp400"] = cand["Ticker"].isin(in400) if in400 else None
    # already in the 400 -> only the S&P 500 jump is left to front-run
    if in400:
        cand.loc[cand["in_sp400"], "cohort"] = "in-400 (500-jump only)"
    print(f"checking most-recent-quarter GAAP earnings for {len(cand)} names...")
    flags = []
    for tkr in cand["yf_ticker"]:
        pos = last_quarter_positive(tkr)
        flags.append("yes" if pos else ("NO" if pos is False else "unverified"))
        time.sleep(0.15)
    cand["last_q_positive"] = flags
    cand = cand[cand["last_q_positive"] != "NO"]
    cand = cand.sort_values("mkt_cap", ascending=False)
    cand.to_csv(path, index=False)

    print(f"\ncandidates: {len(cand)}  (cap >= ${FARBELOW_MIN / 1e9:.1f}B,"
          " TTM GAAP profit, US-domiciled, US-listed, last quarter not a"
          f" loss; <$4B names also need TTM NI >= ${FARBELOW_MIN_NI / 1e6:.0f}M)")
    print(cand["zone"].value_counts().to_string())
    show = cand[in_band.reindex(cand.index, fill_value=False)][
        ["Ticker", "Name", "Sector", "mkt_cap", "ni_ttm", "cohort",
         "in_sp600", "in_sp400", "last_q_positive"]
    ].copy()
    show["mkt_cap_$B"] = (show.pop("mkt_cap") / 1e9).round(1)
    show["ni_ttm_$M"] = (show.pop("ni_ttm") / 1e6).round(0)
    print("\nin-band names (full list; lower zones ranked after scoring):")
    print(show.to_string(index=False))
    print(
        "\n  Read: mechanics only - the committee also weighs sector"
        "\n  balance, float and seasoning, so this is a probability tilt,"
        "\n  not a certainty. Names already in the S&P 600 get promoted"
        "\n  from within the family more often than outsiders. The"
        "\n  backtest says in-band adds were ~priced (+11% avg) while the"
        "\n  approaching zone paid (+95% avg, selection-bias caveat)."
    )
    return cand


def yearly_series(frame: pd.DataFrame, label: str) -> pd.Series:
    """One row of an annual statement as a year-indexed Series (oldest first)."""
    if frame is None or frame.empty or label not in frame.index:
        return pd.Series(dtype=float)
    ser = frame.loc[label].dropna()
    ser.index = [col.year for col in ser.index]
    return ser.sort_index()


def statement_metrics(tkr: str, until: int | None = None) -> dict[str, float | None]:
    """Per-name metrics from ~4 fiscal years of statements (Steps 4-5).

    `until` drops fiscal years after that year - used by backtest.py to
    score with only the data an analyst would have had at the time.
    """
    # pylint: disable=too-many-locals,too-many-statements
    tik = yf.Ticker(tkr)
    try:
        inc, bal, cfs = tik.income_stmt, tik.balance_sheet, tik.cashflow
    except Exception:  # pylint: disable=broad-exception-caught
        return {}
    if until is not None:
        inc, bal, cfs = (
            frame.loc[:, [col for col in frame.columns if col.year <= until]]
            if frame is not None and not frame.empty else frame
            for frame in (inc, bal, cfs)
        )
    rev = yearly_series(inc, "Total Revenue")
    gross = yearly_series(inc, "Gross Profit")
    opinc = yearly_series(inc, "Operating Income")
    ni = yearly_series(inc, "Net Income")
    equity = yearly_series(bal, "Stockholders Equity")
    shares = yearly_series(bal, "Ordinary Shares Number")
    debt = yearly_series(bal, "Total Debt")
    fcf = yearly_series(cfs, "Free Cash Flow")
    divs = -yearly_series(cfs, "Cash Dividends Paid")
    bbs = -yearly_series(cfs, "Repurchase Of Capital Stock")

    out: dict[str, float | None] = {}
    # near-zero equity produces +/-inf ROE - treat as missing, not signal
    roe = (ni / equity.where(equity.abs() > 1e6) * 100).dropna()
    out["roe_avg"] = round(roe.mean(), 1) if len(roe) else None
    out["roe_std"] = round(roe.std(), 1) if len(roe) > 1 else None
    gmargin = (gross / rev * 100).dropna()
    out["gross_margin_avg"] = round(gmargin.mean(), 1) if len(gmargin) else None
    omargin = (opinc / rev * 100).dropna()
    out["op_margin_last"] = round(omargin.iloc[-1], 1) if len(omargin) else None
    out["op_margin_trend"] = (
        round(omargin.iloc[-1] - omargin.iloc[0], 1) if len(omargin) > 1 else None
    )
    if len(rev) > 1 and rev.iloc[0] > 0:
        years = rev.index[-1] - rev.index[0]
        out["rev_cagr"] = round(
            ((rev.iloc[-1] / rev.iloc[0]) ** (1 / years) - 1) * 100, 1
        )
    else:
        out["rev_cagr"] = None
    ni_pos = ni[ni > 0]
    common = fcf.index.intersection(ni_pos.index)
    if len(common):
        out["fcf_conversion"] = round(
            fcf[common].sum() / ni_pos[common].sum(), 2
        )
    else:
        out["fcf_conversion"] = None
    if len(shares) > 1 and shares.iloc[0] > 0:
        years = shares.index[-1] - shares.index[0]
        out["shares_chg_pa"] = round(
            ((shares.iloc[-1] / shares.iloc[0]) ** (1 / years) - 1) * 100, 1
        )
    else:
        out["shares_chg_pa"] = None
    fcf_total = fcf.sum()
    if fcf_total > 0:
        out["cash_returned_vs_fcf"] = round(
            (divs.sum() + bbs.sum()) / fcf_total, 2
        )
    else:
        out["cash_returned_vs_fcf"] = None
    if len(debt) > 1 and len(equity) and equity.iloc[-1] > 0:
        out["debt_chg_pa_pct_eq"] = round(
            (debt.iloc[-1] - debt.iloc[0]) / equity.iloc[-1] * 100, 1
        )
    else:
        out["debt_chg_pa_pct_eq"] = None
    return out


def fetch_metrics(cand: pd.DataFrame, refresh: bool) -> pd.DataFrame:
    """Statement metrics for every candidate, cached."""
    path = DATA_DIR / "quality_metrics.csv"
    have = pd.DataFrame()
    if path.exists() and not refresh:
        have = pd.read_csv(path)
    todo = cand[~cand["yf_ticker"].isin(set(have.get("yf_ticker", [])))]
    if todo.empty:
        return have
    print(f"(pulling ~4yr statements for {len(todo)} candidates...)")
    rows = []
    for count, tkr in enumerate(todo["yf_ticker"], 1):
        met = statement_metrics(tkr)
        met["yf_ticker"] = tkr
        rows.append(met)
        if count % 25 == 0:  # checkpoint so a crash never loses the batch
            pd.concat([have, pd.DataFrame(rows)], ignore_index=True).to_csv(
                path, index=False
            )
        time.sleep(0.15)
    table = pd.concat([have, pd.DataFrame(rows)], ignore_index=True)
    table.to_csv(path, index=False)
    return table


def scale(val: float | None, lo: float, hi: float, pts: float) -> float | None:
    """Linear 0..pts as val moves lo->hi (reversed when lo > hi)."""
    if val is None or pd.isna(val):
        return None
    if lo > hi:
        val, lo, hi = -val, -lo, -hi
    frac = (val - lo) / (hi - lo)
    return pts * min(max(frac, 0.0), 1.0)


def renorm(parts: list[tuple[float | None, float]]) -> float:
    """Sum scored parts, renormalized to 10 over the available components."""
    got = [(sc, mx) for sc, mx in parts if sc is not None]
    if not got:
        return 0.0
    total_max = sum(mx for _, mx in got)
    return round(sum(sc for sc, _ in got) / total_max * 10, 1)


def moat_score(row: pd.Series) -> float:
    """ROE level/stability, gross margin, growth, FCF conversion -> 0-10."""
    financial = row.get("Sector") == "Financials"
    parts = [
        (scale(row.get("roe_avg"), 5, 25, 3), 3),
        (scale(row.get("roe_std"), 8, 2, 2), 2),
        (scale(row.get("gross_margin_avg"), 15, 50, 2), 2),
        (scale(row.get("rev_cagr"), 0, 15, 2), 2),
    ]
    if not financial:
        parts.append((scale(row.get("fcf_conversion"), 0.3, 1.0, 1), 1))
    return renorm(parts)


def mgmt_score(row: pd.Series) -> float:
    """Dilution, cash returned, debt discipline, insider skin -> 0-10."""
    financial = row.get("Sector") == "Financials"
    ret = row.get("cash_returned_vs_fcf")
    if ret is not None and not pd.isna(ret) and ret > 1.3:
        ret = 2.6 - ret  # over-distributing beyond FCF scores down again
    parts = [
        (scale(row.get("shares_chg_pa"), 5, -1, 4), 4),
        (scale(row.get("insider_pct_x100"), 1, 10, 2), 2),
    ]
    if not financial:
        parts.append((scale(ret, 0.0, 0.8, 2.5), 2.5))
        parts.append((scale(row.get("debt_chg_pa_pct_eq"), 40, -10, 1.5), 1.5))
    return renorm(parts)


def growth_score(row: pd.Series) -> float:
    """Business model momentum: revenue growth + margin trend/level -> 0-10."""
    parts = [
        (scale(row.get("rev_cagr"), 0, 20, 5), 5),
        (scale(row.get("op_margin_trend"), -2, 6, 3), 3),
        (scale(row.get("op_margin_last"), 5, 20, 2), 2),
    ]
    return renorm(parts)


def value_score(row: pd.Series) -> float:
    """Loose valuation: FCF yield, P/E, crude PEG -> 0-10. Never eliminates."""
    financial = row.get("Sector") == "Financials"
    pe = row.get("pe_ttm")
    peg = None
    growth = row.get("rev_cagr")
    if pe and growth and not pd.isna(pe) and not pd.isna(growth) and growth > 0:
        peg = pe / growth
    parts = [
        (scale(pe, 60, 12, 4), 4),
        (scale(peg, 6, 1, 3), 3),
    ]
    if not financial:
        parts.append((scale(row.get("fcf_yield_pct"), 0, 7, 3), 3))
    return renorm(parts)


def shortlist_section(cand: pd.DataFrame, metrics: pd.DataFrame) -> None:
    """Steps 4-7: score candidates and print the ranked shortlist."""
    full = cand.merge(metrics, on="yf_ticker", how="left")
    full["insider_pct_x100"] = full["insider_pct"] * 100
    full["fcf_yield_pct"] = full["fcf"] / full["mkt_cap"] * 100

    print("\n=== 4. Moat test (score 0-10) ===")
    print("  formula: avg ROE 5->25% (3pts) + ROE stability std 8->2pp (2)"
          "\n  + gross margin 15->50% (2) + revenue CAGR 0->15% (2)"
          "\n  + FCF/NI conversion 0.3->1.0 (1, non-financials);"
          "\n  missing fields renormalized to /10.")
    full["moat"] = full.apply(moat_score, axis=1)

    print("\n=== 5. Management test (score 0-10) ===")
    print("  formula: share count +5->-1%/yr (4pts) + insider own 1->10% (2)"
          "\n  + cash returned 0->0.8x FCF (2.5, penalty past 1.3x)"
          "\n  + debt change +40->-10% of equity (1.5); financials skip"
          "\n  the FCF-based parts; renormalized to /10.")
    full["mgmt"] = full.apply(mgmt_score, axis=1)

    print("\n=== 6. Price - loose (score 0-10; ranks, never eliminates) ===")
    ijh_pe = None
    try:
        ijh_pe = yf.Ticker("IJH").info.get("trailingPE")
    except Exception:  # pylint: disable=broad-exception-caught
        pass
    anchor = ijh_pe if isinstance(ijh_pe, (int, float)) else SP400_PE_ANCHOR
    print(f"  re-rating anchor: S&P 400 P/E ~{anchor:.1f}x"
          f" ({'IJH live' if ijh_pe else 'Feb-2026 constant'})")
    print("  formula: P/E 60->12x (4pts) + P/E-to-growth 6->1 (3)"
          "\n  + FCF yield 0->7% (3, non-financials); renormalized to /10.")
    full["value"] = full.apply(value_score, axis=1)

    print("\n=== 7. Composite shortlist ===")
    print("  composite = moat*35% + management*25% + model/growth*20%"
          " + value*20%\n")
    full["growth_s"] = full.apply(growth_score, axis=1)
    full["composite"] = (
        full["moat"] * 0.35 + full["mgmt"] * 0.25
        + full["growth_s"] * 0.20 + full["value"] * 0.20
    ).round(2)
    full = full.sort_values("composite", ascending=False)
    full.to_csv(DATA_DIR / "shortlist.csv", index=False)

    cols = [
        "Ticker", "Name", "Sector", "cohort", "mkt_cap", "pe_ttm",
        "rev_cagr", "roe_avg", "moat", "mgmt", "growth_s", "value",
        "composite",
    ]
    zone_order = ["in-band (8B+)", "approaching (4-8B)", "far-below (1.5-4B)"]
    per_zone = {"in-band (8B+)": 15, "approaching (4-8B)": 15,
                "far-below (1.5-4B)": 20}
    for zone in zone_order:
        sub = full[full["zone"] == zone]
        if sub.empty:
            continue
        top_n = per_zone[zone]
        print(f"\n--- {zone}: top {min(top_n, len(sub))} of {len(sub)}"
              " by composite ---")
        show = sub.head(top_n)[cols].copy()
        show["mkt_cap_$B"] = (show.pop("mkt_cap") / 1e9).round(1)
        show["pe_ttm"] = show["pe_ttm"].round(1)
        print(show.to_string(index=False))
    print(
        "\n  Read: a probability tilt, not a promotion list - S&P adds are"
        "\n  committee calls weighing sector balance and seasoning. Per the"
        "\n  backtest, the in-band zone is a 0-2 quarter catalyst trade"
        "\n  (mostly priced), the approaching zone is the 1-year-early"
        "\n  hold where returns concentrated, and far-below is a 2+ year"
        "\n  quality watchlist. Top names per zone deserve a full"
        "\n  single-name workup (analysis-001 style) before any position."
    )


def main() -> None:
    """Run the full graduation screen."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh", action="store_true", help="refetch everything, ignore cache"
    )
    refresh = parser.parse_args().refresh
    DATA_DIR.mkdir(exist_ok=True)

    universe = fetch_universe(refresh)
    if universe.empty:
        sys.exit("no universe data - check network / iShares endpoint")
    universe_section(universe)
    funda = fetch_fundamentals(universe, refresh)
    concentration_section(funda)
    cand = graduation_screen(funda, refresh)
    if cand.empty:
        sys.exit("no graduation candidates survived the screen")
    metrics = fetch_metrics(cand, refresh)
    shortlist_section(cand, metrics)


if __name__ == "__main__":
    main()
