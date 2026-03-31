# Anti-Patterns

## 1. 把內容知識當成系統設計
症狀：寫了很多 domain 筆記，但沒有 core / add-on / connector / deliverable 分層。

## 2. 忘了 deliverable layer
症狀：只談 workflow 與資料來源，卻沒有定義最後交付物。

## 3. 把 connector 寫死
症狀：workflow 與特定資料源綁死，日後無法替換或降級。

## 4. Phase 1 過胖
症狀：一開始就想把所有未來需求都做進第一版。

## 5. 只有框架，沒有收斂
症狀：寫了很多設計原則，但最後沒有產出 scope card、map、phase plan。

## 6. Core / Add-on 切不清
症狀：共享能力與場景專屬能力混在一起，導致維護成本暴增。
