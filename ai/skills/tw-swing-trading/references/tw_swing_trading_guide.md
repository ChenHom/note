# Taiwan Swing Trading Guide v2

## Scope

This reference supports Taiwan stock swing-trading workflows focused on momentum, breakouts, constructive pullbacks, and disciplined risk management.

This v2 guide intentionally borrows useful language patterns from the user's local stock projects:
- `quantitative-trading-decision-system`
- `quant-feather-integration`
- `StrategyExecutor_feather`

## Extracted Trading Language

Use these phrases consistently because they are short, operator-friendly, and map well to how the user already thinks about trading systems.

### Preferred Terms

- 結構完整 / 結構破壞
- 可交易性 / 不可交易性
- 候選池 / 觀察名單 / 主戰場
- 強勢延續 / 剛脫離整理 / 主題跟隨
- 流動性優先
- broad pool first, rank later
- 不要太早 hard gate
- ranking, not prophecy
- watchlist quality ≠ entry quality
- 強而可延續 / 強但已亂掉
- recall first, precision second（用在觀察名單）
- 先定義任務，再調參
- 先判斷是 watchlist quality 還是 entry quality

### Avoid

- 太故事化、沒有結構描述的語句
- 只說「看起來很強」卻沒有 trigger / invalidation
- 把 watchlist 和買進清單混為一談

## Taiwan-Specific Directions

### 1. Liquidity First

For TW swing trading, liquidity still comes before beautiful charts.

Review:
- average turnover
- spread quality
- whether the stock becomes difficult to exit once momentum fades
- whether the stock only looks explosive because liquidity is thin

A stock can look technically strong but still be poor swing material if exit quality is unreliable.

### 2. Watchlist Quality vs Entry Quality

Borrow this distinction from the local intraday project thinking.

Do not ask only:
- 這檔今天是不是最強？

Also ask:
- 這檔值不值得放進波段觀察名單？
- 它現在是 watchlist quality，還是已經是 entry quality？

A stock may deserve monitoring even if it is not yet actionable.

### 3. Broad Pool First, Rank Later

Do not hard-filter too aggressively at the front.

For Taiwan swing workflows, the better sequence is:
1. remove obvious garbage / illiquid names
2. keep a broad candidate pool of interesting names
3. rank by tradability + structure + continuity
4. only then narrow to the final watchlist

This helps avoid missing:
- 剛脫離整理的股票
- 族群內不是最前排、但有機會補漲的股票
- 還沒完全突破、但已開始緊縮的股票

### 4. Three Useful Swing Archetypes

Use at least three archetypes instead of one generic "strong stock" bucket.

#### A. Breakout Continuation

Traits:
- price near pivot / box high / recent swing high
- volume and participation improve
- structure still tight enough to define risk
- not obviously late-stage or exhausted

Use when the stock is close to actionability.

#### B. Expansion From Base

Traits:
- recently expanded from consolidation
- not yet wildly extended
- turnover improving
- likely to produce follow-through if market cooperates

This is often where a lot of good swing names begin.

#### C. High-Turnover Theme Follower

Traits:
- belongs to an active group / theme
- own turnover is large enough
- may not be the strongest chart, but is receiving real money attention
- often becomes a second-wave or lagged continuation candidate

Do not ignore this bucket just because it is not the obvious chart leader.

### 5. Structure Score Over Story Score

Use a structure-first checklist.

Review:
- trend intact or not
- proximity to highs
- quality of consolidation
- whether price tightened before the move
- whether pullback is controlled or messy
- whether overhead supply is too close

A good story with bad structure is not a good swing trade.

### 6. Breakout Failure Handling

Taiwan swing trading needs explicit handling for false breakouts.

Failure signs:
- breakout immediately loses the pivot
- volume spike comes with ugly upper shadow and no follow-through
- price gaps up into resistance and cannot hold
- stock becomes extended too quickly, then stalls

Use language like:
- 突破失敗
- 假突破
- 結構開始鬆掉
- 先降為觀察，不要硬拗成持股理由

### 7. Pullback Quality

Not every red candle is a pullback buy.

Prefer pullbacks that are:
- controlled
- lower-volume than the prior advance
- near a known support zone
- easy to invalidate if wrong

Reject pullbacks that are:
- panicked
- high-volume breakdowns disguised as "便宜了"
- structurally below the area that justified the original thesis

### 8. Event And Theme Awareness

Pure chart reading is not enough in TW equities.

Useful context sources include:
- monthly revenue updates
- earnings / guidance
- conference / legal person attention
- policy / industry themes
- group rotation and leader-follower behavior

Do not turn the skill into a news summarizer. Use events as context for structure and continuity.

### 9. Risk Management For Taiwan Swing Trading

Use risk language that matches the user's local style:
- define risk first
- keep outputs operator-ready
- do not oversize thin names
- do not average down failed breakouts
- separate starter size from confirmation add size

Good planning questions:
- Is the setup already extended and forcing a bad stop distance?
- Is this a full-size setup, or only a starter?
- If the breakout fails tomorrow, do we already know what invalidates the thesis?
- Is this a leader worth holding through noise, or a follower that should be traded tighter?

## Practical Output Style

Prefer concise, decision-ready output:

- setup type
- watchlist quality or entry quality
- trigger
- invalidation
- initial size posture
- trim / add / exit conditions

## Example Phrasing

### Good
- 這檔目前是 watchlist quality，不是 entry quality。
- 結構還算完整，但突破位太近，RR 不夠漂亮。
- 這是強勢延續，不是低風險拉回。
- 可以先小倉位試單，確認突破站穩再談加碼。
- 這檔強，但已經有點亂掉，別把故事感當結構感。

### Bad
- 感覺會漲。
- 看起來滿強的，可以試試。
- 故事很好，所以先買再說。
