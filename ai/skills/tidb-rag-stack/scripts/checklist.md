# Deployment / Detection Checklist

## A. Deployment
- [ ] Existing TiDB stack confirmed
- [ ] rag-stack project directory created
- [ ] qdrant / minio / rag-api / rag-worker added
- [ ] TiDB schema created
- [ ] `.env` configured for embedding provider
- [ ] Qdrant collection dimension matches embedding dimension
- [ ] upload works
- [ ] search works
- [ ] metadata join works
- [ ] retrieval_logs writes
- [ ] reindex works
- [ ] delete works
- [ ] Markdown / HTML section titles verified
- [ ] PDF page numbers verified

## B. Live Stack Detection
- [ ] live project path confirmed
- [ ] compose services confirmed
- [ ] `.env` key settings confirmed
- [ ] schema confirmed
- [ ] app endpoints confirmed from live code
- [ ] preferred write path selected (`/ingest` / `/upload` / internal app)

## C. Knowledge Write
- [ ] source knowledge cleaned up before writing
- [ ] chunks prepared with clear topic boundaries
- [ ] metadata prepared (`document_id`, `title`, `source_type`, `source_uri`, `mime_type`)
- [ ] write response checked
- [ ] `/documents` or `/documents/{id}` verified
- [ ] `/search` verification done when needed
