# Disk Cache Eviction

這是在閱讀 [Discord 如何處理一天數億的訊息](https://tachunwu.github.io/posts/discord-cassandra/?fbclid=IwAR0Kafo0LEdqflpMGRRWPk7ZX-9ESI9uOdjTNqZk1zE5DA69jQ5VKDs6Crc) 時所出現的疑惑。

什麼是 `Disk Cache Eviction` ，講簡單點就是資料更新。進行記憶體內的快取資料更新。

以較新形式的 `NoSql` 或 `In-memory` 資料庫會將整個資料存放在記憶體中加快存取速度。

當記憶體無法存放下所有的資料時，會將當前使用的資料放在記憶體中，暫時不用的放在硬碟。一旦讀取到不在記憶體中的資料時，作業系統就會開始對虛擬記憶體作分頁，這時存取主憶體會導致頁面錯誤，因為頁面錯誤透明[^1]給用戶的。在這種情況下會從硬碟中獲取頁面然後事務會停止之後頁面取回，這就會產生效能問題。

---

Reference:

[Anti-Caching: A New Approach to
Database Management System Architecture](https://www.vldb.org/pvldb/vol6/p1942-debrabant.pdf)

[Caching vs. Anti-Caching [缓存和反缓存]](https://csruiliu.github.io/blog/20161218-cache-vs-anticache/)

---

[^1]: 如果作業系統 (OS) 能夠在用戶不知情的情況下處理它們，則記憶體頁面錯誤對用戶來說是透明的。這是透過使用虛擬記憶體和分頁實現的，當程序訪問當前不在記憶體中的頁面時，作業系統會檢測到頁面錯誤並從硬碟中檢索該頁面。這個過程對用戶是透明的。
