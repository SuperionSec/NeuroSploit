# NeuroSploit v3 工程结构文档

## 概述
AI驱动的自动化渗透测试平台

---

## 目录

1. [项目整体架构](#项目整体架构)
2. [后端架构](#后端架构)
3. [前端架构](#前端架构)
4. [核心模块说明](#核心模块说明)
5. [数据库设计](#数据库设计)
6. [部署架构](#部署架构)
7. [技术栈](#技术栈)

---

## 项目整体架构

```
NeuroSploit v3/
├── backend/              # 后端服务
├── frontend/           # 前端界面
├── core/             # 共享核心模块
├── agents/           # 专用Agent实现
├── tools/            # 渗透测试工具集成
├── config/          # 配置文件
├── data/            # 数据存储
├── docker/          # Docker配置
├── models/          # 模型训练数据
├── prompts/         # Prompt库
├── scripts/        # 脚本工具
└── reports/        # 报告输出
```

---

## 后端架构

### 目录结构

```
backend/
├── api/
│   ├── v1/                    # REST API v1 (20个路由模块)
│   │   ├── auth.py         # 认证与用户管理
│   │   ├── scans.py        # 扫描CRUD+控制
│   │   ├── agent.py       # AI Agent控制
│   │   ├── agent_tasks.py # Agent任务
│   │   ├── dashboard.py    # 仪表板数据
│   │   ├── reports.py    # 报告管理
│   │   ├── scheduler.py  # 定时任务
│   │   ├── vuln_lab.py # 漏洞实验室
│   │   ├── terminal.py   # 终端Agent
│   │   ├── sandbox.py   # 沙箱管理
│   │   ├── targets.py  # 目标验证
│   │   ├── prompts.py  # Prompt预设
│   │   ├── vulnerabilities.py # 漏洞管理
│   │   ├── settings.py # 系统设置
│   │   ├── knowledge.py # 知识库
│   │   ├── mcp.py     # MCP服务
│   │   ├── providers.py # LLM提供商
│   │   ├── full_ia.py  # FULL AI测试
│   │   └── cli_agent.py # CLI Agent
│   ├── websocket.py     # WebSocket管理器
│
├── core/                      # 核心业务逻辑 (~50+模块)
│   ├── autonomous_agent.py    # 主AI Agent (~7000行)
│   ├── auth_manager.py    # 认证管理器
│   ├── request_engine.py   # 请求引擎
│   ├── waf_detector.py    # WAF检测
│   ├── strategy_adapter.py # 策略适配
│   ├── chain_engine.py    # 利用链引擎
│   ├── confidence_scorer.py  # 置信度评分
│   ├── validation_judge.py  # 验证裁决
│   ├── proof_of_execution.py # 执行验证
│   ├── negative_control.py # 阴性对照
│   ├── checkpoint_manager.py # 检查点管理
│   ├── execution_history.py # 执行历史
│   ├── report_generator.py  # 报告生成器
│   ├── poc_generator.py   # PoC生成
│   ├── xss_context_analyzer.py # XSS上下文
│   ├── access_control_learner.py # 访问控制学习
│   ├── ai_prompt_processor.py # Prompt处理
│   ├── agent_memory.py     # Agent记忆
│   ├── agent_orchestrator.py # Agent编排
│   ├── agent_tasks.py     # Agent任务
│   ├── ai_pentest_agent.py # 渗透Agent
│   ├── autonomous_scanner.py # 自动扫描器
│   ├── banner_analyzer.py # Banner分析
│   ├── cli_agent_runner.py # CLI Agent运行器
│   ├── cli_instructions_builder.py # CLI指令构建
│   ├── cli_output_parser.py # CLI输出解析
│   ├── cve_hunter.py    # CVE猎手
│   ├── deep_recon.py     # 深度侦察
│   ├── endpoint_classifier.py # 端点分类
│   ├── exploit_generator.py # 利用生成
│   ├── knowledge_processor.py # 知识处理
│   ├── methodology_loader.py # 方法论加载
│   ├── notification_manager.py # 通知管理
│   ├── param_analyzer.py # 参数分析
│   ├── payload_mutator.py # Payload变异
│   ├── poc_validator.py  # PoC验证
│   ├── reasoning_engine.py # 推理引擎
│   ├── recon_integration.py # 侦察集成
│   ├── request_repeater.py # 请求重复
│   ├── researcher_agent.py # 研究Agent
│   ├── response_verifier.py # 响应验证
│   ├── site_analyzer.py  # 站点分析
│   ├── specialist_agents.py # 专家Agent
│   ├── task_library.py    # 任务库
│   ├── token_budget.py    # Token预算
│   ├── tool_executor.py  # 工具执行
│   ├── vuln_orchestrator.py # 漏洞编排
│   ├── vuln_type_agent.py # 漏洞类型Agent
│   ├── xss_validator.py # XSS验证
│   │
│   ├── vuln_engine/     # 漏洞引擎
│   │   ├── registry.py # 100种漏洞类型定义
│   │   ├── payload_generator.py # 526个Payload
│   │   ├── ai_prompts.py # AI决策Prompt
│   │   ├── system_prompts.py # 系统Prompt
│   │   ├── pentest_playbook.py # 渗透剧本
│   │   └── testers/ # 11个分类测试器
│   │       ├── injection.py
│   │       ├── auth.py
│   │       ├── authorization.py
│   │       ├── file_access.py
│   │       ├── request_forgery.py
│   │       ├── client_side.py
│   │       ├── infrastructure.py
│   │       ├── data_exposure.py
│   │       ├── logic.py
│   │       ├── advanced_injection.py
│   │       └── cloud_supply.py
│   │
│   ├── smart_router/    # 智能路由
│   │   ├── router.py # LLM提供商路由
│   │   ├── provider_registry.py # 提供商注册
│   │   ├── token_extractor.py # Token提取
│   │   └── token_refresher.py # Token刷新
│   │
│   ├── report_engine/   # 报告引擎
│   │   └── generator.py
│   │
│   ├── prompt_engine/  # Prompt引擎
│   │   └── parser.py
│   │
│   └── rag/          # RAG检索增强
│       ├── engine.py
│       ├── few_shot.py
│       ├── vectorstore.py
│       ├── reasoning_memory.py
│       └── reasoning_templates.py
│
├── db/                       # 数据库层
│   └── database.py          # 数据库连接管理
│
├── models/                   # SQLAlchemy ORM模型
│   ├── user.py
│   ├── scan.py
│   ├── vulnerability.py
│   ├── report.py
│   ├── target.py
│   ├── prompt.py
│   ├── agent_task.py
│   ├── endpoint.py
│   └── vuln_lab.py
│
├── schemas/                  # Pydantic模式
│   ├── auth.py
│   ├── scan.py
│   ├── vulnerability.py
│   ├── report.py
│   ├── target.py
│   ├── prompt.py
│   └── agent_task.py
│
├── services/                # 服务层
│   ├── scan_service.py
│   └── report_service.py
│
├── migrations/             # 数据库迁移
│   └── 001_add_dashboard_integration.sql
│
├── config.py             # 配置管理
└── main.py            # FastAPI应用入口
└── requirements.txt    # Python依赖
```

### 后端分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    API 层 (FastAPI)                         │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐              │
│  │Auth │ │Scans│ │Agent│ │Reports│ │... 20 routers   │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘              │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                   Service 层 (业务逻辑)                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Autonomous Agent (主Agent)               │  │
│  │  ┌──────────────┐  ┌──────────────┐             │  │
│  │  │ 3-Stream   │  │ Validation    │             │  │
│  │  │ Parallel   │  │ Pipeline   │             │  │
│  │  └──────────────┘  └──────────────┘             │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│  │Vuln Engine│ │Smart Router │ │Report Eng │        │
│  └─────────────┘ └─────────────┘ └─────────────┘        │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────────┐
│                   数据层 (SQLAlchemy)                            │
│  ┌──────────────┐ ┌──────────────┐ ┌───────────┐         │
│  │   Models   │ │   Schemas   │ │ Database │         │
│  └──────────────┘ └──────────────┘ └───────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### 核心API路由映射

| 模块 | 路由前缀 | 功能 |
|------|---------|------|
| Authentication | `/api/v1/auth` | 认证、用户管理、JWT |
| Scans | `/api/v1/scans` | 扫描CRUD、开始/暂停/恢复/停止 |
| AI Agent | `/api/v1/agent` | Agent运行、状态、日志、发现 |
| Agent Tasks | `/api/v1/agent-tasks` | Agent任务管理 |
| Dashboard | `/api/v1/dashboard` | 统计、活动流 |
| Reports | `/api/v1/reports` | 报告生成、查看、下载 |
| Scheduler | `/api/v1/scheduler` | 定时任务CRUD |
| Vulnerability Lab | `/api/v1/vuln-lab` | 100种漏洞类型测试 |
| Terminal | `/api/v1/terminal` | AI终端Agent |
| Sandbox | `/api/v1/sandbox` | Kali容器管理 |
| Targets | `/api/v1/targets` | 目标URL验证 |
| Prompts | `/api/v1/prompts` | Prompt预设管理 |
| Vulnerabilities | `/api/v1/vulnerabilities` | 漏洞管理 |
| Settings | `/api/v1/settings` | 系统设置 |
| Knowledge | `/api/v1/knowledge` | 知识库 |
| MCP Servers | `/api/v1/mcp` | MCP服务器管理 |
| Providers | `/api/v1/providers` | LLM提供商管理 |
| FULL AI Testing | `/api/v1/full-ia` | FULL AI测试 |
| CLI Agent | `/cli-agent` | CLI Agent |

---

## 前端架构

### 目录结构

```
frontend/
├── src/
│   ├── pages/               # 页面组件 (19个页面)
│   │   ├── HomePage.tsx                 # 仪表板
│   │   ├── UserManagementPage.tsx        # 用户管理
│   │   ├── NewScanPage.tsx               # 新建扫描
│   │   ├── ScanDetailsPage.tsx            # 扫描详情
│   │   ├── AutoPentestPage.tsx            # 自动渗透
│   │   ├── FullIATestingPage.tsx          # FULL AI测试
│   │   ├── AgentStatusPage.tsx            # Agent状态
│   │   ├── TaskLibraryPage.tsx            # 任务库
│   │   ├── RealtimeTaskPage.tsx           # 实时任务
│   │   ├── ReportsPage.tsx               # 报告管理
│   │   ├── ReportViewPage.tsx             # 报告查看
│   │   ├── SchedulerPage.tsx           # 定时任务
│   │   ├── VulnLabPage.tsx               # 漏洞实验室
│   │   ├── TerminalAgentPage.tsx           # 终端Agent
│   │   ├── SandboxDashboardPage.tsx       # 沙箱仪表板
│   │   ├── KnowledgePage.tsx               # 知识库
│   │   ├── MCPManagementPage.tsx        # MCP管理
│   │   ├── ProvidersPage.tsx           # LLM提供商
│   │   └── SettingsPage.tsx             # 系统设置
│   │
│   ├── components/           # 可复用组件
│   │   ├── common/
│   │   │   ├── Badge.tsx
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Textarea.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Layout.tsx
│   │   │   └── Sidebar.tsx
│   │   └── VulnAgentGrid.tsx
│   │
│   ├── services/           # 服务层
│   │   ├── api.ts              # Axios API客户端
│   │   └── websocket.ts       # WebSocket客户端
│   │
│   ├── store/             # 状态管理
│   │   └── index.ts           # Zustand store
│   │
│   ├── config/            # 配置
│   │   ├── menuData.tsx        # 侧边栏菜单数据
│   │   └── proSettings.ts       # Pro组件配置
│   │
│   ├── types/             # TypeScript类型定义
│   │   └── index.ts
│   │
│   ├── styles/            # 样式
│   │   └── globals.css
│   │
│   ├── App.tsx           # 主应用组件
│   └── main.tsx          # 应用入口
│
├── public/               # 静态资源
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
├── tsconfig.json
└── tsconfig.node.json
```

### 前端技术栈

- **框架**: React 18 + TypeScript
- **构建工具**: Vite
- **UI组件库**: Ant Design 5 + ProComponents
- **路由**: React Router DOM
- **状态管理**: Zustand
- **图表**: Recharts
- **HTTP客户端**: Axios
- **样式**: TailwindCSS
- **WebSocket**: Socket.io Client

### 前端路由映射

| 页面 | 路由 | 功能 |
|------|------|------|
| 仪表板 | `/` 或 `/dashboard` | 统计概览、活动流 |
| 用户管理 | `/users` | 用户CRUD、角色管理 |
| 新建扫描 | `/scan/new` | 创建新扫描 |
| 扫描详情 | `/scan/:id` | 扫描发现、验证、控制 |
| 自动渗透 | `/auto-pentest` | 3流并行自动渗透 |
| FULL AI测试 | `/full-ia` | FULL AI测试 |
| Agent状态 | `/agent` | Agent状态监控 |
| 任务库 | `/tasks` | 任务库 |
| 实时任务 | `/realtime` | 实时任务 |
| 报告管理 | `/reports` | 报告列表、生成 |
| 报告查看 | `/reports/:id` | 查看HTML报告 |
| 定时任务 | `/scheduler` | Cron任务管理 |
| 漏洞实验室 | `/vuln-lab` | 100种漏洞类型测试 |
| 终端Agent | `/terminal` | AI终端交互 |
| 沙箱仪表板 | `/sandbox` | Kali容器监控 |
| 知识库 | `/knowledge` | 知识库管理 |
| MCP管理 | `/mcp` | MCP服务器管理 |
| LLM提供商 | `/providers` | LLM提供商管理 |
| 系统设置 | `/settings` | 系统配置 |

---

## 核心模块说明

### 1. Autonomous Agent (自主Agent)

**位置**: `backend/core/autonomous_agent.py`

**架构**:
- **3-Stream并行处理:
  - Stream 1: Recon (侦察) - 页面爬取、参数发现、技术检测、WAF检测
  - Stream 2: Junior Tester (初级测试) - AI优先、3个Payload/端点
  - Stream 3: Tool Runner (工具运行) - Nuclei、Naabu、AI决策额外工具

**模块**:
- Request Engine: 重试回退、按主机限流、熔断器
- WAF Detector: 16种WAF特征、12种绕过技术
- Strategy Adapter: 端点检测、收益递减、优先级重算
- Chain Engine: 10种利用链规则
- Auth Manager: 多用户上下文

### 2. Vuln Engine (漏洞引擎)

**位置**: `backend/core/vuln_engine/`

**100种漏洞类型**:
- Injection (38): XSS(反射/存储/DOM)、SQLi、NoSQLi、命令注入、SSTI等
- Inspection (21): 安全头、CORS、点击劫持、信息泄露等
- AI-Driven (41): BOLA、BFLA、IDOR、竞态条件、业务逻辑等
- Authentication (8): 认证绕过、会话固定、密码重置等
- Authorization (6): 权限提升、强制浏览等
- File Access (5): LFI、RFI、路径遍历、文件上传、XXE
- Request Forgery (4): SSRF、CSRF、云元数据、DNS重绑定
- Client-Side (8): CORS、点击劫持、开放重定向、DOM破坏等
- Infrastructure (6): SSL/TLS、HTTP方法、子域名接管等
- Cloud/Supply (4): 云元数据、S3配置错误、依赖混淆等

### 3. Validation Pipeline (验证管道)

**位置**: `backend/core/`

```
发现候选 → 阴性对照 → 执行验证 → AI解释 → 置信度评分 → 验证裁决
    ↓           ↓           ↓          ↓          ↓           ↓
  (1)        (2)         (3)       (4)        (5)         (6)
```

1. 阴性对照: 发送良性/空请求作为对照
2. 执行验证: 25+种漏洞类型验证方法
3. AI解释: 12种组合Prompt模板
4. 置信度: 0-100分
5. 验证裁决: 最终判定权威

### 4. Kali Sandbox System (Kali沙箱系统)

**位置**: `core/kali_sandbox.py`, `core/container_pool.py`

**特性**:
- 每个扫描独立Kali容器
- 按需工具安装(56个工具)
- 最大5个并发容器
- 自动清理、TTL 60分钟
- 28个预安装工具: Nuclei、Naabu、httpx、Nmap、Nikto等

### 5. Smart Router (智能路由)

**位置**: `backend/core/smart_router/`

**支持LLM提供商**:
- Anthropic Claude
- OpenAI GPT
- Google Gemini
- Ollama
- LMStudio
- OpenRouter

**特性**:
- Token预算管理
- 自动Token刷新
- 提供商选择策略
- 失败自动降级

### 6. RAG检索增强

**位置**: `backend/core/rag/`

**组件**:
- 向量存储: BM25索引
- 推理记忆
- 少样本示例
- 推理模板

---

## 数据库设计

### ORM模型

| 表名 | 说明 |
|------|------|
| users | 用户信息 |
| scans | 扫描记录 |
| vulnerabilities | 漏洞发现 |
| reports | 报告 |
| targets | 目标 |
| prompts | 预设Prompt |
| agent_tasks | Agent任务 |
| endpoints | 端点 |
| vuln_lab | 漏洞实验室运行 |

---

## 部署架构

### Docker Compose

```yaml
services:
  backend:
    build: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - ANTHROPIC_API_KEY
      - OPENAI_API_KEY
      - DATABASE_URL

  frontend:
    build: docker/Dockerfile.frontend
    ports:
      - "3000:3000"

  kali-sandbox:
    build: docker/Dockerfile.kali
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

### 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| 后端API | 8000 | FastAPI |
| 前端界面 | 8001 | Vite dev |
| 前端生产 | 3000 | 静态构建 |
| WebSocket | 8000 | `/ws/scan/{scan_id}` |
| Swagger UI | 8000 | `/api/docs` |

---

## 技术栈

### 后端

| 技术 | 说明 |
|------|------|
| Python 3.10+ | 编程语言 |
| FastAPI | Web框架 |
| SQLAlchemy 2.0+ | ORM |
| Pydantic 2.5+ | 数据验证 |
| Uvicorn | ASGI服务器 |
| aiosqlite | 异步SQLite |
| aiohttp | HTTP客户端 |
| httpx | HTTP客户端 |
| anthropic | Claude API |
| openai | GPT API |
| python-jose | JWT认证 |
| APScheduler | 定时任务 |
| Jinja2 | 模板引擎 |
| WeasyPrint | PDF生成 |

### 前端

| 技术 | 说明 |
|------|------|
| React 18 | UI框架 |
| TypeScript | 类型安全 |
| Vite | 构建工具 |
| Ant Design 5 | UI组件库 |
| ProComponents | 企业级组件 |
| React Router 6 | 路由 |
| Zustand | 状态管理 |
| Recharts | 图表库 |
| TailwindCSS | CSS框架 |
| Axios | HTTP客户端 |
| Socket.io | WebSocket |

### 基础设施

| 技术 | 说明 |
|------|------|
| Docker | 容器化 |
| Docker Compose | 编排 |
| Kali Linux | 渗透测试环境 |
| ProjectDiscovery | 安全工具套件 |
| Nmap | 端口扫描 |
| SQLMap | SQL注入 |
| Nikto | Web扫描 |
| MCP Protocol | 工具协议 |
| Playwright | 浏览器自动化 |

---

## 配置文件

### 环境变量

```bash
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GEMINI_API_KEY=
OLLAMA_BASE_URL=http://localhost:11434
LMSTUDIO_BASE_URL=http://localhost:1234
OPENROUTER_API_KEY=
DATABASE_URL=sqlite+aiosqlite:///./data/neurosploit.db
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

### config/config.json

```json
{
  "llm": { ... },
  "agent_roles": { ... },
  "sandbox": { ... },
  "mcp_servers": { ... }
}
```

---

## 开发流程

### 后端开发

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发

```bash
cd frontend
npm install
npm run dev
```

### 构建Kali沙箱

```bash
./scripts/build-kali.sh
```

---

**NeuroSploit v3 - AI-Powered Autonomous Penetration Testing Platform
