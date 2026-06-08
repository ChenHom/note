# Streaming Market Data 即時行情

This document covers subscribing to real-time market data in Shioaji 1.5+.
本文件說明如何在 Shioaji 1.5+ 中訂閱即時行情資料。

---

## Overview 概覽

In Shioaji 1.5+, real-time market data subscriptions are invoked directly via `api.subscribe()` and `api.unsubscribe()` on the API instance, rather than the deprecated `api.quote.subscribe()`.
在 Shioaji 1.5+ 中，即時串流資料的訂閱與取消訂閱直接呼叫 `api.subscribe()` 與 `api.unsubscribe()`，原 `api.quote.subscribe` 已被棄用。

**Supported Quote Types 報價類型**:
- `sj.QuoteType.Tick` - Trade-by-trade data (逐筆成交行情)
- `sj.QuoteType.BidAsk` - 5 levels order book (五檔委託買賣行情)
- `sj.QuoteType.Quote` - Full tick + bidask combined quote (完整即時行情)

**Data Classes 資料類別**:
- `sj.TickSTKv1` / `sj.TickFOPv1` - Stock / Futures & Options tick data
- `sj.BidAskSTKv1` / `sj.BidAskFOPv1` - Stock / Futures & Options order book
- `sj.QuoteSTKv1` / `sj.QuoteFOPv1` - Stock / Futures & Options combined quote

---

## Subscribing to Quotes 訂閱行情

### 1. Python SDK

```python
import shioaji as sj

api = sj.Shioaji()
api.login(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")

# Stock Tick 訂閱證券逐筆成交
api.subscribe(
    contract=api.Contracts.Stocks["2330"],
    quote_type=sj.QuoteType.Tick
)

# Stock BidAsk 訂閱證券五檔
api.subscribe(
    contract=api.Contracts.Stocks["2330"],
    quote_type=sj.QuoteType.BidAsk
)

# Intraday Odd Lot Tick 訂閱證券盤中零股 Tick
api.subscribe(
    contract=api.Contracts.Stocks["2330"],
    quote_type=sj.QuoteType.Tick,
    intraday_odd=True
)

# Futures Tick 訂閱期貨逐筆成交 (Continuous near-month)
api.subscribe(
    contract=api.Contracts.Futures["TXFR1"],
    quote_type=sj.QuoteType.Tick
)
```

To unsubscribe:
```python
api.unsubscribe(
    contract=api.Contracts.Stocks["2330"],
    quote_type=sj.QuoteType.Tick
)
```

### 2. Standalone CLI

Use `shioaji data stream` to stream live quotes in your terminal (press `Ctrl+C` to stop and unsubscribe):

```bash
# Stream Stock Tick
shioaji data stream --code 2330 --quote-type tick

# Stream Stock BidAsk
shioaji data stream --code 2330 --quote-type bid_ask

# Stream Intraday Odd Lot Tick
shioaji data stream --code 2330 --quote-type tick --intraday-odd

# Stream Futures Tick
shioaji data stream --code TXFR1 --security-type FUT --quote-type tick
```

### 3. HTTP REST & SSE (Server-Sent Events)

First, send a POST request to subscribe, then connect to the corresponding SSE endpoint to receive data.
首先發送 `POST` 訂閱商品，接著連線到 SSE 端點接收串流資料。

#### Step 1: Subscribe
`POST /api/v1/stream/subscribe`
```bash
curl -X POST http://localhost:8080/api/v1/stream/subscribe \
  -H 'Content-Type: application/json' \
  -d '{
    "security_type": "STK",
    "exchange": "TSE",
    "code": "2890",
    "quote_type": "Tick"
  }'
```

#### Step 2: Connect to SSE to receive stream
*   **Stock Ticks**: `GET /api/v1/stream/data/tick_stk`
    ```bash
    curl -N http://localhost:8080/api/v1/stream/data/tick_stk
    ```
*   **Stock BidAsks**: `GET /api/v1/stream/data/bidask_stk`
    ```bash
    curl -N http://localhost:8080/api/v1/stream/data/bidask_stk
    ```
*   **Futures Ticks**: `GET /api/v1/stream/data/tick_fop`
    ```bash
    curl -N http://localhost:8080/api/v1/stream/data/tick_fop
    ```

> [!IMPORTANT]
> When subscribing to continuous futures (e.g. `TXFR1` / `TXFR2`) via HTTP, you must first lookup the `target_code` (e.g. `TXFF6`) via `/api/v1/data/contracts/TXFR1?security_type=FUT` and pass it in the subscription body:
> `{"security_type": "FUT", "exchange": "TAIFEX", "code": "TXFR1", "target_code": "TXFF6", "quote_type": "Tick"}`

---

## Quote Callbacks 行情回調

Define custom callbacks to receive the full quote schemas.
自訂回調以接收即時行情的完整資料欄位：

### 1. Stock Tick Callback

*   **Decorator Mode**:
    ```python
    from shioaji import Exchange, TickSTKv1
    
    @api.on_tick_stk_v1()
    def quote_callback(exchange: Exchange, tick: TickSTKv1):
        print(f"Code: {tick.code} | Close: {tick.close} | Vol: {tick.volume} | DateTime: {tick.datetime}")
    ```
*   **Traditional Mode**:
    ```python
    def quote_callback(exchange: Exchange, tick: TickSTKv1):
        print(f"{exchange} {tick.code}: {tick.close}")
        
    api.set_on_tick_stk_v1_callback(quote_callback)
    ```

### 2. Stock BidAsk Callback

*   **Decorator Mode**:
    ```python
    from shioaji import Exchange, BidAskSTKv1
    
    @api.on_bidask_stk_v1()
    def quote_callback(exchange: Exchange, bidask: BidAskSTKv1):
        print(f"Bid: {bidask.bid_price} | Ask: {bidask.ask_price}")
    ```
*   **Traditional Mode**:
    ```python
    api.set_on_bidask_stk_v1_callback(quote_callback)
    ```

### 3. Stock Combined Quote Callback

*   **Decorator Mode**:
    ```python
    from shioaji import Exchange, QuoteSTKv1
    
    @api.on_quote_stk_v1()
    def quote_callback(exchange: Exchange, quote: QuoteSTKv1):
        print(f"Price: {quote.close} | Top Bid: {quote.bid_price[0]}")
    ```
*   **Traditional Mode**:
    ```python
    api.set_on_quote_stk_v1_callback(quote_callback)
    ```

### 4. Futures / Options Callbacks

Futures & Options use similar callbacks mapping to `fop` classes:
期權行情回調使用類似的方法：

- `@api.on_tick_fop_v1()` / `api.set_on_tick_fop_v1_callback()` (maps to `TickFOPv1`)
- `@api.on_bidask_fop_v1()` / `api.set_on_bidask_fop_v1_callback()` (maps to `BidAskFOPv1`)
- `@api.on_quote_fop_v1()` / `api.set_on_quote_fop_v1_callback()` (maps to `QuoteFOPv1`)

---

## Connection & Event Callback

Register callback to handle server events (e.g. heartbeat, connection, disconnection, and subscriptions):
註冊回調以處理連線中斷、重連以及訂閱事件：

```python
@api.quote.on_event
def event_callback(resp_code: int, event_code: int, info: str, event: str):
    print(f"Event: {event_code} | Info: {info} | Msg: {event}")
```

### Event Codes:
*   `0` - Heartbeat 心跳
*   `1` - Connected 連線成功
*   `2` - Disconnected 斷線
*   `3` - Reconnecting 重新連線中
*   `4` - Reconnected 重新連線成功
*   `16` - Subscribe success 訂閱成功
*   `17` - Unsubscribe success 取消訂閱成功
