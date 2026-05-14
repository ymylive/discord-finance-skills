# Gold Current-Level Re-Analysis

Run this when current XAUUSD/GC1 is near a report support, resistance, breakout, or breakdown level.

## Inputs

Collect:

- latest XAUUSD and, when possible, GC1 price
- report base range
- upside confirmation levels
- downside confirmation levels
- stop/invalidation levels from any trade plan
- event calendar: CPI, PPI, NFP, FOMC, Fed speakers, major geopolitical headlines
- current session: Asia, London, NY, killzone, post-event

## Checks

1. **Location**
   - If price is in the middle of the base range, mark `不做`.
   - If price is at support/resistance, continue only if the report allows a conditional trade there.
2. **Confirmation**
   - For support longs, require stabilization/reclaim, not just a touch.
   - For resistance shorts, require rejection/failure, not just proximity.
   - For breakout trades, require close/hold above the confirmation level and ideally a retest.
   - For breakdown trades, require close/hold below the trigger and retest failure.
3. **Event risk**
   - If a high-impact event is within the no-trade window, mark `不做` or `等确认`.
   - Preserve any report-specific no-trade rule, such as avoiding NFP minutes before/after release.
4. **Reward/risk**
   - Check that the nearest target is far enough from entry relative to stop.
   - If the stop must be too wide for the account/risk rule, mark `轻仓` or `不做`.
5. **Model agreement**
   - If Opus and GPT agree on the level and direction, confidence improves.
   - If one model says range and the other says directional, require stronger confirmation.

## Verdicts

- `可执行`: price is at the level, confirmation exists, event rules allow trading, and risk/reward works.
- `轻仓`: valid but fragile or event risk is elevated.
- `等确认`: price is near the level but confirmation is missing.
- `不做`: middle of range, event window, invalidated, or reward/risk is poor.

State the exact level that would change the verdict.
