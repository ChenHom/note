#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone, timedelta

TZ_TAIPEI = timezone(timedelta(hours=8))


def split_csv(raw: str) -> list[str]:
    if not raw.strip():
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Format a TW day-trading post-market review template.")
    parser.add_argument("--premarket-list", default="", help="Comma-separated symbols from pre-market watchlist")
    parser.add_argument("--event-sync-list", default="", help="Comma-separated symbols added by intraday event sync")
    parser.add_argument("--supplement-915-list", default="", help="Comma-separated symbols added at 09:15")
    parser.add_argument("--supplement-930-list", default="", help="Comma-separated symbols added at 09:30")
    parser.add_argument("--best-trade", default="")
    parser.add_argument("--worst-trade", default="")
    parser.add_argument("--rule-violations", nargs="*", default=[])
    parser.add_argument("--notes", nargs="*", default=[])
    args = parser.parse_args()

    now = datetime.now(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M:%S %Z")
    premarket = split_csv(args.premarket_list)
    event_sync = split_csv(args.event_sync_list)
    sup915 = split_csv(args.supplement_915_list)
    sup930 = split_csv(args.supplement_930_list)

    lines = [
        "## 盤後檢討",
        f"- 產生時間：{now}",
        f"- 盤前名單：{', '.join(premarket) if premarket else '無'}",
        f"- 事件同步新增名單：{', '.join(event_sync) if event_sync else '無'}",
        f"- 09:15 補充名單：{', '.join(sup915) if sup915 else '無'}",
        f"- 09:30 補充名單：{', '.join(sup930) if sup930 else '無'}",
        f"- 最佳交易：{args.best_trade or '待填'}",
        f"- 最差交易：{args.worst_trade or '待填'}",
        "- 檢查項目：",
        "  - 哪個來源產生了最好交易？",
        "  - 哪個來源最容易追高？",
        "  - 停損是否合理？",
        "  - 停利是否太早？",
        "  - 13:20 強制清倉前是否已有更好出場？",
    ]

    lines.append(f"- 規則違反：{', '.join(args.rule_violations) if args.rule_violations else '無'}")
    if args.notes:
        lines.append("- 備註：")
        for note in args.notes:
            lines.append(f"  - {note}")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
