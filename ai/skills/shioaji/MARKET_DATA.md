# Market Data 市場資料

This document covers historical ticks and KBars, snapshots, credit enquiries, short stock sources, scanners, and disposition/attention stocks.
本文件說明如何查詢歷史行情、快照、資券餘額、券源、市場排行以及處置與注意股票。

---

## Historical Ticks 歷史逐筆成交

Query historical tick-by-tick trading data for stocks, futures, or options.
查詢指定日期或時間區段的歷史逐筆成交資料。

### 1. Python SDK

```python
import shioaji as sj

api = sj.Shioaji()
api.login(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")

contract = api.Contracts.Stocks["2330"]

# Query Option 1: All Day (整日)
ticks = api.ticks(contract=contract, date="2026-05-18", query_type=sj.TicksQueryType.AllDay)

# Query Option 2: Range Time (特定時間區段)
ticks = api.ticks(
    contract=contract,
    date="2026-05-18",
    query_type=sj.TicksQueryType.RangeTime,
    time_start="09:00:00",
    time_end="09:20:00"
)

# Query Option 3: Last N Ticks (最後 N 筆)
ticks = api.ticks(
    contract=contract,
    date="2026-05-18",
    query_type=sj.TicksQueryType.LastCount,
    last_cnt=100
)
```

**Ticks Attributes 屬性**:
- `ts` / `datetime`: Timestamps (Unix nanoseconds in Python, ISO string in CLI/HTTP)
- `close`: Trade prices (成交價)
- `volume`: Trade volume (成交量)
- `bid_price` / `ask_price`: Best bid/ask price (委買/賣價)
- `bid_volume` / `ask_volume`: Best bid/ask volume (委買/賣量)
- `tick_type`: 1 = Ask side (外盤), 2 = Bid side (內盤), 0 = Unknown (無法判定)

### 2. Standalone CLI & HTTP REST

*   **CLI**:
    ```bash
    shioaji data ticks --code 2330 --date 2026-05-18 --all
    shioaji data ticks --code 2330 --date 2026-05-18 --last 10
    ```
*   **HTTP REST**: `POST /api/v1/data/ticks`
    ```json
    {
      "contract": { "security_type": "STK", "exchange": "TSE", "code": "2330" },
      "date": "2026-05-18",
      "query_type": "AllDay"
    }
    ```

---

## Historical KBars 歷史 K 線

Query historical 1-minute OHLCV candles (K-bars).
查詢歷史分 K 線資料。

### 1. Python SDK

```python
kbars = api.kbars(
    contract=api.Contracts.Stocks["2330"],
    start="2026-05-17",
    end="2026-05-18"
)
```

**KBars Attributes 屬性**:
- `ts` / `datetime`: Timestamps (Unix nanoseconds in Python, ISO string in CLI/HTTP)
- `Open` / `High` / `Low` / `Close`: K-bar prices (開、高、低、收)
- `Volume`: K-bar volume (成交量)
- `Amount`: K-bar turnover amount (成交額)

### 2. Standalone CLI & HTTP REST

*   **CLI**:
    ```bash
    shioaji data kbars --code 2330 --start 2026-05-17 --end 2026-05-18
    ```
*   **HTTP REST**: `POST /api/v1/data/kbars`
    ```json
    {
      "contract": { "security_type": "STK", "exchange": "TSE", "code": "2330" },
      "start": "2026-05-17",
      "end": "2026-05-18"
    }
    ```

---

## Market Snapshot 即時快照

Retrieve the latest market snapshot for up to 500 contracts.
查詢多個商品合約當下的即時快照（每次上限 500 檔）。

### 1. Python SDK

```python
contracts = [api.Contracts.Stocks["2330"], api.Contracts.Stocks["2890"]]
snapshots = api.snapshots(contracts)

for snap in snapshots:
    print(f"Code: {snap.code} | Close: {snap.close} | Vol: {snap.total_volume} | Change: {snap.change_rate}%")
```

**Snapshot Attributes 快照屬性**:
- `ts`: Timestamp
- `code` / `exchange`: Symbol metadata
- `open` / `high` / `low` / `close` / `average_price`
- `volume` (last trade size) / `total_volume` (total daily size)
- `amount` (last trade amount) / `total_amount` (total daily amount)
- `change_price` / `change_rate`
- `buy_price` / `sell_price` (best bid/ask prices)
- `buy_volume` / `sell_volume` (best bid/ask volumes)
- `volume_ratio` (yesterday volume ratio)

### 2. HTTP REST Endpoint

`POST /api/v1/data/snapshot`
```json
{
  "contracts": [
    { "security_type": "STK", "exchange": "TSE", "code": "2330" }
  ]
}
```

---

## Credit Enquiries 資券餘額

Query margin trading and short selling balances for stock contracts.
查詢個股的融資融券餘額與信用成數。

### 1. Python SDK

```python
contracts = [api.Contracts.Stocks["2330"]]
credit_enquires = api.credit_enquires(contracts)

for c in credit_enquires:
    print(f"Code: {c.stock_id} | Margin: {c.margin_unit} ({c.margin_loan_ratio}%) | Short: {c.short_unit} ({c.short_margin_ratio}%)")
```

**CreditEnquire Attributes 資券屬性**:
- `update_time`: Update time
- `system`: System classification (ALL)
- `stock_id`: Stock code
- `margin_unit`: Margin balance units (融資餘額)
- `short_unit`: Short balance units (融券餘額)
- `margin_loan_ratio`: Margin loan ratio (融資成數)
- `short_margin_ratio`: Short margin ratio (融券成數)

### 2. HTTP REST Endpoint

`POST /api/v1/data/credit_enquire`
```json
{
  "contracts": [
    { "security_type": "STK", "exchange": "TSE", "code": "2330" }
  ]
}
```

---

## Short Stock Sources 或有券源

Query available short selling sources for stock borrowing.
查詢個股當前可借券之或有券源。

### 1. Python SDK

```python
sources = api.short_stock_sources(contracts)
for s in sources:
    print(f"Code: {s.code} | Available Short Source: {s.short_stock_source}")
```

**ShortStockSource Attributes 券源屬性**:
- `code`: Stock code
- `short_stock_source`: Available units for borrowing
- `ts` / `datetime`: Update time

### 2. HTTP REST Endpoint

`POST /api/v1/data/short_stock_sources`
```json
{
  "contracts": [
    { "security_type": "STK", "exchange": "TSE", "code": "2330" }
  ]
}
```

---

## Market Scanners 掃描器排行

Retrieve top-ranked stocks based on various performance and volume metrics.
根據各種價量條件篩選並取得市場即時排行。

### 1. Python SDK

```python
# Available ScannerTypes 排序指標：
# ChangePercentRank (漲跌幅), ChangePriceRank (漲跌價), DayRangeRank (振幅), VolumeRank (成交量), AmountRank (成交金額)

# Top 10 Gainers 漲幅前 10 名
gainers = api.scanners(
    scanner_type=sj.constant.ScannerType.ChangePercentRank,
    ascending=False,
    count=10
)
```

### 2. HTTP REST Endpoint

`POST /api/v1/data/scanners`
```json
{
  "scanner_type": "ChangePercentRank",
  "ascending": false,
  "count": 10
}
```

---

## Disposition & Attention Stocks 處置與注意股

Retrieve stocks flagged under warning or special regulatory regimes.
查詢目前市場上被列為處置股或注意股的名單及交易限制。

### 1. Disposition Stocks 處置股

*   **Query**:
    ```python
    punish = api.punish()
    ```
*   **Attributes**: `code`, `start_date`, `end_date`, `interval` (matching interval e.g. 5m), `unit_limit` (single order limit %), `total_limit` (daily limit %), `description`, `announced_date`

### 2. Attention Stocks 注意股

*   **Query**:
    ```python
    notice = api.notice()
    ```
*   **Attributes**: `code`, `close`, `reason`, `announced_date`, `updated_at`

---

## Data Integration using Polars

Convert query results to [Polars](https://docs.astral.sh/uv/) DataFrames for high-performance calculations.
使用 Polars 將歷史與快照資料轉為 DataFrame 以進行分析：

```python
import polars as pl

# 1. KBars to DataFrame
kbars = api.kbars(api.Contracts.Stocks["2330"], start="2026-05-17", end="2026-05-18")
df_kbars = pl.DataFrame(kbars.dict()).with_columns(
    pl.col("ts").cast(pl.Datetime("ns"))
)

# 2. Snapshots to DataFrame
snapshots = api.snapshots([api.Contracts.Stocks["2330"], api.Contracts.Stocks["2890"]])
df_snaps = pl.DataFrame([s.dict() for s in snapshots])
```
