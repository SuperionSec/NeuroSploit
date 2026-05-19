# NeuroSploit v3.2.4 全面测试计划

## 1. 测试概述

### 1.1 测试目标

验证 NeuroSploit v3.2.4 系统的所有功能流程、界面操作和 API 接口，确保从目标创建到报告生成的完整业务流程可正常运行，覆盖 18 个前端页面、18 个 API 模块（151 个端点）和所有核心子系统。

### 1.2 测试范围

| 范围 | 说明 |
|------|------|
| 前端页面 | 18 个页面，覆盖所有 UI 组件和交互操作 |
| 后端 API | 18 个模块，151 个端点 |
| 业务流程 | 7 大核心流程 + 5 大配置流程 + 4 大管理流程 |
| 子系统 | Smart Router、RAG、Agent、VulnEngine、Sandbox、MCP、Scheduler |
| 数据流转 | 页面间数据传递、WebSocket 实时通信、文件上传下载 |

### 1.3 测试环境

| 项目 | 信息 |
|------|------|
| 系统版本 | NeuroSploit v3.2.4 |
| 后端地址 | http://localhost:8000 |
| 前端地址 | http://localhost:3001 |
| API 版本 | /api/v1 |
| 数据库 | SQLite (aiosqlite) |
| Docker | Kali Linux 沙箱容器 |
| LLM | 需配置至少一个提供商的 API Key |

### 1.4 测试用例统计

| 流程分类 | 测试流程数 | 测试用例数 | 优先级 |
|----------|-----------|-----------|--------|
| 核心业务流程 | 7 | 76 | P0 |
| 配置管理流程 | 5 | 60 | P1 |
| 资源管理流程 | 4 | 33 | P1 |
| 交互通信流程 | 3 | 20 | P1 |
| 报告数据流程 | 2 | 22 | P1 |
| 异常边界场景 | 5 | 30 | P2 |
| **合计** | **26** | **241** | - |

### 1.5 优先级定义

| 优先级 | 定义 | 说明 |
|--------|------|------|
| P0 | 阻塞级 | 核心业务流程无法完成，系统不可用 |
| P1 | 重要级 | 重要功能异常，影响用户体验 |
| P2 | 一般级 | 边界场景、异常处理、体验优化 |

### 1.6 测试前置条件

| 编号 | 前置条件 | 验证方法 |
|------|----------|----------|
| PRE-01 | 后端服务正常运行 | `curl http://localhost:8000/health` 返回 200 |
| PRE-02 | 前端服务正常运行 | 浏览器访问 http://localhost:3001 可看到首页 |
| PRE-03 | 至少一个 LLM 提供商已配置 | Providers 页面显示至少一个 Connected 状态 |
| PRE-04 | Smart Router 已启用 | `.env` 中 `ENABLE_SMART_ROUTER=true` |
| PRE-05 | Docker 服务可用（沙箱测试） | `docker ps` 可正常执行 |
| PRE-06 | Minimax API Key 已配置 | Providers 页面 Minimax 显示 Connected |

---

## 2. 核心业务流程测试（P0）

### 2.1 扫描生命周期流程

**流程描述**: 从创建扫描到查看结果的完整生命周期，是系统最核心的业务流程。

**涉及页面**: NewScanPage → AgentStatusPage → ScanDetailsPage → ReportViewPage
**涉及 API**: Scans API、Agent API、Reports API、Targets API

#### 流程图

```
NewScanPage (/scan/new)
  │ 选择操作模式 → 输入目标 → 配置选项 → 点击"部署代理"
  ▼
AgentStatusPage (/agent/:agentId)
  │ 实时查看代理执行 → 暂停/恢复/停止 → 查看阶段进度
  ▼
ScanDetailsPage (/scan/:scanId)
  │ 查看扫描详情 → 查看漏洞/端点/任务/日志 → 验证漏洞 → 生成报告
  ▼
ReportViewPage (/reports/:reportId)
  │ 查看/下载报告 → 返回报告列表
```

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| FLOW-001 | 打开新建扫描页 | 点击侧边栏 "New Scan" 或首页 "New Scan" 按钮 | NewScanPage 正常加载，显示4个操作模式Tab | GET /api/v1/agent/tasks |
| FLOW-002 | 选择操作模式 | 点击 "Full Auto" Tab | Tab高亮，显示对应表单 | - |
| FLOW-003 | 输入扫描目标 | 在 "Single URL" 模式输入 `http://testphp.vulnweb.com` | 目标输入框显示URL，无报错 | - |
| FLOW-004 | 切换目标模式 | 点击 "Multiple URLs" → 输入多个URL → 点击 "Upload File" | 三种模式切换正常，文件上传支持 .txt/.csv/.lst | POST /api/v1/targets/upload |
| FLOW-005 | 选择任务库 | 展开 Task Library → 选择分类 "Full Auto" → 点击一个预定义任务 | 任务详情显示在右侧面板 | GET /api/v1/agent/tasks |
| FLOW-006 | 配置认证 | Auth Type 选择 "Bearer" → 输入 Token | 认证配置保存到表单状态 | - |
| FLOW-007 | 设置高级选项 | 展开 Advanced Options → 拖动 Max Crawl Depth 滑块到 5 | 滑块值显示为 5 | - |
| FLOW-008 | 部署代理 | 点击 "Deploy Agent" 按钮 | 显示加载动画 → 跳转到 AgentStatusPage | POST /api/v1/agent/run |
| FLOW-009 | 查看代理状态 | AgentStatusPage 加载 | 显示代理名称、状态(running)、当前阶段、进度条 | GET /api/v1/agent/status/{id} |
| FLOW-010 | 实时进度更新 | 等待代理执行 | 进度条实时更新，阶段自动切换，日志流实时显示 | WebSocket /ws |
| FLOW-011 | 暂停代理 | 点击 "Pause" 按钮 | 代理状态变为 paused | POST /api/v1/agent/pause/{id} |
| FLOW-012 | 恢复代理 | 点击 "Resume" 按钮 | 代理状态变为 running | POST /api/v1/agent/resume/{id} |
| FLOW-013 | 发送自定义提示词 | 在提示词输入框输入 "Focus on SQL injection" → 点击发送 | 代理接收提示词并调整行为 | POST /api/v1/agent/prompt/{id} |
| FLOW-014 | 停止代理 | 点击 "Stop" 按钮 → 确认弹窗点击确认 | 代理状态变为 stopped，跳转到 ScanDetailsPage | POST /api/v1/agent/stop/{id} |
| FLOW-015 | 查看扫描详情 | ScanDetailsPage 加载 | 显示扫描信息卡片（目标URL、状态、进度、时间） | GET /api/v1/scans/{id} |
| FLOW-016 | 查看漏洞列表 | 点击 "Vulnerabilities" Tab | 显示发现的漏洞列表，包含严重级别、类型、URL | GET /api/v1/scans/{id}/vulnerabilities |
| FLOW-017 | 查看端点列表 | 点击 "Endpoints" Tab | 显示发现的端点列表，包含方法、路径、状态码 | GET /api/v1/scans/{id}/endpoints |
| FLOW-018 | 查看代理任务 | 点击 "Agent Tasks" Tab | 显示代理执行的任务列表 | GET /api/v1/scans/{id}/tasks |
| FLOW-019 | 查看活动日志 | 点击 "Activity Log" Tab | 显示扫描活动日志 | GET /api/v1/scans/{id}/logs |
| FLOW-020 | 验证漏洞 | 点击漏洞的 "Validate" 按钮 → 选择 "Confirm TP" | 漏洞状态更新为已验证 | PATCH /api/v1/vulnerabilities/{id}/validate |
| FLOW-021 | 生成AI报告 | 点击 "AI Report" 按钮 → 选择提供商和模型 → 点击生成 | 报告生成中 → 完成后跳转到 ReportViewPage | POST /api/v1/reports/ai-generate |
| FLOW-022 | 查看报告 | ReportViewPage 加载 | 报告内容在 iframe 中正常显示 | GET /api/v1/reports/{id}/view |
| FLOW-023 | 下载报告 | 点击 "Download HTML" 按钮 | 浏览器下载 HTML 格式报告文件 | GET /api/v1/reports/{id}/download/html |
| FLOW-024 | 返回报告列表 | 点击 "Back" 按钮 | 返回 ReportsPage，新报告出现在列表中 | GET /api/v1/reports |

---

### 2.2 自动渗透流程

**流程描述**: 一键自动渗透测试，系统自动协调多专家代理完成全流程。

**涉及页面**: AutoPentestPage → AgentStatusPage → ScanDetailsPage
**涉及 API**: Agent API、Scans API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| FLOW-025 | 打开自动渗透页 | 点击侧边栏 "Auto Pentest" | AutoPentestPage 正常加载 | - |
| FLOW-026 | 输入目标 | 在目标输入框输入 `http://testphp.vulnweb.com` | 目标输入正常 | - |
| FLOW-027 | 启用子域发现 | 勾选 "Subdomain Discovery" 复选框 | 复选框选中 | - |
| FLOW-028 | 启用Kali沙箱 | 勾选 "Kali Sandbox" 复选框 | 复选框选中（需Docker运行） | - |
| FLOW-029 | 开始自动渗透 | 点击 "Start Auto Pentest" 按钮 | 创建扫描任务，显示进度区域 | POST /api/v1/agent/run (mode=auto_pentest) |
| FLOW-030 | 查看多会话 | 等待渗透启动 | 显示多个并行会话（Recon、Exploit、Validator等） | GET /api/v1/agent/status/{id} |
| FLOW-031 | 查看测试历史 | 渗透完成后查看历史记录 | 显示历史测试列表，包含三重验证状态 | GET /api/v1/agent/history |
| FLOW-032 | 执行三重验证 | 点击 "Triple Check" 按钮 | 启动三重验证流程 | POST /api/v1/agent/triple-check/{scan_id} |
| FLOW-033 | 重新运行测试 | 点击历史记录的 "Re-run" 按钮 | 重新启动相同配置的渗透测试 | POST /api/v1/agent/run |

---

### 2.3 Full IA 测试流程

**流程描述**: 完整 AI 渗透测试，4阶段自动化执行（Recon→Testing→PostExploit→Report）。

**涉及页面**: FullIATestingPage
**涉及 API**: Full IA API、Agent API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| FLOW-034 | 打开Full IA页 | 点击侧边栏 "Full IA Testing" | FullIATestingPage 正常加载 | - |
| FLOW-035 | 输入目标配置 | 输入目标URL，选择扫描范围 | 配置表单正常填写 | - |
| FLOW-036 | 启动Full IA | 点击 "Start Full IA Test" 按钮 | 创建4阶段测试任务 | POST /api/v1/full-ia/start |
| FLOW-037 | 监控4阶段进度 | 观察 Recon→Testing→PostExploit→Report 进度 | 各阶段依次执行，进度条实时更新 | GET /api/v1/full-ia/status/{id} |
| FLOW-038 | 查看阶段结果 | 点击各阶段查看详细结果 | 显示该阶段的发现和操作记录 | GET /api/v1/full-ia/results/{id} |
| FLOW-039 | 停止Full IA | 点击 "Stop" 按钮 | 测试停止，保留已完成阶段的结果 | POST /api/v1/full-ia/stop/{id} |

---

### 2.4 漏洞实验室流程

**流程描述**: 针对特定漏洞类型进行专项测试，支持挑战模式。

**涉及页面**: VulnLabPage
**涉及 API**: Vuln Lab API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| FLOW-040 | 打开漏洞实验室 | 点击侧边栏 "Vuln Lab" | VulnLabPage 正常加载 | - |
| FLOW-041 | 选择漏洞类型 | 从下拉菜单选择 "SQL Injection" | 显示 SQL Injection 相关测试选项 | GET /api/v1/vuln-lab/categories |
| FLOW-042 | 配置测试参数 | 输入目标URL，选择测试强度 | 参数配置正常 | - |
| FLOW-043 | 启动挑战 | 点击 "Start Challenge" 按钮 | 创建挑战，显示进度 | POST /api/v1/vuln-lab/run |
| FLOW-044 | 查看挑战进度 | 等待挑战执行 | 实时显示测试进度和发现 | GET /api/v1/vuln-lab/challenges |
| FLOW-045 | 停止挑战 | 点击 "Stop" 按钮 | 挑战停止，保留已发现的结果 | POST /api/v1/vuln-lab/challenges/{id}/stop |
| FLOW-046 | 删除挑战 | 点击 "Delete" 按钮 → 确认 | 挑战记录被删除 | DELETE /api/v1/vuln-lab/challenges/{id} |
| FLOW-047 | 查看挑战结果 | 点击挑战查看详情 | 显示测试结果、payload、响应 | GET /api/v1/vuln-lab/challenges/{id} |

---

### 2.5 实时任务流程

**流程描述**: 实时交互式 AI 对话，支持工具执行和报告生成。

**涉及页面**: RealtimeTaskPage
**涉及 API**: Agent API (realtime)

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| FLOW-048 | 打开实时任务页 | 点击侧边栏 "Realtime" | RealtimeTaskPage 正常加载 | - |
| FLOW-049 | 创建新会话 | 点击 "New Session" 按钮 | 创建新的实时会话，显示聊天界面 | POST /api/v1/agent/realtime/session |
| FLOW-050 | 发送消息 | 在输入框输入 "Scan http://testphp.vulnweb.com for XSS" → 回车 | AI代理回复，显示分析结果 | POST /api/v1/agent/realtime/{id}/message |
| FLOW-051 | 使用快速提示 | 点击 "Security Headers" 快速提示按钮 | 自动发送预设提示词 | POST /api/v1/agent/realtime/{id}/message |
| FLOW-052 | 执行安全工具 | 点击工具按钮 → 选择 "nmap" → 确认执行 | 工具执行中 → 返回结果 | POST /api/v1/agent/realtime/{id}/execute-tool |
| FLOW-053 | 查看工具状态 | 点击工具图标查看状态 | 显示6种工具的可用状态 | GET /api/v1/agent/realtime/tools/status |
| FLOW-054 | 查看LLM状态 | 观察LLM状态指示器 | 显示当前LLM连接状态 | GET /api/v1/agent/realtime/llm-status |
| FLOW-055 | 生成实时报告 | 点击 "Generate Report" 按钮 | 生成当前会话的报告 | GET /api/v1/agent/realtime/{id}/report |
| FLOW-056 | 下载JSON报告 | 点击 "Download JSON" 按钮 | 浏览器下载 JSON 格式报告 | GET /api/v1/agent/realtime/{id}/report |
| FLOW-057 | 切换会话 | 点击左侧会话列表中的另一个会话 | 切换到该会话，显示历史消息 | GET /api/v1/agent/realtime/{id} |
| FLOW-058 | 删除会话 | 点击会话的删除按钮 → 确认 | 会话被删除 | DELETE /api/v1/agent/realtime/{id} |
| FLOW-059 | 展开/折叠消息 | 点击消息的展开/折叠按钮 | 消息内容展开或折叠 | - |
| FLOW-060 | 展开/折叠发现 | 点击发现结果的展开/折叠按钮 | 发现详情展开或折叠 | - |

---

### 2.6 终端代理流程

**流程描述**: 终端交互模式，AI 辅助手动渗透测试。

**涉及页面**: TerminalAgentPage
**涉及 API**: Terminal API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| FLOW-061 | 打开终端代理页 | 点击侧边栏 "Terminal" | TerminalAgentPage 正常加载 | - |
| FLOW-062 | 创建终端会话 | 点击 "New Session" 按钮 | 创建新的终端会话 | POST /api/v1/terminal/sessions |
| FLOW-063 | 输入命令 | 在终端输入框输入 "nmap -sV target.com" → 回车 | 命令执行，显示输出结果 | POST /api/v1/terminal/sessions/{id}/execute |
| FLOW-064 | AI辅助建议 | 等待AI分析命令输出 | AI提供下一步建议 | POST /api/v1/terminal/sessions/{id}/ai-suggest |
| FLOW-065 | 查看命令历史 | 向上滚动查看历史命令 | 历史命令正常显示 | GET /api/v1/terminal/sessions/{id}/history |
| FLOW-066 | 停止终端会话 | 点击 "Stop" 按钮 | 终端会话结束 | POST /api/v1/terminal/sessions/{id}/stop |

---

### 2.7 首页仪表板流程

**流程描述**: 系统首页展示全局概览数据，提供快速操作入口。

**涉及页面**: HomePage
**涉及 API**: Dashboard API、Agent API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| FLOW-067 | 打开首页 | 访问 http://localhost:3001/ | HomePage 正常加载 | GET /api/v1/dashboard/stats |
| FLOW-068 | 查看统计卡片 | 观察4个统计卡片 | 显示扫描总数、活跃代理数、漏洞数、报告数 | GET /api/v1/dashboard/stats |
| FLOW-069 | 查看活跃代理 | 观察 Active Agents 区域 | 显示正在运行的代理列表 | GET /api/v1/agent/active |
| FLOW-070 | 查看最近扫描 | 观察 Recent Scans 区域 | 显示最近的扫描记录 | GET /api/v1/dashboard/recent |
| FLOW-071 | 查看活动日志 | 观察 Activity Feed 区域 | 显示系统活动历史 | GET /api/v1/dashboard/activity-feed |
| FLOW-072 | 过滤活动日志 | 点击5种过滤选项 | 日志按类型过滤显示 | GET /api/v1/dashboard/activity-feed?type=xxx |
| FLOW-073 | 快速操作跳转 | 点击 "Auto Pentest" 按钮 | 跳转到 AutoPentestPage | - |
| FLOW-074 | 刷新仪表板 | 点击 "Refresh" 按钮 | 所有数据刷新 | GET /api/v1/dashboard/stats |
| FLOW-075 | WebSocket断连 | 断开网络连接 | 显示连接丢失警告 | WebSocket /ws |
| FLOW-076 | 恢复连接 | 恢复网络连接 | 警告消失，数据自动恢复 | WebSocket /ws |

---

## 3. 配置管理流程测试（P1）

### 3.1 Providers 提供商管理流程

**流程描述**: 配置和管理 LLM 提供商，包括 API Key 添加、CLI 令牌检测、连接测试和环境变量编辑。

**涉及页面**: ProvidersPage
**涉及 API**: Providers API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| CONF-001 | 打开Providers页 | 点击侧边栏 "Providers" | ProvidersPage 正常加载，显示19个提供商卡片 | GET /api/v1/providers |
| CONF-002 | 查看Smart Router状态 | 观察页面标题下方状态 | 显示 "Smart Router active -- X/19 providers connected" | GET /api/v1/providers |
| CONF-003 | 查看统计概览 | 观察4个统计卡片 | 显示 Providers/Connected/Accounts/Total Tokens 数值 | GET /api/v1/providers/status |
| CONF-004 | 查看OAuth提供商 | 观察 OAuth Providers 网格区域 | 显示8个OAuth提供商卡片 | GET /api/v1/providers |
| CONF-005 | 查看API Key提供商 | 观察 API Key Providers 网格区域 | 显示11个API Key提供商卡片 | GET /api/v1/providers |
| CONF-006 | 检测所有CLI令牌 | 点击 "Detect All CLIs" 按钮 | 自动检测本地CLI工具令牌，Toast提示检测结果 | POST /api/v1/providers/detect-all |
| CONF-007 | 打开提供商配置 | 点击 Minimax 提供商卡片 | 打开 ConfigModal，显示提供商详情 | - |
| CONF-008 | 查看提供商信息 | 观察 ConfigModal 头部 | 显示名称、API格式、默认模型 | - |
| CONF-009 | 添加API Key凭据 | 在 Label 输入标签 → 在 API Key 输入框输入 Key → 点击 "Add" | 账户添加成功，显示在账户列表 | POST /api/v1/providers/{id}/connect |
| CONF-010 | 测试账户连接 | 点击账户的 TestTube 图标 | 显示测试结果（成功=绿色/失败=红色） | POST /api/v1/providers/test/{pid}/{aid} |
| CONF-011 | 检测单个CLI令牌 | 打开 Claude Code 配置 → 点击 "Detect CLI Token" | 检测本地 Claude Code CLI 令牌 | POST /api/v1/providers/claude_code/detect |
| CONF-012 | 查看账户详情 | 观察账户列表中的账户信息 | 显示 label、source标签、tokens_used、last_used | - |
| CONF-013 | 查看过期时间 | 观察 OAuth 账户的 expires_at | 显示倒计时（如 "45m left"、"Expired"） | - |
| CONF-014 | 删除账户 | 点击账户的 Trash2 图标 | 账户被删除 | DELETE /api/v1/providers/{pid}/accounts/{aid} |
| CONF-015 | 启用/禁用提供商 | 点击提供商卡片的 ON/OFF 开关 | 提供商状态切换，卡片样式变化 | POST /api/v1/providers/{id}/toggle |
| CONF-016 | 打开环境变量编辑器 | 点击 "Show API Key & Config Manager" | 展开环境变量编辑面板 | GET /api/v1/providers/env |
| CONF-017 | 搜索环境变量 | 在搜索框输入关键词 | 只显示匹配的环境变量键 | - |
| CONF-018 | 编辑环境变量 | 修改某个键的值 → 点击 "Save" | 值保存成功，Toast提示 | POST /api/v1/providers/env |
| CONF-019 | 查看密钥脱敏 | 观察 API Key 类型的值 | 显示为密码输入框，GET返回脱敏值 | GET /api/v1/providers/env |
| CONF-020 | 刷新提供商数据 | 点击 "Refresh" 按钮 | 所有提供商数据刷新 | GET /api/v1/providers, /status |

---

### 3.2 Settings 系统设置流程

**流程描述**: 系统全局设置，包括 LLM 配置、功能开关和通知配置。

**涉及页面**: SettingsPage
**涉及 API**: Settings API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| CONF-021 | 打开Settings页 | 点击侧边栏 "Settings" | SettingsPage 正常加载 | GET /api/v1/settings |
| CONF-022 | 选择LLM提供商 | 在 LLM Provider 下拉框选择 "openai" | 提供商切换，显示对应的模型选择 | GET /api/v1/settings/models/openai |
| CONF-023 | 选择LLM模型 | 在 Model 下拉框选择模型 | 模型切换成功 | GET /api/v1/settings/models/{provider} |
| CONF-024 | 输入API Key | 在 OpenAI API Key 输入框输入 Key | Key 输入正常 | PUT /api/v1/settings |
| CONF-025 | 配置本地LLM | 选择 Ollama → 输入 Base URL | URL 保存成功 | PUT /api/v1/settings |
| CONF-026 | 设置最大Token | 修改 Max Output Tokens 为 4096 | 值保存成功 | PUT /api/v1/settings |
| CONF-027 | 设置并发扫描 | 修改 Max Concurrent Scans 为 3 | 值保存成功 | PUT /api/v1/settings |
| CONF-028 | 启用激进模式 | 打开 Aggressive Mode 开关 | 开关状态切换 | PUT /api/v1/settings |
| CONF-029 | 启用模型路由 | 打开 Enable Model Routing 开关 | Smart Router 启用 | PUT /api/v1/settings |
| CONF-030 | 启用知识增强 | 打开 Enable Knowledge Enhancement 开关 | RAG 功能启用 | PUT /api/v1/settings |
| CONF-031 | 启用浏览器验证 | 打开 Enable Browser Verification 开关 | 浏览器验证启用 | PUT /api/v1/settings |
| CONF-032 | 配置Discord通知 | 输入 Discord Webhook URL → 保存 | URL 保存成功 | PUT /api/v1/settings |
| CONF-033 | 配置Telegram通知 | 输入 Bot Token 和 Chat ID → 保存 | 配置保存成功 | PUT /api/v1/settings |
| CONF-034 | 配置WhatsApp通知 | 输入 Twilio 4项配置 → 保存 | 配置保存成功 | PUT /api/v1/settings |
| CONF-035 | 设置通知过滤 | 选择通知严重级别过滤 | 过滤级别保存 | PUT /api/v1/settings |
| CONF-036 | 测试Discord通知 | 点击 "Test Discord" 按钮 | 发送测试消息到 Discord | POST /api/v1/settings/notifications/test/discord |
| CONF-037 | 测试Telegram通知 | 点击 "Test Telegram" 按钮 | 发送测试消息到 Telegram | POST /api/v1/settings/notifications/test/telegram |
| CONF-038 | 测试WhatsApp通知 | 点击 "Test WhatsApp" 按钮 | 发送测试消息到 WhatsApp | POST /api/v1/settings/notifications/test/whatsapp |
| CONF-039 | 检测工具 | 点击 "Detect Tools" 按钮 | 显示可用安全工具列表 | GET /api/v1/settings/tools |
| CONF-040 | 保存所有设置 | 修改多个设置后点击保存 | 所有设置保存成功 | PUT /api/v1/settings |

---

### 3.3 Scheduler 调度任务流程

**流程描述**: 创建和管理定时扫描调度任务。

**涉及页面**: SchedulerPage
**涉及 API**: Scheduler API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| CONF-041 | 打开调度器页 | 点击侧边栏 "Scheduler" | SchedulerPage 正常加载 | GET /api/v1/scheduler/ |
| CONF-042 | 查看调度列表 | 观察现有调度任务 | 显示所有调度任务 | GET /api/v1/scheduler/ |
| CONF-043 | 创建Preset调度 | 选择 Preset 模式 → 选择 "Daily" → 输入目标URL → 选择代理角色 → 点击创建 | 调度任务创建成功 | POST /api/v1/scheduler/ |
| CONF-044 | 创建Cron调度 | 选择 Custom Cron → 输入 "0 8 * * 1-5" → 配置参数 → 创建 | 自定义Cron调度创建成功 | POST /api/v1/scheduler/ |
| CONF-045 | 创建Interval调度 | 选择 Interval → 选择间隔时间 → 配置参数 → 创建 | 间隔调度创建成功 | POST /api/v1/scheduler/ |
| CONF-046 | 暂停调度 | 点击调度任务的 "Pause" 按钮 | 调度状态变为 paused | POST /api/v1/scheduler/{id}/pause |
| CONF-047 | 恢复调度 | 点击调度任务的 "Resume" 按钮 | 调度状态变为 active | POST /api/v1/scheduler/{id}/resume |
| CONF-048 | 删除调度 | 点击 "Delete" 按钮 → 确认 | 调度任务被删除 | DELETE /api/v1/scheduler/{id} |

---

### 3.4 MCP 服务器管理流程

**流程描述**: 管理和配置 MCP (Model Context Protocol) 服务器。

**涉及页面**: MCPManagementPage
**涉及 API**: MCP API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| CONF-049 | 打开MCP页 | 点击侧边栏 "MCP" | MCPManagementPage 正常加载 | GET /api/v1/mcp/servers |
| CONF-050 | 查看服务器列表 | 观察 MCP 服务器列表 | 显示已配置的 MCP 服务器 | GET /api/v1/mcp/servers |
| CONF-051 | 添加MCP服务器 | 点击 "Add Server" → 输入名称和配置 → 保存 | 服务器添加成功 | POST /api/v1/mcp/servers |
| CONF-052 | 启动MCP服务器 | 点击服务器的 "Start" 按钮 | 服务器状态变为 running | POST /api/v1/mcp/servers/{id}/start |
| CONF-053 | 停止MCP服务器 | 点击服务器的 "Stop" 按钮 | 服务器状态变为 stopped | POST /api/v1/mcp/servers/{id}/stop |
| CONF-054 | 查看服务器工具 | 点击服务器查看可用工具 | 显示该服务器提供的工具列表 | GET /api/v1/mcp/servers/{id}/tools |
| CONF-055 | 删除MCP服务器 | 点击 "Delete" 按钮 → 确认 | 服务器被删除 | DELETE /api/v1/mcp/servers/{id} |

---

### 3.5 Smart Router 路由流程

**流程描述**: 验证 Smart Router 的多提供商负载均衡和故障转移机制。

**涉及页面**: ProvidersPage + 任意发起LLM请求的页面
**涉及 API**: Providers API、Smart Router 内部逻辑

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| CONF-056 | 验证Tier优先级 | 配置 Tier1+Tier2+Tier3 提供商 → 发起请求 | 优先使用 Tier 1 提供商 | Smart Router 内部 |
| CONF-057 | 验证故障转移 | 禁用 Tier 1 提供商 → 发起请求 | 自动切换到 Tier 2 提供商 | Smart Router 内部 |
| CONF-058 | 验证账户轮询 | 同一提供商添加2个账户 → 发起多次请求 | 请求在账户间轮询分配 | Smart Router 内部 |
| CONF-059 | 验证禁用跳过 | 禁用一个提供商 → 发起请求 | 该提供商被跳过 | POST /api/v1/providers/{id}/toggle |
| CONF-060 | 验证配额追踪 | 发起多次请求后查看 Providers 页面 | Token 使用量正确更新 | GET /api/v1/providers/status |

---

## 4. 资源管理流程测试（P1）

### 4.1 知识库管理流程

**流程描述**: 管理知识增强（RAG）文档，上传、查看、搜索和删除知识文档。

**涉及页面**: KnowledgePage
**涉及 API**: Knowledge API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| RES-001 | 打开知识库页 | 点击侧边栏 "Knowledge" | KnowledgePage 正常加载 | GET /api/v1/knowledge/stats |
| RES-002 | 查看统计卡片 | 观察3个统计卡片 | 显示文档数、条目数、覆盖漏洞类型数 | GET /api/v1/knowledge/stats |
| RES-003 | 上传文档 | 拖拽一个 PDF 文件到上传区域 | 文件上传成功，显示在文档列表 | POST /api/v1/knowledge/upload |
| RES-004 | 上传MD文档 | 点击上传按钮选择 .md 文件 | 文件上传成功 | POST /api/v1/knowledge/upload |
| RES-005 | 查看文档列表 | 观察文档列表区域 | 显示所有已上传文档 | GET /api/v1/knowledge/documents |
| RES-006 | 按漏洞类型过滤 | 选择漏洞类型过滤选项 | 只显示匹配类型的文档 | GET /api/v1/knowledge/search |
| RES-007 | 展开文档详情 | 点击文档展开按钮 | 显示文档详细内容和条目 | GET /api/v1/knowledge/documents/{id} |
| RES-008 | 折叠文档详情 | 点击文档折叠按钮 | 文档详情折叠 | - |
| RES-009 | 删除文档 | 点击文档的删除按钮 → 确认 | 文档被删除 | DELETE /api/v1/knowledge/documents/{id} |
| RES-010 | 刷新知识库 | 点击 "Refresh" 按钮 | 统计数据和文档列表刷新 | GET /api/v1/knowledge/stats |

---

### 4.2 沙箱管理流程

**流程描述**: 管理和监控 Kali Linux 沙箱容器。

**涉及页面**: SandboxDashboardPage
**涉及 API**: Sandbox API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| RES-011 | 打开沙箱页 | 点击侧边栏 "Sandboxes" | SandboxDashboardPage 正常加载 | GET /api/v1/sandbox/ |
| RES-012 | 查看容器列表 | 观察容器列表 | 显示所有 Kali 沙箱容器 | GET /api/v1/sandbox/ |
| RES-013 | 健康检查 | 点击容器的健康检查按钮 | 显示容器健康状态 | GET /api/v1/sandbox/{id} |
| RES-014 | 销毁容器 | 点击容器的 "Destroy" 按钮 → 确认 | 容器被销毁 | DELETE /api/v1/sandbox/{id} |
| RES-015 | 清理过期容器 | 点击 "Cleanup Expired" 按钮 | 过期容器被清理 | POST /api/v1/sandbox/cleanup |
| RES-016 | 清理孤儿容器 | 点击 "Cleanup Orphans" 按钮 | 孤儿容器被清理 | POST /api/v1/sandbox/cleanup-orphans |
| RES-017 | 查看关联扫描 | 点击容器的关联扫描链接 | 跳转到 ScanDetailsPage | 路由导航 /scan/{id} |
| RES-018 | 刷新容器列表 | 点击 "Refresh" 按钮 | 容器列表刷新 | GET /api/v1/sandbox/ |

---

### 4.3 任务库管理流程

**流程描述**: 管理预定义和自定义任务模板。

**涉及页面**: TaskLibraryPage
**涉及 API**: Agent Tasks API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| RES-019 | 打开任务库页 | 点击侧边栏 "Tasks" | TaskLibraryPage 正常加载 | GET /api/v1/agent/tasks |
| RES-020 | 查看任务列表 | 观察任务卡片列表 | 显示所有预定义任务 | GET /api/v1/agent/tasks |
| RES-021 | 分类过滤 | 点击 "Recon" 分类过滤 | 只显示 Recon 类型的任务 | GET /api/v1/agent/tasks |
| RES-022 | 搜索任务 | 在搜索框输入 "SQL" | 只显示名称包含 "SQL" 的任务 | 本地搜索 |
| RES-023 | 查看任务详情 | 点击任务卡片 | 显示任务详情 | - |
| RES-024 | 使用任务 | 点击 "Use Task" 按钮 | 跳转到 NewScanPage，任务已预选 | 路由导航 /scan/new |
| RES-025 | 创建自定义任务 | 点击 "Create Custom Task" → 填写表单 → 保存 | 自定义任务创建成功 | POST /api/v1/agent/tasks |
| RES-026 | 删除自定义任务 | 点击自定义任务的删除按钮 → 确认 | 任务被删除 | DELETE /api/v1/agent/tasks/{id} |
| RES-027 | 刷新任务列表 | 点击 "Refresh" 按钮 | 任务列表刷新 | GET /api/v1/agent/tasks |

---

### 4.4 提示词管理流程

**流程描述**: 管理系统提示词模板。

**涉及页面**: 无独立页面（通过 API 管理）
**涉及 API**: Prompts API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| RES-028 | 获取提示词列表 | 调用 API 获取所有提示词 | 返回提示词列表 | GET /api/v1/prompts |
| RES-029 | 获取提示词分类 | 调用 API 获取分类 | 返回提示词分类列表 | GET /api/v1/prompts/categories |
| RES-030 | 创建提示词 | POST 创建新提示词 | 提示词创建成功 | POST /api/v1/prompts |
| RES-031 | 更新提示词 | PUT 更新现有提示词 | 提示词更新成功 | PUT /api/v1/prompts/{id} |
| RES-032 | 删除提示词 | DELETE 删除提示词 | 提示词删除成功 | DELETE /api/v1/prompts/{id} |
| RES-033 | 搜索提示词 | GET 搜索提示词 | 返回匹配结果 | GET /api/v1/prompts/search?q=xxx |

---

## 5. 交互与通信流程测试（P1）

### 5.1 WebSocket 实时通信流程

**流程描述**: 验证 WebSocket 连接、消息推送和断连重连机制。

**涉及页面**: 所有需要实时更新的页面
**涉及 API**: WebSocket /ws

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| COMM-001 | 建立WebSocket连接 | 打开首页 | WebSocket 连接成功建立 | WebSocket /ws |
| COMM-002 | 接收实时更新 | 启动一个扫描任务 | 扫描进度实时推送到前端 | WebSocket /ws |
| COMM-003 | 代理状态推送 | 查看代理状态页 | 代理状态变化实时推送 | WebSocket /ws |
| COMM-004 | 断连检测 | 断开后端服务 | 前端显示连接丢失警告 | WebSocket /ws |
| COMM-005 | 自动重连 | 恢复后端服务 | WebSocket 自动重连，数据恢复 | WebSocket /ws |
| COMM-006 | 多页面同时连接 | 同时打开首页和扫描详情页 | 两个页面都正常接收推送 | WebSocket /ws |

---

### 5.2 目标管理流程

**流程描述**: 目标的创建、验证、上传和管理。

**涉及页面**: NewScanPage（内嵌）、API 直接调用
**涉及 API**: Targets API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| COMM-007 | 验证单个目标 | 输入 URL 进行验证 | 返回验证结果 | POST /api/v1/targets/validate |
| COMM-008 | 批量验证目标 | 提交多个 URL 进行验证 | 返回每个URL的验证结果 | POST /api/v1/targets/validate/bulk |
| COMM-009 | 上传目标文件 | 上传 .txt 文件包含多个目标 | 文件解析成功，目标创建 | POST /api/v1/targets/upload |
| COMM-010 | 获取目标列表 | 查询所有目标 | 返回目标列表 | GET /api/v1/targets |
| COMM-011 | 获取目标详情 | 查询单个目标 | 返回目标详情 | GET /api/v1/targets/{id} |
| COMM-012 | 删除目标 | 删除指定目标 | 目标删除成功 | DELETE /api/v1/targets/{id} |

---

### 5.3 漏洞管理流程

**流程描述**: 漏洞的查看、验证、反馈和搜索。

**涉及页面**: ScanDetailsPage（Vulnerabilities Tab）
**涉及 API**: Vulnerabilities API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| COMM-013 | 查看漏洞列表 | 在扫描详情页点击 Vulnerabilities Tab | 显示漏洞列表 | GET /api/v1/scans/{id}/vulnerabilities |
| COMM-014 | 验证漏洞 | 点击漏洞的 Validate 按钮 | 漏洞状态更新 | PATCH /api/v1/vulnerabilities/{id}/validate |
| COMM-015 | 标记误报 | 选择 "False Positive" | 漏洞标记为误报 | PATCH /api/v1/vulnerabilities/{id}/validate |
| COMM-016 | 确认真阳性 | 选择 "Confirm TP" | 漏洞标记为确认 | PATCH /api/v1/vulnerabilities/{id}/validate |
| COMM-017 | 撤销验证 | 点击 "Revoke Validation" | 验证状态撤销 | PATCH /api/v1/vulnerabilities/{id}/validate |
| COMM-018 | 提交反馈 | 输入漏洞反馈内容 | 反馈提交成功 | POST /api/v1/vulnerabilities/{id}/feedback |
| COMM-019 | 搜索漏洞 | 输入搜索关键词 | 返回匹配漏洞 | GET /api/v1/vulnerabilities/search |
| COMM-020 | 按严重级别过滤 | 选择 Critical/High/Medium/Low | 只显示对应级别的漏洞 | GET /api/v1/vulnerabilities?severity=xxx |

---

## 6. 报告与数据流程测试（P1）

### 6.1 报告生成与管理流程

**流程描述**: 报告的生成、查看、下载和管理。

**涉及页面**: ReportsPage、ReportViewPage、ScanDetailsPage
**涉及 API**: Reports API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| RPT-001 | 打开报告列表 | 点击侧边栏 "Reports" | ReportsPage 正常加载 | GET /api/v1/reports |
| RPT-002 | 查看报告列表 | 观察报告卡片列表 | 显示所有报告 | GET /api/v1/reports |
| RPT-003 | 格式过滤 | 点击 "HTML" 格式过滤 | 只显示 HTML 格式报告 | 本地过滤 |
| RPT-004 | 排序 | 选择 "By Vulns" 排序 | 报告按漏洞数排序 | 本地排序 |
| RPT-005 | 搜索报告 | 在搜索框输入关键词 | 只显示匹配的报告 | 本地搜索 |
| RPT-006 | 查看报告 | 点击报告的 "View" 按钮 | 跳转到 ReportViewPage | GET /api/v1/reports/{id}/view |
| RPT-007 | 下载HTML报告 | 点击 "Download HTML" | 浏览器下载 HTML 文件 | GET /api/v1/reports/{id}/download/html |
| RPT-008 | 下载JSON报告 | 点击 "Download JSON" | 浏览器下载 JSON 文件 | GET /api/v1/reports/{id}/download/json |
| RPT-009 | 下载ZIP报告 | 点击 "Download ZIP" | 浏览器下载 ZIP 文件 | GET /api/v1/reports/{id}/download-zip |
| RPT-010 | AI重新生成 | 点击 "AI Regenerate" 按钮 | AI 重新生成报告 | POST /api/v1/reports/ai-generate |
| RPT-011 | 删除报告 | 点击 "Delete" 按钮 → 确认 | 报告被删除 | DELETE /api/v1/reports/{id} |
| RPT-012 | 从扫描生成报告 | 在 ScanDetailsPage 点击 "Generate Report" | 报告生成成功 | POST /api/v1/reports |
| RPT-013 | AI报告生成 | 在 ScanDetailsPage 点击 "AI Report" → 选择提供商/模型 | AI 生成报告 | POST /api/v1/reports/ai-generate |
| RPT-014 | 查看报告详情 | 在 ReportViewPage 观察 | 报告在 iframe 中正常显示 | GET /api/v1/reports/{id}/view |
| RPT-015 | 新标签页打开 | 点击 "Open in New Tab" | 报告在新窗口打开 | GET /api/v1/reports/{id}/view |
| RPT-016 | 返回报告列表 | 点击 "Back" 按钮 | 返回 ReportsPage | - |
| RPT-017 | 新建扫描跳转 | 点击 "New Scan" 按钮 | 跳转到 NewScanPage | 路由导航 /scan/new |
| RPT-018 | 下载PDF报告 | 点击 "Download PDF" | 浏览器下载 PDF 文件 | GET /api/v1/reports/{id}/download/pdf |

---

### 6.2 仪表板数据流程

**流程描述**: 验证仪表板数据的准确性和实时性。

**涉及页面**: HomePage
**涉及 API**: Dashboard API

#### 测试用例

| 用例ID | 测试步骤 | 操作详情 | 预期结果 | 涉及API |
|--------|----------|----------|----------|---------|
| RPT-019 | 统计数据准确性 | 创建扫描后刷新首页 | 扫描总数+1 | GET /api/v1/dashboard/stats |
| RPT-020 | 活跃代理实时性 | 启动代理后查看首页 | 活跃代理列表实时更新 | GET /api/v1/agent/active |
| RPT-021 | 最近扫描排序 | 创建多个扫描后查看 | 最近扫描按时间倒序排列 | GET /api/v1/dashboard/recent |
| RPT-022 | 活动日志过滤 | 切换5种过滤选项 | 日志按类型正确过滤 | GET /api/v1/dashboard/activity-feed |

---

## 7. 异常与边界场景测试（P2）

### 7.1 输入验证异常

| 用例ID | 测试场景 | 操作详情 | 预期结果 |
|--------|----------|----------|----------|
| ERR-001 | 空目标提交 | 不输入目标URL直接点击"部署代理" | 表单验证提示，不发送请求 |
| ERR-002 | 无效URL格式 | 输入 "not-a-url" 作为目标 | 显示URL格式错误提示 |
| ERR-003 | 超长目标URL | 输入超过2048字符的URL | 正确处理或截断，不崩溃 |
| ERR-004 | 空API Key | 在Providers页面不输入Key直接点击Add | 按钮禁用或提示输入 |
| ERR-005 | 无效API Key | 输入错误的API Key格式 | 连接测试失败，显示错误信息 |
| ERR-006 | 特殊字符输入 | 在各输入框输入 `<script>alert(1)</script>` | 不执行XSS，正确转义显示 |
| ERR-007 | SQL注入输入 | 在搜索框输入 `' OR 1=1 --` | 不执行SQL注入，正常搜索 |
| ERR-008 | 文件上传异常 | 上传非支持格式的文件（如 .exe） | 显示格式不支持提示 |
| ERR-009 | 大文件上传 | 上传超过限制的文件 | 显示文件大小限制提示 |
| ERR-010 | 空文件上传 | 上传空内容的 .txt 文件 | 显示文件为空提示 |

### 7.2 网络与服务异常

| 用例ID | 测试场景 | 操作详情 | 预期结果 |
|--------|----------|----------|----------|
| ERR-011 | 后端服务停止 | 停止后端后操作前端 | 显示 "Service not running" 提示 |
| ERR-012 | LLM API超时 | 配置无效的LLM端点 | 请求超时后显示错误，不崩溃 |
| ERR-013 | LLM API Key过期 | 使用过期的API Key | 连接测试失败，显示过期提示 |
| ERR-014 | Docker不可用 | 停止Docker服务后启动沙箱扫描 | 显示Docker不可用提示，不崩溃 |
| ERR-015 | WebSocket断连 | 断开后端网络连接 | 前端显示连接丢失警告 |
| ERR-016 | 并发请求过多 | 同时启动多个扫描 | 系统按max_concurrent_scans限制处理 |

### 7.3 数据状态异常

| 用例ID | 测试场景 | 操作详情 | 预期结果 |
|--------|----------|----------|----------|
| ERR-017 | 访问不存在的扫描 | 直接访问 /scan/non-existent-id | 显示404或空状态提示 |
| ERR-018 | 访问不存在的报告 | 直接访问 /reports/non-existent-id | 显示404或空状态提示 |
| ERR-019 | 重复操作 | 快速连续点击同一按钮 | 不产生重复请求或正确去重 |
| ERR-020 | 删除后访问 | 删除扫描后访问其详情页 | 显示不存在提示 |
| ERR-021 | 并发编辑 | 同时在两个标签页编辑同一设置 | 最后保存的生效，不产生数据冲突 |

### 7.4 权限与安全异常

| 用例ID | 测试场景 | 操作详情 | 预期结果 |
|--------|----------|----------|----------|
| ERR-022 | 未配置LLM启动扫描 | 不配置任何LLM提供商直接启动扫描 | 显示需要配置LLM的提示 |
| ERR-023 | Smart Router禁用时操作 | ENABLE_SMART_ROUTER=false时访问Providers | 显示Smart Router禁用横幅 |
| ERR-024 | 环境变量注入 | 在环境变量编辑器输入恶意值 | 白名单过滤，不允许修改非白名单键 |
| ERR-025 | API直接访问 | 不通过前端直接调用API | API正常响应（无认证要求时） |

### 7.5 UI交互边界

| 用例ID | 测试场景 | 操作详情 | 预期结果 |
|--------|----------|----------|----------|
| ERR-026 | 浏览器缩放 | 缩放浏览器到50%和200% | 页面布局不错乱 |
| ERR-027 | 窄屏显示 | 缩小浏览器窗口到320px宽度 | 响应式布局正常 |
| ERR-028 | 长文本显示 | 漏洞描述超长文本 | 正确截断或换行，不溢出 |
| ERR-029 | 大量数据列表 | 扫描发现100+漏洞 | 列表正常渲染，不卡顿 |
| ERR-030 | 模态框滚动 | ConfigModal内容超出视口 | 模态框内部可滚动，最大高度85vh |

---

## 8. 测试执行指南

### 8.1 测试执行顺序

按以下顺序执行测试，确保前置条件满足：

```
第1轮: 基础环境验证
  ├── PRE-01 ~ PRE-06 前置条件检查
  └── ERR-011, ERR-014 服务可用性验证

第2轮: 配置流程（P1）
  ├── CONF-001 ~ CONF-020 Providers 配置
  ├── CONF-021 ~ CONF-040 Settings 配置
  ├── CONF-041 ~ CONF-048 Scheduler 配置
  ├── CONF-049 ~ CONF-055 MCP 配置
  └── CONF-056 ~ CONF-060 Smart Router 验证

第3轮: 核心业务流程（P0）
  ├── FLOW-001 ~ FLOW-024 扫描生命周期
  ├── FLOW-025 ~ FLOW-033 自动渗透
  ├── FLOW-034 ~ FLOW-039 Full IA 测试
  ├── FLOW-040 ~ FLOW-047 漏洞实验室
  ├── FLOW-048 ~ FLOW-060 实时任务
  ├── FLOW-061 ~ FLOW-066 终端代理
  └── FLOW-067 ~ FLOW-076 首页仪表板

第4轮: 资源与数据流程（P1）
  ├── RES-001 ~ RES-010 知识库
  ├── RES-011 ~ RES-018 沙箱管理
  ├── RES-019 ~ RES-027 任务库
  ├── RES-028 ~ RES-033 提示词
  ├── COMM-001 ~ COMM-006 WebSocket
  ├── COMM-007 ~ COMM-012 目标管理
  ├── COMM-013 ~ COMM-020 漏洞管理
  ├── RPT-001 ~ RPT-018 报告流程
  └── RPT-019 ~ RPT-022 仪表板数据

第5轮: 异常边界场景（P2）
  └── ERR-001 ~ ERR-030
```

### 8.2 API 快速验证脚本

```bash
#!/bin/bash
BASE="http://localhost:8000/api/v1"

echo "=== NeuroSploit v3.2.4 API 端点验证 ==="

echo "--- 健康检查 ---"
curl -s "$BASE/../health" | head -1

echo "--- Dashboard ---"
curl -s "$BASE/dashboard/stats" | head -1
curl -s "$BASE/dashboard/recent" | head -1
curl -s "$BASE/dashboard/activity-feed" | head -1

echo "--- Scans ---"
curl -s "$BASE/scans" | head -1

echo "--- Agent ---"
curl -s "$BASE/agent/active" | head -1
curl -s "$BASE/agent/tasks" | head -1

echo "--- Providers ---"
curl -s "$BASE/providers" | head -1
curl -s "$BASE/providers/status" | head -1
curl -s "$BASE/providers/available-models" | head -1
curl -s "$BASE/providers/env" | head -1

echo "--- Settings ---"
curl -s "$BASE/settings" | head -1
curl -s "$BASE/settings/tools" | head -1

echo "--- Reports ---"
curl -s "$BASE/reports" | head -1

echo "--- Knowledge ---"
curl -s "$BASE/knowledge/stats" | head -1
curl -s "$BASE/knowledge/documents" | head -1

echo "--- Sandbox ---"
curl -s "$BASE/sandbox/" | head -1

echo "--- MCP ---"
curl -s "$BASE/mcp/servers" | head -1

echo "--- Scheduler ---"
curl -s "$BASE/scheduler/" | head -1

echo "--- Targets ---"
curl -s "$BASE/targets" | head -1

echo "--- Vulnerabilities ---"
curl -s "$BASE/vulnerabilities" | head -1

echo "--- Prompts ---"
curl -s "$BASE/prompts" | head -1

echo "=== 验证完成 ==="
```

### 8.3 测试结果记录模板

| 用例ID | 执行日期 | 执行结果 | 实际行为 | 缺陷编号 | 备注 |
|--------|----------|----------|----------|----------|------|
| FLOW-001 | YYYY-MM-DD | ✅通过/❌失败/⏭跳过 | 描述实际观察到的行为 | BUG-XXX | - |

### 8.4 缺陷严重级别定义

| 级别 | 定义 | 示例 |
|------|------|------|
| S1-致命 | 核心功能完全不可用 | 扫描无法创建、系统无法启动 |
| S2-严重 | 核心功能异常但有替代方案 | 报告无法下载PDF但可下载HTML |
| S3-一般 | 非核心功能异常 | 搜索结果排序不正确 |
| S4-轻微 | UI显示问题 | 按钮对齐偏差、文字截断 |

### 8.5 测试覆盖率矩阵

| 页面 | 流程覆盖 | API覆盖 | 用例数 |
|------|----------|---------|--------|
| HomePage | FLOW-067~076, RPT-019~022 | dashboard, agent | 14 |
| NewScanPage | FLOW-001~008 | agent, targets | 8 |
| AutoPentestPage | FLOW-025~033 | agent | 9 |
| ScanDetailsPage | FLOW-015~021, COMM-013~020 | scans, vulnerabilities | 13 |
| AgentStatusPage | FLOW-009~014 | agent | 6 |
| VulnLabPage | FLOW-040~047 | vuln-lab | 8 |
| TerminalAgentPage | FLOW-061~066 | terminal | 6 |
| ProvidersPage | CONF-001~020, CONF-056~060 | providers | 25 |
| SettingsPage | CONF-021~040 | settings | 20 |
| FullIATestingPage | FLOW-034~039 | full-ia | 6 |
| MCPManagementPage | CONF-049~055 | mcp | 7 |
| SchedulerPage | CONF-041~048 | scheduler | 8 |
| KnowledgePage | RES-001~010 | knowledge | 10 |
| RealtimeTaskPage | FLOW-048~060 | agent/realtime | 13 |
| SandboxDashboardPage | RES-011~018 | sandbox | 8 |
| TaskLibraryPage | RES-019~027 | agent/tasks | 9 |
| ReportsPage | RPT-001~011 | reports | 11 |
| ReportViewPage | RPT-006, RPT-014~018 | reports | 6 |
| 跨页面/系统级 | COMM, ERR | websocket, targets | 30 |
| **合计** | **26个流程** | **18个API模块** | **241** |

### 8.6 关键业务流程验证清单

以下为系统交付前必须全部通过的关键流程：

- [ ] **扫描生命周期**: FLOW-001 ~ FLOW-024 全部通过
- [ ] **自动渗透**: FLOW-025 ~ FLOW-033 全部通过
- [ ] **Providers配置**: CONF-001 ~ CONF-020 全部通过
- [ ] **Smart Router路由**: CONF-056 ~ CONF-060 全部通过
- [ ] **报告生成下载**: RPT-001 ~ RPT-018 全部通过
- [ ] **实时任务对话**: FLOW-048 ~ FLOW-060 全部通过
- [ ] **WebSocket实时通信**: COMM-001 ~ COMM-006 全部通过
- [ ] **服务异常处理**: ERR-011 ~ ERR-016 全部通过
