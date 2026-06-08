---
name: shioaji
description: |
  Shioaji Taiwan financial trading API guide. Use when trading stocks/futures/options on Taiwan markets, subscribing to real-time market data, querying account info, or building automated trading systems.
  Shioaji 台灣金融交易 API 指南。適用於：股票/期貨/選擇權交易、即時行情訂閱、帳務查詢、自動交易系統開發。
---

# Shioaji Trading API

Shioaji is SinoPac Securities' Python API and cross-language trading platform for Taiwan financial markets (stocks, futures, options).
Shioaji 是永豐金證券提供的 Python 交易 API 與跨語言交易平台，支援台灣股票、期貨、選擇權市場。

**Official Docs 官方文檔**: https://sinotrade.github.io/
**LLM Reference**: https://sinotrade.github.io/llms-full.txt

---

## Navigation 功能導覽

| Topic 主題 | File 檔案 | Description 說明 |
|---|---|---|
| Preparation 準備 | [PREPARE.md](PREPARE.md) | Account setup, API keys, testing 開戶/金鑰申請/測試 |
| Contracts 合約 | [CONTRACTS.md](CONTRACTS.md) | Stocks, Futures, Options contracts 股票/期貨/選擇權合約 |
| Orders 下單 | [ORDERS.md](ORDERS.md) | Place, modify, cancel, combo orders 下單/改單/刪單/組合單 |
| Reserve 預收 | [RESERVE.md](RESERVE.md) | Reserve orders for disposition stocks 處置股預收券款 |
| Streaming 行情 | [STREAMING.md](STREAMING.md) | Real-time tick & bidask data 即時 Tick/BidAsk 資料 |
| Market Data 市場資料 | [MARKET_DATA.md](MARKET_DATA.md) | Historical, snapshot, credit, scanners 歷史資料/快照/資券/掃描器 |
| Accounting 帳務 | [ACCOUNTING.md](ACCOUNTING.md) | Balance, margin, P&L, trading limits 餘額/保證金/損益/額度 |
| Watchlist 自選股 | [WATCHLIST.md](WATCHLIST.md) | Custom stock lists management 自選股清單管理 |
| Advanced 進階 | [ADVANCED.md](ADVANCED.md) | Quote binding, non-blocking, stop orders 報價綁定/非阻塞/觸價 |
| Troubleshooting 問題排解 | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and solutions 常見問題與解決 |

---

## Quick Start 快速入門

### Installation 安裝

```bash
# pip
pip install shioaji

# uv (recommended 推薦)
uv add shioaji
```

### Login & Activate CA 登入與憑證啟用

In Shioaji 1.5+, everything is exported directly at the top level for cleaner imports.
在 Shioaji 1.5+ 中，所有模組類別與常數皆已導出至最上層，方便直接引用。

```python
import shioaji as sj

api = sj.Shioaji()

# Login with API Key 使用 API Key 登入
accounts = api.login(
    api_key="YOUR_API_KEY",
    secret_key="YOUR_SECRET_KEY"
)

# Activate CA certificate 啟用憑證 (required for placing orders 下單必須)
api.activate_ca(
    ca_path="/path/to/Sinopac.pfx",
    ca_passwd="YOUR_CA_PASSWORD",
)
```

### Simulation Mode 模擬模式

Test API without real money. 使用模擬環境測試 API。

```python
api = sj.Shioaji(simulation=True)
api.login(api_key="YOUR_KEY", secret_key="YOUR_SECRET")
```

**Available in simulation 模擬模式可用功能**:
- **Quote**: subscribe, unsubscribe, ticks, kbars, snapshots
- **Order**: place_order, update_order, cancel_order, update_status, list_trades
- **Account**: list_positions, list_profit_loss
- **Data**: short_stock_sources, credit_enquires, scanners

### Simple Order Example 簡單下單範例

```python
# Get contract 取得合約
contract = api.Contracts.Stocks["2330"]  # TSMC

# Create stock order 建立證券訂單
order = sj.StockOrder(
    price=580,
    quantity=1,
    action=sj.Action.Buy,
    price_type=sj.StockPriceType.LMT,
    order_type=sj.OrderType.ROD,
    account=api.stock_account,
)

# Place order 下單
trade = api.place_order(contract, order)
```

---

## Common Constants 常用常數

All submodules (constants, enums) are available directly on the top-level `shioaji` import.
常用的常數與列舉可直接在 `shioaji` 套件最上層存取：

### Action 買賣方向
```python
sj.Action.Buy   # 買進
sj.Action.Sell  # 賣出
```

### Stock Price Type 股票價格類型
```python
sj.StockPriceType.LMT  # Limit 限價
sj.StockPriceType.MKT  # Market 市價
sj.StockPriceType.MKP  # Range Market 範圍市價
```

### Futures Price Type 期貨價格類型
```python
sj.FuturesPriceType.LMT  # Limit 限價
sj.FuturesPriceType.MKT  # Market 市價
sj.FuturesPriceType.MKP  # Range Market 範圍市價
```

### Order Type 委託條件
```python
sj.OrderType.ROD  # Rest of Day 當日有效
sj.OrderType.IOC  # Immediate or Cancel 立即成交否則取消
sj.OrderType.FOK  # Fill or Kill 全部成交否則取消
```

### Stock Order Lot 股票交易單位
```python
sj.StockOrderLot.Common      # Regular 整股 (1000 shares)
sj.StockOrderLot.Odd         # After-hours odd lot 盤後零股
sj.StockOrderLot.IntradayOdd # Intraday odd lot 盤中零股
sj.StockOrderLot.Fixing      # Fixing 定盤
```

### Order Condition 信用交易條件
```python
sj.StockOrderCond.Cash          # Cash 現股
sj.StockOrderCond.MarginTrading # Margin 融資
sj.StockOrderCond.ShortSelling  # Short 融券
```

---

## Account Objects 帳戶物件

```python
# Stock account 股票帳戶
api.stock_account

# Futures account 期貨帳戶
api.futopt_account

# List all accounts 列出所有帳戶
api.list_accounts()
```

---

## Common Patterns 常用模式

### Subscribe Market Data 訂閱行情

```python
# Subscribe tick data 訂閱逐筆成交
api.subscribe(
    api.Contracts.Stocks["2330"],
    quote_type=sj.QuoteType.Tick
)

# Set callback using decorator 設定回調
@api.on_tick_stk_v1()
def quote_callback(exchange, tick):
    print(f"Code: {tick.code} | Price: {tick.close} | Vol: {tick.volume}")
```

### Query Positions 查詢持倉

```python
# Stock positions 股票持倉
positions = api.list_positions(api.stock_account)

# Futures positions 期貨持倉
positions = api.list_positions(api.futopt_account)
```

### Cancel Order 刪單
```python
api.cancel_order(trade)
```

### Update Order 改單
```python
# Change price 改價
api.update_order(trade=trade, price=590)

# Reduce quantity 減量 (can only reduce 只能減少)
api.update_order(trade=trade, qty=1)
```

---

## Rate Limits 流量與頻率限制

| Category 類別 | Limit 限制 |
|---|---|
| **Daily Traffic 每日流量** | 500MB - 10GB (based on trading volume 依交易量) |
| **Quote Query 行情查詢** | 50 requests / 5 sec |
| **Accounting Query 帳務查詢** | 25 requests / 5 sec |
| **Connections 連線數** | 5 concurrent connections per Person ID |
| **Daily Logins 每日登入** | 1000 times / day |
