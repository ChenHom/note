---
name: tw-swing-trading
description: Build and review Taiwan stock swing-trading plans, trend-following checklists, breakout and 拉回買點 rules, watchlist quality vs entry quality judgments, and risk controls. Use when the user asks about 台股波段 planning, 強勢股篩選, 趨勢突破, pullback entries, Minervini-style setups, VCP-like contractions, 假突破判斷, 部位管理, or converting stock ideas into rule-based swing trade plans. Do not use for pure當沖 execution, generic skill-authoring tasks, intraday signal debugging, or pure financial statement / sentiment summaries without trade planning.
---

# Taiwan Swing Trading

## Purpose

Structure Taiwan stock swing-trading work into a clear workflow for:

- universe filtering
- trend quality review
- breakout / pullback planning
- stop placement
- position sizing
- post-entry management
- post-trade review

Favor rule-based planning over narrative conviction. Prefer strong trends, tight structures, and defined risk.

## Use This Skill When

Apply this skill when the request is about:

- 台股波段交易計畫
- 強勢股篩選
- 趨勢突破 / pullback / base breakout
- Minervini / momentum / stage-2 style setups
- 進場區、停損、加碼、減碼、移動停損
- 把股票想法寫成可執行的波段計畫
- 檢查一檔股票是否適合波段而不是當沖

## Do Not Use This Skill When

Do not use this skill for:

- 純當沖執行與日內補充邏輯
- skill 建立、benchmark、frontmatter description 改寫
- 純財報摘要、新聞摘要、情緒摘要而沒有交易規劃
- 長期資產配置或價值投資報告

If the request is mainly intraday, prefer `tw-day-trading`.

## Workflow

### 1. Classify The Setup Type

Classify the request before giving advice:

- **breakout**: price is near pivot / box high / stage-2 continuation
- **pullback**: trend is intact and the user wants a lower-risk re-entry
- **base-building**: stock is tightening and not yet actionable
- **position-management**: user already holds and wants stop / trim / hold guidance
- **post-mortem**: user wants to review whether the trade idea was good or sloppy

### 2. Check Trend Quality First

Never start from story alone. Start from structure.

Review these first:
- price above major moving averages
- moving averages aligned in the right order
- 200-day slope not broken
- stock not too far from recent highs
- relative strength versus market / peers
- liquidity sufficient for multi-day positioning

Prefer language like:
- trend intact
- structure constructive
- extended
- loose and noisy
- not yet actionable

Avoid vague language like "感覺不錯".

### 3. Decide Whether It Is Watchlist Quality Or Entry Quality

Make this distinction explicit before discussing entry.

- **watchlist quality**: structurally interesting, worth monitoring, but not yet actionable
- **entry quality**: trigger is near, invalidation is clear, and risk can be defined cleanly

Do not confuse a good story or good relative strength with a ready entry.

### 4. Evaluate The Base Or Pullback

Use one of these three lenses.

#### A. Breakout Setup

Require:
- clear pivot / box high / prior swing high
- tightness before breakout
- no obvious late-stage exhaustion
- volume expansion or at least constructive participation

Avoid when:
- price is already extended well above pivot
- breakout comes from a wide-and-loose mess
- stock is too close to overhead supply

#### B. Pullback Setup

Require:
- prior trend already proven
- pullback into support, moving average, or prior breakout zone
- price action tightens during the pullback
- invalidation point is clear

Prefer pullbacks that look controlled, not panicked.

#### C. Base-Building / Watchlist Setup

Use when the stock is not yet actionable but worth tracking.

Record:
- pivot candidate
- support zone
- what would confirm actionability
- what would invalidate the idea

### 4. Convert The Idea Into A Trade Plan

Write every swing idea into five parts:

1. thesis
2. trigger
3. invalidation
4. position size / risk
5. management plan

Recommended output language:
- Enter only if...
- Invalidate if...
- Trim if...
- Add only after...
- Avoid if...

### 5. Plan Risk Before Entry

Before approving a trade idea, define:

- stop level
- percent risk from entry to stop
- account risk per trade
- max position size
- whether the trade allows scaling in
- what to do if the stock gaps through the stop

Default risk posture unless the user provides house rules:
- risk per trade: `0.25%–1.00%` of account
- avoid oversized positions in names with poor liquidity
- prefer smaller starters when the setup is still emerging

### 6. Manage The Trade After Entry

Keep management explicit.

Possible actions:
- hold while trend remains intact
- trim partials into extension
- raise stop only after structure improves
- do not average down on failed breakouts
- review whether the stock is acting like a leader or stalling

Useful review questions:
- Is the stock acting better than the index?
- Is price respecting the breakout / pullback level?
- Is volume confirming continuation or fading badly?
- Is the trade still early-stage, or already mature and prone to shakeout?

### 7. End With Operator-Ready Output

Prefer clean outputs over essays.

#### Swing Plan

```md
## 台股波段計畫

### 標的
- 代號：
- 類型：突破 / 拉回 / 觀察中

### 結構判斷
- 趨勢：
- 關鍵支撐：
- 關鍵突破位：
- 是否延伸：

### 進場規則
- 只在……時進場
- 若……則放棄

### 風控
- 停損：
- 單筆風險：
- 初始部位：

### 持倉管理
- 加碼條件：
- 減碼條件：
- 完全出場條件：
```

#### Swing Review

```md
## 波段交易檢查

### 結構
- 趨勢是否完整：
- base / pullback 是否乾淨：
- 是否過度延伸：

### 風險
- 停損是否合理：
- 部位是否過大：
- 是否有攤平虧損風險：

### 建議
1. 
2. 
3. 
```

## Scripts

Use bundled scripts when deterministic output is helpful:

- `scripts/generate_swing_plan.py`
  - generate a compact TW swing-trading plan template

- `scripts/review_symbol_setup.py`
  - format a single symbol review into watchlist-quality vs entry-quality language
  - useful when the user asks whether a stock is ready now or only worth monitoring

- `scripts/run_mini_eval.py`
  - run a small local boundary check against bundled positive / boundary / negative queries

## References

Load `references/tw_swing_trading_guide.md` for Taiwan swing-trading workflow guidance.
Load `references/eval_queries.md` and `references/eval_rubric.md` when checking skill boundary quality.
