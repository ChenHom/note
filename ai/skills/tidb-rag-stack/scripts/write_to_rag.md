# Write to RAG

這個 helper script 用來把已準備好的 ingest payload 直接送到 live rag-worker。

## Script
- `scripts/write_to_rag.py`

## Input
- `--payload <json file>`
- `--worker-base <url>`，預設 `http://127.0.0.1:8011`

## Example
```bash
python3 scripts/write_to_rag.py \
  --payload ./telegram-tidb-rag-knowledge-2026-03-31.payload.json \
  --worker-base http://127.0.0.1:8011
```

## Output
- 直接印出 `/ingest` response
