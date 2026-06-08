# Accounting 帳務查詢

This document covers bank balance, margin, positions (unrealized P&L), realized P&L, settlements, and trading limits in Shioaji 1.5+.
本文件說明如何查詢帳戶餘額、保證金、持倉部位（未實現損益）、已實現損益、交割款與交易額度。

---

## Overview 概覽

| Function 函數 | Description 說明 |
| --- | --- |
| `api.account_balance()` | Stock bank account balance 證券交割銀行餘額 |
| `api.margin()` | Futures margin information 期貨帳戶保證金 |
| `api.list_positions()` | Unrealized open positions 未實現持倉部位 |
| `api.list_position_detail()` | Unrealized position details 未實現部位明細 |
| `api.list_profit_loss()` | Realized profit & loss 已實現交易損益 |
| `api.list_profit_loss_detail()` | Realized profit & loss details 已實現交易明細 |
| `api.list_profit_loss_summary()` | Realized profit & loss summary 已實現交易彙總 |
| `api.settlements()` | Stock settlement schedule (T+2) 證券交割款查詢 |
| `api.trading_limits()` | Stock trading limits & available margin 證券交易額度與可用信用額度 |

---

## Bank Balance 銀行餘額 (Stock)

Query the balance of your linked bank account or settlement account (SinoPac Bank, Bankee, LINE Bank, etc.).
查詢證券交割帳戶餘額：

### 1. Python SDK
```python
# Query default stock account balance
balance = api.account_balance()

print(f"Date: {balance.date} | Balance: {balance.acc_balance} | Status: {balance.status} | ErrMsg: {balance.errmsg}")
```
*   **Attributes**: `status` (`FetchStatus`), `acc_balance` (`float`), `date` (`str`), `errmsg` (`str`)

### 2. Standalone CLI & HTTP REST
*   **CLI**:
    ```bash
    shioaji portfolio balance [--account BROKER_ID-ACCOUNT_ID]
    ```
*   **HTTP REST**: `POST /api/v1/portfolio/account_balance`
    ```json
    { "account_type": "S", "broker_id": "YOUR_BROKER_ID", "account_id": "YOUR_ACCOUNT_ID" }
    ```

---

## Margin 保證金查詢 (Futures)

Query margin numbers for futures/options accounts.
查詢期貨帳戶之權益數與保證金狀態：

### 1. Python SDK
```python
margin = api.margin(api.futopt_account)

print(f"Equity (權益數): {margin.equity} | Today Balance (今日餘額): {margin.today_balance}")
print(f"Available Margin (可出金): {margin.available_margin} | Risk Indicator (風險指標): {margin.risk_indicator}%")
```
*   **Key Attributes**: `yesterday_balance`, `today_balance`, `deposit_withdrawal`, `fee`, `tax`, `initial_margin` (原始保證金), `maintenance_margin` (維持保證金), `margin_call` (追繳), `risk_indicator` (風險指標 %), `equity` (權益數), `available_margin` (可動用保證金), `future_open_position` (期貨未平倉損益)

### 2. Standalone CLI & HTTP REST
*   **CLI**:
    ```bash
    shioaji portfolio margin [--account BROKER_ID-ACCOUNT_ID]
    ```
*   **HTTP REST**: `POST /api/v1/portfolio/margin`
    ```json
    { "account_type": "F", "broker_id": "YOUR_BROKER_ID", "account_id": "YOUR_ACCOUNT_ID" }
    ```

---

## Open Positions 未實現部位

Query open positions and unrealized profit/loss.
查詢當前未平倉部位與未實現損益：

### 1. Stock Open Positions 證券持倉
```python
# Query regular lot (Common) or odd lot (Share)
positions = api.list_positions(api.stock_account, unit=sj.Unit.Common)

for pos in positions:
    print(f"Stock: {pos.code} | Quantity: {pos.quantity} | Avg Price: {pos.price} | Last Price: {pos.last_price} | P&L: {pos.pnl}")
```
*   **StockPosition Attributes**: `id` (`int`), `code` (`str`), `direction` (`Action`), `quantity` (`int`), `price` (`float` - average cost), `last_price` (`float`), `pnl` (`float`), `yd_quantity` (`int`), `cond` (`StockOrderCond`), `margin_purchase_amount` (`int`), `collateral` (`int`), `short_sale_margin` (`int`), `interest` (`int`)

### 2. Futures/Options Open Positions 期權持倉
```python
positions = api.list_positions(api.futopt_account)

for pos in positions:
    print(f"Contract: {pos.code} | Quantity: {pos.quantity} | Avg Price: {pos.price} | Last Price: {pos.last_price} | P&L: {pos.pnl}")
```
*   **FuturePosition Attributes**: `id` (`int`), `code` (`str`), `direction` (`Action`), `quantity` (`int`), `price` (`float`), `last_price` (`float`), `pnl` (`float`)

### 3. HTTP REST Endpoint
`POST /api/v1/portfolio/position_unit`
```json
{
  "account_type": "S",
  "unit": "Common",
  "broker_id": "YOUR_BROKER_ID",
  "account_id": "YOUR_ACCOUNT_ID"
}
```

---

## Position Details 未實現明細

Query detailed entry lots for a specific position ID.
查詢特定部位的交易明細（進場日期、書號等）：

### 1. Python SDK
```python
# Get details for StockPosition with id=0
details = api.list_position_detail(api.stock_account, detail_id=0)

for d in details:
    print(f"Date: {d.date} | Qty: {d.quantity} | Price: {d.price} | Fee: {d.fee} | OrderBook Seq: {d.dseq}")
```
*   **StockPositionDetail Attributes**: `date` (`str` - YYYY-MM-DD), `code` (`str`), `quantity` (`int`), `price` (`float` - cost price), `last_price` (`float`), `dseq` (`str` - order book sequence 委託書號), `direction` (`Action`), `pnl` (`float`), `currency` (`Currency`), `fee` (`float`), `cond` (`StockOrderCond`), `ex_dividends` (`int`), `interest` (`int`), `margintrading_amt` (`int`), `collateral` (`int`)

### 2. HTTP REST Endpoint
`POST /api/v1/portfolio/position_detail`
```json
{
  "account_type": "S",
  "detail_id": 0,
  "broker_id": "YOUR_BROKER_ID",
  "account_id": "YOUR_ACCOUNT_ID"
}
```

---

## Realized Profit & Loss 已實現損益

Query matching closed transactions and realized profit/loss.
查詢已平倉沖銷之交易紀錄與已實現損益：

### 1. Realized Transactions List 已實現損益明細列表
```python
pnl_list = api.list_profit_loss(
    api.stock_account,
    begin_date="2026-05-01",
    end_date="2026-05-21"
)

for p in pnl_list:
    print(f"Stock: {p.code} | Date: {p.date} | Price: {p.price} | Qty: {p.quantity} | P&L: {p.pnl}")
```
*   **StockProfitLoss Attributes**: `id` (`int`), `code` (`str`), `quantity` (`int`), `pnl` (`float`), `date` (`str`), `dseq` (`str`), `price` (`float` - close transaction price), `pr_ratio` (`float` - return rate), `cond` (`StockOrderCond`), `seqno` (`str`)
*   **FutureProfitLoss Attributes**: `id` (`int`), `code` (`str`), `quantity` (`int`), `pnl` (`float`), `date` (`str`), `entry_price` (`float`), `cover_price` (`float`), `tax` (`int`), `fee` (`int`), `direction` (`Action`)

### 2. Realized Details已實現損益明細
Query the exact entry and exit legs of a matched transaction.
查詢已實現交易之進出場明細：
```python
details = api.list_profit_loss_detail(api.stock_account, detail_id=0)
for d in details:
    print(f"Trade Date: {d.date} | Cost: {d.cost} | Fee: {d.fee} | Tax: {d.tax} | Price: {d.price}")
```
*   **StockProfitDetail Attributes**: `date`, `code`, `quantity`, `dseq`, `fee`, `tax`, `currency`, `price`, `cost`, `rep_margintrading_amt`, `rep_collateral`, `rep_margin`, `shortselling_fee`, `ex_dividend_amt`, `interest`, `trade_type`, `cond`

### 3. Realized Summary 已實現損益彙總
Query aggregate statistics grouped by ticker.
按個股彙總損益與交易統計：
```python
summary = api.list_profit_loss_summary(
    api.stock_account,
    begin_date="2026-05-01",
    end_date="2026-05-21"
)

# Overall totals
print(f"Total P&L: {summary.total.pnl} | Return: {summary.total.pr_ratio}%")

# Individual stock summaries
for s in summary.profitloss_summary:
    print(f"Stock: {s.code} | Buy Cost: {s.buy_cost} | Sell Cost: {s.sell_cost} | P&L: {s.pnl}")
```

### 4. HTTP REST Endpoints

#### List Realized Profit & Loss (已實現損益列表)
`POST /api/v1/portfolio/profit_loss`
```json
{
  "account_type": "S",
  "begin_date": "2026-05-01",
  "end_date": "2026-05-21",
  "broker_id": "YOUR_BROKER_ID",
  "account_id": "YOUR_ACCOUNT_ID"
}
```

#### Realized Profit & Loss Detail (已實現損益明細)
`POST /api/v1/portfolio/profit_loss_detail`
```json
{
  "account_type": "S",
  "detail_id": 0,
  "broker_id": "YOUR_BROKER_ID",
  "account_id": "YOUR_ACCOUNT_ID"
}
```

#### Realized Profit & Loss Summary (已實現損益彙總)
`POST /api/v1/portfolio/profitloss_sum`
```json
{
  "account_type": "S",
  "begin_date": "2026-05-01",
  "end_date": "2026-05-21",
  "broker_id": "YOUR_BROKER_ID",
  "account_id": "YOUR_ACCOUNT_ID"
}
```


---

## Settlements 交割資訊 (Stock)

Query upcoming settlement schedules (T+1, T+2 cash flows).
查詢證券交易交割款時程與金額：

### 1. Python SDK
```python
settlements = api.settlements(api.stock_account)

for s in settlements:
    print(f"Settlement Date: {s.date} | Amount: {s.amount}")
    print(f"  T-Day: {s.t_money} | T+1: {s.t1_money} | T+2: {s.t2_money}")
```
*   **Attributes**: `date` (`str`), `amount` (`float`), `t_money` (`float`), `t1_money` (`float`), `t2_money` (`float`)

### 2. Standalone CLI & HTTP REST
*   **CLI**:
    ```bash
    shioaji portfolio settlements [--account BROKER_ID-ACCOUNT_ID]
    ```
*   **HTTP REST**: `POST /api/v1/portfolio/settlements`
    ```json
    { "account_type": "S", "broker_id": "YOUR_BROKER_ID", "account_id": "YOUR_ACCOUNT_ID" }
    ```

---

## Trading Limits 交易額度

Query stock trading limits and margin boundaries.
查詢證券交易限額與信用成數額度（限盤中 8:30 - 15:00 查詢）：

### 1. Python SDK
```python
limits = api.trading_limits(api.stock_account)

print(f"Stock Limit: {limits.trading_limit} | Available: {limits.trading_available}")
print(f"Margin Limit: {limits.margin_limit} | Available: {limits.margin_available}")
```
*   **Attributes**: `status` (`FetchStatus`), `trading_limit` / `trading_used` / `trading_available`, `margin_limit` / `margin_used` / `margin_available`, `short_limit` / `short_used` / `short_available`

### 2. HTTP REST Endpoint
`POST /api/v1/portfolio/trading_limits`
```json
{ "account_type": "S", "broker_id": "YOUR_BROKER_ID", "account_id": "YOUR_ACCOUNT_ID" }
```
