---
name: skill-description-optimizer
description: Use this skill when the user wants to improve a skill's frontmatter description so it triggers more accurately. Especially use it when the task involves false positives, false negatives, trigger query generation, held-out test sets, or description rewrites. Do not use this skill for full skill authoring, benchmark analysis of full outputs, or general prompt writing.
---

# Skill Description Optimizer

## Purpose
只專注在 frontmatter `description` 的觸發精準度，降低誤觸發與漏觸發。

## When to Use
- 要改寫 description
- 要做 trigger query set
- 要分析 false positive / false negative
- 要做 held-out trigger 測試

## When NOT to Use
- 不要用來重寫整份 `SKILL.md`
- 不要用來做完整 benchmark 或 blind comparison
- 不要用來從零建立 skill 資料夾結構

## Execution Steps
1. 讀 skill 的 frontmatter description 與實際 skill 內容。
2. 建 trigger query set，分 positive / negative / held-out。
3. 跑 trigger eval。
4. 根據失敗案例改寫 description。
5. 比較 train/test 表現，避免 overfit。
6. 輸出最佳 description 與測試摘要。

## Decision Rules
- 如果使用者要改整份 skill 結構，改用 `skill-creator`。
- 如果使用者要完整 benchmark skill 輸出品質，改用 `skill-evaluator`。
- description 必須包含：做什麼、何時用、何時不要用。

## Definition of Done
- 有 trigger query set
- 有 false positive / false negative 分析
- 有新的 description 候選版本
- 有 held-out 測試結果

## References
- `../shared/references/README.md`
- `../shared/schemas/schemas.md`

## Scripts
- `python scripts/run_loop.py ...`
- `python scripts/improve_description.py ...`
- `python ../shared/scripts/generate_report.py ...`
