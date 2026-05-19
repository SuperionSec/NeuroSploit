# NeuroSploit v3.2.4 完整功能清单

## 目录
1. [系统概览](#系统概览)
2. [后端API接口](#后端api接口)
3. [前端页面功能](#前端页面功能)
4. [数据模型结构](#数据模型结构)
5. [页面流转与导航](#页面流转与导航)
6. [核心工作流程](#核心工作流程)
7. [功能关联性分析](#功能关联性分析)
8. [核心模块架构](#核心模块架构)
9. [各页面布局结构分析](#各页面布局结构分析)
10. [参数来源与关联性分析](#参数来源与关联性分析)
11. [代码与文档一致性检查](#代码与文档一致性检查)
12. [完整功能测试计划](#完整功能测试计划)
13. [Providers与Settings大模型配置区别](#providers与settings大模型配置区别)

---

## 系统概览

NeuroSploit v3.2.4 是一个 AI 驱动的渗透测试平台，具有以下核心特性：
- 自动化 AI 安全代理
- 多种漏洞检测模式
- Kali Linux 沙箱隔离
- 智能 LLM 路由 (Smart Router)
- 知识增强 (RAG)
- 全面的报告生成

---

## 后端API接口

### 1. 扫描管理 (Scans API)
**路径前缀**: `/api/v1/scans`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 获取扫描列表，支持分页和状态过滤 | HomePage, ScanDetailsPage |
| POST | `/` | 创建新扫描 | NewScanPage |
| GET | `/{scan_id}` | 获取单个扫描详情 | ScanDetailsPage |
| POST | `/{scan_id}/start` | 启动扫描 | ScanDetailsPage |
| POST | `/{scan_id}/stop` | 停止运行中的扫描 | ScanDetailsPage |
| POST | `/{scan_id}/pause` | 暂停运行中的扫描 | ScanDetailsPage |
| POST | `/{scan_id}/resume` | 恢复暂停的扫描 | ScanDetailsPage |
| DELETE | `/{scan_id}` | 删除扫描 | ReportsPage |
| GET | `/{scan_id}/endpoints` | 获取扫描发现的端点 | ScanDetailsPage |
| GET | `/{scan_id}/vulnerabilities` | 获取扫描发现的漏洞 | ScanDetailsPage |
| PATCH | `/vulnerabilities/{vuln_id}/validate` | 手动验证漏洞状态 | ScanDetailsPage |
| POST | `/vulnerabilities/{vuln_id}/feedback` | 提交漏洞真假阳性反馈 | ScanDetailsPage |

---

### 2. AI 代理 (Agent API)
**路径前缀**: `/api/v1/agent`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| POST | `/run` | 启动 AI 代理 | NewScanPage, AutoPentestPage |
| GET | `/status` | 获取 LLM 配置状态 | SettingsPage, HomePage |
| GET | `/status/{agent_id}` | 获取代理状态和结果 | AgentStatusPage |
| GET | `/logs/{agent_id}` | 获取代理执行日志 | AgentStatusPage |
| GET | `/findings/{agent_id}` | 获取代理发现结果 | AgentStatusPage |
| POST | `/stop/{agent_id}` | 停止运行中的代理 | AgentStatusPage |
| POST | `/pause/{agent_id}` | 暂停代理 | AgentStatusPage |
| POST | `/resume/{agent_id}` | 恢复代理 | AgentStatusPage |
| POST | `/prompt/{agent_id}` | 发送自定义提示词给代理 | AgentStatusPage |
| GET | `/active` | 获取所有活跃代理列表 | HomePage |
| GET | `/tasks` | 获取任务库任务列表 | TaskLibraryPage |
| POST | `/realtime/session` | 创建实时任务会话 | RealtimeTaskPage |
| POST | `/realtime/{session_id}/message` | 发送实时消息 | RealtimeTaskPage |

---

### 3. 报告生成 (Reports API)
**路径前缀**: `/api/v1/reports`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 获取报告列表，支持过滤 | ReportsPage |
| POST | `/` | 生成新报告 | ReportsPage |
| POST | `/ai-generate` | AI 生成详细报告 | ReportsPage |
| GET | `/{report_id}` | 获取报告详情 | ReportViewPage |
| GET | `/{report_id}/view` | 查看报告 (HTML) | ReportViewPage |
| GET | `/{report_id}/download/{format}` | 下载报告 (HTML/PDF/JSON) | ReportViewPage |
| DELETE | `/{report_id}` | 删除报告 | ReportsPage |

---

### 4. 漏洞实验室 (Vuln Lab API)
**路径前缀**: `/api/v1/vuln-lab`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/types` | 获取所有漏洞类型和分类 | VulnLabPage |
| POST | `/run` | 运行漏洞实验室测试 | VulnLabPage |
| GET | `/challenges` | 获取挑战列表 | VulnLabPage |
| GET | `/challenges/{challenge_id}` | 获取挑战详情 | VulnLabPage |
| POST | `/challenges/{challenge_id}/stop` | 停止挑战 | VulnLabPage |

---

### 5. 终端代理 (Terminal API)
**路径前缀**: `/api/v1/terminal`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| POST | `/session` | 创建终端会话 | TerminalAgentPage |
| GET | `/sessions` | 列出所有终端会话 | TerminalAgentPage |
| POST | `/sessions/{session_id}/message` | 发送聊天消息 | TerminalAgentPage |
| POST | `/sessions/{session_id}/execute` | 执行命令 | TerminalAgentPage |
| GET | `/templates` | 获取可用模板列表 | TerminalAgentPage |

---

### 6. 提供商管理 (Providers API)
**路径前缀**: `/api/v1/providers`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 列出所有 LLM 提供商和账户 | ProvidersPage |
| GET | `/status` | 获取使用配额和状态汇总 | ProvidersPage |
| POST | `/detect-all` | 自动检测所有 CLI 令牌 | ProvidersPage |
| POST | `/test/{provider_id}/{account_id}` | 测试账户连接 | ProvidersPage |
| GET | `/available-models` | 获取可用模型列表 | ProvidersPage |

---

## 前端页面功能

### HomePage (主页仪表板)
**路径**: `/`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 统计卡片网格 | 显示总扫描数、运行中、完成、总漏洞 | GET /api/v1/home/stats |
| 活跃代理卡片 | 显示当前运行中的 AI 代理 | GET /api/v1/agent/active |
| 最近扫描列表 | 显示最近扫描记录 | GET /api/v1/scans |
| 快速操作按钮 | 跳转到 Auto Pentest, Vuln Lab, Terminal | 路由导航 |

---

### NewScanPage (AI Agent 新扫描页)
**路径**: `/scan/new`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 操作模式选择 | Full Auto, Recon Only, AI Prompt Mode, Analyze Only | - |
| 目标 URL 输入 | 输入目标 URL | - |
| 任务库选择 | 显示预设任务列表 | GET /api/v1/agent/tasks |
| 自定义提示词 | 输入自定义提示词 | - |
| 认证配置 | Cookie/Bearer/Basic/Header 认证 | - |
| 部署代理按钮 | 启动 AI 代理扫描 | POST /api/v1/agent/run |

---

### AutoPentestPage (一键自动渗透页)
**路径**: `/auto`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 目标 URL 输入 | 输入渗透测试目标 | - |
| 子域发现切换 | 启用/禁用子域枚举 | - |
| 开始一键渗透按钮 | 启动完整自动化渗透测试 | POST /api/v1/agent/run (mode=auto_pentest) |

---

### VulnLabPage (漏洞实验室页)
**路径**: `/vuln-lab`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 漏洞类型选择 | 选择要测试的漏洞类型 | GET /api/v1/vuln-lab/types |
| 目标 URL 输入 | 输入实验室目标 | - |
| 开始测试按钮 | 启动针对性漏洞测试 | POST /api/v1/vuln-lab/run |
| 挑战列表 | 显示所有历史挑战 | GET /api/v1/vuln-lab/challenges |

---

### TerminalAgentPage (终端代理页)
**路径**: `/terminal`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 创建会话按钮 | 创建新终端会话 | POST /api/v1/terminal/session |
| 模板选择 | 选择预定义场景模板 | GET /api/v1/terminal/templates |
| 聊天区域 | 与 AI 助手对话 | POST /api/v1/terminal/sessions/{id}/message |
| 命令输入框 | 手动输入命令 | POST /api/v1/terminal/sessions/{id}/execute |

---

### ReportsPage (报告管理页)
**路径**: `/reports`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 报告列表 | 显示所有报告 | GET /api/v1/reports |
| 查看报告按钮 | 跳转到报告查看页 | 路由导航 |
| 下载按钮 | 下载各种格式的报告 | GET /api/v1/reports/{id}/download/{format} |
| 删除报告按钮 | 删除报告 | DELETE /api/v1/reports/{id} |

---

## 完整功能测试计划

### 测试环境信息

| 项目 | 信息 |
|------|------|
| 系统版本 | NeuroSploit v3.2.4 |
| 后端地址 | http://localhost:8000 |
| API 版本 | /api/v1 |
| 测试日期 | 2026-05-18 |
| LLM 状态 | 未配置 (需要设置 API Key) |

---

### 测试用例概览

| 模块 | 测试用例数 | 优先级 |
|------|-----------|--------|
| 首页/仪表板 | 8 | P0 |
| 新建扫描 | 12 | P0 |
| 自动渗透 | 6 | P0 |
| 扫描详情 | 10 | P0 |
| 代理状态 | 8 | P1 |
| 报告管理 | 7 | P1 |
| 漏洞实验室 | 8 | P1 |
| 终端代理 | 6 | P1 |
| 提供商管理 | 5 | P2 |
| 设置页面 | 4 | P2 |

---

### P0 优先级测试用例（核心功能）

#### 1. 首页/仪表板测试

| 用例ID | 测试项 | 预期结果 | 测试方法 |
|--------|--------|----------|----------|
| HOME-001 | 页面加载 | 首页正常加载，显示统计卡片、图表、活跃代理、最近扫描 | 访问 http://localhost:8000/ |
| HOME-002 | 统计数据 | 显示正确的扫描总数、活跃代理数、漏洞数、报告数 | 验证数字显示 |
| HOME-003 | 快速操作按钮 | 点击各按钮跳转到对应页面 | 测试 Auto Pentest, New Scan, Vuln Lab, Terminal |
| HOME-004 | 活跃代理列表 | 显示正在运行的代理，支持点击查看详情 | 检查实时更新 |
| HOME-005 | 最近扫描列表 | 显示最近的扫描记录，支持点击查看详情 | 验证数据正确 |
| HOME-006 | 发现结果列表 | 显示漏洞发现结果 | 验证显示 |
| HOME-007 | 活动日志 | 显示系统活动历史记录 | 验证日志刷新 |
| HOME-008 | 图表显示 | 漏洞严重级别饼图、扫描状态柱状图正常显示 | 视觉检查 |

**API 测试命令**:
```bash
# 获取首页统计数据
curl http://localhost:8000/api/v1/home/stats

# 获取活跃代理
curl http://localhost:8000/api/v1/agent/active

# 获取最近扫描
curl http://localhost:8000/api/v1/scans?limit=10
```

---

#### 2. 新建扫描测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| NEW-001 | 页面加载 | NewScanPage 正常加载，显示所有表单元素 | - |
| NEW-002 | 操作模式切换 | Tabs 切换 4 种模式 | - |
| NEW-003 | 目标 URL 输入 | 支持输入目标 URL | - |
| NEW-004 | 子域发现开关 | 启用/禁用子域发现功能 | - |
| NEW-005 | 任务库选择 | 显示预定义任务列表 | - |
| NEW-006 | 自定义提示词 | 支持输入自定义提示词 | - |
| NEW-007 | 认证配置 | 支持 None/Basic/Bearer/API Key/Cookie 类型 | - |
| NEW-008 | 高级选项 | 显示 Kali 沙箱、浏览器验证开关 | - |
| NEW-009 | LLM 提供商选择 | 显示可用提供商列表 | - |
| NEW-010 | 部署代理 | 点击后创建扫描并跳转到 AgentStatusPage | 需要配置 LLM |
| NEW-011 | 表单验证 | 未输入目标 URL 时提示必填 | - |
| NEW-012 | 重置表单 | 点击重置清空所有输入 | - |

**API 测试命令**:
```bash
# 获取任务库
curl http://localhost:8000/api/v1/agent/tasks

# 获取可用提供商
curl http://localhost:8000/api/v1/providers
```

---

#### 3. 自动渗透测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| AUTO-001 | 页面加载 | AutoPentestPage 正常加载 | - |
| AUTO-002 | 目标输入 | 支持输入目标 URL | - |
| AUTO-003 | 子域发现 | 可选启用子域发现 | - |
| AUTO-004 | Kali 沙箱 | 可选启用 Kali 沙箱 | Docker 运行 |
| AUTO-005 | 开始扫描 | 点击后启动自动渗透流程 | 需要配置 LLM |
| AUTO-006 | 自动跳转 | 扫描开始后自动跳转到代理状态页 | - |

**API 测试命令**:
```bash
# 启动自动渗透
curl -X POST http://localhost:8000/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "target": "http://example.com",
    "mode": "auto_pentest"
  }'
```

---

#### 4. 扫描详情测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| SCAN-001 | 页面加载 | ScanDetailsPage 正常加载 | 需要存在扫描记录 |
| SCAN-002 | 扫描信息卡片 | 显示目标 URL、状态、进度、创建时间 | - |
| SCAN-003 | 扫描控制 | 支持暂停、恢复、停止、删除操作 | 扫描运行中 |
| SCAN-004 | 统计卡片 | 显示端点数、漏洞数、各严重级别数量 | - |
| SCAN-005 | 端点选项卡 | 显示发现的端点列表 | - |
| SCAN-006 | 漏洞选项卡 | 显示发现的漏洞列表 | - |
| SCAN-007 | 报告选项卡 | 显示生成的报告列表 | - |
| SCAN-008 | AI 报告生成 | 支持生成 AI 报告 | - |
| SCAN-009 | 漏洞验证 | 支持验证、误报、忽略操作 | - |
| SCAN-010 | 返回导航 | 返回按钮正确返回上一页 | - |

**API 测试命令**:
```bash
# 获取扫描列表
curl http://localhost:8000/api/v1/scans

# 获取扫描详情
curl http://localhost:8000/api/v1/scans/{scan_id}

# 暂停扫描
curl -X POST http://localhost:8000/api/v1/scans/{scan_id}/pause

# 恢复扫描
curl -X POST http://localhost:8000/api/v1/scans/{scan_id}/resume

# 停止扫描
curl -X POST http://localhost:8000/api/v1/scans/{scan_id}/stop
```

---

### P1 优先级测试用例（重要功能）

#### 5. 代理状态测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| AGENT-001 | 页面加载 | AgentStatusPage 正常加载 | 需要存在代理记录 |
| AGENT-002 | 代理状态显示 | 显示代理 ID、状态、当前阶段 | - |
| AGENT-003 | 执行日志 | 实时显示代理执行日志 | 代理运行中 |
| AGENT-004 | 发现结果 | 显示发现的漏洞和端点 | - |
| AGENT-005 | 控制按钮 | 支持暂停、恢复、停止代理 | - |
| AGENT-006 | 自定义提示词 | 支持发送自定义提示词给 AI | 代理运行中 |
| AGENT-007 | 阶段跳转 | 支持跳转到指定阶段 | 代理运行中 |
| AGENT-008 | 查看扫描详情 | 支持跳转到扫描详情页 | - |

**API 测试命令**:
```bash
# 获取代理状态
curl http://localhost:8000/api/v1/agent/status/{agent_id}

# 获取代理日志
curl http://localhost:8000/api/v1/agent/logs/{agent_id}

# 发送自定义提示词
curl -X POST http://localhost:8000/api/v1/agent/prompt/{agent_id} \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your custom instruction"}'
```

---

#### 6. 报告管理测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| REP-001 | 页面加载 | ReportsPage 正常加载 | - |
| REP-002 | 报告列表 | 显示所有报告 | - |
| REP-003 | 统计卡片 | 显示总报告数、自动生成数、本周生成数 | - |
| REP-004 | 扫描ID过滤 | 支持按扫描 ID 筛选报告 | - |
| REP-005 | 自动生成过滤 | 支持只看自动生成的报告 | - |
| REP-006 | 查看报告 | 点击查看打开报告详情页 | - |
| REP-007 | 删除报告 | 支持删除单个报告 | - |

**API 测试命令**:
```bash
# 获取报告列表
curl http://localhost:8000/api/v1/reports

# 下载报告 (HTML)
curl -O http://localhost:8000/api/v1/reports/{report_id}/download/html

# 删除报告
curl -X DELETE http://localhost:8000/api/v1/reports/{report_id}
```

---

#### 7. 漏洞实验室测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| VULN-001 | 页面加载 | VulnLabPage 正常加载 | - |
| VULN-002 | 漏洞类型分类 | 显示漏洞分类 | - |
| VULN-003 | 漏洞类型列表 | 显示各分类下的漏洞类型 | - |
| VULN-004 | 目标输入 | 支持输入目标 URL | - |
| VULN-005 | 认证配置 | 支持配置认证信息 | - |
| VULN-006 | 开始测试 | 点击后启动漏洞测试 | 需要配置 LLM |
| VULN-007 | 实时状态 | 显示测试执行状态和日志 | 测试运行中 |
| VULN-008 | 停止测试 | 支持停止正在运行的测试 | - |

**API 测试命令**:
```bash
# 获取漏洞类型
curl http://localhost:8000/api/v1/vuln-lab/types

# 获取挑战列表
curl http://localhost:8000/api/v1/vuln-lab/challenges

# 运行漏洞测试
curl -X POST http://localhost:8000/api/v1/vuln-lab/run \
  -H "Content-Type: application/json" \
  -d '{
    "vuln_type": "xss_reflected",
    "target_url": "http://example.com"
  }'

# 停止挑战
curl -X POST http://localhost:8000/api/v1/vuln-lab/challenges/{challenge_id}/stop
```

---

#### 8. 终端代理测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| TERM-001 | 页面加载 | TerminalAgentPage 正常加载 | - |
| TERM-002 | 场景模板 | 显示预定义模板 | - |
| TERM-003 | 创建会话 | 支持创建新的终端会话 | 需要配置 LLM |
| TERM-004 | 聊天交互 | 支持与 AI 聊天交互 | - |
| TERM-005 | 命令执行 | 支持执行系统命令 | - |
| TERM-006 | 利用路径 | 支持记录利用路径步骤 | - |

**API 测试命令**:
```bash
# 获取模板列表
curl http://localhost:8000/api/v1/terminal/templates

# 创建会话
curl -X POST http://localhost:8000/api/v1/terminal/session \
  -H "Content-Type: application/json" \
  -d '{"template_id": "network_scanner"}'

# 发送消息
curl -X POST http://localhost:8000/api/v1/terminal/sessions/{session_id}/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Run nmap scan"}'

# 执行命令
curl -X POST http://localhost:8000/api/v1/terminal/sessions/{session_id}/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "nmap -p 80,443 localhost"}'
```

---

### P2 优先级测试用例（辅助功能）

#### 9. 提供商管理测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| PROV-001 | 页面加载 | ProvidersPage 正常加载 | - |
| PROV-002 | 提供商列表 | 显示所有 LLM 提供商 | - |
| PROV-003 | 使用配额 | 显示各提供商的配额使用情况 | - |
| PROV-004 | CLI 检测 | 支持自动检测 CLI 令牌 | CLI 工具已安装 |
| PROV-005 | 连接测试 | 支持手动连接和测试账户 | - |

**API 测试命令**:
```bash
# 获取提供商列表
curl http://localhost:8000/api/v1/providers

# 获取配额状态
curl http://localhost:8000/api/v1/providers/status

# 检测所有 CLI 令牌
curl -X POST http://localhost:8000/api/v1/providers/detect-all
```

---

#### 10. 设置页面测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| SET-001 | 页面加载 | SettingsPage 正常加载 | - |
| SET-002 | 功能开关 | 支持启用/禁用各项功能 | - |
| SET-003 | 默认配置 | 支持设置默认 LLM 提供商和模型 | - |
| SET-004 | 自适应学习 | 支持查看学习统计 | - |

---

### 测试数据准备

#### 1. 测试目标建议

| 目标类型 | 推荐目标 | 用途 |
|----------|----------|------|
| 官方测试站点 | http://testphp.vulnweb.com | SQLi, XSS, etc. |
| OWASP 站点 | https://juice-shop.herokuapp.com | 多种漏洞 |
| 本地 DVWA | http://localhost/dvwa | 多种漏洞 |
| HTTPBin | https://httpbin.org | API 测试 |

#### 2. 测试认证凭据

| 类型 | 示例 |
|------|------|
| Basic Auth | username: admin, password: admin |
| Bearer Token | Bearer eyJhbGciOiJIUzI1NiIs... |
| API Key | X-API-Key: test-api-key-12345 |
| Cookie | PHPSESSID=test-session-id |

---

### 测试执行检查清单

#### 测试前检查
- [ ] 确认后端服务运行中 (curl http://localhost:8000/api/v1/agent/status)
- [ ] 确认 LLM API Key 已配置
- [ ] 确认 Docker 服务运行中 (如需沙箱测试)
- [ ] 确认测试目标可达

#### 测试后清理
- [ ] 停止所有运行中的扫描
- [ ] 删除测试创建的扫描记录
- [ ] 删除测试创建的报告
- [ ] 清理测试数据

---

### 测试结果记录模板

#### 测试执行记录

| 执行日期 | 测试人员 | 通过用例数 | 失败用例数 | 阻塞用例数 | 备注 |
|----------|----------|------------|------------|------------|------|
| 2026-05-18 | - | 0/75 | 0 | 0 | 初始测试 |

#### 测试用例结果

| 用例ID | 执行状态 | 执行时间 | 备注 |
|--------|----------|----------|------|
| HOME-001 | Pass/Fail/Blocked | - | - |
| HOME-002 | Pass/Fail/Blocked | - | - |

---

### 实际测试结果记录

#### API 基础测试结果 (2026-05-18)

| API 端点 | 请求方法 | 测试结果 | 备注 |
|----------|----------|----------|------|
| /api/v1/agent/status | GET | ✅ 通过 | 返回 LLM 未配置状态 |
| /api/v1/scans | GET | ✅ 通过 | 返回空扫描列表 |
| /api/v1/providers | GET | ✅ 通过 | 返回 10+ 提供商列表 |
| /api/v1/agent/tasks | GET | ✅ 通过 | 返回预设任务列表 |
| /api/v1/vuln-lab/types | GET | ✅ 通过 | 返回漏洞类型分类 |
| /api/v1/terminal/templates | GET | ✅ 通过 | 返回 4 个模板 |
| /api/v1/reports | GET | ✅ 通过 | 返回空报告列表 |

#### 测试发现

1. **LLM 未配置**: 系统返回 `status: not_configured`，需要配置 ANTHROPIC_API_KEY
2. **所有 API 端点正常**: 后端 API 响应正常
3. **数据为空**: 扫描列表、报告列表为空 (正常初始状态)
4. **提供商已配置**: 系统预置了 10+ 个 LLM 提供商配置

---

## Providers与Settings大模型配置区别

### 概述

Providers 页面和 Settings 页面虽然都涉及大模型配置，但它们的**定位、作用层级和配置方式**完全不同。Settings 是"基础/默认"的单提供商模式，Providers 是"高级/多提供商"的 Smart Router 路由模式。

---

### Settings 页面 — 基础/默认配置

**定位**: 系统全局的**默认 LLM 配置**，是"传统"的单提供商模式。

**文件**: [frontend/src/pages/SettingsPage.tsx](file:///workspace/frontend/src/pages/SettingsPage.tsx)

| 配置项 | 说明 |
|--------|------|
| `llm_provider` | 选择**唯一的默认提供商** (claude/openai/gemini/openrouter/together/fireworks/ollama/lmstudio) |
| `llm_model` | 选择默认模型 |
| API Key 输入 | 为选中的提供商**直接输入 API Key**，保存到 `.env` 文件 |
| `max_output_tokens` | 全局最大输出 token 限制 |
| `enable_model_routing` | 启用/禁用模型路由功能 |

**关键特征**:
- **单提供商模式**: 一次只用一个 LLM 提供商
- **API Key 存储在 `.env` 文件**: 如 `ANTHROPIC_API_KEY=sk-ant-...`
- **通过 `PUT /api/v1/settings` 保存**: 修改后需要重启服务
- **不启用 Smart Router 时生效**: 这是 `ENABLE_SMART_ROUTER=false` 时的默认行为
- **代码位置**: [backend/config.py](file:///workspace/backend/config.py#L33-L41) 中的 `DEFAULT_LLM_PROVIDER` 和 `DEFAULT_LLM_MODEL`

---

### Providers 页面 — Smart Router 多提供商管理

**定位**: Smart Router 的**多提供商、多账户管理**，是"高级"的多提供商路由模式。

**文件**: [frontend/src/pages/ProvidersPage.tsx](file:///workspace/frontend/src/pages/ProvidersPage.tsx)

| 配置项 | 说明 |
|--------|------|
| OAuth 提供商 | Claude Code、Codex CLI、Gemini CLI、Cursor、Copilot 等 (通过 CLI 令牌检测) |
| API Key 提供商 | Anthropic、OpenAI、Gemini、OpenRouter、GLM、Kimi 等 (手动添加) |
| 多账户管理 | 同一提供商可以有**多个账户** (不同 API Key 或令牌) |
| CLI 令牌检测 | 自动从本地 CLI 工具检测 OAuth 令牌 |
| 账户测试 | 测试每个账户的连接是否正常 |
| 启用/禁用提供商 | 可以单独启用或禁用某个提供商 |
| Tier 分级 | Tier 1 (付费)、Tier 2 (廉价)、Tier 3 (免费/本地) |
| 环境变量编辑器 | 直接编辑 `.env` 文件中的配置 |

**关键特征**:
- **多提供商模式**: 可以同时配置多个提供商，Smart Router 自动选择
- **多账户支持**: 同一提供商可以添加多个 API Key，支持负载均衡
- **故障转移**: 当一个提供商/账户失败时，自动切换到下一个
- **轮询负载均衡**: 多个账户之间轮询分配请求
- **需要启用 Smart Router**: 必须设置 `ENABLE_SMART_ROUTER=true`
- **代码位置**: [backend/core/smart_router/router.py](file:///workspace/backend/core/smart_router/router.py#L50-L68)

---

### 核心区别对比

| 维度 | Settings 页面 | Providers 页面 |
|------|--------------|----------------|
| **模式** | 单提供商模式 | 多提供商路由模式 |
| **Smart Router** | 不需要 | 必须启用 |
| **提供商数量** | 1 个默认提供商 | 可同时配置 10+ 个提供商 |
| **账户数量** | 每个提供商 1 个 Key | 每个提供商可多个账户 |
| **故障转移** | ❌ 无 | ✅ 自动切换 |
| **负载均衡** | ❌ 无 | ✅ 轮询 |
| **CLI 令牌** | ❌ 不支持 | ✅ 自动检测 |
| **API Key 存储** | `.env` 文件 | 内存 + `.env` 文件 |
| **Tier 优先级** | ❌ 无 | ✅ Tier 1→2→3 |
| **配额追踪** | ❌ 无 | ✅ 自动追踪 token 使用 |
| **账户过期检测** | ❌ 无 | ✅ 令牌过期倒计时 |
| **连接测试** | ❌ 无 | ✅ 测试单个账户连接 |
| **适用场景** | 简单使用、快速配置 | 生产环境、高可用 |

---

### 两者协作的请求路由流程

```
用户发起 LLM 请求
    │
    ├── ENABLE_SMART_ROUTER=false ?
    │   └── 使用 Settings 中的 DEFAULT_LLM_PROVIDER + DEFAULT_LLM_MODEL
    │       直接调用该提供商的 API
    │
    └── ENABLE_SMART_ROUTER=true ?
        └── Smart Router 接管
            ├── 1. 检查是否有 preferred_provider 指定
            ├── 2. 按 Tier 优先级排序所有已连接的提供商
            ├── 3. 在每个提供商内轮询选择可用账户
            ├── 4. 调用选中的提供商/账户
            ├── 5. 失败时自动故障转移到下一个
            └── 6. 记录 token 使用和配额
```

---

### 配置建议

| 使用场景 | 推荐配置 | 操作步骤 |
|----------|----------|----------|
| 个人使用、只有一个 API Key | Settings 页面 | 1. 选择提供商 2. 输入 API Key 3. 保存 |
| 团队使用、需要高可用 | Providers 页面 | 1. 设置 `ENABLE_SMART_ROUTER=true` 2. 添加多个提供商 3. 检测 CLI 令牌 |
| 使用本地模型 (Ollama/LM Studio) | Settings 页面 | 1. 选择 Ollama/LM Studio 2. 输入 Base URL 3. 保存 |
| 混合使用 (云端+本地) | Providers 页面 | 1. 启用 Smart Router 2. 添加云端提供商 3. 添加本地提供商 4. Tier 自动排序 |

---

## 总结

NeuroSploit v3.2.4 是一个功能完整的 AI 驱动渗透测试平台，包含：
- **17+ 个主要页面** 提供完整的用户界面
- **16+ 个 API 模块** 处理所有后端功能
- **50+ 种漏洞类型** 内置检测支持
- **4 种操作模式** 满足不同测试需求
- **Kali Linux 沙箱** 提供安全隔离执行
- **Smart Router** 实现多 LLM 智能管理
- **RAG 知识增强** 提升 AI 专业水平
- **完整报告生成** 输出专业渗透测试文档
- **详细页面布局分析** 提供 UI/UX 结构参考
- **完整参数关联性** 明确数据流与模型关联
- **完整功能测试计划** 覆盖所有系统功能
