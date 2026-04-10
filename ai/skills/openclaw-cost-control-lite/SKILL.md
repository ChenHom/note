---
name: openclaw-cost-control-lite
description: Use when the user asks for a quick, always-on reminder of OpenClaw cost control and efficiency rules. Trigger on requests about saving token cost, using cheaper models, shrinking context, caching repeated answers, or making the workflow cheaper and faster. Do not use for unrelated billing or generic prompt advice.
---

# OpenClaw Cost Control Lite

## One-line rule
少把不必要的 token 丟給 AI。

## Always-on rules
- 先縮上下文，不要整包塞歷史
- 簡單任務先用便宜模型或本地模型
- 重複問題先查 cache
- prompt 只留必要規則
- 設用量上限與告警

## Default routing
- FAQ / 格式化 / 短摘要 -> cheap/local
- 長推理 / 高風險 -> strong model
- 重複答案 -> cache

## If unsure
先看：
1. 能不能少送上下文
2. 能不能換便宜模型
3. 能不能快取
