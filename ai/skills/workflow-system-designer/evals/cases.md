# Eval Cases

## Positive Case 1
使用者有一堆零散 prompts，想整理成一套可維護的 workflow system。
應輸出：core / add-on / connector / deliverable 分層。

## Positive Case 2
使用者想把某個專業流程拆成 core + add-on + connector。
應輸出：清楚邊界與 phased plan。

## Positive Case 3
使用者已經寫了很多內容筆記，但還沒釐清哪些是系統層，哪些只是內容層。
應輸出：content layer vs system layer 的分離建議。

## Negative Case 1
使用者只想改一個 prompt 或 command 描述。
不應觸發這個 skill。

## Negative Case 2
使用者要的是完整 benchmark / blind comparison。
應改用 skill-evaluator，而不是本 skill。

## Edge Case 1
使用者同時要：workflow 設計、connector 實作、production integration。
應先收斂出 phase 1 系統設計，再把 integration 切出去。

## Common Fail Clusters
- 把內容知識當成系統設計
- 忘了 deliverable layer
- 把 connector 問題混進 workflow 方法論
- core / add-on 切不清
- phase 1 過胖
