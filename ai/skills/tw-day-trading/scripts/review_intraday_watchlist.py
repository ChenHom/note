#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone, timedelta

TZ_TAIPEI = timezone(timedelta(hours=8))


def parse_items(raw_items: list[str]) -> list[dict]:
    items = []
    for raw in raw_items:
        parts = raw.split("|")
        symbol = parts[0].strip() if len(parts) > 0 else ""
        source = parts[1].strip() if len(parts) > 1 else "unknown"
        status = parts[2].strip() if len(parts) > 2 else "watch"
        note = parts[3].strip() if len(parts) > 3 else ""
        if symbol:
            items.append({
                "symbol": symbol,
                "source": source,
                "status": status,
                "note": note,
            })
    return items


def classify_status(status: str) -> tuple[str, str]:
    b = status.strip().lower()
    if b in {"near_entry", "entry", "ready", "go"}:
        return "接近進場", "可列為優先觀察，等條件確認就能出手。"
    if b in {"drop", "remove", "avoid"}:
        return "降級移除", "目前不宜繼續花太多注意力，除非結構重新轉強。"
    return "持續觀察", "先保留在 watchlist，等待 VWAP、量能、大盤條件更清楚。"


def main() -> None:
    # Note: this script is a formatter, not a signal judge.
    parser = argparse.ArgumentParser(description="Format a manually reviewed TW intraday watchlist into operator-ready notes.")
    parser.add_argument(
        "--item",
        action="append",
        default=[],
        help="Format: symbol|source|status|note  where source=manual/premarket/event_sync/supplement_915/supplement_930 and status=watch/near_entry/drop",
    )
    parser.add_argument("--market-bias", default="", help="e.g. 偏多 / 偏空 / 震盪")
    parser.add_argument("--risk-note", default="", help="e.g. 單筆 0.5R，連虧兩筆停手")
    args = parser.parse_args()

    now = datetime.now(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M:%S %Z")
    items = parse_items(args.item)

    lines = [
        "## 當沖 watchlist 檢查",
        f"- 產生時間：{now}",
        f"- 市場背景：{args.market_bias or '待補'}",
        f"- 風控提醒：{args.risk_note or '請補單筆風險、單日停損與連虧停手條件'}",
    ]

    if not items:
        lines.append("- 目前沒有提供標的。")
        print("\n".join(lines))
        return

    lines.append("- 標的檢查：")
    for item in items:
        label, action = classify_status(item["status"])
        source_label = {
            'manual': '手動優先',
            'premarket': '盤前名單',
            'event_sync': '事件同步',
            'supplement_915': '09:15 補充',
            'supplement_930': '09:30 補充',
        }.get(item['source'], item['source'])
        lines.append(f"  - {item['symbol']}｜來源={source_label}｜結論={label}")
        lines.append(f"    - 行動：{action}")
        if item["note"]:
            lines.append(f"    - 備註：{item['note']}")

    lines.extend([
        "- 總結提醒：",
        "  - 盤前名單與盤中補充不要用同樣信任等級處理。",
        "  - 補充標的若已過度延伸，寧可降級成觀察，不要硬追。",
        "  - 進場前還是要回到 VWAP、量能、大盤條件與失效點。",
    ])

    print("\n".join(lines))


if __name__ == "__main__":
    main()
