---
name: workflow-system-designer
description: Design a reusable workflow system for a domain by separating shared core capabilities, add-on workflows, data/tool connectors, and final deliverables. Use when the user wants to turn a pile of prompts, docs, scripts, or ad-hoc processes into a maintainable skill/plugin architecture with clear boundaries and phased build order. Do not use for doing the domain task itself, implementing full production integrations, or simple one-off prompt edits.
---

# Workflow System Designer

把一個領域工作流整理成可維護、可擴充、可驗證的系統草案。

## In Scope
- 把 domain workflow 拆成 core / add-on 結構
- 辨識哪些應是 plugin / skill / connector / deliverable
- 定義責任邊界
- 設計 workflow system 的資料夾與文檔骨架
- 列出哪些能力值得先做、哪些應延後
- 幫使用者從「很多 prompts / scripts」收斂成系統設計

## Out of Scope
- 不直接替代 domain execution 本身
- 不直接完成所有 connector 實作
- 不直接實作完整產品或平台
- 不處理單純 frontmatter 觸發優化
- 不把整個問題硬包成 skill，如果還沒收斂架構

## When to Use
- 使用者想把某類工作流系統化
- 想把 skill / command / connector / output 分層
- 想把既有零散 prompts / docs / scripts 重構成可維護架構
- 想做 core plugin + add-on workflow 的能力設計
- 想先定系統骨架，再決定哪些要落成 skill

## When NOT to Use
- 只是要完成單次任務，不需要設計系統
- 只是要改一個 prompt 或 command 描述
- 已經有成熟架構，只差小修
- 需要的是 benchmark / routing eval，而不是系統設計

## Inputs You Should Collect
開始前先盤點：
- 目前要處理的是哪一類 domain workflow
- 現在有哪些 prompts / scripts / docs / tools
- 哪些是共享能力，哪些是場景專屬能力
- 哪些外部資料源 / 系統會接進來
- 最終交付物有哪些
- 誰會使用這個系統
- 哪些地方最容易 drift / 混線 / 重複

## Core Questions
一定要先回答：
1. 這個系統真正的 **core** 是什麼？
2. 哪些是 **add-on workflows**，不該混進 core？
3. 哪些是 **connector/data/tool interfaces**？
4. 最終要交付哪些 **deliverables**？
5. 哪些部分是 workflow，哪些部分只是內容知識？
6. 哪些是現在就該做，哪些該延後？

## Recommended Workflow
1. **定義問題邊界**
   - 先說清楚這個系統要解什麼，不解什麼
2. **抽 core layer**
   - 找出共享能力與底座
3. **拆 add-on workflows**
   - 按角色 / 任務 /場景拆分
4. **抽 connector layer**
   - 資料源、外部工具、平台接面獨立出來
5. **定 deliverables**
   - 最終輸出物要明確，不要只停在分析過程
6. **定觸發條件與責任邊界**
   - 什麼時候該叫這個系統，什麼時候不該
7. **做 phased plan**
   - Phase 1 / 2 / 3 怎麼演進

## Design Rules
- 先分清楚 core 與 add-on，不要一開始就全塞一起
- workflow 與 connector 分離，不要把資料源寫死進方法論
- deliverable 必須被定義，不然系統只會停在半路
- 不要把方法論、資料接面、最終輸出混成一坨
- 不要為了看起來完整，把所有未來需求都硬塞進 phase 1

## Typical Deliverables
這個 skill 應產出的東西通常包括：
- system scope summary
- core vs add-on map
- connector map
- deliverable map
- folder / file skeleton
- phase plan
- risk / drift points
- system scope card
- connector / deliverable mapping sheet

## Output Format
建議至少包含：
1. 目標與邊界
2. Core layer
3. Add-on workflows
4. Connector layer
5. Deliverable layer
6. Phase plan
7. What to build now vs later
8. Top failure modes / drift risks
9. Recommended next artifact to draft

## Quality Bar
- 不要只寫抽象原則，要能落成結構
- 不要把使用者的 domain 內容直接等同於 system design
- 不要把 connector 問題假裝成 skill 問題
- 不要缺 deliverable 規劃
- 不要忽略維護與擴充成本

## Definition of Done
- 核心層與擴充層清楚分開
- connector 與 workflow 有清楚邊界
- deliverables 被明確定義
- phase plan 可執行
- 使用者能看懂下一步該先建什麼、不該先建什麼
