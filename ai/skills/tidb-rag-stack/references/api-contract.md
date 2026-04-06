# API Contract

這份文件整理 `tidb-rag-stack` 目前的主要 API 介面與常見 request / response 範例。

---

## rag-worker

### `GET /health`
#### Response
```json
{
  "ok": true,
  "role": "worker",
  "qdrant_collection": "document_chunks",
  "minio_bucket": "documents"
}
```

---

### `POST /ingest`
用於直接傳 chunks（不經 file upload）。

#### Request
```json
{
  "document_id": "doc-1",
  "title": "測試文件",
  "source_type": "manual",
  "source_uri": "telegram:test",
  "mime_type": "text/plain",
  "chunks": ["第一段內容", "第二段內容"],
  "object_key": null
}
```

#### Response
```json
{
  "document_id": "doc-1",
  "ingested_chunks": 2,
  "tidb_written": true,
  "object_key": null
}
```

---

### `POST /upload`
上傳檔案到 MinIO，解析、chunk、embedding、寫入 Qdrant 與 TiDB。

#### Form fields
- `file`
- `document_id`
- `title`
- `source_type`
- `source_uri`（optional）
- `chunk_size`（optional）
- `chunk_overlap`（optional）

#### Example
```bash
curl -X POST http://127.0.0.1:8011/upload \
  -F 'document_id=doc-md-1' \
  -F 'title=Markdown 測試文件' \
  -F 'source_type=upload' \
  -F 'file=@./example.md;type=text/markdown'
```

#### Response
```json
{
  "document_id": "doc-md-1",
  "ingested_chunks": 4,
  "tidb_written": true,
  "object_key": "raw/docs/doc-md-1/example.md",
  "filename": "example.md"
}
```

---

## rag-api

### `GET /health`
#### Response
```json
{
  "ok": true,
  "role": "api",
  "qdrant_collection": "document_chunks",
  "embedding_provider": "openai-compatible",
  "tidb": "tidb:4000/rag"
}
```

---

### `POST /search`
支援 vector retrieval + metadata join + filters + hybrid rerank。

#### Request
```json
{
  "query": "OpenAI embedding",
  "limit": 5,
  "document_id": null,
  "source_type": "upload",
  "mime_type": null,
  "title_contains": null,
  "hybrid": true
}
```

#### Response
```json
{
  "query": "OpenAI embedding",
  "count": 1,
  "latency_ms": 210,
  "results": [
    {
      "id": "96bfba1f-a026-5f29-9cb6-eef33495c01d",
      "score": 0.842512,
      "vector_score": 0.8123,
      "document_id": "doc-md-1",
      "chunk_index": 0,
      "section_title": "檢索重點",
      "page_no": null,
      "snippet": "…OpenAI embedding 可以提升語意搜尋品質…",
      "metadata": {
        "id": "doc-md-1:0",
        "document_id": "doc-md-1",
        "chunk_index": 0,
        "content_text": "OpenAI embedding 可以提升語意搜尋品質。",
        "token_count": 18,
        "section_title": "檢索重點",
        "page_no": null,
        "qdrant_point_id": "96bfba1f-a026-5f29-9cb6-eef33495c01d",
        "title": "Markdown 測試文件",
        "source_type": "upload",
        "source_uri": null,
        "mime_type": "text/markdown",
        "status": "active"
      }
    }
  ]
}
```

---

### `GET /documents`
列出文件與 chunk 數量，支援輕量 query filters：
- `source_type`
- `mime_type`
- `title_contains`
- `status`
- `limit`
- `offset`

#### Example
```bash
curl 'http://127.0.0.1:8010/documents?source_type=upload&mime_type=text/markdown&title_contains=測試&status=active'
```

#### Response
```json
{
  "count": 2,
  "documents": [
    {
      "id": "doc-md-1",
      "title": "Markdown 測試文件",
      "source_type": "upload",
      "source_uri": null,
      "object_key": "raw/docs/doc-md-1/example.md",
      "mime_type": "text/markdown",
      "status": "active",
      "created_at": "2026-03-31T02:14:39",
      "updated_at": "2026-03-31T02:14:39",
      "chunk_count": 4
    }
  ],
  "filters": {
    "source_type": "upload",
    "mime_type": "text/markdown",
    "title_contains": "測試",
    "status": "active"
  }
}
```

---

### `GET /documents/{id}`
查看單一文件與 chunks 詳情。

#### Response
```json
{
  "document": {
    "id": "doc-md-1",
    "title": "Markdown 測試文件",
    "source_type": "upload",
    "source_uri": null,
    "object_key": "raw/docs/doc-md-1/example.md",
    "mime_type": "text/markdown",
    "checksum": null,
    "status": "active",
    "created_at": "2026-03-31T02:14:39",
    "updated_at": "2026-03-31T02:14:39"
  },
  "chunks": [
    {
      "id": "doc-md-1:0",
      "document_id": "doc-md-1",
      "chunk_index": 0,
      "content_text": "OpenAI embedding 可以提升語意搜尋品質。",
      "token_count": 18,
      "section_title": "檢索重點",
      "page_no": null,
      "qdrant_point_id": "96bfba1f-a026-5f29-9cb6-eef33495c01d",
      "created_at": "2026-03-31T02:14:39",
      "updated_at": "2026-03-31T02:14:39"
    }
  ],
  "chunk_count": 4
}
```

---

### `POST /documents/{id}/reindex`
根據 MinIO 原始檔重新 parse / chunk / embed / upsert。

#### Request
```json
{
  "chunk_size": 500,
  "chunk_overlap": 50
}
```

#### Response
```json
{
  "reindexed": true,
  "document_id": "doc-md-1",
  "chunk_count": 4
}
```

---

### `DELETE /documents/{id}`
刪除文件對應的：
- TiDB document / chunks
- Qdrant points
- MinIO object（若存在）

#### Response
```json
{
  "deleted": true,
  "document_id": "doc-md-1"
}
```

---

## Notes
- `section_title` 主要用於 Markdown / HTML 結構化 chunking
- `page_no` 主要用於 PDF page-aware chunking
- `snippet` 是給 UI / 人類閱讀的摘要，不等於完整 chunk
- `metadata.content_text` 才是完整 chunk 內容
