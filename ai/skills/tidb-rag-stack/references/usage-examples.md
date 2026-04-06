# Usage Examples

## Check TiDB Docker stack readiness
- Look for `tidb`, `tikv*`, `pd*`
- Confirm this is a data base layer, not a complete RAG retrieval stack

## Build the stack
Typical files:
- `/home/hom/services/rag-stack/docker-compose.yml`
- `/home/hom/services/rag-stack/.env`
- `/home/hom/services/rag-stack/sql/001_init.sql`

## Bring services up
```bash
cd /home/hom/services/rag-stack
docker compose up -d --build
```

## Upload Markdown
```bash
curl -X POST http://127.0.0.1:8011/upload \
  -F 'document_id=doc-md-1' \
  -F 'title=Markdown 測試文件' \
  -F 'source_type=upload' \
  -F 'file=@./example.md;type=text/markdown'
```

## Search
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

## List documents with filters
```bash
curl 'http://127.0.0.1:8010/documents?source_type=upload&mime_type=text/markdown&title_contains=測試&status=active'
```

## Reindex document
```bash
curl -X POST http://127.0.0.1:8010/documents/doc-md-1/reindex \
  -H 'content-type: application/json' \
  -d '{"chunk_size":500,"chunk_overlap":50}'
```

## Delete document
```bash
curl -X DELETE http://127.0.0.1:8010/documents/doc-md-1
```

## PDF upload
```bash
curl -X POST http://127.0.0.1:8011/upload \
  -F 'document_id=doc-pdf-1' \
  -F 'title=PDF 測試文件' \
  -F 'source_type=upload' \
  -F 'file=@./example.pdf;type=application/pdf'
```
