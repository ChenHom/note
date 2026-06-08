# Orders 交易委託

This document covers placing, modifying, and canceling stock, futures, options, and combo orders.
本文件說明如何進行證券、期貨、選擇權與組合單之委託下單、改單、刪單。

---

## Prerequisites 前置條件

Before placing orders, ensure you have successfully logged in and activated your CA certificate.
下單前請確認已成功登入並啟用憑證。

```python
import os
import shioaji as sj
from dotenv import load_dotenv

load_dotenv()

api = sj.Shioaji()
api.login(api_key=os.environ["SJ_API_KEY"], secret_key=os.environ["SJ_SEC_KEY"])

# Activate CA Certificate 啟用憑證
api.activate_ca(
    ca_path=os.environ["SJ_CA_PATH"],
    ca_passwd=os.environ["SJ_CA_PASSWD"]
)
```

---

## Stock Orders 證券下單

In Shioaji 1.5+, use the dedicated `sj.StockOrder` class instead of the deprecated `api.Order`.
Shioaji 1.5+ 請使用專屬的 `sj.StockOrder` 類別進行證券委託。

### 1. Basic Stock Order 限價整股單

```python
contract = api.Contracts.Stocks["2330"]  # TSMC

order = sj.StockOrder(
    action=sj.Action.Buy,
    price=580,
    quantity=1,
    price_type=sj.StockPriceType.LMT,      # LMT: Limit 限價
    order_type=sj.OrderType.ROD,           # ROD: Rest of Day 當日有效
    order_lot=sj.StockOrderLot.Common,     # Common: Regular 整股 (1000 shares)
    order_cond=sj.StockOrderCond.Cash,     # Cash: 現股
    account=api.stock_account,
)

trade = api.place_order(contract, order)
```

### 2. Market Order 市價單 / 範圍市價單

Market orders (MKT/MKP) only accept `IOC` (Immediate or Cancel) or `FOK` (Fill or Kill) order types.
市價或範圍市價單僅接受 `IOC` 或 `FOK` 委託條件。

```python
# Market Order 市價單 (price must be 0)
mkt_order = sj.StockOrder(
    action=sj.Action.Buy,
    price=0, 
    quantity=1,
    price_type=sj.StockPriceType.MKT,
    order_type=sj.OrderType.IOC,           # Must use IOC or FOK
    account=api.stock_account,
)
trade = api.place_order(contract, mkt_order)

# Range Market Order 範圍市價單
mkp_order = sj.StockOrder(
    action=sj.Action.Buy,
    price=0,
    quantity=1,
    price_type=sj.StockPriceType.MKP,
    order_type=sj.OrderType.IOC,
    account=api.stock_account,
)
trade = api.place_order(contract, mkp_order)
```

### 3. Odd Lot Orders 零股下單

```python
# Intraday Odd Lot 盤中零股 (9:00 - 13:30)
# Note: IntradayOdd orders cannot update price, only reduce quantity.
intraday_odd_order = sj.StockOrder(
    action=sj.Action.Buy,
    price=580,
    quantity=10,                           # 1-999 shares
    price_type=sj.StockPriceType.LMT,
    order_type=sj.OrderType.ROD,
    order_lot=sj.StockOrderLot.IntradayOdd,
    account=api.stock_account,
)
trade = api.place_order(contract, intraday_odd_order)

# After-hours Odd Lot 盤後零股 (13:40 - 14:30)
after_hours_odd_order = sj.StockOrder(
    action=sj.Action.Buy,
    price=580,
    quantity=10,
    price_type=sj.StockPriceType.LMT,
    order_type=sj.OrderType.ROD,
    order_lot=sj.StockOrderLot.Odd,
    account=api.stock_account,
)
trade = api.place_order(contract, after_hours_odd_order)
```

### 4. Margin Trading & Short Selling 信用交易

```python
# Margin Buying 融資買進
margin_buy_order = sj.StockOrder(
    action=sj.Action.Buy,
    price=580,
    quantity=1,
    price_type=sj.StockPriceType.LMT,
    order_type=sj.OrderType.ROD,
    order_cond=sj.StockOrderCond.MarginTrading,
    account=api.stock_account,
)

# Short Selling 融券賣出
short_sell_order = sj.StockOrder(
    action=sj.Action.Sell,
    price=580,
    quantity=1,
    price_type=sj.StockPriceType.LMT,
    order_type=sj.OrderType.ROD,
    order_cond=sj.StockOrderCond.ShortSelling,
    account=api.stock_account,
)
```

---

## Futures & Options Orders 期權下單

In Shioaji 1.5+, use the dedicated `sj.FuturesOrder` class instead of the deprecated `api.Order`.
Shioaji 1.5+ 請使用專屬的 `sj.FuturesOrder` 類別進行期權委託。

### 1. Futures Order 期貨下單

```python
futures_contract = api.Contracts.Futures["TXFR1"]  # Near-month TXF

futures_order = sj.FuturesOrder(
    action=sj.Action.Buy,
    price=18200,
    quantity=1,
    price_type=sj.FuturesPriceType.LMT,
    order_type=sj.OrderType.ROD,
    octype=sj.FuturesOCType.Auto,         # Auto: 自動開平倉 (New / Cover)
    account=api.futopt_account,
)

trade = api.place_order(futures_contract, futures_order)
```

### 2. Options Order 選擇權下單

```python
option_contract = api.Contracts.Options["TXO20260644000C"]

option_order = sj.FuturesOrder(
    action=sj.Action.Buy,
    price=120,
    quantity=1,
    price_type=sj.FuturesPriceType.LMT,
    order_type=sj.OrderType.ROD,
    octype=sj.FuturesOCType.Auto,
    account=api.futopt_account,
)

trade = api.place_order(option_contract, option_order)
```

---

## Combo Orders 組合單下單

Combo contracts are used to execute multi-leg strategies (e.g. Option Spread, Straddle, Strangle).
組合單用於執行多腳策略（例如：價差、跨式、勒式等選擇權組合）。

### 1. Build Combo Contract & Place Order

```python
# Leg 1: Buy TXO Call @ 27000
call_leg_buy = api.Contracts.Options.TXO.get("TXO20260527000C")
# Leg 2: Sell TXO Call @ 27200
call_leg_sell = api.Contracts.Options.TXO.get("TXO20260527200C")

# Build ComboContract
combo_contract = sj.ComboContract(
    legs=[
        sj.ComboBase.from_contract(call_leg_buy, action=sj.Action.Buy),
        sj.ComboBase.from_contract(call_leg_sell, action=sj.Action.Sell)
    ]
)

# Build ComboOrder
combo_order = sj.ComboOrder(
    action=sj.Action.Buy,
    price=50,  # Spread price
    quantity=1,
    price_type=sj.FuturesPriceType.LMT,
    order_type=sj.OrderType.ROD,
    octype=sj.FuturesOCType.New,
    account=api.futopt_account,
)

# Place Combo Order
combo_trade = api.place_comboorder(combo_contract, combo_order)
```

### 2. Query & Cancel Combo Orders

```python
# Update and list combo orders (HTTP equivalant gets status instantly)
api.update_combostatus(api.futopt_account)
combo_trades = api.list_combotrades()

# Cancel Combo Order
api.cancel_comboorder(combo_trade)
```

---

## Modifying & Canceling Orders 改單與刪單

For modifying and canceling orders, you must supply the original `Trade` object.
改單與刪單時皆必須提供原 `Trade` 物件。

### 1. Update Order Price / Qty 改單

*   **Change Price (改價)**: Updates LMT price.
*   **Reduce Quantity (減量)**: You can only reduce quantity, never increase.

```python
# Change limit price
api.update_order(trade=trade, price=582)

# Reduce quantity to 1 share/contract
api.update_order(trade=trade, qty=1)
```

### 2. Cancel Order 刪單

```python
# Cancel order
api.cancel_order(trade)
```

> [!NOTE]
> Call `api.update_status(api.stock_account)` before cancel/update to ensure the order has received an `ordno` (委託書號) from the exchange.

---

## Order Status 委託狀態

### 1. Update Order Status

Update the local state of trade objects.
更新本地 Trade 物件狀態：

```python
# Update all stock trades
api.update_status(api.stock_account)

# Update all futures trades
api.update_status(api.futopt_account)

# Check active list
trades = api.list_trades()
for t in trades:
    print(f"ID: {t.order.id} | Status: {t.status.status} | Filled: {t.status.deal_quantity}")
```

### 2. Order Status Codes

*   `PendingSubmit`: Submitting to broker/exchange 傳送中
*   `PreSubmitted`: Pre-order/After-hours reservation 預約單
*   `Submitted`: Order accepted by exchange 傳送成功
*   `Failed`: Order rejected 失敗
*   `Cancelled`: Order cancelled 已刪除
*   `Filled`: Fully filled and matched 完全成交
*   `PartFilled`: Partially filled 部分成交

---

## Standalone CLI & HTTP ordering

If you run the local HTTP server (`shioaji server start`), you can place, update, and cancel orders from any programming language or terminal command.

### 1. Place Order

*   **CLI**:
    ```bash
    shioaji order place --code 2890 --action buy --price 27.1 --quantity 2 --price-type lmt --order-type rod --order-lot common --order-cond cash --account YOUR_BROKER_ID-YOUR_ACCOUNT_ID
    ```
*   **HTTP REST**:
    `POST /api/v1/order/place_order`
    ```json
    {
      "contract": {"security_type": "STK", "exchange": "TSE", "code": "2890"},
      "stock_order": {
        "action": "Buy",
        "price": 27.1,
        "quantity": 2,
        "price_type": "LMT",
        "order_type": "ROD",
        "order_lot": "Common",
        "order_cond": "Cash",
        "account": { "broker_id": "YOUR_BROKER_ID", "account_id": "YOUR_ACCOUNT_ID" }
      }
    }
    ```

### 2. Update / Cancel Order (HTTP)

*   **Update Price**: `POST /api/v1/order/update_price`
    ```json
    { "trade_id": "YOUR_TRADE_ID", "price": 27.2 }
    ```
*   **Reduce Qty**: `POST /api/v1/order/update_qty`
    ```json
    { "trade_id": "YOUR_TRADE_ID", "quantity": 1 }
    ```
*   **Cancel Order**: `POST /api/v1/order/cancel_order`
    ```json
    { "trade_id": "YOUR_TRADE_ID" }
    ```
*   **Query Active Status**: `POST /api/v1/order/trades`
    ```json
    { "broker_id": "YOUR_BROKER_ID", "account_id": "YOUR_ACCOUNT_ID" }
    ```
