# Live Stack Detection

這份文件補上 `tidb-rag-stack` 的可執行型操作重點：不是只講理論，而是要去確認現場到底有沒有可用的 RAG stack、API 與寫入口。

## 目的
當使用者說「直接寫進 RAG」、「幫我確認現場有沒有 ingest」、「這個 skill 能不能直接拿來寫資料」時，應先做現場探測，而不是只引用 skill 裡的理想 API contract。

## 探測順序

### 1. 找專案位置
優先找常見路徑：
- `/home/hom/services/rag-stack`
- 使用者明講的 repo/path

若找不到，再搜尋：
- `docker-compose.yml`
- `.env`
- `sql/001_init.sql`
- `app/api/server.py`
- `app/worker/server.py`

### 2. 看 compose
確認是否真的有：
- `qdrant`
- `minio`
- `rag-api`
- `rag-worker`

同時記下：
- port
- network
- env_file
- container name

### 3. 看 `.env`
確認：
- `RAG_API_PORT`
- `RAG_WORKER_PORT`
- `TIDB_HOST`
- `QDRANT_COLLECTION`
- `EMBEDDING_PROVIDER`
- `EMBEDDING_DIMENSIONS`

注意：若看到真實 API key，不要回貼、不重複暴露。

### 4. 看 schema
至少應有：
- `documents`
- `document_chunks`
- `retrieval_logs`

### 5. 看 app code
重點找：
- `POST /ingest`
- `POST /upload`
- `POST /search`
- `GET /documents`
- `GET /documents/{id}`
- `POST /documents/{id}/reindex`
- `DELETE /documents/{id}`

### 6. 建立可執行結論
結論要回答這幾件事：
- 現場有沒有 rag-stack
- 哪些服務是真的存在
- 哪些 endpoint 是真的存在
- 寫入應優先走哪個入口
- 寫入 payload 大致長什麼樣

## 寫入入口判斷

### 情境 A：有 `POST /ingest`
最適合拿來寫整理後的知識 chunk。

常見 payload：
```json
{
  "document_id": "...",
  "title": "...",
  "source_type": "manual",
  "source_uri": "...",
  "mime_type": "text/markdown",
  "chunks": ["...", "..."]
}
```

### 情境 B：只有 `POST /upload`
先把知識整理成 markdown / txt 檔，再走 upload。

### 情境 C：沒有 API，但 schema 與 app 邏輯存在
再考慮用內部程式碼、一次性 script 或 SQL + vector 寫入方案；這時要特別小心，不要跳過 Qdrant/TiDB 同步。

## 原則
- skill 是 playbook，不是 live connector
- 文件可當提示，但現場可執行入口一定要再查一次
- 以現場程式碼、健康檢查與成功 response 為準
