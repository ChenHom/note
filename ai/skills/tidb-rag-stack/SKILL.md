---
name: tidb-rag-stack
description: Build and operate a pragmatic self-hosted RAG stack on top of an existing TiDB deployment. Use when the user wants to assess whether a TiDB Docker stack can serve as the metadata/data base for RAG, add the missing retrieval/storage services (typically Qdrant, MinIO, rag-api, rag-worker), validate upload/ingest/search/reindex/delete flows, or detect a live rag-stack and prepare executable write/search actions. Do not use for TiDB-only SQL questions, generic non-TiDB RAG design, or heavy OpenSearch/ACL/OCR platform design.
---

# TiDB RAG Stack

把既有 TiDB Docker 叢集補成一套可用、可維護、可擴充的自架 RAG 基底；必要時直接探測現場 rag-stack，找出可執行的寫入與查詢入口。

## In Scope
- 檢查 TiDB / TiKV / PD / TiSpark 現況，判斷是否適合做 RAG 資料底座
- 規劃與部署 `qdrant`、`minio`、`rag-api`、`rag-worker`
- 建立 TiDB schema：`documents`、`document_chunks`、`retrieval_logs`
- 將 upload / ingest / search / reindex / delete 串起來
- 接 OpenAI-compatible embeddings
- 支援 txt / md / html / pdf（基礎版）
- 支援 Markdown / HTML 結構化 chunking
- 支援 PDF page-aware chunking（`page_no`）
- 補 filters、snippet、metadata join、基本 hybrid rerank
- 探測現場 rag-stack 是否存在、服務是否啟動、API 是否可用
- 找出實際寫入入口（如 `/ingest`、`/upload`）與 payload 形狀
- 針對已整理好的知識，產出可直接寫入 RAG 的內容與執行方案

## Out of Scope
- OCR 掃描型 PDF
- docx / xlsx / pptx 完整解析
- OpenSearch / Elasticsearch / 真正 BM25 系統
- cross-encoder reranker
- 完整 ACL / 多租戶 / auth 產品化
- queue / job orchestration / retry system 完整版
- 在未檢查實際環境前，憑空假設 API 一定存在或 payload 一定固定

## When to Use
- 使用者已經有 TiDB Docker 叢集，想確認能不能做 RAG
- 想走「TiDB 做 metadata、Qdrant 做向量檢索、MinIO 放原始檔」的務實路線
- 想把 MVP 做到：upload → parse → chunk → embed → search → reindex → delete
- 想把零散的 TiDB RAG 實作整理成可重複使用的操作流程
- 想知道現場是否已經有可用的 rag-stack 與 ingest/search 入口
- 想把已整理的核心知識直接寫入現場 RAG

## When NOT to Use
- 只是單一檔案小修，直接改檔即可
- 使用者要的是純雲端託管 RAG，不是自架 TiDB base
- 使用者要的是重型全文搜尋平台（應先評估 OpenSearch / Elasticsearch）
- 使用者只想問 TiDB 理論，不打算部署、探測或驗證任何實作

## Inputs You Should Collect
在動手前，先盤點這些資訊：
- 現有 Docker stack 有哪些容器
- TiDB host / network 怎麼連
- 是否已存在 rag 專案目錄
- embedding provider 要用 mock、OpenAI，或其他 OpenAI-compatible API
- Qdrant collection 名稱與 embedding 維度
- 是否需要保留舊 collection / 是否允許重建
- 是否只做文字檔，還是要驗 md/html/pdf
- 若目標是寫入知識：知識來源、要不要先整理、希望保留哪些 metadata

## Architecture
- **TiDB**：documents / chunks / retrieval logs / metadata
- **Qdrant**：向量索引與召回
- **MinIO**：原始檔案保存
- **rag-worker**：upload / parse / chunk / embed / ingest
- **rag-api**：search / filters / metadata join / docs management
- **Embedding provider**：OpenAI-compatible API（可先 mock，再切真 provider）

## Execution Modes
### Mode A：Architecture / Deployment
用於從零規劃或補齊 RAG stack。

### Mode B：Live Stack Detection
用於現場已可能存在 rag-stack，要確認實際服務、API、schema、環境變數與可執行入口。

### Mode C：Knowledge-to-RAG Write
用於把已整理的知識寫進現場 RAG。先整理知識，再找真實寫入口，再寫入與驗證。

## Execution Steps
1. **先判斷模式**
   - 如果使用者要架構/部署：走 Mode A
   - 如果使用者要確認現場有沒有可寫入 RAG：走 Mode B
   - 如果使用者要把知識寫進 RAG：走 Mode C

2. **盤現有 TiDB stack / rag-stack**
   - 確認有 `tidb`, `tikv*`, `pd*`
   - 不要把 TiSpark 當 query-time retrieval engine
   - 若已有 rag 專案，檢查 compose、`.env`、schema、app code
   - 下結論：TiDB 是資料底座，不是完整 RAG retrieval stack

3. **探測 live stack（Mode B/C 必做）**
   - 先找專案目錄，例如 `/home/hom/services/rag-stack`
   - 檢查 `docker-compose.yml`、`.env`、`sql/*.sql`
   - 檢查 app code 是否有 `POST /ingest`、`POST /upload`、`POST /search`
   - 檢查 health endpoint 與 port
   - 檢查是否有 `documents`、`document_chunks`、`retrieval_logs`
   - 若有敏感資訊（如 API key），不要回貼給使用者

4. **建立實際寫入判斷**
   - 若存在 `POST /ingest`：優先用它寫已整理好的 chunks
   - 若只有 `POST /upload`：產出 markdown/file 後再上傳
   - 若沒有 API 但有 DB schema：再考慮 SQL/程式內部寫入方案
   - 不要只根據 skill 文件假設 endpoint 存在；一定要先查現場實作

5. **整理知識內容（Mode C）**
   - 先把對話或草稿整理成乾淨知識
   - 拆成數個語意清楚的 chunks
   - 每塊要能單獨被搜到，不要全塞成一大段
   - 補齊 `document_id`、`title`、`source_type`、`source_uri`、`mime_type`

6. **執行寫入（Mode C）**
   - 優先用現場已存在的 worker/api 入口
   - 寫入後確認 response 成功
   - 需要時再用 `/search` 或 `/documents` 驗證資料可查到

7. **驗證核心工作流**
   - `POST /upload`
   - `POST /ingest`
   - `POST /search`
   - `GET /documents`
   - `GET /documents/{id}`
   - `POST /documents/{id}/reindex`
   - `DELETE /documents/{id}`

8. **驗證 parser / chunking**
   - Markdown 要能帶 `section_title`
   - HTML 要能帶 `section_title`
   - PDF 要能帶 `page_no`

9. **補 search 體驗**
   - filters：`document_id`, `source_type`, `mime_type`, `title_contains`
   - snippet
   - metadata join
   - hybrid rerank（輕量版）

## Decision Rules
- 如果只有 TiDB / TiKV / PD：判定為「可做資料底座，但不是完整 RAG stack」
- 如果使用者要最務實方案：優先 TiDB + Qdrant + MinIO + rag-api/worker
- 如果 embedding model 維度改變：優先提醒重建 collection
- 如果 HTML 結果很髒：提醒 reindex，因為 parser 改了後舊 chunks 不會自動變乾淨
- 如果 PDF 沒 page info：檢查 parser 是否已切到 page-aware，並要求 reindex
- 如果使用者只想快速 demo：可先用 mock embedding；但明說排序品質不能當真
- 如果要進實戰：必須切真 embedding provider
- 如果 skill 文件與現場程式碼不一致：以現場程式碼與可執行 endpoint 為準
- 如果使用者要直接寫入 RAG：先整理知識，再確認 live endpoint，再寫入

## Search Features
- Qdrant vector retrieval
- TiDB metadata join
- filters:
  - `document_id`
  - `source_type`
  - `mime_type`
  - `title_contains`
- hybrid rerank（輕量 keyword + vector）
- `snippet`
- `section_title`
- `page_no`（PDF）

## Validation Checklist
- `rag-api` / `rag-worker` / `qdrant` / `minio` 都正常啟動
- ingest 同時寫入 Qdrant 與 TiDB
- search 會回 metadata
- retrieval_logs 有寫入
- upload 會產生 `object_key`
- reindex 會重建 chunks 與向量
- delete 會清 TiDB / Qdrant / MinIO
- Markdown / HTML 會帶 `section_title`
- PDF 會帶 `page_no`
- 現場寫入入口已確認，不是只憑文件推測
- 知識寫入後可用 `/documents` 或 `/search` 驗證

## Definition of Done
要算完成，至少要達到：
- 使用者可以 upload 一份文件並搜得到，或把整理後知識直接 ingest 進去
- documents / chunks / logs 都有寫進 TiDB
- search 結果不是只有向量分數，還有 metadata/snippet
- reindex 和 delete 都實測成功
- 現場寫入入口與 payload 形狀已確認
- 使用範例與排錯說明已寫清楚

## Deliverables
至少應包含：
- `docker-compose.yml`
- `.env.example`
- Python app skeleton
- TiDB schema SQL
- parser / chunker
- upload / search / management APIs
- live detection / knowledge write runbook
- 使用範例與驗證指令
- troubleshooting notes
- 可重用 templates（如 `.env.example`、compose 核心片段）

## References
- `references/architecture.md`
- `references/deployment-runbook.md`
- `references/config-examples.md`
- `references/api-contract.md`
- `references/usage-examples.md`
- `references/troubleshooting.md`
- `references/live-stack-detection.md`
- `references/knowledge-write-runbook.md`

## Scripts
- `scripts/checklist.md`
- `scripts/detect_live_stack.md`
- `scripts/prepare_ingest_payload.md`
- `scripts/verify_write.md`
- `scripts/write_to_rag.md`
- `scripts/run_knowledge_to_rag.md`
- `scripts/detect_live_stack.py`
- `scripts/prepare_ingest_payload.py`
- `scripts/verify_write.py`
- `scripts/write_to_rag.py`
- `scripts/run_knowledge_to_rag.py`

## Templates
- `templates/.env.example`
- `templates/docker-compose.core.yml`

## Evals
- `evals/README.md`
- `evals/cases.md`
- `evals/checklist-scenarios.md`
