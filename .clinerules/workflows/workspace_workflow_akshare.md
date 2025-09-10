# Workspace Workflow — AkShare 监控项目 — 2025-09-10

## MDI#1：命令行跑通 + 本地日志
- 产出：
  - `src/akmon/app.py`：从配置读入目标、采集一次、计算一个指标、按阈值触发日志提示。
  - `configs/app.example.yaml`：示例含一个股票与一个期货指标。

## MDI#2：定时任务与持久化
- 增量：APScheduler 每 1 分钟采一次分钟线；存 SQLite/Parquet；失败重试。

## MDI#3：通知打通
- 实现 `notifiers/wecom.py`（企业微信机器人 Webhook）；用环境变量注入 URL。
- 验证：当阈值满足时在群里接收到消息。

## MDI#4：查询网页
- FastAPI + Jinja2 输出静态表格与近期图；或导出 `docs/site/` 纯静态页面。
- 提供 `/api/latest` 返回 JSON，前端用 fetch 渲染。

## MDI#5：小程序联动（二选一）
- A. 云开发/云函数：提供 HTTPS 接口，小程序请求触发查询。
- B. 服务号/企业微信：关键字命令返回最新指标。

## CI/CD
- GitHub Actions：`lint + type + test`；可选打包 Docker 镜像。
- 发布：打 Tag 同步生成 `docs/site/`（GitHub Pages/OSS）。
