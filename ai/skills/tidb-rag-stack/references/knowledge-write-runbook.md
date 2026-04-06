# Knowledge Write Runbook

當使用者要把討論整理後直接寫進 RAG，請走這份流程。

## 1. 先整理知識，不要把原始對話整包塞進去
至少整理成：
- 核心結論
- 架構分工
- 落地步驟
- 常見坑
- 可直接重用的決策規則

## 2. 拆成可檢索 chunks
原則：
- 每個 chunk 一個明確主題
- 不要過長
- 每塊要能單獨被 query 命中
- 盡量保留標題感與語意完整性

## 3. 補 metadata
至少帶：
- `document_id`
- `title`
- `source_type`
- `source_uri`
- `mime_type`

若是對話整理，建議：
- `source_type=telegram-summary` 或其他可辨識值
- `mime_type=text/markdown`

## 4. 找真實寫入口
優先順序：
1. `POST /ingest`
2. `POST /upload`
3. 內部 app / script

不要只因 skill 文件寫了某個 endpoint，就假設現場一定有。

## 5. 執行寫入
### 範例：`POST /ingest`
```json
{
  "document_id": "telegram-tidb-rag-knowledge-2026-03-31",
  "title": "TiDB-based 自架 RAG 核心知識整理",
  "source_type": "telegram-summary",
  "source_uri": "telegram://meeting-room/2026-03-31/tidb-rag-stack",
  "mime_type": "text/markdown",
  "chunks": [
    "chunk 1...",
    "chunk 2..."
  ]
}
```

### 可用 helper scripts
- `scripts/detect_live_stack.py`
- `scripts/prepare_ingest_payload.py`
- `scripts/write_to_rag.py`
- `scripts/verify_write.py`
- `scripts/run_knowledge_to_rag.py`

用途：
- 先探測現場 rag-stack
- 再從整理好的 markdown 生成 ingest payload
- 直接寫入 `/ingest`
- 寫入後驗證 document 與 search
- 若想一條龍執行，直接跑 `run_knowledge_to_rag.py`

## 6. 寫入後驗證
至少確認：
- response 成功
- `ingested_chunks` 數量合理
- `tidb_written=true`（若有此欄位）
- 可再用 `/documents`、`/documents/{id}` 或 `/search` 驗證

## 7. 回報時要說清楚
- 寫到哪個 document_id
- 幾個 chunks
- 用哪個入口寫進去
- 有沒有 object storage
- 若看到敏感資訊風險（如 API key 明碼），可以提醒，但不要回貼內容

## 用詞提醒
說明 skill 能力時，避免說「天然知道」。
改用：
- 「不會天生知道你目前環境裡的資訊」
- 「本來就不會知道你目前的環境裡有哪些實作細節」
