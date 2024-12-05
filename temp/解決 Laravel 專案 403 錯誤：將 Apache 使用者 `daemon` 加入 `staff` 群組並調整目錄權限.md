**解決 Laravel 專案 403 錯誤：將 Apache 使用者 `daemon` 加入 `staff` 群組並調整目錄權限**

權限錯誤的問題總結如下：

---

### 問題描述
訪問 Laravel 專案時，伺服器返回 `403 Forbidden` 錯誤，Apache 錯誤日誌顯示：
```plaintext
Permission denied: access to / denied (filesystem path '/Users/hom/code')
```
此錯誤是由於 Apache 使用者 `daemon` 無法存取專案所在目錄 `/Users/hom/code` 及其上層目錄，缺少目錄的「搜尋權限」（執行權限 `x`）。

---

### 解決方案
1. **確認 Apache 使用者**：
   使用 `ps aux | grep httpd` 確認 Apache 的執行使用者為 `daemon`。

2. **確認目錄權限與群組**：
   - 使用 `groups hom` 確認 `hom` 使用者的群組為 `staff`。
   - 使用 `ls -ld` 檢查專案目錄及其上層目錄的權限。

3. **將 `daemon` 加入 `staff` 群組**：
   - 使用以下命令將 `daemon` 加入 `staff` 群組：
     ```bash
     sudo dseditgroup -o edit -a daemon -t user staff
     ```
   - 確認 `daemon` 已成功加入：
     ```bash
     groups daemon
     ```

4. **調整目錄權限**：
   為目錄 `/Users/hom/code` 及其上層目錄新增執行權限，讓 `staff` 群組成員可以存取：
   ```bash
   sudo chmod -R 770 /Users/hom/code
   ```

5. **重啟 Apache**：
   變更完成後，重新啟動 Apache：
   ```bash
   sudo apachectl restart
   ```

---

### 結果
完成上述操作後，`daemon` 使用者成功獲取專案目錄的訪問權限，問題解決，Laravel 專案可以正常運行。

---
