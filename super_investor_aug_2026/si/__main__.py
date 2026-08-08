"""CLI entry point: uv run python -m si <command>."""

import argparse
import json
import sys
from pathlib import Path

from si import db


def main() -> int:
    parser = argparse.ArgumentParser(prog="si", description="Superinvestor pipeline")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scrape = sub.add_parser("scrape", help="Scrape Dataroma into the DB")
    p_scrape.add_argument(
        "--managers", help="Comma-separated manager codes (e.g. SAM,BRK)"
    )
    p_scrape.add_argument("--limit", type=int, help="Only first N managers")

    p_enrich = sub.add_parser("enrich", help="Fetch fundamentals for buy/add tickers")
    p_enrich.add_argument(
        "--tickers", help="Comma-separated tickers (default: pending)"
    )

    p_mom = sub.add_parser("momentum", help="Compute momentum signals")
    p_mom.add_argument("--tickers", help="Comma-separated tickers (default: pending)")

    p_pending = sub.add_parser("pending", help="Dump JSON packets for analyst agents")
    p_pending.add_argument(
        "--tickers", help="Comma-separated tickers (default: all pending)"
    )
    p_pending.add_argument(
        "--out", default="data/pending", help="Output dir (default: data/pending)"
    )

    p_save = sub.add_parser("save-analysis", help="Persist an analyst JSON file")
    p_save.add_argument("files", nargs="+", help="Analysis JSON file(s)")

    p_report = sub.add_parser("report", help="Print canned reports")
    p_report.add_argument(
        "kind",
        nargs="?",
        default="full",
        choices=["new-buys", "conviction", "momentum", "verdicts", "full"],
    )

    args = parser.parse_args()

    if args.cmd == "scrape":
        from si.scrape import scrape

        managers = args.managers.split(",") if args.managers else None
        result = scrape(managers_filter=managers, limit=args.limit)
        print(f"Scraped {result['managers']} managers.")
        if result["new_activity"]:
            n = len(result["new_activity"])
            print(f"\nNEW activity since last run ({n} rows):")
            for e in result["new_activity"]:
                pct = e["portfolio_change_pct"]
                print(
                    f"  {e['manager']:>5}  {e['action']:<8} {e['ticker']:<6} "
                    f"{e['quarter']}  ({pct if pct is not None else '?'}% of portfolio)"
                )
        else:
            print("No new activity.")
        if result["errors"]:
            print(f"Errors: {result['errors']}", file=sys.stderr)

    elif args.cmd == "enrich":
        from si.enrich import enrich

        result = enrich(args.tickers.split(",") if args.tickers else None)
        print(f"Enriched: {result['enriched']}\nFailed: {result['failed']}")

    elif args.cmd == "momentum":
        from si.momentum import compute

        result = compute(args.tickers.split(",") if args.tickers else None)
        print(f"Computed: {result['computed']}\nFailed: {result['failed']}")

    elif args.cmd == "pending":
        from si.analysis_io import dump_pending

        out_dir = db.PROJECT_ROOT / args.out
        paths = dump_pending(out_dir, args.tickers.split(",") if args.tickers else None)
        print(json.dumps([str(p) for p in paths], indent=2))

    elif args.cmd == "save-analysis":
        from si.analysis_io import save_analysis

        for f in args.files:
            ticker = save_analysis(Path(f))
            print(f"Saved analysis for {ticker}")

    elif args.cmd == "report":
        from si.report import report

        report(args.kind)

    return 0


if __name__ == "__main__":
    sys.exit(main())
