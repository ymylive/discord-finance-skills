# US Stock Discord Extraction Workflow

## Channel Map

- Daily index: `#美股-日常更新`, channel `1489576184978079845`
- Individual reports: links inside daily messages, usually under `#美股个股研报`
- Avoid by default: `#美股状态看板`

## Extraction Notes

Discord desktop caches API responses under:

```text
~/Library/Application Support/discord/Cache/Cache_Data
```

Cache entries contain the request URL followed by gzip-compressed JSON. Search for:

```text
https://discord.com/api/v9/channels/
```

Then find the following gzip header `\x1f\x8b` and decompress with:

```python
zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(blob[pos:])
```

Use `scripts/cache_dump.py --channel <id>` to dump cached messages. If a thread is missing latest messages, open:

```text
discord://-/channels/<server_id>/<thread_or_channel_id>
```

Then dump the cache again.

## PDF Parsing

Download attachments from the message `attachments[].url` and run:

```bash
pdftotext -layout report.pdf report.txt
```

Search text for:

```text
判定
入场区间
ENTRY
Entry
触发条件
失效条件
SL
TP1
TP2
WAIT_PULLBACK
ENTER_NOW
WAIT_BREAKOUT
```

## Decision Logic

1. Exclude latest `PASS`, `HOLD`, `SELL`, and `NOT_YET`.
2. Keep `BUY + ENTER_NOW` as the cleanest group, but still check whether current price has moved above the published entry range.
3. For `BUY + WAIT_PULLBACK`, promote only if the live price has reached the timing entry zone.
4. For `WAIT_BREAKOUT`, require breakout and retest; do not call it a current buy point from price alone.

## Lessons From Prior Runs

- Daily index can be complete while thread details are stale; open threads if missing.
- Embed research zones can be wider than timing PDF entries; timing PDF wins.
- A ticker can remain `BUY` fundamentally while no longer being attractive tactically.
