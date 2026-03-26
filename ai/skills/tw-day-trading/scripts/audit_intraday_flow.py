#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone, timedelta

TZ_TAIPEI = timezone(timedelta(hours=8))


def yn(value: str) -> str:
    v = value.strip().lower()
    if v in {"yes", "y", "true", "1", "ok", "done"}:
        return "正常"
    if v in {"no", "n", "false", "0", "fail", "broken"}:
        return "異常"
    return "待確認"


def main() -> None:
    # Note: this script structures operator input; it does not inspect logs automatically.
    parser = argparse.ArgumentParser(description="Format a QTDS intraday flow audit summary from operator-provided statuses.")
    parser.add_argument("--trading-day", default="")
    parser.add_argument("--broker-login", default="")
    parser.add_argument("--premarket", default="")
    parser.add_argument("--event-sync", default="")
    parser.add_argument("--supplement-915", default="")
    parser.add_argument("--supplement-930", default="")
    parser.add_argument("--entries", default="")
    parser.add_argument("--exits", default="")
    parser.add_argument("--force-exit", default="")
    parser.add_argument("--notes", nargs="*", default=[])
    args = parser.parse_args()

    now = datetime.now(TZ_TAIPEI).strftime("%Y-%m-%d %H:%M:%S %Z")
    checks = [
        ("交易日檢查", yn(args.trading_day)),
        ("券商登入 / 合約準備", yn(args.broker_login)),
        ("盤前 watchlist", yn(args.premarket)),
        ("事件同步", yn(args.event_sync)),
        ("09:15 補充", yn(args.supplement_915)),
        ("09:30 補充", yn(args.supplement_930)),
        ("進場判斷", yn(args.entries)),
        ("出場判斷", yn(args.exits)),
        ("13:20 強制清倉", yn(args.force_exit)),
    ]

    lines = [
        "## 當沖流程稽核",
        f"- 產生時間：{now}",
        "- 檢查結果：",
    ]
    for name, status in checks:
        lines.append(f"  - {name}：{status}")

    abnormal = [name for name, status in checks if status == "異常"]
    pending = [name for name, status in checks if status == "待確認"]

    lines.append(f"- 異常項目：{', '.join(abnormal) if abnormal else '無'}")
    lines.append(f"- 待確認項目：{', '.join(pending) if pending else '無'}")

    lines.extend([
        "- 稽核提醒：",
        "  - 若盤前正常但盤中異常，優先懷疑事件同步、補充節點或 live entry window。",
        "  - 若進場數量不合理，回頭檢查 VWAP、量能與 market floor 條件是否過鬆或過緊。",
        "  - 若尾盤還殘留部位，優先檢查 force-exit 與前面 exit 邏輯的銜接。",
    ])

    if args.notes:
        lines.append("- 備註：")
        for note in args.notes:
            lines.append(f"  - {note}")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
