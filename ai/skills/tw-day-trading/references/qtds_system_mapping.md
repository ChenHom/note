# quantitative-trading-decision-system Mapping

## Project Identity

- Alias: `當沖`
- Path: `~/services/stock/quantitative-trading-decision-system`
- Cron entrypoint: `scripts/run_trading_system.sh`
- Intraday monitor entrypoint: `scripts/run_intraday_event_monitor.sh`

## Runtime Phases

### Before Open
- check Taiwan trading day
- login broker
- load contracts
- run pre-market screening
- optionally merge manual watchlist
- subscribe watchlist + market index

### After Open
- 09:00–09:30 poll intraday event signals from `logs/intraday_event_signals.json`
- 09:15 run first supplement
- 09:30 run second supplement
- evaluate entries during trading window
- evaluate exits for open positions continuously

### End Of Day
- 13:20 start forced liquidation logic
- after shutdown, calculate performance metrics
- run trade analysis / markdown reporting

## Important Config Knobs Observed

- `STRATEGY_VWAP_HOLD_MINUTES = 3`
- `STRATEGY_VOLUME_SURGE_RATIO = 1.5`
- `STRATEGY_MARKET_INDEX_FLOOR = -0.005`
- `STRATEGY_PREVIOUS_HIGH_LOOKBACK_BARS = 5`
- `STRATEGY_PARTIAL_EXIT_RATIO = 0.5`
- `SUPPLEMENT_MIN_CHANGE_PCT_915 = 0.05`
- `SUPPLEMENT_MIN_VOLUME_915 = 1000`
- `SUPPLEMENT_MIN_CHANGE_PCT_930 = 0.05`
- `SUPPLEMENT_MIN_VOLUME_930 = 2000`
- `SUPPLEMENT_MAX_ADD = 5`
- `INTRADAY_SIGNAL_REFRESH_SEC = 10`
- `MANUAL_WATCHLIST_PATH = config/manual_watchlist.json`

## Candidate Sources

1. Pre-market scanner
2. Manual watchlist merge
3. Intraday event signal sync
4. 09:15 supplement
5. 09:30 supplement

When diagnosing a missed trade, identify which source should have surfaced the symbol.

## Entry Vocabulary To Reuse

- VWAP hold
- volume surge
- market index floor
- previous high / previous low
- opening window
- entry count limits
- stop-loss cooldown

## Exit Vocabulary To Reuse

- `EXIT_STOP_LOSS`
- `EXIT_TAKE_PROFIT`
- `EXIT_INDICATOR_BREAK`
- `EXIT_TIME`
- forced exit

## Practical Audit Questions

1. Was the symbol ever in any candidate source?
2. If added late, was it extended before evaluation started?
3. Did the market floor block entries correctly?
4. Was VWAP hold satisfied before entry?
5. Did partial profit logic reduce size too early?
6. Did the position survive until 13:20 because earlier exit logic was too weak?
