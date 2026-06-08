# Reserve Orders 預收券款

For stocks under trading restrictions (處置股, 注意股, 警示股, 管理股), you must reserve funds or shares before placing orders.
現貨觸發注意股、警示股、處置股、管理股等交易異常條件時，下單前需先進行預收券款。

Service hours: **8:00 - 14:30** on trading days.
服務時間為交易日 **8:00 至 14:30**。

---

## Earmarking Cash 預收款項 (Buy 買進)

When buying restricted stocks, you must reserve cash (pre-pay funds).
買進處置/警示商品時，需先預收券款（圈存資金）。

### 1. Python SDK

```python
import shioaji as sj

api = sj.Shioaji()
api.login(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")
api.activate_ca(ca_path="Sinopac.pfx", ca_passwd="YOUR_CA_PASSWORD")

contract = api.Contracts.Stocks["1217"]

# Apply Earmarking (Buy)
# Note: First argument is contract, not account!
resp = api.reserve_earmarking(
    contract=contract,
    share=1000,
    price=9.0,
    account=api.stock_account
)
print(resp.response.status) # True if successful
```

### 2. HTTP REST Endpoint

`POST /api/v1/order/reserve_earmarking`
```json
{
  "contract": {
    "security_type": "STK",
    "exchange": "TSE",
    "code": "1217"
  },
  "share": 1000,
  "price": 9.0,
  "account": {
    "broker_id": "YOUR_BROKER_ID",
    "account_id": "YOUR_ACCOUNT_ID"
  }
}
```
**Response**:
```json
{
  "contract": {"security_type": "STK", "exchange": "TSE", "code": "1217", "target_code": ""},
  "account": {"account_type": "S", "person_id": "YOUR_PERSON_ID", "broker_id": "YOUR_BROKER_ID", "account_id": "YOUR_ACCOUNT_ID", "signed": true, "username": ""},
  "share": 1000,
  "price": 9.0,
  "status": true,
  "info": "OK"
}
```

---

## Querying Earmarking Details 查詢預收款項

Query active cash reservations and their status.
查詢已申請之預收款項明細：

### 1. Python SDK

```python
details = api.earmarking_detail(account=api.stock_account)

for stock in details.response.stocks:
    print(f"Code: {stock.contract.code} | Shares: {stock.share} | Price: {stock.price} | Status: {stock.info}")
```

### 2. HTTP REST Endpoint

`POST /api/v1/order/earmarking_detail`
```json
{
  "account": {
    "broker_id": "YOUR_BROKER_ID",
    "account_id": "YOUR_ACCOUNT_ID"
  }
}
```

---

## Reserving Stock 預收股票 (Sell 賣出)

When selling restricted stocks or holding short positions under special regimes, you must reserve shares first (圈券).
賣出處置股或進行融券相關操作時，需先申請預收股票（圈券）。

### 1. Python SDK

```python
contract = api.Contracts.Stocks["1217"]

# Apply Reserve Stock (Sell)
# Note: First argument is contract, not account!
resp = api.reserve_stock(
    contract=contract,
    share=1000,
    account=api.stock_account
)
print(resp.response.status) # True if successful
```

### 2. HTTP REST Endpoint

`POST /api/v1/order/reserve_stock`
```json
{
  "contract": {
    "security_type": "STK",
    "exchange": "TSE",
    "code": "1217"
  },
  "share": 1000,
  "account": {
    "broker_id": "YOUR_BROKER_ID",
    "account_id": "YOUR_ACCOUNT_ID"
  }
}
```

---

## Querying Reserve Stock Status 查詢預收股票狀態

### 1. Summary (可預收券總量與已預收量)

Query available and reserved shares for your stocks.
查詢名下持股可圈券額度與已圈券數量：

*   **Python SDK**:
    ```python
    summary = api.stock_reserve_summary(account=api.stock_account)
    for stock in summary.response.stocks:
        print(f"Code: {stock.contract.code} | Available: {stock.available_share} | Reserved: {stock.reserved_share}")
    ```
*   **HTTP REST**: `POST /api/v1/order/stock_reserve_summary`
    ```json
    { "account": { "broker_id": "YOUR_BROKER_ID", "account_id": "YOUR_ACCOUNT_ID" } }
    ```

### 2. Detail (預收股票明細)

Query detailed logs of reserved stock submissions.
查詢預收股票的圈券審核明細與執行進度：

*   **Python SDK**:
    ```python
    detail = api.stock_reserve_detail(account=api.stock_account)
    for s in detail.response.stocks:
        print(f"Code: {s.contract.code} | Share: {s.share} | Date: {s.order_datetime} | Status: {s.info}")
    ```
*   **HTTP REST**: `POST /api/v1/order/stock_reserve_detail`
    ```json
    { "account": { "broker_id": "YOUR_BROKER_ID", "account_id": "YOUR_ACCOUNT_ID" } }
    ```

---

## Application: Auto-Reserve All Available 批次預收股票

Example of querying all stock accounts and automatically reserving all available shares:
自動查詢名下所有證券帳號的圈券狀態，將可圈額度全數申請預收股票：

```python
import shioaji as sj

api = sj.Shioaji()
api.login(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")
api.activate_ca(ca_path="Sinopac.pfx", ca_passwd="YOUR_CA_PASSWORD")

for account in api.list_accounts():
    if account.account_type == sj.AccountType.Stock:
        summary = api.stock_reserve_summary(account=account)
        for s in summary.stocks:
            if s.available_share > 0:
                api.reserve_stock(
                    contract=s.contract, 
                    share=s.available_share, 
                    account=account
                )
                print(f"Reserved {s.contract.code}: {s.available_share} shares.")
```
