#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

TZ_TAIPEI = timezone(timedelta(hours=8))


def load_manual_watchlist(path: Path) -> list[str]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []
    raw = payload.get("manual_symbols", []) if isinstance(payload, dict) else []
    seen = set()
    result = []
    for item in raw:
        s = str(item).strip()
        if s and s not in seen:
            seen.add(s)
            result.append(s)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a TW day-trading pre-market checklist.")
    parser.add_argument("--mode", default="simulation", help="simulation or production")
    parser.add_argument("--watchlist", nargs="*", default=[], help="Initial watchlist symbols")
    parser.add_argument("--manual-watchlist-path", default="config/manual_watchlist.json")
    parser.add_argument("--risk-budget", default="", help="e.g. 單筆 0.5R / 單日 2R")
    parser.add_argument("--market-bias", default="", help="e.g. 偏多 / 偏空 / 震盪")
    parser.add_argument("--notes", nargs="*", default=[])
    args = parser.parse_args()

    now = datetime.now(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M:%S %Z")
    manual = load_manual_watchlist(Path(args.manual_watchlist_path).expanduser())
    initial = []
    seen = set()
    for symbol in [*args.watchlist, *manual]:
        s = str(symbol).strip()
        if s and s not in seen:
            seen.add(s)
            initial.append(s)

    lines = [
        "## 盤前清單",
        f"- 產生時間：{now}",
        f"- 系統模式：{args.mode}",
        f"- 市場偏向：{args.market_bias or '待判斷'}",
        f"- 初始 watchlist：{', '.join(initial) if initial else '（尚未提供）'}",
        f"- 手動名單：{', '.join(manual) if manual else '無'}",
        f"- 今日風險預算：{args.risk_budget or '待填'}",
        "- 關鍵檢查：昨高 / 昨低 / VWAP / 開盤區間 / 大盤方向",
        "- 盤中補充：留意 intraday event sync、09:15 supplement、09:30 supplement",
    ]

    if args.notes:
        lines.append("- 備註：")
        for note in args.notes:
            lines.append(f"  - {note}")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
