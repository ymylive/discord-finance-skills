# Gold Discord Extraction Workflow

## Channel Map

- Opus daily/weekly: `黄金-研报-opus`, channel `1501911797148684338`
- GPT daily/weekly: `黄金-研报-gpt`, channel `1501911798264369303`
- Review channels: use only if the user asks for replay, validation, or backtest context.

## Extraction Steps

1. Dump the latest messages from both gold report channels.
2. Keep the latest daily and weekly report from each model.
3. Download attached PDFs if the embed is truncated.
4. Convert PDFs with `pdftotext -layout`.
5. Extract bias, base range, key levels, macro drivers, and scenario probabilities.
6. Reconcile Opus/GPT:
   - GPT often provides cleaner scenario levels.
   - Opus often explains the dominant macro driver shift.
   - The final summary should focus on overlapping actionable levels.

## Gold-Specific Framing

Do not force gold into stock-style `BUY/HOLD` categories. Use scenario language:

- `base case`
- `upside confirmation`
- `downside confirmation`
- `range trade`
- `no-trade mid-zone`
- `event risk`

Gold reports frequently require conditional execution around CPI/PPI/NFP/FOMC. Always preserve time windows and event no-trade restrictions.

## Useful Search Terms

```text
未来1-3日判断
本周判断
震荡
震荡偏多
震荡偏空
转多确认
转空确认
上方
下方
支撑
阻力
基准情景
概率
失守
站上
突破
破位
禁交易
NFP
CPI
PPI
FOMC
```
