# A-Share Output Template

Start with:

```text
我按 #a股-日常更新 + 个股线程/PDF 提取，未使用 a股状态看板。东方财富行情快照时间：...
```

Candidate table:

| 代码 | 名称 | 现价 | 研究 | 择时 | Entry / Zone | 判断 |
|---|---|---:|---|---|---|---|
| 300014 | 亿纬锂能 | 66.41 | BUY | WAIT_PULLBACK | Entry 67.5 / SL 62 | 已回踩到首档下方，需企稳 |

Preferred labels:

- `已到位`
- `研究区间内`
- `接近`
- `需企稳`
- `等突破`
- `排除`

If all rows are requested, write a Markdown file and include:

- source channel
- quote timestamp
- number of threads
- candidate table
- full extraction table
