---
name: tw-day-trading
description: Build and review Taiwan stock day-trading plans, pre-market checklists, intraday entry/exit rules, day-risk controls, and `quantitative-trading-decision-system` workflow checks. Use when the user asks about 台股當沖 planning, 盤前準備, 盤中補充標的, VWAP/量能/大盤條件, 停損停利, force-exit timing, or debugging the `當沖` project. Do not use for long-term investing, pure財報研究, or classic波段 setups unless the user explicitly wants an intraday adaptation.
---

# Taiwan Day Trading

## Purpose

Structure Taiwan stock day-trading work into a disciplined workflow that maps onto the user's existing project:

- repo: `~/services/stock/quantitative-trading-decision-system`
- alias: `當沖`
- runtime flow: pre-market watchlist → intraday event sync → 09:15 supplement → 09:30 supplement → live entries/exits → 13:20 force exit

Prefer concrete rules over vague opinions. Reuse the system's existing vocabulary so recommendations map directly onto the codebase.

## Use This Skill When

Apply this skill when the request is about:

- 台股當沖計畫
- 盤前 checklist
- 盤中補充標的邏輯
- 某標的今天能不能當沖
- VWAP / 量能 / 大盤條件設定
- 停損、停利、時間出場、強制清倉
- `quantitative-trading-decision-system` 的流程、風控、cron、runtime 檢查
- 把當沖流程寫成 SOP / spec / checklist

## Do Not Use This Skill When

Do not use this skill for:

- 長線投資配置
- 純財報或基本面研究
- 純情緒分析 / 輿情彙整
- 經典波段趨勢交易（除非使用者要求改寫成日內版本）

If the request is primarily about波段，prefer the separate swing-trading skill.

## Workflow

### 1. Classify The Request

Classify the task before giving advice:

- **plan**: build a same-day trading plan
- **audit**: inspect system flow / ops / scheduling / data sync
- **debug**: explain a missed trade, bad exit, or unexpected behavior
- **rewrite**: convert loose ideas into a checklist, SOP, or spec

### 2. Anchor To The Live System

Start from the actual project path and runtime:

- entrypoint: `scripts/run_trading_system.sh`
- main loop: `src/main.py`
- trading-day gate: `scripts/is_taiwan_trading_day.py`
- event monitor: `scripts/run_intraday_event_monitor.sh`

If the issue is operational, inspect in this order:

1. trading-day check
2. broker login and contract readiness
3. pre-market watchlist generation
4. manual watchlist merge / force-date override
5. market index subscription
6. intraday signal file creation
7. 09:00–09:30 signal sync
8. 09:15 supplement
9. 09:30 supplement
10. live entry evaluation
11. exit actions
12. 13:20 force exit
13. logs and post-trade analysis

Use this order because many apparent strategy failures are really upstream candidate or synchronization failures.

### 3. Build The Candidate Map

Separate candidate sources. Do not treat all names with the same confidence.

#### A. Pre-Market Watchlist

Treat this as the highest-confidence source.

Use for:
- primary focus names
- best execution quality
- names with cleaner level planning

Review:
- scanner output
- manual watchlist merge via `config/manual_watchlist.json`
- force date override via `FORCE_MANUAL_WATCHLIST_DATE`
- whether names are liquid and operationally tradable

#### B. Intraday Event Sync (09:00–09:30)

Read this path as opportunistic but valid.

Current mapping:
- file: `logs/intraday_event_signals.json`
- setting: `INTRADAY_SIGNAL_REFRESH_SEC` default `10`
- writer: `run_intraday_event_monitor.py`
- reader: `IntradaySignalLoader(settings.intraday_signal_path)`

Review:
- whether the file is written on time
- whether new symbols are truly new
- whether contracts exist
- whether tradability screening blocks the right names
- whether the buffer initialization is strong enough for later evaluation

#### C. 09:15 / 09:30 Supplements

Treat fixed-time supplements more conservatively than preplanned names.

Current observed defaults:
- `SUPPLEMENT_MIN_CHANGE_PCT_915 = 0.05`
- `SUPPLEMENT_MIN_VOLUME_915 = 1000`
- `SUPPLEMENT_MIN_CHANGE_PCT_930 = 0.05`
- `SUPPLEMENT_MIN_VOLUME_930 = 2000`
- `SUPPLEMENT_MAX_ADD = 5`

Review:
- whether thresholds are too loose or too strict
- whether late additions are already extended
- whether added names remain liquid enough for the entry logic
- whether 09:15 and 09:30 should have different aggressiveness

### 4. Map Advice To Existing Entry Logic

Write entry recommendations in the same language as the codebase.

Current concepts already present in the project:
- VWAP hold
- volume surge
- market index floor
- previous high / previous low structure
- intraday entry timing window

Current visible defaults:
- `STRATEGY_VWAP_HOLD_MINUTES = 3`
- `STRATEGY_VOLUME_SURGE_RATIO = 1.5`
- `STRATEGY_MARKET_INDEX_FLOOR = -0.005`
- `STRATEGY_PREVIOUS_HIGH_LOOKBACK_BARS = 5`

Phrase recommendations like this:
- Enter only after price holds above VWAP for the configured hold window.
- Require current volume to exceed recent average tick volume by the configured surge ratio.
- Do not force long entries if the market index is already below the allowed floor.
- Use previous high / low structure as the first invalidation map.

Ask these audit questions:
- Is the VWAP hold window too strict for fast names, or too loose for noisy names?
- Is the volume surge ratio catching real momentum or too many false positives?
- Is the market index floor filtering enough bad market conditions?
- Are late-added names given enough structure before evaluation begins?

### 5. Map Advice To Existing Exit Logic

Keep all current exit families explicit:

- `EXIT_STOP_LOSS`
- `EXIT_TAKE_PROFIT`
- `EXIT_INDICATOR_BREAK`
- `EXIT_TIME`
- forced liquidation from 13:20 onward
- partial take-profit via `STRATEGY_PARTIAL_EXIT_RATIO = 0.5`

Review:
- whether stops match real structure
- whether partial profit-taking is too early
- whether indicator breaks are too noisy for the strategy horizon
- whether force-exit timing matches liquidity decay late in the session

### 6. Enforce Mandatory Risk Controls

Treat these as default non-negotiables unless the user explicitly overrides them:

- do not average down on losers
- do not hold overnight unless intentionally converting to swing mode
- use smaller size for supplement names than planned names
- define a daily stop and stop-trading rule after repeated losses
- cap correlated exposure
- log why a trade was entered, not only that it was entered

Recommended planning ranges unless house rules already exist:
- risk per trade: `0.25%–1.00%` of account
- daily stop: `1.5R–3R`
- fresh entries after 11:00: stricter filter, smaller size

### 7. End With Actionable Output

Prefer operator-ready output over essays.

Use one of these two formats.

#### Same-Day Plan

```md
## 台股當沖計畫

### 系統模式
- 模擬 / 正式：
- 今日重點：原始 watchlist / 事件補充 / 09:15 / 09:30 補充

### 觀察名單
- 標的 A：來源 / 關鍵價位 / 理由
- 標的 B：來源 / 關鍵價位 / 理由

### 進場規則
- VWAP：
- 量能條件：
- 大盤條件：
- 失效點：

### 出場規則
- 停損：
- 停利：
- 時間出場：
- 強制清倉：13:20 後

### 風控
- 單筆風險：
- 單日最大虧損：
- 連虧停手條件：
```

#### System Review

```md
## 當沖系統檢查

### 候選來源
- 盤前：
- 事件同步：
- 09:15 補充：
- 09:30 補充：

### 進場邏輯
- VWAP：
- 量能：
- 大盤：
- 結構：

### 出場邏輯
- 停損：
- 停利：
- 條件破壞：
- 強制清倉：

### 風險點
1. 
2. 
3. 

### 建議修正
1. 
2. 
3. 
```

## Tool Selection

Choose tools by task:

- 盤前準備缺什麼、今天要檢查哪些項目 → `scripts/generate_premarket_checklist.py`
- 開盤前要看一份當日總覽 → `scripts/format_daily_intraday_brief.py`
- 盤中要整理多檔標的、區分持續觀察 / 接近進場 / 降級移除 → `scripts/review_intraday_watchlist.py`
- 懷疑流程節點有問題、要快速做 ops/status 稽核 → `scripts/audit_intraday_flow.py`
- 收盤後要做來源回顧與規則違反檢討 → `scripts/format_postmarket_review.py`
- 修改 skill 後要檢查邊界有沒有跑掉 → `scripts/run_mini_eval.py`

## Scripts

Use bundled scripts when deterministic output is helpful:

- `scripts/generate_premarket_checklist.py`
  - generate a compact pre-market checklist
  - accepts initial watchlist, manual watchlist path, mode, risk budget, and notes

- `scripts/review_intraday_watchlist.py`
  - format a manually reviewed intraday watchlist into 持續觀察 / 接近進場 / 降級移除 language
  - does not classify signals on its own; it only structures labels and notes provided by the operator

- `scripts/audit_intraday_flow.py`
  - format a compact ops/status review of the main intraday runtime path from trading-day check to force exit
  - does not inspect logs or infer health automatically; it only structures the statuses provided as input

- `scripts/format_daily_intraday_brief.py`
  - format a daily intraday briefing from provided market bias, lists, priorities, and risk notes
  - does not rank candidates or generate signals automatically

- `scripts/format_postmarket_review.py`
  - generate a compact post-market review template
  - accepts symbols by source (pre-market / event sync / 09:15 / 09:30), best/worst trade, and rule violations

- `scripts/run_mini_eval.py`
  - run a small local boundary check against bundled positive / boundary / negative queries
  - useful after editing the skill description or narrowing scope

## References

Load `references/tw_day_trading_guide.md` for Taiwan intraday workflow guidance.
Load `references/qtds_system_mapping.md` when the task specifically concerns the user's `quantitative-trading-decision-system`.
Load `references/script_vocabulary.md` when editing or extending bundled scripts so internal naming stays consistent while human-facing output remains natural Chinese.
