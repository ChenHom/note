---
name: openclaw-cost-control-lite
description: Use as the always-on shortcut for OpenClaw cost control and efficiency. Trigger on saving token cost, shrinking context, using cheaper models, caching repeated answers, or making workflows cheaper and faster. Do not use for unrelated billing or generic prompt advice.
---

# OpenClaw Cost Control Lite

## Shortcut
少把不必要的 token 丟給 AI。

## Always-on rules
- 先縮上下文
- 簡單任務先用便宜模型或本地模型
- 重複問題先查 cache
- prompt 只留必要規則
- 設用量上限與告警

## Default routing
- FAQ / 格式化 / 短摘要 -> cheap/local
- 長推理 / 高風險 -> strong model
- 重複答案 -> cache

## How to use
當你需要省成本時，先看這三件事：
1. 能不能少送上下文
2. 能不能換便宜模型
3. 能不能快取
