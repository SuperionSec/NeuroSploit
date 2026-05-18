# NeuroSploit v3.2.4 完整功能清单

## 目录
1. [系统概览](#系统概览)
2. [后端API接口](#后端api接口)
3. [前端页面功能](#前端页面功能)
4. [功能关联性分析](#功能关联性分析)
5. [核心模块架构](#核心模块架构)

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
