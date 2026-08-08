"""Momentum signals: price trend, short interest, options put/call.

Composite score (0-100), weights documented in COMPONENTS:
  - trend (40%): blended 3/6/12-month returns mapped onto 0-100
  - rsi (15%): RSI14 as-is (overbought/oversold read left to the analyst)
  - vs_200dma (25%): distance above/below the 200-day moving average
  - short_squeeze (10%): higher short interest -> higher potential energy
  - options_skew (10%): put/call OI ratio below 1 scores bullish
"""

import json
import sqlite3

import pandas as pd
import yfinance as yf

from si import db
from si.enrich import pending_tickers

WEIGHTS = {
    "trend": 0.40,
    "rsi": 0.15,
    "vs_200dma": 0.25,
    "short_squeeze": 0.10,
    "options_skew": 0.10,
}


def _clamp(v: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, v))


def _ret(closes: pd.Series, days: int) -> float | None:
    if len(closes) <= days:
        return None
    past = closes.iloc[-days - 1]
    return float((closes.iloc[-1] / past - 1) * 100) if past else None


def _rsi14(closes: pd.Series) -> float | None:
    if len(closes) < 15:
        return None
    delta = closes.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, pd.NA)
    rsi = 100 - (100 / (1 + rs))
    val = rsi.iloc[-1]
    return float(val) if pd.notna(val) else None


def _putcall_ratio(tkr: yf.Ticker) -> float | None:
    try:
        expiries = tkr.options
        if not expiries:
            return None
        chain = tkr.option_chain(expiries[min(1, len(expiries) - 1)])
        call_oi = chain.calls["openInterest"].sum()
        put_oi = chain.puts["openInterest"].sum()
        return float(put_oi / call_oi) if call_oi else None
    except Exception:
        return None


def compute_ticker(conn: sqlite3.Connection, ticker: str) -> bool:
    tkr = yf.Ticker(ticker)
    try:
        hist = tkr.history(period="2y", auto_adjust=True)
        info = tkr.info or {}
    except Exception as exc:
        db.log_run(conn, "momentum", "error", f"{ticker}: {exc}")
        return False
    if hist.empty:
        db.log_run(conn, "momentum", "error", f"{ticker}: no price history")
        return False

    closes = hist["Close"].dropna()
    ret_1m, ret_3m = _ret(closes, 21), _ret(closes, 63)
    ret_6m, ret_12m = _ret(closes, 126), _ret(closes, 252)
    rsi14 = _rsi14(closes)
    dma200 = float(closes.rolling(200).mean().iloc[-1]) if len(closes) >= 200 else None
    pct_vs_200dma = (
        float((closes.iloc[-1] / dma200 - 1) * 100) if dma200 else None
    )

    short_pct_float = info.get("shortPercentOfFloat")
    short_ratio = info.get("shortRatio")
    putcall = _putcall_ratio(tkr)

    # component scores, each 0-100
    trend_blend = sum(
        r * w
        for r, w in ((ret_3m, 0.3), (ret_6m, 0.3), (ret_12m, 0.4))
        if r is not None
    )
    components = {
        "trend": _clamp(50 + trend_blend),  # +50% blended return saturates at 100
        "rsi": _clamp(rsi14) if rsi14 is not None else 50.0,
        "vs_200dma": _clamp(50 + (pct_vs_200dma or 0) * 2),
        "short_squeeze": _clamp((short_pct_float or 0) * 100 * 5),  # 20% SI -> 100
        "options_skew": _clamp((1.5 - putcall) * 66.7) if putcall else 50.0,
    }
    score = round(sum(components[k] * WEIGHTS[k] for k in WEIGHTS), 1)

    asof = db.today()
    db.upsert(
        conn,
        "market_stats",
        {"ticker": ticker, "asof": asof},
        {
            "short_pct_float": short_pct_float,
            "short_ratio": short_ratio,
            "putcall_oi_ratio": putcall,
            "avg_volume": info.get("averageVolume"),
            "beta": info.get("beta"),
        },
    )
    db.upsert(
        conn,
        "momentum",
        {"ticker": ticker, "asof": asof},
        {
            "ret_1m": ret_1m,
            "ret_3m": ret_3m,
            "ret_6m": ret_6m,
            "ret_12m": ret_12m,
            "rsi14": rsi14,
            "pct_vs_200dma": pct_vs_200dma,
            "score": score,
            "components_json": json.dumps(components),
            # thesis is filled in later by the momentum-analyst agent
        },
    )
    conn.commit()
    return True


def compute(tickers: list[str] | None = None) -> dict:
    conn = db.connect()
    targets = tickers or pending_tickers(conn, "momentum")
    done, failed = [], []
    for t in targets:
        (done if compute_ticker(conn, t) else failed).append(t)
    db.log_run(conn, "momentum", "ok", f"{len(done)} computed, {len(failed)} failed")
    conn.close()
    return {"computed": done, "failed": failed}
