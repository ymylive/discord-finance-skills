# A-Share Discord Extraction Workflow

## Channel Map

- Daily index: `#a股-日常更新`, channel `1489576520849555497`
- Individual reports: `#a股个股研报` threads
- Avoid by default: `#a股状态看板`

## Thread Refresh

The daily index can show a code with an older verdict if the thread has since updated. For a reliable run:

1. Parse the daily index and collect all thread IDs.
2. Open each thread deep link once:

```text
discord://-/channels/1470575198901375172/<thread_id>
```

3. Re-read the Discord cache.
4. Keep the latest thread-level `深度研究` and `择时分析` messages.

## Quote Source

Use Eastmoney for live A-share quotes.

Batch endpoint:

```text
https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f12,f14,f2,f3,f4,f17,f18,f15,f16,f5,f6,f124&secids=1.600030,0.300059
```

Rules:

- `1.<code>` for Shanghai and STAR: codes beginning with `6`
- `0.<code>` for Shenzhen and ChiNext: codes beginning with `0` or `3`
- If the endpoint closes the connection, retry in batches of 8 or single-stock `qt/stock/get`.

## PDF Fields

Search timing PDFs for:

```text
ENTRY 1
ENTRY 2
入场
回踩
突破
SL
止损
TP1
TP2
触发条件
失效条件
```

## Decision Logic

1. Promote only latest `research=BUY` names.
2. Demote latest `HOLD`, even if an older daily index said `BUY`.
3. For `WAIT_PULLBACK`, compare live price with Entry 1/2, not only the research entry zone.
4. For `WAIT_BREAKOUT`, require breakout/retest confirmation.
5. If price is below entry and near stop, mark `需企稳` instead of `已到位`.

## Prior Run Lessons

- 2026-05-10 thread data changed several old BUY names to HOLD.
- A full run should open all 74+ threads once before final classification.
- Candidate output should be short; put all rows in a local Markdown or CSV file.
