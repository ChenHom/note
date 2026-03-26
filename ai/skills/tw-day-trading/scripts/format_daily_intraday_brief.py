#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
import json

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


def split_csv(raw: str) -> list[str]:
    if not raw.strip():
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def main() -> None:
    # Note: this script formats a briefing from provided inputs; it does not rank or score candidates.
    parser = argparse.ArgumentParser(description="Format a daily TW intraday briefing from provided inputs.")
    parser.add_argument("--mode", default="simulation")
    parser.add_argument("--market-bias", default="")
    parser.add_argument("--premarket-list", default="", help="Comma-separated premarket symbols")
    parser.add_argument("--manual-watchlist-path", default="config/manual_watchlist.json")
    parser.add_argument("--focus-list", default="", help="Comma-separated symbols requiring first attention")
    parser.add_argument("--risk-note", default="")
    parser.add_argument("--notes", nargs="*", default=[])
    args = parser.parse_args()

    now = datetime.now(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M:%S %Z")
    manual = load_manual_watchlist(Path(args.manual_watchlist_path).expanduser())
    premarket = split_csv(args.premarket_list)
    focus = split_csv(args.focus_list)

    lines = [
        "## 每日當沖簡報",
        f"- 產生時間：{now}",
        f"- 系統模式：{args.mode}",
        f"- 市場偏向：{args.market_bias or '待判斷'}",
        f"- 盤前名單：{', '.join(premarket) if premarket else '待填'}",
        f"- 手動優先名單：{', '.join(manual) if manual else '無'}",
        f"- 今日優先關注：{', '.join(focus) if focus else '待填'}",
        f"- 風控提醒：{args.risk_note or '請補單筆風險、單日停損與停手條件'}",
        "- 今日工作流：盤前 watchlist → event sync → 09:15 supplement → 09:30 supplement → entries/exits → force exit",
        "- 開盤提醒：先看 VWAP、量能、大盤條件，不要急著把盤中補充股當成原始主戰場。",
    ]

    if args.notes:
        lines.append("- 備註：")
        for note in args.notes:
            lines.append(f"  - {note}")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
