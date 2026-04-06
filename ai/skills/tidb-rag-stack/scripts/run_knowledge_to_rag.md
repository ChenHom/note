# Run Knowledge to RAG

這個一條龍 helper script 會做：
1. 讀整理好的知識檔
2. 拆 chunks
3. 生成 payload JSON
4. 直接寫到 `/ingest`
5. 再用 `/documents/{id}` 驗證
6. 若有提供 query，再補一次 `/search` 驗證

## Script
- `scripts/run_knowledge_to_rag.py`

## Example
```bash
python3 scripts/run_knowledge_to_rag.py \
  --input ./knowledge.md \
  --document-id telegram-tidb-rag-knowledge-2026-03-31 \
  --title "TiDB-based 自架 RAG 核心知識整理" \
  --source-type telegram-summary \
  --source-uri "telegram://meeting-room/2026-03-31/tidb-rag-stack" \
  --worker-base http://127.0.0.1:8011 \
  --api-base http://127.0.0.1:8010 \
  --query "Qdrant collection 維度" \
  --output-dir ./out
```

## Output
會輸出：
- `payload_path`
- `write_result`
- `verify.document_detail`
- `verify.search_result`（若有 query）
