# FinMind Dataset Index

> This reference contains detailed information on 75+ Taiwan market datasets and international market data.

## 1. Taiwan Market - Technical (20 datasets)
- `TaiwanStockInfo`: (Free) Stock universe.
- `TaiwanStockPrice`: (Free with data_id) Daily price. `close` is lowercase.
- `TaiwanStockPriceAdj`: (Free with data_id) Adjusted daily price.
- `TaiwanStockPriceTick`: (Backer/Sponsor) Historical tick-by-tick.
- `TaiwanStockPER`: (Free) PER, PBR, dividend yield.
- `TaiwanStockDayTrading`: (Free) Day trading volume and amount.
- `TaiwanStockKBar`: (Sponsor) Intraday K-bars.
- `TaiwanStockPriceLimit`: (Free) Daily price limits (漲跌停價).

## 2. Taiwan Market - Chip / Institutional (18 datasets)
- `TaiwanStockInstitutionalInvestorsBuySell`: (Free) Buy/Sell by institutions.
- `TaiwanStockMarginPurchaseShortSale`: (Free) Margin/Short sale balances.
- `TaiwanStockShareholding`: (Free) Foreign ownership.
- `TaiwanStockHoldingSharesPer`: (Backer/Sponsor) Shareholder level distribution (股權分級).
- `TaiwanStockTradingDailyReport`: (Sponsor) Broker daily report (分點資料).
- `TaiwanstockGovernmentBankBuySell`: (Sponsor) Eight major government-owned banks buy/sell.

## 3. Taiwan Market - Fundamental (12 datasets)
- `TaiwanStockFinancialStatements`: (Free) Income statement, balance sheet, cash flows.
- `TaiwanStockMonthRevenue`: (Free) Monthly revenue.
- `TaiwanStockDividend`: (Free) Dividend policy.
- `TaiwanStockMarketValue`: (Backer/Sponsor) Market capitalization.

## 4. Taiwan Market - Derivative (16 datasets)
- `TaiwanFuturesDaily`: (Free) Futures daily trading data.
- `TaiwanOptionDaily`: (Free) Options daily trading data.
- `TaiwanFuturesTick`: (Backer/Sponsor) Futures ticks.
- `TaiwanOptionTIck`: (Backer/Sponsor) Options ticks.

## 5. Taiwan Market - Real-Time (4 datasets)
- `taiwan_stock_tick_snapshot`: (Sponsor) Real-time stock quotes.
- `taiwan_futures_snapshot`: (Sponsor) Real-time futures quotes.

## 6. International Markets
- `USStockInfo` / `USStockPrice`: US market overview and daily prices.
- `UKStockInfo` / `UKStockPrice`: UK market.
- `EuropeStockInfo` / `EuropeStockPrice`: European markets.
- `JapanStockInfo` / `JapanStockPrice`: Japanese market.

## 7. Global Economic Data
- `TaiwanExchangeRate`: FX rates (USD, EUR, JPY, etc.).
- `InterestRate`: Central bank interest rates (FED, BOE, ECB, etc.).
- `GoldPrice` / `CrudeOilPrices`: Global commodities.
- `CnnFearGreedIndex`: (Backer/Sponsor) CNN Fear & Greed Index.

---
For more details, refer to the [official documentation](https://finmind.github.io/).
