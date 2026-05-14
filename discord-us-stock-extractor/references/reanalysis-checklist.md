# Second-Pass Timing Re-Analysis

Run this after the first screen identifies a ticker as `已到位` or `接近`.

## Inputs

Collect:

- current price and quote timestamp
- Entry 1 / Entry 2 from the timing PDF
- research entry zone
- stop loss or invalidation level
- TP1 / TP2
- timing verdict
- market session state: regular, pre-market, post-market, closed
- any near-term catalyst from the report, such as earnings or macro data

## Checks

1. **Validity**
   - If price is below stop/invalidation, mark `放弃` unless the report explicitly allows a re-entry after reclaim.
   - If price is at or beyond TP1, mark `放弃` or `追高不入`.
2. **Distance to entry**
   - If price is within the timing entry zone, continue.
   - If price is 1-3% above the intended entry, mark `轻仓试探` or `追高不入` depending on risk/reward.
   - If price is below entry but above stop, mark `等确认`.
3. **Reward/risk**
   - Estimate `(TP1 - current price) / (current price - stop)` for longs.
   - Prefer `>= 1.5` for a tactical entry and `>= 2.0` for a cleaner setup.
   - If reward/risk is weak, mark `放弃` even if price touched the zone.
4. **Confirmation**
   - For `WAIT_PULLBACK`, require stabilization: reversal candle, reclaim of key level, volume contraction on pullback, or RSI/MACD improvement if available.
   - For `WAIT_BREAKOUT`, require breakout plus retest; do not enter just because price is near resistance.
   - For `ENTER_NOW`, verify the price has not moved beyond the stated upper entry range.
5. **Event risk**
   - Reduce confidence or mark `等确认` before earnings, CPI/FOMC, or other high-impact events mentioned in the report.

## Verdicts

- `仍可入场`: all checks pass.
- `轻仓试探`: entry is valid but marginal.
- `等确认`: price reached the area but confirmation is missing.
- `放弃`: invalidation triggered or reward/risk collapsed.
- `追高不入`: price ran above the entry window.

Explain the reason in one short clause.
