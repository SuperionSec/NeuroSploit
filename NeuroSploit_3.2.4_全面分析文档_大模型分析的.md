# NeuroSploit v3.2.4 全面分析文档

## 目录

1. [系统概览](#1-系统概览)
2. [后端API接口](#2-后端api接口)
3. [前端页面功能](#3-前端页面功能)
4. [完整功能测试计划](#4-完整功能测试计划)
5. [Providers与Settings大模型配置区别](#5-providers与settings大模型配置区别)
6. [后端核心架构](#6-后端核心架构)
7. [数据模型详解](#7-数据模型详解)
8. [配置与部署](#8-配置与部署)

---

# 1. 系统概览

## 1.1 系统简介

NeuroSploit v3.2.4 是一个 AI 驱动的渗透测试平台，旨在通过大语言模型（LLM）的智能推理能力，实现自动化、系统化的安全评估与漏洞检测。该平台将传统渗透测试方法论与前沿 AI 技术深度融合，提供从目标侦察、漏洞发现、漏洞利用到报告生成的全流程自动化能力，同时保持专业级的安全检测精度和可控性。

平台的核心设计理念是"AI 赋能安全"，通过智能 LLM 路由（Smart Router）实现多提供商负载均衡与故障转移，通过知识增强（RAG）为 AI 代理注入专业安全知识，通过 Kali Linux 沙箱隔离确保工具执行的安全性，最终为安全研究人员和渗透测试工程师提供一套高效、智能、可靠的自动化渗透测试解决方案。

## 1.2 技术栈

### 后端技术栈

| 依赖 | 版本 | 用途 |
|------|------|------|
| Python | 3.11+ | 核心运行时环境 |
| FastAPI | ≥0.109.0 | 高性能异步 Web 框架 |
| Pydantic | ≥2.5.0 | 数据验证与序列化 |
| SQLAlchemy[asyncio] | ≥2.0.0 | 异步 ORM 数据库操作 |
| aiosqlite | ≥0.19.0 | SQLite 异步驱动 |
| aiohttp | ≥3.9.0 | 异步 HTTP 客户端（LLM 请求） |
| anthropic | ≥0.18.0 | Anthropic Claude API SDK |
| openai | ≥1.10.0 | OpenAI API SDK |
| docker | ≥7.0.0 | Docker 容器管理（Kali 沙箱） |
| uvicorn[standard] | ≥0.27.0 | ASGI 服务器 |
| jinja2 | ≥3.1.0 | HTML 报告模板引擎 |
| weasyprint | ≥60.0 | HTML 转 PDF 报告 |
| apscheduler | ≥3.10.0 | 定时扫描调度器 |
| httpx | ≥0.26.0 | 同步/异步 HTTP 客户端 |

### 前端技术栈

| 依赖 | 版本 | 用途 |
|------|------|------|
| React | ^18.2.0 | UI 组件框架 |
| React Router DOM | ^6.21.0 | 前端路由管理 |
| TypeScript | ^5.3.0 | 类型安全的开发语言 |
| Vite | ^5.0.0 | 构建工具与开发服务器 |
| Zustand | ^4.4.0 | 轻量级状态管理 |
| Axios | ^1.6.0 | HTTP 请求客户端 |
| Socket.io-client | ^4.6.0 | WebSocket 实时通信 |
| Recharts | ^2.10.0 | 数据可视化图表 |
| TailwindCSS | ^3.4.0 | 原子化 CSS 框架 |
| lucide-react | ^0.303.0 | 图标库 |

## 1.3 核心特性

### 自动化 AI 安全代理（7种操作模式）

NeuroSploit 提供 7 种 AI 代理操作模式，覆盖从侦察到报告的完整渗透测试生命周期：

1. **Full Auto** — 全自动化渗透测试，从侦察到报告一键完成
2. **Recon Only** — 仅执行目标侦察，收集信息不进行攻击
3. **AI Prompt Mode** — 自定义提示词模式，用户直接控制 AI 行为
4. **Analyze Only** — 仅分析已有数据，不执行主动扫描
5. **Auto Pentest** — 一键自动渗透，自动协调多专家代理
6. **Vuln Lab** — 针对性漏洞实验室，测试特定漏洞类型
7. **Terminal Agent** — 终端交互模式，AI 辅助手动渗透

### 多种漏洞检测模式（100+漏洞类型，70+测试器）

平台内置超过 100 种漏洞类型检测和 70+ 专业测试器，覆盖 OWASP Top 10 及更多：

- **注入类**: SQL 注入、NoSQL 注入、命令注入、LDAP 注入、XXE 注入
- **跨站脚本**: 反射型 XSS、存储型 XSS、DOM 型 XSS
- **服务端请求伪造**: SSRF 基础检测、SSRF 内网探测
- **认证与会话**: 认证绕过、会话固定、权限提升
- **配置安全**: CORS 错误配置、安全头缺失、信息泄露
- **业务逻辑**: IDOR、参数篡改、竞态条件

### Kali Linux 沙箱隔离（Docker容器池）

- 基于 Docker 的 Kali Linux 容器化沙箱
- 每次扫描自动创建隔离容器，扫描完成自动销毁
- 支持容器池管理，监控资源使用
- 孤儿容器自动清理机制
- 内置 nmap、nikto、sqlmap、dirb、gobuster 等安全工具

### 智能 LLM 路由 (Smart Router)

- 多提供商负载均衡和故障转移
- Tier 分级策略：Tier 1（付费）→ Tier 2（廉价）→ Tier 3（免费/本地）
- 同一提供商多账户轮询
- CLI 令牌自动检测（Claude Code、Codex CLI、Gemini CLI 等）
- 配额追踪与令牌过期监控
- 支持 OAuth 和 API Key 两种认证方式

### 知识增强 (RAG)

- BM25/TF-IDF/ChromaDB 三种检索后端
- 支持 PDF/MD/TXT/HTML 文档上传
- 自动文档分块与索引
- 语义向量检索与关键词检索融合
- 为 AI 代理提供专业安全知识上下文

### 全面的报告生成

- HTML/PDF/JSON/ZIP 多格式输出
- AI 自动生成详细渗透测试报告
- Jinja2 模板引擎驱动报告渲染
- WeasyPrint 实现 HTML 到 PDF 转换
- 包含 PoC、修复建议、风险评级等完整内容

### MCP服务器集成

- 支持 Model Context Protocol 服务器管理
- stdio 和 SSE 两种传输方式
- 动态工具发现与调用
- 服务器连接测试与状态监控

### 定时扫描调度

- 基于 APScheduler 的 Cron 调度
- 支持创建、暂停、恢复、删除调度任务
- 可选择代理角色和操作模式
- 自动清理过期任务

## 1.4 启动流程

基于 `main.py` 的应用启动与关闭流程：

### 启动流程

```
应用启动 (uvicorn)
    │
    ├── 1. 打印启动信息
    │   └── 输出 APP_NAME + APP_VERSION
    │
    ├── 2. 初始化数据库 (init_db)
    │   ├── create_all — 创建所有数据表
    │   └── migrations — 执行数据库迁移
    │
    ├── 3. 初始化调度器
    │   ├── 读取 config/config.json
    │   └── ScanScheduler.start() — 启动定时任务调度
    │
    ├── 4. 清理孤立沙箱容器
    │   └── container_pool.cleanup_orphans() — 清理残留容器
    │
    └── 5. 初始化智能路由
        └── smart_router.init_router() — 加载提供商配置、启动Token刷新器
```

### 关闭流程

```
应用关闭 (shutdown event)
    │
    ├── 1. 停止智能路由Token刷新器
    │   └── smart_router.stop_token_refresher()
    │
    ├── 2. 销毁所有沙箱容器
    │   └── container_pool.destroy_all()
    │
    ├── 3. 停止调度器
    │   └── scheduler.shutdown()
    │
    └── 4. 关闭数据库
        └── db_session.close_all()
```

## 1.5 应用配置

### FastAPI 应用配置

| 配置项 | 值 |
|--------|-----|
| title | "NeuroSploit v3" |
| docs_url | "/api/docs" |
| redoc_url | "/api/redoc" |

### CORS 跨域配置

| 配置项 | 值 |
|--------|-----|
| allow_origins | ["http://localhost:3000", "http://127.0.0.1:3000"] |
| allow_credentials | True |
| allow_methods | ["*"] |
| allow_headers | ["*"] |

### 特殊端点

| 方法 | 端点 | 功能描述 |
|------|------|----------|
| GET | /api/health | 健康检查，返回应用状态及LLM配置情况 |
| WebSocket | /ws/scan/{scan_id} | 实时扫描更新推送，支持ping/pong心跳 |

### 前端静态文件服务

| 路径 | 处理方式 |
|------|----------|
| /assets | StaticFiles — 静态资源文件 |
| /{full_path:path} | SPA fallback — 单页应用路由回退 |

## 1.6 路由挂载

18 个 API 模块挂载在 `/api/v1/` 路径下：

| 序号 | 模块名 | 路径前缀 | 核心功能 |
|------|--------|----------|----------|
| 1 | scans | /api/v1/scans | 扫描管理 |
| 2 | targets | /api/v1/targets | 目标管理 |
| 3 | prompts | /api/v1/prompts | 提示词管理 |
| 4 | reports | /api/v1/reports | 报告生成 |
| 5 | dashboard | /api/v1/dashboard | 仪表板数据 |
| 6 | vulnerabilities | /api/v1/vulnerabilities | 漏洞信息 |
| 7 | settings | /api/v1/settings | 系统设置 |
| 8 | agent | /api/v1/agent | AI代理管理 |
| 9 | agent-tasks | /api/v1/agent-tasks | 代理任务 |
| 10 | scheduler | /api/v1/scheduler | 调度任务 |
| 11 | vuln-lab | /api/v1/vuln-lab | 漏洞实验室 |
| 12 | terminal | /api/v1/terminal | 终端代理 |
| 13 | sandbox | /api/v1/sandbox | 沙箱管理 |
| 14 | knowledge | /api/v1/knowledge | 知识库 |
| 15 | mcp | /api/v1/mcp | MCP服务器 |
| 16 | providers | /api/v1/providers | 提供商管理 |
| 17 | full-ia | /api/v1/full-ia | 完整AI测试 |
| 18 | cli-agent | /api/v1/cli-agent | CLI代理 |

---

# 2. 后端API接口

本章详细记录 NeuroSploit v3.2.4 全部 18 个 API 模块的所有端点，包括请求参数、响应模型和关联前端页面。

## 2.1 Scans API — 扫描管理

**路径前缀**: `/api/v1/scans`

扫描管理模块是平台的核心模块之一，提供扫描任务的完整生命周期管理，包括创建、启动、暂停、恢复、停止、删除，以及扫描结果的端点和漏洞查询，还支持漏洞验证和自适应学习反馈。

| 方法 | 端点 | 功能描述 | 请求参数 | 响应模型 | 相关前端 |
|------|------|----------|----------|----------|----------|
| GET | / | 获取扫描列表，支持分页和状态过滤 | skip(int), limit(int), status(str) | ScanListResponse | HomePage, ScanDetailsPage |
| POST | / | 创建新扫描 | ScanCreate(body) | ScanResponse | NewScanPage |
| GET | /{scan_id} | 获取单个扫描详情 | scan_id(path) | ScanResponse | ScanDetailsPage |
| POST | /{scan_id}/start | 启动扫描 | scan_id(path) | ScanResponse | ScanDetailsPage |
| POST | /{scan_id}/stop | 停止运行中的扫描 | scan_id(path) | ScanResponse | ScanDetailsPage |
| POST | /{scan_id}/pause | 暂停运行中的扫描 | scan_id(path) | ScanResponse | ScanDetailsPage |
| POST | /{scan_id}/resume | 恢复暂停的扫描 | scan_id(path) | ScanResponse | ScanDetailsPage |
| POST | /{scan_id}/skip-to/{target_phase} | 跳转到指定扫描阶段 | scan_id(path), target_phase(path) | Dict | ScanDetailsPage |
| GET | /{scan_id}/status | 获取扫描进度 | scan_id(path) | ScanProgress | ScanDetailsPage |
| DELETE | /{scan_id} | 删除扫描 | scan_id(path) | Dict | ReportsPage |
| GET | /{scan_id}/endpoints | 获取扫描发现的端点 | scan_id(path) | List[Endpoint] | ScanDetailsPage |
| GET | /{scan_id}/vulnerabilities | 获取扫描发现的漏洞 | scan_id(path) | List[Vulnerability] | ScanDetailsPage |
| PATCH | /vulnerabilities/{vuln_id}/validate | 手动验证漏洞状态 | vuln_id(path), status(body) | Dict | ScanDetailsPage |
| POST | /vulnerabilities/{vuln_id}/feedback | 提交漏洞真假阳性反馈 | vuln_id(path), is_true_positive(bool), feedback_text(str)(body) | Dict | ScanDetailsPage |
| GET | /vulnerabilities/learning/stats | 获取自适应学习统计 | - | Dict | SettingsPage |

**关键数据模型**:

- **ScanCreate**: target_url, mode, auth_type, auth_value, custom_prompt, task_id, enable_sandbox, enable_browser_validation, llm_provider, llm_model
- **ScanResponse**: id, target_url, status, mode, created_at, updated_at, progress, endpoints_count, vulnerabilities_count
- **ScanProgress**: scan_id, current_phase, total_phases, progress_percent, status
- **ScanListResponse**: items, total, skip, limit

## 2.2 Agent API — AI代理管理

**路径前缀**: `/api/v1/agent`

AI 代理模块是平台最大的 API 模块，提供 33 个端点，覆盖代理的完整生命周期管理、实时任务会话、任务库管理、检查点等功能。

| 方法 | 端点 | 功能描述 | 请求参数 | 响应模型 | 相关前端 |
|------|------|----------|----------|----------|----------|
| GET | /status | 获取LLM配置状态 | - | Dict | HomePage, SettingsPage |
| POST | /run | 启动AI代理 | AgentRunRequest(body) | AgentResponse | NewScanPage, AutoPentestPage |
| POST | /quick | 快速运行代理 | QuickRunRequest(body) | AgentResponse | - |
| GET | /active | 获取所有活跃代理 | - | List[Dict] | HomePage |
| GET | /history | 获取代理历史记录 | limit(int), offset(int) | List[Dict] | AutoPentestPage |
| GET | /by-scan/{scan_id} | 按扫描ID查找代理 | scan_id(path) | Dict | ScanDetailsPage |
| GET | /status/{agent_id} | 获取代理状态和结果 | agent_id(path) | AgentStatus | AgentStatusPage |
| POST | /stop/{agent_id} | 停止运行中的代理 | agent_id(path) | Dict | AgentStatusPage |
| POST | /pause/{agent_id} | 暂停代理 | agent_id(path) | Dict | AgentStatusPage |
| POST | /resume/{agent_id} | 恢复代理 | agent_id(path) | Dict | AgentStatusPage |
| POST | /triple-check/{scan_id} | 三重验证扫描结果 | scan_id(path), provider(str), model(str)(body) | Dict | AutoPentestPage |
| POST | /skip-to/{agent_id}/{target_phase} | 跳转到指定代理阶段 | agent_id(path), target_phase(path) | Dict | AgentStatusPage |
| POST | /prompt/{agent_id} | 发送自定义提示词 | agent_id(path), prompt(str)(body) | Dict | AgentStatusPage |
| GET | /prompts/{agent_id} | 获取代理提示词历史 | agent_id(path) | List[Dict] | - |
| GET | /logs/{agent_id} | 获取代理执行日志 | agent_id(path), limit(int)(query) | List[AgentLog] | AgentStatusPage |
| GET | /findings/{agent_id} | 获取代理发现结果 | agent_id(path) | List[Dict] | AgentStatusPage |
| GET | /tasks | 获取任务列表 | category(str)(query) | List[TaskResponse] | TaskLibraryPage, NewScanPage |
| GET | /tasks/{task_id} | 获取特定任务 | task_id(path) | TaskResponse | TaskLibraryPage |
| POST | /tasks | 创建任务 | TaskCreate(body) | TaskResponse | TaskLibraryPage |
| DELETE | /tasks/{task_id} | 删除任务 | task_id(path) | Dict | TaskLibraryPage |
| DELETE | /{agent_id} | 删除代理结果 | agent_id(path) | Dict | - |
| GET | /realtime/llm-status | 获取LLM连接状态 | - | Dict | RealtimeTaskPage |
| POST | /realtime/session | 创建实时任务会话 | target(str), name(str)(body) | Dict | RealtimeTaskPage |
| POST | /realtime/{session_id}/message | 发送实时消息 | session_id(path), message(str)(body) | Dict | RealtimeTaskPage |
| GET | /realtime/{session_id} | 获取实时会话详情 | session_id(path) | Dict | RealtimeTaskPage |
| GET | /realtime/{session_id}/report | 获取实时会话报告 | session_id(path) | Dict | RealtimeTaskPage |
| DELETE | /realtime/{session_id} | 删除实时会话 | session_id(path) | Dict | RealtimeTaskPage |
| GET | /realtime/sessions/list | 列出所有实时会话 | - | List[Dict] | RealtimeTaskPage |
| GET | /realtime/tools/list | 列出实时工具 | - | List[Dict] | RealtimeTaskPage |
| GET | /realtime/tools/status | 获取工具状态 | - | Dict | RealtimeTaskPage |
| POST | /realtime/{session_id}/execute-tool | 执行实时工具 | session_id(path), tool_name(str), args(dict)(body) | Dict | RealtimeTaskPage |
| GET | /checkpoints | 获取检查点列表 | - | List[Dict] | - |

**关键数据模型**:

- **AgentRunRequest**: target, mode, auth_type, auth_value, custom_prompt, task_id, enable_sandbox, enable_browser_validation, llm_provider, llm_model, enable_subdomain_discovery
- **QuickRunRequest**: target, vuln_type, auth_type, auth_value
- **AgentResponse**: agent_id, scan_id, status, created_at
- **AgentStatus**: agent_id, status, current_phase, findings, logs, started_at, updated_at
- **AgentLog**: id, agent_id, log_type, message, timestamp
- **TaskCreate**: name, description, category, steps, prompt_template
- **TaskResponse**: id, name, description, category, steps, is_custom, created_at

## 2.3 Reports API — 报告生成

**路径前缀**: `/api/v1/reports`

报告模块提供扫描结果的报告生成、查看、下载和删除功能，支持 AI 自动生成和手动生成两种方式，输出格式包括 HTML、PDF、JSON 和 ZIP。

| 方法 | 端点 | 功能描述 | 请求参数 | 响应模型 | 相关前端 |
|------|------|----------|----------|----------|----------|
| GET | / | 获取报告列表，支持过滤 | scan_id(str), auto_generated(bool), skip(int), limit(int) | ReportListResponse | ReportsPage |
| POST | / | 生成新报告 | scan_id(str), format(str), title(str), include_poc(bool), include_remediation(bool)(body) | ReportResponse | ScanDetailsPage |
| POST | /ai-generate | AI生成详细报告 | scan_id(str), title(str), preferred_provider(str), preferred_model(str)(body) | ReportResponse | ScanDetailsPage, AutoPentestPage |
| GET | /{report_id} | 获取报告详情 | report_id(path) | ReportResponse | ReportViewPage |
| GET | /{report_id}/view | 查看报告(HTML) | report_id(path) | HTML | ReportViewPage |
| GET | /{report_id}/download/{format} | 下载报告(HTML/PDF/JSON) | report_id(path), format(path: html/pdf/json) | File | ReportViewPage |
| GET | /{report_id}/download-zip | 下载ZIP格式报告 | report_id(path) | ZIP File | ScanDetailsPage |
| DELETE | /{report_id} | 删除报告 | report_id(path) | Dict | ReportsPage |

**关键数据模型**:

- **ReportResponse**: id, scan_id, title, format, auto_generated, created_at, vulnerability_count, severity_summary
- **ReportListResponse**: items, total, skip, limit

## 2.4 Vuln Lab API — 漏洞实验室

**路径前缀**: `/api/v1/vuln-lab`

漏洞实验室模块提供针对性漏洞测试功能，支持选择特定漏洞类型进行深度测试，并以挑战（Challenge）的形式管理测试过程。

| 方法 | 端点 | 功能描述 | 请求参数 | 响应模型 | 相关前端 |
|------|------|----------|----------|----------|----------|
| GET | /types | 获取所有漏洞类型和分类 | - | Dict | VulnLabPage |
| POST | /run | 运行漏洞实验室测试 | target_url(str), vuln_type(str), auth_type(str), auth_value(str), challenge_name(str)(body) | VulnLabResponse | VulnLabPage |
| GET | /challenges | 获取挑战列表 | - | List[Dict] | VulnLabPage |
| GET | /challenges/{challenge_id} | 获取挑战详情 | challenge_id(path) | Dict | VulnLabPage |
| GET | /stats | 获取漏洞实验室统计 | - | Dict | VulnLabPage |
| POST | /challenges/{challenge_id}/stop | 停止挑战 | challenge_id(path) | Dict | VulnLabPage |
| DELETE | /challenges/{challenge_id} | 删除挑战 | challenge_id(path) | Dict | VulnLabPage |
| GET | /logs/{challenge_id} | 获取挑战日志 | challenge_id(path) | List[Dict] | VulnLabPage |

**关键数据模型**:

- **VulnLabResponse**: challenge_id, status, vuln_type, target_url, created_at
- 漏洞类型分类结构: category → sub_types

## 2.5 Terminal API — 终端代理

**路径前缀**: `/api/v1/terminal`

终端代理模块提供交互式终端会话管理，支持 AI 聊天、命令执行、利用路径记录和 VPN 连接管理。

| 方法 | 端点 | 功能描述 | 请求参数 | 响应模型 | 相关前端 |
|------|------|----------|----------|----------|----------|
| GET | /templates | 获取可用模板列表 | - | List[Dict] | TerminalAgentPage |
| POST | /session | 创建终端会话 | target(str), name(str), template_id(str), use_sandbox(bool)(body) | Dict | TerminalAgentPage |
| GET | /sessions | 列出所有终端会话 | - | List[Dict] | TerminalAgentPage |
| GET | /sessions/{session_id} | 获取会话详情 | session_id(path) | Dict | TerminalAgentPage |
| DELETE | /sessions/{session_id} | 删除会话 | session_id(path) | Dict | TerminalAgentPage |
| POST | /sessions/{session_id}/message | 发送聊天消息 | session_id(path), message(str)(body) | Dict | TerminalAgentPage |
| POST | /sessions/{session_id}/execute | 执行命令 | session_id(path), command(str)(body) | Dict | TerminalAgentPage |
| POST | /sessions/{session_id}/exploitation-path | 创建利用路径 | session_id(path), steps(list)(body) | Dict | TerminalAgentPage |
| GET | /sessions/{session_id}/exploitation-path | 获取利用路径 | session_id(path) | Dict | TerminalAgentPage |
| POST | /sessions/{session_id}/vpn/upload | 上传VPN配置 | session_id(path), file(upload), username(str), password(str)(form) | Dict | TerminalAgentPage |
| POST | /sessions/{session_id}/vpn/connect | 连接VPN | session_id(path) | Dict | TerminalAgentPage |
| POST | /sessions/{session_id}/vpn/disconnect | 断开VPN | session_id(path) | Dict | TerminalAgentPage |
| GET | /sessions/{session_id}/vpn-status | 获取VPN状态 | session_id(path) | Dict | TerminalAgentPage |

**关键数据模型**:

- 会话创建参数: target, name, template_id, use_sandbox
- 消息格式: message (str)
- 命令执行: command (str)
- 利用路径: steps (list of exploitation step objects)
- VPN上传: file (UploadFile), username, password (form fields)

## 2.6 Providers API — 提供商管理

**路径前缀**: `/api/v1/providers`

提供商管理模块是 Smart Router 的管理接口，支持多 LLM 提供商的账户管理、CLI 令牌检测、连接测试、配额监控和环境变量编辑。

| 方法 | 端点 | 功能描述 | 请求参数 | 响应模型 | 相关前端 |
|------|------|----------|----------|----------|----------|
| GET | / | 列出所有LLM提供商和账户 | - | Dict | ProvidersPage |
| GET | /status | 获取使用配额和状态汇总 | - | Dict | ProvidersPage |
| POST | /detect-all | 自动检测所有CLI令牌 | - | Dict | ProvidersPage |
| POST | /{provider_id}/detect | 检测单个提供商令牌 | provider_id(path) | Dict | ProvidersPage |
| POST | /{provider_id}/connect | 连接提供商账户 | provider_id(path), api_key(str), label(str)(body) | Dict | ProvidersPage |
| DELETE | /{provider_id}/accounts/{account_id} | 删除账户 | provider_id(path), account_id(path) | Dict | ProvidersPage |
| POST | /test/{provider_id}/{account_id} | 测试账户连接 | provider_id(path), account_id(path) | Dict | ProvidersPage |
| GET | /available-models | 获取可用模型列表 | - | Dict | ProvidersPage, AutoPentestPage |
| POST | /{provider_id}/toggle | 切换提供商启用状态 | provider_id(path) | Dict | ProvidersPage |
| GET | /env | 获取环境变量 | - | Dict | ProvidersPage |
| POST | /env | 更新环境变量 | env_vars(dict)(body) | Dict | ProvidersPage |

**关键数据模型**:

- 提供商信息: provider_id, name, tier, enabled, accounts
- 账户信息: account_id, label, api_key(masked), status, token_usage, expires_at
- 配额状态: provider_id, total_tokens, used_tokens, remaining_tokens, account_count
- 环境变量: key-value pairs from .env file

## 2.7 Dashboard API — 仪表板数据

**路径前缀**: `/api/v1/dashboard`

仪表板模块为首页提供所有统计数据，包括概览统计、最近扫描、发现结果、漏洞分布、历史趋势、代理任务和活动日志。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | /stats | 获取仪表板统计数据（扫描总数、运行中扫描数、完成扫描数、漏洞总数等） | HomePage |
| GET | /recent | 获取最近扫描记录 | HomePage |
| GET | /findings | 获取最近发现结果 | HomePage |
| GET | /vulnerability-types | 获取漏洞类型分布统计 | HomePage |
| GET | /scan-history | 获取扫描历史趋势 | HomePage |
| GET | /agent-tasks | 获取最近的代理任务 | HomePage |
| GET | /activity-feed | 获取活动日志流 | HomePage |

**关键数据模型**:

- stats: total_scans, active_scans, completed_scans, total_vulnerabilities, critical_count, high_count, medium_count, low_count
- recent: list of recent scan summaries
- findings: list of recent vulnerability findings
- vulnerability-types: category distribution for pie chart
- scan-history: time-series data for trend chart
- agent-tasks: list of recent agent task summaries
- activity-feed: list of activity log entries

## 2.8 Settings API — 系统设置

**路径前缀**: `/api/v1/settings`

系统设置模块提供全局配置管理，包括 LLM 默认设置、功能开关、通知配置、数据库管理和工具检测。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | / | 获取当前系统设置 | SettingsPage |
| PUT | / | 更新系统设置 | SettingsPage |
| POST | /notifications/test/{channel} | 测试通知渠道(discord/telegram/whatsapp) | SettingsPage |
| POST | /clear-database | 清空数据库 | SettingsPage |
| GET | /stats | 获取数据库统计 | SettingsPage |
| GET | /tools | 检测可用工具 | SettingsPage |
| GET | /models/{provider} | 获取指定提供商的模型目录 | SettingsPage |

**关键数据模型**:

- Settings: llm_provider, llm_model, api_key(masked), max_output_tokens, enable_model_routing, enable_knowledge, enable_browser_validation, enable_reasoning, enable_cve_hunter, enable_multi_agent, enable_researcher_ai, notification_config
- notification channel: discord / telegram / whatsapp
- tools: list of detected security tools with availability status
- models: list of available models for the specified provider

## 2.9 Sandbox API — 沙箱管理

**路径前缀**: `/api/v1/sandbox`

沙箱管理模块提供 Docker 容器化的 Kali Linux 沙箱管理，支持容器列表查看、详情查询、销毁和清理操作。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | / | 列出所有沙箱容器 | SandboxDashboardPage |
| GET | /{scan_id} | 获取沙箱容器详情 | SandboxDashboardPage |
| DELETE | /{scan_id} | 销毁沙箱容器 | SandboxDashboardPage |
| POST | /cleanup | 清理过期容器 | SandboxDashboardPage |
| POST | /cleanup-orphans | 清理孤儿容器 | SandboxDashboardPage |

**关键数据模型**:

- 容器列表: list of container objects with id, scan_id, status, image, created_at, resource_usage
- 容器详情: id, scan_id, status, image, ip, ports, tools, health, resource_usage(cpu/memory)
- 清理结果: cleaned_count, remaining_count

## 2.10 Knowledge API — 知识库

**路径前缀**: `/api/v1/knowledge`

知识库模块提供 RAG 系统的文档管理接口，支持文档上传、索引、检索和统计。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| POST | /upload | 上传知识文档(PDF/MD/TXT/HTML) | KnowledgePage |
| GET | /documents | 列出所有知识文档 | KnowledgePage |
| GET | /documents/{doc_id} | 获取文档详情和条目 | KnowledgePage |
| DELETE | /documents/{doc_id} | 删除知识文档 | KnowledgePage |
| GET | /search | 搜索知识库内容 | KnowledgePage |
| GET | /stats | 获取知识库统计 | KnowledgePage |

**关键数据模型**:

- 文档上传: file (UploadFile), 支持格式 PDF/MD/TXT/HTML
- 文档列表: list of document objects with id, filename, file_type, chunk_count, vuln_types, created_at
- 文档详情: id, filename, file_type, chunks, metadata, vuln_types
- 搜索参数: query (str), top_k (int)
- 统计: total_documents, total_chunks, total_vuln_types_covered, backend_type

## 2.11 MCP API — MCP服务器管理

**路径前缀**: `/api/v1/mcp`

MCP 服务器模块提供 Model Context Protocol 服务器的完整 CRUD 管理，包括创建、配置、测试和工具发现。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | /servers | 列出所有MCP服务器 | MCPManagementPage |
| GET | /servers/{name} | 获取特定MCP服务器详情 | MCPManagementPage |
| POST | /servers | 创建MCP服务器 | MCPManagementPage |
| PUT | /servers/{name} | 更新MCP服务器配置 | MCPManagementPage |
| DELETE | /servers/{name} | 删除MCP服务器 | MCPManagementPage |
| POST | /servers/{name}/toggle | 切换服务器启用状态 | MCPManagementPage |
| POST | /servers/{name}/test | 测试服务器连接 | MCPManagementPage |
| GET | /servers/{name}/tools | 列出服务器提供的工具 | MCPManagementPage |

**关键数据模型**:

- 服务器配置: name, transport_type(stdio/sse), command/url, args, env, enabled, description
- 服务器详情: name, transport_type, status, enabled, tools_count, last_test_result
- 工具列表: list of tool objects with name, description, input_schema

## 2.12 Scheduler API — 调度任务

**路径前缀**: `/api/v1/scheduler`

调度任务模块提供基于 Cron 表达式的定时扫描任务管理，支持任务的创建、删除、暂停和恢复。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | / | 列出所有调度任务 | SchedulerPage |
| POST | / | 创建调度任务 | SchedulerPage |
| DELETE | /{job_id} | 删除调度任务 | SchedulerPage |
| POST | /{job_id}/pause | 暂停调度任务 | SchedulerPage |
| POST | /{job_id}/resume | 恢复调度任务 | SchedulerPage |
| GET | /agent-roles | 获取代理角色列表 | SchedulerPage |

**关键数据模型**:

- 调度任务创建: name, target_url, cron_expression, agent_role, mode, auth_type, auth_value
- 调度任务列表: list of job objects with id, name, target_url, cron_expression, status, last_run, next_run
- 代理角色: list of available agent role names

## 2.13 Targets API — 目标管理

**路径前缀**: `/api/v1/targets`

目标管理模块提供目标 URL 的验证、批量验证、文件上传和输入解析功能。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| POST | /validate | 验证单个目标URL | NewScanPage |
| POST | /validate/bulk | 批量验证目标URL | NewScanPage |
| POST | /upload | 上传目标文件 | NewScanPage |
| POST | /parse-input | 解析目标输入 | NewScanPage |

**关键数据模型**:

- 验证请求: url (str)
- 批量验证请求: urls (list[str])
- 文件上传: file (UploadFile)
- 输入解析: input (str), 支持逗号分隔、换行分隔等多种格式
- 验证响应: url, is_valid, resolved_ip, http_status, redirect_url

## 2.14 Vulnerabilities API — 漏洞信息

**路径前缀**: `/api/v1/vulnerabilities`

漏洞信息模块提供漏洞类型和漏洞详情的查询接口。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | /types | 获取所有漏洞类型 | VulnLabPage |
| GET | /types/{category} | 按类别获取漏洞类型 | VulnLabPage |
| GET | /types/{category}/{vuln_type} | 获取漏洞类型详情 | VulnLabPage |
| GET | /{vuln_id} | 获取特定漏洞详情 | ScanDetailsPage |

**关键数据模型**:

- 漏洞类型列表: list of categories with sub_types
- 漏洞类型详情: name, category, description, severity, detection_method, remediation
- 漏洞详情: id, scan_id, vuln_type, severity, url, parameter, payload, response, confidence, verified, created_at

## 2.15 Prompts API — 提示词管理

**路径前缀**: `/api/v1/prompts`

提示词管理模块提供预设提示词和自定义提示词的完整 CRUD 管理，包括模板解析和文件上传。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | /presets | 获取预设提示词列表 | NewScanPage |
| GET | /presets/{preset_id} | 获取特定预设提示词 | NewScanPage |
| POST | /parse | 解析提示词模板 | NewScanPage |
| GET | / | 列出自定义提示词 | SettingsPage |
| POST | / | 创建自定义提示词 | SettingsPage |
| GET | /{prompt_id} | 获取特定提示词 | SettingsPage |
| PUT | /{prompt_id} | 更新提示词 | SettingsPage |
| DELETE | /{prompt_id} | 删除提示词 | SettingsPage |
| POST | /upload | 上传提示词文件 | SettingsPage |

**关键数据模型**:

- 预设提示词: id, name, description, category, template
- 自定义提示词: id, name, content, category, created_at, updated_at
- 模板解析: template (str), variables (dict) → rendered prompt
- 文件上传: file (UploadFile), 支持格式 MD/TXT

## 2.16 Full IA API — 完整AI测试

**路径前缀**: `/api/v1/full-ia`

完整 AI 测试模块提供获取 AI 渗透测试完整提示内容的接口。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | /prompt | 获取完整AI渗透测试提示内容 | FullIATestingPage |

**关键数据模型**:

- 响应: prompt (str), 包含完整的 AI 渗透测试系统提示词和方法论

## 2.17 CLI Agent API — CLI代理

**路径前缀**: `/api/v1/cli-agent`

CLI 代理模块提供 CLI 代理的提供商信息和方法论列表查询。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | /providers | 获取CLI代理提供商信息 | AutoPentestPage |
| GET | /methodologies | 获取方法论列表 | AutoPentestPage |

**关键数据模型**:

- 提供商信息: list of CLI-compatible provider objects
- 方法论列表: list of methodology objects with name, description, phases

## 2.18 Agent Tasks API — 代理任务

**路径前缀**: `/api/v1/agent-tasks`

代理任务模块提供代理任务的查询和扫描时间线接口。

| 方法 | 端点 | 功能描述 | 相关前端 |
|------|------|----------|----------|
| GET | / | 列出代理任务 | TaskLibraryPage |
| GET | /summary | 获取代理任务摘要 | TaskLibraryPage |
| GET | /{task_id} | 获取特定代理任务 | TaskLibraryPage |
| GET | /scan/{scan_id}/timeline | 获取扫描任务时间线 | ScanDetailsPage |

**关键数据模型**:

- 任务列表: list of task objects with id, name, category, status, created_at
- 任务摘要: total_tasks, by_category, by_status
- 任务详情: id, name, description, category, steps, prompt_template, is_custom
- 时间线: list of timeline events with timestamp, phase, action, result

## 2.19 特殊端点

除上述 18 个 API 模块外，系统还提供以下特殊端点：

| 方法 | 端点 | 功能描述 |
|------|------|----------|
| GET | /api/health | 健康检查，返回应用状态及LLM配置情况 |
| WebSocket | /ws/scan/{scan_id} | 实时扫描更新推送，支持ping/pong心跳 |

**健康检查响应**:

```json
{
  "status": "healthy",
  "version": "3.2.4",
  "llm_configured": true,
  "llm_provider": "anthropic",
  "database_connected": true,
  "docker_available": true
}
```

**WebSocket 消息格式**:

```json
{
  "type": "scan_update",
  "scan_id": "uuid",
  "data": {
    "status": "running",
    "current_phase": "vulnerability_testing",
    "progress": 65,
    "new_findings": [...]
  }
}
```

## 2.20 API 汇总统计

| 统计项 | 数值 |
|--------|------|
| API 模块总数 | 18 |
| API 端点总数 | 151（含 2 个特殊端点） |
| 最大模块 | Agent API — 33 个端点 |
| 端点数 ≥ 8 的模块 | Scans(15), Agent(33), Reports(8), Vuln Lab(8), Terminal(13), Providers(11), MCP(8) |
| 仅查询模块 | Dashboard(7), Vulnerabilities(4), Full IA(1), CLI Agent(2), Agent Tasks(4) |

**各模块端点数量分布**:

| 模块 | 端点数 |
|------|--------|
| Agent | 33 |
| Terminal | 13 |
| Scans | 15 |
| Providers | 11 |
| Prompts | 9 |
| MCP | 8 |
| Reports | 8 |
| Vuln Lab | 8 |
| Dashboard | 7 |
| Settings | 7 |
| Knowledge | 6 |
| Scheduler | 6 |
| Sandbox | 5 |
| Targets | 4 |
| Vulnerabilities | 4 |
| Agent Tasks | 4 |
| CLI Agent | 2 |
| Full IA | 1 |
| 特殊端点 | 2 |
| **合计** | **151** |

---

# 3. 前端页面功能

NeuroSploit v3.2.4 前端共包含 18 个页面，覆盖从扫描创建、代理监控、漏洞测试到报告生成的完整渗透测试工作流。以下逐一列出每个页面的所有交互元素及其调用的 API。

### Page 1: HomePage (/)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 统计卡片网格 | 显示总扫描数、运行中、完成、总漏洞 | GET /api/v1/dashboard/stats |
| 活跃代理卡片 | 显示当前运行中的AI代理 | GET /api/v1/agent/active |
| 最近扫描列表 | 显示最近扫描记录，可点击查看详情 | GET /api/v1/dashboard/recent |
| 活动日志流 | 显示系统活动历史，支持5种过滤(All/Scans/Vulns/Tasks/Reports) | GET /api/v1/dashboard/activity-feed |
| 刷新按钮 | 刷新所有仪表板数据 | GET /api/v1/dashboard/stats, recent, activity-feed, agent/active |
| 快速操作按钮 | 跳转到 Auto Pentest, New Scan, Vuln Lab, Terminal, Full IA | 路由导航 |
| 连接丢失提示 | WebSocket断连时显示警告 | 本地状态 |

---

### Page 2: NewScanPage (/scan/new)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 操作模式选择 | 4种模式: Full Auto, Recon Only, AI Prompt Mode, Analyze Only | - |
| 目标模式选择 | 3种: Single URL, Multiple URLs, Upload File | - |
| 单URL输入 | 输入目标URL | - |
| 多URL文本区 | 批量输入URL | - |
| 文件上传 | 上传.txt/.csv/.lst文件 | POST /api/v1/targets/upload |
| 任务库切换 | 显示/隐藏任务库 | - |
| 任务分类过滤 | 6种: All/Full Auto/Recon/Vuln/Custom/Reporting | GET /api/v1/agent/tasks |
| 任务卡片选择 | 选择预定义任务 | - |
| 清除任务 | 清除已选任务 | - |
| 自定义提示词开关 | 切换使用自定义提示词 | - |
| 自定义提示词输入 | 输入自定义提示词 | - |
| 认证类型选择 | 5种: None/Cookie/Bearer/Basic/Header | - |
| 认证值输入 | 输入认证凭据 | - |
| 高级选项切换 | 显示/隐藏高级选项 | - |
| 最大爬取深度 | 滑块1-10 | - |
| 部署代理按钮 | 创建扫描并跳转到AgentStatusPage | POST /api/v1/targets/validate/bulk, POST /api/v1/agent/run |
| 取消按钮 | 返回首页 | 路由导航 / |

---

### Page 3: AutoPentestPage (/auto) — 最复杂的页面(~2008行)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 目标URL输入 | 输入渗透测试目标 | - |
| 多目标切换 | 启用多目标模式 | - |
| 多目标文本区 | 输入额外目标 | - |
| 子域发现开关 | 启用/禁用子域枚举 | - |
| Kali沙箱开关 | 启用/禁用Kali沙箱 | - |
| 认证配置 | 展开认证选项(5种类型) | - |
| 自定义AI提示词 | 展开自定义提示词输入 | - |
| 已保存提示词 | 展开已保存提示词列表，支持多选 | GET /api/v1/prompts |
| 测试模式选择 | Auto Pentest / CLI Agent | - |
| CLI提供商选择 | 选择CLI代理提供商 | GET /api/v1/cli-agent/providers |
| 方法论选择 | 选择渗透测试方法论 | GET /api/v1/cli-agent/methodologies |
| CLI阶段开关 | 启用/禁用CLI代理阶段 | - |
| LLM提供商/模型选择 | 选择LLM提供商和模型 | GET /api/v1/providers/available-models |
| 开始渗透按钮 | 启动完整自动化渗透测试 | POST /api/v1/agent/run |
| 停止按钮 | 停止运行中的测试 | POST /api/v1/agent/stop/{id} |
| 测试历史 | 显示历史测试记录 | GET /api/v1/agent/history |
| 三重验证 | 对历史扫描执行三重验证 | POST /api/v1/agent/triple-check/{scan_id} |
| 重新运行 | 重新运行历史测试 | - |
| 多会话标签 | 多个并行扫描会话 | - |
| 发现结果过滤 | All/Confirmed/Rejected | - |
| 日志过滤 | all/stream1/stream2/stream3/deep/container/cli_agent/error | - |
| 生成AI报告 | 测试完成后生成AI报告 | POST /api/v1/reports/ai-generate |
| 下载ZIP | 下载ZIP格式报告 | GET /api/v1/reports/{id}/download-zip |

---

### Page 4: ScanDetailsPage (/scan/:scanId)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 返回按钮 | 返回上一页 | 路由导航 |
| 查看代理状态按钮 | 跳转到AgentStatusPage | 路由导航 /agent/:id |
| 扫描信息卡片 | 显示目标URL、状态、进度条、创建时间 | GET /api/v1/scans/{id} |
| 暂停/恢复/停止按钮 | 控制扫描执行 | POST /api/v1/scans/{id}/pause, resume, stop |
| 阶段跳转 | 跳转到指定执行阶段(需确认) | POST /api/v1/scans/{id}/skip-to/{phase} |
| 删除按钮 | 删除扫描 | DELETE /api/v1/scans/{id} |
| 统计卡片 | 显示端点数、漏洞数、Critical/High数量 | GET /api/v1/scans/{id} |
| 4个选项卡 | Vulnerabilities/Endpoints/Agent Tasks/Activity Log | - |
| 验证状态过滤 | All/Confirmed/Rejected/Validated | - |
| 漏洞展开/折叠 | 查看漏洞详情(PoC、请求、响应) | - |
| 复制PoC | 复制漏洞PoC到剪贴板 | - |
| 验证漏洞 | 手动验证漏洞状态 | PATCH /api/v1/scans/vulnerabilities/{vid}/validate |
| 标记误报/确认TP | 弹出反馈模态框 | POST /api/v1/scans/vulnerabilities/{vid}/feedback |
| 撤销验证 | 恢复之前的验证状态 | PATCH /api/v1/scans/vulnerabilities/{vid}/validate |
| 端点测试按钮 | 对单个端点执行测试 | POST /api/v1/agent/run |
| 生成报告 | 生成标准报告 | POST /api/v1/reports |
| AI报告 | 选择提供商/模型后生成AI报告 | POST /api/v1/reports/ai-generate |
| 查看报告 | 在新窗口查看报告 | GET /api/v1/reports/{id}/view |
| 下载ZIP | 下载ZIP格式报告 | GET /api/v1/reports/{id}/download-zip |
| 日志搜索 | 搜索日志内容 | - |
| 日志过滤 | All/Recon/Junior/Tools/Deep/Errors | - |
| 工具执行展开 | 查看Kali工具执行详情 | - |
| WebSocket实时更新 | 实时推送扫描进度 | WS /ws/scan/{id} |
| 已用时间计时器 | 显示扫描已运行时间 | 本地计算 |

---

### Page 5: AgentStatusPage (/agent/:agentId)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 返回按钮 | 返回上一页 | 路由导航 |
| 查看扫描详情按钮 | 跳转到ScanDetailsPage | 路由导航 /scan/{id} |
| 代理状态卡片 | 显示代理ID、状态、当前阶段 | GET /api/v1/agent/status/{id} |
| 暂停/恢复/停止按钮 | 控制代理执行 | POST /api/v1/agent/pause/resume/stop/{id} |
| 阶段跳转 | 跳转到指定阶段(需确认) | POST /api/v1/agent/skip-to/{id}/{phase} |
| 执行日志面板 | 实时显示代理执行日志，支持自动滚动 | GET /api/v1/agent/logs/{id} |
| 发现结果面板 | 显示发现的漏洞和端点，支持展开/折叠 | GET /api/v1/agent/findings/{id} |
| 自定义提示词输入 | 发送自定义指令给AI代理(支持Enter键) | POST /api/v1/agent/prompt/{id} |
| 复制payload/请求/响应/PoC | 复制到剪贴板 | - |
| 生成报告 | 生成HTML/JSON/AI报告 | POST /api/v1/reports/ai-generate |
| 刷新按钮 | 刷新代理状态和日志 | GET /api/v1/agent/status/{id}, logs/{id} |

---

### Page 6: VulnLabPage (/vuln-lab)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 3个选项卡 | Test/History/Stats | - |
| 漏洞类型选择 | 按分类选择漏洞类型 | GET /api/v1/vuln-lab/types |
| 目标URL输入 | 输入实验室目标 | - |
| 挑战名称输入 | 输入挑战名称 | - |
| 认证配置 | 展开认证选项(5种类型) | - |
| 笔记输入 | 输入测试笔记 | - |
| 搜索过滤 | 搜索漏洞类型 | - |
| 开始测试按钮 | 启动针对性漏洞测试 | POST /api/v1/vuln-lab/run |
| 停止测试按钮 | 停止正在运行的测试 | POST /api/v1/vuln-lab/challenges/{id}/stop |
| 实时日志 | 显示测试执行日志 | - |
| 挑战列表 | 显示所有历史挑战 | GET /api/v1/vuln-lab/challenges |
| 挑战展开/折叠 | 查看挑战详情 | GET /api/v1/vuln-lab/challenges/{id} |
| 删除挑战 | 删除历史挑战 | DELETE /api/v1/vuln-lab/challenges/{id} |
| 查看扫描详情 | 跳转到关联的扫描详情 | 路由导航 /scan/{id} |
| 统计面板 | 显示测试统计和漏洞分布 | GET /api/v1/vuln-lab/stats |

---

### Page 7: TerminalAgentPage (/terminal)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 创建会话按钮 | 创建新终端会话 | POST /api/v1/terminal/session |
| 会话列表 | 显示所有终端会话 | GET /api/v1/terminal/sessions |
| 删除会话 | 删除终端会话 | DELETE /api/v1/terminal/sessions/{id} |
| 模板选择 | 选择预定义场景模板 | GET /api/v1/terminal/templates |
| 聊天区域 | 与AI助手对话 | POST /api/v1/terminal/sessions/{id}/message |
| 命令输入框 | 手动输入命令 | POST /api/v1/terminal/sessions/{id}/execute |
| 沙箱/直连切换 | 切换沙箱模式 | - |
| VPN管理 | 上传.ovpn配置文件 | POST /api/v1/terminal/sessions/{id}/vpn/upload |
| VPN连接 | 连接VPN | POST /api/v1/terminal/sessions/{id}/vpn/connect |
| VPN断开 | 断开VPN | POST /api/v1/terminal/sessions/{id}/vpn/disconnect |
| VPN状态 | 查看VPN连接状态 | GET /api/v1/terminal/sessions/{id}/vpn-status |
| 利用路径 | 创建和查看利用路径 | POST/GET /api/v1/terminal/sessions/{id}/exploitation-path |
| 建议命令 | 快速输入常用命令 | - |

---

### Page 8: ProvidersPage (/providers)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 提供商列表 | 显示所有LLM提供商和账户 | GET /api/v1/providers |
| 配额状态卡片 | 显示各提供商的配额使用情况 | GET /api/v1/providers/status |
| 检测所有CLI令牌 | 自动检测本地CLI工具令牌 | POST /api/v1/providers/detect-all |
| 提供商卡片点击 | 打开配置模态框 | - |
| 提供商启用/禁用 | 切换提供商启用状态 | POST /api/v1/providers/{id}/toggle |
| 环境变量编辑器 | 查看/编辑.env配置 | GET/POST /api/v1/providers/env |
| 配置模态框: 检测CLI令牌 | 检测单个提供商令牌 | POST /api/v1/providers/{id}/detect |
| 配置模态框: 添加凭据 | 手动添加API Key | POST /api/v1/providers/{id}/connect |
| 配置模态框: 测试连接 | 测试单个账户连接 | POST /api/v1/providers/test/{pid}/{aid} |
| 配置模态框: 删除账户 | 删除提供商账户 | DELETE /api/v1/providers/{pid}/accounts/{aid} |
| 可用模型列表 | 查看提供商支持的模型 | GET /api/v1/providers/available-models |
| 刷新按钮 | 刷新提供商数据 | GET /api/v1/providers, /status |

---

### Page 9: SettingsPage (/settings)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| LLM提供商选择 | 8种: claude/openai/gemini/openrouter/together/fireworks/ollama/lmstudio | GET/PUT /api/v1/settings |
| LLM模型选择 | 选择默认模型 | GET /api/v1/settings/models/{provider} |
| API Key输入(6个) | Anthropic/OpenAI/OpenRouter/Gemini/Together/Fireworks | PUT /api/v1/settings |
| Ollama/LM Studio URL | 输入本地LLM地址 | PUT /api/v1/settings |
| 最大输出Token | 设置全局最大输出token | PUT /api/v1/settings |
| 最大并发扫描数 | 设置最大并发扫描数 | PUT /api/v1/settings |
| 激进模式开关 | 启用/禁用激进模式 | PUT /api/v1/settings |
| 启用模型路由开关 | 启用/禁用Smart Router | PUT /api/v1/settings |
| 启用知识增强开关 | 启用/禁用RAG | PUT /api/v1/settings |
| 启用浏览器验证开关 | 启用/禁用浏览器验证 | PUT /api/v1/settings |
| 启用通知开关 | 启用/禁用通知 | PUT /api/v1/settings |
| Discord Webhook URL | 配置Discord通知 | PUT /api/v1/settings |
| Telegram Bot Token/Chat ID | 配置Telegram通知 | PUT /api/v1/settings |
| Twilio配置(4项) | 配置WhatsApp通知 | PUT /api/v1/settings |
| 通知严重级别过滤 | 设置通知过滤级别 | PUT /api/v1/settings |
| 测试Discord/Telegram/WhatsApp | 测试通知渠道 | POST /api/v1/settings/notifications/test/{channel} |
| 工具检测 | 检测可用工具 | GET /api/v1/settings/tools |
| 数据库统计 | 显示数据库统计信息 | GET /api/v1/settings/stats |
| 清空数据库按钮 | 清空所有数据(需确认) | POST /api/v1/settings/clear-database |
| 保存设置 | 保存所有设置 | PUT /api/v1/settings |

---

### Page 10: FullIATestingPage (/full-ia)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 目标URL输入 | 输入渗透测试目标 | - |
| 认证配置 | 展开认证选项 | - |
| LLM提供商/模型选择 | 选择LLM | GET /api/v1/providers/available-models |
| 查看渗透提示 | 预览完整LLM渗透测试提示 | GET /api/v1/full-ia/prompt |
| 开始测试按钮 | 启动完整AI渗透测试 | POST /api/v1/agent/run (mode=full_llm_pentest) |
| 停止按钮 | 停止运行中的测试 | POST /api/v1/agent/stop/{id} |
| 2个选项卡 | Findings/Log | - |
| 发现结果过滤 | All/Confirmed/Rejected | - |
| 日志过滤 | All/LLM Pentest/AI Decisions/Errors | - |
| 日志搜索 | 搜索日志内容 | - |
| 工具执行展开 | 查看工具执行详情 | - |
| 查看完整结果 | 跳转到AgentStatusPage | 路由导航 /agent/{id} |
| 生成AI报告 | 测试完成后生成报告 | POST /api/v1/reports/ai-generate |
| 查看报告/下载ZIP | 查看或下载报告 | GET /api/v1/reports/{id}/view, download-zip |

---

### Page 11: MCPManagementPage (/mcp)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 服务器列表 | 显示所有MCP服务器 | GET /api/v1/mcp/servers |
| 添加服务器 | 打开创建模态框 | - |
| 传输类型选择 | stdio或sse | - |
| 服务器名称/命令/参数/URL/环境变量/描述 | 创建/编辑服务器表单 | - |
| 启用/禁用切换 | 切换服务器启用状态 | POST /api/v1/mcp/servers/{name}/toggle |
| 测试连接 | 测试服务器连接 | POST /api/v1/mcp/servers/{name}/test |
| 编辑服务器 | 打开编辑模态框 | - |
| 删除服务器 | 删除MCP服务器(需确认) | DELETE /api/v1/mcp/servers/{name} |
| 工具浏览器 | 展开查看服务器提供的工具 | GET /api/v1/mcp/servers/{name}/tools |
| 保存服务器 | 创建或更新服务器 | POST/PUT /api/v1/mcp/servers |

---

### Page 12: SchedulerPage (/scheduler)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 调度任务列表 | 显示所有定时任务 | GET /api/v1/scheduler/ |
| 创建调度 | 打开创建表单 | - |
| 扫描类型选择 | Quick/Full/Custom | - |
| 调度模式选择 | Preset/Days/Interval | - |
| Cron预设(8种+Custom) | 选择调度时间 | - |
| 自定义Cron表达式 | 输入自定义Cron | - |
| 执行时间选择 | 小时(0-23)/分钟(00/15/30/45) | - |
| 星期选择 | Sun-Sat + Weekdays/Weekends/Every Day快捷 | - |
| 间隔选择(8种) | 选择间隔分钟数 | - |
| 代理角色选择 | 选择扫描代理角色 | GET /api/v1/scheduler/agent-roles |
| 创建调度按钮 | 创建调度任务 | POST /api/v1/scheduler/ |
| 暂停/恢复调度 | 控制调度任务 | POST /api/v1/scheduler/{id}/pause, resume |
| 删除调度 | 删除调度任务(需确认) | DELETE /api/v1/scheduler/{id} |

---

### Page 13: KnowledgePage (/knowledge)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 文档上传(拖拽) | 上传PDF/MD/TXT/HTML文件 | POST /api/v1/knowledge/upload |
| 文档列表 | 显示所有知识文档 | GET /api/v1/knowledge/documents |
| 漏洞类型过滤 | 按漏洞类型筛选文档 | GET /api/v1/knowledge/search |
| 文档展开/折叠 | 查看文档详细内容和条目 | GET /api/v1/knowledge/documents/{id} |
| 删除文档 | 删除知识文档(需确认) | DELETE /api/v1/knowledge/documents/{id} |
| 统计卡片 | 显示文档数、条目数、覆盖漏洞类型数 | GET /api/v1/knowledge/stats |
| 刷新按钮 | 刷新知识库数据 | GET /api/v1/knowledge/stats, documents |

---

### Page 14: RealtimeTaskPage (/realtime)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 创建会话 | 创建新的实时任务会话 | POST /api/v1/agent/realtime/session |
| 会话列表 | 显示所有实时会话 | GET /api/v1/agent/realtime/sessions/list |
| 会话点击 | 切换到指定会话 | GET /api/v1/agent/realtime/{id} |
| 删除会话 | 删除实时会话 | DELETE /api/v1/agent/realtime/{id} |
| 聊天输入框 | 发送消息给AI代理 | POST /api/v1/agent/realtime/{id}/message |
| 快速提示(6种) | Security Headers/Full Scan/XSS/SQLi/Dir Enum/Tech Stack | - |
| 工具按钮 | 打开工具模态框 | GET /api/v1/agent/realtime/tools/status |
| 工具执行(6种) | ffuf/feroxbuster/nuclei/nmap/nikto/httpx | POST /api/v1/agent/realtime/{id}/execute-tool |
| 生成报告 | 生成实时会话报告 | GET /api/v1/agent/realtime/{id}/report |
| 下载JSON | 下载JSON格式报告 | GET /api/v1/agent/realtime/{id}/report |
| LLM状态指示器 | 显示LLM连接状态 | GET /api/v1/agent/realtime/llm-status |
| 发现结果展开/折叠 | 查看发现的漏洞 | - |
| 消息展开/折叠 | 查看完整消息内容 | - |

---

### Page 15: SandboxDashboardPage (/sandboxes)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 容器列表 | 显示所有Kali沙箱容器 | GET /api/v1/sandbox/ |
| 健康检查 | 检查容器健康状态 | GET /api/v1/sandbox/{id} |
| 销毁容器 | 销毁指定沙箱容器(需确认) | DELETE /api/v1/sandbox/{id} |
| 清理过期按钮 | 清理过期容器 | POST /api/v1/sandbox/cleanup |
| 清理孤儿按钮 | 清理孤儿容器 | POST /api/v1/sandbox/cleanup-orphans |
| 刷新按钮 | 刷新容器列表 | GET /api/v1/sandbox/ |
| 查看关联扫描 | 跳转到关联的扫描详情 | 路由导航 /scan/{id} |

---

### Page 16: TaskLibraryPage (/tasks)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 任务列表 | 显示所有预定义任务 | GET /api/v1/agent/tasks |
| 分类过滤(6种) | All/Full Auto/Recon/Vuln/Custom/Reporting | GET /api/v1/agent/tasks |
| 搜索框 | 搜索任务名称 | 本地搜索 |
| 任务卡片选择 | 查看任务详情 | - |
| 使用任务按钮 | 将任务用于新扫描 | 路由导航 /scan/new |
| 创建自定义任务 | 打开创建模态框 | - |
| 创建表单: 名称/描述/分类/提示词/系统提示词/标签 | 创建新任务 | POST /api/v1/agent/tasks |
| 删除任务 | 删除自定义任务(需确认) | DELETE /api/v1/agent/tasks/{id} |
| 刷新按钮 | 刷新任务列表 | GET /api/v1/agent/tasks |

---

### Page 17: ReportsPage (/reports)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 报告列表 | 显示所有报告 | GET /api/v1/reports |
| 格式过滤(4种) | All/HTML/JSON/PDF | - |
| 排序(3种) | Date/Name/Vulns | - |
| 搜索框 | 搜索报告 | - |
| 查看报告 | 在新窗口查看 | GET /api/v1/reports/{id}/view |
| 下载HTML/JSON | 下载各种格式的报告 | GET /api/v1/reports/{id}/download/{format} |
| 下载ZIP | 下载ZIP格式 | GET /api/v1/reports/{id}/download-zip |
| AI重新生成 | AI重新生成报告 | POST /api/v1/reports/ai-generate |
| 删除报告 | 删除报告(需确认) | DELETE /api/v1/reports/{id} |
| 新建扫描 | 跳转到新建扫描 | 路由导航 /scan/new |

---

### Page 18: ReportViewPage (/reports/:reportId)

| 组件/按钮 | 功能描述 | 调用API |
|----------|----------|--------|
| 返回按钮 | 返回报告列表页 | 路由导航 /reports |
| 刷新按钮 | 刷新报告内容(重新加载iframe) | - |
| 全屏按钮 | 切换全屏模式 | 本地状态 |
| HTML下载按钮 | 下载HTML格式报告 | GET /api/v1/reports/{id}/download/html |
| JSON下载按钮 | 下载JSON格式报告 | GET /api/v1/reports/{id}/download/json |
| 新标签页打开 | 在新窗口查看报告 | GET /api/v1/reports/{id}/view |
| 报告iframe | 内嵌显示HTML报告 | GET /api/v1/reports/{id}/view |

---

### 页面路由图

```
Sidebar导航结构:
├── Operations
│   ├── / → HomePage (Dashboard)
│   ├── /auto → AutoPentestPage
│   ├── /scan/new → NewScanPage
│   ├── /realtime → RealtimeTaskPage
│   └── /full-ia → FullIATestingPage
├── Tools
│   ├── /vuln-lab → VulnLabPage
│   ├── /terminal → TerminalAgentPage
│   ├── /sandboxes → SandboxDashboardPage
│   ├── /tasks → TaskLibraryPage
│   ├── /knowledge → KnowledgePage
│   ├── /mcp → MCPManagementPage
│   └── /providers → ProvidersPage
└── Configuration
    ├── /scheduler → SchedulerPage
    ├── /reports → ReportsPage
    └── /settings → SettingsPage

动态路由:
├── /scan/:scanId → ScanDetailsPage
├── /agent/:agentId → AgentStatusPage
└── /reports/:reportId → ReportViewPage
```

---

### 页面间数据流转

```
用户创建扫描 → NewScanPage → POST /api/v1/agent/run → 跳转 AgentStatusPage
    │
    ├── AgentStatusPage → GET /api/v1/agent/status/{id} → 实时查看代理执行
    │   ├── 暂停/恢复/停止 → POST pause/resume/stop
    │   ├── 发送自定义提示词 → POST /api/v1/agent/prompt/{id}
    │   └── 跳转 ScanDetailsPage → /scan/{scan_id}
    │
    └── ScanDetailsPage → GET /api/v1/scans/{id} → 查看扫描详情
        ├── 查看端点/漏洞/任务/日志 → 4个Tab
        ├── 验证漏洞 → PATCH validate / POST feedback
        ├── 跳转 AgentStatusPage → /agent/{agent_id}
        ├── 生成报告 → POST /api/v1/reports 或 ai-generate
        └── 查看报告 → ReportViewPage → /reports/{id}

AutoPentestPage → POST /api/v1/agent/run (mode=auto_pentest)
    └── 多会话并行 → 每个会话独立跟踪状态

FullIATestingPage → POST /api/v1/agent/run (mode=full_llm_pentest)
    └── 4阶段进度 (Recon→Testing→PostExploit→Report)

VulnLabPage → POST /api/v1/vuln-lab/run
    └── 挑战管理 → 查看/停止/删除挑战

RealtimeTaskPage → POST /api/v1/agent/realtime/session
    └── 实时对话 → 发送消息/执行工具/生成报告
```

---

# 4. 完整功能测试计划

### 测试环境信息

| 项目 | 信息 |
|------|------|
| 系统版本 | NeuroSploit v3.2.4 |
| 后端地址 | http://localhost:8000 |
| API 版本 | /api/v1 |
| 测试日期 | 2026-05-19 |
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
| 沙箱管理 | 6 | P1 |
| 知识库 | 8 | P1 |
| MCP服务器 | 7 | P1 |
| 实时任务 | 8 | P1 |
| 提供商管理 | 10 | P2 |
| 设置页面 | 10 | P2 |
| 调度器 | 6 | P2 |
| Full IA | 6 | P2 |
| 任务库 | 6 | P2 |
| **合计** | **132** | - |

---

### P0 优先级测试用例（核心功能）

#### 1. 首页/仪表板测试

| 用例ID | 测试项 | 预期结果 | 测试方法 |
|--------|--------|----------|----------|
| HOME-001 | 页面加载 | 首页正常加载，显示统计卡片、图表、活跃代理、最近扫描 | 访问 http://localhost:8000/ |
| HOME-002 | 统计数据 | 显示正确的扫描总数、活跃代理数、漏洞数、报告数 | 验证数字显示 |
| HOME-003 | 快速操作按钮 | 点击各按钮跳转到对应页面 | 测试 Auto Pentest, New Scan, Vuln Lab, Terminal, Full IA |
| HOME-004 | 活跃代理列表 | 显示正在运行的代理，支持点击查看详情 | 检查实时更新 |
| HOME-005 | 最近扫描列表 | 显示最近的扫描记录，支持点击查看详情 | 验证数据正确 |
| HOME-006 | 活动日志流 | 显示系统活动历史，支持5种过滤 | 验证日志刷新和过滤 |
| HOME-007 | 刷新按钮 | 点击刷新所有仪表板数据 | 验证数据更新 |
| HOME-008 | 连接丢失提示 | WebSocket断连时显示警告 | 断开网络测试 |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/dashboard/stats
curl http://localhost:8000/api/v1/agent/active
curl http://localhost:8000/api/v1/dashboard/recent
curl http://localhost:8000/api/v1/dashboard/activity-feed
```

---

#### 2. 新建扫描测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| NEW-001 | 页面加载 | NewScanPage 正常加载，显示所有表单元素 | - |
| NEW-002 | 操作模式切换 | Tabs 切换 4 种模式 (Full Auto, Recon Only, AI Prompt Mode, Analyze Only) | - |
| NEW-003 | 目标模式选择 | 支持 Single URL, Multiple URLs, Upload File 三种模式 | - |
| NEW-004 | 单URL输入 | 支持输入目标 URL | - |
| NEW-005 | 多URL文本区 | 支持批量输入URL | - |
| NEW-006 | 文件上传 | 支持上传 .txt/.csv/.lst 文件 | - |
| NEW-007 | 任务库选择 | 显示预定义任务列表，支持6种分类过滤 | - |
| NEW-008 | 自定义提示词 | 支持输入自定义提示词 | - |
| NEW-009 | 认证配置 | 支持 None/Cookie/Bearer/Basic/Header 5种类型 | - |
| NEW-010 | 高级选项 | 显示最大爬取深度滑块(1-10) | - |
| NEW-011 | 部署代理 | 点击后创建扫描并跳转到 AgentStatusPage | 需要配置 LLM |
| NEW-012 | 取消按钮 | 返回首页 | - |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/agent/tasks
curl -X POST http://localhost:8000/api/v1/targets/upload -F "file=@targets.txt"
curl -X POST http://localhost:8000/api/v1/targets/validate/bulk \
  -H "Content-Type: application/json" \
  -d '{"targets": ["http://example.com"]}'
```

---

#### 3. 自动渗透测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| AUTO-001 | 页面加载 | AutoPentestPage 正常加载 | - |
| AUTO-002 | 目标输入 | 支持输入目标 URL，支持多目标模式 | - |
| AUTO-003 | 子域发现 | 可选启用子域发现 | - |
| AUTO-004 | Kali 沙箱 | 可选启用 Kali 沙箱 | Docker 运行 |
| AUTO-005 | 开始扫描 | 点击后启动自动渗透流程 | 需要配置 LLM |
| AUTO-006 | 测试历史 | 显示历史测试记录，支持三重验证和重新运行 | - |

**API 测试命令**:
```bash
curl -X POST http://localhost:8000/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{"target": "http://example.com", "mode": "auto_pentest"}'
curl http://localhost:8000/api/v1/agent/history
curl -X POST http://localhost:8000/api/v1/agent/triple-check/{scan_id}
```

---

#### 4. 扫描详情测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| SCAN-001 | 页面加载 | ScanDetailsPage 正常加载 | 需要存在扫描记录 |
| SCAN-002 | 扫描信息卡片 | 显示目标 URL、状态、进度、创建时间 | - |
| SCAN-003 | 扫描控制 | 支持暂停、恢复、停止、删除操作 | 扫描运行中 |
| SCAN-004 | 阶段跳转 | 支持跳转到指定执行阶段(需确认) | 扫描运行中 |
| SCAN-005 | 统计卡片 | 显示端点数、漏洞数、各严重级别数量 | - |
| SCAN-006 | 4个选项卡 | Vulnerabilities/Endpoints/Agent Tasks/Activity Log 切换正常 | - |
| SCAN-007 | 漏洞验证 | 支持验证、标记误报/确认TP、撤销验证 | - |
| SCAN-008 | AI 报告生成 | 支持生成 AI 报告，可选择提供商/模型 | - |
| SCAN-009 | WebSocket实时更新 | 实时推送扫描进度 | 扫描运行中 |
| SCAN-010 | 返回导航 | 返回按钮和查看代理状态按钮正常工作 | - |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/scans/{scan_id}
curl -X POST http://localhost:8000/api/v1/scans/{scan_id}/pause
curl -X POST http://localhost:8000/api/v1/scans/{scan_id}/resume
curl -X POST http://localhost:8000/api/v1/scans/{scan_id}/stop
curl -X POST http://localhost:8000/api/v1/scans/{scan_id}/skip-to/{phase}
curl -X PATCH http://localhost:8000/api/v1/scans/vulnerabilities/{vid}/validate
curl -X POST http://localhost:8000/api/v1/scans/vulnerabilities/{vid}/feedback
```

---

### P1 优先级测试用例（重要功能）

#### 5. 代理状态测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| AGENT-001 | 页面加载 | AgentStatusPage 正常加载 | 需要存在代理记录 |
| AGENT-002 | 代理状态显示 | 显示代理 ID、状态、当前阶段 | - |
| AGENT-003 | 执行日志 | 实时显示代理执行日志，支持自动滚动 | 代理运行中 |
| AGENT-004 | 发现结果 | 显示发现的漏洞和端点，支持展开/折叠 | - |
| AGENT-005 | 控制按钮 | 支持暂停、恢复、停止代理 | - |
| AGENT-006 | 自定义提示词 | 支持发送自定义提示词给 AI (支持Enter键) | 代理运行中 |
| AGENT-007 | 阶段跳转 | 支持跳转到指定阶段(需确认) | 代理运行中 |
| AGENT-008 | 生成报告 | 支持生成 HTML/JSON/AI 报告 | 代理完成 |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/agent/status/{agent_id}
curl http://localhost:8000/api/v1/agent/logs/{agent_id}
curl http://localhost:8000/api/v1/agent/findings/{agent_id}
curl -X POST http://localhost:8000/api/v1/agent/prompt/{agent_id} \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your custom instruction"}'
curl -X POST http://localhost:8000/api/v1/agent/skip-to/{agent_id}/{phase}
```

---

#### 6. 报告管理测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| REP-001 | 页面加载 | ReportsPage 正常加载 | - |
| REP-002 | 报告列表 | 显示所有报告 | - |
| REP-003 | 格式过滤 | 支持 All/HTML/JSON/PDF 过滤 | - |
| REP-004 | 排序 | 支持 Date/Name/Vulns 排序 | - |
| REP-005 | 查看报告 | 点击查看打开报告详情页 | - |
| REP-006 | 下载报告 | 支持 HTML/JSON/ZIP 下载 | - |
| REP-007 | 删除报告 | 支持删除单个报告(需确认) | - |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/reports
curl -O http://localhost:8000/api/v1/reports/{report_id}/download/html
curl -O http://localhost:8000/api/v1/reports/{report_id}/download-zip
curl -X DELETE http://localhost:8000/api/v1/reports/{report_id}
```

---

#### 7. 漏洞实验室测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| VULN-001 | 页面加载 | VulnLabPage 正常加载 | - |
| VULN-002 | 漏洞类型分类 | 显示漏洞分类和类型列表 | - |
| VULN-003 | 目标输入 | 支持输入目标 URL 和挑战名称 | - |
| VULN-004 | 认证配置 | 支持配置认证信息(5种类型) | - |
| VULN-005 | 开始测试 | 点击后启动漏洞测试 | 需要配置 LLM |
| VULN-006 | 停止测试 | 支持停止正在运行的测试 | 测试运行中 |
| VULN-007 | 挑战列表 | 显示所有历史挑战，支持展开/折叠和删除 | - |
| VULN-008 | 统计面板 | 显示测试统计和漏洞分布 | - |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/vuln-lab/types
curl http://localhost:8000/api/v1/vuln-lab/challenges
curl -X POST http://localhost:8000/api/v1/vuln-lab/run \
  -H "Content-Type: application/json" \
  -d '{"vuln_type": "xss_reflected", "target_url": "http://example.com"}'
curl -X POST http://localhost:8000/api/v1/vuln-lab/challenges/{id}/stop
curl -X DELETE http://localhost:8000/api/v1/vuln-lab/challenges/{id}
curl http://localhost:8000/api/v1/vuln-lab/stats
```

---

#### 8. 终端代理测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| TERM-001 | 页面加载 | TerminalAgentPage 正常加载 | - |
| TERM-002 | 场景模板 | 显示预定义模板 | - |
| TERM-003 | 创建会话 | 支持创建新的终端会话 | 需要配置 LLM |
| TERM-004 | 聊天交互 | 支持与 AI 聊天交互 | 有活跃会话 |
| TERM-005 | 命令执行 | 支持执行系统命令，支持沙箱/直连切换 | 有活跃会话 |
| TERM-006 | VPN管理 | 支持上传.ovpn、连接/断开VPN、查看状态 | 有活跃会话 |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/terminal/templates
curl -X POST http://localhost:8000/api/v1/terminal/session
curl -X POST http://localhost:8000/api/v1/terminal/sessions/{id}/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Run nmap scan"}'
curl -X POST http://localhost:8000/api/v1/terminal/sessions/{id}/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "nmap -p 80,443 localhost"}'
curl -X POST http://localhost:8000/api/v1/terminal/sessions/{id}/vpn/upload \
  -F "file=@config.ovpn"
curl -X POST http://localhost:8000/api/v1/terminal/sessions/{id}/vpn/connect
```

---

#### 9. 沙箱管理测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| SAND-001 | 页面加载 | SandboxDashboardPage正常加载 | - |
| SAND-002 | 容器列表 | 显示所有Kali沙箱容器 | Docker运行 |
| SAND-003 | 健康检查 | 检查容器健康状态 | 容器运行中 |
| SAND-004 | 销毁容器 | 销毁指定沙箱容器 | 容器存在 |
| SAND-005 | 清理过期 | 清理过期容器 | 存在过期容器 |
| SAND-006 | 清理孤儿 | 清理孤儿容器 | 存在孤儿容器 |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/sandbox/
curl http://localhost:8000/api/v1/sandbox/{id}
curl -X DELETE http://localhost:8000/api/v1/sandbox/{id}
curl -X POST http://localhost:8000/api/v1/sandbox/cleanup
curl -X POST http://localhost:8000/api/v1/sandbox/cleanup-orphans
```

---

#### 10. 知识库测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| KNOW-001 | 页面加载 | KnowledgePage正常加载 | - |
| KNOW-002 | 文档上传 | 支持上传PDF/MD/TXT/HTML | - |
| KNOW-003 | 文档列表 | 显示所有知识文档 | 有上传文档 |
| KNOW-004 | 文档详情 | 查看文档详细内容和条目 | 有上传文档 |
| KNOW-005 | 删除文档 | 删除知识文档 | 有上传文档 |
| KNOW-006 | 搜索知识 | 搜索知识库内容 | 有上传文档 |
| KNOW-007 | 统计卡片 | 显示文档数、条目数 | - |
| KNOW-008 | 漏洞类型过滤 | 按漏洞类型筛选文档 | 有上传文档 |

**API 测试命令**:
```bash
curl -X POST http://localhost:8000/api/v1/knowledge/upload -F "file=@doc.pdf"
curl http://localhost:8000/api/v1/knowledge/documents
curl http://localhost:8000/api/v1/knowledge/documents/{id}
curl http://localhost:8000/api/v1/knowledge/search?q=xss
curl http://localhost:8000/api/v1/knowledge/stats
curl -X DELETE http://localhost:8000/api/v1/knowledge/documents/{id}
```

---

#### 11. MCP服务器测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| MCP-001 | 页面加载 | MCPManagementPage正常加载 | - |
| MCP-002 | 服务器列表 | 显示所有MCP服务器 | - |
| MCP-003 | 创建服务器 | 支持创建stdio/sse类型服务器 | - |
| MCP-004 | 编辑服务器 | 修改服务器配置 | 有服务器 |
| MCP-005 | 启用/禁用 | 切换服务器启用状态 | 有服务器 |
| MCP-006 | 测试连接 | 测试服务器连接 | 有服务器 |
| MCP-007 | 工具列表 | 查看服务器提供的工具 | 服务器已连接 |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/mcp/servers
curl -X POST http://localhost:8000/api/v1/mcp/servers \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "transport_type": "stdio", "command": "node", "args": ["server.js"]}'
curl -X POST http://localhost:8000/api/v1/mcp/servers/{name}/toggle
curl -X POST http://localhost:8000/api/v1/mcp/servers/{name}/test
curl http://localhost:8000/api/v1/mcp/servers/{name}/tools
curl -X DELETE http://localhost:8000/api/v1/mcp/servers/{name}
```

---

#### 12. 实时任务测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| REAL-001 | 页面加载 | RealtimeTaskPage正常加载 | - |
| REAL-002 | 创建会话 | 创建新的实时任务会话 | 需要配置LLM |
| REAL-003 | 发送消息 | 发送消息给AI代理 | 有活跃会话 |
| REAL-004 | 快速提示 | 使用预定义提示(Security Headers/Full Scan/XSS/SQLi/Dir Enum/Tech Stack) | 有活跃会话 |
| REAL-005 | 工具执行 | 执行安全工具(ffuf/feroxbuster/nuclei/nmap/nikto/httpx) | 有活跃会话+Docker |
| REAL-006 | 生成报告 | 生成实时会话报告 | 会话有发现 |
| REAL-007 | 删除会话 | 删除实时会话 | 有会话 |
| REAL-008 | LLM状态 | 显示LLM连接状态 | - |

**API 测试命令**:
```bash
curl -X POST http://localhost:8000/api/v1/agent/realtime/session
curl http://localhost:8000/api/v1/agent/realtime/sessions/list
curl -X POST http://localhost:8000/api/v1/agent/realtime/{id}/message \
  -H "Content-Type: application/json" \
  -d '{"message": "Check security headers"}'
curl -X POST http://localhost:8000/api/v1/agent/realtime/{id}/execute-tool \
  -H "Content-Type: application/json" \
  -d '{"tool": "nmap", "args": "-p 80,443 target"}'
curl http://localhost:8000/api/v1/agent/realtime/{id}/report
curl http://localhost:8000/api/v1/agent/realtime/llm-status
curl -X DELETE http://localhost:8000/api/v1/agent/realtime/{id}
```

---

### P2 优先级测试用例（辅助功能）

#### 13. 提供商管理测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| PROV-001 | 页面加载 | ProvidersPage 正常加载 | - |
| PROV-002 | 提供商列表 | 显示所有 LLM 提供商 | - |
| PROV-003 | 使用配额 | 显示各提供商的配额使用情况 | - |
| PROV-004 | CLI 检测 | 支持自动检测所有 CLI 令牌 | CLI 工具已安装 |
| PROV-005 | 连接测试 | 支持手动连接和测试账户 | - |
| PROV-006 | 环境变量编辑器 | 查看/编辑.env配置 | - |
| PROV-007 | 单提供商检测 | 检测单个提供商令牌 | CLI工具已安装 |
| PROV-008 | 提供商切换 | 启用/禁用提供商 | 有提供商 |
| PROV-009 | 添加凭据 | 手动添加API Key | - |
| PROV-010 | 删除账户 | 删除提供商账户 | 有账户 |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/providers
curl http://localhost:8000/api/v1/providers/status
curl -X POST http://localhost:8000/api/v1/providers/detect-all
curl -X POST http://localhost:8000/api/v1/providers/{id}/detect
curl -X POST http://localhost:8000/api/v1/providers/{id}/toggle
curl -X POST http://localhost:8000/api/v1/providers/{id}/connect \
  -H "Content-Type: application/json" \
  -d '{"label": "My Key", "api_key": "sk-..."}'
curl -X POST http://localhost:8000/api/v1/providers/test/{pid}/{aid}
curl -X DELETE http://localhost:8000/api/v1/providers/{pid}/accounts/{aid}
curl http://localhost:8000/api/v1/providers/env
curl -X POST http://localhost:8000/api/v1/providers/env \
  -H "Content-Type: application/json" \
  -d '{"key": "ANTHROPIC_API_KEY", "value": "sk-ant-..."}'
```

---

#### 14. 设置页面测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| SET-001 | 页面加载 | SettingsPage 正常加载 | - |
| SET-002 | 功能开关 | 支持启用/禁用各项功能 | - |
| SET-003 | 默认配置 | 支持设置默认 LLM 提供商和模型 | - |
| SET-004 | 保存设置 | 保存所有设置 | - |
| SET-005 | 通知配置 | 配置Discord/Telegram/WhatsApp | 有Webhook/Token |
| SET-006 | 测试通知 | 测试通知渠道 | 已配置通知 |
| SET-007 | 工具检测 | 检测可用工具 | - |
| SET-008 | 数据库统计 | 显示数据库统计信息 | - |
| SET-009 | 清空数据库 | 清空所有数据 | 需确认 |
| SET-010 | 模型目录 | 获取指定提供商的模型列表 | - |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/settings
curl -X PUT http://localhost:8000/api/v1/settings \
  -H "Content-Type: application/json" \
  -d '{"llm_provider": "claude", "enable_model_routing": true}'
curl http://localhost:8000/api/v1/settings/models/claude
curl -X POST http://localhost:8000/api/v1/settings/notifications/test/discord
curl -X POST http://localhost:8000/api/v1/settings/notifications/test/telegram
curl http://localhost:8000/api/v1/settings/tools
curl http://localhost:8000/api/v1/settings/stats
curl -X POST http://localhost:8000/api/v1/settings/clear-database
```

---

#### 15. 调度器测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| SCHED-001 | 页面加载 | SchedulerPage正常加载 | - |
| SCHED-002 | 创建调度 | 创建定时扫描任务 | - |
| SCHED-003 | 暂停调度 | 暂停调度任务 | 有调度任务 |
| SCHED-004 | 恢复调度 | 恢复暂停的调度任务 | 有暂停任务 |
| SCHED-005 | 删除调度 | 删除调度任务 | 有调度任务 |
| SCHED-006 | 代理角色 | 获取代理角色列表 | - |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/scheduler/
curl -X POST http://localhost:8000/api/v1/scheduler/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Daily Scan", "cron": "0 8 * * *", "target": "http://example.com"}'
curl -X POST http://localhost:8000/api/v1/scheduler/{id}/pause
curl -X POST http://localhost:8000/api/v1/scheduler/{id}/resume
curl -X DELETE http://localhost:8000/api/v1/scheduler/{id}
curl http://localhost:8000/api/v1/scheduler/agent-roles
```

---

#### 16. Full IA测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| FIA-001 | 页面加载 | FullIATestingPage正常加载 | - |
| FIA-002 | 目标输入 | 支持输入目标URL | - |
| FIA-003 | LLM选择 | 选择LLM提供商和模型 | - |
| FIA-004 | 查看提示 | 预览完整LLM渗透测试提示 | - |
| FIA-005 | 开始测试 | 启动完整AI渗透测试 | 需要配置LLM |
| FIA-006 | 生成报告 | 测试完成后生成AI报告 | 测试已完成 |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/full-ia/prompt
curl http://localhost:8000/api/v1/providers/available-models
curl -X POST http://localhost:8000/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{"target": "http://example.com", "mode": "full_llm_pentest"}'
curl -X POST http://localhost:8000/api/v1/reports/ai-generate \
  -H "Content-Type: application/json" \
  -d '{"scan_id": "{id}", "provider": "claude"}'
```

---

#### 17. 任务库测试

| 用例ID | 测试项 | 预期结果 | 前置条件 |
|--------|--------|----------|----------|
| TASK-001 | 页面加载 | TaskLibraryPage正常加载 | - |
| TASK-002 | 任务列表 | 显示预定义任务列表 | - |
| TASK-003 | 分类过滤 | 按类别筛选任务(6种) | - |
| TASK-004 | 搜索任务 | 搜索任务名称 | - |
| TASK-005 | 创建任务 | 创建自定义任务 | - |
| TASK-006 | 删除任务 | 删除自定义任务 | 有自定义任务 |

**API 测试命令**:
```bash
curl http://localhost:8000/api/v1/agent/tasks
curl -X POST http://localhost:8000/api/v1/agent/tasks \
  -H "Content-Type: application/json" \
  -d '{"name": "Custom Task", "category": "custom", "prompt": "..."}'
curl -X DELETE http://localhost:8000/api/v1/agent/tasks/{id}
```

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
| 2026-05-19 | - | 0/132 | 0 | 0 | 初始测试 |

#### 测试用例结果

| 用例ID | 执行状态 | 执行时间 | 备注 |
|--------|----------|----------|------|
| HOME-001 | Pass/Fail/Blocked | - | - |
| HOME-002 | Pass/Fail/Blocked | - | - |

---

# 5. Providers与Settings大模型配置区别

### 概述

Providers 页面和 Settings 页面虽然都涉及大模型配置，但它们的**定位、作用层级和配置方式**完全不同。Settings 是"基础/默认"的单提供商模式，Providers 是"高级/多提供商"的 Smart Router 路由模式。

---

### Settings 页面 — 基础/默认配置

**定位**: 系统全局的**默认 LLM 配置**，是"传统"的单提供商模式。

| 配置项 | 说明 |
|--------|------|
| `llm_provider` | 选择**唯一的默认提供商** (claude/openai/gemini/openrouter/together/fireworks/ollama/lmstudio) |
| `llm_model` | 选择默认模型 |
| API Key 输入 | 为选中的提供商**直接输入 API Key**，保存到 `.env` 文件 |
| `max_output_tokens` | 全局最大输出 token 限制 |
| `max_concurrent_scans` | 最大并发扫描数 |
| `aggressive_mode` | 激进模式开关 |
| `enable_model_routing` | 启用/禁用模型路由功能 |
| `enable_knowledge_enhancement` | 启用/禁用RAG知识增强 |
| `enable_browser_verification` | 启用/禁用浏览器验证 |
| `enable_notifications` | 启用/禁用通知 |
| 通知配置 | Discord Webhook / Telegram Bot / Twilio(WhatsApp) |
| `notification_severity_filter` | 通知严重级别过滤 |

**关键特征**:
- **单提供商模式**: 一次只用一个 LLM 提供商
- **API Key 存储在 `.env` 文件**: 如 `ANTHROPIC_API_KEY=sk-ant-...`
- **通过 `PUT /api/v1/settings` 保存**: 修改后需要重启服务
- **不启用 Smart Router 时生效**: 这是 `ENABLE_SMART_ROUTER=false` 时的默认行为

---

### Providers 页面 — Smart Router 多提供商管理

**定位**: Smart Router 的**多提供商、多账户管理**，是"高级"的多提供商路由模式。

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
| **环境变量编辑器** | ❌ 无 | ✅ 直接编辑.env |
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

### 环境变量编辑器功能

ProvidersPage内置环境变量编辑器，通过 GET/POST /api/v1/providers/env 端点直接查看和修改 .env 文件内容。支持搜索过滤、只显示允许的键（envAllowedKeys）、实时编辑和保存。

---

### Minimax配置实例

1. 在Providers页面找到Minimax提供商卡片
2. 点击打开配置模态框
3. 输入Label（如"Minimax-M2.7"）
4. 输入API Key（sk-cp-...）
5. 点击"Add Credential"添加账户
6. 点击"Test Connection"测试连接
7. 默认配置: base_url=https://api.minimaxi.com/v1, default_model=MiniMax-M2.7

---

### Smart Router请求路由详细流程（含方法调用链）

```
LLM 请求 → SmartRouter.route(prompt, system, max_tokens, ...)
    │
    ├── 1. SmartRouter._select_provider(preferred_provider)
    │   ├── 检查 preferred_provider 是否指定
    │   ├── ProviderRegistry.get_providers() → 按 Tier 排序
    │   ├── 遍历每个 Provider 的 accounts
    │   ├── ProviderAccount.is_available() → 检查配额和过期
    │   └── 轮询选择下一个可用账户
    │
    ├── 2. SmartRouter._call_provider(provider, account, prompt, system, max_tokens, model, temperature)
    │   ├── 构建 OpenAI/Anthropic/Gemini 格式请求
    │   ├── aiohttp.ClientSession(trust_env=True) → 支持代理
    │   └── 发送 POST 请求到 provider.base_url
    │
    ├── 3. SmartRouter._parse_openai_response(data)
    │   ├── 提取 choices[0].message.content
    │   ├── re.sub(r'<think\b[^>]*>.*?</think\s*>', '', text) → 过滤推理标签
    │   └── 提取 usage.total_tokens
    │
    ├── 4. 失败处理 → SmartRouter._handle_failure(provider, account, error)
    │   ├── 标记账户为不可用
    │   ├── 记录错误信息
    │   └── 自动故障转移到下一个 Provider/Account
    │
    └── 5. 记录使用 → ProviderAccount.record_usage(tokens)
        ├── 更新配额追踪
        └── 更新最后使用时间
```

---
# 6. 后端核心架构

## 架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                        NeuroSploit v3.2.4 后端架构                    │
├─────────────────────────────────────────────────────────────────────┤
│  API Layer (FastAPI) — 18个模块，151个端点                            │
├─────────────────────────────────────────────────────────────────────┤
│  Core Layer                                                         │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  Agent System (10 modules)                                   │    │
│  │  AgentBase → AutonomousAgent → AIPentestAgent               │    │
│  │  AgentOrchestrator → SpecialistAgents(5)                    │    │
│  │  VulnOrchestrator → VulnTypeAgent                           │    │
│  │  ResearcherAgent → AgentMemory/Tasks                        │    │
│  └──────────────────────────┬──────────────────────────────────┘    │
│  ┌──────────────────────────┼──────────────────────────────────┐    │
│  │  VulnEngine (16 modules) │  Smart Router (6 modules)        │    │
│  │  Engine→Registry→Testers │  Router→Registry→Account         │    │
│  │  →PayloadGenerator       │  →TokenExtractor→Refresher       │    │
│  │  →AIPrompts→SystemPrompts│  →CredentialStore               │    │
│  │  →PentestPlaybook        │                                   │    │
│  └──────────────────────────┼──────────────────────────────────┘    │
│  ┌──────────────────────────┼──────────────────────────────────┐    │
│  │  RAG Engine (9 modules)  │  Validation Pipeline (6 modules) │    │
│  │  Engine→VectorStore(3)   │  NegativeControl                 │    │
│  │  →ReasoningTemplates     │  ProofOfExecution                │    │
│  │  →ReasoningMemory        │  ConfidenceScorer                │    │
│  │  →FewShot                │  ValidationJudge                 │    │
│  │  →Processor/Chunker/Emb  │  AdaptiveLearner                 │    │
│  │  →Retriever              │  AccessControlLearner            │    │
│  └──────────────────────────┼──────────────────────────────────┘    │
│  ┌──────────────────────────┼──────────────────────────────────┐    │
│  │  Request Engine (5)      │  AI Reasoning (7)                │    │
│  │  RequestEngine           │  ReasoningEngine                 │    │
│  │  WAFDetector             │  TokenBudget                     │    │
│  │  StrategyAdapter         │  CVEHunter                       │    │
│  │  ChainEngine             │  DeepRecon/BannerAnalyzer        │    │
│  │  AuthManager             │  ParamAnalyzer/EndpointClass.    │    │
│  └──────────────────────────┼──────────────────────────────────┘    │
│  ┌──────────────────────────┼──────────────────────────────────┐    │
│  │  Report Engine (2)       │  Sandbox/CLI (4)                 │    │
│  │  ReportGenerator         │  ToolExecutor                    │    │
│  │  ReportEngine            │  CLIAgentRunner/OutputParser     │    │
│  │                          │  CLIInstructionsBuilder          │    │
│  └──────────────────────────┴──────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  Supporting Modules (19)                                     │    │
│  │  CheckpointManager  NotificationManager  KnowledgeProcessor │    │
│  │  TaskLibrary  ExecutionHistory  MethodologyLoader           │    │
│  │  PayloadMutator  POCGenerator  POCValidator                 │    │
│  │  ExploitGenerator  XSSValidator  XSSContextAnalyzer         │    │
│  │  SiteAnalyzer  RequestRepeater  PromptEngine(3)             │    │
│  │  AutonomousScanner  ReconIntegration                        │    │
│  │  AIPromptProcessor  ResponseVerifier                        │    │
│  └─────────────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────────────┤
│  Data Layer: SQLAlchemy(Async) + SQLite(aiosqlite) + File Storage   │
└─────────────────────────────────────────────────────────────────────┘
```

## 1. Agent 系统 (10 modules)

### agent_base.py — AgentResult + SpecialistAgent

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/agent_base.py` |
| 主要类 | `AgentResult`, `SpecialistAgent` |

**AgentResult** — 数据类，封装代理执行结果：

| 字段 | 类型 | 说明 |
|------|------|------|
| agent_name | str | 代理名称 |
| status | str | 执行状态 |
| findings | List | 发现结果列表 |
| data | Dict | 附加数据 |
| tasks_completed | int | 完成任务数 |
| tokens_used | int | 消耗Token数 |
| duration | float | 执行时长(秒) |
| error | Optional[str] | 错误信息 |
| handoff_to | Optional[str] | 转移目标代理 |
| handoff_context | Optional[Dict] | 转移上下文 |

**SpecialistAgent** — 专家代理基类：

| 方法签名 | 说明 |
|----------|------|
| `__init__(self, name, llm=None, memory=None, budget_allocation=0.0, budget=None)` | 初始化代理，配置名称、LLM客户端、记忆、预算分配 |
| `async run(self, context: Dict) -> AgentResult` | 子类必须重写的核心执行方法 |
| `async execute(self, context: Dict) -> AgentResult` | 包装器：自动计时 + 错误捕获 |
| `cancel(self)` | 发送信号停止代理 |
| `async handoff_to(self, target_agent, context) -> AgentResult` | 转移执行到另一个专家代理 |
| `as_tool(self) -> Dict` | 将代理暴露为LLM可调用的工具格式 |
| `async _llm_call(self, prompt, category, estimated_tokens) -> Optional[str]` | 带预算追踪的LLM调用，超预算自动拒绝 |

### autonomous_agent.py — AutonomousAgent (5900+行，核心代理)

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/autonomous_agent.py` |
| 主要类 | `AutonomousAgent`, `LLMClient`, `OperationMode` |

**OperationMode** — 7种操作模式枚举：

| 模式 | 说明 |
|------|------|
| RECON_ONLY | 仅侦察模式 |
| FULL_AUTO | 全自动模式 |
| PROMPT_ONLY | 仅提示词模式 |
| ANALYZE_ONLY | 仅分析模式 |
| AUTO_PENTEST | 自动渗透模式 |
| CLI_AGENT | CLI代理模式 |
| FULL_LLM_PENTEST | 完整LLM渗透模式 |

**LLMClient** — 多提供商LLM客户端，优先级：SmartRouter → Claude → OpenAI → Codex → Gemini → OpenRouter → Together → Fireworks → Ollama → LMStudio

**AutonomousAgent** 关键方法：

| 方法签名 | 说明 |
|----------|------|
| `__init__(self, target, mode, ...)` | 初始化30+子系统（VulnEngine、RAG、Validation、SmartRouter等） |
| `async run(self) -> Dict` | 主运行入口，根据mode分发到对应执行方法 |
| `skip_to_phase(self, target_phase) -> bool` | 跳转到指定执行阶段 |
| `pause() / resume() / cancel()` | 生命周期控制 |
| `async _run_recon_only(self)` | 侦察模式实现 |
| `async _run_full_auto(self)` | 全自动模式实现 |
| `async _run_auto_pentest(self)` | 自动渗透模式实现 |
| `async _run_cli_agent(self)` | CLI代理模式实现 |
| `async _run_full_llm_pentest(self)` | 完整LLM渗透模式实现 |
| `async _add_finding(self, finding)` | 添加发现（含验证管道） |
| `async _ai_deep_test(...)` | AI深度测试（迭代循环） |
| `async _stream_recon(self)` | 流式侦察 |
| `async _ai_analyze_recon(self)` | AI分析侦察数据 |

### ai_pentest_agent.py — AIPentestAgent

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/ai_pentest_agent.py` |
| 主要类 | `AIPentestAgent`, `AgentAction` |

**AgentAction** — 代理动作枚举：

| 动作 | 说明 |
|------|------|
| DISCOVER | 发现目标 |
| TEST | 测试漏洞 |
| EXPLOIT | 利用漏洞 |
| CHAIN | 链式攻击 |
| REPORT | 生成报告 |
| PIVOT | 横向移动 |

**AIPentestAgent** 关键方法：

| 方法签名 | 说明 |
|----------|------|
| `async run(self) -> Dict` | Think→Act→Observe→Adapt 循环 |
| `async _recon_phase(self)` | 侦察阶段 |
| `async _testing_phase(self)` | 测试阶段 |
| `async _exploitation_phase(self)` | 利用阶段 |
| `async _chaining_phase(self)` | 链式攻击阶段 |
| `async _llm_confirm_vulnerability(...)` | LLM确认漏洞真实性 |
| `async _generate_poc(self, finding) -> str` | LLM生成PoC |

### specialist_agents.py — 5个专家代理

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/specialist_agents.py` |
| 主要类 | `ReconAgent`, `ExploitAgent`, `ValidatorAgent`, `CVEHunterAgent`, `ReportAgent` |

| 代理 | 预算分配 | 职责 |
|------|----------|------|
| ReconAgent | 20% | 深度侦察：sitemap/robots/API枚举/指纹/Banner分析 |
| ExploitAgent | 35% | 分类端点、排序参数、自适应payload测试 |
| ValidatorAgent | 20% | 独立重测每个发现，确认可复现性 |
| CVEHunterAgent | 10% | 提取版本信息，搜索NVD+GitHub已知漏洞 |
| ReportAgent | 15% | AI增强描述、生成PoC、准备报告 |

### agent_orchestrator.py — AgentOrchestrator

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/agent_orchestrator.py` |
| 主要类 | `AgentOrchestrator` |

| 方法签名 | 说明 |
|----------|------|
| `_init_agents(self)` | 创建5个专家代理（含预算分配） |
| `async run(self, target, recon_data, initial_context) -> Dict` | 三阶段管道执行 |
| `async reason_about_handoff(self, current_agent, result) -> Optional[str]` | AI决定下一个代理 |

**三阶段管道**：

| 阶段 | 并行代理 | 说明 |
|------|----------|------|
| Phase 1 | Recon + CVEHunter | 并行执行侦察和CVE搜索 |
| Phase 2 | Exploit | 顺序执行漏洞利用 |
| Phase 3 | Validator + Reporter | 并行执行验证和报告 |

### vuln_orchestrator.py — VulnOrchestrator

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/vuln_orchestrator.py` |
| 主要类 | `VulnOrchestrator` |

**SEVERITY_GROUPS** — 严重度分组：

| 组别 | 漏洞类型 |
|------|----------|
| critical | sqli, command_injection, auth_bypass, ssrf, ssti 等 |
| high | xss, csrf, idor, bola, bfla 等 |

| 方法签名 | 说明 |
|----------|------|
| `async run(self, vuln_types, test_targets, prioritized_types) -> Dict` | 按优先级批次运行（critical→high→rest，批内并行，批间顺序） |
| `async _run_agent_gated(self, vuln_type, agent)` | 信号量门控并发执行 |

### 其他 Agent 模块

| 模块 | 文件 | 主要类 | 说明 |
|------|------|--------|------|
| vuln_type_agent.py | `backend/core/vuln_type_agent.py` | `VulnTypeAgent` | 单一漏洞类型测试的专家代理 |
| researcher_agent.py | `backend/core/researcher_agent.py` | `ResearcherAgent` | AI驱动的0日漏洞研究员，使用Kali沙箱 |
| agent_memory.py | `backend/core/agent_memory.py` | `AgentMemory` | 测试组合、基线响应、端点指纹和发现存储 |
| agent_tasks.py | `backend/core/agent_tasks.py` | `AgentTask`, `AgentTaskManager` | 优先队列和并发执行管理 |

## 2. VulnEngine 系统 (16 modules)

### engine.py — DynamicVulnerabilityEngine

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/vuln_engine/engine.py` |
| 主要类 | `DynamicVulnerabilityEngine` |

| 方法签名 | 说明 |
|----------|------|
| `async test_endpoint(self, endpoint, vuln_types, context, progress_callback) -> List[TestResult]` | 测试端点的多种漏洞类型 |
| `async _execute_test(self, endpoint, vuln_type, payload, tester, context) -> TestResult` | 执行单个测试 |
| `async _deep_test(self, endpoint, vuln_type, initial_result, tester, context) -> List[TestResult]` | 深度测试（初始发现后的迭代测试） |
| `async create_vulnerability_record(self, scan_id, endpoint, result) -> Vulnerability` | 创建漏洞记录 |

### registry.py — VulnerabilityRegistry

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/vuln_engine/registry.py` |
| 主要类 | `VulnerabilityRegistry` |

| 数据 | 说明 |
|------|------|
| VULNERABILITY_INFO | 100+条目（title/severity/cwe_id/description/impact/remediation） |
| TESTER_CLASSES | 100+映射（vuln_type → tester class） |

| 方法签名 | 说明 |
|----------|------|
| `get_tester(vuln_type)` | 获取漏洞类型对应的测试器类 |
| `get_severity(vuln_type)` | 获取严重级别 |
| `get_cwe_id(vuln_type)` | 获取CWE ID |
| `get_title(vuln_type)` | 获取漏洞标题 |
| `get_description(vuln_type)` | 获取漏洞描述 |
| `get_impact(vuln_type)` | 获取影响说明 |
| `get_remediation(vuln_type)` | 获取修复建议 |

### payload_generator.py — PayloadGenerator

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/vuln_engine/payload_generator.py` |
| 主要类 | `PayloadGenerator` |

**60+ payload分类**：xss_reflected/stored/dom, sqli_error/union/blind/time, command_injection, ssti, nosql, lfi, rfi, path_traversal, xxe, ssrf, open_redirect, cors, jwt, auth_bypass, idor, ldap, xpath, graphql, crlf, header_injection, email_injection, el_injection, log_injection, html_injection, csv_injection, orm_injection, blind_xss, mutation_xss, arbitrary_file_read/delete, zip_slip, weak_password, default_credentials, two_factor_bypass, oauth_misconfig, bfla, mass_assignment, forced_browsing, dom_clobbering, postmessage, websocket_hijack, prototype_pollution, css_injection, tabnabbing, directory_listing, debug_mode, exposed_admin/api_docs, insecure_cookie, http_smuggling, cache_poisoning, race_condition, business_logic, rate_limit_bypass, parameter_pollution, type_juggling, insecure_deserialization, subdomain_takeover, host_header, timing_attack, improper_error_handling, sensitive_data_exposure, information_disclosure, api_key_exposure, source_code_disclosure, backup_file_exposure, version_disclosure, weak_encryption/hashing/random, cleartext_transmission, vulnerable_dependency, outdated_component, insecure_cdn, container_escape, s3_bucket_misconfig, cloud_metadata_exposure, serverless_misconfig, graphql_introspection/dos, rest_api_versioning, soap_injection, api_rate_limiting, excessive_data_exposure

| 方法签名 | 说明 |
|----------|------|
| `get_payloads(vuln_type)` | 获取基础payload列表 |
| `get_exploitation_payloads(vuln_type)` | 获取利用payload |
| `get_context_payloads(vuln_type, context)` | 获取上下文相关payload |
| `get_filter_bypass_payloads(vuln_type)` | 获取过滤器绕过payload |
| `_add_waf_bypasses(payloads)` | 为payload添加WAF绕过变体 |

### system_prompts.py — 16个反幻觉提示

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/vuln_engine/system_prompts.py` |

**16个反幻觉系统提示**：

| 提示名称 | 说明 |
|----------|------|
| PROMPT_ANTI_HALLUCINATION | 反幻觉核心提示 |
| PROMPT_ANTI_SCANNER | 反扫描器模式提示 |
| PROMPT_NEGATIVE_CONTROLS | 负面控制提示 |
| PROMPT_THINK_LIKE_PENTESTER | 渗透测试思维提示 |
| PROMPT_PROOF_OF_EXECUTION | 执行证明提示 |
| PROMPT_FRONTEND_BACKEND_CORRELATION | 前后端关联提示 |
| PROMPT_MULTI_PHASE_TESTS | 多阶段测试提示 |
| PROMPT_FINAL_JUDGMENT | 最终判断提示 |
| PROMPT_CONFIDENCE_SCORE | 置信度评分提示 |
| PROMPT_ANTI_SEVERITY_INFLATION | 反严重性膨胀提示 |
| PROMPT_OPERATIONAL_HUMILITY | 操作谦逊提示 |
| PROMPT_ACCESS_CONTROL_INTELLIGENCE | 访问控制智能提示 |
| PROMPT_ITERATIVE_TESTING | 迭代测试提示 |
| PROMPT_OFFENSIVE_MINDSET | 攻击性思维提示 |
| PROMPT_ARCHITECTURE_ANALYSIS | 架构分析提示 |
| PROMPT_METHOD_VARIATION | 方法变异提示 |

**其他数据**：
- VULN_TYPE_PROOF_REQUIREMENTS: 100条漏洞类型证明要求
- CONTEXT_PROMPTS: 8个上下文（testing/verification/confirmation/strategy/reporting/interpretation/poc_generation/deep_testing/playbook）

### ai_prompts.py — 100+漏洞AI提示模板

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/vuln_engine/ai_prompts.py` |

**核心数据**：VULN_AI_PROMPTS, POC_TEMPLATES

| 函数签名 | 说明 |
|----------|------|
| `get_prompt(vuln_type)` | 获取漏洞类型AI提示 |
| `build_testing_prompt(vuln_type, endpoint, context)` | 构建测试提示 |
| `get_verification_prompt(vuln_type, finding)` | 获取验证提示 |
| `get_poc_prompt(vuln_type, finding)` | 获取PoC生成提示 |
| `get_deep_test_plan_prompt(vuln_type, endpoint, initial_results)` | 获取深度测试计划提示 |
| `get_deep_test_analysis_prompt(vuln_type, results)` | 获取深度测试分析提示 |
| `get_master_plan_prompt(target_info, vuln_types)` | 获取主计划提示 |
| `get_junior_ai_test_prompt(vuln_type, endpoint)` | 获取初级AI测试提示 |
| `get_tool_analysis_prompt(tool_name, output)` | 获取工具分析提示 |
| `get_recon_analysis_prompt(recon_data)` | 获取侦察分析提示 |
| `get_full_llm_pentest_system_prompt()` | 获取完整LLM渗透系统提示 |
| `get_full_llm_pentest_round_prompt(round_num, findings)` | 获取完整LLM渗透轮次提示 |
| `get_full_llm_pentest_report_prompt(findings)` | 获取完整LLM渗透报告提示 |

### pentest_playbook.py — 100种漏洞完整测试方法论

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/vuln_engine/pentest_playbook.py` |

**PENTEST_PLAYBOOK** — 每种漏洞包含：category/title/overview/threat_model/discovery/test_phases/bypass_strategies/verification_checklist/chain_attacks/anti_false_positive

| 函数签名 | 说明 |
|----------|------|
| `get_playbook_entry(vuln_type)` | 获取漏洞测试方法论条目 |
| `get_testing_prompts(vuln_type)` | 获取测试提示 |
| `get_bypass_strategies(vuln_type)` | 获取绕过策略 |
| `get_verification_checklist(vuln_type)` | 获取验证清单 |
| `get_chain_attacks(vuln_type)` | 获取链式攻击 |
| `get_anti_fp_rules(vuln_type)` | 获取反误报规则 |
| `get_all_vuln_types()` | 获取所有漏洞类型 |
| `get_playbook_summary()` | 获取方法论摘要 |
| `build_agent_testing_prompt(vuln_type, endpoint, context)` | 构建代理测试提示 |

### testers/ — 12个测试器文件，70+测试器类

#### base_tester.py — BaseTester

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/vuln_engine/testers/base_tester.py` |
| 主要类 | `BaseTester` |
| 说明 | 基类，提供 `build_request` 和 `analyze_response` 接口 |

#### injection.py — 10个注入测试器

| 测试器类 | 说明 |
|----------|------|
| XSSReflectedTester | 反射型XSS测试 |
| XSSStoredTester | 存储型XSS测试 |
| XSSDomTester | DOM型XSS测试 |
| SQLiErrorTester | 错误型SQL注入测试 |
| SQLiUnionTester | 联合查询SQL注入测试 |
| SQLiBlindTester | 盲注SQL注入测试 |
| SQLiTimeTester | 时间盲注SQL注入测试 |
| CommandInjectionTester | 命令注入测试 |
| SSTITester | 服务端模板注入测试 |
| NoSQLInjectionTester | NoSQL注入测试 |

#### auth.py — 7个认证测试器

| 测试器类 | 说明 |
|----------|------|
| AuthBypassTester | 认证绕过测试 |
| JWTManipulationTester | JWT操纵测试 |
| SessionFixationTester | 会话固定测试 |
| WeakPasswordTester | 弱密码测试 |
| DefaultCredentialsTester | 默认凭据测试 |
| TwoFactorBypassTester | 双因素绕过测试 |
| OauthMisconfigTester | OAuth错误配置测试 |

#### authorization.py — 6个授权测试器

| 测试器类 | 说明 |
|----------|------|
| IDORTester | 越权访问测试 |
| BOLATester | BOLA越权测试 |
| PrivilegeEscalationTester | 权限提升测试 |
| BflaTester | BFLA越权测试 |
| MassAssignmentTester | 批量赋值测试 |
| ForcedBrowsingTester | 强制浏览测试 |

#### client_side.py — 9个客户端测试器

| 测试器类 | 说明 |
|----------|------|
| CORSTester | CORS错误配置测试 |
| ClickjackingTester | 点击劫持测试 |
| OpenRedirectTester | 开放重定向测试 |
| DomClobberingTester | DOM篡改测试 |
| PostMessageVulnTester | PostMessage漏洞测试 |
| WebsocketHijackTester | WebSocket劫持测试 |
| PrototypePollutionTester | 原型链污染测试 |
| CssInjectionTester | CSS注入测试 |
| TabnabbingTester | 标签劫持测试 |

#### advanced_injection.py — 11个高级注入测试器

| 测试器类 | 说明 |
|----------|------|
| LdapInjectionTester | LDAP注入测试 |
| XpathInjectionTester | XPath注入测试 |
| GraphqlInjectionTester | GraphQL注入测试 |
| CrlfInjectionTester | CRLF注入测试 |
| HeaderInjectionTester | HTTP头注入测试 |
| EmailInjectionTester | 邮件注入测试 |
| ELInjectionTester | EL表达式注入测试 |
| LogInjectionTester | 日志注入测试 |
| HtmlInjectionTester | HTML注入测试 |
| CsvInjectionTester | CSV注入测试 |
| OrmInjectionTester | ORM注入测试 |

#### data_exposure.py — 6个数据暴露测试器

| 测试器类 | 说明 |
|----------|------|
| SensitiveDataExposureTester | 敏感数据暴露测试 |
| InformationDisclosureTester | 信息泄露测试 |
| ApiKeyExposureTester | API Key暴露测试 |
| SourceCodeDisclosureTester | 源码泄露测试 |
| BackupFileExposureTester | 备份文件暴露测试 |
| VersionDisclosureTester | 版本信息泄露测试 |

#### file_access.py — 8个文件访问测试器

| 测试器类 | 说明 |
|----------|------|
| LFITester | 本地文件包含测试 |
| RFITester | 远程文件包含测试 |
| PathTraversalTester | 路径遍历测试 |
| XXETester | XML外部实体注入测试 |
| FileUploadTester | 文件上传测试 |
| ArbitraryFileReadTester | 任意文件读取测试 |
| ArbitraryFileDeleteTester | 任意文件删除测试 |
| ZipSlipTester | Zip Slip测试 |

#### logic.py — 9个逻辑漏洞测试器

| 测试器类 | 说明 |
|----------|------|
| RaceConditionTester | 竞态条件测试 |
| BusinessLogicTester | 业务逻辑测试 |
| RateLimitBypassTester | 速率限制绕过测试 |
| ParameterPollutionTester | 参数污染测试 |
| TypeJugglingTester | 类型混淆测试 |
| TimingAttackTester | 时序攻击测试 |
| HostHeaderInjectionTester | Host头注入测试 |
| HttpSmugglingTester | HTTP走私测试 |
| CachePoisoningTester | 缓存投毒测试 |

#### request_forgery.py — 4个请求伪造测试器

| 测试器类 | 说明 |
|----------|------|
| SSRFTester | 服务端请求伪造测试 |
| CSRFTester | 跨站请求伪造测试 |
| GraphqlIntrospectionTester | GraphQL内省测试 |
| GraphqlDosTester | GraphQL DoS测试 |

#### cloud_supply.py — 6个云/供应链测试器

| 测试器类 | 说明 |
|----------|------|
| S3BucketMisconfigTester | S3存储桶错误配置测试 |
| CloudMetadataExposureTester | 云元数据暴露测试 |
| SubdomainTakeoverTester | 子域接管测试 |
| VulnerableDependencyTester | 易受攻击依赖测试 |
| ContainerEscapeTester | 容器逃逸测试 |
| ServerlessMisconfigTester | 无服务器错误配置测试 |

#### infrastructure.py — 10个基础设施测试器

| 测试器类 | 说明 |
|----------|------|
| SecurityHeadersTester | 安全头测试 |
| SSLTester | SSL/TLS测试 |
| HTTPMethodsTester | HTTP方法测试 |
| DirectoryListingTester | 目录列表测试 |
| DebugModeTester | 调试模式测试 |
| ExposedAdminPanelTester | 管理面板暴露测试 |
| ExposedApiDocsTester | API文档暴露测试 |
| InsecureCookieFlagsTester | 不安全Cookie标志测试 |
| HttpSmugglingTester | HTTP走私测试 |
| CachePoisoningTester | 缓存投毒测试 |

## 3. Smart Router 系统 (6 modules)

### router.py — SmartRouter

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/smart_router/router.py` |
| 主要类 | `SmartRouter` |

| 方法签名 | 说明 |
|----------|------|
| `async route(self, prompt, system, max_tokens, model, temperature, preferred_provider) -> Tuple[str, int]` | 主路由入口，返回(响应文本, token数) |
| `async _select_provider(self, preferred_provider) -> Tuple[Provider, ProviderAccount]` | 按Tier优先级选择提供商和账户 |
| `async _call_provider(self, provider, account, prompt, system, max_tokens, model, temperature) -> Tuple[str, int]` | 调用指定提供商API |
| `_parse_openai_response(self, data) -> Tuple[str, int]` | 解析OpenAI格式响应（含`<think\>`标签过滤） |
| `async test_account(self, provider, account) -> Tuple[bool, str]` | 测试账户连接 |

### provider_registry.py — ProviderRegistry

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/smart_router/provider_registry.py` |
| 主要类 | `ProviderRegistry` |

管理提供商配置、账户、CLI令牌检测。维护所有已注册的LLM提供商及其账户信息，支持Tier分级排序。

### provider_account.py — ProviderAccount

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/smart_router/provider_account.py` |
| 主要类 | `ProviderAccount` |

API Key管理、配额追踪、过期检测。每个账户维护独立的使用统计和可用性状态。

### credential_store.py — CredentialStore

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/smart_router/credential_store.py` |
| 主要类 | `CredentialStore` |

安全存储和管理API Key，提供加密存储和检索接口。

### token_extractor.py — TokenExtractor

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/smart_router/token_extractor.py` |
| 主要类 | `TokenExtractor` |

支持8种CLI工具令牌检测：

| CLI工具 | 提取来源 |
|----------|----------|
| claude_code | macOS Keychain / JSON配置文件 |
| codex_cli | JSON配置文件 |
| gemini_cli | JSON配置文件 |
| cursor | SQLite数据库 |
| copilot | JSON配置文件 |
| iflow | JSON配置文件 |
| qwen_code | JSON配置文件 |
| kiro | JSON配置文件 |

| 方法签名 | 说明 |
|----------|------|
| `detect(self, provider_id) -> Optional[ExtractedToken]` | 检测单个提供商令牌 |
| `detect_all(self) -> List[ExtractedToken]` | 检测所有提供商令牌 |

### token_refresher.py — TokenRefresher

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/smart_router/token_refresher.py` |
| 主要类 | `TokenRefresher` |

| 方法签名 | 说明 |
|----------|------|
| `async start(self)` | 启动后台刷新循环 |
| `async _refresh_loop(self)` | 后台刷新主循环 |
| `async _refresh_google(self, account_id, refresh_token) -> bool` | 刷新Google OAuth令牌 |
| `async _refresh_anthropic(self, account_id, refresh_token) -> bool` | 刷新Anthropic令牌 |
| `async _refresh_openai(self, account_id, refresh_token) -> bool` | 刷新OpenAI令牌 |

## 4. RAG 系统 (9 modules)

### engine.py — RAGEngine

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/rag/engine.py` |
| 主要类 | `RAGEngine` |

**5个集合**：bug_bounty, vuln_methods, custom, reasoning, attack_patterns

| 方法签名 | 说明 |
|----------|------|
| `async index_all(self, force=False) -> Dict[str, int]` | 索引所有文档，返回各集合文档数 |
| `async query(self, query_text, collections, top_k, vuln_type, technology, chunk_type) -> RAGContext` | 查询知识库 |
| `get_testing_context(vuln_type, endpoint)` | 获取测试上下文 |
| `get_verification_context(vuln_type, finding)` | 获取验证上下文 |
| `get_strategy_context(vuln_type, technology)` | 获取策略上下文 |

### vectorstore.py — 3种后端

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/rag/vectorstore.py` |

| 类 | 说明 | 依赖 |
|----|------|------|
| BaseVectorStore(ABC) | 抽象基类：add, query, collection_exists, delete_collection, collection_count | - |
| BM25VectorStore | 零依赖，默认方案 | 无 |
| TFIDFVectorStore | TF-IDF向量存储 | scikit-learn + numpy |
| ChromaVectorStore | ChromaDB向量存储 | chromadb + sentence-transformers |

工厂函数：`create_vectorstore(persist_dir, backend)` — 根据配置创建对应后端实例

### reasoning_templates.py — 40+漏洞推理模板

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/rag/reasoning_templates.py` |

**REASONING_TEMPLATES** — 每个模板包含：reasoning_chain, decision_criteria, proof_requirements, common_pitfalls

| 函数签名 | 说明 |
|----------|------|
| `get_reasoning_template(vuln_type)` | 获取推理模板 |
| `format_reasoning_prompt(vuln_type, context)` | 格式化推理提示 |
| `get_available_types()` | 获取可用漏洞类型列表 |

### reasoning_memory.py — 跨扫描持久推理记忆

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/rag/reasoning_memory.py` |

**3种数据类**：

| 数据类 | 说明 |
|--------|------|
| ReasoningTrace | 推理轨迹记录 |
| FailureRecord | 失败记录 |
| StrategyRecord | 策略记录 |

**ReasoningMemory** 方法：

| 方法签名 | 说明 |
|----------|------|
| `record_success(vuln_type, strategy, context)` | 记录成功策略 |
| `record_failure(vuln_type, approach, reason)` | 记录失败方法 |
| `record_strategy(vuln_type, strategy, effectiveness)` | 记录策略有效性 |
| `get_relevant_traces(vuln_type, context)` | 获取相关推理轨迹 |
| `get_failure_patterns(vuln_type)` | 获取失败模式 |
| `get_context_for_testing(vuln_type, endpoint)` | 获取测试上下文 |

**容量限制**：MAX_TRACES=500, MAX_FAILURES=200, MAX_STRATEGIES=100

### few_shot.py — 少样本学习

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/rag/few_shot.py` |

**FewShotExample** 字段：vuln_type, technology, scenario, reasoning_chain, outcome, payload, proof, score

**FewShotSelector** 方法：

| 方法签名 | 说明 |
|----------|------|
| `get_testing_examples(vuln_type, technology)` | 获取测试示例 |
| `get_verification_examples(vuln_type, finding)` | 获取验证示例 |
| `get_strategy_examples(vuln_type, technology)` | 获取策略示例 |

支持RAG检索 + 策划示例库双模式

### 其他 RAG 模块

| 模块 | 文件 | 说明 |
|------|------|------|
| processor.py | `backend/core/rag/processor.py` | 文档预处理 |
| chunker.py | `backend/core/rag/chunker.py` | 文档分块 |
| embedder.py | `backend/core/rag/embedder.py` | 文本嵌入 |
| retriever.py | `backend/core/rag/retriever.py` | 检索器 |

## 5. 验证管线 (6 modules)

### negative_control.py — NegativeControl

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/validation/negative_control.py` |
| 主要类 | `NegativeControl` |

对已知安全端点执行相同测试，确保不会产生误报。如果安全端点也报告漏洞，则标记为假阳性。

### proof_of_execution.py — ProofOfExecution

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/validation/proof_of_execution.py` |
| 主要类 | `ProofOfExecution` |

要求每个漏洞发现提供可执行的证明：完整的HTTP请求/响应对、可复现的PoC步骤、独特的响应特征。

### confidence_scorer.py — ConfidenceScorer

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/validation/confidence_scorer.py` |
| 主要类 | `ConfidenceScorer` |

多维度置信度评分：响应匹配度、payload效果、基线差异、独立验证一致性。输出0-100的置信度分数和分项明细。

### validation_judge.py — ValidationJudge

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/validation/validation_judge.py` |
| 主要类 | `ValidationJudge` |

LLM驱动的最终判断：综合所有验证信号，AI判断漏洞真实性。使用独立LLM调用避免确认偏差。

### adaptive_learner.py — AdaptiveLearner

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/validation/adaptive_learner.py` |
| 主要类 | `AdaptiveLearner` |

从用户反馈中学习：记录真假阳性判断，调整置信度阈值，优化未来验证策略。

### access_control_learner.py — AccessControlLearner

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/validation/access_control_learner.py` |
| 主要类 | `AccessControlLearner` |

访问控制专用学习器：学习认证/授权模式，识别角色权限边界，优化IDOR/BOLA检测策略。

## 6. Request Engine (5 modules)

| 模块 | 文件 | 主要类 | 说明 |
|------|------|--------|------|
| request_engine.py | `backend/core/request_engine.py` | `RequestEngine` | 统一HTTP请求引擎，支持重试、限速、代理 |
| waf_detector.py | `backend/core/waf_detector.py` | `WAFDetector` | WAF检测和绕过策略选择 |
| strategy_adapter.py | `backend/core/strategy_adapter.py` | `StrategyAdapter` | 根据目标特征自适应调整请求策略 |
| chain_engine.py | `backend/core/chain_engine.py` | `ChainEngine` | 漏洞链式利用引擎 |
| auth_manager.py | `backend/core/auth_manager.py` | `AuthManager` | 认证管理（Cookie/Bearer/Basic/Header） |

## 7. AI Reasoning (7 modules)

| 模块 | 文件 | 主要类 | 说明 |
|------|------|--------|------|
| reasoning_engine.py | `backend/core/reasoning_engine.py` | `ReasoningEngine` | AI推理引擎，协调推理流程 |
| token_budget.py | `backend/core/token_budget.py` | `TokenBudget` | Token预算管理和分配 |
| cve_hunter.py | `backend/core/cve_hunter.py` | `CVEHunter` | CVE搜索（NVD + GitHub Advisory） |
| deep_recon.py | `backend/core/deep_recon.py` | `DeepRecon` | 深度侦察分析 |
| banner_analyzer.py | `backend/core/banner_analyzer.py` | `BannerAnalyzer` | Banner指纹分析 |
| param_analyzer.py | `backend/core/param_analyzer.py` | `ParamAnalyzer` | 参数分析和分类 |
| endpoint_classifier.py | `backend/core/endpoint_classifier.py` | `EndpointClassifier` | 端点分类和优先级排序 |

## 8. Report Engine (2 modules)

| 模块 | 文件 | 主要类 | 说明 |
|------|------|--------|------|
| report_generator.py | `backend/core/report_generator.py` | `ReportGenerator` | 报告生成器（HTML/PDF/JSON/ZIP） |
| report_engine.py | `backend/core/report_engine.py` | `ReportEngine` | 报告引擎，AI增强报告内容 |

## 9. Sandbox/CLI (4 modules)

| 模块 | 文件 | 主要类 | 说明 |
|------|------|--------|------|
| tool_executor.py | `backend/core/tool_executor.py` | `ToolExecutor` | 安全工具执行器（Kali沙箱内） |
| cli_agent_runner.py | `backend/core/cli_agent_runner.py` | `CLIAgentRunner` | CLI代理运行器 |
| output_parser.py | `backend/core/output_parser.py` | `OutputParser` | 工具输出解析器 |
| cli_instructions_builder.py | `backend/core/cli_instructions_builder.py` | `CLIInstructionsBuilder` | CLI指令构建器 |

## 10. Supporting Modules (19 modules)

### 基础支撑模块

| 模块 | 文件 | 主要类 | 说明 |
|------|------|--------|------|
| checkpoint_manager.py | `backend/core/checkpoint_manager.py` | `CheckpointManager` | 扫描检查点管理，支持断点续扫 |
| notification_manager.py | `backend/core/notification_manager.py` | `NotificationManager` | 多渠道通知（Discord/Telegram/WhatsApp） |
| knowledge_processor.py | `backend/core/knowledge_processor.py` | `KnowledgeProcessor` | 知识文档处理和索引 |
| task_library.py | `backend/core/task_library.py` | `TaskLibrary` | 任务库管理 |
| execution_history.py | `backend/core/execution_history.py` | `ExecutionHistory` | 执行历史记录 |
| methodology_loader.py | `backend/core/methodology_loader.py` | `MethodologyLoader` | 外部方法论文件加载 |

### Payload和PoC模块

| 模块 | 文件 | 主要类 | 说明 |
|------|------|--------|------|
| payload_mutator.py | `backend/core/payload_mutator.py` | `PayloadMutator` | Payload变异和编码 |
| poc_generator.py | `backend/core/poc_generator.py` | `POCGenerator` | PoC代码生成 |
| poc_validator.py | `backend/core/poc_validator.py` | `POCValidator` | PoC验证 |
| exploit_generator.py | `backend/core/exploit_generator.py` | `ExploitGenerator` | 利用代码生成 |

### XSS专项模块

| 模块 | 文件 | 主要类 | 说明 |
|------|------|--------|------|
| xss_validator.py | `backend/core/xss_validator.py` | `XSSValidator` | XSS专用验证器 |
| xss_context_analyzer.py | `backend/core/xss_context_analyzer.py` | `XSSContextAnalyzer` | XSS上下文分析器 |

### 请求和分析模块

| 模块 | 文件 | 主要类 | 说明 |
|------|------|--------|------|
| site_analyzer.py | `backend/core/site_analyzer.py` | `SiteAnalyzer` | 站点分析器 |
| request_repeater.py | `backend/core/request_repeater.py` | `RequestRepeater` | 请求重放器 |
| prompt_engine.py | `backend/core/prompt_engine.py` | `PromptEngine` | 提示词引擎（3个子模块） |

### 新增自主模块

#### autonomous_scanner.py — AutonomousScanner

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/autonomous_scanner.py` |
| 主要类 | `AutonomousScanner` |

独立自主扫描器，支持目录发现、参数发现、XSS/SQLi/LFI/CMDi/SSTI/Open Redirect测试。

| 方法签名 | 说明 |
|----------|------|
| `run_autonomous_scan(target, ...)` | 运行自主扫描 |
| `_probe_target(target)` | 探测目标 |
| `_discover_directories(target)` | 目录发现 |
| `_crawl_site(target)` | 站点爬取 |
| `_test_xss(target, endpoint)` | XSS测试 |
| `_test_sqli(target, endpoint)` | SQLi测试 |
| `_test_lfi(target, endpoint)` | LFI测试 |
| `_test_cmdi(target, endpoint)` | 命令注入测试 |
| `_test_ssti(target, endpoint)` | SSTI测试 |
| `_test_open_redirect(target, endpoint)` | 开放重定向测试 |

#### recon_integration.py — ReconIntegration

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/recon_integration.py` |
| 主要类 | `ReconIntegration` |

多阶段侦察集成：DNS解析→HTTP探测→路径检查→子域枚举→URL收集→端口扫描→技术检测→爬取→参数发现→JS分析→目录模糊→Nuclei扫描→截图

| 方法签名 | 说明 |
|----------|------|
| `run_full_recon(target, depth="medium")` | 运行完整侦察 |

#### ai_prompt_processor.py — AIPromptProcessor + AIVulnerabilityAnalyzer

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/ai_prompt_processor.py` |
| 主要类 | `AIPromptProcessor`, `AIVulnerabilityAnalyzer` |

| 方法签名 | 说明 |
|----------|------|
| `AIPromptProcessor.process_prompt(prompt) -> TestingPlan` | 处理提示词，返回测试计划（vuln_types, endpoints, parameters, custom_payloads, priority_order） |
| `AIVulnerabilityAnalyzer.analyze_finding(finding)` | AI分析漏洞发现 |

#### response_verifier.py — ResponseVerifier

| 项目 | 内容 |
|------|------|
| 文件路径 | `backend/core/response_verifier.py` |
| 主要类 | `ResponseVerifier` |

多信号验证机制：
- 4个独立信号：tester模式匹配 / 基线差异 / payload效果 / 新错误模式
- 2+信号 = 确认，1信号+0.8置信度 = 确认，0信号 = 拒绝

| 方法签名 | 说明 |
|----------|------|
| `check_target_health(target)` | 检查目标健康状态 |
| `compute_response_diff(baseline, response)` | 计算响应差异 |
| `_check_payload_effect(payload, response)` | 检查payload效果 |
| `multi_signal_verify(finding, signals) -> bool` | 多信号综合验证 |

---

# 7. 数据模型详解

## 数据库配置

| 配置项 | 值 |
|--------|-----|
| ORM | SQLAlchemy (Async) with DeclarativeBase |
| 默认数据库 | SQLite (aiosqlite) at `data/neurosploit.db` |
| 会话管理 | async_sessionmaker with expire_on_commit=False |
| 迁移策略 | init_db → create_all + _run_migrations (增量添加列和表) |

## 模型1: Scan (scans)

| 列名 | 类型 | 约束 | 默认值 |
|------|------|------|--------|
| id | String(36) | primary_key | uuid4() |
| name | String(255) | nullable | - |
| status | String(50) | - | "pending" |
| scan_type | String(50) | - | "full" |
| recon_enabled | Boolean | - | True |
| progress | Integer | - | 0 |
| current_phase | String(50) | nullable | - |
| config | JSON | - | {} |
| custom_prompt | Text | nullable | - |
| prompt_id | String(36) | nullable | - |
| auth_type | String(50) | nullable | - |
| auth_credentials | JSON | nullable | - |
| custom_headers | JSON | nullable | - |
| created_at | DateTime | - | utcnow |
| started_at | DateTime | nullable | - |
| completed_at | DateTime | nullable | - |
| duration | Integer | nullable | - |
| error_message | Text | nullable | - |
| total_endpoints | Integer | - | 0 |
| total_vulnerabilities | Integer | - | 0 |
| critical_count | Integer | - | 0 |
| high_count | Integer | - | 0 |
| medium_count | Integer | - | 0 |
| low_count | Integer | - | 0 |
| info_count | Integer | - | 0 |

**关系**：targets(1:N Target), endpoints(1:N Endpoint), vulnerabilities(1:N Vulnerability), reports(1:N Report), agent_tasks(1:N AgentTask) — 全部 cascade=delete-orphan

## 模型2: Target (targets)

| 列名 | 类型 | 约束 | 默认值 |
|------|------|------|--------|
| id | String(36) | primary_key | uuid4() |
| scan_id | String(36) | ForeignKey("scans.id", ondelete="CASCADE") | - |
| url | String(2048) | - | - |
| hostname | String(255) | nullable | - |
| port | Integer | nullable | - |
| protocol | String(10) | nullable | - |
| path | String(2048) | nullable | - |
| status | String(50) | - | "pending" |
| created_at | DateTime | - | utcnow |

## 模型3: Endpoint (endpoints)

| 列名 | 类型 | 约束 | 默认值 |
|------|------|------|--------|
| id | String(36) | primary_key | uuid4() |
| scan_id | String(36) | ForeignKey("scans.id", ondelete="CASCADE") | - |
| target_id | String(36) | ForeignKey("targets.id", ondelete="SET NULL"), nullable | - |
| url | Text | - | - |
| method | String(10) | - | "GET" |
| path | Text | nullable | - |
| parameters | JSON | - | [] |
| headers | JSON | - | {} |
| response_status | Integer | nullable | - |
| content_type | String(100) | nullable | - |
| content_length | Integer | nullable | - |
| technologies | JSON | - | [] |
| interesting | Boolean | - | False |
| discovered_at | DateTime | - | utcnow |

## 模型4: Vulnerability (vulnerabilities)

| 列名 | 类型 | 约束 | 默认值 |
|------|------|------|--------|
| id | String(36) | primary_key | uuid4() |
| scan_id | String(36) | ForeignKey("scans.id", ondelete="CASCADE") | - |
| test_id | String(36) | ForeignKey("vulnerability_tests.id", ondelete="SET NULL"), nullable | - |
| title | String(500) | - | - |
| vulnerability_type | String(100) | - | - |
| severity | String(20) | - | - |
| cvss_score | Float | nullable | - |
| cvss_vector | String(100) | nullable | - |
| cwe_id | String(50) | nullable | - |
| description | Text | nullable | - |
| affected_endpoint | Text | nullable | - |
| poc_request | Text | nullable | - |
| poc_response | Text | nullable | - |
| poc_payload | Text | nullable | - |
| poc_parameter | String(500) | nullable | - |
| poc_evidence | Text | nullable | - |
| impact | Text | nullable | - |
| remediation | Text | nullable | - |
| references | JSON | - | [] |
| ai_analysis | Text | nullable | - |
| poc_code | Text | nullable | - |
| screenshots | JSON | - | [] |
| url | Text | nullable | - |
| parameter | String(500) | nullable | - |
| confidence_score | Integer | nullable | - |
| confidence_breakdown | JSON | - | {} |
| proof_of_execution | Text | nullable | - |
| validation_status | String(20) | - | "ai_confirmed" |
| ai_rejection_reason | Text | nullable | - |
| created_at | DateTime | - | utcnow |

## 模型5: VulnerabilityTest (vulnerability_tests)

| 列名 | 类型 | 约束 | 默认值 |
|------|------|------|--------|
| id | String(36) | primary_key | uuid4() |
| scan_id | String(36) | ForeignKey("scans.id", ondelete="CASCADE") | - |
| endpoint_id | String(36) | ForeignKey("endpoints.id", ondelete="SET NULL"), nullable | - |
| vulnerability_type | String(100) | - | - |
| payload | Text | nullable | - |
| request_data | JSON | - | {} |
| response_data | JSON | - | {} |
| is_vulnerable | Boolean | - | False |
| confidence | Float | nullable | - |
| evidence | Text | nullable | - |
| tested_at | DateTime | - | utcnow |

**索引**：idx_vulnerability_tests_scan_id ON scan_id

## 模型6: Report (reports)

| 列名 | 类型 | 约束 | 默认值 |
|------|------|------|--------|
| id | String(36) | primary_key | uuid4() |
| scan_id | String(36) | ForeignKey("scans.id", ondelete="CASCADE") | - |
| title | String(255) | nullable | - |
| format | String(20) | - | "html" |
| file_path | Text | nullable | - |
| executive_summary | Text | nullable | - |
| auto_generated | Boolean | - | False |
| is_partial | Boolean | - | False |
| generated_at | DateTime | - | utcnow |

## 模型7: AgentTask (agent_tasks)

| 列名 | 类型 | 约束 | 默认值 |
|------|------|------|--------|
| id | String(36) | primary_key | uuid4() |
| scan_id | String(36) | ForeignKey("scans.id", ondelete="CASCADE") | - |
| task_type | String(50) | - | - |
| task_name | String(255) | - | - |
| description | Text | nullable | - |
| tool_name | String(100) | nullable | - |
| tool_category | String(50) | nullable | - |
| status | String(20) | - | "pending" |
| started_at | DateTime | nullable | - |
| completed_at | DateTime | nullable | - |
| duration_ms | Integer | nullable | - |
| items_processed | Integer | - | 0 |
| items_found | Integer | - | 0 |
| result_summary | Text | nullable | - |
| error_message | Text | nullable | - |
| created_at | DateTime | - | utcnow |

**索引**：idx_agent_tasks_scan_id, idx_agent_tasks_status

## 模型8: VulnLabChallenge (vuln_lab_challenges)

| 列名 | 类型 | 约束 | 默认值 |
|------|------|------|--------|
| id | String(36) | primary_key | uuid4() |
| target_url | Text | - | - |
| challenge_name | String(255) | nullable | - |
| vuln_type | String(100) | - | - |
| vuln_category | String(50) | nullable | - |
| auth_type | String(20) | nullable | - |
| auth_value | Text | nullable | - |
| status | String(20) | - | "pending" |
| result | String(20) | nullable | - |
| agent_id | String(36) | nullable | - |
| scan_id | String(36) | nullable | - |
| findings_count | Integer | - | 0 |
| critical_count | Integer | - | 0 |
| high_count | Integer | - | 0 |
| medium_count | Integer | - | 0 |
| low_count | Integer | - | 0 |
| info_count | Integer | - | 0 |
| findings_detail | JSON | - | [] |
| started_at | DateTime | nullable | - |
| completed_at | DateTime | nullable | - |
| duration | Integer | nullable | - |
| notes | Text | nullable | - |
| logs | JSON | - | [] |
| endpoints_count | Integer | - | 0 |
| created_at | DateTime | - | utcnow |

**索引**：idx_vuln_lab_status, idx_vuln_lab_vuln_type

## 模型9: Prompt (prompts)

| 列名 | 类型 | 约束 | 默认值 |
|------|------|------|--------|
| id | String(36) | primary_key | uuid4() |
| name | String(255) | - | - |
| description | Text | nullable | - |
| content | Text | - | - |
| is_preset | Boolean | - | False |
| category | String(100) | nullable | - |
| parsed_vulnerabilities | JSON | - | [] |
| created_at | DateTime | - | utcnow |
| updated_at | DateTime | - | utcnow (onupdate=utcnow) |

## 模型关系ER图

```
Scan (scans)
 ├── Target (targets)          — 1:N, cascade=delete-orphan
 ├── Endpoint (endpoints)      — 1:N, cascade=delete-orphan
 │    └── VulnerabilityTest     — N:1 via endpoint_id
 ├── Vulnerability (vulnerabilities) — 1:N, cascade=delete-orphan
 │    └── VulnerabilityTest     — N:1 via test_id
 ├── Report (reports)          — 1:N, cascade=delete-orphan
 └── AgentTask (agent_tasks)   — 1:N, cascade=delete-orphan

Prompt (prompts)               — 独立表
VulnLabChallenge               — 独立表 (scan_id为普通字段，无FK)
```

## 索引汇总

| 索引名 | 表 | 列 |
|--------|-----|-----|
| idx_agent_tasks_scan_id | agent_tasks | scan_id |
| idx_agent_tasks_status | agent_tasks | status |
| idx_vulnerability_tests_scan_id | vulnerability_tests | scan_id |
| idx_vuln_lab_status | vuln_lab_challenges | status |
| idx_vuln_lab_vuln_type | vuln_lab_challenges | vuln_type |

---

# 8. 配置与部署

## 8.1 环境变量配置清单

以下为 `backend/config.py` 中 `Settings` 类的完整配置项：

| 配置项 | 环境变量 | 类型 | 默认值 | 说明 |
|--------|---------|------|--------|------|
| APP_NAME | - | str | "NeuroSploit v3" | 应用名称 |
| APP_VERSION | - | str | "3.0.0" | 版本号 |
| DEBUG | DEBUG | bool | True | 调试模式 |
| HOST | HOST | str | "0.0.0.0" | 监听地址 |
| PORT | PORT | int | 8000 | 监听端口 |
| DATABASE_URL | DATABASE_URL | str | "sqlite+aiosqlite:///./data/neurosploit.db" | 数据库URL |
| ANTHROPIC_API_KEY | ANTHROPIC_API_KEY | Optional[str] | None | Anthropic API Key |
| OPENAI_API_KEY | OPENAI_API_KEY | Optional[str] | None | OpenAI API Key |
| OPENROUTER_API_KEY | OPENROUTER_API_KEY | Optional[str] | None | OpenRouter API Key |
| GEMINI_API_KEY | GEMINI_API_KEY | Optional[str] | None | Gemini API Key |
| TOGETHER_API_KEY | TOGETHER_API_KEY | Optional[str] | None | Together API Key |
| FIREWORKS_API_KEY | FIREWORKS_API_KEY | Optional[str] | None | Fireworks API Key |
| DEFAULT_LLM_PROVIDER | DEFAULT_LLM_PROVIDER | str | "claude" | 默认LLM提供商 |
| DEFAULT_LLM_MODEL | DEFAULT_LLM_MODEL | str | "claude-sonnet-4-20250514" | 默认LLM模型 |
| MAX_OUTPUT_TOKENS | MAX_OUTPUT_TOKENS | Optional[int] | None | 最大输出Token |
| ENABLE_MODEL_ROUTING | ENABLE_MODEL_ROUTING | bool | False | 模型路由 |
| ENABLE_KNOWLEDGE_AUGMENTATION | ENABLE_KNOWLEDGE_AUGMENTATION | bool | False | 知识增强 |
| ENABLE_BROWSER_VALIDATION | ENABLE_BROWSER_VALIDATION | bool | False | 浏览器验证 |
| ENABLE_VULN_AGENTS | ENABLE_VULN_AGENTS | bool | False | 漏洞Agent |
| VULN_AGENT_CONCURRENCY | VULN_AGENT_CONCURRENCY | int | 10 | 漏洞Agent并发数 |
| ENABLE_SMART_ROUTER | ENABLE_SMART_ROUTER | bool | False | 智能路由 |
| ENABLE_RAG | ENABLE_RAG | bool | True | RAG系统 |
| RAG_BACKEND | RAG_BACKEND | str | "auto" | RAG后端(auto/chromadb/tfidf/bm25) |
| METHODOLOGY_FILE | METHODOLOGY_FILE | Optional[str] | None | 方法论文件路径 |
| ENABLE_CLI_AGENT | ENABLE_CLI_AGENT | bool | False | CLI Agent |
| CLI_AGENT_MAX_RUNTIME | CLI_AGENT_MAX_RUNTIME | int | 1800 | CLI Agent最大运行时间(秒) |
| CLI_AGENT_DEFAULT_PROVIDER | CLI_AGENT_DEFAULT_PROVIDER | str | "claude_code" | CLI Agent默认提供商 |
| CODEX_API_KEY | CODEX_API_KEY | Optional[str] | None | Codex API Key |
| MAX_CONCURRENT_SCANS | MAX_CONCURRENT_SCANS | int | 5 | 最大并发扫描数 |
| DEFAULT_TIMEOUT | DEFAULT_TIMEOUT | int | 30 | 默认超时(秒) |
| MAX_REQUESTS_PER_SECOND | MAX_REQUESTS_PER_SECOND | int | 10 | 最大请求/秒 |
| CORS_ORIGINS | - | list | ["http://localhost:3000","http://127.0.0.1:3000"] | CORS允许源 |

## 8.2 .env文件配置

以下为项目根目录 `.env` 文件的完整内容：

```env
# NeuroSploit v3 Environment Variables
# =====================================

# =============================================================================
# LLM API Keys (REQUIRED - at least one must be set)
# =============================================================================
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GEMINI_API_KEY=
OPENROUTER_API_KEY=
TOGETHER_API_KEY=
FIREWORKS_API_KEY=

# Minimax: https://platform.minimaxi.com/
MINIMAX_API_KEY=

# =============================================================================
# Local LLM (optional - no API key needed)
# =============================================================================
#OLLAMA_BASE_URL=http://localhost:11434
#LMSTUDIO_BASE_URL=http://localhost:1234

# =============================================================================
# LLM Configuration
# =============================================================================
#MAX_OUTPUT_TOKENS=64000
#DEFAULT_LLM_MODEL=
ENABLE_MODEL_ROUTING=false

# =============================================================================
# Feature Flags
# =============================================================================
ENABLE_KNOWLEDGE_AUGMENTATION=false
ENABLE_BROWSER_VALIDATION=false

# =============================================================================
# Agent Autonomy (Phase 1-5 modules)
# =============================================================================
#TOKEN_BUDGET=100000
ENABLE_REASONING=true
ENABLE_CVE_HUNT=true
#NVD_API_KEY=
#GITHUB_TOKEN=
ENABLE_MULTI_AGENT=false
ENABLE_RESEARCHER_AI=true
#ENABLE_CLI_AGENT=true
#CLI_AGENT_MAX_RUNTIME=1800
#CLI_AGENT_DEFAULT_PROVIDER=claude_code
#KALI_SANDBOX_IMAGE=neurosploit-kali:latest

# =============================================================================
# Smart Router (OAuth + API provider routing)
# =============================================================================
ENABLE_SMART_ROUTER=true

# =============================================================================
# RAG System (Retrieval-Augmented Generation)
# =============================================================================
ENABLE_RAG=true
RAG_BACKEND=auto

# =============================================================================
# Methodology File (deep injection into agent prompts)
# =============================================================================
#METHODOLOGY_FILE=/opt/Prompts-PenTest/pentestcompleto_en.md

# =============================================================================
# Vuln Type Agents (per-vuln parallel orchestration)
# =============================================================================
ENABLE_VULN_AGENTS=false

# =============================================================================
# Notifications (multi-channel scan alerts)
# =============================================================================
#ENABLE_NOTIFICATIONS=false
#NOTIFICATION_SEVERITY_FILTER=critical,high
#DISCORD_WEBHOOK_URL=
#TELEGRAM_BOT_TOKEN=
#TELEGRAM_CHAT_ID=
#TWILIO_ACCOUNT_SID=
#TWILIO_AUTH_TOKEN=
#TWILIO_FROM_NUMBER=
#TWILIO_TO_NUMBER=

# =============================================================================
# Database (default is SQLite - no config needed)
# =============================================================================
DATABASE_URL=sqlite+aiosqlite:///./data/neurosploit.db

# =============================================================================
# Server Configuration
# =============================================================================
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

**配置分类说明**：

| 分类 | 活跃变量 | 注释变量 | 说明 |
|------|----------|----------|------|
| LLM API Keys | 6个(空值) + MINIMAX_API_KEY | - | 至少需配置一个API Key |
| Local LLM | - | OLLAMA_BASE_URL, LMSTUDIO_BASE_URL | 本地LLM连接地址 |
| LLM Configuration | ENABLE_MODEL_ROUTING | MAX_OUTPUT_TOKENS, DEFAULT_LLM_MODEL | LLM行为配置 |
| Feature Flags | ENABLE_KNOWLEDGE_AUGMENTATION, ENABLE_BROWSER_VALIDATION | - | 功能开关 |
| Agent Autonomy | ENABLE_REASONING, ENABLE_CVE_HUNT, ENABLE_MULTI_AGENT, ENABLE_RESEARCHER_AI | TOKEN_BUDGET, NVD_API_KEY, GITHUB_TOKEN, ENABLE_CLI_AGENT, CLI_AGENT_MAX_RUNTIME, CLI_AGENT_DEFAULT_PROVIDER, KALI_SANDBOX_IMAGE | 代理自主性配置 |
| Smart Router | ENABLE_SMART_ROUTER | - | 智能路由开关 |
| RAG System | ENABLE_RAG, RAG_BACKEND | - | RAG系统配置 |
| Methodology File | - | METHODOLOGY_FILE | 外部方法论文件 |
| Vuln Type Agents | ENABLE_VULN_AGENTS | - | 漏洞类型代理 |
| Notifications | - | 全部8个 | 通知渠道配置 |
| Database | DATABASE_URL | - | 数据库连接 |
| Server | HOST, PORT, DEBUG | - | 服务器配置 |

## 8.3 Docker部署

### docker-compose.yml

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    container_name: neurosploit-backend
    env_file:
      - .env
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
      - OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - DATABASE_URL=sqlite+aiosqlite:///./data/neurosploit.db
    volumes:
      - neurosploit-data:/app/data
    ports:
      - "8000:8000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile.frontend
    container_name: neurosploit-frontend
    ports:
      - "3000:80"
    depends_on:
      backend:
        condition: service_healthy
    restart: unless-stopped

volumes:
  neurosploit-data:

networks:
  default:
    name: neurosploit-network
```

**服务说明**：

| 服务 | Dockerfile | 端口 | 依赖 | 说明 |
|------|-----------|------|------|------|
| backend | docker/Dockerfile.backend | 8000 | - | 后端服务，含健康检查 |
| frontend | docker/Dockerfile.frontend | 3000→80 | backend healthy | 前端服务，依赖后端健康 |

**存储和网络**：

| 资源 | 名称 | 说明 |
|------|------|------|
| Volume | neurosploit-data | 持久化数据（数据库、报告、扫描数据） |
| Network | neurosploit-network | 服务间通信网络 |

### Dockerfile.backend (3阶段构建)

**Stage 1: go-builder** — 编译Go安全工具

```dockerfile
FROM golang:1.22-alpine AS go-builder
RUN apk add --no-cache git
WORKDIR /build
# 并行编译15个Go安全工具
```

| 工具 | 来源 | 用途 |
|------|------|------|
| subfinder | projectdiscovery/subfinder/v2 | 子域发现 |
| httpx | projectdiscovery/httpx | HTTP探测 |
| nuclei | projectdiscovery/nuclei/v3 | 漏洞扫描 |
| waybackurls | tomnomnom/waybackurls | Wayback URL收集 |
| ffuf | ffuf/ffuf/v2 | 模糊测试 |
| katana | projectdiscovery/katana | 爬虫 |
| dnsx | projectdiscovery/dnsx | DNS解析 |
| gau | lc/gau/v2 | URL收集 |
| gf | tomnomnom/gf | Pattern匹配 |
| qsreplace | tomnomnom/qsreplace | URL参数替换 |
| dalfox | hahwul/dalfox/v2 | XSS扫描 |
| gobuster | OJ/gobuster/v3 | 目录爆破 |
| gospider | jaeles-project/gospider | 爬虫 |
| anew | tomnomnom/anew | 去重工具 |
| naabu | projectdiscovery/naabu/v2 | 端口扫描（可选） |
| hakrawler | hakluke/hakrawler | 爬虫（可选） |

**Stage 2: python-deps** — 安装Python依赖

```dockerfile
FROM python:3.11-slim AS python-deps
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt && \
    pip install --no-cache-dir --user arjun wafw00f
```

**Stage 3: runtime** — 最终运行镜像

```dockerfile
FROM python:3.11-slim AS runtime
# 安装运行时依赖: curl, wget, git, dnsutils, nmap, sqlmap, jq
# 复制Go二进制 → Python包 → 应用代码
# 下载SecLists词表 + nuclei模板
# 健康检查 + 启动命令
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**运行时系统依赖**：

| 包 | 用途 |
|----|------|
| curl | 健康检查、HTTP请求 |
| wget | 下载词表 |
| git | 工具安装 |
| dnsutils | DNS查询 |
| nmap | 端口扫描 |
| sqlmap | SQL注入 |
| jq | JSON处理 |
| ca-certificates | SSL证书 |
| libpcap0.8 | 网络抓包 |

## 8.4 数据库迁移

数据库迁移通过 `backend/db/database.py` 中的 `init_db` 和 `_run_migrations` 函数实现，采用增量迁移策略：

### 迁移流程

```
init_db()
    ├── Base.metadata.create_all — 创建所有数据表（基于ORM模型）
    └── _run_migrations(conn) — 增量添加缺失的列和表
```

### 迁移明细

| 目标表 | 迁移操作 | 说明 |
|--------|----------|------|
| scans | ADD COLUMN duration INTEGER | 添加扫描时长字段 |
| reports | ADD COLUMN auto_generated BOOLEAN DEFAULT 0 | 添加AI自动生成标记 |
| reports | ADD COLUMN is_partial BOOLEAN DEFAULT 0 | 添加部分报告标记 |
| vulnerabilities | ADD COLUMN test_id VARCHAR(36) | 关联VulnerabilityTest |
| vulnerabilities | ADD COLUMN poc_parameter VARCHAR(500) | 添加PoC参数字段 |
| vulnerabilities | ADD COLUMN poc_evidence TEXT | 添加PoC证据字段 |
| vulnerabilities | ADD COLUMN screenshots JSON DEFAULT '[]' | 添加截图字段 |
| vulnerabilities | ADD COLUMN url TEXT | 添加URL字段 |
| vulnerabilities | ADD COLUMN parameter VARCHAR(500) | 添加参数字段 |
| vulnerabilities | ADD COLUMN validation_status VARCHAR(20) DEFAULT 'ai_confirmed' | 添加验证状态字段 |
| vulnerabilities | ADD COLUMN ai_rejection_reason TEXT | 添加AI拒绝原因字段 |
| vulnerabilities | ADD COLUMN poc_code TEXT | 添加PoC代码字段 |
| vulnerabilities | ADD COLUMN confidence_score INTEGER | 添加置信度分数字段 |
| vulnerabilities | ADD COLUMN confidence_breakdown JSON DEFAULT '{}' | 添加置信度明细字段 |
| vulnerabilities | ADD COLUMN proof_of_execution TEXT | 添加执行证明字段 |
| agent_tasks | CREATE TABLE (整表创建) | 创建代理任务表 + 2个索引 |
| vulnerability_tests | CREATE TABLE (整表创建) | 创建漏洞测试表 + 1个索引 |
| vuln_lab_challenges | CREATE TABLE (整表创建) | 创建漏洞实验室挑战表 + 2个索引 |
| vuln_lab_challenges | ADD COLUMN logs JSON DEFAULT '[]' | 添加日志字段 |
| vuln_lab_challenges | ADD COLUMN endpoints_count INTEGER DEFAULT 0 | 添加端点计数字段 |

## 8.5 目录结构

```
/workspace/
├── backend/
│   ├── api/v1/          — 18个API路由模块
│   ├── core/            — 60+核心模块
│   ├── db/              — 数据库配置
│   ├── models/          — 9个数据模型
│   ├── config.py        — 配置类
│   ├── main.py          — 应用入口
│   └── requirements.txt
├── frontend/
│   ├── src/pages/       — 18个页面组件
│   ├── src/components/  — 共享组件
│   ├── src/services/    — API服务层
│   ├── src/types/       — TypeScript类型
│   └── package.json
├── data/
│   ├── neurosploit.db   — SQLite数据库
│   ├── providers.json   — 提供商配置
│   ├── reports/         — 生成的报告
│   └── scans/           — 扫描数据
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml
└── .env                 — 环境变量
```
