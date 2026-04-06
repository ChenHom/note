# Prepare Ingest Payload

當使用者要把整理後的知識直接寫入 RAG，請照這份流程準備 payload。

## Goal
把原始討論整理成適合 `POST /ingest` 的資料。

## Steps
1. 先整理知識
   - 不要直接把原始對話整包塞進去
   - 至少整理成：核心結論、架構分工、落地步驟、常見坑、決策規則

2. 拆成 chunks
   - 每個 chunk 一個主題
   - 每塊可獨立被命中
   - 不要太長

3. 準備 metadata
   - `document_id`
   - `title`
   - `source_type`
   - `source_uri`
   - `mime_type`

4. 組 payload
```json
{
  "document_id": "...",
  "title": "...",
  "source_type": "telegram-summary",
  "source_uri": "...",
  "mime_type": "text/markdown",
  "chunks": [
    "chunk 1",
    "chunk 2"
  ]
}
```

5. 檢查一致性
   - `document_id` 可追蹤來源
   - `title` 能讓人一看就懂
   - `chunks` 數量合理
   - 不要混入 secrets

## Notes
- 如果現場只有 `/upload`，就改成先生成 markdown 檔再上傳
- 如果 skill 文件與現場 request model 不一致，以現場 request model 為準
