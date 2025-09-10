# PRD — AkMon

## 1. 产品概述

### 1.1 产品名称
AkMon — AkShare驱动的期货监控与提醒系统

### 1.2 产品定位
专注于股指期货基差和贴水率监控的可视化分析平台，为量化交易员和研究人员提供实时数据采集、历史数据分析、预警通知和用户管理功能。

### 1.3 核心价值
- **实时监控**：通过AkShare接口获取IC期货实时数据，提供准确的基差和贴水率计算
- **历史分析**：支持过去5年历史数据分析，提供多时间窗口的百分位计算
- **可视化展示**：提供交互式图表，直观展示基差走势和百分位水平
- **智能预警**：支持自定义阈值设置，及时通知用户超阈值情况
- **用户管理**：提供完善的用户权限管理，支持多用户独立使用

### 1.4 技术架构
- **数据源**：AkShare金融数据接口
- **后端**：Python + FastAPI
- **前端**：Web界面（参考stock-analysis-demo布局）
- **数据库**：SQLite/Parquet
- **通知服务**：第三方邮件服务（SendGrid、Mailgun等）
- **任务调度**：APScheduler

## 2. 目标用户

### 2.1 主要用户
- **量化交易员**：需要实时监控期货基差变化，寻找套利机会
- **套利研究者**：研究期货基差的长期规律和统计特征
- **期货分析师**：分析期货市场走势和基差变化趋势

### 2.2 次要用户
- **程序化交易爱好者**：基于基差变化开发交易策略
- **金融数据分析师**：进行期货市场数据分析和研究

### 2.3 用户画像
- **专业程度**：中高级金融从业者
- **技术能力**：具备基本的计算机操作能力，了解金融数据
- **使用场景**：日常工作中的市场监控、研究分析、策略制定
- **痛点需求**：需要准确的基差数据、直观的可视化展示、及时的预警通知

## 3. 用户故事（节选）

### 3.1 核心用户故事
1. **作为量化交易员**，我希望能实时查看IC合约的基差走势，以便及时发现套利机会。
2. **作为套利研究者**，我希望能分析基差的历史百分位水平，了解当前基差在历史中的位置。
3. **作为期货分析师**，我希望能设置预警阈值，当基差超过特定范围时收到邮件通知。
4. **作为系统管理员**，我希望能管理用户权限，为不同用户配置不同的预警设置。
5. **作为数据分析师**，我希望能导出历史数据和分析结果，用于进一步的研究。

### 3.2 详细用户故事
1. **数据采集用户故事**
   - 我能配置一组品种与阈值，当满足条件时收到提醒。
   - 系统能自动从AkShare获取IC期货的实时数据。
   - 系统在接口异常/频率受限时，不会频繁报错并能自我恢复。

2. **可视化用户故事**
   - 我能打开网页随时查询最近1小时与当日的指标走势。
   - 我能看到IC合约基差的蜡烛图，包含开盘、收盘、最高、最低点位。
   - 我能看到基差在5年历史中的百分位水平变化趋势。
   - 我能看到贴水率在5年历史中的百分位水平变化趋势。
   - 我能通过图表交互功能（缩放、悬停、时间选择）深入了解数据。

3. **预警用户故事**
   - 我能设置基差和贴水率的预警阈值。
   - 我能选择预警的触发方向（上穿/下穿）。
   - 我能看到图表中用颜色标注的超阈值时间段。
   - 我能查看超阈值时间段的统计信息（交易日数量、占比等）。
   - 我能配置预警检查的频率（1分钟、5分钟、10分钟、30分钟、1小时）。

4. **通知用户故事**
   - 我能配置我的邮箱地址接收预警通知。
   - 我能收到包含详细预警信息的邮件通知。
   - 我能管理我的通知偏好设置。

5. **用户管理用户故事**
   - 作为管理员，我能创建和管理用户账号。
   - 作为管理员，我能设置用户的权限和访问级别。
   - 作为用户，我能管理我的个人信息和预警设置。

## 4. 验收标准（MDI#1-#5 对应）

### 4.1 数据采集验收标准
- **MDI#1**：本地一次采集→日志内出现指标与阈值判定结果。
- **MDI#2**：系统能正确获取IC期货的实时数据，包含所有必需字段。
- **MDI#3**：数据采集失败时，系统能自动重试并记录错误日志。

### 4.2 可视化验收标准
- **MDI#4**：网页 `/` 能看到最近50条记录与一张单品种曲线。
- **MDI#5**：三个图表能正确显示，包含基差走势、基差百分位、贴水率百分位。
- **MDI#6**：图表交互功能正常工作（缩放、悬停、时间选择）。

### 4.3 预警验收标准
- **MDI#7**：预警阈值设置功能正常工作。
- **MDI#8**：超阈值时间段能在图表中正确标注。
- **MDI#9**：预警统计信息计算准确。

### 4.4 通知验收标准
- **MDI#10**：邮件通知功能正常工作，能及时发送预警邮件。
- **MDI#11**：通知内容包含完整的预警信息。

### 4.5 用户管理验收标准
- **MDI#12**：用户注册和登录功能正常工作。
- **MDI#13**：管理员能正常管理用户权限。
- **MDI#14**：用户数据隔离正常工作，不同用户数据相互独立。

## 5. 功能需求详细描述

### 5.1 数据采集模块
- **数据源**：AkShare金融数据接口
- **支持品种**：IC、IF、IH等股指期货（可扩展）
- **数据字段**：开盘价、收盘价、最高价、最低价、成交量、成交金额
- **数据频率**：日线数据
- **数据计算**：
  - 基差 = 期货价格 - 中证500指数价格
  - 贴水率 = (期货价格 - 现货价格) / 现货价格 × 100%
- **数据存储**：SQLite/Parquet格式，支持历史数据查询

### 5.2 数据分析与计算模块
- **基差计算**：实时计算IC合约与中证500指数的基差
- **贴水率计算**：计算期货相对于现货的贴水率
- **百分位计算**：
  - 支持1年、3年、5年滚动窗口
  - 计算当前基差/贴水率在历史数据中的百分位位置
  - 提供百分位时间序列数据
- **统计分析**：
  - 计算超阈值时间段的交易日数量
  - 计算超阈值时间段占历史同期比例
  - 提供统计摘要信息

### 5.3 可视化展示模块
- **图1 - 基差走势图**：
  - 蜡烛图形式展示基差变化
  - 包含开盘、收盘、最高、最低点位
  - 支持时间范围选择
  - 超阈值时间段用颜色标注

- **图2 - 基差百分位图**：
  - 线图展示基差在5年历史中的百分位水平
  - Y轴：0-100%百分位
  - X轴：时间
  - 支持时间范围选择
  - 超阈值时间段用颜色标注

- **图3 - 贴水率百分位图**：
  - 线图展示贴水率在5年历史中的百分位水平
  - Y轴：0-100%百分位
  - X轴：时间
  - 支持时间范围选择
  - 超阈值时间段用颜色标注

- **交互功能**：
  - 图表缩放
  - 悬停显示数值
  - 时间范围选择器
  - 图表导出功能

### 5.4 预警系统模块
- **阈值设置**：
  - 支持基差阈值设置
  - 支持贴水率阈值设置
  - 支持上穿/下穿触发选择
  - 支持数值输入验证

- **检查频率**：
  - 1分钟、5分钟、10分钟、30分钟、1小时可选
  - 支持自定义检查时间

- **预警标注**：
  - 在图表中用颜色标注超阈值时间段
  - 显示超阈值的具体数值和时间
  - 提供超阈值统计信息

- **预警管理**：
  - 预警规则创建、编辑、删除
  - 预警历史记录查询
  - 预警状态管理（启用/禁用）

### 5.5 通知系统模块
- **邮件通知**：
  - 支持第三方邮件服务（SendGrid、Mailgun等）
  - 支持自定义邮件模板
  - 支持邮件发送状态跟踪

- **用户邮箱管理**：
  - 支持用户添加/删除邮箱地址
  - 支持邮箱验证
  - 支持通知偏好设置

- **通知内容**：
  - 包含预警详情（合约、阈值、触发时间、当前值）
  - 包含统计信息（超阈值天数、占比等）
  - 包含快速访问链接

### 5.6 用户管理模块
- **用户认证**：
  - 用户注册功能
  - 用户登录功能
  - 密码加密存储
  - 会话管理

- **权限管理**：
  - 管理员账号（网页端管理）
  - 普通用户权限
  - 数据访问权限控制
  - 功能权限控制

- **用户配置**：
  - 个人信息管理
  - 预警设置管理
  - 通知偏好设置
  - 数据导出权限

### 5.7 数据导出模块
- **导出格式**：
  - CSV格式
  - Excel格式
  - JSON格式

- **导出内容**：
  - 历史基差数据
  - 百分位数据
  - 预警记录
  - 统计分析结果

- **导出管理**：
  - 时间范围选择
  - 数据字段选择
  - 导出历史记录
  - 批量导出支持

## 6. UI/UX需求

### 6.1 界面布局
- **整体布局**：参考https://github.com/Pikady/stock-analysis-demo.git
- **页面结构**：
  - 顶部导航栏：包含Logo、用户信息、设置等
  - 侧边栏：合约选择、时间范围选择、预警设置等
  - 主内容区：三个图表垂直排列
  - 底部信息栏：系统状态、版权信息等

- **图表布局**：
  - 图1（基差走势图）：占据主内容区上部
  - 图2（基差百分位图）：占据主内容区中部
  - 图3（贴水率百分位图）：占据主内容区下部
  - 每个图表高度约300-400px，宽度自适应

### 6.2 交互设计
- **合约选择**：
  - 下拉菜单选择IC合约
  - 支持搜索过滤
  - 显示合约到期日信息

- **时间范围选择**：
  - 日期选择器
  - 快速选择按钮（今日、本周、本月、本年等）
  - 自定义时间范围

- **阈值设置**：
  - 文本框输入数值
  - 下拉选择触发方向（上穿/下穿）
  - 实时验证输入有效性

- **图表交互**：
  - 鼠标悬停显示详细数值
  - 滚轮缩放
  - 拖拽平移
  - 双击重置

### 6.3 响应式设计
- **桌面端**：完整功能展示
- **平板端**：适当调整布局，保持核心功能
- **移动端**：简化界面，重点展示关键信息

### 6.4 视觉设计
- **色彩方案**：
  - 主色调：蓝色系（专业、可信）
  - 警示色：红色（超阈值）
  - 背景色：浅灰色（减少视觉疲劳）

- **字体规范**：
  - 标题：使用无衬线字体，字号16-24px
  - 正文：使用易读字体，字号12-14px
  - 数据：使用等宽字体，便于对齐

## 7. 数据模型设计

### 7.1 合约信息表 (contracts)
```sql
CREATE TABLE contracts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_code VARCHAR(20) NOT NULL UNIQUE,  -- 合约代码，如IC2509
    contract_name VARCHAR(50),                  -- 合约名称
    underlying_index VARCHAR(20),               -- 标的指数，如中证500
    expiry_date DATE,                           -- 到期日
    contract_type VARCHAR(10),                 -- 合约类型，如IC/IF/IH
    is_active BOOLEAN DEFAULT TRUE,            -- 是否活跃
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7.2 基差数据表 (basis_data)
```sql
CREATE TABLE basis_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_code VARCHAR(20) NOT NULL,         -- 合约代码
    trade_date DATE NOT NULL,                   -- 交易日期
    open_price DECIMAL(10,2),                   -- 开盘价
    high_price DECIMAL(10,2),                   -- 最高价
    low_price DECIMAL(10,2),                    -- 最低价
    close_price DECIMAL(10,2),                  -- 收盘价
    volume BIGINT,                              -- 成交量
    amount DECIMAL(20,2),                       -- 成交金额
    basis_value DECIMAL(10,2),                  -- 基差值
    carry_rate DECIMAL(10,4),                   -- 贴水率
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(contract_code, trade_date)
);
```

### 7.3 百分位数据表 (percentile_data)
```sql
CREATE TABLE percentile_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contract_code VARCHAR(20) NOT NULL,         -- 合约代码
    trade_date DATE NOT NULL,                   -- 交易日期
    window_type VARCHAR(10) NOT NULL,           -- 窗口类型：1Y/3Y/5Y
    basis_percentile DECIMAL(10,4),             -- 基差百分位
    carry_rate_percentile DECIMAL(10,4),         -- 贴水率百分位
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(contract_code, trade_date, window_type)
);
```

### 7.4 用户表 (users)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,       -- 用户名
    email VARCHAR(100) NOT NULL UNIQUE,         -- 邮箱
    password_hash VARCHAR(255) NOT NULL,         -- 密码哈希
    full_name VARCHAR(100),                     -- 全名
    role VARCHAR(20) DEFAULT 'user',           -- 角色：admin/user
    is_active BOOLEAN DEFAULT TRUE,            -- 是否激活
    email_verified BOOLEAN DEFAULT FALSE,       -- 邮箱是否验证
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7.5 预警配置表 (alert_configs)
```sql
CREATE TABLE alert_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,                   -- 用户ID
    contract_code VARCHAR(20) NOT NULL,         -- 合约代码
    alert_type VARCHAR(20) NOT NULL,            -- 预警类型：basis/carry_rate
    threshold_value DECIMAL(10,2) NOT NULL,     -- 阈值
    trigger_direction VARCHAR(10) NOT NULL,     -- 触发方向：above/below
    check_frequency INTEGER NOT NULL,           -- 检查频率（分钟）
    is_active BOOLEAN DEFAULT TRUE,            -- 是否激活
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 7.6 预警记录表 (alert_history)
```sql
CREATE TABLE alert_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,                   -- 用户ID
    alert_config_id INTEGER NOT NULL,           -- 预警配置ID
    contract_code VARCHAR(20) NOT NULL,         -- 合约代码
    alert_type VARCHAR(20) NOT NULL,            -- 预警类型
    trigger_value DECIMAL(10,2) NOT NULL,       -- 触发值
    threshold_value DECIMAL(10,2) NOT NULL,     -- 阈值
    trigger_direction VARCHAR(10) NOT NULL,     -- 触发方向
    triggered_at TIMESTAMP NOT NULL,            -- 触发时间
    notification_sent BOOLEAN DEFAULT FALSE,   -- 通知是否已发送
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (alert_config_id) REFERENCES alert_configs(id)
);
```

## 8. API设计扩展

### 8.1 合约相关API

#### GET /api/contracts
获取可选择的合约列表

**请求参数**：
- `type`: 合约类型（可选，如IC/IF/IH）
- `active`: 是否活跃（可选，true/false）

**响应示例**：
```json
{
  "status": "success",
  "data": [
    {
      "contract_code": "IC2509",
      "contract_name": "中证500股指期货2509合约",
      "underlying_index": "中证500",
      "expiry_date": "2025-09-18",
      "contract_type": "IC",
      "is_active": true
    }
  ]
}
```

#### GET /api/contracts/{contract_code}
获取指定合约的详细信息

**响应示例**：
```json
{
  "status": "success",
  "data": {
    "contract_code": "IC2509",
    "contract_name": "中证500股指期货2509合约",
    "underlying_index": "中证500",
    "expiry_date": "2025-09-18",
    "contract_type": "IC",
    "is_active": true
  }
}
```

### 8.2 数据相关API

#### GET /api/basis-history
获取基差历史数据

**请求参数**：
- `contract_code`: 合约代码（必需）
- `start_date`: 开始日期（可选，格式：YYYY-MM-DD）
- `end_date`: 结束日期（可选，格式：YYYY-MM-DD）

**响应示例**：
```json
{
  "status": "success",
  "data": [
    {
      "trade_date": "2025-09-10",
      "open_price": 4500.0,
      "high_price": 4520.0,
      "low_price": 4480.0,
      "close_price": 4510.0,
      "volume": 10000,
      "amount": 45100000.0,
      "basis_value": -23.4,
      "carry_rate": -0.52
    }
  ]
}
```

#### GET /api/percentile
获取百分位数据

**请求参数**：
- `contract_code`: 合约代码（必需）
- `window_type`: 窗口类型（必需，1Y/3Y/5Y）
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）

**响应示例**：
```json
{
  "status": "success",
  "data": [
    {
      "trade_date": "2025-09-10",
      "basis_percentile": 25.5,
      "carry_rate_percentile": 30.2
    }
  ]
}
```

### 8.3 预警相关API

#### POST /api/alert-config
创建预警配置

**请求体**：
```json
{
  "contract_code": "IC2509",
  "alert_type": "basis",
  "threshold_value": -30.0,
  "trigger_direction": "below",
  "check_frequency": 5
}
```

**响应示例**：
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "user_id": 1,
    "contract_code": "IC2509",
    "alert_type": "basis",
    "threshold_value": -30.0,
    "trigger_direction": "below",
    "check_frequency": 5,
    "is_active": true
  }
}
```

#### GET /api/alert-configs
获取用户的预警配置列表

**响应示例**：
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "contract_code": "IC2509",
      "alert_type": "basis",
      "threshold_value": -30.0,
      "trigger_direction": "below",
      "check_frequency": 5,
      "is_active": true
    }
  ]
}
```

#### PUT /api/alert-configs/{id}
更新预警配置

#### DELETE /api/alert-configs/{id}
删除预警配置

#### GET /api/alert-history
获取预警历史记录

**请求参数**：
- `page`: 页码（可选，默认1）
- `limit`: 每页数量（可选，默认20）
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）

### 8.4 用户相关API

#### POST /api/user/register
用户注册

**请求体**：
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "full_name": "Test User"
}
```

#### POST /api/user/login
用户登录

**请求体**：
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**响应示例**：
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "full_name": "Test User",
      "role": "user"
    }
  }
}
```

#### GET /api/user/profile
获取用户信息

#### PUT /api/user/profile
更新用户信息

### 8.5 数据导出API

#### GET /api/export-data
导出数据

**请求参数**：
- `contract_code`: 合约代码（必需）
- `data_type`: 数据类型（必需，basis/percentile/alert）
- `start_date`: 开始日期（可选）
- `end_date`: 结束日期（可选）
- `format`: 导出格式（可选，csv/excel/json，默认csv）

**响应**：文件下载

## 9. 非功能需求

### 9.1 性能需求
- **响应时间**：
  - API响应时间 < 3秒
  - 页面加载时间 < 5秒
  - 图表渲染时间 < 2秒

- **并发处理**：
  - 支持100+并发用户
  - 数据采集任务不阻塞用户请求

- **数据处理**：
  - 支持5年历史数据的快速查询
  - 支持百万级数据量的统计分析

### 9.2 可靠性需求
- **系统可用性**：> 99%
- **数据准确性**：基差计算准确率100%
- **故障恢复**：
  - 数据采集失败自动重试
  - 系统崩溃后自动恢复
  - 数据备份和恢复机制

### 9.3 安全性需求
- **数据安全**：
  - 用户密码加密存储
  - 敏感数据传输加密
  - 数据访问权限控制

- **访问控制**：
  - 用户身份验证
  - API访问频率限制
  - 恶意请求防护

- **数据隐私**：
  - 用户数据隔离
  - 个人信息保护
  - 符合数据保护法规

### 9.4 可扩展性需求
- **功能扩展**：
  - 支持新增期货品种
  - 支持新增通知渠道
  - 支持新增数据源

- **性能扩展**：
  - 支持数据库水平扩展
  - 支持应用服务集群部署
  - 支持缓存机制优化

- **用户扩展**：
  - 支持用户数量增长
  - 支持多租户架构
  - 支持个性化配置

### 9.5 可维护性需求
- **代码质量**：
  - 代码覆盖率 > 80%
  - 代码规范符合PEP8
  - 模块化设计，低耦合高内聚

- **文档完善**：
  - API文档完整
  - 部署文档清晰
  - 用户手册详细

- **监控告警**：
  - 系统状态监控
  - 性能指标监控
  - 错误日志监控

## 10. 部署与运维需求

### 10.1 部署需求
- **环境要求**：
  - Python 3.8+
  - Node.js 14+（如使用前端框架）
  - SQLite/PostgreSQL
  - Redis（可选，用于缓存）

- **部署方式**：
  - Docker容器化部署
  - 支持云平台部署（AWS/阿里云/腾讯云）
  - 支持本地开发环境

- **配置管理**：
  - 环境变量配置
  - 配置文件管理
  - 敏感信息加密存储

### 10.2 运维需求
- **监控告警**：
  - 系统健康检查
  - 性能指标监控
  - 错误日志收集
  - 告警通知机制

- **日志管理**：
  - 结构化日志记录
  - 日志分级管理
  - 日志轮转和归档
  - 日志查询和分析

- **备份恢复**：
  - 定期数据备份
  - 备份文件加密
  - 恢复测试验证
  - 灾难恢复预案

### 10.3 升级维护
- **版本管理**：
  - 语义化版本控制
  - 版本兼容性保证
  - 升级脚本和说明

- **问题处理**：
  - 问题跟踪和分类
  - 紧急修复流程
  - 版本回滚机制

- **性能优化**：
  - 定期性能评估
  - 慢查询优化
  - 缓存策略优化
