# AkMon — AkShare驱动的期货监控与提醒系统

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-development-orange.svg)](https://github.com/yourusername/akmon)

AkMon是一个基于AkShare的期货监控与提醒系统，专注于股指期货基差和贴水率的实时监控、历史数据分析和智能预警。系统提供直观的可视化界面，支持多用户管理，为量化交易员和研究人员提供专业的市场分析工具。

## 🚀 功能特性

### 实时数据采集
- 📈 基于AkShare接口获取IC期货实时数据
- 📊 支持开盘价、收盘价、最高价、最低价、成交量、成交金额等完整字段
- 🔄 自动数据采集和更新机制
- 🛡️ 接口异常自动重试和错误恢复

### 多维度数据分析
- 📏 实时基差计算（期货价格 - 中证500指数价格）
- 📉 贴水率计算和分析
- 📈 支持1年、3年、5年滚动窗口的百分位计算
- 📊 超阈值时间段统计分析

### 交互式可视化
- 🕯️ 基差走势蜡烛图（包含开盘、收盘、最高、最低点位）
- 📊 基差5年百分位水平趋势图
- 📈 贴水率5年百分位水平趋势图
- 🔍 图表交互功能（缩放、悬停、时间范围选择）
- 🎨 超阈值时间段颜色标注

### 智能预警系统
- ⚡ 支持基差和贴水率阈值设置
- 🎯 灵活的触发方向选择（上穿/下穿）
- ⏰ 可配置的检查频率（1分钟、5分钟、10分钟、30分钟、1小时）
- 📈 图表中的超阈值时间段标注
- 📊 详细的超阈值统计信息

### 多渠道通知
- 📧 邮件通知功能（支持SendGrid、Mailgun等第三方服务）
- 🔔 用户自定义邮箱管理
- 📋 详细的预警信息内容
- ⚙️ 通知偏好设置

### 用户权限管理
- 👥 完整的用户注册和登录系统
- 🔐 管理员账号和权限管理
- 🛡️ 用户数据隔离保护
- ⚙️ 个性化配置管理

### 数据导出功能
- 📄 支持CSV、Excel、JSON多种格式导出
- 📊 历史数据、百分位数据、预警记录导出
- 📅 灵活的时间范围选择
- 📋 批量导出支持

## 🏗️ 系统架构

### 技术栈
- **后端**: Python + FastAPI
- **前端**: Web界面（参考[stock-analysis-demo](https://github.com/Pikady/stock-analysis-demo.git)布局）
- **数据库**: SQLite/Parquet
- **任务调度**: APScheduler
- **通知服务**: 第三方邮件服务（SendGrid、Mailgun等）
- **数据源**: AkShare金融数据接口

### 架构图
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   数据采集层     │    │   数据处理层     │    │   应用服务层     │
│                │    │                │    │                │
│  • AkShare API  │───▶│  • 基差计算     │───▶│  • FastAPI     │
│  • 数据清洗     │    │  • 贴水率计算   │    │  • 用户管理     │
│  • 错误处理     │    │  • 百分位计算   │    │  • 预警系统     │
│  • 重试机制     │    │  • 统计分析     │    │  • 通知服务     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   数据存储层     │    │   前端展示层     │    │   运维监控层     │
│                │    │                │    │                │
│  • SQLite       │    │  • Web界面      │    │  • 日志监控     │
│  • Parquet      │    │  • 交互图表     │    │  • 性能监控     │
│  • 数据备份     │    │  • 响应式设计   │    │  • 告警通知     │
│  • 数据恢复     │    │  • 用户体验     │    │  • 健康检查     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 数据流
```
AkShare API → 数据采集 → 数据清洗 → 基差计算 → 百分位分析 → 数据存储
    ↓
预警检查 → 阈值判断 → 触发通知 → 用户接收 → 界面展示 → 数据导出
```

## 📦 快速开始

### 环境要求
- Python 3.8+
- Node.js 14+ (如使用前端框架)
- Git

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/akmon.git
cd akmon
```

2. **创建虚拟环境**
```bash
make venv
```

3. **激活虚拟环境**
```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

4. **安装依赖**
```bash
make install
```

5. **配置环境**
```bash
cp .env.example .env
cp configs/app.example.yaml configs/app.yaml
```

6. **编辑配置文件**
```bash
# 编辑 .env 文件，设置必要的环境变量
nano .env

# 编辑 configs/app.yaml，配置应用参数
nano configs/app.yaml
```

7. **初始化数据库**
```bash
make init-db
```

8. **启动应用**
```bash
make run
```

### 访问应用
- **Web界面**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **管理员界面**: http://localhost:8000/admin

## 🔧 开发指南

### 项目结构
```
akmon/
├── src/
│   ├── akmon/
│   │   ├── collectors/     # 数据采集器
│   │   ├── indicators/     # 指标计算
│   │   ├── rules/          # 触发规则
│   │   ├── notifiers/      # 通知实现
│   │   ├── web/            # Web界面
│   │   ├── auth/           # 用户认证
│   │   ├── models/         # 数据模型
│   │   ├── api/            # API接口
│   │   ├── config.py       # 配置管理
│   │   └── app.py          # 应用入口
│   └── tests/              # 测试文件
├── configs/
│   ├── app.example.yaml    # 应用配置示例
│   └── database.yaml      # 数据库配置
├── docs/
│   ├── PRD.md             # 产品需求文档
│   ├── API.md             # API文档
│   └── DEPLOYMENT.md      # 部署文档
├── scripts/
│   ├── setup.sh           # 环境设置脚本
│   ├── deploy.sh          # 部署脚本
│   └── backup.sh          # 备份脚本
├── data/
│   ├── raw/               # 原始数据
│   ├── processed/         # 处理后数据
│   └── exports/           # 导出数据
├── tests/
│   ├── unit/              # 单元测试
│   ├── integration/       # 集成测试
│   └── e2e/               # 端到端测试
├── .env.example           # 环境变量示例
├── requirements.txt       # Python依赖
├── package.json           # Node.js依赖
├── Dockerfile            # Docker配置
├── docker-compose.yml    # Docker Compose配置
├── Makefile              # 构建脚本
└── README.md             # 项目说明
```

### 开发环境设置

1. **安装开发依赖**
```bash
pip install -r requirements-dev.txt
```

2. **运行测试**
```bash
make test
```

3. **代码格式化**
```bash
make format
```

4. **代码检查**
```bash
make lint
```

### 可用命令
```bash
make help          # 显示所有可用命令
make venv          # 创建虚拟环境
make install       # 安装依赖
make run           # 启动应用
make test          # 运行测试
make lint          # 代码检查
make format        # 代码格式化
make clean         # 清理临时文件
make build         # 构建应用
make deploy        # 部署应用
make backup        # 备份数据
make restore       # 恢复数据
```

## 📊 使用指南

### 基本使用流程

1. **用户注册/登录**
   - 访问Web界面
   - 注册新账号或使用现有账号登录
   - 验证邮箱地址

2. **选择合约**
   - 在侧边栏选择IC合约
   - 查看合约详细信息
   - 选择时间范围

3. **查看数据**
   - 查看基差走势蜡烛图
   - 分析基差百分位趋势
   - 分析贴水率百分位趋势
   - 使用图表交互功能深入了解数据

4. **设置预警**
   - 配置基差或贴水率阈值
   - 选择触发方向（上穿/下穿）
   - 设置检查频率
   - 配置通知邮箱

5. **导出数据**
   - 选择导出格式
   - 设置时间范围
   - 下载导出文件

### 高级功能

#### 管理员功能
- 用户管理：创建、编辑、删除用户
- 权限管理：设置用户权限和访问级别
- 系统监控：查看系统状态和性能指标
- 数据管理：数据备份、恢复、清理

#### 预警管理
- 创建多个预警规则
- 设置不同的检查频率
- 查看预警历史记录
- 分析预警触发统计

#### 数据分析
- 多时间窗口分析
- 自定义指标计算
- 批量数据处理
- 自定义报表生成

## 🚀 部署指南

### Docker部署

1. **构建镜像**
```bash
docker build -t akmon .
```

2. **运行容器**
```bash
docker run -d -p 8000:8000 --name akmon akmon
```

### Docker Compose部署

1. **启动服务**
```bash
docker-compose up -d
```

2. **查看状态**
```bash
docker-compose ps
```

### 云平台部署

#### AWS部署
```bash
# 使用ECS
aws ecs create-cluster --cluster-name akmon
aws ecs register-task-definition --family akmon --cli-input-json file://task-definition.json
aws ecs create-service --cluster akmon --service-name akmon --task-definition akmon --desired-count 1
```

#### 阿里云部署
```bash
# 使用容器服务
aliyun cs POST /clusters --header "Content-Type=application/json" --body "$(cat cluster.json)"
aliyun cs POST /services --header "Content-Type=application/json" --body "$(cat service.json)"
```

## 🔧 配置说明

### 环境变量配置
```bash
# .env
DATABASE_URL=sqlite:///akmon.db
SECRET_KEY=your-secret-key-here
AKSHARE_API_KEY=your-akshare-api-key
SENDGRID_API_KEY=your-sendgrid-api-key
MAILGUN_API_KEY=your-mailgun-api-key
REDIS_URL=redis://localhost:6379/0
```

### 应用配置
```yaml
# configs/app.yaml
timezone: Asia/Shanghai
symbols:
  - type: future
    code: IC
    rule: "carry_rate < -1.0 and volume > 5000"
  - type: stock
    code: 600519
    rule: "pct_change_5m < -1.5 and outflow_rate > 0.8"
scheduler:
  interval_seconds: 60
notifier:
  type: wecom
  webhook_url: "https://qyapi.weixin.qq.com/robot/send?key=REPLACE_ME"
storage:
  type: sqlite
  dsn: "sqlite:///akmon.db"
```

## 📈 API文档

### 认证
所有API请求都需要在Header中包含认证token：
```
Authorization: Bearer <your-access-token>
```

### 主要接口

#### 获取合约列表
```http
GET /api/contracts
```

#### 获取基差历史数据
```http
GET /api/basis-history?contract_code=IC2509&start_date=2025-01-01&end_date=2025-12-31
```

#### 获取百分位数据
```http
GET /api/percentile?contract_code=IC2509&window_type=5Y
```

#### 创建预警配置
```http
POST /api/alert-config
Content-Type: application/json

{
  "contract_code": "IC2509",
  "alert_type": "basis",
  "threshold_value": -30.0,
  "trigger_direction": "below",
  "check_frequency": 5
}
```

#### 导出数据
```http
GET /api/export-data?contract_code=IC2509&data_type=basis&format=csv
```

完整的API文档请访问：http://localhost:8000/docs

## 🤝 贡献指南

### 开发流程

1. **Fork项目**
   ```bash
   # Fork项目到您的GitHub账号
   # 克隆您的fork
   git clone https://github.com/yourusername/akmon.git
   cd akmon
   ```

2. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **开发功能**
   ```bash
   # 编写代码
   # 添加测试
   # 更新文档
   ```

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建Pull Request**
   - 在GitHub上创建PR
   - 填写PR模板
   - 等待代码审查

### 代码规范

- 遵循PEP 8代码规范
- 使用类型注解
- 编写单元测试
- 更新相关文档

### 提交规范
使用Conventional Commits格式：
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式化
refactor: 代码重构
test: 测试相关
chore: 构建或辅助工具变动
```

## 📄 许可证

本项目采用MIT许可证。详情请参阅[LICENSE](LICENSE)文件。

## 🙏 致谢

- [AkShare](https://github.com/akfamily/akshare) - 金融数据接口
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Web框架
- [stock-analysis-demo](https://github.com/Pikady/stock-analysis-demo.git) - 界面设计参考
- [SendGrid](https://sendgrid.com/) - 邮件服务
- [Mailgun](https://www.mailgun.com/) - 邮件服务

## 📞 联系我们

- **项目主页**: https://github.com/yourusername/akmon
- **问题反馈**: https://github.com/yourusername/akmon/issues
- **邮件联系**: your-email@example.com
- **文档**: https://akmon.readthedocs.io

## 📊 项目状态

- [x] 需求分析
- [x] 系统设计
- [ ] 数据采集模块开发
- [ ] 数据分析模块开发
- [ ] 可视化模块开发
- [ ] 预警系统开发
- [ ] 通知系统开发
- [ ] 用户管理开发
- [ ] 前端界面开发
- [ ] 测试编写
- [ ] 文档完善
- [ ] 部署上线

---

**AkMon** - 让期货监控更简单，让投资决策更明智！
