# Eval Cases

## Happy Path
### Case 1: Existing TiDB stack is present
Expected:
- identify TiDB/TiKV/PD correctly
- recommend adding Qdrant/MinIO/rag-api/rag-worker
- do not call TiSpark the retrieval engine

### Case 1B: Existing live rag-stack is present
Expected:
- find the actual project path
- inspect compose, .env, schema, and app code
- confirm which endpoints really exist
- distinguish documented API contract from live implementation

### Case 2: Mock embedding bootstrap
Expected:
- stand up services
- validate ingest and search
- explain ranking quality limitations clearly

### Case 3: Real embedding cutover
Expected:
- detect dimension mismatch risk
- instruct rebuild/new collection
- validate improved ranking quality

## Parser / Chunking
### Case 4: Markdown upload
Expected:
- `section_title` populated
- search returns snippet, not raw giant chunk

### Case 5: HTML upload
Expected:
- `section_title` populated from headings
- noisy raw HTML not returned as-is after reindex

### Case 6: PDF upload
Expected:
- `page_no` populated
- search results include page number

## Failure Cases
### Case 7: `host.docker.internal` timeout
Expected:
- recommend shared Docker network
- switch to service/container name

### Case 8: Qdrant invalid point ID
Expected:
- recommend UUID or unsigned integer
- do not keep `doc-1:0` as point ID

### Case 9: Collection exists (409)
Expected:
- treat create as idempotent
- ignore or catch 409 safely

### Case 10: TiDB metadata missing after search
Expected:
- inspect schema and worker writes
- verify `documents` and `document_chunks`

## Knowledge Write Cases
### Case 11: User wants discussion notes written into RAG
Expected:
- first clean up and structure the knowledge
- find a real write path such as `POST /ingest`
- prepare a valid payload with metadata
- write successfully and report the result

### Case 12: Skill docs mention an endpoint but live code differs
Expected:
- trust live code and reachable endpoints over reference docs
- avoid claiming the skill can directly write without environment checks

## Misclassification Guardrails
### Case 13: User only asks for theory
Expected:
- explain architecture without forcing deployment steps

### Case 14: User wants heavy full-text search platform
Expected:
- note this skill is not for OpenSearch/Elasticsearch-first design
