# Checklist Scenarios

這份清單用來快速人工驗證 `tidb-rag-stack` skill 是否仍然維持正確邊界與實作建議。

---

## Scenario 1 — Existing TiDB Docker stack only
### Prompt
> 我家已經有 TiDB / TiKV / PD，這樣能直接做 RAG 嗎？

### Expected
- 應回答：可作為資料底座
- 不應回答：已經是完整 RAG 檢索系統
- 應建議補：Qdrant、MinIO、rag-api、rag-worker
- 不應把 TiSpark 當 retrieval core

---

## Scenario 2 — User wants the most pragmatic architecture
### Prompt
> 幫我選最務實的自架方案，盡量沿用現有 TiDB。

### Expected
- 優先建議 TiDB + Qdrant + MinIO + rag-api/rag-worker
- 說明 TiDB 負責 metadata，不是主要向量檢索引擎

---

## Scenario 3 — Mock embedding bootstrap
### Prompt
> 先用 mock 跑起來驗流程就好。

### Expected
- 應允許 mock 先打通 upload / ingest / search
- 應明說 mock 排名品質不能當真

---

## Scenario 4 — Real embedding cutover
### Prompt
> 我現在要切 OpenAI embedding。

### Expected
- 應提醒設定 `.env`
- 應提醒 `EMBEDDING_DIMENSIONS` 與 collection 維度一致
- 應提醒需要重建 collection 或改新 collection 名稱

---

## Scenario 5 — Linux network failure
### Prompt
> rag-worker 連 TiDB timeout，host.docker.internal 不通。

### Expected
- 應建議 shared Docker network
- 應建議改用 TiDB service/container name

---

## Scenario 6 — Qdrant point ID failure
### Prompt
> Qdrant 說 point ID 不合法。

### Expected
- 應指出只能用 unsigned integer 或 UUID
- 不應繼續使用 `doc-1:0` 這種 point ID

---

## Scenario 7 — Markdown / HTML structure
### Prompt
> 為什麼 `section_title` 都是 null？

### Expected
- 應檢查 parser 是否真的做結構化解析
- 應提醒舊資料可能需要 reindex

---

## Scenario 8 — PDF support
### Prompt
> PDF 已能上傳，但 search 沒 page_no。

### Expected
- 應檢查 PDF page-aware parser 是否生效
- 應提醒 reindex PDF
- 不應把問題只歸咎於 search 層

---

## Scenario 9 — Search result quality
### Prompt
> 查詢結果排序怪怪的。

### Expected
- 應先檢查是否仍在 mock embedding
- 應檢查 hybrid / parser / reindex 狀態

---

## Scenario 10 — Existing live rag-stack detection
### Prompt
> 幫我看看現在這台機器上有沒有可直接寫入的 rag-stack。

### Expected
- 應先找實際專案路徑
- 應讀 compose、.env、schema、app code
- 應指出真的存在的 endpoint
- 不應只拿 reference docs 當現場事實

---

## Scenario 11 — Knowledge write into RAG
### Prompt
> 把昨天整理好的知識直接寫進 RAG。

### Expected
- 應先整理知識再寫入
- 應拆成可檢索 chunks
- 應補 metadata
- 應優先找 live `/ingest` 或 `/upload`
- 應在寫入後回報結果

---

## Scenario 12 — Out of scope guardrail
### Prompt
> 我要做完整 ACL / 多租戶 / OCR / cross-encoder reranker 平台。

### Expected
- 應明說這已超出 skill 的 MVP / pragmatic scope
- 不應假裝這份 skill 已完整涵蓋上述內容
