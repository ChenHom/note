# Detect Live RAG Stack

當使用者要確認現場是不是已經有可用的 rag-stack，請照這份腳本化流程執行。

## Goal
找出：
- 專案路徑
- compose services
- `.env` 關鍵設定
- schema 是否存在
- app code 中真的有哪些 endpoint
- 實際可用的寫入入口

## Steps
1. 找常見路徑，例如：
   - `/home/hom/services/rag-stack`
   - 使用者明講的 repo/path

2. 讀 `docker-compose.yml`
   - 確認 `qdrant`、`minio`、`rag-api`、`rag-worker`
   - 記下 ports、network、container_name、env_file

3. 讀 `.env`
   - 找 `RAG_API_PORT`、`RAG_WORKER_PORT`
   - 找 `TIDB_HOST`、`QDRANT_COLLECTION`
   - 找 `EMBEDDING_PROVIDER`、`EMBEDDING_DIMENSIONS`
   - 若含敏感值，不要回貼

4. 讀 schema
   - 確認 `documents`、`document_chunks`、`retrieval_logs`

5. 讀 app code
   - 檢查是否真的有：
     - `POST /ingest`
     - `POST /upload`
     - `POST /search`
     - `GET /documents`
     - `GET /documents/{id}`
     - `POST /documents/{id}/reindex`
     - `DELETE /documents/{id}`

6. 形成結論
   - 現場是否真的有 live rag-stack
   - 可用寫入入口是什麼
   - payload 應參考哪個 request model
   - 若 skill 文件和 live code 不一致，以 live code 為準

## Output Format
建議回報：
- project path
- detected services
- detected endpoints
- preferred write path
- warnings

## Warnings
- 不要只根據 `references/api-contract.md` 就說 endpoint 一定存在
- 不要暴露 `.env` 的 secrets
