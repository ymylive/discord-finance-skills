---
name: discord-gold-extractor
description: Extract gold daily and weekly reports from private Discord finance channels, reconcile Opus and GPT model views, summarize XAUUSD/GC1 bias, key levels, scenarios, triggers, invalidation rules, and trade-plan constraints. Use when the user asks for Discord 黄金研报, gold reports, XAUUSD analysis, daily/weekly gold summaries, or gold trading levels from Discord.
---

# Discord Gold Extractor

## Core Workflow

1. Use the gold research channels as the source of truth:
   - `黄金-研报-opus`: channel `1501911797148684338`
   - `黄金-研报-gpt`: channel `1501911798264369303`
   - gold replay/review channels when the user asks for review or backtest context.
2. Extract the latest daily and weekly messages from Discord cache with `scripts/cache_dump.py`. Open the Discord channel if the latest message is missing.
3. Download attached PDFs and convert them with `pdftotext -layout` when the embed summary is not enough.
4. Reconcile model views:
   - Opus often emphasizes macro/news causality and dominant driver shifts.
   - GPT often gives cleaner scenario probabilities and levels.
   - If they disagree, present both and state the common actionable overlap.
5. Summarize gold as scenarios, not as a single stock-style buy zone.

## Required Summary Fields

Always extract:

- report date and model
- 1-3 day or weekly bias: `震荡`, `震荡偏多`, `震荡偏空`, `转多`, `转空`
- base range
- upside confirmation levels
- downside confirmation levels
- support/resistance clusters
- macro drivers
- invalidation triggers
- no-trade zones and event restrictions

For intraday decision cards, also extract:

- event calendar and killzone
- plan A/B/C
- entry, stop, TP1/TP2/TP3
- risk percentage and position-size adjustment
- time-based cancellation rules

## Output Shape

Use a concise structure:

1. `结论`: one sentence.
2. `共同区间`: base range and chop/no-trade zone.
3. `转多条件`: levels and required confirmation.
4. `转空条件`: levels and required confirmation.
5. `执行`: what to do near support/resistance, and when not to trade.
6. `分歧`: Opus vs GPT if material.

## References

- For the latest extracted gold summary pattern, read `references/gold-summary.md`.
- For the detailed workflow and channel map, read `references/workflow.md`.
