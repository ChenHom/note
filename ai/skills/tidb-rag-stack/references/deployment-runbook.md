# Deployment Runbook

## 1. Inspect Existing TiDB Stack
Confirm the existing Docker deployment is a TiDB base layer:
- `tidb`
- `tikv*`
- `pd*`
- optional: `tispark*`, `grafana`, `prometheus`

Decision:
- Good as metadata/data base layer
- Not yet a full RAG retrieval stack

## 2. Create Separate Project
Recommended path:
- `/home/hom/services/rag-stack`

Keep it separate from the existing `tidb-docker-compose` project.

## 3. Add Minimal Services
- `qdrant`
- `minio`
- `rag-api`
- `rag-worker`

## 4. Fix Docker Networking
If `host.docker.internal` does not work on Linux:
- attach `rag-api` and `rag-worker` to the same Docker network as TiDB
- use TiDB service/container name as `TIDB_HOST`

## 5. Create TiDB Schema
Required tables:
- `documents`
- `document_chunks`
- `retrieval_logs`

Important fields to keep:
- `object_key`
- `qdrant_point_id`
- `section_title`
- `page_no`

## 6. Start with Mock Embeddings
Use mock embeddings first to verify:
- health endpoints
- ingest flow
- search flow
- metadata writes

Do not judge ranking quality while still on mock embeddings.

## 7. Switch to Real Embeddings
Example `.env` fields:
- `EMBEDDING_PROVIDER=openai-compatible`
- `EMBEDDING_MODEL=text-embedding-3-small`
- `EMBEDDING_BASE_URL=https://api.openai.com/v1`
- `EMBEDDING_API_KEY=...`
- `EMBEDDING_DIMENSIONS=1536`

If dimensions change:
- rebuild collection
or
- use a new collection name

## 8. Validate End-to-End
### Upload / ingest
- plain text
- markdown
- html
- pdf

### Search
Confirm:
- metadata present
- snippet present
- `section_title` for md/html
- `page_no` for pdf

### Management APIs
Confirm:
- list
- detail
- reindex
- delete

## 9. Common Failure Modes
- Docker CLI unavailable in current runtime
- `host.docker.internal` timeout
- invalid Qdrant point ID
- collection already exists (409)
- embedding dimension mismatch
- parser upgraded but old chunks not reindexed

## 10. Ready State
The stack is considered ready when:
- uploads work
- searches return relevant results with metadata
- TiDB/Qdrant/MinIO stay in sync for reindex/delete
