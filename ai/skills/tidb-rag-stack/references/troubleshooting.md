# Troubleshooting

## `docker` not found
You are not on the target host or the runtime cannot access Docker CLI.

## `host.docker.internal` timed out
On Linux, put `rag-api` / `rag-worker` on the same Docker network as TiDB and use the TiDB service/container name.

## Qdrant point ID invalid
Use unsigned integer or UUID, not strings like `doc-1:0`.

## Qdrant 409 collection exists
Make collection creation idempotent or ignore 409 on startup.

## Embedding dimension mismatch
If you switch embedding provider/model, rebuild the Qdrant collection or use a new collection name.

## Search ranking looks wrong
Check whether you're still on mock embeddings. Verify `.env` for provider/model/dimensions.

## HTML results too noisy
Reindex after parser changes so old chunks are replaced.

## PDF works but no page info
Ensure page-aware parsing is active and reindex PDF after upgrading parser.

## TiDB write fails
Check network reachability between rag services and TiDB; confirm schema exists.
