---
name: discord-us-stock-extractor
description: Extract US stock research and timing updates from private Discord finance channels, parse attached report PDFs, compare report entry levels with current market prices, and identify tickers currently at or near buy levels. Use when the user asks to analyze Discord 美股日常更新, 美股个股研报, US stock reports, timing reports, buy zones, timing hardness, or latest stock status from Discord.
---

# Discord US Stock Extractor

## Core Workflow

1. Open or inspect Discord only as a read-only source. Do not send messages, react, edit, or rely on Discord status-board channels unless the user explicitly asks for them.
2. Use `#美股-日常更新` as the daily index and individual stock threads as the source of truth.
3. Prefer local Discord cache extraction over manual clicking when possible. Run `scripts/cache_dump.py` to inspect cached API payloads, then open missing thread deep links in Discord to force the client to cache the newest messages.
4. For each ticker, pair the latest `深度研究` report with the latest `择时分析` report from the same or newest available date.
5. Download attached PDFs when available and convert them with `pdftotext -layout`. Use the embed summary only as a fallback.
6. Compare:
   - research verdict: `BUY`, `HOLD`, `PASS`, `SELL`
   - timing verdict: `ENTER_NOW`, `WAIT_PULLBACK`, `WAIT_BREAKOUT`, `NOT_YET`
   - research entry zone
   - timing Entry 1 / Entry 2, stop loss, TP levels
   - latest price
7. Classify tickers conservatively. A clean candidate usually needs `research=BUY` and current price inside or below the research/timing entry zone. Treat `WAIT_PULLBACK` as actionable only if the price has actually pulled back into the specified entry zone.
8. Run a second-pass timing re-analysis for every `已到位` or `接近` ticker before presenting it as actionable. Do not stop at "price touched the entry zone"; decide whether the setup is still worth entering now.

## Source Priorities

Use the sources in this order:

1. Individual ticker thread latest PDF, especially `*_timing_*`.
2. Individual ticker thread latest embed summary.
3. `#美股-日常更新` daily index.
4. Current external quote source.

Avoid `#美股状态看板` unless the user explicitly requests it; it can lag or use different assumptions.

## Price Checks

Use current market data because prices are unstable. Prefer `web.finance` for US equities. If a ticker is not covered, use a current finance page/search result and state the quote timestamp/source.

When the market is closed, label the quote as latest regular-market, post-market, or pre-market if known.

## Output Shape

Give a short methodology line, then a table:

| Ticker | Price | Research | Timing | Entry / Zone | Status |
|---|---:|---|---|---|---|

Use these status labels:

- `已到位`: research BUY and current price is in/under the timing entry zone.
- `接近`: price is within about 1-3% of the timing entry or inside research zone but not ideal timing.
- `等回调`: BUY thesis remains, but price is above timing entry.
- `等突破`: timing report requires breakout/retest confirmation.
- `剔除`: latest research is HOLD/PASS/SELL or timing is NOT_YET.

For all `已到位` and `接近` rows, add a second-pass conclusion:

- `仍可入场`: price is still in the valid entry window, invalidation has not triggered, and reward/risk remains acceptable.
- `轻仓试探`: valid but marginal because price is near the top of the zone, volatility is high, or confirmation is incomplete.
- `等确认`: price reached the zone but needs stabilization, breakout retest, volume contraction, or candle confirmation.
- `放弃`: stop/invalidation has triggered, price has already reached TP1, or reward/risk has collapsed.
- `追高不入`: price is above the intended entry window.

When the user asks for timing hardness, grade the setup with `H0`-`H5` using `references/timing-hardness.md`.

Always include a brief financial-risk caveat.

## References

- For implementation details and examples, read `references/workflow.md`.
- For second-pass timing checks, read `references/reanalysis-checklist.md`.
- For US stock timing hardness grading, read `references/timing-hardness.md`.
- For output wording and known field names, read `references/output-template.md`.
