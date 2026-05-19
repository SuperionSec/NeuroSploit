# NeuroSploit v3.2.4 完整功能清单

## 目录
1. [系统概览](#系统概览)
2. [后端API接口](#后端api接口) — 18个API模块，80+端点
3. [前端页面功能](#前端页面功能) — 18个页面完整覆盖
4. [完整功能测试计划](#完整功能测试计划) — 75+测试用例
5. [Providers与Settings大模型配置区别](#providers与settings大模型配置区别)
6. [后端核心架构](#后端核心架构) — 10大子系统，60+模块

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

### 7. 仪表板 (Dashboard API)
**路径前缀**: `/api/v1/dashboard`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/stats` | 获取仪表板统计数据（扫描数、漏洞数、代理数等） | HomePage |
| GET | `/recent` | 获取最近扫描记录 | HomePage |
| GET | `/findings` | 获取最近发现结果 | HomePage |
| GET | `/vulnerability-types` | 获取漏洞类型分布统计 | HomePage |
| GET | `/scan-history` | 获取扫描历史趋势 | HomePage |
| GET | `/agent-tasks` | 获取最近的代理任务 | HomePage |
| GET | `/activity-feed` | 获取活动日志流 | HomePage |

---

### 8. 设置管理 (Settings API)
**路径前缀**: `/api/v1/settings`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 获取当前系统设置 | SettingsPage |
| PUT | `/` | 更新系统设置 | SettingsPage |
| POST | `/notifications/test/{channel}` | 测试通知渠道 | SettingsPage |
| POST | `/clear-database` | 清空数据库 | SettingsPage |
| GET | `/stats` | 获取数据库统计 | SettingsPage |
| GET | `/tools` | 检测可用工具 | SettingsPage |
| GET | `/models/{provider}` | 获取指定提供商的模型目录 | SettingsPage |

---

### 9. 沙箱管理 (Sandbox API)
**路径前缀**: `/api/v1/sandbox`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 列出所有沙箱容器 | SandboxDashboardPage |
| GET | `/{scan_id}` | 获取沙箱容器详情 | SandboxDashboardPage |
| DELETE | `/{scan_id}` | 销毁沙箱容器 | SandboxDashboardPage |
| POST | `/cleanup` | 清理过期容器 | SandboxDashboardPage |
| POST | `/cleanup-orphans` | 清理孤儿容器 | SandboxDashboardPage |

---

### 10. 知识库 (Knowledge API)
**路径前缀**: `/api/v1/knowledge`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| POST | `/upload` | 上传知识文档 (PDF/MD/TXT/HTML) | KnowledgePage |
| GET | `/documents` | 列出所有知识文档 | KnowledgePage |
| GET | `/documents/{doc_id}` | 获取文档详情和条目 | KnowledgePage |
| DELETE | `/documents/{doc_id}` | 删除知识文档 | KnowledgePage |
| GET | `/search` | 搜索知识库内容 | KnowledgePage |
| GET | `/stats` | 获取知识库统计 | KnowledgePage |

---

### 11. MCP服务器 (MCP API)
**路径前缀**: `/api/v1/mcp`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/servers` | 列出所有MCP服务器 | MCPManagementPage |
| GET | `/servers/{name}` | 获取特定MCP服务器详情 | MCPManagementPage |
| POST | `/servers` | 创建MCP服务器 | MCPManagementPage |
| PUT | `/servers/{name}` | 更新MCP服务器配置 | MCPManagementPage |
| DELETE | `/servers/{name}` | 删除MCP服务器 | MCPManagementPage |
| POST | `/servers/{name}/toggle` | 切换服务器启用状态 | MCPManagementPage |
| POST | `/servers/{name}/test` | 测试服务器连接 | MCPManagementPage |
| GET | `/servers/{name}/tools` | 列出服务器提供的工具 | MCPManagementPage |

---

### 12. 调度任务 (Scheduler API)
**路径前缀**: `/api/v1/scheduler`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 列出所有调度任务 | SchedulerPage |
| POST | `/` | 创建调度任务 | SchedulerPage |
| DELETE | `/{job_id}` | 删除调度任务 | SchedulerPage |
| POST | `/{job_id}/pause` | 暂停调度任务 | SchedulerPage |
| POST | `/{job_id}/resume` | 恢复调度任务 | SchedulerPage |
| GET | `/agent-roles` | 获取代理角色列表 | SchedulerPage |

---

### 13. 目标管理 (Targets API)
**路径前缀**: `/api/v1/targets`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| POST | `/validate` | 验证单个目标URL | NewScanPage |
| POST | `/validate/bulk` | 批量验证目标URL | NewScanPage |
| POST | `/upload` | 上传目标文件 | NewScanPage |
| POST | `/parse-input` | 解析目标输入 | NewScanPage |

---

### 14. 漏洞信息 (Vulnerabilities API)
**路径前缀**: `/api/v1/vulnerabilities`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/types` | 获取所有漏洞类型 | VulnLabPage |
| GET | `/types/{category}` | 按类别获取漏洞类型 | VulnLabPage |
| GET | `/types/{category}/{vuln_type}` | 获取漏洞类型详情 | VulnLabPage |
| GET | `/{vuln_id}` | 获取特定漏洞详情 | ScanDetailsPage |

---

### 15. 提示词管理 (Prompts API)
**路径前缀**: `/api/v1/prompts`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/presets` | 获取预设提示词列表 | NewScanPage |
| GET | `/presets/{preset_id}` | 获取特定预设提示词 | NewScanPage |
| POST | `/parse` | 解析提示词模板 | NewScanPage |
| GET | `/` | 列出自定义提示词 | SettingsPage |
| POST | `/` | 创建自定义提示词 | SettingsPage |
| GET | `/{prompt_id}` | 获取特定提示词 | SettingsPage |
| PUT | `/{prompt_id}` | 更新提示词 | SettingsPage |
| DELETE | `/{prompt_id}` | 删除提示词 | SettingsPage |
| POST | `/upload` | 上传提示词文件 | SettingsPage |

---

### 16. 完整AI测试 (Full IA API)
**路径前缀**: `/api/v1/full-ia`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/prompt` | 获取完整AI渗透测试提示内容 | FullIATestingPage |

---

### 17. CLI代理 (CLI Agent API)
**路径前缀**: `/api/v1/cli-agent`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/providers` | 获取CLI代理提供商信息 | TerminalAgentPage |
| GET | `/methodologies` | 获取方法论列表 | TerminalAgentPage |

---

### 18. 代理任务 (Agent Tasks API)
**路径前缀**: `/api/v1/agent-tasks`

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | `/` | 列出代理任务 | TaskLibraryPage |
| GET | `/summary` | 获取代理任务摘要 | TaskLibraryPage |
| GET | `/{task_id}` | 获取特定代理任务 | TaskLibraryPage |
| GET | `/scan/{scan_id}/timeline` | 获取扫描任务时间线 | ScanDetailsPage |

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

### ScanDetailsPage (扫描详情页)
**路径**: `/scans/:scanId`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 返回按钮 | 返回上一页 | 路由导航 |
| 查看代理状态按钮 | 跳转到AgentStatusPage | 路由导航 /agent/:id |
| 扫描信息卡片 | 显示目标URL、状态、进度条、创建时间 | GET /api/v1/scans/{id} |
| 暂停按钮 | 暂停运行中的扫描 | POST /api/v1/scans/{id}/pause |
| 恢复按钮 | 恢复暂停的扫描 | POST /api/v1/scans/{id}/resume |
| 停止按钮 | 停止运行中的扫描 | POST /api/v1/scans/{id}/stop |
| 删除按钮 | 删除扫描 | DELETE /api/v1/scans/{id} |
| 统计卡片 | 显示端点数、漏洞数、Critical/High数量 | GET /api/v1/scans/{id} |
| 端点选项卡 | 显示发现的端点列表 | GET /api/v1/scans/{id}/endpoints |
| 端点测试按钮 | 对单个端点执行测试 | POST /api/v1/agent/run |
| 漏洞选项卡 | 显示发现的漏洞列表 | GET /api/v1/scans/{id}/vulnerabilities |
| 验证漏洞按钮 | 手动验证漏洞 | PATCH /api/v1/scans/vulnerabilities/{vid}/validate |
| 标记误报按钮 | 标记漏洞为误报 | POST /api/v1/scans/vulnerabilities/{vid}/feedback |
| 忽略漏洞按钮 | 忽略该漏洞 | POST /api/v1/scans/vulnerabilities/{vid}/feedback |
| 报告选项卡 | 显示生成的报告列表 | GET /api/v1/reports?scan_id={id} |
| 生成AI报告按钮 | AI生成报告 | POST /api/v1/reports/ai-generate |
| 生成详细报告按钮 | 生成详细报告 | POST /api/v1/reports |

---

### AgentStatusPage (代理状态页)
**路径**: `/agent/:agentId`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 返回按钮 | 返回上一页 | 路由导航 |
| 查看扫描详情按钮 | 跳转到ScanDetailsPage | 路由导航 /scans/{id} |
| 代理状态卡片 | 显示代理ID、状态、当前阶段 | GET /api/v1/agent/status/{id} |
| 暂停按钮 | 暂停代理执行 | POST /api/v1/agent/pause/{id} |
| 恢复按钮 | 恢复代理执行 | POST /api/v1/agent/resume/{id} |
| 停止按钮 | 停止代理执行 | POST /api/v1/agent/stop/{id} |
| 执行日志面板 | 实时显示代理执行日志 | GET /api/v1/agent/logs/{id} |
| 发现结果面板 | 显示发现的漏洞和端点 | GET /api/v1/agent/findings/{id} |
| 自定义提示词输入 | 发送自定义指令给AI代理 | POST /api/v1/agent/prompt/{id} |
| 阶段跳转按钮 | 跳转到指定执行阶段 | POST /api/v1/agent/skip-to/{id}/{phase} |
| 生成报告按钮 | 代理完成后生成报告 | POST /api/v1/reports |

---

### SettingsPage (设置页)
**路径**: `/settings`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| LLM提供商选择 | 选择默认LLM提供商 | GET/PUT /api/v1/settings |
| LLM模型选择 | 选择默认模型 | GET /api/v1/settings/models/{provider} |
| API Key输入 | 输入提供商API Key | PUT /api/v1/settings |
| 最大输出Token | 设置全局最大输出token | PUT /api/v1/settings |
| 启用模型路由开关 | 启用/禁用Smart Router | PUT /api/v1/settings |
| 启用知识增强开关 | 启用/禁用RAG | PUT /api/v1/settings |
| 启用浏览器验证开关 | 启用/禁用浏览器验证 | PUT /api/v1/settings |
| 启用推理引擎开关 | 启用/禁用推理能力 | PUT /api/v1/settings |
| 启用CVE猎手开关 | 启用/禁用CVE搜索 | PUT /api/v1/settings |
| 启用多代理开关 | 启用/禁用并行代理 | PUT /api/v1/settings |
| 启用研究员AI开关 | 启用/禁用研究员代理 | PUT /api/v1/settings |
| 通知配置 | 配置Discord/Telegram/Twilio通知 | PUT /api/v1/settings |
| 测试通知按钮 | 测试通知渠道 | POST /api/v1/settings/notifications/test/{channel} |
| 工具检测 | 检测可用工具 | GET /api/v1/settings/tools |
| 数据库统计 | 显示数据库统计信息 | GET /api/v1/settings/stats |
| 清空数据库按钮 | 清空所有数据 | POST /api/v1/settings/clear-database |
| 自适应学习统计 | 显示学习统计和阈值 | GET /api/v1/scans/vulnerabilities/learning/stats |

---

### ProvidersPage (提供商管理页)
**路径**: `/providers`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 提供商列表 | 显示所有LLM提供商和账户 | GET /api/v1/providers |
| 配额状态卡片 | 显示各提供商的配额使用情况 | GET /api/v1/providers/status |
| 检测CLI令牌按钮 | 自动检测本地CLI工具令牌 | POST /api/v1/providers/detect-all |
| 添加API Key按钮 | 手动添加API Key | POST /api/v1/providers/{id}/connect |
| 测试连接按钮 | 测试单个账户连接 | POST /api/v1/providers/test/{pid}/{aid} |
| 启用/禁用提供商 | 切换提供商启用状态 | POST /api/v1/providers/{id}/toggle |
| 删除账户按钮 | 删除提供商账户 | DELETE /api/v1/providers/{pid}/accounts/{aid} |
| 环境变量编辑器 | 直接编辑.env配置 | PUT /api/v1/settings |
| 可用模型列表 | 查看提供商支持的模型 | GET /api/v1/providers/available-models |

---

### ReportViewPage (报告查看页)
**路径**: `/reports/:reportId`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 返回按钮 | 返回报告列表页 | 路由导航 /reports |
| 报告ID显示 | 显示当前报告ID | URL参数 |
| 刷新按钮 | 刷新报告内容 | 重新加载 iframe |
| 全屏按钮 | 切换全屏模式 | 本地状态切换 |
| HTML下载按钮 | 下载HTML格式报告 | GET /api/v1/reports/{id}/download/html |
| JSON下载按钮 | 下载JSON格式报告 | GET /api/v1/reports/{id}/download/json |
| 新标签页打开 | 在新窗口查看报告 | GET /api/v1/reports/{id}/view |
| 报告iframe | 内嵌显示HTML报告 | GET /api/v1/reports/{id}/view |

---

### FullIATestingPage (完整AI渗透测试页)
**路径**: `/full-ia`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 目标URL输入 | 输入渗透测试目标 | - |
| 操作模式选择 | 选择AI渗透模式 | - |
| 开始测试按钮 | 启动完整AI渗透测试 | POST /api/v1/agent/run |
| 停止按钮 | 停止运行中的测试 | POST /api/v1/agent/stop/{id} |
| 阶段进度条 | 显示4阶段进度 (Recon→Testing→PostExploit→Report) | GET /api/v1/agent/status/{id} |
| 执行日志 | 实时显示LLM决策和工具执行日志 | GET /api/v1/agent/logs/{id} |
| 发现结果列表 | 显示发现的漏洞和端点 | GET /api/v1/agent/findings/{id} |
| 漏洞严重级别饼图 | 显示漏洞分布 | 本地计算 |
| 日志过滤 | 按类型过滤日志 (All/LLM/AI/Errors) | 本地过滤 |
| 工具执行详情 | 显示Kali工具执行结果 | GET /api/v1/agent/status/{id} |
| 生成报告按钮 | 测试完成后生成报告 | POST /api/v1/reports |
| 查看报告按钮 | 跳转查看报告 | 路由导航 |

---

### TaskLibraryPage (任务库页)
**路径**: `/tasks`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 任务列表 | 显示所有预定义任务 | GET /api/v1/agent/tasks |
| 分类过滤 | 按类别筛选 (Full Auto/Recon/Vuln/Custom/Reporting) | 本地过滤 |
| 搜索框 | 搜索任务名称 | 本地搜索 |
| 使用任务按钮 | 将任务用于新扫描 | 路由导航 /scan/new |
| 创建自定义任务 | 创建新的自定义任务 | POST /api/v1/agent/tasks |
| 删除任务按钮 | 删除自定义任务 | DELETE /api/v1/agent/tasks/{id} |
| 任务详情展开 | 查看任务描述和步骤 | 本地展开 |

---

### RealtimeTaskPage (实时任务页)
**路径**: `/realtime`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 创建会话按钮 | 创建新的实时任务会话 | POST /api/v1/agent/realtime/session |
| 会话列表 | 显示所有实时会话 | GET /api/v1/agent/realtime/sessions/list |
| 聊天输入框 | 发送消息给AI代理 | POST /api/v1/agent/realtime/{id}/message |
| 消息列表 | 显示AI和用户的对话历史 | WebSocket 实时推送 |
| 发现结果面板 | 显示实时发现的漏洞 | GET /api/v1/agent/findings/{id} |
| 删除会话按钮 | 删除实时会话 | DELETE /api/v1/agent/realtime/{id} |
| LLM状态指示器 | 显示LLM连接状态 | GET /api/v1/agent/realtime/llm-status |
| 工具列表 | 显示可用工具 | GET /api/v1/agent/realtime/tools/list |
| 执行工具按钮 | 执行指定工具 | POST /api/v1/agent/realtime/{id}/execute-tool |
| Docker状态提示 | 显示Docker是否可用 | 本地检测 |

---

### SandboxDashboardPage (沙箱仪表板页)
**路径**: `/sandboxes`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 容器列表 | 显示所有Kali沙箱容器 | GET /api/v1/sandbox/ |
| 容器状态 | 显示运行中/已停止容器数量 | GET /api/v1/sandbox/ |
| 健康检查 | 显示容器健康状态 | GET /api/v1/sandbox/{scan_id} |
| 销毁容器按钮 | 销毁指定沙箱容器 | DELETE /api/v1/sandbox/{scan_id} |
| 清理过期按钮 | 清理过期容器 | POST /api/v1/sandbox/cleanup |
| 清理孤儿按钮 | 清理孤儿容器 | POST /api/v1/sandbox/cleanup-orphans |
| 资源使用饼图 | 显示CPU/内存使用分布 | 本地计算 |
| 容器详情展开 | 显示容器详细信息和工具列表 | GET /api/v1/sandbox/{scan_id} |

---

### KnowledgePage (知识库管理页)
**路径**: `/knowledge`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 文档上传 | 上传PDF/MD/TXT/HTML文件 | POST /api/v1/knowledge/upload |
| 文档列表 | 显示所有知识文档 | GET /api/v1/knowledge/documents |
| 文档详情 | 查看文档详细内容和条目 | GET /api/v1/knowledge/documents/{id} |
| 删除文档 | 删除知识文档 | DELETE /api/v1/knowledge/documents/{id} |
| 搜索知识 | 搜索知识库内容 | GET /api/v1/knowledge/search |
| 统计卡片 | 显示文档数、条目数、覆盖漏洞类型数 | GET /api/v1/knowledge/stats |
| 文件类型过滤 | 按文件类型筛选文档 | 本地过滤 |
| 漏洞类型标签 | 显示文档关联的漏洞类型 | GET /api/v1/knowledge/documents/{id} |

---

### MCPManagementPage (MCP服务器管理页)
**路径**: `/mcp`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 服务器列表 | 显示所有MCP服务器 | GET /api/v1/mcp/servers |
| 创建服务器 | 添加新的MCP服务器 | POST /api/v1/mcp/servers |
| 编辑服务器 | 修改服务器配置 | PUT /api/v1/mcp/servers/{name} |
| 删除服务器 | 删除MCP服务器 | DELETE /api/v1/mcp/servers/{name} |
| 启用/禁用切换 | 切换服务器启用状态 | POST /api/v1/mcp/servers/{name}/toggle |
| 测试连接 | 测试服务器连接是否正常 | POST /api/v1/mcp/servers/{name}/test |
| 工具列表 | 显示服务器提供的工具 | GET /api/v1/mcp/servers/{name}/tools |
| 传输类型选择 | 选择stdio或sse传输方式 | - |
| 环境变量配置 | 配置服务器环境变量 | - |

---

### SchedulerPage (调度任务管理页)
**路径**: `/scheduler`

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 调度任务列表 | 显示所有定时任务 | GET /api/v1/scheduler/ |
| 创建调度 | 创建新的定时扫描任务 | POST /api/v1/scheduler/ |
| 删除调度 | 删除调度任务 | DELETE /api/v1/scheduler/{job_id} |
| 暂停调度 | 暂停调度任务 | POST /api/v1/scheduler/{job_id}/pause |
| 恢复调度 | 恢复暂停的调度任务 | POST /api/v1/scheduler/{job_id}/resume |
| 代理角色选择 | 选择扫描代理角色 | GET /api/v1/scheduler/agent-roles |
| Cron表达式输入 | 设置调度时间表达式 | - |
| 目标URL输入 | 设置扫描目标 | - |
| 删除确认弹窗 | 确认删除操作 | - |

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

## 后端核心架构

### 架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                        NeuroSploit v3.2.4 后端架构                    │
├─────────────────────────────────────────────────────────────────────┤
│  API Layer (FastAPI)                                                │
│  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐         │
│  │agent │scans │report│vuln  │term  │mcp   │sched │...18 │         │
│  │      │      │s     │lab   │inal  │      │uler  │modules│         │
│  └──┬───┴──┬───┴──┬───┴──┬───┴──┬───┴──┬───┴──┬───┴──────┘         │
├─────┼──────┼──────┼──────┼──────┼──────┼───────────────────────────┤
│     │      Core Layer                                                │
│     ▼      ▼      ▼      ▼      ▼                                   │
│  ┌──────────────────────────────────────────┐                       │
│  │         Agent System (10 modules)         │                       │
│  │  AgentBase → SpecialistAgents             │                       │
│  │  AIPentestAgent → AgentOrchestrator       │                       │
│  │  VulnOrchestrator → VulnTypeAgent         │                       │
│  │  ResearcherAgent → AgentMemory/Tasks      │                       │
│  └──────────────────┬───────────────────────┘                       │
│                     │                                                │
│  ┌──────────────────┼───────────────────────┐                       │
│  │    Smart Router   │   RAG Engine          │                       │
│  │  (4 modules)     │   (5 modules)         │                       │
│  │  Router→Registry │   Engine→Processor    │                       │
│  │  →ProviderAcct   │   →Chunker→Embedder   │                       │
│  └──────────────────┼───────────────────────┘                       │
│                     │                                                │
│  ┌──────────────────┼───────────────────────┐                       │
│  │   VulnEngine     │   Validation Pipeline  │                       │
│  │  (8 modules)    │   (6 modules)          │                       │
│  │  Engine→Registry│   NegativeControl      │                       │
│  │  →Generator     │   ProofOfExecution     │                       │
│  │  →Executor      │   ConfidenceScorer     │                       │
│  │  →Reporter      │   ValidationJudge      │                       │
│  └──────────────────┼───────────────────────┘                       │
│                     │                                                │
│  ┌──────────────────┼───────────────────────┐                       │
│  │  Request Engine  │   AI Reasoning        │                       │
│  │  (5 modules)    │   (7 modules)          │                       │
│  │  RequestEngine  │   ReasoningEngine      │                       │
│  │  WAFDetector    │   TokenBudget          │                       │
│  │  StrategyAdapter│   CVEHunter            │                       │
│  │  ChainEngine    │   DeepRecon            │                       │
│  │  AuthManager    │   BannerAnalyzer       │                       │
│  └──────────────────┼───────────────────────┘                       │
│                     │                                                │
│  ┌──────────────────┼───────────────────────┐                       │
│  │  Report Engine   │   Sandbox/CLI         │                       │
│  │  (2 modules)    │   (4 modules)          │                       │
│  │  ReportGenerator│   ToolExecutor         │                       │
│  │  ReportEngine   │   CLIAgentRunner       │                       │
│  │                  │   CLIOutputParser      │                       │
│  │                  │   CLIInstructionsBldr  │                       │
│  └──────────────────┴───────────────────────┘                       │
│                                                                     │
│  ┌──────────────────────────────────────────┐                       │
│  │         Supporting Modules (15)           │                       │
│  │  CheckpointManager  NotificationManager   │                       │
│  │  KnowledgeProcessor TaskLibrary           │                       │
│  │  ExecutionHistory   MethodologyLoader     │                       │
│  │  PayloadMutator     POCGenerator          │                       │
│  │  POCValidator        ExploitGenerator     │                       │
│  │  XSSValidator       XSSContextAnalyzer    │                       │
│  │  SiteAnalyzer       RequestRepeater       │                       │
│  │  PromptEngine (parser+builder+manager)    │                       │
│  └──────────────────────────────────────────┘                       │
├─────────────────────────────────────────────────────────────────────┤
│  Data Layer                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ SQLAlchemy   │  │ SQLite       │  │ File Storage │             │
│  │ (Async ORM)  │  │ (Default DB) │  │ (Reports/KB) │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 1. Agent 系统 (10 modules)

Agent 系统是 NeuroSploit 的核心，负责协调 AI 代理执行渗透测试任务。

| 模块文件 | 主要类 | 核心职责 | 依赖模块 |
|----------|--------|----------|----------|
| [agent_base.py](file:///workspace/backend/core/agent_base.py) | AgentResult, SpecialistAgent | 定义专家代理基类和结果数据结构，提供执行、取消、手递手等通用功能 | 无 |
| [autonomous_agent.py](file:///workspace/backend/core/autonomous_agent.py) | AutonomousAgent | 自主代理，驱动完整的自动化渗透测试流程 | agent_base, smart_router, rag |
| [ai_pentest_agent.py](file:///workspace/backend/core/ai_pentest_agent.py) | AIPentestAgent | AI驱动的渗透测试代理，使用LLM推理进行漏洞检测和PoC生成 | llm_manager, request_engine |
| [agent_orchestrator.py](file:///workspace/backend/core/agent_orchestrator.py) | AgentOrchestrator | 协调多个专家代理的执行流程，管理手递手路由和共享内存 | specialist_agents |
| [specialist_agents.py](file:///workspace/backend/core/specialist_agents.py) | ReconAgent, ExploitAgent, ValidatorAgent, CVEHunterAgent, ReportAgent | 实现具体的专家代理：侦察、利用、验证、CVE搜索和报告 | deep_recon, banner_analyzer, cve_hunter, payload_mutator, param_analyzer, endpoint_classifier, exploit_generator, poc_validator |
| [vuln_orchestrator.py](file:///workspace/backend/core/vuln_orchestrator.py) | VulnOrchestrator | 为每个漏洞类型并行协调专家代理 | vuln_type_agent, agent_base |
| [vuln_type_agent.py](file:///workspace/backend/core/vuln_type_agent.py) | VulnTypeAgent | 单一漏洞类型测试的专家代理 | agent_base |
| [researcher_agent.py](file:///workspace/backend/core/researcher_agent.py) | ResearcherAgent | AI驱动的0日漏洞研究员，使用Kali沙箱执行工具 | kali_sandbox, tool_registry, sandbox_manager |
| [agent_memory.py](file:///workspace/backend/core/agent_memory.py) | AgentMemory | 代理内存管理：测试组合、基线响应、端点指纹和发现存储 | 无 |
| [agent_tasks.py](file:///workspace/backend/core/agent_tasks.py) | AgentTask, AgentTaskManager | 代理任务管理器，支持优先队列和并发执行 | 无 |

**Agent 执行流程**:
```
用户启动扫描
    │
    ▼
AutonomousAgent / AIPentestAgent
    │
    ├── AgentOrchestrator (多专家协调)
    │   ├── ReconAgent (侦察)
    │   ├── ExploitAgent (利用)
    │   ├── ValidatorAgent (验证)
    │   ├── CVEHunterAgent (CVE搜索)
    │   └── ReportAgent (报告)
    │
    └── VulnOrchestrator (并行漏洞测试)
        ├── VulnTypeAgent (XSS)
        ├── VulnTypeAgent (SQLi)
        ├── VulnTypeAgent (SSRF)
        └── ... (每种漏洞类型一个)
```

---

### 2. VulnEngine 系统 (8 modules)

漏洞引擎负责管理和执行具体的漏洞检测逻辑。

| 模块文件 | 主要类 | 核心职责 | 依赖模块 |
|----------|--------|----------|----------|
| [vuln_engine/engine.py](file:///workspace/backend/core/vuln_engine/engine.py) | VulnEngine | 漏洞引擎核心：接收目标和漏洞类型，构建并执行检测任务，生成报告 | smart_router, rag |
| [vuln_engine/registry.py](file:///workspace/backend/core/vuln_engine/registry.py) | VulnRegistry | 漏洞类型注册表，管理所有支持的漏洞类型和对应的检测器 | 无 |
| [vuln_engine/generator.py](file:///workspace/backend/core/vuln_engine/generator.py) | PayloadGenerator | 攻击载荷生成器，根据漏洞类型生成测试载荷 | 无 |
| [vuln_engine/executor.py](file:///workspace/backend/core/vuln_engine/executor.py) | VulnExecutor | 漏洞检测执行器，发送请求并收集响应 | request_engine |
| [vuln_engine/analyzer.py](file:///workspace/backend/core/vuln_engine/analyzer.py) | ResponseAnalyzer | 响应分析器，判断是否存在漏洞 | 无 |
| [vuln_engine/reporter.py](file:///workspace/backend/core/vuln_engine/reporter.py) | VulnReporter | 漏洞报告器，汇总检测结果 | 无 |
| [vuln_engine/mutator.py](file:///workspace/backend/core/vuln_engine/mutator.py) | PayloadMutator | 载荷变异器，绕过WAF和过滤器 | waf_detector |
| [vuln_engine/context.py](file:///workspace/backend/core/vuln_engine/context.py) | VulnContext | 漏洞检测上下文，管理检测状态和参数 | 无 |

---

### 3. Smart Router 系统 (4 modules)

智能路由系统管理多个 LLM 提供商，实现负载均衡和故障转移。

| 模块文件 | 主要类 | 核心职责 | 依赖模块 |
|----------|--------|----------|----------|
| [smart_router/router.py](file:///workspace/backend/core/smart_router/router.py) | SmartRouter | 智能路由引擎：多提供商选择、负载均衡、故障转移、配额追踪 | provider_registry |
| [smart_router/provider_registry.py](file:///workspace/backend/core/smart_router/provider_registry.py) | ProviderRegistry | 提供商注册表：管理提供商配置、账户、CLI令牌检测 | 无 |
| [smart_router/provider_account.py](file:///workspace/backend/core/smart_router/provider_account.py) | ProviderAccount | 提供商账户：API Key管理、配额追踪、过期检测 | 无 |
| [smart_router/credential_store.py](file:///workspace/backend/core/smart_router/credential_store.py) | CredentialStore | 凭据存储：安全存储和管理API Key | 无 |

**Smart Router 请求流程**:
```
LLM 请求 → SmartRouter.route()
    │
    ├── 1. 检查 preferred_provider
    ├── 2. 按 Tier 排序 (1→2→3)
    ├── 3. 轮询选择可用账户
    ├── 4. 构建请求 (OpenAI/Anthropic/Gemini 格式)
    ├── 5. 发送请求 (aiohttp + trust_env)
    ├── 6. 解析响应 (过滤 <think\> 标签)
    ├── 7. 失败 → 故障转移到下一个
    └── 8. 记录 token 使用和配额
```

---

### 4. RAG 系统 (5 modules)

检索增强生成系统，为AI代理提供专业知识支持。

| 模块文件 | 主要类 | 核心职责 | 依赖模块 |
|----------|--------|----------|----------|
| [rag/engine.py](file:///workspace/backend/core/rag/engine.py) | RAGEngine | RAG引擎核心：整合外部知识库，为检测引擎提供上下文感知信息 | knowledge_processor |
| [rag/processor.py](file:///workspace/backend/core/rag/processor.py) | KnowledgeProcessor | 知识处理器：处理和索引知识文档 | 无 |
| [rag/chunker.py](file:///workspace/backend/core/rag/chunker.py) | DocumentChunker | 文档分块器：将文档分割为适合检索的块 | 无 |
| [rag/embedder.py](file:///workspace/backend/core/rag/embedder.py) | Embedder | 嵌入器：生成文本向量嵌入 | smart_router |
| [rag/retriever.py](file:///workspace/backend/core/rag/retriever.py) | Retriever | 检索器：基于向量相似度检索相关知识 | embedder |

---

### 5. 验证管线 (6 modules)

验证管线确保漏洞检测结果的准确性和可靠性。

| 模块文件 | 主要类 | 核心职责 | 依赖模块 |
|----------|--------|----------|----------|
| [negative_control.py](file:///workspace/backend/core/negative_control.py) | NegativeControl | 负面控制：过滤误报，防止扫描行为过于激进或无效 | 无 |
| [proof_of_execution.py](file:///workspace/backend/core/proof_of_execution.py) | ProofOfExecution | 执行证明：确保操作步骤可验证和可追踪，提供审计链 | 无 |
| [confidence_scorer.py](file:///workspace/backend/core/confidence_scorer.py) | ConfidenceScorer | 置信度评分：计算检测结果的置信度分数，优化检测准确性 | 无 |
| [validation_judge.py](file:///workspace/backend/core/validation_judge.py) | ValidationJudge | 验证判断：通过人工反馈和推理对检测结果进行最终确认 | 无 |
| [access_control_learner.py](file:///workspace/backend/core/access_control_learner.py) | AccessControlLearner | 访问控制学习：学习访问控制策略，优化权限管理 | 无 |
| [adaptive_learner.py](file:///workspace/backend/core/adaptive_learner.py) | AdaptiveLearner | 自适应学习：持续优化系统策略和性能 | 无 |

**验证管线流程**:
```
漏洞检测结果
    │
    ▼
NegativeControl (过滤误报)
    │
    ▼
ConfidenceScorer (计算置信度)
    │
    ▼
ProofOfExecution (生成执行证明)
    │
    ▼
ValidationJudge (最终判断)
    │
    ├── AdaptiveLearner (学习反馈)
    └── AccessControlLearner (学习访问控制)
```

---

### 6. 请求引擎 (5 modules)

请求引擎负责发送HTTP请求，处理WAF检测和策略适配。

| 模块文件 | 主要类 | 核心职责 | 依赖模块 |
|----------|--------|----------|----------|
| [request_engine.py](file:///workspace/backend/core/request_engine.py) | RequestEngine | 请求引擎：发起和管理HTTP请求，执行目标访问和数据提取 | 无 |
| [waf_detector.py](file:///workspace/backend/core/waf_detector.py) | WAFDetector | WAF检测：识别Web应用防火墙，提供绕过策略 | request_engine |
| [strategy_adapter.py](file:///workspace/backend/core/strategy_adapter.py) | StrategyAdapter | 策略适配：动态调整扫描策略，优化任务分配 | waf_detector |
| [chain_engine.py](file:///workspace/backend/core/chain_engine.py) | ChainEngine | 攻击链引擎：分析漏洞关联性，构建攻击链 | 无 |
| [auth_manager.py](file:///workspace/backend/core/auth_manager.py) | AuthManager | 认证管理：管理认证状态和会话，支持多用户上下文 | 无 |

---

### 7. AI 推理 (7 modules)

AI推理模块提供高级分析能力，支持智能决策。

| 模块文件 | 主要类 | 核心职责 | 依赖模块 |
|----------|--------|----------|----------|
| [reasoning_engine.py](file:///workspace/backend/core/reasoning_engine.py) | ReasoningEngine | 推理引擎：实现高级推理能力，对安全场景进行深入分析 | smart_router |
| [token_budget.py](file:///workspace/backend/core/token_budget.py) | TokenBudget | Token预算：管理和控制AI服务中的token使用量 | 无 |
| [endpoint_classifier.py](file:///workspace/backend/core/endpoint_classifier.py) | EndpointClassifier | 端点分类：识别并分类目标端点的属性和类型 | 无 |
| [cve_hunter.py](file:///workspace/backend/core/cve_hunter.py) | CVEHunter | CVE猎手：扫描并识别目标系统中已知的CVE漏洞 | 无 |
| [deep_recon.py](file:///workspace/backend/core/deep_recon.py) | DeepRecon | 深度侦察：收集目标系统的详细信息 | request_engine |
| [banner_analyzer.py](file:///workspace/backend/core/banner_analyzer.py) | BannerAnalyzer | Banner分析：分析目标系统的banner信息，识别版本和服务 | 无 |
| [param_analyzer.py](file:///workspace/backend/core/param_analyzer.py) | ParamAnalyzer | 参数分析：分析请求参数，识别安全风险和注入点 | 无 |

---

### 8. 报告引擎 (2 modules)

| 模块文件 | 主要类 | 核心职责 | 依赖模块 |
|----------|--------|----------|----------|
| [report_generator.py](file:///workspace/backend/core/report_generator.py) | ReportGenerator | 报告生成器：将扫描发现转换为结构化报告 | 无 |
| [report_engine/generator.py](file:///workspace/backend/core/report_engine/generator.py) | ReportEngine | 报告引擎：处理漏洞分析、历史回溯和审计追踪 | report_generator |

---

### 9. 沙箱/CLI 系统 (4 modules)

| 模块文件 | 主要类 | 核心职责 | 依赖模块 |
|----------|--------|----------|----------|
| [tool_executor.py](file:///workspace/backend/core/tool_executor.py) | ToolExecutor | 工具执行器：执行外部工具和插件，扩展扫描能力 | 无 |
| [cli_agent_runner.py](file:///workspace/backend/core/cli_agent_runner.py) | CLIAgentRunner | CLI代理运行器：管理命令行代理的执行和交互 | tool_executor |
| [cli_output_parser.py](file:///workspace/backend/core/cli_output_parser.py) | CLIOutputParser | CLI输出解析器：解析CLI输出，提取结构化数据 | 无 |
| [cli_instructions_builder.py](file:///workspace/backend/core/cli_instructions_builder.py) | CLIInstructionsBuilder | CLI指令构建器：构建CLI指令，用于自动化执行 | 无 |

---

### 10. 其他支撑模块 (15 modules)

| 模块文件 | 主要类 | 核心职责 |
|----------|--------|----------|
| [checkpoint_manager.py](file:///workspace/backend/core/checkpoint_manager.py) | CheckpointManager | 管理扫描进度检查点，支持断点续传和状态恢复 |
| [notification_manager.py](file:///workspace/backend/core/notification_manager.py) | NotificationManager | 处理通知消息（Discord/Telegram/Twilio），支持任务完成和异常告警 |
| [knowledge_processor.py](file:///workspace/backend/core/knowledge_processor.py) | KnowledgeProcessor | 处理和存储知识库信息，为系统提供智能决策支持 |
| [task_library.py](file:///workspace/backend/core/task_library.py) | TaskLibrary | 管理扫描任务模板和调度策略，确保任务的可复用性 |
| [execution_history.py](file:///workspace/backend/core/execution_history.py) | ExecutionHistory | 记录执行历史，用于追踪、审计和回溯 |
| [methodology_loader.py](file:///workspace/backend/core/methodology_loader.py) | MethodologyLoader | 加载和应用不同的检测方法论，注入到代理提示词中 |
| [payload_mutator.py](file:///workspace/backend/core/payload_mutator.py) | PayloadMutator | 变异和生成攻击载荷，增强扫描的覆盖率 |
| [poc_generator.py](file:///workspace/backend/core/poc_generator.py) | POCGenerator | 生成攻击的PoC（Proof of Concept），验证漏洞存在 |
| [poc_validator.py](file:///workspace/backend/core/poc_validator.py) | POCValidator | 验证生成的PoC是否有效，确保漏洞利用的准确性 |
| [exploit_generator.py](file:///workspace/backend/core/exploit_generator.py) | ExploitGenerator | 生成具体的漏洞利用代码，支持自动化利用 |
| [xss_validator.py](file:///workspace/backend/core/xss_validator.py) | XSSValidator | 验证和测试XSS漏洞，确保扫描的有效性 |
| [xss_context_analyzer.py](file:///workspace/backend/core/xss_context_analyzer.py) | XSSContextAnalyzer | 分析XSS漏洞的上下文环境，优化检测和利用策略 |
| [site_analyzer.py](file:///workspace/backend/core/site_analyzer.py) | SiteAnalyzer | 分析网站结构和内容，提取关键信息 |
| [request_repeater.py](file:///workspace/backend/core/request_repeater.py) | RequestRepeater | 重复执行请求，模拟异常行为，增强检测鲁棒性 |
| [prompt_engine/](file:///workspace/backend/core/prompt_engine/) | PromptParser, PromptBuilder, PromptManager | 提示词引擎：解析、构建和管理LLM提示词 |

---

### 数据层架构

| 组件 | 技术 | 用途 |
|------|------|------|
| ORM | SQLAlchemy (Async) | 异步数据库操作 |
| 默认数据库 | SQLite (aiosqlite) | 零配置本地存储 |
| 可选数据库 | PostgreSQL | 生产环境部署 |
| 文件存储 | 本地文件系统 | 报告、知识文档、上传文件 |
| 数据目录 | `/workspace/data/` | 数据库、providers.json、知识库 |

**数据模型关系**:
```
Scan (扫描)
  ├── 1:N → Target (目标URL)
  ├── 1:N → Endpoint (发现的端点)
  ├── 1:N → Vulnerability (发现的漏洞)
  │           └── 1:N → VulnerabilityTest (漏洞测试记录)
  └── 1:N → Report (生成的报告)

AgentTask (代理任务)
  └── N:1 → Scan (关联扫描)

VulnLabChallenge (漏洞实验室挑战)
  └── 1:1 → AgentInstance (可选关联)

Prompt (自定义提示词)
  └── 独立模型

MCP Server (MCP服务器配置)
  └── 独立模型

Scheduler Job (调度任务)
  └── 独立模型
```

---

## 总结

NeuroSploit v3.2.4 是一个功能完整的 AI 驱动渗透测试平台，包含：
- **18 个主要页面** 提供完整的用户界面
- **18 个 API 模块** (80+ 端点) 处理所有后端功能
- **60+ 个核心模块** 组成完整的后端架构
- **50+ 种漏洞类型** 内置检测支持
- **4 种操作模式** 满足不同测试需求
- **Kali Linux 沙箱** 提供安全隔离执行
- **Smart Router** 实现多 LLM 智能管理
- **RAG 知识增强** 提升 AI 专业水平
- **完整报告生成** 输出专业渗透测试文档
- **详细页面布局分析** 提供 UI/UX 结构参考
- **完整参数关联性** 明确数据流与模型关联
- **完整功能测试计划** 覆盖所有系统功能
- **后端核心架构** 10大子系统详细分析
