# Workspace Rules — AkShare 市场与期货监控 — 2025-09-10

## 目标
- 使用 **Python + AkShare** 获取 A 股/期货行情与基差/贴水等指标；
- 达到**可配置条件触发**：
  - 触发 **微信小程序**（或服务号/企业微信）的通知；
  - 生成/更新一个 **查询网页**（静态或轻后端）。

## 边界
- 尽量只读行情；不做实盘交易与投顾。

## 约束
- 定时/事件驱动统一使用 `APScheduler`（或 `cron + make task`）。
- 通知通道抽象为接口：`Notifier`（支持企业微信 Webhook、Server酱、飞书、短信可选）。
- 存储：本地 SQLite/Parquet 初期即可；接口封装以便后续替换。
- 配置：`.env` 与 `configs/app.yaml`；必须有示例与校验。
- 监控：Prometheus 指标 or 简版 CSV + Grafana 可选。

## 目录结构（建议）
```
akmon/
  src/
    akmon/
      collectors/     # AkShare 数据采集器
      indicators/     # 指标计算（基差/贴水率/均线/波动）
      rules/          # 触发规则（DSL/表达式）
      notifiers/      # 通知实现（wecom/feishu/email/...）
      web/            # FastAPI 或静态站点生成器
      miniapp/        # 小程序接口（云函数/HTTP）
      config.py
      app.py          # 入口：加载配置→调度→采集→计算→触发→通知
  configs/
    app.example.yaml
  docs/
    PRD.md
    API.md
  tests/
  Makefile
  .env.example
```

## 数据口径与校验
- **时间对齐**：统一时区 Asia/Shanghai；K线/分钟线落库需去重。
- **来源多样**：AkShare 为主；必要时加入冗余源并做一致性比对。

## 触发规则（例）
- IC 当月合约贴水率 \> X% 且成交量 \> N → 触发“套利观察”告警；
- 指定股票 5 分钟跌幅 \> Y% 且资金流出加速 → 推送提醒。

## 安全与速率
- AkShare/目标站点的频率限制需在 `collectors` 做节流与缓存；失败退避重试。

