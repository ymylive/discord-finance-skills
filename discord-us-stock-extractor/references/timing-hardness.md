# US Stock Timing Hardness Standard

Hardness measures how executable the current US stock timing setup is. It is not the same as fundamental conviction; grade it only after refreshing the current quote and running the second-pass timing re-analysis.

## Required Evidence

Use the latest stock timing PDF/embed as the sample shape:

- research verdict: BUY, HOLD, PASS, SELL
- timing verdict: ENTER_NOW, WAIT_PULLBACK, WAIT_BREAKOUT, NOT_YET
- Entry 1 / Entry 2 or entry zone
- stop loss or invalidation
- TP1 / TP2
- current price, quote timestamp, and session state
- near-term events such as earnings, CPI, FOMC, or major company news

## Hard Gates

- If current price is below stop/invalidation, grade `H0`.
- If price is already at or beyond TP1, cap at `H1` and mark `追高不入` or `放弃`.
- If research is not BUY or timing is NOT_YET, cap at `H1`; do not promote as a buy point.
- If Entry, stop, or current price is missing, cap at `H2`.
- If the quote is stale or only pre/post-market, state that and cap at `H3` unless the user explicitly wants extended-hours execution.
- If a high-impact event is imminent, cap at `H2` unless the report explicitly allows event risk.

## Grades

| Grade | Meaning | Stock sample mapping |
|---|---|---|
| `H0` | Invalid / no trade | Stop broken, stale superseded report, NOT_YET, or price is in the middle of nowhere. |
| `H1` | Thesis only | BUY thesis exists, but price is far above entry, near TP1, or lacks usable Entry/SL. |
| `H2` | Soft watch | Price is near the zone, but confirmation, reward/risk, or event safety is missing. |
| `H3` | Conditional entry | Price is in/near the entry zone, stop is intact, reward/risk is at least acceptable, but size should be reduced or confirmation is still needed. |
| `H4` | Actionable | Price is in the entry window, stop is clean, TP1 reward/risk is usually `>= 1.5`, confirmation exists, and event risk is controlled. |
| `H5` | Rare high-quality tactical entry | H4 plus fresh quote, strong report alignment, clear market support, clean invalidation, and reward/risk usually `>= 2.0`. |

## Verdict Mapping

- `ENTER_NOW`: H4 if current price remains inside the stated entry window; H3 if it is near the top of the zone or confirmation is incomplete; H1-H2 if it has run above the window.
- `WAIT_PULLBACK`: H4 only after price reaches Entry 1/2 and stabilizes; H2-H3 if it touched the zone but is still falling; H0 if stop breaks.
- `WAIT_BREAKOUT`: H2 before breakout; H4 only after breakout plus hold/retest; H1 if breakout already ran close to TP1.
- `接近`: usually H2-H3, never H4 unless the current quote has actually entered the timing zone or a breakout trigger completed.
- `追高不入` or `放弃`: H0-H1 even if the original research verdict is BUY.

## Output Rule

When reporting hardness, include:

```text
Hardness: H3 - price is in Entry zone but still needs reclaim/volume confirmation.
Next trigger: reclaim 78.80 and hold; invalid below 76.20.
```

Keep the reason numeric and tied to Entry, stop, TP, confirmation, or event risk.
