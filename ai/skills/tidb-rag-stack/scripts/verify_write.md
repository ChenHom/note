# Verify RAG Write

知識寫進 RAG 後，不要只看寫入 response；還要做最小驗證。

## Goal
確認資料真的寫進 TiDB / Qdrant，且能被查到。

## Steps
1. 看寫入 response
   - 是否成功
   - `document_id` 是否正確
   - `ingested_chunks` 是否合理
   - 是否有 `tidb_written=true`

2. 用文件 API 驗證
   - `GET /documents`
   - `GET /documents/{id}`

3. 用搜尋 API 驗證
   - 用 chunk 內的關鍵詞查一次
   - 確認能回到該 document

4. 判斷結果
   - 如果寫入成功但查不到：檢查 search / metadata join / embedding 問題
   - 如果 TiDB 有資料但搜尋不到：檢查 Qdrant / embedding / collection
   - 如果搜尋命中但 metadata 不完整：檢查 schema / join / worker 寫入欄位

## Output Format
建議回報：
- write response summary
- document lookup result
- search verification result
- follow-up warnings
