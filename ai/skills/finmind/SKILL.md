---
name: finmind
description: |
  FinMind Financial Data API guide. Use for fetching historical or statistical data (75+ datasets) for Taiwan and International markets (US/UK/EU/JP), including stock prices, institutional buy/sell, margin trading, FX rates, interest rates, and commodities. Supports high-performance async batch queries and quota management. DO NOT use for real-time order execution.
---

# FinMind Data API Skill

This skill provides comprehensive guidance for using the FinMind Python SDK to fetch Taiwan stock market data.

## Overview
FinMind is an open-source financial data provider offering technical, fundamental, and chip-level data for the Taiwan Stock Exchange (TWSE).

## Core Usage

### 1. Initialization & Authentication
Always use `login_by_token` to increase your API quota (usually to 600+ calls per hour).

```python
from FinMind.data import DataLoader
dl = DataLoader()
dl.login_by_token(api_token="YOUR_TOKEN")
```

### 2. Fetching Market Data
Most methods support `stock_id` (single) or `stock_id_list` (bulk).

#### Daily Price Data
- **Method**: `taiwan_stock_daily`
- **Columns**: `date`, `stock_id`, `Trading_Volume`, `Trading_money`, `open`, `max`, `min`, `close`, `spread`
- **Note**: `close` is lowercase.

#### Institutional Investors
- **Method**: `taiwan_stock_institutional_investors`
- **Columns**: `date`, `stock_id`, `name`, `buy`, `sell`
- **Logic**: Net buy = `buy - sell`.

#### Margin Purchase & Short Sale
- **Method**: `taiwan_stock_margin_purchase_short_sale`
- **Columns**: `MarginPurchaseTodayBalance`, `MarginPurchaseYesterdayBalance`, `date`, `stock_id`, etc.

#### Stock Info (Universe)
- **Method**: `taiwan_stock_info`
- **Columns**: `stock_id`, `industry_category` (used to filter ETFs/Warrants).

## Best Practices
- **Bulk Fetching**: Prefer `stock_id_list` over individual calls to save quota and reduce latency.
- **Date Format**: Always use `YYYY-MM-DD`.
- **Data Update**: Market data is usually updated after 15:30 Taipei time. Margin data might lag until 21:00.
- **Error Handling**: Use exponential backoff for 502/504 errors or quota limits.

## Troubleshooting
- `AttributeError: 'DataLoader' object has no attribute 'taiwan_stock_price'`: Use `taiwan_stock_daily` instead.
- `TypeError: login_by_token() got an unexpected keyword argument 'token'`: Use `api_token` as the parameter name.
- `KeyError: 'Close'`: Remember `close` is lowercase in the `taiwan_stock_daily` result.
