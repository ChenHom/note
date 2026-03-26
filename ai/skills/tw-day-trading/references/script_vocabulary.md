# tw-day-trading Script Vocabulary

Use this vocabulary consistently across scripts and outputs.

## Candidate Sources

- `manual` — manually prioritized symbols
- `premarket` — symbols from pre-market watchlist generation
- `event_sync` — symbols added from intraday event signal sync
- `supplement_915` — symbols added at 09:15 supplement
- `supplement_930` — symbols added at 09:30 supplement

## Candidate Status

- `watch` — keep on watchlist, not near entry yet
- `near_entry` — deserves priority attention, pending confirmation
- `drop` — downgrade / remove from active focus

## Core Lists

- `premarket_list` — original pre-market symbols
- `manual_list` — manual-priority symbols
- `focus_list` — first-attention symbols for the session

## Notes

- `review_intraday_watchlist.py` is a formatter, so status must be provided by the operator.
- `format_daily_intraday_brief.py` should present premarket, manual, and focus lists separately.
- `format_postmarket_review.py` should refer to `event_sync`, `supplement_915`, and `supplement_930` consistently.
