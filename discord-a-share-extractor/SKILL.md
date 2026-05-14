---
name: discord-a-share-extractor
description: Extract A-share research and timing updates from private Discord finance channels, parse attached A股 report PDFs, compare report entry levels with Eastmoney quotes, and identify stocks currently at or near buy levels. Use when the user asks to analyze Discord A股日常更新, A股个股研报, A-share reports, timing reports, buy zones, or latest A股 status from Discord.
---

# Discord A-Share Extractor

## Core Workflow

1. Use `#a股-日常更新` as the daily index and `#a股个股研报` threads as the source of truth.
2. Do not use `#a股状态看板` unless the user explicitly asks for it.
3. Extract the daily index from Discord cache, then open all relevant thread deep links once to force Discord to cache the latest 05-10/05-11 style thread messages. This avoids stale daily-list verdicts.
4. Re-read local Discord cache after thread loading. For each six-digit code, keep the latest `深度研究` and latest `择时分析`.
5. Download attached PDFs and convert with `pdftotext -layout`. Timing PDFs often contain stricter Entry 1 / Entry 2 than the embed summary.
6. Pull current A-share quotes from Eastmoney. Use `secid=1.<code>` for Shanghai/STAR codes beginning with `6`, and `secid=0.<code>` for Shenzhen/ChiNext codes beginning with `0` or `3`.
7. Classify only latest `research=BUY` names as buy candidates. Keep HOLD/SELL/NOT_YET in the full extraction table but do not promote them as buy points.
8. Run a second-pass timing re-analysis for every `已到位`, `接近`, or `研究区间内` candidate. The final answer must say whether it is still worth entering now, not merely that price is near the old entry level.

## Candidate Rules

Promote candidates only when the price and report agree:

- `已到位`: current price is in or below the timing entry zone.
- `研究区间内`: current price is inside the research entry zone, but timing asks for a slightly better pullback.
- `需企稳`: price has fallen below entry or close to stop, so wait for stabilization before treating it as actionable.
- `等突破`: timing says `WAIT_BREAKOUT`; require breakout and retest.
- `排除`: latest research is HOLD/SELL or timing is NOT_YET.

When in doubt, prefer the timing PDF over the research embed summary.

## Second-Pass Timing Verdicts

After the first screen, assign one of these conclusions:

- `仍可入场`: price is in the timing entry zone, above invalidation, and reward/risk is still reasonable.
- `轻仓试探`: setup is valid but only marginal; use reduced size due to incomplete confirmation or wide stop.
- `等确认`: price reached the zone but there is no stabilization, volume contraction, or reversal signal yet.
- `放弃`: price has broken the stop/invalidation, moved too close to TP1, or no longer offers acceptable reward/risk.
- `追高不入`: price has rebounded above the entry window before execution.

## Eastmoney Quote Pattern

Use this endpoint for batches:

```text
https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f12,f14,f2,f3,f4,f17,f18,f15,f16,f5,f6,f124&secids=1.600030,0.300059
```

Fields:

- `f12`: code
- `f14`: name
- `f2`: latest price
- `f3`: percent change
- `f18`: previous close
- `f124`: Unix timestamp

Retry in small batches if Eastmoney closes the connection.

## Output Shape

Produce:

1. quote timestamp
2. current candidates table
3. excluded/latest-HOLD notes if relevant
4. local Markdown or CSV file when the user asks for all rows

## References

- For detailed extraction steps, read `references/workflow.md`.
- For second-pass timing checks, read `references/reanalysis-checklist.md`.
- For a compact output template, read `references/output-template.md`.
