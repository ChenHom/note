# Taiwan Day Trading Reference Guide

## Scope

This reference supports Taiwan stock intraday workflows, especially for momentum, opening-drive, watchlist supplementation, and disciplined day-risk control.

## Taiwan-Specific Considerations

### 1. Liquidity First

For TW day trading, liquidity is not optional. Review:
- average turnover
- bid/ask stability
- order-book depth
- whether the stock becomes untradeable once momentum cools

### 2. Day-Trade Eligibility / Restrictions

Before adding a name to an intraday watchlist, verify that it can actually be traded in the intended way. Prefer explicit filters for:
- buy-first-sell-later day-trade eligibility
- attention / warning / disposition handling
- special restrictions

### 3. Intraday Additions

A practical TW intraday system often needs two candidate sources:
- pre-market candidates
- post-open supplemental names

For supplemental names, record:
- why the stock was added
- what price structure justified the addition
- whether its first pullback held
- whether the setup remained valid after subscription delay

### 4. Core Intraday Metrics

Useful metrics to organize around:
- opening range high / low
- VWAP
- previous session high / low
- cumulative volume
- turnover acceleration
- relative strength versus index
- high/low of day and whether they keep expanding constructively

### 5. Common Failure Modes

- chasing the first spike without retest
- adding late after extension
- using a stop that is too wide for the expected intraday move
- treating a weak rebound as momentum continuation
- ignoring market-wide deterioration
- overtrading after missing the first clean setup

## Default Review Questions

Use these questions after a trading session:

1. Was the best trade already visible in pre-market, or did it emerge intraday?
2. Did supplemental names outperform the original watchlist?
3. Were entries taken at structure, or emotionally after extension?
4. Were stop-outs acceptable, or the result of poor location?
5. Did time stops prevent capital from being trapped in dead trades?
6. Was daily loss control respected?

## Adapting To Semi-Auto / Automated Systems

When reviewing a TW intraday bot, inspect the pipeline in this order:

1. Candidate generation
2. Manual watchlist override
3. Intraday supplement logic
4. Event-signal sync / file-based sync
5. Tick subscription timing
6. Entry evaluation window
7. Exit rule priority
8. Forced end-of-day liquidation
9. Logs and post-trade analytics

## Good Output Style

Prefer concise operator-ready output:
- what to watch
- what qualifies
- what invalidates
- how much to risk
- when to stop trading

Avoid fake precision when data quality is weak.
