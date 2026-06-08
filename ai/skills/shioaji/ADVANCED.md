# Advanced Features 進階功能

This document covers high-performance and automated trading workflows: non-blocking API calls, quote binding with context, stop/touch order patterns, and high-performance market data management using Polars.
本文件說明非阻塞模式、報價綁定機制、觸價單實作，以及如何利用 Polars 處理高頻行情。

---

## Non-blocking Mode 非阻塞模式

By default, Shioaji API calls block execution while waiting for the server/exchange response. Specifying `timeout=0` enables non-blocking mode, where functions return immediately.
預設情況下，Shioaji 呼叫會阻塞等待回應。指定 `timeout=0` 即可啟用非阻塞模式，讓函數立即返回。

### 1. Performance Comparison 效能比對

| Mode 模式 | Round-trip Delay 執行時間 | Speed Improvement 效能提昇 |
| --- | --- | --- |
| **Blocking 阻塞** | ~136 ms | Baseline 基準 |
| **Non-blocking 非阻塞** | ~12 ms | **~11.3x Faster** |

### 2. Async Callbacks

In non-blocking mode, use per-call callbacks (`cb`) or top-level handlers to receive the result.
非阻塞模式下，結果需透過回調函數（`cb`）或全域回調來取得。

```python
import shioaji as sj

api = sj.Shioaji()
api.login(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")
api.activate_ca(ca_path="Sinopac.pfx", ca_passwd="YOUR_CA_PASSWORD")

contract = api.Contracts.Stocks["2330"]
order = sj.StockOrder(
    action=sj.Action.Buy,
    price=580,
    quantity=1,
    price_type=sj.StockPriceType.LMT,
    order_type=sj.OrderType.ROD,
    account=api.stock_account
)

# Callback for non-blocking order placement
def place_order_cb(trade: sj.Trade):
    print(f"Non-blocking place_order completed: {trade.order.id} | Status: {trade.status.status}")

# Place order with timeout=0
trade = api.place_order(contract, order, timeout=0, cb=place_order_cb)
# Returns immediately with status 'PendingSubmit'
```

### 3. Supported Non-blocking APIs

Specify `timeout=0` on any of these functions:
以下函數皆支援 `timeout=0` 進行非阻塞呼叫：
- `place_order()`, `place_comboorder()`
- `update_order()`, `cancel_order()`, `cancel_comboorder()`
- `update_status()`, `update_combostatus()`
- `list_positions()`, `list_position_detail()`
- `list_profit_loss()`, `list_profit_loss_detail()`
- `margin()`, `account_balance()`, `settlements()`, `trading_limits()`

---

## Quote Binding 報價綁定

Quote binding permits binding a context object (like a queue, dict, or database client) directly to quote callback functions using `bind=True`.
報價綁定模式允許將上下文（例如佇列、Redis 連線、字典等）綁定到行情回調函數中。

### 1. Thread-safe Queue Binding 綁定訊息佇列

```python
from collections import defaultdict, deque
from shioaji import Exchange, TickSTKv1

# Create a queue
msg_queue = defaultdict(deque)

# Set the context on the API instance
api.set_context(msg_queue)

# Bind the context using bind=True in decorator
@api.on_tick_stk_v1(bind=True)
def quote_callback(self, exchange: Exchange, tick: TickSTKv1):
    # 'self' refers directly to msg_queue context
    self[tick.code].append(tick)
```

### 2. Redis Stream Binding 綁定 Redis 行情流

```python
import redis
import json
from shioaji import Exchange, TickFOPv1

# Setup Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)
api.set_context(r)

@api.on_tick_fop_v1(bind=True)
def quote_callback(self, exchange: Exchange, tick: TickFOPv1):
    channel = f"Q:{tick.code}"
    # 'self' refers directly to the redis.Redis client
    self.xadd(channel, {'tick': json.dumps(tick.to_dict(raw=True))})
```

---

## Touch/Stop Orders 觸價委託

Shioaji does not run a server-side touch order engine for stocks/futures. You can implement a local client-side trigger loop.
Shioaji 未提供證券端點的伺服器端觸價單，以下為在用戶端實現價格監控與觸發下單的實作模式。

```python
import shioaji as sj
from pydantic import BaseModel

class TouchOrderCond(BaseModel):
    contract: sj.contracts.BaseContract
    order: sj.order.StockOrder # or sj.order.FuturesOrder
    touch_price: float

class TouchOrderExecutor:
    def __init__(self, api: sj.Shioaji, condition: TouchOrderCond):
        self.flag = False
        self.api = api
        self.order = condition.order
        self.contract = condition.contract
        self.touch_price = condition.touch_price
        
        # Subscribe to target contract quotes
        self.api.subscribe(self.contract, quote_type=sj.QuoteType.Tick)
        
        # Hook callback
        self.api.set_on_tick_stk_v1_callback(self.touch_handler)

    def touch_handler(self, exchange: sj.Exchange, tick: sj.TickSTKv1):
        price = float(tick.close)
        if price == self.touch_price and not self.flag:
            self.flag = True
            # Trigger order placement
            self.api.place_order(self.contract, self.order)
            # Unsubscribe to clean up
            self.api.unsubscribe(self.contract, quote_type=sj.QuoteType.Tick)
            print(f"Touch Order Triggered: {self.contract.code} at {price}")
```

---

## High-Performance Quote Management with Polars

Using **Polars** and **polars_talib** allows parallel and vectorized technical indicator calculations on multi-symbol streams without blocking main callbacks.
利用 Polars 與 polars_talib 處理大量行情資料，並利用 over("code") 進行多商品指標的並行運算。

### Installation
```bash
uv add polars polars_talib
```

### QuoteManager Implementation
```python
import shioaji as sj
import polars as pl
import polars_talib as plta
from typing import List, Set

class QuoteManager:
    def __init__(self, api: sj.Shioaji):
        self.api = api
        self.subscribed_stk_tick: Set[str] = set()
        
        # Set callbacks to simply append ticks (minimal logic inside callback threads)
        self.api.set_on_tick_stk_v1_callback(self.on_stk_v1_tick_handler)
        self.ticks_stk_v1: List[sj.TickSTKv1] = []
        
        # Empty placeholder DataFrame
        self.df_stk: pl.DataFrame = pl.DataFrame(
            [],
            schema=[
                ("datetime", pl.Datetime),
                ("code", pl.Utf8),
                ("price", pl.Float64),
                ("volume", pl.Int64),
                ("tick_type", pl.Int8),
            ],
        )

    def on_stk_v1_tick_handler(self, exchange: sj.Exchange, tick: sj.TickSTKv1):
        self.ticks_stk_v1.append(tick)

    def subscribe_stk_tick(self, codes: List[str], recover: bool = False):
        """Subscribe to stock tick quotes, optionally recovering historical day-ticks."""
        for code in codes:
            contract = self.api.Contracts.Stocks[code]
            if contract is not None and code not in self.subscribed_stk_tick:
                self.api.subscribe(contract, sj.QuoteType.Tick)
                self.subscribed_stk_tick.add(code)
                
                if recover:
                    # Fetch historical ticks from API to fill in missing morning data
                    hist_df = self.fetch_ticks(contract)
                    if not hist_df.is_empty():
                        self.df_stk = self.df_stk.vstack(hist_df)

    def fetch_ticks(self, contract: sj.contracts.BaseContract) -> pl.DataFrame:
        ticks = self.api.ticks(contract)
        return pl.DataFrame(ticks.dict()).select([
            # Convert nanosecond ts to datetime
            pl.from_epoch("ts", time_unit="ns").dt.cast_time_unit("us").alias("datetime"),
            pl.lit(contract.code).alias("code"),
            pl.col("close").alias("price"),
            pl.col("volume").cast(pl.Int64),
            pl.col("tick_type").cast(pl.Int8),
        ])

    def get_df_stk(self) -> pl.DataFrame:
        """Flushes tick list buffer and stacks to Polars DataFrame."""
        poped_ticks, self.ticks_stk_v1 = self.ticks_stk_v1, []
        if poped_ticks:
            df = pl.DataFrame([tick.to_dict() for tick in poped_ticks]).select([
                pl.col("datetime", "code"),
                pl.col("close").cast(pl.Float64).alias("price"),
                pl.col("volume").cast(pl.Int64),
                pl.col("tick_type").cast(pl.Int8),
            ])
            self.df_stk = self.df_stk.vstack(df)
        return self.df_stk

    def get_df_stk_kbar(self, unit: str = "1m", exprs: List[pl.Expr] = []) -> pl.DataFrame:
        """Aggregates tick streams to OHLCV K-bars and runs technical expressions."""
        df = self.get_df_stk()
        if df.is_empty():
            return df
            
        # Group and aggregate
        df_kbar = df.group_by(
            pl.col("datetime").dt.truncate(unit),
            pl.col("code"),
            maintain_order=True,
        ).agg([
            pl.col("price").first().alias("open"),
            pl.col("price").max().alias("high"),
            pl.col("price").min().alias("low"),
            pl.col("price").last().alias("close"),
            pl.col("volume").sum().alias("volume"),
        ])
        
        if exprs:
            df_kbar = df_kbar.with_columns(exprs)
        return df_kbar

    def unsubscribe_all(self):
        for code in self.subscribed_stk_tick:
            contract = self.api.Contracts.Stocks[code]
            if contract is not None:
                self.api.unsubscribe(contract, sj.QuoteType.Tick)
        self.subscribed_stk_tick.clear()
```

### Running Indicators (Example)
Calculate EMA and MACD on multiple symbols simultaneously using Polars expressions:

```python
qm = QuoteManager(api)
qm.subscribe_stk_tick(["2330", "2317", "2890"], recover=True)

# Define Technical Expressions
exprs = [
    # 5-period EMA calculated independently for each stock code
    pl.col("close").ta.ema(5).over("code").fill_nan(None).alias("ema5"),
    # MACD line calculated independently
    plta.macd(pl.col("close"), 12, 26, 9).over("code").struct.field("macd").fill_nan(None).alias("macd")
]

# Fetch updated K-bars with indicators
df_kbars = qm.get_df_stk_kbar(unit="5m", exprs=exprs)
```
