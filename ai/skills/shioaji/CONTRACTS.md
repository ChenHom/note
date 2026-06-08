# Contracts 商品合約

This document covers how to access, search, and parse contract objects in Shioaji.
本文件說明如何在 Shioaji 中查詢與解析合約物件。

---

## Overview 概覽

Contracts are daily market metadata (stocks, futures, options, indices) required for placing orders and subscribing to quotes.
合約包含每日市場商品之基本資料（證券、期貨、選擇權、指數），是下單與訂閱行情所必需的。

**Daily Update Schedule 商品檔每日更新時間**:
- **07:50** - Futures contracts update 期貨商品檔更新
- **08:00** - All markets contracts update 全市場商品檔更新
- **14:45** - Futures night-session contracts update 期貨夜盤商品檔更新
- **17:15** - Futures night-session contracts update 期貨夜盤商品檔更新

---

## Fetching Contracts 取得商品檔

By default, contracts are downloaded during login. You can control this behavior or manually fetch them.
預設情況下，登入時會自動下載商品檔。您也可以控制是否自動下載或進行手動更新：

```python
import shioaji as sj

api = sj.Shioaji()

# Method 1: Download during login (default)
# 方法 1：登入時同步下載（設定 contracts_timeout 等待毫秒）
api.login(
    api_key="YOUR_API_KEY",
    secret_key="YOUR_SECRET_KEY",
    contracts_timeout=10000, 
)

# Check download status
# 檢查商品檔下載進度
print(api.Contracts.status)

# Method 2: Manual download after login
# 方法 2：登入時不下載，之後手動更新
api.login(
    api_key="YOUR_API_KEY",
    secret_key="YOUR_SECRET_KEY",
    fetch_contract=False,
)
api.fetch_contracts(contract_download=True)
```

---

## Contract Object Attributes 商品檔屬性

The attributes of a contract object (SDK representation of `Stock`, `Future`, `Option`, or `Index`):
商品合約物件所支援的屬性欄位如下：

| Attribute 屬性 | Type 類型 | Description 說明 |
| --- | --- | --- |
| `security_type` | `str` | Security type 商品類型: `STK`, `FUT`, `OPT`, `IND` |
| `exchange` | `str` | Exchange 交易所 (e.g., `TSE`, `OTC`, `TAIFEX`) |
| `code` | `str` | Code 商品代碼 (e.g., `"2330"`, `"TXFR1"`) |
| `symbol` | `str` | Symbol 符號 (e.g., `"TSE2330"`) |
| `name` | `str` | Name 商品名稱 (e.g., `"台積電"`) |
| `category` | `str` | Category 產業別或商品類別 (e.g., `"24"`) |
| `currency` | `str` | Currency 計價幣別 (e.g., `"TWD"`) |
| `unit` | `float` | Unit 交易單位 (e.g., `1000.0` shares for stock) |
| `limit_up` | `float` | Limit Up price 漲停價 |
| `limit_down` | `float` | Limit Down price 跌停價 |
| `reference` | `float` | Reference price 昨日收盤/昨收參考價 |
| `update_date` | `str` | Update date 更新日期 (e.g., `"2026/05/14"`) |
| `day_trade` | `str` / `enum` | Day trade eligibility 可否當沖: `Yes`, `No`, `OnlyBuy` |
| `margin_trading_balance` | `int` | Margin balance 融資餘額 (STK) |
| `short_selling_balance` | `int` | Short balance 融券餘額 (STK) |
| `delivery_month` | `str` | Delivery month 交割月份 (FUT/OPT) |
| `delivery_date` | `str` | Delivery date 結算日 (FUT/OPT) |
| `strike_price` | `float` | Strike price 履約價 (OPT) |
| `option_right` | `str` / `enum` | Option right 買賣權別: `Call` / `Put` (OPT) |
| `underlying_kind` | `str` | Underlying kind 標的類型 (FUT/OPT) |
| `underlying_code` | `str` | Underlying code 標的商品代碼 (OPT) |
| `multiplier` | `int` | Multiplier 契約乘數 (FUT/OPT) |
| `target_code` | `str` | Target contract code for continuous contracts (e.g., Continuous near month continuous targets `TXFE6` for `TXFR1`) (FUT) |

---

## Querying Contracts in Python

### 1. Stocks 證券

```python
# Query by code directly
tsmc = api.Contracts.Stocks["2330"]

# List all stocks under TSE or OTC
tse_stocks = list(api.Contracts.Stocks.TSE)
otc_stocks = list(api.Contracts.Stocks.OTC)
```

### 2. Futures 期貨

For expired/continuous historical data, Shioaji provides continuous contracts: `R1` (near-month continuous) and `R2` (next-month continuous).
針對已過期/連續歷史資料，Shioaji 提供連續契約：`R1` (近月連續) 與 `R2` (次近月連續)。

```python
# Specific futures contract
txf_202606 = api.Contracts.Futures["TXF202606"]

# Continuous near-month contract
txf_near = api.Contracts.Futures["TXFR1"]  # Target maps to specific code (e.g. TXFE6)

# List all futures under a category
all_txf = list(api.Contracts.Futures.TXF)
```

### 3. Options 選擇權

```python
# List all TXO option contracts
txo_options = list(api.Contracts.Options.TXO)

# Filter Call options at specific strike and expiry
calls_44000 = [
    c for c in txo_options 
    if c.delivery_month == "202606" 
    and c.strike_price == 44000 
    and c.option_right == sj.OptionRight.Call
]
```

### 4. Indices 指數

```python
# Get Taiwan Weighted Index
weighted_idx = api.Contracts.Indexs.TSE["001"] # Or api.Contracts.Indexs.TSE.TSE001
```

---

## Querying Contracts via HTTP API

Other language users can fetch contract specifications by making a `GET` request to the local HTTP server.
其他語言使用者可透過對本地伺服器發送 `GET` 請求取得合約內容。

**URL Format**: `GET /api/v1/data/contracts/{code}?security_type=<TYPE>`
- `{code}`: Contract code (e.g. `2330`, `TXFR1`).
- `security_type`: Product type (`STK`, `FUT`, `OPT`, `IND`).

### Examples:

#### Stock (STK)
```bash
curl "http://localhost:8080/api/v1/data/contracts/2330?security_type=STK"
```
**Response**:
```json
{
  "security_type": "STK",
  "exchange": "TSE",
  "code": "2330",
  "symbol": "TSE2330",
  "name": "台積電",
  "category": "24",
  "currency": "TWD",
  "delivery_month": "",
  "delivery_date": "",
  "strike_price": 0.0,
  "option_right": "",
  "underlying_kind": "",
  "underlying_code": "",
  "unit": 1000.0,
  "multiplier": 0,
  "limit_up": 2440.0,
  "limit_down": 2000.0,
  "reference": 2220.0,
  "update_date": "2026/05/14",
  "margin_trading_balance": 167,
  "short_selling_balance": 0,
  "day_trade": "Yes",
  "target_code": ""
}
```

#### Futures (FUT)
```bash
curl "http://localhost:8080/api/v1/data/contracts/TXFR1?security_type=FUT"
```
**Response**:
```json
{
  "security_type": "FUT",
  "exchange": "TAIFEX",
  "code": "TXFR1",
  "symbol": "TXFR1",
  "name": "臺股期貨近月",
  "category": "TXF",
  "currency": "TWD",
  "delivery_month": "202605",
  "delivery_date": "2026/05/20",
  "strike_price": 0.0,
  "option_right": "",
  "underlying_kind": "I",
  "underlying_code": "",
  "unit": 1.0,
  "multiplier": 0,
  "limit_up": 45799.0,
  "limit_down": 37473.0,
  "reference": 41636.0,
  "update_date": "2026/05/15",
  "margin_trading_balance": 0,
  "short_selling_balance": 0,
  "day_trade": "",
  "target_code": "TXFE6"
}
```

---

## Best Practices 最佳實踐

1. **Verify Limit Prices Before Placing Orders**:
   Always retrieve `limit_up` and `limit_down` dynamically from the contract object rather than hardcoding them, as they change daily.
   下單限價單或市價單時，應動態取得 `limit_up` 或 `limit_down`，避免寫死數值。
2. **Speed Up Login**:
   If you only query accounts or do not need contract references, set `fetch_contract=False` during login to save bandwidth and decrease startup delay.
   如果登入不需要使用完整的商品合約檔，設定 `fetch_contract=False` 以加速初始化。
