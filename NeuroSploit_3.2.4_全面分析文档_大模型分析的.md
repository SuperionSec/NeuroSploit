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
| GET | `/` | 获取扫描列表，支持分页和状态过滤 | [HomePage](#homepage-主页仪表板), [ScanDetailsPage](#scandetailspage-扫描详情页) |
| POST | `/` | 创建新扫描 | [NewScanPage](#newscanpage-ai-agent-新扫描页) |
| GET | `/{scan_id}` | 获取单个扫描详情 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| POST | `/{scan_id}/start` | 启动扫描 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| POST | `/{scan_id}/stop` | 停止运行中的扫描 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| POST | `/{scan_id}/pause` | 暂停运行中的扫描 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| POST | `/{scan_id}/resume` | 恢复暂停的扫描 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| POST | `/{scan_id}/skip-to/{phase}` | 跳转到指定扫描阶段 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| DELETE | `/{scan_id}` | 删除扫描 | [ReportsPage](#reportspage-报告管理页) |
| GET | `/{scan_id}/endpoints` | 获取扫描发现的端点 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| GET | `/{scan_id}/vulnerabilities` | 获取扫描发现的漏洞 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| PATCH | `/vulnerabilities/{vuln_id}/validate` | 手动验证漏洞状态 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| POST | `/vulnerabilities/{vuln_id}/feedback` | 提交漏洞真假阳性反馈 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| GET | `/vulnerabilities/learning/stats` | 获取自适应学习统计 | [SettingsPage](#settingspage-设置页) |

---

### 2. 目标验证 (Targets API)
**路径前缀**: `/api/v1/targets`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| POST | `/validate` | 验证单个目标 URL | [NewScanPage](#newscanpage-ai-agent-新扫描页) |
| POST | `/validate/bulk` | 批量验证目标 URL | [NewScanPage](#newscanpage-ai-agent-新扫描页) |
| POST | `/upload` | 上传包含目标列表的文件 | [NewScanPage](#newscanpage-ai-agent-新扫描页) |

---

### 3. AI 代理 (Agent API)
**路径前缀**: `/api/v1/agent`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| POST | `/run` | 启动 AI 代理 | [NewScanPage](#newscanpage-ai-agent-新扫描页), [AutoPentestPage](#autopentestpage-一键自动渗透页) |
| GET | `/status` | 获取 LLM 配置状态 | [SettingsPage](#settingspage-设置页), [HomePage](#homepage-主页仪表板) |
| GET | `/status/{agent_id}` | 获取代理状态和结果 | [AgentStatusPage](#agentstatuspage-代理状态页) |
| GET | `/by-scan/{scan_id}` | 通过扫描 ID 查找代理 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| GET | `/logs/{agent_id}` | 获取代理执行日志 | [AgentStatusPage](#agentstatuspage-代理状态页) |
| GET | `/findings/{agent_id}` | 获取代理发现结果 | [AgentStatusPage](#agentstatuspage-代理状态页) |
| GET | `/vuln-agents/{agent_id}` | 获取漏洞代理编排状态 | [AgentStatusPage](#agentstatuspage-代理状态页) |
| DELETE | `/{agent_id}` | 删除代理结果 | [ReportsPage](#reportspage-报告管理页) |
| POST | `/stop/{agent_id}` | 停止运行中的代理 | [AgentStatusPage](#agentstatuspage-代理状态页) |
| POST | `/pause/{agent_id}` | 暂停代理 | [AgentStatusPage](#agentstatuspage-代理状态页) |
| POST | `/resume/{agent_id}` | 恢复代理 | [AgentStatusPage](#agentstatuspage-代理状态页) |
| POST | `/skip-to/{agent_id}/{phase}` | 代理跳转到阶段 | [AgentStatusPage](#agentstatuspage-代理状态页) |
| POST | `/prompt/{agent_id}` | 发送自定义提示词给代理 | [AgentStatusPage](#agentstatuspage-代理状态页) |
| GET | `/active` | 获取所有活跃代理列表 | [HomePage](#homepage-主页仪表板) |
| GET | `/history` | 获取代理历史记录 | [ReportsPage](#reportspage-报告管理页) |
| POST | `/triple-check/{scan_id}` | 用不同模型重新验证发现 | [ScanDetailsPage](#scandetailspage-扫描详情页) |
| GET | `/tasks` | 获取任务库任务列表 | [TaskLibraryPage](#tasklibrarypage-任务库页) |
| GET | `/tasks/{task_id}` | 获取单个任务详情 | [TaskLibraryPage](#tasklibrarypage-任务库页) |
| POST | `/tasks` | 创建自定义任务 | [TaskLibraryPage](#tasklibrarypage-任务库页) |
| DELETE | `/tasks/{task_id}` | 删除任务 | [TaskLibraryPage](#tasklibrarypage-任务库页) |
| POST | `/realtime/session` | 创建实时任务会话 | [RealtimeTaskPage](#realtimetaskpage-实时任务页) |
| POST | `/realtime/{session_id}/message` | 发送实时消息 | [RealtimeTaskPage](#realtimetaskpage-实时任务页) |
| GET | `/realtime/{session_id}` | 获取实时会话状态 | [RealtimeTaskPage](#realtimetaskpage-实时任务页) |
| GET | `/realtime/{session_id}/report` | 获取实时会话报告 | [RealtimeTaskPage](#realtimetaskpage-实时任务页) |
| DELETE | `/realtime/{session_id}` | 删除实时会话 | [RealtimeTaskPage](#realtimetaskpage-实时任务页) |
| GET | `/realtime/sessions/list` | 列出所有实时会话 | [RealtimeTaskPage](#realtimetaskpage-实时任务页) |
| GET | `/realtime/llm-status` | 获取实时任务 LLM 状态 | [RealtimeTaskPage](#realtimetaskpage-实时任务页) |
| GET | `/realtime/tools/list` | 获取可用工具列表 | [RealtimeTaskPage](#realtimetaskpage-实时任务页) |
| GET | `/realtime/tools/status` | 获取工具状态 | [RealtimeTaskPage](#realtimetaskpage-实时任务页) |
| POST | `/realtime/{session_id}/execute-tool` | 手动执行工具 | [RealtimeTaskPage](#realtimetaskpage-实时任务页) |

---

### 4. 报告生成 (Reports API)
**路径前缀**: `/api/v1/reports`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 获取报告列表，支持过滤 | [ReportsPage](#reportspage-报告管理页) |
| POST | `/` | 生成新报告 | [ReportsPage](#reportspage-报告管理页) |
| POST | `/ai-generate` | AI 生成详细报告 | [ReportsPage](#reportspage-报告管理页) |
| GET | `/{report_id}` | 获取报告详情 | [ReportViewPage](#reportviewpage-报告查看页) |
| GET | `/{report_id}/view` | 查看报告 (HTML) | [ReportViewPage](#reportviewpage-报告查看页) |
| GET | `/{report_id}/download/{format}` | 下载报告 (HTML/PDF/JSON) | [ReportViewPage](#reportviewpage-报告查看页) |
| GET | `/{report_id}/download-zip` | 下载完整报告包 | [ReportViewPage](#reportviewpage-报告查看页) |
| DELETE | `/{report_id}` | 删除报告 | [ReportsPage](#reportspage-报告管理页) |

---

### 5. 漏洞实验室 (Vuln Lab API)
**路径前缀**: `/api/v1/vuln-lab`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/types` | 获取所有漏洞类型和分类 | [VulnLabPage](#vulnlabpage-漏洞实验室页) |
| POST | `/run` | 运行漏洞实验室测试 | [VulnLabPage](#vulnlabpage-漏洞实验室页) |
| GET | `/challenges` | 获取挑战列表，支持过滤 | [VulnLabPage](#vulnlabpage-漏洞实验室页) |
| GET | `/challenges/{challenge_id}` | 获取挑战详情和实时状态 | [VulnLabPage](#vulnlabpage-漏洞实验室页) |
| GET | `/stats` | 获取实验室统计数据 | [VulnLabPage](#vulnlabpage-漏洞实验室页) |
| POST | `/challenges/{challenge_id}/stop` | 停止运行中的挑战 | [VulnLabPage](#vulnlabpage-漏洞实验室页) |
| DELETE | `/challenges/{challenge_id}` | 删除挑战记录 | [VulnLabPage](#vulnlabpage-漏洞实验室页) |
| GET | `/logs/{challenge_id}` | 获取挑战执行日志 | [VulnLabPage](#vulnlabpage-漏洞实验室页) |

**支持的漏洞类型分类**:
1. **Injection (注入类)**: XSS, SQLi, Command Injection, SSTI, NoSQL 等
2. **Advanced Injection (高级注入)**: LDAP, XPath, GraphQL, CRLF 等
3. **File Access (文件访问)**: LFI, RFI, Path Traversal, XXE, File Upload 等
4. **Request Forgery (请求伪造)**: SSRF, CSRF, GraphQL 相关
5. **Authentication (认证)**: Auth Bypass, JWT, Session Fixation 等
6. **Authorization (授权)**: IDOR, Broken Access Control 等
7. **Client-side (客户端)**: DOM Clobbering, Open Redirect 等
8. **Data Exposure (数据泄露)**: Information Disclosure, Exposed Secrets 等
9. **Infrastructure (基础设施)**: Subdomain Takeover, DNS Issues 等
10. **Logic (逻辑)**: Business Logic, Race Conditions 等

---

### 6. 终端代理 (Terminal API)
**路径前缀**: `/api/v1/terminal`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| POST | `/session` | 创建终端会话 | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| GET | `/sessions` | 列出所有终端会话 | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| GET | `/sessions/{session_id}` | 获取会话详情 | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| DELETE | `/sessions/{session_id}` | 删除会话 | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| POST | `/sessions/{session_id}/message` | 发送聊天消息 | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| POST | `/sessions/{session_id}/execute` | 执行命令 | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| POST | `/sessions/{session_id}/exploitation-path` | 添加利用路径步骤 | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| GET | `/sessions/{session_id}/exploitation-path` | 获取利用路径 | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| GET | `/sessions/{session_id}/vpn-status` | 获取 VPN 状态 | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| GET | `/templates` | 获取可用模板列表 | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| POST | `/sessions/{session_id}/vpn/upload` | 上传 VPN 配置 | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| POST | `/sessions/{session_id}/vpn/connect` | 连接 VPN | [TerminalAgentPage](#terminalagentpage-终端代理页) |
| POST | `/sessions/{session_id}/vpn/disconnect` | 断开 VPN | [TerminalAgentPage](#terminalagentpage-终端代理页) |

**内置模板**:
1. **Network Scanner**: 网络扫描、主机发现、端口探测
2. **Lateral Movement**: 横向移动、SMB 中继、SSH 隧道
3. **Privilege Escalation**: 提权、SUID 二进制、内核漏洞
4. **VPN Reconnaissance**: VPN 连接和内网侦察

---

### 7. 沙箱管理 (Sandbox API)
**路径前缀**: `/api/v1/sandbox`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 获取沙箱池状态和容器列表 | [SandboxDashboardPage](#sandboxdashboardpage-沙箱仪表板页) |
| GET | `/{scan_id}` | 获取单个沙箱健康检查 | [SandboxDashboardPage](#sandboxdashboardpage-沙箱仪表板页) |
| DELETE | `/{scan_id}` | 销毁指定沙箱 | [SandboxDashboardPage](#sandboxdashboardpage-沙箱仪表板页) |
| POST | `/cleanup` | 清理所有沙箱 | [SandboxDashboardPage](#sandboxdashboardpage-沙箱仪表板页) |
| POST | `/cleanup-orphans` | 清理孤儿容器 | [SandboxDashboardPage](#sandboxdashboardpage-沙箱仪表板页) |

---

### 8. 提供商管理 (Providers API)
**路径前缀**: `/api/v1/providers`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 列出所有 LLM 提供商和账户 | [ProvidersPage](#providerspage-提供商管理页) |
| GET | `/status` | 获取使用配额和状态汇总 | [ProvidersPage](#providerspage-提供商管理页) |
| POST | `/detect-all` | 自动检测所有 CLI 令牌 | [ProvidersPage](#providerspage-提供商管理页) |
| POST | `/{provider_id}/detect` | 检测特定提供商的 CLI 令牌 | [ProvidersPage](#providerspage-提供商管理页) |
| POST | `/{provider_id}/connect` | 手动连接 API 密钥 | [ProvidersPage](#providerspage-提供商管理页) |
| DELETE | `/{provider_id}/accounts/{account_id}` | 删除账户 | [ProvidersPage](#providerspage-提供商管理页) |
| POST | `/test/{provider_id}/{account_id}` | 测试账户连接 | [ProvidersPage](#providerspage-提供商管理页) |
| POST | `/{provider_id}/toggle` | 启用/禁用提供商 | [ProvidersPage](#providerspage-提供商管理页) |
| GET | `/available-models` | 获取可用模型列表 | [ProvidersPage](#providerspage-提供商管理页) |
| GET | `/env` | 获取环境变量配置 | [ProvidersPage](#providerspage-提供商管理页) |
| POST | `/env` | 更新环境变量 | [ProvidersPage](#providerspage-提供商管理页) |

---

### 9. 知识管理 (Knowledge API)
**路径前缀**: `/api/v1/knowledge`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| POST | `/upload` | 上传知识文档 | [KnowledgePage](#knowledgepage-知识管理页) |
| GET | `/documents` | 列出所有文档 | [KnowledgePage](#knowledgepage-知识管理页) |
| GET | `/documents/{doc_id}` | 获取文档详情 | [KnowledgePage](#knowledgepage-知识管理页) |
| DELETE | `/documents/{doc_id}` | 删除文档 | [KnowledgePage](#knowledgepage-知识管理页) |
| GET | `/search` | 按漏洞类型搜索知识 | [KnowledgePage](#knowledgepage-知识管理页) |
| GET | `/stats` | 获取知识库统计 | [KnowledgePage](#knowledgepage-知识管理页) |

---

### 10. MCP 服务器 (MCP API)
**路径前缀**: `/api/v1/mcp`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/servers` | 列出所有 MCP 服务器 | [MCPManagementPage](#mcpmanagementpage-mcp-服务器管理页) |
| GET | `/servers/{name}` | 获取服务器详情 | [MCPManagementPage](#mcpmanagementpage-mcp-服务器管理页) |
| POST | `/servers` | 创建新 MCP 服务器配置 | [MCPManagementPage](#mcpmanagementpage-mcp-服务器管理页) |
| PUT | `/servers/{name}` | 更新服务器配置 | [MCPManagementPage](#mcpmanagementpage-mcp-服务器管理页) |
| DELETE | `/servers/{name}` | 删除服务器 | [MCPManagementPage](#mcpmanagementpage-mcp-服务器管理页) |
| POST | `/servers/{name}/toggle` | 启用/禁用服务器 | [MCPManagementPage](#mcpmanagementpage-mcp-服务器管理页) |
| POST | `/servers/{name}/test` | 测试服务器连接 | [MCPManagementPage](#mcpmanagementpage-mcp-服务器管理页) |
| GET | `/servers/{name}/tools` | 列出服务器工具 | [MCPManagementPage](#mcpmanagementpage-mcp-服务器管理页) |

---

### 11. 调度器 (Scheduler API)
**路径前缀**: `/api/v1/scheduler`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 列出所有定时任务 | [SchedulerPage](#schedulerpage-调度器页) |
| POST | `/` | 创建新定时任务 | [SchedulerPage](#schedulerpage-调度器页) |
| DELETE | `/{job_id}` | 删除定时任务 | [SchedulerPage](#schedulerpage-调度器页) |
| POST | `/{job_id}/pause` | 暂停定时任务 | [SchedulerPage](#schedulerpage-调度器页) |
| POST | `/{job_id}/resume` | 恢复定时任务 | [SchedulerPage](#schedulerpage-调度器页) |
| GET | `/agent-roles` | 获取可用代理角色 | [SchedulerPage](#schedulerpage-调度器页) |

---

### 12. 仪表板 (Dashboard API)
**路径前缀**: `/api/v1/dashboard`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/stats` | 获取总体统计数据 | [HomePage](#homepage-主页仪表板) |
| GET | `/recent` | 获取最近扫描和漏洞 | [HomePage](#homepage-主页仪表板) |
| GET | `/findings` | 获取最近发现 | [HomePage](#homepage-主页仪表板) |
| GET | `/vulnerability-types` | 获取漏洞类型分布 | [HomePage](#homepage-主页仪表板) |
| GET | `/scan-history` | 获取扫描历史图表数据 | [HomePage](#homepage-主页仪表板) |
| GET | `/agent-tasks` | 获取最近代理任务 | [HomePage](#homepage-主页仪表板) |
| GET | `/activity-feed` | 获取统一活动流 | [HomePage](#homepage-主页仪表板) |

---

### 13. 设置 (Settings API)
**路径前缀**: `/api/v1/settings`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 获取系统设置 | [SettingsPage](#settingspage-设置页) |
| PUT | `/` | 更新系统设置 | [SettingsPage](#settingspage-设置页) |
| GET | `/config` | 获取配置文件内容 | [SettingsPage](#settingspage-设置页) |
| POST | `/config` | 保存配置文件 | [SettingsPage](#settingspage-设置页) |

---

### 14. 提示词库 (Prompts API)
**路径前缀**: `/api/v1/prompts`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/presets` | 获取提示词预设列表 | [NewScanPage](#newscanpage-ai-agent-新扫描页) |
| GET | `/presets/{preset_id}` | 获取单个预设详情 | [NewScanPage](#newscanpage-ai-agent-新扫描页) |
| POST | `/parse` | 解析提示词 | [NewScanPage](#newscanpage-ai-agent-新扫描页) |
| GET | `/` | 获取自定义提示词列表 | [NewScanPage](#newscanpage-ai-agent-新扫描页) |
| POST | `/` | 创建自定义提示词 | [NewScanPage](#newscanpage-ai-agent-新扫描页) |
| POST | `/upload` | 上传提示词文件 | [NewScanPage](#newscanpage-ai-agent-新扫描页) |

---

### 15. WebSocket 接口
| 端点 | 功能描述 | 相关前端 |
|------|----------|----------|
| `/ws/scan/{scan_id}` | 扫描实时更新推送 | [ScanDetailsPage](#scandetailspage-扫描详情页) |

---

### 16. 健康检查
| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/api/health` | 系统健康检查和 LLM 状态 | [HomePage](#homepage-主页仪表板) |

---

## 前端页面功能

### HomePage (主页仪表板)
**路径**: `/`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 统计卡片网格 | 显示总扫描数、运行中、完成、总漏洞、严重、高危 | `GET /api/v1/dashboard/stats` |
| 漏洞严重程度环形图 | 可视化展示漏洞分布 | `GET /api/v1/dashboard/stats` |
| 扫描状态环形图 | 可视化展示扫描状态分布 | `GET /api/v1/dashboard/stats` |
| 活跃代理卡片 | 显示当前运行中的 AI 代理，可跳转 | `GET /api/v1/agent/active` |
| 最近扫描列表 | 显示最近扫描记录，可跳转详情 | `GET /api/v1/dashboard/recent` |
| 最近发现列表 | 显示最近漏洞发现，带验证状态 | `GET /api/v1/dashboard/findings` |
| 活动流 | 显示统一活动时间线，可过滤类型 | `GET /api/v1/dashboard/activity-feed` |
| 快速操作按钮 | 一键跳转到 Auto Pentest、Full IA、Vuln Lab、Terminal | 路由导航 |
| 刷新按钮 | 手动刷新仪表板数据 | `GET /api/v1/dashboard/*` |
| 侧边栏折叠/展开 | 切换侧边栏显示模式 | - |

---

### NewScanPage (AI Agent 新扫描页)
**路径**: `/scan/new`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 操作模式选择 | Full Auto, Recon Only, AI Prompt Mode, Analyze Only | - |
| Single URL 输入框 | 输入单个目标 URL | - |
| Multiple URLs 文本区域 | 输入多个 URL (逗号/换行分隔) | - |
| Upload File 按钮 | 上传包含 URL 的文件 | `POST /api/v1/targets/upload` |
| 目标验证 | 验证 URL 格式和可达性 | `POST /api/v1/targets/validate/bulk` |
| 任务库展开/折叠 | 显示/隐藏任务选择区域 | - |
| 任务分类筛选 | 按分类过滤任务列表 | `GET /api/v1/agent/tasks` |
| 任务卡片选择 | 选择预设任务或自定义任务 | `GET /api/v1/agent/tasks/{task_id}` |
| 自定义提示词切换 | 切换使用自定义提示词而不是任务 | - |
| 自定义提示词输入区 | 输入自定义系统提示词 | - |
| 认证选项展开/折叠 | 显示/隐藏认证配置 | - |
| 认证类型选择 | None, Cookie, Bearer Token, Basic Auth, Custom Header | - |
| 认证值输入 | 输入认证凭证 | - |
| 高级选项展开/折叠 | 显示/隐藏高级设置 | - |
| 最大深度滑块 | 设置爬虫深度 | - |
| 部署代理按钮 | 启动 AI 代理扫描 | `POST /api/v1/agent/run` |
| 取消按钮 | 返回主页 | 路由导航 |

---

### AutoPentestPage (一键自动渗透页)
**路径**: `/auto`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 目标 URL 输入 | 输入渗透测试目标 | - |
| 子域发现切换 | 启用/禁用子域枚举 | - |
| Kali 沙箱切换 | 启用/禁用 Kali 沙箱执行 | - |
| CLI Agent 切换 | 启用/禁用 CLI 代理模式 | - |
| 自定义提示词输入 | 可选的自定义提示词 | - |
| 自定义提示词 ID 输入 | 可选的自定义提示词 ID | - |
| 方法文件输入 | 可选的外部方法文件 | - |
| 首选提供商选择 | 选择 LLM 提供商 | - |
| 首选模型选择 | 选择 LLM 模型 | - |
| 开始一键渗透按钮 | 启动完整自动化渗透测试 | `POST /api/v1/agent/run` (mode=auto_pentest) |

---

### FullIATestingPage (全 AI 测试页)
**路径**: `/full-ia`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 目标选择 | 选择测试目标 | - |
| 漏洞类型多选 | 选择要测试的所有漏洞类型 | `GET /api/v1/vuln-lab/types` |
| 并行度设置 | 设置同时运行的漏洞代理数量 | - |
| 开始完整测试按钮 | 启动全 AI 驱动测试 | `POST /api/v1/full-ia/run` |

---

### RealtimeTaskPage (实时任务页)
**路径**: `/realtime`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 创建会话按钮 | 创建新的实时任务会话 | `POST /api/v1/agent/realtime/session` |
| 会话列表 | 显示所有活跃/历史会话 | `GET /api/v1/agent/realtime/sessions/list` |
| 会话选择 | 切换查看不同会话 | `GET /api/v1/agent/realtime/{session_id}` |
| 聊天输入框 | 发送自然语言指令给 AI | `POST /api/v1/agent/realtime/{session_id}/message` |
| 聊天消息流 | 显示 AI 和用户的对话历史 | `GET /api/v1/agent/realtime/{session_id}` |
| 工具执行按钮 | 手动调用安全工具 | `POST /api/v1/agent/realtime/{session_id}/execute-tool` |
| 工具列表面板 | 显示可用工具 | `GET /api/v1/agent/realtime/tools/list` |
| 生成报告按钮 | 为会话生成安全报告 | `GET /api/v1/agent/realtime/{session_id}/report` |
| 删除会话按钮 | 删除当前会话 | `DELETE /api/v1/agent/realtime/{session_id}` |

---

### VulnLabPage (漏洞实验室页)
**路径**: `/vuln-lab`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 漏洞类型分类选择 | 选择漏洞类别 (Injection, File Access, Auth 等) | `GET /api/v1/vuln-lab/types` |
| 具体漏洞类型选择 | 选择要测试的具体漏洞类型 | `GET /api/v1/vuln-lab/types` |
| 目标 URL 输入 | 输入实验室/CTF 目标 | - |
| 挑战名称输入 | 可选的挑战名称 | - |
| 认证配置 | Cookie/Bearer/Basic/Header 认证 | - |
| 自定义头设置 | 可选的自定义 HTTP 头 | - |
| 备注输入 | 可选的挑战备注 | - |
| 开始测试按钮 | 启动针对性漏洞测试 | `POST /api/v1/vuln-lab/run` |
| 挑战列表 | 显示所有历史挑战 | `GET /api/v1/vuln-lab/challenges` |
| 挑战筛选器 | 按类型、状态、结果筛选 | `GET /api/v1/vuln-lab/challenges?*` |
| 实时状态面板 | 显示正在运行的挑战进度 | `GET /api/v1/vuln-lab/challenges/{challenge_id}` |
| 日志查看 | 查看挑战执行日志 | `GET /api/v1/vuln-lab/logs/{challenge_id}` |
| 停止挑战按钮 | 停止运行中的挑战 | `POST /api/v1/vuln-lab/challenges/{challenge_id}/stop` |
| 删除挑战按钮 | 删除挑战记录 | `DELETE /api/v1/vuln-lab/challenges/{challenge_id}` |
| 统计卡片 | 显示实验室总体统计 | `GET /api/v1/vuln-lab/stats` |

---

### TerminalAgentPage (终端代理页)
**路径**: `/terminal`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 创建会话按钮 | 创建新终端会话 | `POST /api/v1/terminal/session` |
| 模板选择 | 选择预定义场景模板 | `GET /api/v1/terminal/templates` |
| 会话列表 | 显示所有会话 | `GET /api/v1/terminal/sessions` |
| 聊天区域 | 与 AI 助手对话 | `POST /api/v1/terminal/sessions/{session_id}/message` |
| 终端输出区 | 显示命令执行结果 | - |
| 命令输入框 | 手动输入命令 | `POST /api/v1/terminal/sessions/{session_id}/execute` |
| 执行按钮 | 执行输入的命令 | `POST /api/v1/terminal/sessions/{session_id}/execute` |
| 利用路径面板 | 记录和显示利用步骤 | `GET /api/v1/terminal/sessions/{session_id}/exploitation-path` |
| 添加步骤按钮 | 记录新的利用步骤 | `POST /api/v1/terminal/sessions/{session_id}/exploitation-path` |
| VPN 状态显示 | 显示 VPN 连接状态 | `GET /api/v1/terminal/sessions/{session_id}/vpn-status` |
| VPN 配置上传 | 上传 OpenVPN 配置文件 | `POST /api/v1/terminal/sessions/{session_id}/vpn/upload` |
| VPN 连接按钮 | 连接 VPN | `POST /api/v1/terminal/sessions/{session_id}/vpn/connect` |
| VPN 断开按钮 | 断开 VPN | `POST /api/v1/terminal/sessions/{session_id}/vpn/disconnect` |
| 删除会话按钮 | 删除会话 | `DELETE /api/v1/terminal/sessions/{session_id}` |

---

### AgentStatusPage (代理状态页)
**路径**: `/agent/{agent_id}`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 状态头部 | 显示代理状态、进度、阶段、目标 | `GET /api/v1/agent/status/{agent_id}` |
| 日志面板 | 实时显示代理执行日志 | `GET /api/v1/agent/logs/{agent_id}` |
| 发现结果面板 | 显示已发现的漏洞列表 | `GET /api/v1/agent/findings/{agent_id}` |
| 工具执行记录 | 显示所有工具执行历史 | `GET /api/v1/agent/status/{agent_id}` |
| 容器状态卡片 | 显示 Kali 沙箱状态 | `GET /api/v1/agent/status/{agent_id}` |
| 自定义提示词输入 | 发送自定义提示词给代理 | `POST /api/v1/agent/prompt/{agent_id}` |
| 暂停按钮 | 暂停代理执行 | `POST /api/v1/agent/pause/{agent_id}` |
| 恢复按钮 | 恢复代理执行 | `POST /api/v1/agent/resume/{agent_id}` |
| 停止按钮 | 停止代理并保存结果 | `POST /api/v1/agent/stop/{agent_id}` |
| 跳转阶段选择 | 选择要跳转到的阶段 | `POST /api/v1/agent/skip-to/{agent_id}/{phase}` |

---

### ScanDetailsPage (扫描详情页)
**路径**: `/scan/{scan_id}`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 扫描状态头部 | 显示扫描基本信息和状态 | `GET /api/v1/scans/{scan_id}` |
| 代理状态链接 | 跳转到关联的代理状态页 | `GET /api/v1/agent/by-scan/{scan_id}` |
| 端点列表 | 显示所有发现的端点 | `GET /api/v1/scans/{scan_id}/endpoints` |
| 漏洞列表 | 显示发现的漏洞，按严重度筛选 | `GET /api/v1/scans/{scan_id}/vulnerabilities` |
| 漏洞详情卡片 | 显示单个漏洞的完整信息 | `GET /api/v1/vulnerabilities/{vuln_id}` |
| 验证状态选择 | 手动设置验证状态 | `PATCH /api/v1/scans/vulnerabilities/{vuln_id}/validate` |
| 反馈提交 | 提交真假阳性反馈 | `POST /api/v1/scans/vulnerabilities/{vuln_id}/feedback` |
| 生成报告按钮 | 生成扫描报告 | `POST /api/v1/reports` |
| AI 生成报告按钮 | AI 生成详细报告 | `POST /api/v1/reports/ai-generate` |
| 三重检查按钮 | 用不同模型重新验证 | `POST /api/v1/agent/triple-check/{scan_id}` |
| 暂停/恢复/停止控制 | 控制扫描执行 | `POST /api/v1/scans/{scan_id}/{pause\|resume\|stop}` |

---

### ReportsPage (报告管理页)
**路径**: `/reports`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 报告列表 | 显示所有报告，可过滤 | `GET /api/v1/reports` |
| 扫描 ID 筛选 | 按扫描筛选报告 | `GET /api/v1/reports?scan_id=` |
| 自动生成筛选 | 筛选自动/手动报告 | `GET /api/v1/reports?auto_generated=` |
| 查看报告按钮 | 跳转到报告查看页 | 路由导航 |
| 下载按钮 | 下载各种格式的报告 | `GET /api/v1/reports/{report_id}/download/{format}` |
| 下载 ZIP 按钮 | 下载完整报告包 | `GET /api/v1/reports/{report_id}/download-zip` |
| 删除报告按钮 | 删除报告 | `DELETE /api/v1/reports/{report_id}` |

---

### ReportViewPage (报告查看页)
**路径**: `/reports/{report_id}`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 报告内容区 | 显示 HTML 格式报告 | `GET /api/v1/reports/{report_id}/view` |
| 执行摘要 | 显示发现概览 | `GET /api/v1/reports/{report_id}` |
| 严重度分布图表 | 可视化漏洞分布 | `GET /api/v1/reports/{report_id}` |
| 漏洞详情表格 | 列出所有漏洞 | `GET /api/v1/reports/{report_id}` |
| 下载菜单 | 选择格式下载 | `GET /api/v1/reports/{report_id}/download/{format}` |

---

### TaskLibraryPage (任务库页)
**路径**: `/tasks`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 任务分类筛选 | 按分类筛选任务 | `GET /api/v1/agent/tasks` |
| 任务卡片网格 | 显示所有任务 | `GET /api/v1/agent/tasks` |
| 任务详情展开 | 显示任务完整信息 | `GET /api/v1/agent/tasks/{task_id}` |
| 创建任务按钮 | 打开创建任务表单 | - |
| 任务名称输入 | 输入新任务名称 | - |
| 任务描述输入 | 输入任务描述 | - |
| 任务提示词输入 | 输入任务系统提示词 | - |
| 分类选择 | 选择任务分类 | - |
| 标签输入 | 添加标签 | - |
| 保存任务按钮 | 保存新任务 | `POST /api/v1/agent/tasks` |
| 删除任务按钮 | 删除自定义任务 | `DELETE /api/v1/agent/tasks/{task_id}` |
| 使用任务按钮 | 跳转到新扫描页并选中任务 | 路由导航 |

---

### KnowledgePage (知识管理页)
**路径**: `/knowledge`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 文档列表 | 显示所有上传的知识文档 | `GET /api/v1/knowledge/documents` |
| 上传区域 | 拖拽或点击上传文档 | `POST /api/v1/knowledge/upload` |
| 文档卡片 | 显示文档信息 | `GET /api/v1/knowledge/documents/{doc_id}` |
| 删除文档按钮 | 删除文档 | `DELETE /api/v1/knowledge/documents/{doc_id}` |
| 搜索框 | 按漏洞类型搜索知识 | `GET /api/v1/knowledge/search?vuln_type=` |
| 统计卡片 | 显示知识库统计 | `GET /api/v1/knowledge/stats` |

---

### MCPManagementPage (MCP 服务器管理页)
**路径**: `/mcp`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 服务器列表 | 显示所有配置的 MCP 服务器 | `GET /api/v1/mcp/servers` |
| 创建服务器按钮 | 打开创建表单 | - |
| 服务器名称输入 | 输入服务器名称 | - |
| 传输类型选择 | Stdio/HTTP/WebSocket | - |
| 命令/URL 输入 | 配置连接参数 | - |
| 环境变量设置 | 配置环境变量 | - |
| 保存服务器按钮 | 保存配置 | `POST /api/v1/mcp/servers` |
| 编辑服务器按钮 | 修改现有配置 | `PUT /api/v1/mcp/servers/{name}` |
| 删除服务器按钮 | 删除服务器 | `DELETE /api/v1/mcp/servers/{name}` |
| 启用/禁用切换 | 切换服务器状态 | `POST /api/v1/mcp/servers/{name}/toggle` |
| 测试连接按钮 | 测试服务器连接 | `POST /api/v1/mcp/servers/{name}/test` |
| 查看工具按钮 | 显示服务器提供的工具 | `GET /api/v1/mcp/servers/{name}/tools` |

---

### ProvidersPage (提供商管理页)
**路径**: `/providers`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 提供商列表 | 显示所有 LLM 提供商 | `GET /api/v1/providers` |
| 状态汇总卡片 | 显示配额和使用情况 | `GET /api/v1/providers/status` |
| 检测所有 CLI 令牌按钮 | 自动检测 CLI 会话中的令牌 | `POST /api/v1/providers/detect-all` |
| 检测单个提供商令牌按钮 | 检测特定提供商 | `POST /api/v1/providers/{provider_id}/detect` |
| 连接新账户表单 | 手动添加 API 密钥 | `POST /api/v1/providers/{provider_id}/connect` |
| 账户标签输入 | 设置账户显示名称 | - |
| API 密钥输入 | 输入 API 密钥 | - |
| 模型覆盖输入 | 可选的模型覆盖 | - |
| 测试连接按钮 | 测试账户是否有效 | `POST /api/v1/providers/test/{provider_id}/{account_id}` |
| 删除账户按钮 | 删除账户 | `DELETE /api/v1/providers/{provider_id}/accounts/{account_id}` |
| 启用/禁用提供商切换 | 切换提供商是否可用 | `POST /api/v1/providers/{provider_id}/toggle` |
| 可用模型列表 | 显示所有可用模型 | `GET /api/v1/providers/available-models` |
| 环境变量编辑器 | 查看和编辑 .env | `GET /api/v1/providers/env`, `POST /api/v1/providers/env` |

---

### SandboxDashboardPage (沙箱仪表板页)
**路径**: `/sandboxes`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 池状态卡片 | 显示活跃容器数、最大并发、镜像信息等 | `GET /api/v1/sandbox/` |
| 容器列表 | 显示所有沙箱容器 | `GET /api/v1/sandbox/` |
| 健康检查按钮 | 检查单个沙箱状态 | `GET /api/v1/sandbox/{scan_id}` |
| 销毁按钮 | 销毁指定沙箱 | `DELETE /api/v1/sandbox/{scan_id}` |
| 清理所有按钮 | 销毁所有沙箱 | `POST /api/v1/sandbox/cleanup` |
| 清理孤儿按钮 | 清理孤立容器 | `POST /api/v1/sandbox/cleanup-orphans` |

---

### SchedulerPage (调度器页)
**路径**: `/scheduler`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 定时任务列表 | 显示所有定时任务 | `GET /api/v1/scheduler/` |
| 创建任务按钮 | 打开创建表单 | - |
| 目标输入 | 设置扫描目标 | - |
| 扫描类型选择 | 选择扫描类型 | - |
| Cron 表达式输入 | 设置执行时间表 | - |
| 间隔分钟输入 | 或者设置固定间隔 | - |
| 代理角色选择 | 选择预定义代理角色 | `GET /api/v1/scheduler/agent-roles` |
| LLM 配置选择 | 选择 LLM 配置 | - |
| 保存任务按钮 | 保存定时任务 | `POST /api/v1/scheduler/` |
| 暂停任务按钮 | 暂停定时任务 | `POST /api/v1/scheduler/{job_id}/pause` |
| 恢复任务按钮 | 恢复定时任务 | `POST /api/v1/scheduler/{job_id}/resume` |
| 删除任务按钮 | 删除定时任务 | `DELETE /api/v1/scheduler/{job_id}` |

---

### SettingsPage (设置页)
**路径**: `/settings`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 系统设置表单 | 编辑各项系统配置 | `GET /api/v1/settings`, `PUT /api/v1/settings` |
| 配置文件编辑器 | 直接编辑配置文件 | `GET /api/v1/settings/config`, `POST /api/v1/settings/config` |
| 学习统计显示 | 显示自适应学习统计 | `GET /api/v1/scans/vulnerabilities/learning/stats` |
| LLM 配置区域 | 查看和设置 LLM 相关配置 | - |
| 扫描设置区域 | 并发限制、超时、速率限制等 | - |
| 功能开关区域 | 启用/禁用各种功能模块 | - |
| 保存设置按钮 | 保存所有更改 | `PUT /api/v1/settings` |

---

## 数据模型结构

### 数据库实体关系图

```
┌─────────────────┐
│     Scan        │
│  (主扫描记录)    │
├─────────────────┤
│ id (PK)         │
│ name            │
│ status          │
│ progress        │
│ current_phase   │
│ auth_type       │
│ created_at      │
│ started_at      │
│ completed_at    │
│ total_endpoints │
│ total_vulns     │
│ critical_count  │
└────────┬────────┘
         │1
         │
         │N
┌────────▼────────┐
│    Target       │
│ (目标URL)       │
├─────────────────┤
│ id (PK)         │
│ scan_id (FK)    │
│ url             │
│ hostname        │
│ port            │
│ protocol        │
└────────┬────────┘
         │
         │
         │
         │N
┌────────▼────────┐
│    Endpoint     │
│ (发现的端点)    │
├─────────────────┤
│ id (PK)         │
│ scan_id (FK)    │
│ target_id (FK)  │
│ url             │
│ method          │
│ parameters      │
│ technologies    │
│ interesting     │
└────────┬────────┘
         │
         │
         │
         │N
┌────────▼────────┐     ┌─────────────────┐
│  Vulnerability  │     │ Vulnerability-  │
│  (漏洞记录)     │◄────┤ Test (测试记录) │
├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │
│ scan_id (FK)    │     │ scan_id (FK)    │
│ test_id (FK)    │     │ endpoint_id (FK)│
│ title           │     │ vuln_type       │
│ vuln_type       │     │ payload         │
│ severity        │     │ is_vulnerable   │
│ cvss_score      │     │ evidence        │
│ cvss_vector     │     └─────────────────┘
│ cwe_id          │
│ description     │
│ affected_endpoint│
│ poc_request     │
│ poc_response    │
│ poc_payload     │
│ poc_code        │
│ screenshots     │
│ confidence_score│
│ validation_status│
└────────┬────────┘
         │
         │
         │
         │N
┌────────▼────────┐
│    Report       │
│ (报告记录)      │
├─────────────────┤
│ id (PK)         │
│ scan_id (FK)    │
│ title           │
│ format          │
│ executive_summary│
│ auto_generated  │
│ is_partial      │
│ generated_at    │
└─────────────────┘

┌─────────────────┐
│   AgentTask     │
│(代理任务记录)   │
├─────────────────┤
│ id (PK)         │
│ scan_id (FK)    │
│ task_type       │
│ task_name       │
│ tool_name       │
│ status          │
│ started_at      │
│ completed_at    │
│ duration_ms     │
│ items_processed │
│ items_found     │
└─────────────────┘

┌─────────────────┐
│   Prompt        │
│(自定义提示词)   │
├─────────────────┤
│ id (PK)         │
│ name            │
│ description     │
│ content         │
│ is_preset       │
│ category        │
└─────────────────┘

┌─────────────────┐
│ VulnLabChallenge│
│(漏洞实验室挑战) │
├─────────────────┤
│ id (PK)         │
│ target_url      │
│ challenge_name  │
│ vuln_type       │
│ vuln_category   │
│ status          │
│ result          │
│ agent_id        │
│ scan_id         │
│ findings_count  │
│ logs            │
│ created_at      │
└─────────────────┘
```

### 核心数据模型详解

#### 1. Scan 模型 (扫描主记录)
**文件**: [backend/models/scan.py](file:///workspace/backend/models/scan.py)

字段说明:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(36) | UUID主键 |
| name | String(255) | 扫描名称 (可选) |
| status | String(50) | 扫描状态 (pending/running/completed/failed/stopped) |
| scan_type | String(50) | 扫描类型 (quick/full/custom) |
| recon_enabled | Boolean | 是否启用侦察 |
| progress | Integer | 进度百分比 (0-100) |
| current_phase | String(50) | 当前阶段 (recon/testing/reporting) |
| config | JSON | 扫描配置参数 |
| custom_prompt | Text | 自定义提示词 |
| prompt_id | String(36) | 关联的提示词ID |
| auth_type | String(50) | 认证类型 (none/cookie/header/basic/bearer) |
| auth_credentials | JSON | 认证凭证 (加密存储) |
| custom_headers | JSON | 自定义HTTP头 |
| created_at | DateTime | 创建时间 |
| started_at | DateTime | 开始时间 |
| completed_at | DateTime | 完成时间 |
| duration | Integer | 持续时间(秒) |
| error_message | Text | 错误信息 |
| total_endpoints | Integer | 发现的端点总数 |
| total_vulnerabilities | Integer | 发现的漏洞总数 |
| critical_count | Integer | Critical级别漏洞数 |
| high_count | Integer | High级别漏洞数 |
| medium_count | Integer | Medium级别漏洞数 |
| low_count | Integer | Low级别漏洞数 |
| info_count | Integer | Info级别漏洞数 |

关系:
- targets (1:N) - 关联的目标URL列表
- endpoints (1:N) - 发现的端点列表
- vulnerabilities (1:N) - 发现的漏洞列表
- reports (1:N) - 生成的报告列表
- agent_tasks (1:N) - 执行的代理任务列表

---

#### 2. Target 模型 (目标URL)
**文件**: [backend/models/target.py](file:///workspace/backend/models/target.py)

字段说明:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(36) | UUID主键 |
| scan_id | String(36) | 关联的扫描ID(外键) |
| url | String(2048) | 完整URL |
| hostname | String(255) | 主机名 |
| port | Integer | 端口号 |
| protocol | String(10) | 协议 (http/https) |
| path | String(2048) | 路径 |
| status | String(50) | 状态 |
| created_at | DateTime | 创建时间 |

关系:
- scan (N:1) - 所属的扫描
- endpoints (1:N) - 从此目标发现的端点

---

#### 3. Endpoint 模型 (发现的端点)
**文件**: [backend/models/endpoint.py](file:///workspace/backend/models/endpoint.py)

字段说明:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(36) | UUID主键 |
| scan_id | String(36) | 关联的扫描ID(外键) |
| target_id | String(36) | 关联的目标ID(外键) |
| url | Text | 完整URL |
| method | String(10) | HTTP方法 (GET/POST/PUT/DELETE等) |
| path | Text | URL路径 |
| parameters | JSON | 参数列表 [{name, type, value}] |
| headers | JSON | 响应头 |
| response_status | Integer | 响应状态码 |
| content_type | String(100) | 内容类型 |
| content_length | Integer | 内容长度 |
| technologies | JSON | 识别的技术栈列表 |
| interesting | Boolean | 是否标记为"有趣"的端点 |
| discovered_at | DateTime | 发现时间 |

关系:
- scan (N:1) - 所属的扫描
- target (N:1) - 来源目标
- vulnerability_tests (1:N) - 针对此端点的测试

---

#### 4. Vulnerability 模型 (漏洞记录)
**文件**: [backend/models/vulnerability.py](file:///workspace/backend/models/vulnerability.py)

字段说明:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(36) | UUID主键 |
| scan_id | String(36) | 关联的扫描ID(外键) |
| test_id | String(36) | 关联的测试记录ID(外键) |
| title | String(500) | 漏洞标题 |
| vulnerability_type | String(100) | 漏洞类型 (xss_reflected/sqli_union等) |
| severity | String(20) | 严重级别 (critical/high/medium/low/info) |
| cvss_score | Float | CVSS评分 (0-10) |
| cvss_vector | String(100) | CVSS向量字符串 |
| cwe_id | String(50) | CWE编号 (如CWE-79) |
| description | Text | 漏洞描述 |
| affected_endpoint | Text | 受影响的端点URL |
| poc_request | Text | PoC请求 |
| poc_response | Text | PoC响应 |
| poc_payload | Text | PoC有效载荷 |
| poc_parameter | String(500) | 漏洞参数 |
| poc_evidence | Text | 漏洞证据 |
| impact | Text | 影响分析 |
| remediation | Text | 修复建议 |
| references | JSON | 参考链接列表 |
| ai_analysis | Text | AI补充分析 |
| poc_code | Text | 可执行的PoC代码 |
| screenshots | JSON | 截图列表 (base64或文件路径) |
| url | Text | 来源URL |
| parameter | String(500) | 来源参数 |
| confidence_score | Integer | 置信度 (0-100) |
| confidence_breakdown | JSON | 置信度细分 (proof/impact/controls) |
| proof_of_execution | Text | 执行证明 |
| validation_status | String(20) | 验证状态 (ai_confirmed/validated/false_positive/pending_review) |
| ai_rejection_reason | Text | AI拒绝原因 |
| created_at | DateTime | 创建时间 |

关系:
- scan (N:1) - 所属的扫描
- test (1:1) - 关联的测试记录

---

#### 5. VulnerabilityTest 模型 (漏洞测试记录)
**文件**: [backend/models/vulnerability.py](file:///workspace/backend/models/vulnerability.py)

字段说明:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(36) | UUID主键 |
| scan_id | String(36) | 关联的扫描ID(外键) |
| endpoint_id | String(36) | 关联的端点ID(外键) |
| vulnerability_type | String(100) | 测试的漏洞类型 |
| payload | Text | 使用的有效载荷 |
| request_data | JSON | 请求数据 |
| response_data | JSON | 响应数据 |
| is_vulnerable | Boolean | 是否判定为漏洞 |
| confidence | Float | 置信度 (0.0-1.0) |
| evidence | Text | 证据 |
| tested_at | DateTime | 测试时间 |

关系:
- scan (N:1) - 所属的扫描
- endpoint (N:1) - 测试的端点
- vulnerability (1:1) - 生成的漏洞记录

---

#### 6. Report 模型 (报告记录)
**文件**: [backend/models/report.py](file:///workspace/backend/models/report.py)

字段说明:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(36) | UUID主键 |
| scan_id | String(36) | 关联的扫描ID(外键) |
| title | String(255) | 报告标题 |
| format | String(20) | 格式 (html/pdf/json) |
| file_path | Text | 文件存储路径 |
| executive_summary | Text | 执行摘要 |
| auto_generated | Boolean | 是否自动生成 |
| is_partial | Boolean | 是否为部分报告 (未完成的扫描) |
| generated_at | DateTime | 生成时间 |

关系:
- scan (N:1) - 所属的扫描

---

#### 7. AgentTask 模型 (代理任务记录)
**文件**: [backend/models/agent_task.py](file:///workspace/backend/models/agent_task.py)

字段说明:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(36) | UUID主键 |
| scan_id | String(36) | 关联的扫描ID(外键) |
| task_type | String(50) | 任务类型 (recon/analysis/testing/reporting) |
| task_name | String(255) | 任务名称 |
| description | Text | 任务描述 |
| tool_name | String(100) | 使用的工具 (nmap/nuclei/claude等) |
| tool_category | String(50) | 工具类别 (scanner/analyzer/ai/crawler) |
| status | String(20) | 状态 (pending/running/completed/failed/cancelled) |
| started_at | DateTime | 开始时间 |
| completed_at | DateTime | 完成时间 |
| duration_ms | Integer | 持续时间(毫秒) |
| items_processed | Integer | 处理的项目数 |
| items_found | Integer | 发现的项目数 |
| result_summary | Text | 结果摘要 |
| error_message | Text | 错误信息 |
| created_at | DateTime | 创建时间 |

关系:
- scan (N:1) - 所属的扫描

方法:
- start() - 标记为开始
- complete(items_processed, items_found, summary) - 标记为完成
- fail(error) - 标记为失败

---

#### 8. Prompt 模型 (自定义提示词)
**文件**: [backend/models/prompt.py](file:///workspace/backend/models/prompt.py)

字段说明:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(36) | UUID主键 |
| name | String(255) | 提示词名称 |
| description | Text | 描述 |
| content | Text | 提示词内容 |
| is_preset | Boolean | 是否为预设提示词 |
| category | String(100) | 分类 (pentest/bug_bounty/api等) |
| parsed_vulnerabilities | JSON | AI解析出的漏洞类型列表 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

---

#### 9. VulnLabChallenge 模型 (漏洞实验室挑战)
**文件**: [backend/models/vuln_lab.py](file:///workspace/backend/models/vuln_lab.py)

字段说明:
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String(36) | UUID主键 |
| target_url | Text | 目标URL |
| challenge_name | String(255) | 挑战名称 |
| vuln_type | String(100) | 漏洞类型 |
| vuln_category | String(50) | 漏洞分类 |
| auth_type | String(20) | 认证类型 |
| auth_value | Text | 认证值 |
| status | String(20) | 状态 (pending/running/completed/failed/stopped) |
| result | String(20) | 结果 (detected/not_detected/error) |
| agent_id | String(36) | 关联的代理ID |
| scan_id | String(36) | 关联的扫描ID |
| findings_count | Integer | 发现数 |
| critical_count | Integer | Critical发现数 |
| high_count | Integer | High发现数 |
| medium_count | Integer | Medium发现数 |
| low_count | Integer | Low发现数 |
| info_count | Integer | Info发现数 |
| findings_detail | JSON | 发现详情列表 |
| started_at | DateTime | 开始时间 |
| completed_at | DateTime | 完成时间 |
| duration | Integer | 持续时间(秒) |
| notes | Text | 备注 |
| logs | JSON | 执行日志列表 |
| endpoints_count | Integer | 发现的端点数 |
| created_at | DateTime | 创建时间 |

---

### 内存状态管理

除了持久化存储外，系统还使用内存字典管理运行时状态:

| 字典 | 说明 | 位置 |
|------|------|------|
| `agent_results` | 代理结果缓存 | [backend/api/v1/agent.py](file:///workspace/backend/api/v1/agent.py) |
| `agent_tasks` | 异步任务字典 | [backend/api/v1/agent.py](file:///workspace/backend/api/v1/agent.py) |
| `agent_instances` | 代理实例字典 | [backend/api/v1/agent.py](file:///workspace/backend/api/v1/agent.py) |
| `agent_to_scan` | agent_id → scan_id映射 | [backend/api/v1/agent.py](file:///workspace/backend/api/v1/agent.py) |
| `scan_to_agent` | scan_id → agent_id映射 | [backend/api/v1/agent.py](file:///workspace/backend/api/v1/agent.py) |

---

## 页面流转与导航

### 前端路由表
**文件**: [frontend/src/App.tsx](file:///workspace/frontend/src/App.tsx)

| 路径 | 页面组件 | 说明 |
|------|----------|------|
| `/` | HomePage | 主页仪表板 |
| `/auto` | AutoPentestPage | 一键自动渗透 |
| `/full-ia` | FullIATestingPage | 全AI测试 |
| `/vuln-lab` | VulnLabPage | 漏洞实验室 |
| `/terminal` | TerminalAgentPage | 终端代理 |
| `/scan/new` | NewScanPage | 创建新扫描 |
| `/scan/:scan_id` | ScanDetailsPage | 扫描详情页 |
| `/agent/:agent_id` | AgentStatusPage | 代理状态页 |
| `/tasks` | TaskLibraryPage | 任务库 |
| `/realtime` | RealtimeTaskPage | 实时任务 |
| `/knowledge` | KnowledgePage | 知识管理 |
| `/mcp` | MCPManagementPage | MCP服务器管理 |
| `/scheduler` | SchedulerPage | 调度器 |
| `/sandboxes` | SandboxDashboardPage | 沙箱仪表板 |
| `/reports` | ReportsPage | 报告管理 |
| `/reports/:report_id` | ReportViewPage | 报告查看 |
| `/providers` | ProvidersPage | 提供商管理 |
| `/settings` | SettingsPage | 设置页 |

---

### 导航入口点

所有页面都通过侧边栏 (Sidebar) 导航，侧边栏包含以下导航项:

| 导航项 | 图标 | 跳转路径 |
|--------|------|----------|
| Dashboard | 🏠 | `/` |
| Auto Pentest | ⚡ | `/auto` |
| Full IA | 🤖 | `/full-ia` |
| Vuln Lab | 🧪 | `/vuln-lab` |
| Terminal | 💻 | `/terminal` |
| New Scan | ➕ | `/scan/new` |
| Tasks | 📋 | `/tasks` |
| Realtime | 🔄 | `/realtime` |
| Knowledge | 📚 | `/knowledge` |
| MCP | 🔌 | `/mcp` |
| Scheduler | ⏰ | `/scheduler` |
| Sandboxes | 📦 | `/sandboxes` |
| Reports | 📄 | `/reports` |
| Providers | 🔑 | `/providers` |
| Settings | ⚙️ | `/settings` |

---

### 核心页面流转路径

#### 1. 创建并执行扫描的完整流程

```
HomePage
    ↓ (点击 "New Scan" 按钮或侧边栏导航)
NewScanPage
    ├─→ 输入目标URL
    ├─→ (可选) 选择任务或输入自定义提示词
    ├─→ (可选) 配置认证
    ├─→ (可选) 配置高级选项
    ↓ (点击 "Deploy Agent" 按钮)
POST /api/v1/agent/run → 创建 Scan + Agent 记录
    ↓ (自动跳转)
AgentStatusPage (/agent/{agent_id})
    ├─→ 实时查看执行日志
    ├─→ 暂停/恢复/停止代理
    ├─→ 发送自定义提示词
    ├─→ 跳转到指定阶段
    └─→ 查看发现结果
    ↓ (扫描完成或停止后)
    ↓ (点击 "View Scan Details" 或通过 Scan 链接)
ScanDetailsPage (/scan/{scan_id})
    ├─→ 查看扫描统计
    ├─→ 查看发现的端点
    ├─→ 查看发现的漏洞
    ├─→ 验证漏洞状态
    ├─→ 生成报告
    └─→ AI生成详细报告
    ↓ (点击报告链接或 "View Report")
ReportViewPage (/reports/{report_id})
    ├─→ 查看HTML报告
    ├─→ 下载报告 (HTML/PDF/JSON)
    └─→ 下载完整报告ZIP
```

---

#### 2. 一键自动渗透流程

```
HomePage
    ↓ (点击 "Auto Pentest" 快速操作按钮)
AutoPentestPage
    ├─→ 输入目标
    ├─→ (可选) 启用子域发现
    ├─→ (可选) 启用Kali沙箱
    ├─→ (可选) 配置LLM提供商
    ↓ (点击 "Start Auto Pentest")
POST /api/v1/agent/run (mode=auto_pentest)
    ↓ (自动跳转)
AgentStatusPage
```

---

#### 3. 漏洞实验室测试流程

```
HomePage / VulnLabPage
    ↓ (选择漏洞类型分类)
VulnLabPage
    ├─→ 选择具体漏洞类型
    ├─→ 输入目标URL
    ├─→ (可选) 配置认证
    ↓ (点击 "Start Test")
POST /api/v1/vuln-lab/run → 创建 VulnLabChallenge + Agent
    ↓
VulnLabPage (实时状态更新)
    ├─→ 查看执行日志
    ├─→ 查看发现结果
    └─→ 停止测试
```

---

#### 4. 终端代理会话流程

```
HomePage / TerminalAgentPage
    ↓
TerminalAgentPage
    ├─→ (可选) 选择场景模板
    ├─→ 创建新会话 → POST /api/v1/terminal/session
    ├─→ 选择会话
    ├─→ 与AI聊天 → POST /api/v1/terminal/sessions/{id}/message
    ├─→ 执行命令 → POST /api/v1/terminal/sessions/{id}/execute
    ├─→ (可选) 记录利用路径步骤
    └─→ (可选) 连接VPN
```

---

#### 5. 报告生成与查看流程

```
HomePage / ReportsPage / ScanDetailsPage
    ↓
ReportsPage
    ├─→ 查看报告列表
    ├─→ (可选) 按扫描ID/自动生成筛选
    ├─→ (可选) 删除报告
    ↓ (点击 "View" 按钮)
ReportViewPage
    ├─→ 查看HTML报告内容
    ├─→ 下载各种格式
    └─→ 下载报告包
```

---

#### 6. 提供商配置流程

```
HomePage / ProvidersPage
    ↓
ProvidersPage
    ├─→ 查看提供商列表
    ├─→ 查看使用配额
    ├─→ 检测CLI令牌 → POST /api/v1/providers/detect-all
    ├─→ 手动连接账户 → POST /api/v1/providers/{id}/connect
    ├─→ 测试账户连接 → POST /api/v1/providers/test/{id}/{acc}
    └─→ 编辑环境变量 → POST /api/v1/providers/env
```

---

### 页面间的交叉链接

| 源页面 | 目标页面 | 触发条件 |
|--------|----------|----------|
| HomePage | AgentStatusPage | 点击活跃代理卡片 |
| HomePage | ScanDetailsPage | 点击最近扫描列表项 |
| HomePage | ReportsPage | 点击报告相关链接 |
| NewScanPage | AgentStatusPage | 成功启动代理后自动跳转 |
| AgentStatusPage | ScanDetailsPage | 点击 "View Scan" 链接 |
| ScanDetailsPage | AgentStatusPage | 点击 "View Agent Status" 链接 |
| ScanDetailsPage | ReportViewPage | 点击生成的报告 |
| ReportsPage | ReportViewPage | 点击报告 "View" 按钮 |
| ReportsPage | ScanDetailsPage | 点击扫描ID链接 |
| TaskLibraryPage | NewScanPage | 点击 "Use Task" 按钮 |
| VulnLabPage | AgentStatusPage | 如果挑战关联了代理 |

---

### 状态流转

#### 扫描状态流转

```
pending
    ↓ (开始扫描)
running
    ├─→ (用户暂停) → paused ──┐
    │                            │
    │   (用户恢复) ←────────────┘
    │
    ├─→ (用户停止) → stopped
    │
    └─→ (正常完成) → completed
    │
    └─→ (出错) → failed
```

#### 漏洞验证状态流转

```
ai_confirmed (AI初始状态)
    ↓ (用户验证)
    ├─→ validated (确认真阳性)
    └─→ false_positive (标记为假阳性)
```

---

## 核心工作流程

### 1. 自主代理扫描完整工作流

#### 步骤1: 初始化阶段
**触发点**: `POST /api/v1/agent/run`
**代码**: [backend/api/v1/agent.py](file:///workspace/backend/api/v1/agent.py)

流程:
1. 接收扫描配置 (目标、模式、提示词、认证等)
2. 创建数据库记录:
   - 创建 [Scan](file:///workspace/backend/models/scan.py) 记录 (status=pending)
   - 创建 [Target](file:///workspace/backend/models/target.py) 记录
3. 初始化内存状态:
   - 生成 agent_id (UUID)
   - 建立 agent_id ↔ scan_id 双向映射
   - 保存 agent_instances 实例
4. 在后台启动异步任务
5. 返回 agent_id 给前端

#### 步骤2: 侦察阶段 (Recon Phase)
**代码**: [backend/core/autonomous_agent.py](file:///workspace/backend/core/autonomous_agent.py)

流程:
1. 启动爬虫/发现工具
2. 发现URL和端点:
   - 从目标URL开始爬取
   - 提取链接、表单、API端点
   - 识别参数和输入点
3. 技术栈识别:
   - WAF检测
   - 框架识别 (React、Django等)
   - 技术指纹
4. 存储发现结果:
   - 创建 [Endpoint](file:///workspace/backend/models/endpoint.py) 记录
   - 标记 "interesting" 端点
5. 更新 [Scan](file:///workspace/backend/models/scan.py) 进度和阶段
6. 创建 [AgentTask](file:///workspace/backend/models/agent_task.py) 记录

#### 步骤3: 分析阶段 (Analyze Phase)
**代码**: [backend/core/autonomous_agent.py](file:///workspace/backend/core/autonomous_agent.py)

流程:
1. 收集所有发现的端点
2. AI分析:
   - 确定优先测试的端点
   - 识别潜在漏洞面
   - 构建测试计划
3. 优先级排序:
   - 基于风险评分
   - 基于可访问性
   - 基于用户自定义提示词
4. (可选) RAG知识注入:
   - 检索相关安全文档
   - 注入到提示词中

#### 步骤4: 测试阶段 (Test Phase)
**代码**: [backend/core/autonomous_agent.py](file:///workspace/backend/core/autonomous_agent.py) + [backend/core/vuln_engine/](file:///workspace/backend/core/vuln_engine/)

流程:
1. 遍历优先级队列中的端点
2. 对于每个端点:
   a. 选择适用的漏洞检测器
   b. 生成有效载荷
   c. 发送请求
   d. 分析响应
   e. 判定是否存在漏洞
3. 如果检测到漏洞:
   - 创建 [VulnerabilityTest](file:///workspace/backend/models/vulnerability.py) 记录
   - 执行验证 (Proof of Execution)
   - 创建 [Vulnerability](file:///workspace/backend/models/vulnerability.py) 记录
   - 赋值严重级别、CVSS评分
4. (可选) 漏洞代理编排:
   - 并行启动多个AI代理
   - 每个代理专攻特定漏洞类型
5. 更新 [Scan](file:///workspace/backend/models/scan.py) 统计 (total_vulns, counts)
6. 实时推送更新到前端 (WebSocket)

#### 步骤5: 报告阶段 (Report Phase)
**代码**: [backend/core/report_engine/](file:///workspace/backend/core/report_engine/)

流程:
1. 收集所有发现
2. AI分析:
   - 生成执行摘要
   - 提供修复建议
   - 按风险优先级排序
3. 生成 [Report](file:///workspace/backend/models/report.py) 记录
4. 输出多种格式 (HTML、PDF、JSON)
5. 更新 [Scan](file:///workspace/backend/models/scan.py) 状态为 completed

#### 步骤6: 后处理
1. 清理内存中的代理实例
2. (可选) 清理Kali沙箱容器
3. (可选) 自适应学习:
   - 记录用户的验证反馈
   - 优化未来扫描的判断

---

### 2. 漏洞检测的完整数据流

```
目标URL
    ↓
侦察阶段 → 发现端点 → 分析攻击面 → 测试阶段 → 漏洞验证 → 报告生成
```

---

### 3. Smart Router 的LLM调用路由流程

**路径**: [backend/core/smart_router/](file:///workspace/backend/core/smart_router/)

当系统需要调用LLM时:

1. Smart Router 接收请求和偏好的提供商/模型
2. 检查可用的已连接账户和配额:
   - 如果指定了提供商和模型，尝试使用该配置
   - 如果指定的不可用，自动回退到下一个可用的提供商
3. 根据配置的策略选择最佳的账户:
   - 负载均衡 (轮询或最少使用)
   - 故障转移 (自动切换到健康的账户)
   - 基于之前的成功/失败历史记录
4. 调用选择的提供商的API:
   - 如果启用了CLI令牌复用，使用CLI会话的令牌
   - 否则使用存储的API密钥
5. 记录调用的指标 (token使用、成功/失败状态、延迟)
6. 返回结果或处理错误:
   - 如果调用失败，自动尝试下一个可用的账户/提供商
   - 记录失败以便将来进行故障转移决策
7. 可选的自适应学习:
   - 基于验证反馈调整置信度阈值
   - 优化不同提供商的使用优先级

---

### 4. 实时任务的消息流 (RealtimeTask)

**相关页面**: [RealtimeTaskPage](file:///workspace/frontend/src/pages/RealtimeTaskPage.tsx)

当用户在实时任务页面发送消息时:

1. 用户在聊天框中输入自然语言指令
2. 点击发送 → `POST /api/v1/agent/realtime/{session_id}/message`
3. 后端接收请求:
   - 确定用户的意图
   - (可选) 检索相关的RAG知识
   - 构造合适的工具调用或直接回答
   - 如果需要，调用安全工具执行
   - 记录工具执行的结果
   - 生成AI回应
4. 结果返回前端:
   - 更新聊天历史
   - 显示工具执行的输出
   - 可用时显示发现的漏洞
5. 用户可以继续对话或:
   - 查看会话的报告
   - 删除会话
   - 手动执行特定的工具

---

## 功能关联性分析

### 数据流向
```
用户输入目标
    ↓
[NewScanPage / AutoPentestPage] → POST /api/v1/agent/run
    ↓
[Agent Orchestrator] 创建 Scan 记录 + 启动 AutonomousAgent
    ↓
[Recon Phase] 发现端点 → 存储到 Endpoint 表
    ↓
[Vuln Detection Phase] 检测漏洞 → 存储到 Vulnerability 表
    ↓
[Report Phase] 生成 Report 记录
    ↓
WebSocket 实时推送 → [HomePage / ScanDetailsPage]
    ↓
用户查看结果 → [ScanDetailsPage / ReportsPage]
```

### 核心依赖关系

| 功能模块 | 依赖的 API | 依赖的前端 |
|---------|-----------|----------|
| 自动渗透测试 | Agent API, Scans API, Reports API | AutoPentestPage, AgentStatusPage, ReportsPage |
| 漏洞实验室 | Vuln Lab API, Agent API | VulnLabPage, AgentStatusPage |
| 终端代理 | Terminal API, Sandbox API | TerminalAgentPage, SandboxDashboardPage |
| 实时任务 | Agent Realtime API | RealtimeTaskPage |
| 知识增强 | Knowledge API, RAG Engine | KnowledgePage |
| 智能路由 | Providers API, Smart Router | ProvidersPage |
| 报告生成 | Reports API, Scan/Agent Data | ReportsPage, ReportViewPage |

### 跨模块交互

1. **Agent → Scan → Vulnerability → Report 流程**:
   - Agent 创建 Scan 记录
   - Agent 运行时更新 Scan 进度和阶段
   - 发现结果存储为 Vulnerability
   - 完成时生成 Report

2. **Smart Router 集成**:
   - 所有 LLM 调用通过 Smart Router 路由
   - 支持多账户、自动故障转移、令牌管理
   - ProvidersPage 管理路由配置

3. **Kali 沙箱集成**:
   - 可配置是否使用沙箱执行工具
   - SandboxDashboardPage 监控容器状态
   - TerminalAgentPage 使用专属沙箱

4. **RAG 知识增强**:
   - KnowledgePage 上传文档
   - Agent 运行时自动检索相关知识注入提示词

---

## 核心模块架构

### 1. AutonomousAgent (自主代理)
**文件**: `backend/core/autonomous_agent.py`

功能:
- 多阶段执行流 (Recon → Analyze → Test → Report)
- 工具调用和编排
- 漏洞验证 (Proof of Execution)
- 自适应学习反馈
- 可配置的操作模式

### 2. VulnEngine (漏洞引擎)
**路径**: `backend/core/vuln_engine/`

功能:
- 50+ 种漏洞类型检测器
- 有效负载生成和变异
- 验证判断引擎
- 漏洞注册表 (VulnerabilityRegistry)

### 3. SmartRouter (智能路由)
**路径**: `backend/core/smart_router/`

功能:
- 多 LLM 提供商支持 (Anthropic, OpenAI, Gemini, Together, Fireworks 等)
- CLI 令牌自动检测和刷新
- 故障转移和负载均衡
- 使用统计和配额管理

### 4. RAG Engine (检索增强生成)
**路径**: `backend/core/rag/`

功能:
- 文档向量化存储
- 相似性检索
- 少样本提示注入
- 支持 BM25 (零依赖) 和 ChromaDB

### 5. ContainerPool (容器池)
**文件**: `core/container_pool.py`

功能:
- 按需创建 Kali Linux 沙箱
- 资源限制和隔离
- TTL 自动清理
- 健康检查监控

### 6. ReportEngine (报告引擎)
**路径**: `backend/core/report_engine/`

功能:
- HTML/PDF/JSON 报告生成
- 执行摘要生成
- PoC 文档化
- 修复建议

### 7. TaskLibrary (任务库)
**文件**: `backend/core/task_library.py`

功能:
- 预定义任务模板
- 自定义任务管理
- 分类和标签系统

---

## 配置项 (Settings)

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `MAX_CONCURRENT_SCANS` | 最大并发扫描数 | 5 |
| `DEFAULT_TIMEOUT` | 默认请求超时 (秒) | 30 |
| `MAX_REQUESTS_PER_SECOND` | 速率限制 | 10 |
| `ENABLE_SMART_ROUTER` | 启用智能路由 | false |
| `ENABLE_KNOWLEDGE_AUGMENTATION` | 启用知识增强 | false |
| `ENABLE_BROWSER_VALIDATION` | 启用浏览器验证 | false |
| `ENABLE_VULN_AGENTS` | 启用漏洞代理编排 | false |
| `VULN_AGENT_CONCURRENCY` | 漏洞代理并发数 | 10 |
| `ENABLE_RAG` | 启用 RAG | true |
| `RAG_BACKEND` | RAG 后端 (auto/chroma/tfidf/bm25) | auto |
| `ENABLE_CLI_AGENT` | 启用 CLI Agent | false |
| `CLI_AGENT_MAX_RUNTIME` | CLI Agent 最大运行时间 (秒) | 1800 |
| `CLI_AGENT_DEFAULT_PROVIDER` | CLI Agent 默认提供商 | claude_code |
| `DEFAULT_LLM_PROVIDER` | 默认 LLM 提供商 | claude |
| `DEFAULT_LLM_MODEL` | 默认 LLM 模型 | claude-sonnet-4-20250514 |

---

## 各页面布局结构分析

### HomePage 布局分析

**文件**: [frontend/src/pages/HomePage.tsx](file:///workspace/frontend/src/pages/HomePage.tsx)

#### 页面结构分区
```
┌─────────────────────────────────────────────────────────────┐
│  Header (标题: "NeuroSploit v3.2.4 - AI驱动渗透测试平台")      │
├─────────────────────────────────────────────────────────────┤
│  快速操作栏 (Quick Actions)                                  │
│  [Auto Pentest] [New Scan] [Vuln Lab] [Terminal]             │
├─────────────────────────────────────────────────────────────┤
│  统计卡片区域 (Statistics Grid - 4 cards)                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────┐
│  │ 总扫描数     │ │ 活跃代理     │ │ 发现漏洞     │ │ 总报告 │
│  └──────────────┘ └──────────────┘ └──────────────┘ └───────┘
├─────────────────────────────────────────────────────────────┤
│  图表区域 (Charts Grid - 2 cards)                            │
│  ┌──────────────────────────────────┐ ┌───────────────────┐
│  │ 漏洞严重级别分布 (饼图)           │ │ 扫描状态分布 (柱) │
│  └──────────────────────────────────┘ └───────────────────┘
├─────────────────────────────────────────────────────────────┤
│  双列内容区 (Two-column layout)                              │
│  ┌──────────────────────┐ ┌──────────────────────────────┐
│  │ 活跃代理列表         │ │ 最近扫描列表                 │
│  │ (Live Agents)        │ │ (Recent Scans)               │
│  ├──────────────────────┤ ├──────────────────────────────┤
│  │ 发现结果列表         │ │ 活动日志                     │
│  │ (Findings)           │ │ (Activity Feed)              │
│  └──────────────────────┘ └──────────────────────────────┘
└─────────────────────────────────────────────────────────────┘
```

#### 关键布局组件
1. **Header**: `h1` 标题 + `p` 描述
2. **快速操作**: `flex flex-wrap gap-3 mb-8`
3. **统计卡片**: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8`
4. **图表**: `grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8`
5. **底部双列**: `grid grid-cols-1 lg:grid-cols-2 gap-6`

#### 数据源
| 区域 | API 端点 | 数据模型 | 更新频率 |
|------|----------|----------|----------|
| 统计卡片 | GET /api/v1/home/stats | Scan, Vulnerability, Report, Agent | 页面加载 |
| 活跃代理 | GET /api/v1/agent/live | AgentInstance | 每3秒刷新 |
| 最近扫描 | GET /api/v1/scans?limit=10 | Scan | 页面加载 |
| 发现结果 | GET /api/v1/home/findings | Vulnerability | 页面加载 |
| 活动日志 | GET /api/v1/home/activity | ActivityLog | 页面加载 |

---

### NewScanPage 布局分析

**文件**: [frontend/src/pages/NewScanPage.tsx](file:///workspace/frontend/src/pages/NewScanPage.tsx)

#### 页面结构分区
```
┌─────────────────────────────────────────────────────────────┐
│  操作模式选择 (Tabs - 4个选项)                               │
│  [自主代理] [自动渗透] [全AI] [漏洞实验室]                   │
├─────────────────────────────────────────────────────────────┤
│  目标输入区 (Target Input)                                   │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 输入框: 目标 URL                                       │ │
│  │ 复选框: 启用子域发现                                   │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  任务库选择 (Task Library - 条件渲染)                       │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 搜索框 + 分类过滤 + 任务卡片列表                       │ │
│  │ [任务1] [任务2] [任务3] ...                            │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  自定义提示词 (Custom Prompt)                               │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 文本区域: 输入自定义提示词                             │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  认证配置 (Authentication - 折叠面板)                       │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 类型选择 (None/Basic/Bearer/API Key/Cookie)            │ │
│  │ 相应的输入字段组                                       │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  高级选项 (Advanced Options - 折叠面板)                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 复选框: Kali 沙箱、浏览器验证、漏洞代理                 │ │
│  │ LLM 提供商 + 模型 下拉选择                             │ │
│  │ 自定义 Header 输入                                     │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  操作按钮 (Deploy Agent)                                    │
│  [部署代理] [重置]                                          │
└─────────────────────────────────────────────────────────────┘
```

#### 关键布局组件
1. **Tabs**: `flex gap-2 border-b border-gray-700 mb-6`
2. **表单字段**: `space-y-4`
3. **折叠面板**: `div` 带 `Details` 组件
4. **按钮**: `mt-6 flex gap-3`

#### 表单字段参数
| 字段 | 类型 | 数据来源 | 默认值 |
|------|------|----------|--------|
| operation_mode | string | 本地状态 | autonomous_agent |
| target_url | string | 用户输入 | - |
| enable_subdomain | bool | 用户输入 | false |
| custom_prompt | string | 用户输入 | - |
| selected_task_id | string | 任务库 | - |
| auth_type | string | 用户输入 | none |
| auth_username | string | 用户输入 | - |
| auth_password | string | 用户输入 | - |
| auth_token | string | 用户输入 | - |
| auth_cookie | string | 用户输入 | - |
| use_sandbox | bool | 用户输入 | false |
| use_browser_validation | bool | 用户输入 | false |
| use_vuln_agents | bool | 用户输入 | false |
| llm_provider | string | 提供商列表 | 默认值 |
| llm_model | string | 模型列表 | 默认值 |
| custom_headers | string | 用户输入 | - |

---

### ScanDetailsPage 布局分析

**文件**: [frontend/src/pages/ScanDetailsPage.tsx](file:///workspace/frontend/src/pages/ScanDetailsPage.tsx)

#### 页面结构分区
```
┌─────────────────────────────────────────────────────────────┐
│  标题栏: 扫描详情 + [返回] [查看代理状态]                     │
├─────────────────────────────────────────────────────────────┤
│  扫描信息卡片 (Scan Info)                                    │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 目标: xxx.com                                          │ │
│  │ 状态: running                                          │ │
│  │ 进度: 75% [██████████░░]                               │ │
│  │ 创建时间: 2024-01-01 10:00                             │ │
│  │ 按钮: [暂停] [恢复] [停止] [删除]                       │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  统计卡片 (Statistics Grid - 4 cards)                       │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │
│  │ 端点    │ │ 漏洞    │ │ Critical│ │ High    │         │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘         │
├─────────────────────────────────────────────────────────────┤
│  选项卡导航 (Tabs - 3个)                                     │
│  [端点] [漏洞] [报告]                                        │
├─────────────────────────────────────────────────────────────┤
│  端点列表 (Endpoints Table)                                  │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ URL │ Method │ Status │ Interesting │ Actions         │ │
│  │ ... │ ...    │ ...    │ [x]         │ [测试]          │ │
│  └───────────────────────────────────────────────────────┘ │
│  OR 漏洞列表 (Vulnerabilities List)                         │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 标题 │ 严重级别 │ 验证状态 │ Actions                   │ │
│  │ ...  │ Critical │ ✓        │ [验证][误报][忽略]       │ │
│  └───────────────────────────────────────────────────────┘ │
│  OR 报告列表 (Reports List)                                 │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 标题 │ 创建时间 │ [查看][下载]                          │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  AI 报告生成 (AI Report Generation)                         │
│  [生成 AI 报告] [生成详细报告]                              │
└─────────────────────────────────────────────────────────────┘
```

#### 关键布局组件
1. **标题栏**: `flex justify-between items-center mb-6`
2. **扫描信息**: `bg-gray-800 rounded-lg p-6 mb-6`
3. **统计卡片**: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6`
4. **Tabs**: `flex gap-2 mb-6`
5. **表格/列表**: `space-y-4`

#### 端点表格列
| 列名 | 数据来源 | 类型 |
|------|----------|------|
| URL | Endpoint.url | string |
| Method | Endpoint.method | string |
| Status | Endpoint.status_code | number |
| Interesting | Endpoint.interesting | bool |
| Actions | 操作按钮 | - |

#### 漏洞表格列
| 列名 | 数据来源 | 类型 |
|------|----------|------|
| 标题 | Vulnerability.title | string |
| 严重级别 | Vulnerability.severity | string |
| 验证状态 | Vulnerability.validation_status | string |
| Actions | 操作按钮 | - |

---

### ReportsPage 布局分析

**文件**: [frontend/src/pages/ReportsPage.tsx](file:///workspace/frontend/src/pages/ReportsPage.tsx)

#### 页面结构分区
```
┌─────────────────────────────────────────────────────────────┐
│  标题: 报告管理 + [返回]                                     │
├─────────────────────────────────────────────────────────────┤
│  统计卡片 (Statistics Grid - 3 cards)                       │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ 总报告数     │ │ 自动生成     │ │ 本周生成     │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
├─────────────────────────────────────────────────────────────┤
│  过滤区 (Filters)                                            │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 扫描ID输入框 | 自动生成筛选开关                         │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  报告列表 (Reports List)                                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 报告1: [标题] [时间] [扫描ID] [View][Download][Delete] │ │
│  │ 报告2: [标题] [时间] [扫描ID] [View][Download][Delete] │ │
│  │ ...                                                   │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### 关键布局组件
1. **统计卡片**: `grid grid-cols-1 md:grid-cols-3 gap-4 mb-6`
2. **过滤器**: `flex gap-4 mb-6`
3. **报告卡片**: `space-y-4`

#### 过滤器参数
| 参数 | 类型 | 来源 |
|------|------|------|
| scanIdFilter | string | 用户输入 |
| autoGeneratedOnly | bool | 用户输入 |

---

### TerminalAgentPage 布局分析

**文件**: [frontend/src/pages/TerminalAgentPage.tsx](file:///workspace/frontend/src/pages/TerminalAgentPage.tsx)

#### 页面结构分区
```
┌─────────────────────────────────────────────────────────────┐
│  标题: AI 终端代理                                           │
├─────────────────────────────────────────────────────────────┤
│  会话管理 (Session Management)                               │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 场景模板选择 [模板1] [模板2] ... [新会话] [删除]       │ │
│  │ 会话列表: [会话1] [会话2] ...                          │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  聊天区 (Chat Interface)                                     │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 消息列表: AI消息、用户消息                              │ │
│  │ ┌───────────────────────────────────────────────┐    │ │
│  │ │ AI: 您想要执行什么操作?                        │    │ │
│  │ └───────────────────────────────────────────────┘    │ │
│  │ ┌───────────────────────────────────────────────┐    │ │
│  │ │ 用户: 运行 nmap 扫描                          │    │ │
│  │ └───────────────────────────────────────────────┘    │ │
│  │ ...                                                   │ │
│  │ 输入框 + [发送] 按钮                                    │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  命令输出区 (Command Output)                                 │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ $ nmap -p 80,443 example.com                           │ │
│  │ Starting Nmap...                                       │ │
│  │ PORT    STATE SERVICE                                  │ │
│  │ 80/tcp  open  http                                     │ │
│  │ 443/tcp open  https                                    │ │
│  └───────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  控制区 (Controls)                                           │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ 利用路径记录: [添加步骤] [删除步骤] [保存]              │ │
│  │ VPN 连接: [连接VPN] [断开VPN]                          │ │
│  │ 会话管理: [销毁会话]                                   │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 参数来源与关联性分析

### 数据库模型关联性

```
Scan (扫描)
  ├── 1:N → Target (目标)
  ├── 1:N → Endpoint (端点)
  ├── 1:N → Vulnerability (漏洞)
  └── 1:1 → Report (报告)

Vulnerability (漏洞)
  ├── 1:N → VulnerabilityTest (漏洞测试)
  └── N:1 → Scan (扫描)

Report (报告)
  └── N:1 → Scan (扫描)

AgentInstance (代理实例 - 内存中)
  └── 1:1 → Scan (通过 agent_id ↔ scan_id 映射)

VulnLabChallenge (漏洞实验室)
  └── 1:1 → AgentInstance (可选)

TerminalSession (终端会话)
  ├── 1:N → ChatMessage (聊天消息)
  └── 1:N → ExploitStep (利用步骤)
```

### API 端点参数映射

#### /api/v1/agent/run (POST)

**请求参数**
| 参数 | 类型 | 前端来源 | 数据库关联 |
|------|------|----------|------------|
| operation_mode | string | NewScanPage.state.operationMode | Scan.operation_mode |
| target_url | string | NewScanPage.state.targetUrl | Target.url |
| custom_prompt | string | NewScanPage.state.customPrompt | Scan.custom_prompt |
| task_id | string | NewScanPage.state.selectedTaskId | AgentTask.task_id |
| auth | object | NewScanPage.state.authConfig | - |
| options | object | NewScanPage.state (sandbox, browser, vuln_agents) | Scan.options |
| llm_provider | string | NewScanPage.state.llmProvider | Scan.llm_provider |
| llm_model | string | NewScanPage.state.llmModel | Scan.llm_model |

**响应参数**
| 参数 | 类型 | 用途 |
|------|------|------|
| agent_id | string | AgentStatusPage 路由参数 |
| scan_id | string | ScanDetailsPage 路由参数 |

#### /api/v1/scans/:scan_id (GET)

**路径参数**
| 参数 | 类型 | 来源 |
|------|------|------|
| scan_id | string | URL 路由参数 |

**响应数据**
| 字段 | 模型 | 前端显示位置 |
|------|------|--------------|
| id | Scan.id | 标题栏 |
| target_url | Target.url | 扫描信息卡片 |
| status | Scan.status | 扫描信息卡片 |
| progress | Scan.progress | 进度条 |
| statistics | Scan.statistics | 统计卡片 |
| created_at | Scan.created_at | 扫描信息卡片 |

#### /api/v1/scans/:scan_id/endpoints (GET)

**响应数据 - Endpoint[]**
| 字段 | 用途 |
|------|------|
| url | 表格 URL 列 |
| method | 表格 Method 列 |
| status_code | 表格 Status 列 |
| interesting | 表格 Interesting 复选框 |

#### /api/v1/scans/:scan_id/vulnerabilities (GET)

**响应数据 - Vulnerability[]**
| 字段 | 用途 |
|------|------|
| title | 表格标题列 |
| severity | 表格严重级别列 |
| validation_status | 表格验证状态列 |
| description | 详情模态框 |
| cvss_score | CVSS 评分显示 |

---

## 代码与文档一致性检查

### 已发现的一致性问题修正

#### 1. ReportsPage 组件完整实现
文档需要补充 ReportsPage 包含的完整功能：
- ✅ 统计卡片（总报告数、自动生成、本周生成）
- ✅ 过滤功能（扫描ID、自动生成）
- ✅ 报告卡片列表（标题、创建时间、扫描ID链接）
- ✅ 操作按钮（查看、下载、删除）
- ✅ 自动检测 API 端点路径

#### 2. ScanDetailsPage 完整功能
文档需要补充 ScanDetailsPage 的：
- ✅ 扫描控制按钮（暂停、恢复、停止、删除）
- ✅ 端点表格（测试单个端点功能）
- ✅ 漏洞验证功能（验证、误报、忽略）
- ✅ AI 报告生成功能

#### 3. TerminalAgentPage 完整功能
文档需要补充 TerminalAgentPage 的：
- ✅ 场景模板支持
- ✅ 聊天消息系统
- ✅ 命令输出显示
- ✅ 利用路径记录
- ✅ VPN 连接控制
- ✅ 会话管理

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
