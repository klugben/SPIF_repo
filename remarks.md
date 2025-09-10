
工作流:
二、给你一套“对标最佳实践”的改进版工作流（简版总览）

A. 对齐目标：一页纸问题陈述 + SLO/OKR → Spike 验证最大不确定性。

B. 文档即代码：README 草案 → PRD → ADR → API 契约（OpenAPI/Schema）。

C. 实现（循环）：选择一个 MDI → 写测试/契约 → 实现 → lint+type+test → 文档同步。

D. 可观测与发布：日志/指标/告警到位 → 打 Tag/灰度 → 回滚预案。

E. 复盘：每个里程碑 30 分钟，总结行动项写回 TODO.md。



五、如何在 Cursor + Cline + GLM4.5 下落地（速用清单）

把以上文件放入新仓库，按建议目录组织（docs/, src/, configs/, tests/…）。

在 Cline 的系统规则里粘贴《Global_rules_V4.md》的“强制习惯”段，并添加：

“先读 README_AkMon.md、PRD_AkMon.md、API_AkMon.md、workspace_rules_akshare.md、workspace_workflow_akshare.md、/src 目录，再写 TODO.md 并输出执行计划，未确认不准修改代码。”

第一轮让 AI 只做 MDI#1：

生成 src/akmon/app.py 骨架（读取配置 → 调 AkShare → 计算一个指标 → 控制台输出阈值判定）。

同时生成 tests/ 的最小用例（契约/边界值）。

确认后，才允许进入 MDI#2（定时 + 落库）和 MDI#3（企业微信通知）。

全程使用 make lint test run 的门禁命令，任何失败先修再继续。