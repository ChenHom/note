---
name: skill-evaluator
description: Use this skill when the user wants to evaluate whether a skill is performing correctly, compare it against a baseline, or analyze failures across test cases. Especially use it when the task involves eval prompts, assertions, rubrics, benchmark summaries, blind comparisons, or regression tracking. Do not use this skill to write a new skill from scratch or to optimize only the frontmatter description.
---

# Skill Evaluator

## Purpose
評估一個 skill 是否真的比 baseline 更好，並找出退化、失敗案例、波動來源與可量化差異。

## When to Use
- 要建立或擴充 eval prompt set
- 要寫 assertions / rubrics / benchmark summary
- 要做 baseline vs with-skill 比較
- 要做 blind comparison
- 要分析 fail cluster、variance、regression

## When NOT to Use
- 不要用來從零寫一個新 skill
- 不要用來重寫整份 `SKILL.md`
- 不要用來只優化 frontmatter description

## Execution Steps
1. 讀 skill 與既有 eval 資料。
2. 建 prompt set，區分 explicit / implicit / negative / edge cases。
3. 建 deterministic checks 與 rubric。
4. 跑 with-skill / baseline 或 old-skill 對照。
5. 產出 grading、benchmark、blind comparison、fail cluster 分析。
6. 總結哪些 assertion 有區辨力，哪些 eval 本身有問題。

## Decision Rules
- 如果任務重心是 skill 邊界、資料夾結構、`SKILL.md` authoring，改用 `skill-creator`。
- 如果任務重心是 frontmatter description trigger rate，改用 `skill-description-optimizer`。
- 若 assertion 可程式化，優先腳本化，不靠純文字判斷。

## Definition of Done
- 有 prompt set
- 有 assertions / rubric
- 有 benchmark 或 comparison 結果
- 有清楚的 fail / regression 分析

## References
- `../shared/schemas/schemas.md`
- `agents/grader.md`
- `agents/comparator.md`
- `agents/analyzer.md`

## Scripts
- `python scripts/run_eval.py ...`
- `python ../shared/scripts/aggregate_benchmark.py ...`
- `python ../shared/scripts/generate_report.py ...`
