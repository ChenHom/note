#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone, timedelta

TZ_TAIPEI = timezone(timedelta(hours=8))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a TW swing-trading plan template.")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--setup", default="breakout", help="breakout / pullback / watchlist")
    parser.add_argument("--trend", default="", help="e.g. 多頭趨勢完整")
    parser.add_argument("--support", default="")
    parser.add_argument("--pivot", default="")
    parser.add_argument("--risk", default="", help="e.g. 單筆 0.5R")
    parser.add_argument("--notes", nargs="*", default=[])
    args = parser.parse_args()

    now = datetime.now(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M:%S %Z")
    lines = [
        "## 台股波段計畫",
        f"- 產生時間：{now}",
        f"- 標的：{args.symbol}",
        f"- 類型：{args.setup}",
        f"- 趨勢：{args.trend or '待判斷'}",
        f"- 支撐：{args.support or '待填'}",
        f"- 突破位：{args.pivot or '待填'}",
        f"- 風險預算：{args.risk or '待填'}",
        "- 進場：只在結構確認後進場，避免追高失控",
        "- 管理：若突破失敗或跌破關鍵支撐，重新評估或退出",
    ]
    if args.notes:
        lines.append("- 備註：")
        for note in args.notes:
            lines.append(f"  - {note}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
