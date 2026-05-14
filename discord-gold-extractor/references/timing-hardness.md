# Gold Timing Hardness Standard

Hardness measures how executable the current XAUUSD/GC1 setup is. Gold must be graded from gold report samples: base range, support/resistance, breakout/breakdown confirmation, Opus/GPT agreement, and event no-trade windows. Do not reuse stock-style BUY/HOLD logic.

## Required Evidence

Use the latest gold daily/weekly reports as the sample shape:

- current XAUUSD and, when possible, GC1 price
- base range and mid-zone
- support and resistance clusters
- upside confirmation and downside confirmation levels
- scenario probabilities or base/upside/downside cases
- Opus/GPT agreement or material divergence
- event calendar and no-trade windows: CPI, PPI, NFP, FOMC, Fed speakers, geopolitical shock
- entry, stop, TP levels if the report provides an intraday card

## Hard Gates

- If price is in the middle of the base range, grade `H0` or `H1`; do not force a trade.
- If a report-defined no-trade event window is active, grade `H0` unless the user asks only for scenario monitoring.
- If the relevant support/resistance or breakout level has not been reached, cap at `H2`.
- If confirmation is missing, cap at `H2`.
- If Opus and GPT disagree materially, cap at `H3` unless price action confirms one side.
- If stop/invalidation is missing for an intraday trade plan, cap at `H2`.

## Grades

| Grade | Meaning | Gold sample mapping |
|---|---|---|
| `H0` | No trade | Middle of range, event no-trade window, invalidated level, or no usable current price. |
| `H1` | Scenario only | Directional bias exists, but current price is not near a tradable support/resistance/trigger. |
| `H2` | Wait for confirmation | Price is near a key level, but no reclaim/rejection/close/retest evidence yet, or event risk is elevated. |
| `H3` | Light execution | Level is valid and partial confirmation exists, but model disagreement, wide stop, or session risk argues for reduced size. |
| `H4` | Actionable | Price is at the level, confirmation exists, event rules allow trading, stop is defined, and reward/risk is acceptable. |
| `H5` | Rare high-quality tactical setup | H4 plus Opus/GPT agreement, daily/weekly alignment, completed retest or strong rejection/reclaim, clean stop, and no near event risk. |

## Scenario Mapping

- `range trade`: H0 in the middle of the range; H3-H4 only near support/resistance after reclaim/rejection.
- `upside confirmation`: H2 before the confirmation level breaks; H4 after close/hold above and retest; H1 if price has already extended into target.
- `downside confirmation`: H2 before trigger; H4 after close/hold below and failed retest.
- `震荡偏多` or `震荡偏空`: H1-H2 by itself; upgrade only when price reaches the actionable level.
- `event trade`: H0 during no-trade window; H2 after event until spread/volatility normalizes; H3-H4 only when the report's post-event trigger confirms.

## Output Rule

When reporting hardness, include:

```text
Hardness: H3 - price is testing support and reclaim started, but CPI window keeps size light.
Level that changes verdict: hold above 2348 for H4; lose 2336 to H0.
```

Keep the reason tied to the exact gold level, scenario, confirmation, event rule, and invalidation.
