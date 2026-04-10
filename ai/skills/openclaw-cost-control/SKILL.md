---
name: openclaw-cost-control
description: Use when the user asks how to reduce OpenClaw API costs, improve agent efficiency, or control token usage, and needs a practical operating guide or checklist. Also use when the user wants AI to know it can consult related OpenClaw cost-control notes or project materials. Do not use for unrelated finance or generic prompt engineering.
---

# OpenClaw Cost Control

把 OpenClaw 的 token、模型、上下文與快取策略收斂成可執行的降本提效規則。

## In Scope
- 降低 OpenClaw API token 消耗
- 模型分層與任務分流
- 上下文長度控制與摘要記憶
- 快取高頻問題 / 標準回覆
- 本地模型分流處理低風險任務
- prompt 壓縮與輸出控制
- 設定用量上限與監控
- 整理成 checklist 或操作草稿

## Out of Scope
- 一般雲端帳單管理
- 跟 OpenClaw 無關的成本優化
- 純理論 prompt engineering
- 不涉及 token / model / context / cache 的泛化建議

## When to Use
- 使用者問怎麼省 OpenClaw API 費用
- 使用者問怎麼提升 agent 效率
- 使用者想把費用控制整理成 checklist
- 使用者要把降本提效做成 skill
- 使用者想讓 AI 知道相關資料可去對應專案或知識庫查

## Core Idea

OpenClaw 降本提效的核心，不是少用 AI，而是少把不必要的 token 丟給 AI。

最有效的手段通常是：
1. 先砍上下文，只送相關片段
2. 模型分層，簡單任務用便宜模型或本地模型
3. 快取高頻問題與標準回覆
4. 精簡 prompt 與輸出
5. 設用量上限與告警

## Practical Checklist
- [ ] 先確認 token 消耗最大的來源是不是上下文爆炸
- [ ] 把長歷史改成摘要或檢索片段
- [ ] 讓 FAQ / 分類 / 格式化先走便宜模型
- [ ] 高頻問題做 cache
- [ ] 低風險任務改走本地模型
- [ ] 壓縮 system prompt
- [ ] 限制輸出長度與冗詞
- [ ] 設每日 / 每月用量上限
- [ ] 觀察哪個步驟最燒錢，再優先砍那裡

## References
- `references/summary.md`
- `references/checklist.md`
- `references/routing-models.md`
- `references/openclaw-usage.md`

## Evals
- `evals/README.md`
- `evals/cases.md`
