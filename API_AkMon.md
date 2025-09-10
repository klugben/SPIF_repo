# API 契约（草案）

## GET /api/latest?symbol=IC&window=1h
- 200: `{"symbol":"IC","basis":-23.4,"carry_rate":-1.2,"ts":"2025-09-10T10:12:00+08:00"}`

## GET /api/history?symbol=IC&start=...&end=...
- 200: 时间序列列表
