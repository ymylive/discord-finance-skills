# A-Share Timing Hardness Standard

Hardness measures how executable the current A-share timing setup is. It is not the same as research conviction; grade it only after refreshing Eastmoney quotes and running the second-pass timing re-analysis.

## Required Evidence

Use the latest A-share timing PDF/embed as the sample shape:

- latest research verdict: BUY, HOLD, SELL
- timing verdict: ENTER_NOW, WAIT_PULLBACK, WAIT_BREAKOUT, NOT_YET
- Entry 1 / Entry 2 or entry zone
- stop loss or structural invalidation
- TP1 / TP2
- Eastmoney latest price, percent change, and quote timestamp
- intraday context if available: gap, high/low, limit-up/down, sharp selloff, sector/index pressure

## Hard Gates

- If current price is below stop or structural invalidation, grade `H0`.
- If latest research is HOLD/SELL or timing is NOT_YET, cap at `H1`.
- If price has rebounded more than about 2% above Entry 1 before execution, cap at `H2` unless the report allows breakout/retest entry.
- If price is at or near TP1, cap at `H1`.
- If Entry, stop, or Eastmoney timestamp is missing, cap at `H2`.
- If the stock is limit-up/limit-down or liquidity is distorted, cap at `H2` for fresh entries.

## Grades

| Grade | Meaning | A-share sample mapping |
|---|---|---|
| `H0` | Invalid / no trade | Stop broken, latest HOLD/SELL, NOT_YET, or limit/liquidity state makes entry impossible. |
| `H1` | Thesis only | BUY thesis exists, but price is far from timing entry, near TP1, or core timing fields are missing. |
| `H2` | Soft watch | Price is close to Entry 1/2 or inside research zone, but no stabilization, close confirmation, or acceptable reward/risk yet. |
| `H3` | Conditional entry | Price is in the timing zone, stop is intact, reward/risk is acceptable, but A-share intraday volatility or confirmation is imperfect. |
| `H4` | Actionable | Price is in the entry window, stop is clean, TP1 reward/risk is usually `>= 1.5`, no limit distortion, and price action has stabilized. |
| `H5` | Rare high-quality tactical entry | H4 plus fresh quote, sector/index support, clean pullback or retest, clear invalidation, and reward/risk usually `>= 2.0`. |

## Verdict Mapping

- `ENTER_NOW`: H4 if price remains inside the stated entry window and not in distorted limit behavior; H3 if confirmation is weaker.
- `WAIT_PULLBACK`: H4 only after price reaches Entry 1/2 and shows stabilization; H2-H3 if it is below Entry 2 but above stop; H0 if stop breaks.
- `WAIT_BREAKOUT`: H2 before breakout; H4 only after breakout plus retest or close confirmation.
- `研究区间内`: usually H2-H3 because research zones are wider than timing entries.
- `需企稳`: H2 until stabilization/reclaim appears; upgrade only after evidence.
- `追高不入` or `放弃`: H0-H1 even if the fundamental research is BUY.

## Output Rule

When reporting hardness, include:

```text
Hardness: H2 - price is below Entry 2 but above stop; wait for stabilization.
Next trigger: reclaim Entry 2 or close back above Entry 1; invalid below stop.
```

Keep the reason tied to Eastmoney price, Entry, stop, TP, confirmation, or market microstructure.
