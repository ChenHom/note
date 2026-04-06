# Architecture

## Recommended Layout

- Existing TiDB stack stays where it is
- New project lives separately, e.g. `/home/hom/services/rag-stack`

### Roles
- TiDB: metadata, chunks, retrieval logs
- Qdrant: vector search
- MinIO: original files
- rag-worker: upload / parse / chunk / embed / ingest
- rag-api: query / filters / metadata join / docs management

## Why not TiSpark as retrieval core?
TiSpark is useful for batch analysis and ETL, not for query-time semantic retrieval.

## Minimal Service Set
- qdrant
- minio
- rag-api
- rag-worker

## Data Flow
1. Upload file to MinIO
2. Parse into text
3. Chunk text
4. Generate embeddings
5. Upsert vectors to Qdrant
6. Write metadata/chunks/logs to TiDB
7. Query via rag-api with optional filters
