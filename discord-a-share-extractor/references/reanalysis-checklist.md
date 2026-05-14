# Second-Pass Timing Re-Analysis

Run this after the first screen identifies an A-share as `已到位`, `接近`, or `研究区间内`.

## Inputs

Collect:

- Eastmoney latest price, percent change, and quote timestamp
- Entry 1 / Entry 2 from timing PDF
- research entry zone
- stop loss or invalidation
- TP1 / TP2
- timing verdict
- daily price action context if available: limit-up/down, gap, intraday high/low
- report catalysts: earnings date, sector event, macro event, index risk

## Checks

1. **Invalidation**
   - If current price is below stop or the report's structural failure level, mark `放弃`.
   - If price is below Entry 2 but above stop, mark `等确认`, not `已到位`.
2. **Entry freshness**
   - If price is within Entry 1/2 zone, continue.
   - If it has rebounded more than about 2% above Entry 1, mark `追高不入` unless the timing report allows breakout/retest entry.
   - If it is inside the wider research zone but above timing entry, mark `轻仓试探` or `等回调`.
3. **Reward/risk**
   - Estimate `(TP1 - current price) / (current price - stop)`.
   - Prefer `>= 1.5`; below that, mark `放弃` or `轻仓试探`.
4. **A-share microstructure**
   - Avoid fresh entries during limit-up/limit-down behavior.
   - Be careful when the stock is down sharply intraday but no stabilization is visible; mark `等确认`.
   - If quote is mid-session and volatility is large, state that close confirmation is stronger than intraday touch.
5. **Timing verdict semantics**
   - `WAIT_PULLBACK`: require pullback plus stabilization.
   - `WAIT_BREAKOUT`: require breakout and retest.
   - `ENTER_NOW`: verify price remains in the stated window.

## Verdicts

- `仍可入场`: entry is fresh, stop is intact, and reward/risk works.
- `轻仓试探`: valid but marginal; use reduced size.
- `等确认`: wait for stabilization/reclaim/close confirmation.
- `放弃`: invalidated or poor reward/risk.
- `追高不入`: price already left the entry window.

Write the reason in one short clause.
