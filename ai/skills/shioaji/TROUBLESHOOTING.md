# Troubleshooting 常見問題與解決方案

This document lists common issues, error messages, and solutions when working with the Shioaji API.
本文件整理使用 Shioaji API 時常遇到的問題、錯誤訊息與對應的排解方法。

---

## 1. Orders 下單相關問題

### Q1: How do I place Market (MKT) or Range Market (MKP) orders? (如何下市價單或範圍市價單？)
*   **Cause**: Market/Range Market orders do not accept a custom price (must set `price=0`) and only support `IOC` or `FOK` order types.
    市價或範圍市價單不得自訂價格（必須設價格為 0），且委託條件僅接受 `IOC` 或 `FOK`。
*   **Solution**:
    ```python
    import shioaji as sj
    
    order = sj.StockOrder(
        action=sj.Action.Buy,
        price=0,                               # Must be 0 for MKT/MKP
        quantity=1,
        price_type=sj.StockPriceType.MKT,      # Or StockPriceType.MKP
        order_type=sj.OrderType.IOC,           # Must be IOC or FOK
        account=api.stock_account
    )
    trade = api.place_order(contract, order)
    ```

### Q2: How do I place limit up/down orders? (如何掛漲跌停板價委託？)
*   **Solution**: Retrieve the limit values dynamically from the contract object.
    應自合約物件動態取得當日漲跌停價：
    ```python
    contract = api.Contracts.Stocks["2330"]
    
    # Limit Up (漲停)
    price_up = contract.limit_up
    # Limit Down (跌停)
    price_down = contract.limit_down
    ```

---

## 2. Streaming 行情相關問題

### Q3: Why does my quote stream terminate after receiving a few lines? (為什麼行情串流接收幾筆就沒了？)
*   **Cause**: When running scripts from the CLI or terminal (e.g. `python stream.py`), the script finishes executing and exits immediately, which closes the Solace stream.
    直接於終端機執行腳本時，若執行完訂閱後即結束腳本，則 Solace 串流會隨主程式結束而被強制關閉。
*   **Solution**: Keep the main thread alive using `Event().wait()` or a loop.
    使用執行緒事件阻塞主程式使其常駐運行：
    ```python
    import shioaji as sj
    from threading import Event
    
    api = sj.Shioaji()
    api.login(api_key="YOUR_KEY", secret_key="YOUR_SECRET")
    
    # Register callback and subscribe...
    api.subscribe(api.Contracts.Stocks["2330"], quote_type=sj.QuoteType.Tick)
    
    # Wait and keep alive
    Event().wait()
    ```

---

## 3. Account & Login 帳戶與登入問題

### Q4: "Account not acceptable" Error (帳戶無法使用)
*   **Cause 1**: You have not signed the API Trading Terms of Service or completed the simulation trading quiz.
    尚未至永豐金理財網完成 API 條款簽署或模擬測試審核。
*   **Cause 2**: `api.update_status()` is called without specifying an account. By default, it queries all accounts under your Person ID. If any of those accounts are unsigned, it throws this error.
    `update_status()` 預設會查詢旗下所有帳號，若其中一個帳號未簽署即會報錯。
*   **Solution**: Specify the account explicitly:
    指定具體已簽署之帳號進行查詢：
    ```python
    api.update_status(account=api.stock_account)
    ```

### Q5: "Sign data is timeout" Error (登入簽章逾時)
*   **Cause 1**: Your system clock is out of sync with the SinoPac servers.
    您的系統時間與伺服器時間誤差過大。
*   **Cause 2**: The network delay exceeds the `receive_window` parameter.
    登入連線時間超過了限制。
*   **Solution**:
    1. Synchronize your system clock using NTP. (校準系統時間)
    2. Increase the `receive_window` during login:
       ```python
       api.login(
           api_key="YOUR_API_KEY",
           secret_key="YOUR_SECRET_KEY",
           receive_window=60000 # Increase to 60 seconds (default 30,000ms)
       )
       ```

---

## 4. Environment & Paths 環境與路徑問題

### Q6: How do I change the log file path or location? (如何變更日誌檔路徑？)
*   **Solution**: Define the `SJ_LOG_PATH` environment variable **before** importing the shioaji package.
    在導入 shioaji 模組之前設定 `SJ_LOG_PATH` 環境變數：
    ```python
    import os
    os.environ["SJ_LOG_PATH"] = "/path/to/my_shioaji.log"
    
    import shioaji as sj
    ```
    Or in shell:
    ```bash
    export SJ_LOG_PATH=/path/to/my_shioaji.log
    ```

### Q7: How do I change the contracts cache download path? (如何自訂商品合約下載快取路徑？)
*   **Solution**: Set the `SJ_CONTRACTS_PATH` environment variable before importing:
    ```python
    import os
    os.environ["SJ_CONTRACTS_PATH"] = "/path/to/my_contracts_folder"
    
    import shioaji as sj
    ```

---

## 5. Rate Limits 流量與次數限制

To protect system integrity, Shioaji enforces strict rate limits. Violations may result in connection blocks for 1 minute or IP suspension.
為避免過大負載，API 設有流量與頻率限制，違規將被暫停服務 1 分鐘甚至封鎖 IP。

| Category 類別 | Limit 限制 | Mitigation 解決方案 |
| --- | --- | --- |
| **Quote Query 行情查詢** | 50 requests / 5 seconds | Use callbacks (`api.subscribe`) instead of polling `api.ticks` or `api.snapshots`. |
| **Accounting 帳務查詢** | 25 requests / 5 seconds | Cache position arrays or limit balance queries to a timer (e.g. once every 10s). |
| **Order Commands 委託下單** | 250 requests / 10 seconds | Use non-blocking mode (`timeout=0`) when executing batch orders. |
| **Connections 連線數** | 5 concurrent per Person ID | Explicitly call `api.logout()` when closing a process to release slots. |
| **Logins 登入次數** | 1000 times / day | Keep connection alive instead of calling `login()` inside short-lived scripts. |
