#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone, timedelta

TZ_TAIPEI = timezone(timedelta(hours=8))


def main() -> None:
    parser = argparse.ArgumentParser(description="Review a TW swing-trading setup and format it into operator-ready language.")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--setup", default="watchlist", help="breakout / pullback / base / watchlist")
    parser.add_argument("--trend", default="", help="e.g. 多頭趨勢完整 / 結構鬆動")
    parser.add_argument("--support", default="")
    parser.add_argument("--pivot", default="")
    parser.add_argument("--status", default="watchlist", help="watchlist / entry")
    parser.add_argument("--risk-note", default="", help="e.g. 停損放前低下方")
    parser.add_argument("--notes", nargs="*", default=[])
    args = parser.parse_args()

    now = datetime.now(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M:%S %Z")
    status = args.status.strip().lower()
    if status not in {"watchlist", "entry"}:
        status = "watchlist"

    if status == "watchlist":
        quality_line = "目前偏 **watchlist quality**：值得追蹤，但還不是乾淨的進場點。"
        action_line = "建議先觀察結構是否更緊、是否更接近 trigger，再決定要不要出手。"
    else:
        quality_line = "目前偏 **entry quality**：觸發點與失效點都相對清楚，可開始規劃部位。"
        action_line = "建議把進場、停損、初始倉位與加碼條件一次寫清楚，不要靠盤中臨場感覺。"

    lines = [
        "## 台股波段標的檢查",
        f"- 產生時間：{now}",
        f"- 標的：{args.symbol}",
        f"- setup 類型：{args.setup}",
        f"- 趨勢判讀：{args.trend or '待補'}",
        f"- 支撐區：{args.support or '待補'}",
        f"- trigger / pivot：{args.pivot or '待補'}",
        f"- 結論：{quality_line}",
        f"- 行動建議：{action_line}",
        f"- 風控提醒：{args.risk_note or '請補停損與失效條件，不要只寫看法。'}",
        "- 檢查重點：",
        "  - 這是結構完整，還是其實已經開始鬆掉？",
        "  - 這是可交易性提高，還是只是故事更好聽？",
        "  - 如果明天走弱，哪個位置算 thesis invalidated？",
    ]

    if args.notes:
        lines.append("- 備註：")
        for note in args.notes:
            lines.append(f"  - {note}")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
