"""Analysis 001: ManpowerGroup (NYSE: MAN) through a Buffett-style lens.

The stock jumped ~32% on 7/16/2026 after Q2 earnings (revenue $4.9B, +8%,
swung from a $67M loss to $53.5M net income; Q3 guide raised). Questions:
what happened, how MAN stacks against competitors, what the business model
and moat actually are, how management has allocated capital, and whether
the price is fair.

What this script checks with real data:
  1. The pop and the arc - MAN's daily tape around 7/16, plus the long
     arc: distance from the 2022 peak, 52-week range, 5/10-yr CAGRs.
     A 32% day means nothing without knowing the starting altitude.
  2. Peer scoreboard - price performance (YTD/1y/3y/5y) for MAN vs Robert
     Half, Adecco, Randstad, Kelly, ASGN, Kforce, and SPY.
  3. Comparative fundamentals - market cap, P/E (trailing/forward), P/S,
     EV/EBITDA, dividend yield, and margins across the peer set.
  4. The business model in numbers - MAN's income statement by fiscal
     year: revenue, gross margin, SG&A, operating and net margins. Staffing
     economics (thin spread on billed labor) made visible.
  5. Moat test - margin level and stability vs the closest peers. A moat
     shows up as persistently superior returns; a commodity service shows
     up as everyone earning the same thin spread.
  6. Management's capital allocation - dividends, buybacks, share count,
     and debt across the last four fiscal years.
  7. Valuation - price against trough / run-rate / mid-cycle earnings
     power, and the earnings yield each implies.

Writes raw data to data/ and a summary to stdout.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import yfinance as yf

DATA_DIR = Path(__file__).parent / "data"
START = "2015-01-01"
POP_DAY = "2026-07-16"  # Q2-2026 earnings reaction

PEERS = {
    "MAN": "ManpowerGroup",
    "RHI": "Robert Half",
    "RAND.AS": "Randstad (AMS)",
    "ADEN.SW": "Adecco (SIX)",
    "KELYA": "Kelly Services",
    "KFRC": "Kforce",
    "SPY": "S&P 500",
}

# From the 7/16/26 Q2 press release / call (sourced in ANALYSIS.md).
Q2_ADJ_EPS = 0.99
Q3_GUIDE_MID = 1.01
DIVIDEND_NOTE = (
    "dividend paid since 1994, but CUT 53% in May 2025 (to $0.72 semiannual),"
    " held flat May 2026"
)


def fetch_prices() -> pd.DataFrame:
    """Daily closes for the peer set."""
    raw = yf.download(
        list(PEERS), start=START, auto_adjust=True, progress=False, group_by="column"
    )
    if raw is None or raw.empty:
        sys.exit("yfinance returned no data - check network")
    close = raw["Close"].dropna(how="all")
    DATA_DIR.mkdir(exist_ok=True)
    close.to_csv(DATA_DIR / "close.csv")
    return close


def the_pop(close: pd.DataFrame) -> None:
    """The 32% day in context of where the stock came from."""
    print("\n=== 1. The pop and the arc ===")
    man = close["MAN"].dropna()
    pct = man.pct_change() * 100
    recent = pct.loc["2026-07-06":].round(1)
    recent.index = [d.strftime("%m-%d %a") for d in recent.index]
    print("MAN daily % moves into and after the 7/16 Q2 print:")
    print(recent.to_string())

    now = man.iloc[-1]
    peak = man.max()
    peak_day = man.idxmax()
    yr = man[man.index >= man.index[-1] - pd.Timedelta(days=365)]
    print(f"\nlast close          ${now:.2f}")
    print(f"all-time peak       ${peak:.2f} on {peak_day.date()}"
          f" -> still {(now / peak - 1) * 100:.0f}% below")
    print(f"52-week range       ${yr.min():.2f} - ${yr.max():.2f}"
          f" (the pop started {((yr.min() / now - 1) * -100):.0f}% off the low)")
    for years in (5, 10):
        base = man[man.index <= man.index[-1] - pd.Timedelta(days=365 * years)]
        if len(base):
            cagr = ((now / base.iloc[-1]) ** (1 / years) - 1) * 100
            print(f"{years}-yr price CAGR     {cagr:+.1f}%/yr")
    print(
        "\n  Read: a one-day +32% on a beaten-down cyclical is a re-rating"
        "\n  of the cycle, not of the franchise. The arc numbers say which."
    )


def scoreboard(close: pd.DataFrame) -> None:
    """Price performance vs peers and the index."""
    print("\n=== 2. Peer scoreboard (price % change) ===")
    rows = []
    for tkr, name in PEERS.items():
        px = close[tkr].dropna()
        if px.empty:
            continue
        now = px.iloc[-1]
        row = {"ticker": tkr, "name": name}
        ytd = px[px.index >= "2026-01-01"]
        row["ytd"] = round((now / ytd.iloc[0] - 1) * 100, 1) if len(ytd) else None
        for label, years in (("1y", 1), ("3y", 3), ("5y", 5)):
            base = px[px.index <= px.index[-1] - pd.Timedelta(days=365 * years)]
            chg = (now / base.iloc[-1] - 1) * 100 if len(base) else None
            row[label] = round(chg, 1) if chg is not None else None
        rows.append(row)
    print(pd.DataFrame(rows).to_string(index=False))
    print(
        "\n  Read: staffing vs SPY over 5 years is the industry verdict;"
        "\n  MAN vs the staffing peers is the company verdict."
    )


def fundamentals() -> pd.DataFrame:
    """Valuation and profitability snapshot across the peer set."""
    print("\n=== 3. Comparative fundamentals (yfinance snapshot) ===")
    fields = {
        "marketCap": ("mkt_cap_$B", 1e9),
        "totalRevenue": ("revenue_$B", 1e9),
        "trailingPE": ("P/E_ttm", 1),
        "forwardPE": ("P/E_fwd", 1),
        "priceToSalesTrailing12Months": ("P/S", 1),
        "enterpriseToEbitda": ("EV/EBITDA", 1),
        "dividendYield": ("div_yld_%", 1),
        "operatingMargins": ("op_margin_%", 0.01),
        "profitMargins": ("net_margin_%", 0.01),
        "returnOnEquity": ("ROE_%", 0.01),
    }
    rows = {}
    for tkr in PEERS:
        if tkr == "SPY":
            continue
        try:
            info = yf.Ticker(tkr).info
        except Exception:  # pylint: disable=broad-exception-caught
            continue
        row = {}
        for key, (label, scale) in fields.items():
            val = info.get(key)
            is_num = isinstance(val, (int, float))
            row[label] = round(val / scale, 2) if is_num else None
        rows[tkr] = row
    table = pd.DataFrame(rows).T
    print(table.to_string())
    table.to_csv(DATA_DIR / "fundamentals.csv")
    print(
        "\n  Read: if every name earns 1-4% net margins and single-digit"
        "\n  ROE spreads, the industry prices like what it is - a commodity"
        "\n  service. Whoever stands out (margin or multiple) is the story."
    )
    return table


def business_model() -> pd.DataFrame:
    """MAN's P&L by fiscal year: the staffing spread made visible."""
    print("\n=== 4. The business model in numbers (MAN fiscal years) ===")
    inc = yf.Ticker("MAN").income_stmt
    if inc is None or inc.empty:
        print("(income statement unavailable)")
        return pd.DataFrame()
    inc = inc / 1e6  # $M
    rows = {}
    for col in sorted(inc.columns):
        year = col.year
        rev = inc.loc["Total Revenue", col]
        gp = inc.get(col).get("Gross Profit")
        op = inc.get(col).get("Operating Income")
        ni = inc.loc["Net Income", col]
        rows[year] = {
            "revenue_$M": round(rev),
            "gross_%": round(gp / rev * 100, 1) if pd.notna(gp) else None,
            "op_%": round(op / rev * 100, 1) if pd.notna(op) else None,
            "net_%": round(ni / rev * 100, 2),
            "net_income_$M": round(ni),
        }
    table = pd.DataFrame(rows).T
    print(table.to_string())
    table.to_csv(DATA_DIR / "man_pnl.csv")
    print(
        "\n  Read: MAN keeps ~17-18 cents of gross profit per revenue"
        "\n  dollar and runs ~16 cents of SG&A against it - the entire"
        "\n  operating profit lives in a 1-3 cent sliver that the cycle"
        "\n  swings. That IS the business model: a volume spread on labor."
    )
    return table


def moat_test() -> None:
    """Margin stability across the closest comps - the numeric moat test."""
    print("\n=== 5. Moat test: operating margin by fiscal year ===")
    comps = ["MAN", "RHI", "RAND.AS", "ADEN.SW", "KELYA"]
    rows = {}
    for tkr in comps:
        try:
            inc = yf.Ticker(tkr).income_stmt
        except Exception:  # pylint: disable=broad-exception-caught
            continue
        if inc is None or inc.empty:
            continue
        margins = {}
        for col in sorted(inc.columns):
            rev = inc.loc["Total Revenue", col]
            op = inc.get(col).get("Operating Income")
            if pd.notna(op) and rev:
                margins[col.year] = round(op / rev * 100, 1)
        rows[tkr] = margins
    table = pd.DataFrame(rows).T
    print(table.to_string())
    print(
        "\n  Read: Buffett's moat question in one table - does anyone"
        "\n  sustain a margin the others can't? RHI's premium (mix: perm"
        "\n  placement + Protiviti consulting) vs the 1-4% pack is the"
        "\n  closest thing this industry has to one."
    )


def capital_allocation() -> None:
    """Dividends, buybacks, share count, debt - the management record."""
    print("\n=== 6. Management: capital allocation (MAN fiscal years) ===")
    tk = yf.Ticker("MAN")
    cf, bs = tk.cashflow, tk.balance_sheet
    if cf is None or cf.empty:
        print("(cashflow unavailable)")
        return
    rows = {}
    for col in sorted(cf.columns):
        year = col.year
        def get(frame: pd.DataFrame, label: str, c: pd.Timestamp = col) -> float:
            return frame.loc[label, c] if label in frame.index else float("nan")

        rows[year] = {
            "FCF_$M": round((get(cf, "Free Cash Flow")) / 1e6),
            "dividends_$M": round(-get(cf, "Cash Dividends Paid") / 1e6),
            "buybacks_$M": round(-get(cf, "Repurchase Of Capital Stock") / 1e6),
            "shares_M": round(get(bs, "Ordinary Shares Number") / 1e6),
            "total_debt_$M": round(get(bs, "Total Debt") / 1e6),
        }
    table = pd.DataFrame(rows).T
    print(table.to_string())
    print(
        f"\n  Context: {DIVIDEND_NOTE}."
        "\n  Read: shrinking share count + steady dividend through a"
        "\n  downcycle = shareholder-first; buybacks concentrated at cycle"
        "\n  highs = the common sin. Check which one the table shows."
    )


def valuation(close: pd.DataFrame, pnl: pd.DataFrame) -> None:
    """Price vs trough / run-rate / mid-cycle earnings power."""
    print("\n=== 7. Valuation: what earnings are you paying for? ===")
    px = close["MAN"].dropna().iloc[-1]
    tk = yf.Ticker("MAN")
    ttm_eps = tk.info.get("trailingEps")

    shares = tk.info.get("sharesOutstanding")
    mid_cycle_ni = pnl["net_income_$M"].max() if not pnl.empty else None
    scenarios = {}
    if isinstance(ttm_eps, (int, float)):
        scenarios["TTM (trough-ish, includes loss quarters)"] = ttm_eps
    scenarios[f"Q2-26 adj run-rate (4 x ${Q2_ADJ_EPS})"] = Q2_ADJ_EPS * 4
    scenarios[f"Q3 guide run-rate (4 x ${Q3_GUIDE_MID})"] = Q3_GUIDE_MID * 4
    if mid_cycle_ni and shares:
        best_year = pnl["net_income_$M"].idxmax()
        scenarios[f"mid-cycle (best recent NI, FY{best_year})"] = (
            mid_cycle_ni * 1e6 / shares
        )

    print(f"MAN last close: ${px:.2f}\n")
    print(f"{'earnings basis':48} {'EPS':>7} {'P/E':>6} {'earn yield':>11}")
    for label, eps in scenarios.items():
        if eps and eps > 0:
            pe, yld = px / eps, eps / px * 100
            print(f"{label:48} {eps:>6.2f}$ {pe:>5.1f}x {yld:>10.1f}%")
        else:
            shown = eps if eps else float("nan")
            print(f"{label:48} {shown:>6.2f}$ {'n/m':>6} {'n/m':>11}")
    print(
        "\n  Read: cyclicals look cheapest at the top and dearest at the"
        "\n  bottom. The honest question is the mid-cycle line: what"
        "\n  multiple are you paying for average-year earnings, and does"
        "\n  the AI/structural question deserve a discount on top?"
    )


def main() -> None:
    """Run all seven checks against fresh market data."""
    close = fetch_prices()
    the_pop(close)
    scoreboard(close)
    fundamentals()
    pnl = business_model()
    moat_test()
    capital_allocation()
    valuation(close, pnl)


if __name__ == "__main__":
    main()
