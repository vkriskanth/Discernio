"""Dataroma scraper: manager list, per-manager holdings, and activity.

Polite by design: real User-Agent, ~1.5s delay between requests, and raw
HTML cached under data/raw/<date>/ so a day's pages are fetched at most once.
"""

import re
import time

import requests
from bs4 import BeautifulSoup

from si import db

BASE = "https://www.dataroma.com/m"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
DELAY_SECONDS = 1.5

RAW_DIR = db.PROJECT_ROOT / "data" / "raw"


def _fetch(session: requests.Session, path: str, cache_name: str) -> str:
    """Fetch a Dataroma page, using today's raw-HTML cache when present."""
    cache_file = RAW_DIR / db.today() / cache_name
    if cache_file.exists():
        return cache_file.read_text()
    resp = session.get(f"{BASE}/{path}", timeout=30)
    resp.raise_for_status()
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(resp.text)
    time.sleep(DELAY_SECONDS)
    return resp.text


def _num(text: str) -> float | None:
    text = text.strip().replace(",", "").replace("$", "").rstrip("%")
    try:
        return float(text)
    except ValueError:
        return None


def parse_managers(html: str) -> list[dict]:
    """Parse home.php: [{code, name, last_seen_update}]."""
    soup = BeautifulSoup(html, "lxml")
    managers = []
    body = soup.find(id="port_body")
    if body is None:
        return managers
    for a in body.find_all("a", href=re.compile(r"holdings\.php\?m=")):
        code = a["href"].split("m=")[1]
        updated_span = a.find("span", class_="portb")
        updated = (
            updated_span.get_text(strip=True).replace("Updated ", "")
            if updated_span
            else None
        )
        # manager name is the <a> text minus the span contents
        name = a.get_text(strip=True)
        if updated_span:
            name = name.replace(updated_span.get_text(strip=True), "").strip()
        managers.append({"code": code, "name": name, "last_seen_update": updated})
    return managers


def parse_holdings(html: str) -> dict:
    """Parse holdings.php?m=X: {quarter, portfolio_date, rows: [...]}."""
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ")
    quarter_m = re.search(r"Period:\s*(Q\d \d{4})", text)
    date_m = re.search(r"Portfolio date:\s*(\d{1,2} \w{3} \d{4})", text)
    quarter = quarter_m.group(1) if quarter_m else "unknown"
    portfolio_date = date_m.group(1) if date_m else None

    rows = []
    grid = soup.find("table", id="grid")
    if grid and grid.tbody:
        for tr in grid.tbody.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) < 7:
                continue
            stock_a = tds[1].find("a")
            if not stock_a:
                continue
            ticker = (
                stock_a.contents[0].get_text(strip=True) if stock_a.contents else ""
            )
            name_span = stock_a.find("span")
            name = (
                name_span.get_text(strip=True).lstrip("- ").strip()
                if name_span
                else None
            )
            rows.append(
                {
                    "ticker": ticker,
                    "name": name,
                    "pct_portfolio": _num(tds[2].get_text()),
                    "recent_activity": tds[3].get_text(strip=True) or None,
                    "shares": int(_num(tds[4].get_text()) or 0) or None,
                    "reported_price": _num(tds[5].get_text()),
                }
            )
    return {"quarter": quarter, "portfolio_date": portfolio_date, "rows": rows}


def _classify(action_text: str) -> tuple[str, float | None]:
    """Map Dataroma activity text to (action, share_change_pct)."""
    t = action_text.strip()
    pct_m = re.search(r"([\d.]+)%", t)
    pct = float(pct_m.group(1)) if pct_m else None
    lower = t.lower()
    if lower.startswith("buy"):
        return "buy_new", None
    if lower.startswith("add"):
        return "add", pct
    if lower.startswith("sell"):
        return "sell_all" if pct == 100.0 else "reduce", pct
    if lower.startswith("reduce"):
        return "reduce", pct
    return lower.split()[0] if lower else "unknown", pct


def parse_activity(html: str) -> list[dict]:
    """Parse m_activity.php?m=X&typ=a.

    Returns [{quarter, ticker, action, share_change_pct, portfolio_change_pct}].
    Note: rows after the q_chg separator are missing <tr> openers in the raw
    HTML; lxml normalizes this, so we walk tds in groups keyed by td.hist.
    """
    soup = BeautifulSoup(html, "lxml")
    grid = soup.find("table", id="grid")
    entries: list[dict] = []
    tbody = grid.find("tbody") if grid else None
    if tbody is None:
        return entries

    quarter = "unknown"
    row_tds: list = []

    def emit(tds: list) -> None:
        if len(tds) < 5:
            return
        stock_a = tds[1].find("a")
        if not stock_a:
            return
        ticker = stock_a.contents[0].get_text(strip=True) if stock_a.contents else ""
        action, share_change_pct = _classify(tds[2].get_text(strip=True))
        entries.append(
            {
                "quarter": quarter,
                "ticker": ticker,
                "action": action,
                "share_change_pct": share_change_pct,
                "portfolio_change_pct": _num(tds[4].get_text()),
            }
        )

    # The site omits <tr> openers after the quarter separator rows, so lxml
    # leaves each data row's <td>s as direct tbody children. Walk them in
    # order, using td.hist as the row boundary and q_chg rows as quarter marks.
    for child in tbody.children:
        name = getattr(child, "name", None)
        if name == "tr":
            if "q_chg" in (child.get("class") or []):
                emit(row_tds)
                row_tds = []
                quarter = " ".join(b.get_text(strip=True) for b in child.find_all("b"))
            else:
                emit(row_tds)
                row_tds = []
                emit(child.find_all("td"))
        elif name == "td":
            if "hist" in (child.get("class") or []):
                emit(row_tds)
                row_tds = []
            row_tds.append(child)
    emit(row_tds)
    return entries


def scrape(managers_filter: list[str] | None = None, limit: int | None = None) -> dict:
    """Full scrape: manager list -> holdings + activity per manager -> DB.

    Returns a summary dict of what is new today.
    """
    conn = db.connect()
    session = requests.Session()
    session.headers["User-Agent"] = UA
    snapshot_date = db.today()

    managers = parse_managers(_fetch(session, "home.php", "home.html"))
    if managers_filter:
        wanted = {m.upper() for m in managers_filter}
        managers = [m for m in managers if m["code"].upper() in wanted]
    if limit:
        managers = managers[:limit]

    new_activity: list[dict] = []
    errors: list[str] = []
    for mgr in managers:
        code = mgr["code"]
        try:
            holdings = parse_holdings(
                _fetch(session, f"holdings.php?m={code}", f"holdings_{code}.html")
            )
            activity = parse_activity(
                _fetch(
                    session, f"m_activity.php?m={code}&typ=a", f"activity_{code}.html"
                )
            )
        except requests.RequestException as exc:
            errors.append(f"{code}: {exc}")
            continue

        db.upsert(
            conn,
            "managers",
            {"code": code},
            {
                "name": mgr["name"],
                "portfolio_date": holdings["portfolio_date"],
                "last_seen_update": mgr["last_seen_update"],
            },
        )
        for row in holdings["rows"]:
            db.upsert(
                conn,
                "stocks",
                {"ticker": row["ticker"]},
                {"name": row["name"]},
            )
            db.upsert(
                conn,
                "holdings",
                {
                    "manager_code": code,
                    "ticker": row["ticker"],
                    "quarter": holdings["quarter"],
                },
                {
                    "pct_portfolio": row["pct_portfolio"],
                    "shares": row["shares"],
                    "recent_activity": row["recent_activity"],
                    "reported_price": row["reported_price"],
                    "snapshot_date": snapshot_date,
                },
            )
        # only latest quarter's activity is of interest for "new this season"
        latest_quarter = activity[0]["quarter"] if activity else None
        for entry in activity:
            if entry["quarter"] != latest_quarter:
                continue
            existing = conn.execute(
                "SELECT 1 FROM activity WHERE manager_code=? AND ticker=? "
                "AND quarter=? AND action=?",
                (code, entry["ticker"], entry["quarter"], entry["action"]),
            ).fetchone()
            if existing:
                continue  # keep original first_seen_date
            new_activity.append({"manager": code, **entry})
            db.upsert(
                conn,
                "activity",
                {
                    "manager_code": code,
                    "ticker": entry["ticker"],
                    "quarter": entry["quarter"],
                    "action": entry["action"],
                },
                {
                    "share_change_pct": entry["share_change_pct"],
                    # % change to portfolio from the filing; for new buys this
                    # equals the position's size as % of portfolio
                    "pct_of_portfolio": entry["portfolio_change_pct"],
                    "first_seen_date": snapshot_date,
                },
            )
        conn.commit()

    db.log_run(
        conn,
        "scrape",
        "ok" if not errors else "partial",
        f"{len(managers)} managers, {len(new_activity)} new activity rows"
        + (f"; errors: {errors}" if errors else ""),
    )
    conn.close()
    return {"managers": len(managers), "new_activity": new_activity, "errors": errors}
