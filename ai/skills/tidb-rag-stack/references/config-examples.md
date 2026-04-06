# Config Examples

這份文件整理 `tidb-rag-stack` 最常用的設定範例，重點是：
- `.env` 怎麼填
- `docker-compose.yml` 哪些欄位最關鍵
- 切 embedding model / collection 時要注意什麼

---

## 1. `.env` 範例

### A. Mock embedding（先打通流程）
```env
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=change-me-minio
MINIO_CONSOLE_PORT=9001
MINIO_API_PORT=9000
QDRANT_PORT=6333
QDRANT_GRPC_PORT=6334
RAG_API_PORT=8010
RAG_WORKER_PORT=8011

TIDB_HOST=tidb
TIDB_PORT=4000
TIDB_USER=root
TIDB_PASSWORD=
TIDB_DATABASE=rag

EMBEDDING_PROVIDER=mock
EMBEDDING_MODEL=mock-384
EMBEDDING_BASE_URL=
EMBEDDING_API_KEY=
EMBEDDING_DIMENSIONS=384

QDRANT_COLLECTION=document_chunks
MINIO_BUCKET=documents
LOG_LEVEL=INFO
```

### B. OpenAI 官方 embedding
```env
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=change-me-minio
MINIO_CONSOLE_PORT=9001
MINIO_API_PORT=9000
QDRANT_PORT=6333
QDRANT_GRPC_PORT=6334
RAG_API_PORT=8010
RAG_WORKER_PORT=8011

TIDB_HOST=tidb
TIDB_PORT=4000
TIDB_USER=root
TIDB_PASSWORD=
TIDB_DATABASE=rag

EMBEDDING_PROVIDER=openai-compatible
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_API_KEY=your_openai_api_key
EMBEDDING_DIMENSIONS=1536

QDRANT_COLLECTION=document_chunks
MINIO_BUCKET=documents
LOG_LEVEL=INFO
```

### C. OpenAI-compatible 本地端點
例如本地有相容 `/embeddings` API：
```env
EMBEDDING_PROVIDER=openai-compatible
EMBEDDING_MODEL=bge-m3
EMBEDDING_BASE_URL=http://your-local-embedding-service:8000/v1
EMBEDDING_API_KEY=
EMBEDDING_DIMENSIONS=1024
QDRANT_COLLECTION=document_chunks_local
```

---

## 2. `docker-compose.yml` 關鍵欄位

### 最小核心 services
應至少有：
- `qdrant`
- `minio`
- `rag-api`
- `rag-worker`

### 關鍵設計原則
- `rag-api` / `rag-worker` 要能連到 TiDB
- Linux 上如果 `host.docker.internal` 不通，就把 rag services 掛到 TiDB 的 Docker network
- `env_file: .env` 要確保 API / worker 用同一組 embedding 與 collection 設定

### 例：rag-api / rag-worker 關鍵片段
```yaml
rag-api:
  build:
    context: ./app
    dockerfile: Dockerfile
  env_file:
    - .env
  environment:
    APP_ROLE: api
  depends_on:
    - qdrant
    - minio
  ports:
    - "${RAG_API_PORT:-8010}:8010"
  networks:
    - default
    - tidb_net

rag-worker:
  build:
    context: ./app
    dockerfile: Dockerfile
  env_file:
    - .env
  environment:
    APP_ROLE: worker
  depends_on:
    - qdrant
    - minio
  ports:
    - "${RAG_WORKER_PORT:-8011}:8011"
  networks:
    - default
    - tidb_net
```

### 例：external network（Linux 常見）
```yaml
networks:
  tidb_net:
    external: true
    name: tidb-docker-compose_default
```

如果原 TiDB compose network 名不同，要改成實際名稱。

---

## 3. TiDB 連線注意事項

### 情境 A：同 network，可用 service/container name
```env
TIDB_HOST=tidb
```
或：
```env
TIDB_HOST=tidb-docker-compose-tidb-1
```

### 情境 B：使用 host.docker.internal
只在某些環境可行：
```env
TIDB_HOST=host.docker.internal
```

如果 timeout，優先改 shared Docker network，不要硬撐。

---

## 4. Embedding / Collection 切換注意事項

這是最容易踩坑的地方。

### 原則
**Qdrant collection 的向量維度，必須和 embedding model 的維度一致。**

例如：
- `mock-384` → `EMBEDDING_DIMENSIONS=384`
- `text-embedding-3-small` → `EMBEDDING_DIMENSIONS=1536`

如果你改了 embedding model，但 collection 還是舊維度，就會出現：
- ingest 失敗
- search 失敗
- vector dimension mismatch

### 安全切換方法

#### 方法 A：直接重建 collection
適合：
- 舊資料可丟
- 測試環境

流程：
1. 改 `.env`
2. 刪掉舊 collection
3. 重建 `rag-api` / `rag-worker`
4. 重新 ingest 文件

刪除 collection 範例：
```bash
curl -X DELETE http://127.0.0.1:6333/collections/document_chunks
```

#### 方法 B：換新 collection 名稱
適合：
- 想保留舊資料
- 想做平滑切換

例如：
```env
QDRANT_COLLECTION=document_chunks_v2
EMBEDDING_DIMENSIONS=1536
```

然後重建 API / worker，再重新 ingest。

### 建議
- **測試環境**：直接重建 collection
- **想保留舊資料**：改 collection 名稱

---

## 5. Mock → 真 embedding 的建議流程

### Step 1：先用 mock 驗證流程
確認：
- upload 可用
- ingest 可用
- search 可用
- reindex / delete 可用

### Step 2：切 OpenAI-compatible
改 `.env`：
```env
EMBEDDING_PROVIDER=openai-compatible
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_API_KEY=...
EMBEDDING_DIMENSIONS=1536
```

### Step 3：重建 collection
- 刪掉舊 collection，或改新 collection 名稱

### Step 4：重建服務
```bash
cd /home/hom/services/rag-stack
docker compose up -d --build rag-api rag-worker
```

### Step 5：重新 ingest
舊的 mock vectors 不要留著混用。

---

## 6. 服務重建指令

### 重建 API / worker
```bash
cd /home/hom/services/rag-stack
docker compose up -d --build rag-api rag-worker
```

### 全部重建
```bash
cd /home/hom/services/rag-stack
docker compose up -d --build
```

---

## 7. 驗證指令

### health
```bash
curl http://127.0.0.1:8010/health
curl http://127.0.0.1:8011/health
```

### upload
```bash
curl -X POST http://127.0.0.1:8011/upload \
  -F 'document_id=doc-md-1' \
  -F 'title=Markdown 測試文件' \
  -F 'source_type=upload' \
  -F 'file=@./example.md;type=text/markdown'
```

### search
```bash
curl -X POST http://127.0.0.1:8010/search \
  -H 'content-type: application/json' \
  -d '{
    "query":"OpenAI embedding",
    "limit":5,
    "source_type":"upload",
    "hybrid":true
  }'
```

### list documents
```bash
curl 'http://127.0.0.1:8010/documents?status=active'
```

### document detail
```bash
curl http://127.0.0.1:8010/documents/doc-md-1
```

---

## 8. 常見誤區

### 誤區 1：TiSpark = retrieval engine
不是。TiSpark 偏 batch / ETL / analysis。

### 誤區 2：mock embedding 搜尋排不好 = 架構有問題
不一定。先看是不是還沒切真 embedding。

### 誤區 3：改 model 不用重建 collection
錯。維度不同時一定要重建或改 collection 名。

### 誤區 4：parser 改好了，舊資料會自動變乾淨
不會。要 `reindex`。

### 誤區 5：PDF 沒 page_no 只是 search 問題
通常是 parser / reindex 沒跟上。
