# NeuroSploit v3.2.4 泛化功能验证测试计划

> 本测试计划采用三层架构设计：**适配器配置层**（定义路由映射）→ **功能契约层**（定义行为预期）→ **验证逻辑层**（定义判定标准）。
> 移植到新系统时，只需修改适配器配置层的路由映射，功能契约和验证逻辑无需改动。

---

## 1. 适配器配置层

### 1.1 环境变量

| 变量 | 含义 | 示例值 | 说明 |
|------|------|--------|------|
| `BASE_URL` | 后端服务根地址 | `http://localhost:8000` | 新系统替换为实际后端地址 |
| `FRONTEND_URL` | 前端服务根地址 | `http://localhost:3001` | 新系统替换为实际前端地址 |
| `API_PREFIX` | API路由前缀 | `/api/v1` | 新系统可能为 `/v2`、`/rest` 等 |
| `WS_ENDPOINT` | WebSocket端点 | `/ws` | 实时通信端点 |
| `AUTH_HEADER` | 认证头名称 | `Authorization` | 如需认证，填写认证头名称 |
| `AUTH_TOKEN` | 认证令牌 | 空 | 如需认证，填写有效令牌 |

### 1.2 功能资源-路由映射表

以下表格定义了每个功能资源到实际路由的映射。**移植时只需修改此表**，测试用例通过功能资源名引用路由。

| 功能资源ID | 功能描述 | HTTP方法 | 通用路由模板 | v3.2.4 完整路由 |
|-----------|----------|----------|-------------|----------------|
| RES-HEALTH | 健康检查 | GET | `/health` | `http://localhost:8000/health` |
| RES-DASHBOARD-STATS | 仪表板统计 | GET | `${API_PREFIX}/dashboard/stats` | `http://localhost:8000/api/v1/dashboard/stats` |
| RES-DASHBOARD-RECENT | 最近扫描 | GET | `${API_PREFIX}/dashboard/recent` | `http://localhost:8000/api/v1/dashboard/recent` |
| RES-DASHBOARD-ACTIVITY | 活动日志 | GET | `${API_PREFIX}/dashboard/activity-feed` | `http://localhost:8000/api/v1/dashboard/activity-feed` |
| RES-SCAN-LIST | 扫描列表 | GET | `${API_PREFIX}/scans` | `http://localhost:8000/api/v1/scans` |
| RES-SCAN-DETAIL | 扫描详情 | GET | `${API_PREFIX}/scans/{id}` | `http://localhost:8000/api/v1/scans/{id}` |
| RES-SCAN-VULNS | 扫描漏洞 | GET | `${API_PREFIX}/scans/{id}/vulnerabilities` | `http://localhost:8000/api/v1/scans/{id}/vulnerabilities` |
| RES-SCAN-ENDPOINTS | 扫描端点 | GET | `${API_PREFIX}/scans/{id}/endpoints` | `http://localhost:8000/api/v1/scans/{id}/endpoints` |
| RES-SCAN-TASKS | 扫描任务 | GET | `${API_PREFIX}/scans/{id}/tasks` | `http://localhost:8000/api/v1/scans/{id}/tasks` |
| RES-SCAN-LOGS | 扫描日志 | GET | `${API_PREFIX}/scans/{id}/logs` | `http://localhost:8000/api/v1/scans/{id}/logs` |
| RES-SCAN-CREATE | 创建扫描 | POST | `${API_PREFIX}/scans` | `http://localhost:8000/api/v1/scans` |
| RES-SCAN-DELETE | 删除扫描 | DELETE | `${API_PREFIX}/scans/{id}` | `http://localhost:8000/api/v1/scans/{id}` |
| RES-AGENT-RUN | 启动代理 | POST | `${API_PREFIX}/agent/run` | `http://localhost:8000/api/v1/agent/run` |
| RES-AGENT-STATUS | 代理状态 | GET | `${API_PREFIX}/agent/status/{id}` | `http://localhost:8000/api/v1/agent/status/{id}` |
| RES-AGENT-ACTIVE | 活跃代理 | GET | `${API_PREFIX}/agent/active` | `http://localhost:8000/api/v1/agent/active` |
| RES-AGENT-PAUSE | 暂停代理 | POST | `${API_PREFIX}/agent/pause/{id}` | `http://localhost:8000/api/v1/agent/pause/{id}` |
| RES-AGENT-RESUME | 恢复代理 | POST | `${API_PREFIX}/agent/resume/{id}` | `http://localhost:8000/api/v1/agent/resume/{id}` |
| RES-AGENT-STOP | 停止代理 | POST | `${API_PREFIX}/agent/stop/{id}` | `http://localhost:8000/api/v1/agent/stop/{id}` |
| RES-AGENT-PROMPT | 发送提示词 | POST | `${API_PREFIX}/agent/prompt/{id}` | `http://localhost:8000/api/v1/agent/prompt/{id}` |
| RES-AGENT-TASKS | 代理任务模板 | GET | `${API_PREFIX}/agent/tasks` | `http://localhost:8000/api/v1/agent/tasks` |
| RES-AGENT-REALTIME-SESSION | 实时会话创建 | POST | `${API_PREFIX}/agent/realtime/session` | `http://localhost:8000/api/v1/agent/realtime/session` |
| RES-AGENT-REALTIME-MSG | 实时消息发送 | POST | `${API_PREFIX}/agent/realtime/{id}/message` | `http://localhost:8000/api/v1/agent/realtime/{id}/message` |
| RES-AGENT-REALTIME-TOOL | 实时工具执行 | POST | `${API_PREFIX}/agent/realtime/{id}/execute-tool` | `http://localhost:8000/api/v1/agent/realtime/{id}/execute-tool` |
| RES-AGENT-REALTIME-TOOLS | 工具状态 | GET | `${API_PREFIX}/agent/realtime/tools/status` | `http://localhost:8000/api/v1/agent/realtime/tools/status` |
| RES-AGENT-REALTIME-LLM | LLM状态 | GET | `${API_PREFIX}/agent/realtime/llm-status` | `http://localhost:8000/api/v1/agent/realtime/llm-status` |
| RES-AGENT-REALTIME-REPORT | 实时报告 | GET | `${API_PREFIX}/agent/realtime/{id}/report` | `http://localhost:8000/api/v1/agent/realtime/{id}/report` |
| RES-PROVIDER-LIST | 提供商列表 | GET | `${API_PREFIX}/providers` | `http://localhost:8000/api/v1/providers` |
| RES-PROVIDER-STATUS | 提供商状态 | GET | `${API_PREFIX}/providers/status` | `http://localhost:8000/api/v1/providers/status` |
| RES-PROVIDER-CONNECT | 连接提供商 | POST | `${API_PREFIX}/providers/{id}/connect` | `http://localhost:8000/api/v1/providers/{id}/connect` |
| RES-PROVIDER-TEST | 测试连接 | POST | `${API_PREFIX}/providers/test/{pid}/{aid}` | `http://localhost:8000/api/v1/providers/test/{pid}/{aid}` |
| RES-PROVIDER-TOGGLE | 启用禁用 | POST | `${API_PREFIX}/providers/{id}/toggle` | `http://localhost:8000/api/v1/providers/{id}/toggle` |
| RES-PROVIDER-DETECT | 检测CLI令牌 | POST | `${API_PREFIX}/providers/{id}/detect` | `http://localhost:8000/api/v1/providers/{id}/detect` |
| RES-PROVIDER-DETECT-ALL | 检测所有CLI | POST | `${API_PREFIX}/providers/detect-all` | `http://localhost:8000/api/v1/providers/detect-all` |
| RES-PROVIDER-ACCT-DEL | 删除账户 | DELETE | `${API_PREFIX}/providers/{pid}/accounts/{aid}` | `http://localhost:8000/api/v1/providers/{pid}/accounts/{aid}` |
| RES-PROVIDER-ENV | 环境变量 | GET/POST | `${API_PREFIX}/providers/env` | `http://localhost:8000/api/v1/providers/env` |
| RES-PROVIDER-MODELS | 可用模型 | GET | `${API_PREFIX}/providers/available-models` | `http://localhost:8000/api/v1/providers/available-models` |
| RES-SETTINGS | 系统设置 | GET/PUT | `${API_PREFIX}/settings` | `http://localhost:8000/api/v1/settings` |
| RES-SETTINGS-TOOLS | 工具检测 | GET | `${API_PREFIX}/settings/tools` | `http://localhost:8000/api/v1/settings/tools` |
| RES-SETTINGS-NOTIFY-TEST | 通知测试 | POST | `${API_PREFIX}/settings/notifications/test/{channel}` | `http://localhost:8000/api/v1/settings/notifications/test/{channel}` |
| RES-REPORT-LIST | 报告列表 | GET | `${API_PREFIX}/reports` | `http://localhost:8000/api/v1/reports` |
| RES-REPORT-VIEW | 报告查看 | GET | `${API_PREFIX}/reports/{id}/view` | `http://localhost:8000/api/v1/reports/{id}/view` |
| RES-REPORT-DOWNLOAD | 报告下载 | GET | `${API_PREFIX}/reports/{id}/download/{format}` | `http://localhost:8000/api/v1/reports/{id}/download/{format}` |
| RES-REPORT-CREATE | 报告生成 | POST | `${API_PREFIX}/reports` | `http://localhost:8000/api/v1/reports` |
| RES-REPORT-AI | AI报告生成 | POST | `${API_PREFIX}/reports/ai-generate` | `http://localhost:8000/api/v1/reports/ai-generate` |
| RES-REPORT-DELETE | 删除报告 | DELETE | `${API_PREFIX}/reports/{id}` | `http://localhost:8000/api/v1/reports/{id}` |
| RES-VULN-LIST | 漏洞列表 | GET | `${API_PREFIX}/scans/{id}/vulnerabilities` | `http://localhost:8000/api/v1/scans/{id}/vulnerabilities` |
| RES-VULN-VALIDATE | 漏洞验证 | PATCH | `${API_PREFIX}/vulnerabilities/{id}/validate` | `http://localhost:8000/api/v1/vulnerabilities/{id}/validate` |
| RES-VULN-FEEDBACK | 漏洞反馈 | POST | `${API_PREFIX}/vulnerabilities/{id}/feedback` | `http://localhost:8000/api/v1/vulnerabilities/{id}/feedback` |
| RES-VULNLAB-CATEGORIES | 漏洞实验室分类 | GET | `${API_PREFIX}/vuln-lab/categories` | `http://localhost:8000/api/v1/vuln-lab/categories` |
| RES-VULNLAB-RUN | 启动挑战 | POST | `${API_PREFIX}/vuln-lab/run` | `http://localhost:8000/api/v1/vuln-lab/run` |
| RES-VULNLAB-CHALLENGES | 挑战列表 | GET | `${API_PREFIX}/vuln-lab/challenges` | `http://localhost:8000/api/v1/vuln-lab/challenges` |
| RES-VULNLAB-STOP | 停止挑战 | POST | `${API_PREFIX}/vuln-lab/challenges/{id}/stop` | `http://localhost:8000/api/v1/vuln-lab/challenges/{id}/stop` |
| RES-VULNLAB-DELETE | 删除挑战 | DELETE | `${API_PREFIX}/vuln-lab/challenges/{id}` | `http://localhost:8000/api/v1/vuln-lab/challenges/{id}` |
| RES-TERMINAL-SESSIONS | 终端会话 | GET/POST | `${API_PREFIX}/terminal/sessions` | `http://localhost:8000/api/v1/terminal/sessions` |
| RES-TERMINAL-EXEC | 终端执行 | POST | `${API_PREFIX}/terminal/sessions/{id}/execute` | `http://localhost:8000/api/v1/terminal/sessions/{id}/execute` |
| RES-TERMINAL-AI | AI建议 | POST | `${API_PREFIX}/terminal/sessions/{id}/ai-suggest` | `http://localhost:8000/api/v1/terminal/sessions/{id}/ai-suggest` |
| RES-SANDBOX-LIST | 沙箱列表 | GET | `${API_PREFIX}/sandbox/` | `http://localhost:8000/api/v1/sandbox/` |
| RES-SANDBOX-DETAIL | 沙箱详情 | GET | `${API_PREFIX}/sandbox/{id}` | `http://localhost:8000/api/v1/sandbox/{id}` |
| RES-SANDBOX-DESTROY | 销毁沙箱 | DELETE | `${API_PREFIX}/sandbox/{id}` | `http://localhost:8000/api/v1/sandbox/{id}` |
| RES-SANDBOX-CLEANUP | 清理沙箱 | POST | `${API_PREFIX}/sandbox/cleanup` | `http://localhost:8000/api/v1/sandbox/cleanup` |
| RES-KNOWLEDGE-STATS | 知识库统计 | GET | `${API_PREFIX}/knowledge/stats` | `http://localhost:8000/api/v1/knowledge/stats` |
| RES-KNOWLEDGE-DOCS | 知识库文档 | GET | `${API_PREFIX}/knowledge/documents` | `http://localhost:8000/api/v1/knowledge/documents` |
| RES-KNOWLEDGE-UPLOAD | 知识库上传 | POST | `${API_PREFIX}/knowledge/upload` | `http://localhost:8000/api/v1/knowledge/upload` |
| RES-KNOWLEDGE-DELETE | 删除文档 | DELETE | `${API_PREFIX}/knowledge/documents/{id}` | `http://localhost:8000/api/v1/knowledge/documents/{id}` |
| RES-MCP-SERVERS | MCP服务器 | GET/POST | `${API_PREFIX}/mcp/servers` | `http://localhost:8000/api/v1/mcp/servers` |
| RES-MCP-START | 启动MCP | POST | `${API_PREFIX}/mcp/servers/{id}/start` | `http://localhost:8000/api/v1/mcp/servers/{id}/start` |
| RES-MCP-STOP | 停止MCP | POST | `${API_PREFIX}/mcp/servers/{id}/stop` | `http://localhost:8000/api/v1/mcp/servers/{id}/stop` |
| RES-MCP-TOOLS | MCP工具 | GET | `${API_PREFIX}/mcp/servers/{id}/tools` | `http://localhost:8000/api/v1/mcp/servers/{id}/tools` |
| RES-MCP-DELETE | 删除MCP | DELETE | `${API_PREFIX}/mcp/servers/{id}` | `http://localhost:8000/api/v1/mcp/servers/{id}` |
| RES-SCHEDULER-LIST | 调度列表 | GET | `${API_PREFIX}/scheduler/` | `http://localhost:8000/api/v1/scheduler/` |
| RES-SCHEDULER-CREATE | 创建调度 | POST | `${API_PREFIX}/scheduler/` | `http://localhost:8000/api/v1/scheduler/` |
| RES-SCHEDULER-PAUSE | 暂停调度 | POST | `${API_PREFIX}/scheduler/{id}/pause` | `http://localhost:8000/api/v1/scheduler/{id}/pause` |
| RES-SCHEDULER-RESUME | 恢复调度 | POST | `${API_PREFIX}/scheduler/{id}/resume` | `http://localhost:8000/api/v1/scheduler/{id}/resume` |
| RES-SCHEDULER-DELETE | 删除调度 | DELETE | `${API_PREFIX}/scheduler/{id}` | `http://localhost:8000/api/v1/scheduler/{id}` |
| RES-TARGET-VALIDATE | 目标验证 | POST | `${API_PREFIX}/targets/validate` | `http://localhost:8000/api/v1/targets/validate` |
| RES-TARGET-VALIDATE-BULK | 批量验证 | POST | `${API_PREFIX}/targets/validate/bulk` | `http://localhost:8000/api/v1/targets/validate/bulk` |
| RES-TARGET-UPLOAD | 目标上传 | POST | `${API_PREFIX}/targets/upload` | `http://localhost:8000/api/v1/targets/upload` |
| RES-PROMPT-LIST | 提示词列表 | GET | `${API_PREFIX}/prompts` | `http://localhost:8000/api/v1/prompts` |
| RES-PROMPT-CREATE | 创建提示词 | POST | `${API_PREFIX}/prompts` | `http://localhost:8000/api/v1/prompts` |
| RES-PROMPT-UPDATE | 更新提示词 | PUT | `${API_PREFIX}/prompts/{id}` | `http://localhost:8000/api/v1/prompts/{id}` |
| RES-PROMPT-DELETE | 删除提示词 | DELETE | `${API_PREFIX}/prompts/{id}` | `http://localhost:8000/api/v1/prompts/{id}` |
| RES-FULLIA-START | Full IA启动 | POST | `${API_PREFIX}/full-ia/start` | `http://localhost:8000/api/v1/full-ia/start` |
| RES-FULLIA-STATUS | Full IA状态 | GET | `${API_PREFIX}/full-ia/status/{id}` | `http://localhost:8000/api/v1/full-ia/status/{id}` |
| RES-FULLIA-STOP | Full IA停止 | POST | `${API_PREFIX}/full-ia/stop/{id}` | `http://localhost:8000/api/v1/full-ia/stop/{id}` |

### 1.3 前端页面路由映射

| 页面功能ID | 功能描述 | 通用路径模板 | v3.2.4 完整URL |
|-----------|----------|-------------|----------------|
| PAGE-HOME | 首页仪表板 | `/` | `http://localhost:3001/` |
| PAGE-NEW-SCAN | 新建扫描 | `/scan/new` | `http://localhost:3001/scan/new` |
| PAGE-AUTO-PENTEST | 自动渗透 | `/auto-pentest` | `http://localhost:3001/auto-pentest` |
| PAGE-SCAN-DETAIL | 扫描详情 | `/scan/{id}` | `http://localhost:3001/scan/{id}` |
| PAGE-AGENT-STATUS | 代理状态 | `/agent/{id}` | `http://localhost:3001/agent/{id}` |
| PAGE-VULN-LAB | 漏洞实验室 | `/vuln-lab` | `http://localhost:3001/vuln-lab` |
| PAGE-TERMINAL | 终端代理 | `/terminal` | `http://localhost:3001/terminal` |
| PAGE-PROVIDERS | 提供商管理 | `/providers` | `http://localhost:3001/providers` |
| PAGE-SETTINGS | 系统设置 | `/settings` | `http://localhost:3001/settings` |
| PAGE-FULL-IA | Full IA测试 | `/full-ia` | `http://localhost:3001/full-ia` |
| PAGE-MCP | MCP管理 | `/mcp` | `http://localhost:3001/mcp` |
| PAGE-SCHEDULER | 调度器 | `/scheduler` | `http://localhost:3001/scheduler` |
| PAGE-KNOWLEDGE | 知识库 | `/knowledge` | `http://localhost:3001/knowledge` |
| PAGE-REALTIME | 实时任务 | `/realtime` | `http://localhost:3001/realtime` |
| PAGE-SANDBOX | 沙箱管理 | `/sandboxes` | `http://localhost:3001/sandboxes` |
| PAGE-TASKS | 任务库 | `/tasks` | `http://localhost:3001/tasks` |
| PAGE-REPORTS | 报告列表 | `/reports` | `http://localhost:3001/reports` |
| PAGE-REPORT-VIEW | 报告查看 | `/reports/{id}` | `http://localhost:3001/reports/{id}` |

---

## 2. 功能域定义

系统按功能域组织，每个功能域包含一组相关的功能资源和业务规则。

### 2.1 功能域概览

| 功能域 | 核心能力 | 关键资源 | 依赖域 |
|--------|----------|----------|--------|
| 扫描引擎 | 创建/管理/查询安全扫描 | RES-SCAN-* | 代理系统、提供商管理 |
| 代理系统 | AI代理的启动/暂停/停止/交互 | RES-AGENT-* | 提供商管理 |
| 提供商管理 | LLM提供商配置/连接/测试 | RES-PROVIDER-* | 无 |
| 漏洞实验室 | 漏洞专项测试和挑战 | RES-VULNLAB-* | 代理系统 |
| 实时任务 | AI对话式安全测试 | RES-AGENT-REALTIME-* | 提供商管理 |
| 终端代理 | 命令行交互式测试 | RES-TERMINAL-* | 提供商管理 |
| 报告系统 | 报告生成/查看/下载 | RES-REPORT-* | 扫描引擎 |
| 知识增强 | RAG文档管理 | RES-KNOWLEDGE-* | 无 |
| 沙箱执行 | Kali容器管理 | RES-SANDBOX-* | 扫描引擎 |
| MCP集成 | MCP服务器管理 | RES-MCP-* | 无 |
| 调度系统 | 定时任务调度 | RES-SCHEDULER-* | 代理系统 |
| 系统配置 | 全局设置/通知 | RES-SETTINGS* | 无 |
| 漏洞管理 | 漏洞验证/反馈 | RES-VULN-* | 扫描引擎 |
| 目标管理 | 目标验证/上传 | RES-TARGET-* | 无 |
| 提示词管理 | 提示词CRUD | RES-PROMPT-* | 无 |
| Full IA | 全流程AI测试 | RES-FULLIA-* | 代理系统 |
| 仪表板 | 全局统计/概览 | RES-DASHBOARD-* | 扫描引擎、代理系统 |

### 2.2 资源状态机

每个核心资源都有明确的状态流转，测试需验证每个状态转换的正确性。

**扫描 (Scan) 状态机：**
```
pending → running → completed
                 → failed
                 → stopped (用户手动停止)
```

**代理 (Agent) 状态机：**
```
running → paused → running (恢复)
       → stopped (手动停止)
       → completed (自然完成)
       → failed (执行异常)
```

**提供商 (Provider) 状态机：**
```
disconnected → connected (添加凭据/检测到令牌)
connected → disconnected (删除所有账户)
enabled → disabled (toggle)
disabled → enabled (toggle)
```

**漏洞 (Vulnerability) 验证状态：**
```
unverified → confirmed (确认真阳性)
           → false_positive (标记误报)
confirmed → unverified (撤销验证)
false_positive → unverified (撤销验证)
```

**沙箱 (Sandbox) 状态机：**
```
creating → running → expired (超时)
                 → destroyed (手动销毁)
running → orphaned (关联扫描丢失)
```

**调度 (Schedule) 状态机：**
```
active → paused (暂停)
paused → active (恢复)
active/paused → deleted (删除)
```

---

## 3. LLM 执行指引

### 3.1 如何使用本测试计划

本测试计划专为 LLM 自动化验证设计。执行步骤如下：

1. **读取适配器配置**：从第1章获取环境变量和路由映射
2. **填充路由**：将每个测试用例中的 `{RES-XXX}` 替换为实际路由
3. **构造请求**：根据功能契约构造 HTTP 请求
4. **执行验证**：根据验证逻辑判定通过/失败
5. **记录结果**：按结果模板记录

### 3.2 路由替换规则

测试用例中使用 `{RES-XXX}` 标记引用功能资源，执行时替换规则：

```
{RES-HEALTH} → ${BASE_URL}/health
{RES-PROVIDER-LIST} → ${BASE_URL}${API_PREFIX}/providers
{RES-SCAN-DETAIL(id=123)} → ${BASE_URL}${API_PREFIX}/scans/123
```

如新系统路由已填写在映射表中，使用新系统路由；否则使用原始路由。

### 3.3 验证判定标准

| 判定 | 条件 |
|------|------|
| ✅ 通过 | 预期结果完全匹配实际行为 |
| ⚠️ 需关注 | 核心功能正常但存在非关键偏差（如响应格式不同但语义一致） |
| ❌ 失败 | 预期结果与实际行为不符 |
| ⏭️ 跳过 | 前置条件不满足（如Docker不可用） |

### 3.4 通用验证问题

对每个测试用例，LLM应依次回答以下问题：

1. **可达性**：请求是否返回了有效响应（非网络错误）？
2. **状态码**：HTTP状态码是否符合预期？
3. **语义正确性**：响应内容是否包含预期的数据/结构？
4. **副作用**：操作是否产生了预期的状态变化？
5. **幂等性**：重复执行是否产生一致的结果（GET请求）？

---

## 4. 核心业务流程验证（P0）

### 4.1 扫描生命周期流程

**流程意图**：验证从创建扫描到查看结果的完整业务闭环。

#### TC-FLOW-001: 创建扫描任务

- 功能域: 扫描引擎
- 操作意图: 提交一个有效的扫描目标，启动安全扫描
- 前置状态: 系统运行中，至少一个LLM提供商已连接
- 操作步骤:
  1. 向 `{RES-AGENT-RUN}` 发送 POST 请求，body 包含 `target`(有效URL) 和 `mode`(操作模式)
- 预期结果:
  - 返回 2xx 状态码
  - 响应包含新创建的代理/扫描标识符
  - 系统开始执行扫描任务
- 验证方法:
  - 检查响应状态码为 2xx
  - 检查响应体包含唯一标识符（id/agent_id/scan_id）
  - 后续通过 `{RES-AGENT-STATUS(id)}` 可查询到该代理状态为 running
- 失败判定: 返回 4xx/5xx，或响应不包含标识符

#### TC-FLOW-002: 查询代理执行状态

- 功能域: 代理系统
- 操作意图: 实时获取正在执行的代理状态
- 前置状态: 存在一个状态为 running 的代理
- 操作步骤:
  1. 向 `{RES-AGENT-STATUS(id)}` 发送 GET 请求
- 预期结果:
  - 返回 2xx 状态码
  - 响应包含代理状态（running/paused/stopped/completed/failed）
  - 响应包含当前执行阶段和进度信息
- 验证方法:
  - 检查响应包含 status 字段
  - 检查 status 值为有效状态枚举之一
- 失败判定: 返回 404（代理不存在），或 status 值不在有效枚举中

#### TC-FLOW-003: 暂停代理

- 功能域: 代理系统
- 操作意图: 暂停正在执行的代理
- 前置状态: 存在一个状态为 running 的代理
- 操作步骤:
  1. 向 `{RES-AGENT-PAUSE(id)}` 发送 POST 请求
- 预期结果:
  - 返回 2xx 状态码
  - 代理状态变为 paused
- 验证方法:
  - 操作后查询 `{RES-AGENT-STATUS(id)}`，status 应为 paused
- 失败判定: 代理状态未变为 paused

#### TC-FLOW-004: 恢复代理

- 功能域: 代理系统
- 操作意图: 恢复已暂停的代理
- 前置状态: 存在一个状态为 paused 的代理
- 操作步骤:
  1. 向 `{RES-AGENT-RESUME(id)}` 发送 POST 请求
- 预期结果:
  - 返回 2xx 状态码
  - 代理状态变为 running
- 验证方法:
  - 操作后查询 `{RES-AGENT-STATUS(id)}`，status 应为 running
- 失败判定: 代理状态未变为 running

#### TC-FLOW-005: 停止代理

- 功能域: 代理系统
- 操作意图: 终止代理执行
- 前置状态: 存在一个状态为 running 或 paused 的代理
- 操作步骤:
  1. 向 `{RES-AGENT-STOP(id)}` 发送 POST 请求
- 预期结果:
  - 返回 2xx 状态码
  - 代理状态变为 stopped
- 验证方法:
  - 操作后查询 `{RES-AGENT-STATUS(id)}`，status 应为 stopped
- 失败判定: 代理状态未变为 stopped

#### TC-FLOW-006: 查看扫描详情

- 功能域: 扫描引擎
- 操作意图: 获取已完成扫描的完整信息
- 前置状态: 存在一个已完成的扫描
- 操作步骤:
  1. 向 `{RES-SCAN-DETAIL(id)}` 发送 GET 请求
- 预期结果:
  - 返回 2xx 状态码
  - 响应包含扫描目标、状态、创建时间、漏洞数等基本信息
- 验证方法:
  - 检查响应包含 target_url、status、created_at 等字段
- 失败判定: 缺少核心信息字段

#### TC-FLOW-007: 查看扫描发现的漏洞

- 功能域: 漏洞管理
- 操作意图: 获取扫描发现的漏洞列表
- 前置状态: 存在一个有漏洞发现的扫描
- 操作步骤:
  1. 向 `{RES-SCAN-VULNS(id)}` 发送 GET 请求
- 预期结果:
  - 返回 2xx 状态码
  - 响应包含漏洞列表，每个漏洞有严重级别、类型、URL
- 验证方法:
  - 检查响应包含漏洞数组
  - 检查漏洞对象包含 severity/type/url 字段
- 失败判定: 响应不包含漏洞列表结构

#### TC-FLOW-008: 查看扫描发现的端点

- 功能域: 扫描引擎
- 操作意图: 获取扫描发现的端点列表
- 前置状态: 存在一个有端点发现的扫描
- 操作步骤:
  1. 向 `{RES-SCAN-ENDPOINTS(id)}` 发送 GET 请求
- 预期结果:
  - 返回 2xx 状态码
  - 响应包含端点列表，每个端点有HTTP方法、路径、状态码
- 验证方法:
  - 检查响应包含端点数组
  - 检查端点对象包含 method/path/status_code 字段
- 失败判定: 响应不包含端点列表结构

#### TC-FLOW-009: 验证漏洞

- 功能域: 漏洞管理
- 操作意图: 对发现的漏洞进行人工验证判定
- 前置状态: 存在一个未验证的漏洞
- 操作步骤:
  1. 向 `{RES-VULN-VALIDATE(id)}` 发送 PATCH 请求，body 包含验证结果（confirmed/false_positive）
- 预期结果:
  - 返回 2xx 状态码
  - 漏洞验证状态更新
- 验证方法:
  - 操作后查询该漏洞，验证状态已变更
- 失败判定: 漏洞验证状态未变更

#### TC-FLOW-010: 生成扫描报告

- 功能域: 报告系统
- 操作意图: 为扫描结果生成报告
- 前置状态: 存在一个已完成的扫描
- 操作步骤:
  1. 向 `{RES-REPORT-CREATE}` 发送 POST 请求，body 包含 scan_id
- 预期结果:
  - 返回 2xx 状态码
  - 报告生成成功，返回报告标识符
- 验证方法:
  - 检查响应包含报告标识符
  - 后续可通过 `{RES-REPORT-VIEW(id)}` 查看报告
- 失败判定: 报告生成失败或无法查看

#### TC-FLOW-011: AI生成报告

- 功能域: 报告系统
- 操作意图: 使用AI为扫描结果生成智能分析报告
- 前置状态: 存在一个已完成的扫描，LLM提供商可用
- 操作步骤:
  1. 向 `{RES-REPORT-AI}` 发送 POST 请求，body 包含 scan_id 和可选的 provider/model
- 预期结果:
  - 返回 2xx 状态码
  - AI报告生成成功
- 验证方法:
  - 检查响应包含报告标识符
  - 报告内容包含AI分析文本
- 失败判定: AI报告生成失败

#### TC-FLOW-012: 查看和下载报告

- 功能域: 报告系统
- 操作意图: 查看报告内容并下载为文件
- 前置状态: 存在一个已生成的报告
- 操作步骤:
  1. 向 `{RES-REPORT-VIEW(id)}` 发送 GET 请求查看报告
  2. 向 `{RES-REPORT-DOWNLOAD(id, format)}` 发送 GET 请求下载报告（format 可为 html/json/pdf）
- 预期结果:
  - 查看返回 2xx，包含报告内容
  - 下载返回 2xx，Content-Disposition 包含文件名
- 验证方法:
  - 查看响应包含报告正文内容
  - 下载响应包含正确的 Content-Type 和文件内容
- 失败判定: 报告内容为空或下载失败

---

### 4.2 自动渗透流程

**流程意图**：验证一键自动渗透测试功能，系统自动协调多专家代理。

#### TC-FLOW-013: 启动自动渗透

- 功能域: 代理系统
- 操作意图: 提交目标URL启动自动渗透测试
- 前置状态: LLM提供商可用
- 操作步骤:
  1. 向 `{RES-AGENT-RUN}` 发送 POST 请求，mode 为 auto_pentest，包含目标URL
- 预期结果:
  - 返回 2xx 状态码
  - 创建多个并行代理会话（侦察、利用、验证等）
- 验证方法:
  - 检查响应包含代理标识符
  - 查询活跃代理列表，存在多个关联代理
- 失败判定: 只创建单个代理或创建失败

#### TC-FLOW-014: 查看渗透历史

- 功能域: 代理系统
- 操作意图: 查看已完成的渗透测试历史
- 前置状态: 存在已完成的渗透测试
- 操作步骤:
  1. 查询扫描列表，筛选 auto_pentest 类型的扫描
- 预期结果:
  - 返回历史记录列表
  - 每条记录包含目标、状态、发现数量
- 验证方法:
  - 检查列表非空
  - 检查记录包含必要字段
- 失败判定: 列表为空或缺少必要字段

---

### 4.3 实时任务流程

**流程意图**：验证AI对话式安全测试的完整交互。

#### TC-FLOW-015: 创建实时会话

- 功能域: 实时任务
- 操作意图: 创建一个新的实时AI对话会话
- 前置状态: LLM提供商可用
- 操作步骤:
  1. 向 `{RES-AGENT-REALTIME-SESSION}` 发送 POST 请求
- 预期结果:
  - 返回 2xx 状态码
  - 响应包含会话标识符
- 验证方法:
  - 检查响应包含 session_id 或 id
  - 后续可通过该ID发送消息
- 失败判定: 会话创建失败

#### TC-FLOW-016: 发送消息并获取AI回复

- 功能域: 实时任务
- 操作意图: 在实时会话中发送安全测试指令，获取AI分析回复
- 前置状态: 存在一个活跃的实时会话
- 操作步骤:
  1. 向 `{RES-AGENT-REALTIME-MSG(id)}` 发送 POST 请求，body 包含消息内容
- 预期结果:
  - 返回 2xx 状态码
  - AI返回分析结果或执行建议
- 验证方法:
  - 检查响应包含AI回复内容
  - 回复内容与用户消息语义相关
- 失败判定: 无AI回复或回复与消息无关

#### TC-FLOW-017: 查询工具和LLM状态

- 功能域: 实时任务
- 操作意图: 查看可用安全工具和LLM连接状态
- 前置状态: 实时会话存在
- 操作步骤:
  1. 向 `{RES-AGENT-REALTIME-TOOLS}` 发送 GET 请求
  2. 向 `{RES-AGENT-REALTIME-LLM}` 发送 GET 请求
- 预期结果:
  - 工具状态返回可用工具列表及各工具状态
  - LLM状态返回连接是否可用
- 验证方法:
  - 工具状态包含至少一个工具条目
  - LLM状态包含 available=true/false
- 失败判定: 工具列表为空或LLM状态不可查询

#### TC-FLOW-018: 生成实时报告

- 功能域: 实时任务
- 操作意图: 为当前实时会话生成总结报告
- 前置状态: 实时会话中有对话历史
- 操作步骤:
  1. 向 `{RES-AGENT-REALTIME-REPORT(id)}` 发送 GET 请求
- 预期结果:
  - 返回 2xx 状态码
  - 响应包含报告内容
- 验证方法:
  - 检查响应包含报告数据
- 失败判定: 报告为空或生成失败

---

### 4.4 漏洞实验室流程

**流程意图**：验证漏洞专项测试的挑战模式。

#### TC-FLOW-019: 启动漏洞挑战

- 功能域: 漏洞实验室
- 操作意图: 针对特定漏洞类型启动测试挑战
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-VULNLAB-RUN}` 发送 POST 请求，body 包含漏洞类型和目标
- 预期结果:
  - 返回 2xx 状态码
  - 创建挑战，返回挑战标识符
- 验证方法:
  - 检查响应包含挑战标识符
  - 挑战列表中出现新挑战
- 失败判定: 挑战创建失败

#### TC-FLOW-020: 管理挑战生命周期

- 功能域: 漏洞实验室
- 操作意图: 停止和删除漏洞挑战
- 前置状态: 存在一个运行中的挑战
- 操作步骤:
  1. 向 `{RES-VULNLAB-STOP(id)}` 发送 POST 请求停止挑战
  2. 向 `{RES-VULNLAB-DELETE(id)}` 发送 DELETE 请求删除挑战
- 预期结果:
  - 停止操作后挑战状态变为 stopped
  - 删除操作后挑战从列表中移除
- 验证方法:
  - 停止后查询挑战列表，该挑战状态为 stopped
  - 删除后查询挑战列表，该挑战不存在
- 失败判定: 挑战状态未变更或删除后仍存在

---

### 4.5 终端代理流程

**流程意图**：验证命令行交互式安全测试。

#### TC-FLOW-021: 终端会话交互

- 功能域: 终端代理
- 操作意图: 创建终端会话并执行命令
- 前置状态: LLM提供商可用
- 操作步骤:
  1. 向 `{RES-TERMINAL-SESSIONS}` 发送 POST 请求创建会话
  2. 向 `{RES-TERMINAL-EXEC(id)}` 发送 POST 请求执行命令
  3. 向 `{RES-TERMINAL-AI(id)}` 发送 POST 请求获取AI建议
- 预期结果:
  - 会话创建成功，返回会话ID
  - 命令执行返回输出结果
  - AI返回下一步建议
- 验证方法:
  - 检查每步返回 2xx 状态码
  - 命令输出非空
  - AI建议与命令上下文相关
- 失败判定: 任一步骤返回错误

---

### 4.6 仪表板流程

**流程意图**：验证全局概览数据的正确性。

#### TC-FLOW-022: 仪表板数据完整性

- 功能域: 仪表板
- 操作意图: 验证仪表板统计数据与实际数据一致
- 前置状态: 系统中存在扫描数据
- 操作步骤:
  1. 向 `{RES-DASHBOARD-STATS}` 发送 GET 请求
  2. 向 `{RES-DASHBOARD-RECENT}` 发送 GET 请求
  3. 向 `{RES-DASHBOARD-ACTIVITY}` 发送 GET 请求
- 预期结果:
  - 统计数据包含扫描数、漏洞数、代理数等计数
  - 最近扫描列表按时间倒序
  - 活动日志包含系统操作记录
- 验证方法:
  - 统计数值与实际查询结果一致
  - 最近扫描列表非空（如有历史数据）
  - 活动日志条目包含时间戳和操作类型
- 失败判定: 统计数值与实际不符，或列表排序错误

#### TC-FLOW-023: 活动日志过滤

- 功能域: 仪表板
- 操作意图: 验证活动日志可按类型过滤
- 前置状态: 系统有活动日志
- 操作步骤:
  1. 向 `{RES-DASHBOARD-ACTIVITY}` 发送 GET 请求，附带 type 过滤参数
- 预期结果:
  - 只返回匹配类型的活动记录
  - 不同类型参数返回不同子集
- 验证方法:
  - 过滤后的日志条目类型与过滤条件一致
- 失败判定: 过滤无效或返回不匹配的记录

---

## 5. 配置管理流程验证（P1）

### 5.1 提供商管理流程

**流程意图**：验证LLM提供商的完整管理生命周期。

#### TC-CONF-001: 查询提供商列表

- 功能域: 提供商管理
- 操作意图: 获取所有已注册的LLM提供商
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-PROVIDER-LIST}` 发送 GET 请求
- 预期结果:
  - 返回 2xx 状态码
  - 响应包含提供商列表
  - 每个提供商包含 id/name/auth_type/tier/connected/enabled 字段
- 验证方法:
  - 检查列表非空
  - 检查每个提供商包含必要字段
  - auth_type 为 oauth 或 api_key
  - tier 为正整数
- 失败判定: 列表为空或缺少必要字段

#### TC-CONF-002: 查询提供商状态

- 功能域: 提供商管理
- 操作意图: 获取提供商的连接状态和配额信息
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-PROVIDER-STATUS}` 发送 GET 请求
- 预期结果:
  - 返回 2xx 状态码
  - 响应包含各提供商的连接状态和Token使用量
- 验证方法:
  - 检查响应包含 enabled/total_requests/total_tokens 等统计字段
- 失败判定: 缺少统计字段

#### TC-CONF-003: 添加提供商凭据

- 功能域: 提供商管理
- 操作意图: 为API Key类型提供商添加认证凭据
- 前置状态: 存在一个 auth_type=api_key 的提供商
- 操作步骤:
  1. 向 `{RES-PROVIDER-CONNECT(id)}` 发送 POST 请求，body 包含 label 和 credential
- 预期结果:
  - credential 非空时返回 2xx，账户创建成功
  - credential 为空时应返回 4xx（输入验证错误）
- 验证方法:
  - 有效凭据：检查响应包含 account_id
  - 空凭据：检查返回 4xx 或错误信息
- 失败判定: 空凭据被接受（BUG），或有效凭据创建失败

#### TC-CONF-004: 测试提供商连接

- 功能域: 提供商管理
- 操作意图: 验证提供商账户的API连接是否正常
- 前置状态: 提供商有至少一个账户
- 操作步骤:
  1. 向 `{RES-PROVIDER-TEST(pid, aid)}` 发送 POST 请求
- 预期结果:
  - 有效账户：返回 success=true
  - 无效账户：返回 success=false 并包含错误信息
- 验证方法:
  - 检查响应包含 success 字段
  - 成功时检查无错误信息
  - 失败时检查包含可读的错误描述
- 失败判定: 无法区分成功/失败，或错误信息不可读

#### TC-CONF-005: 启用/禁用提供商

- 功能域: 提供商管理
- 操作意图: 切换提供商的启用状态
- 前置状态: 存在一个已启用的提供商
- 操作步骤:
  1. 向 `{RES-PROVIDER-TOGGLE(id)}` 发送 POST 请求，body 包含 enabled=false
  2. 再次发送 enabled=true 恢复
- 预期结果:
  - 禁用后提供商 enabled=false
  - 恢复后提供商 enabled=true
- 验证方法:
  - 操作后查询 `{RES-PROVIDER-LIST}`，检查目标提供商的 enabled 字段
- 失败判定: enabled 字段未变更

#### TC-CONF-006: 检测CLI令牌

- 功能域: 提供商管理
- 操作意图: 自动检测本地CLI工具的认证令牌
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-PROVIDER-DETECT-ALL}` 发送 POST 请求
- 预期结果:
  - 返回 2xx 状态码
  - 响应包含 detected_count（检测到的令牌数）
- 验证方法:
  - 检查响应包含 detected_count 字段
  - detected_count >= 0
- 失败判定: 缺少 detected_count 或请求失败

#### TC-CONF-007: 删除提供商账户

- 功能域: 提供商管理
- 操作意图: 删除提供商下的指定账户
- 前置状态: 提供商有至少一个账户
- 操作步骤:
  1. 向 `{RES-PROVIDER-ACCT-DEL(pid, aid)}` 发送 DELETE 请求
- 预期结果:
  - 返回 2xx 状态码
  - 账户从提供商账户列表中移除
- 验证方法:
  - 操作后查询提供商详情，该账户不再存在
- 失败判定: 账户仍存在

#### TC-CONF-008: 环境变量管理

- 功能域: 提供商管理
- 操作意图: 查询和修改系统环境变量（仅限白名单键）
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-PROVIDER-ENV}` 发送 GET 请求查询
  2. 向 `{RES-PROVIDER-ENV}` 发送 POST 请求修改白名单内的键
  3. 向 `{RES-PROVIDER-ENV}` 发送 POST 请求修改白名单外的键
- 预期结果:
  - GET 返回环境变量列表和允许的键白名单
  - 修改白名单内键返回成功
  - 修改白名单外键返回错误（拒绝修改）
- 验证方法:
  - GET 响应包含 allowed_keys 列表
  - 白名单内键修改后值已更新
  - 白名单外键返回 4xx 或包含拒绝信息
- 失败判定: 白名单外键被接受（安全漏洞）

#### TC-CONF-009: Smart Router 路由验证

- 功能域: 提供商管理
- 操作意图: 验证 Smart Router 的多提供商优先级和故障转移
- 前置状态: 配置了多个不同 Tier 的提供商
- 操作步骤:
  1. 确认 Tier 1 提供商已连接
  2. 发起LLM请求，验证使用 Tier 1 提供商
  3. 禁用 Tier 1 提供商，再次发起请求
  4. 验证自动切换到 Tier 2 提供商
- 预期结果:
  - 优先使用高 Tier 提供商
  - 高 Tier 不可用时自动降级
- 验证方法:
  - 检查请求日志或Token使用量变化
  - 禁用后请求仍能成功（故障转移）
- 失败判定: 禁用高Tier后请求全部失败

---

### 5.2 系统设置流程

#### TC-CONF-010: 查询和修改系统设置

- 功能域: 系统配置
- 操作意图: 获取和更新全局配置
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-SETTINGS}` 发送 GET 请求
  2. 向 `{RES-SETTINGS}` 发送 PUT 请求修改配置
- 预期结果:
  - GET 返回当前配置（LLM提供商、模型、功能开关等）
  - PUT 修改后配置生效
- 验证方法:
  - GET 响应包含 llm_provider/model 等字段
  - PUT 后再次 GET，值已更新
- 失败判定: 配置未生效或GET缺少必要字段

#### TC-CONF-011: 通知渠道测试

- 功能域: 系统配置
- 操作意图: 测试通知渠道连通性
- 前置状态: 已配置通知渠道（Discord/Telegram/WhatsApp）
- 操作步骤:
  1. 向 `{RES-SETTINGS-NOTIFY-TEST(channel)}` 发送 POST 请求
- 预期结果:
  - 已配置渠道返回测试结果（成功/失败）
  - 未配置渠道返回配置缺失提示
- 验证方法:
  - 检查响应包含测试结果
- 失败判定: 无法区分已配置/未配置

---

### 5.3 调度任务流程

#### TC-CONF-012: 调度任务CRUD

- 功能域: 调度系统
- 操作意图: 创建/暂停/恢复/删除调度任务
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-SCHEDULER-CREATE}` 发送 POST 请求创建调度
  2. 向 `{RES-SCHEDULER-LIST}` 发送 GET 请求查询列表
  3. 向 `{RES-SCHEDULER-PAUSE(id)}` 发送 POST 请求暂停
  4. 向 `{RES-SCHEDULER-RESUME(id)}` 发送 POST 请求恢复
  5. 向 `{RES-SCHEDULER-DELETE(id)}` 发送 DELETE 请求删除
- 预期结果:
  - 创建成功返回调度标识符
  - 列表包含新创建的调度
  - 暂停后状态为 paused
  - 恢复后状态为 active
  - 删除后列表中不存在
- 验证方法:
  - 每步操作后查询列表验证状态
- 失败判定: 状态转换不正确

---

### 5.4 MCP 服务器管理流程

#### TC-CONF-013: MCP服务器CRUD

- 功能域: MCP集成
- 操作意图: 添加/启动/停止/删除MCP服务器
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-MCP-SERVERS}` 发送 POST 请求添加服务器
  2. 向 `{RES-MCP-START(id)}` 发送 POST 请求启动
  3. 向 `{RES-MCP-TOOLS(id)}` 发送 GET 请求查看工具
  4. 向 `{RES-MCP-STOP(id)}` 发送 POST 请求停止
  5. 向 `{RES-MCP-DELETE(id)}` 发送 DELETE 请求删除
- 预期结果:
  - 添加成功返回服务器配置
  - 启动后状态为 running
  - 工具列表包含该服务器提供的工具
  - 停止后状态为 stopped
  - 删除后列表中不存在
- 验证方法:
  - 每步操作后验证状态变更
- 失败判定: 状态转换不正确

---

## 6. 资源管理流程验证（P1）

### 6.1 知识库管理

#### TC-RES-001: 知识库文档管理

- 功能域: 知识增强
- 操作意图: 上传/查询/删除知识文档
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-KNOWLEDGE-STATS}` 发送 GET 请求查看统计
  2. 向 `{RES-KNOWLEDGE-UPLOAD}` 发送 POST 请求上传文档
  3. 向 `{RES-KNOWLEDGE-DOCS}` 发送 GET 请求查询文档列表
  4. 向 `{RES-KNOWLEDGE-DELETE(id)}` 发送 DELETE 请求删除文档
- 预期结果:
  - 统计包含文档数和条目数
  - 上传成功后文档出现在列表中
  - 删除后文档从列表中移除
  - 统计数值相应更新
- 验证方法:
  - 上传前后对比统计数值
  - 删除前后对比文档列表
- 失败判定: 上传后文档未出现或删除后仍存在

### 6.2 沙箱管理

#### TC-RES-002: 沙箱容器管理

- 功能域: 沙箱执行
- 操作意图: 查询/销毁/清理沙箱容器
- 前置状态: Docker服务可用
- 操作步骤:
  1. 向 `{RES-SANDBOX-LIST}` 发送 GET 请求查看容器列表
  2. 向 `{RES-SANDBOX-DESTROY(id)}` 发送 DELETE 请求销毁容器
  3. 向 `{RES-SANDBOX-CLEANUP}` 发送 POST 请求清理过期容器
- 预期结果:
  - 列表包含容器信息（状态、关联扫描、创建时间）
  - 销毁后容器从列表移除
  - 清理操作移除过期容器
- 验证方法:
  - 操作前后对比容器列表
- 失败判定: 容器状态不正确或操作无效

### 6.3 任务库管理

#### TC-RES-003: 任务模板管理

- 功能域: 代理系统
- 操作意图: 查询/创建/删除任务模板
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-AGENT-TASKS}` 发送 GET 请求查询任务列表
  2. 创建自定义任务（POST）
  3. 删除自定义任务（DELETE）
- 预期结果:
  - 列表包含预定义和自定义任务
  - 自定义任务创建后出现在列表中
  - 预定义任务不可删除
- 验证方法:
  - 检查列表包含 is_preset 或类似字段区分类型
  - 删除预定义任务返回错误
- 失败判定: 无法区分任务类型或预定义任务被删除

### 6.4 提示词管理

#### TC-RES-004: 提示词CRUD

- 功能域: 提示词管理
- 操作意图: 创建/查询/更新/删除提示词
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-PROMPT-LIST}` 发送 GET 请求
  2. 向 `{RES-PROMPT-CREATE}` 发送 POST 请求创建
  3. 向 `{RES-PROMPT-UPDATE(id)}` 发送 PUT 请求更新
  4. 向 `{RES-PROMPT-DELETE(id)}` 发送 DELETE 请求删除
- 预期结果:
  - 每步操作返回正确状态码
  - 创建后提示词出现在列表中
  - 更新后内容已变更
  - 删除后提示词不存在
- 验证方法:
  - 每步操作后查询列表验证
- 失败判定: CRUD操作不完整

---

## 7. 异常与边界场景验证（P2）

### 7.1 输入验证

#### TC-ERR-001: 空值和无效输入

- 功能域: 跨域
- 操作意图: 验证系统对空值和无效输入的防护
- 操作步骤:
  1. 向 `{RES-AGENT-RUN}` 发送空 target 字符串
  2. 向 `{RES-PROVIDER-CONNECT(id)}` 发送空 credential
  3. 向 `{RES-KNOWLEDGE-UPLOAD}` 上传非支持格式文件
- 预期结果:
  - 每种情况应返回 4xx 错误
  - 错误信息清晰描述问题
  - 不应创建无效资源
- 验证方法:
  - 检查返回 4xx 状态码
  - 检查无效资源未被创建
- 失败判定: 空值被接受（BUG），系统崩溃

#### TC-ERR-002: 特殊字符和注入

- 功能域: 跨域
- 操作意图: 验证系统对XSS和注入攻击的防护
- 操作步骤:
  1. 在输入框提交 `<script>alert(1)</script>`
  2. 在搜索框提交 `' OR 1=1 --`
  3. 在环境变量编辑器提交非白名单键
- 预期结果:
  - XSS脚本不执行，正确转义
  - SQL注入不影响数据
  - 环境变量白名单阻止非授权修改
- 验证方法:
  - 检查响应不包含可执行脚本
  - 检查数据完整性未受影响
  - 检查白名单外键被拒绝
- 失败判定: 脚本执行、数据被篡改、白名单被绕过

### 7.2 资源不存在

#### TC-ERR-003: 访问不存在的资源

- 功能域: 跨域
- 操作意图: 验证系统对不存在资源的处理
- 操作步骤:
  1. 请求不存在的扫描ID
  2. 请求不存在的报告ID
  3. 请求不存在的代理ID
- 预期结果:
  - 返回 404 状态码
  - 错误信息包含资源类型描述
- 验证方法:
  - 检查 HTTP 状态码为 404
  - 检查错误信息可读
- 失败判定: 返回 500 或无错误信息

### 7.3 服务异常

#### TC-ERR-004: 依赖服务不可用

- 功能域: 跨域
- 操作意图: 验证系统在依赖服务不可用时的降级行为
- 操作步骤:
  1. 停止后端服务后操作前端
  2. 使用无效LLM端点发起请求
  3. Docker不可用时启动沙箱扫描
- 预期结果:
  - 前端显示友好的服务不可用提示
  - LLM请求超时后返回可读错误
  - 沙箱操作返回Docker不可用提示
- 验证方法:
  - 检查错误提示用户可读
  - 检查系统不崩溃
- 失败判定: 系统崩溃或错误信息不可读

### 7.4 并发和重复

#### TC-ERR-005: 并发操作

- 功能域: 跨域
- 操作意图: 验证系统对并发和重复操作的处理
- 操作步骤:
  1. 快速连续点击同一按钮（重复提交）
  2. 同时在两个窗口编辑同一设置
- 预期结果:
  - 不产生重复资源
  - 最后操作生效，不产生数据冲突
- 验证方法:
  - 检查资源数量未异常增长
  - 检查数据一致性
- 失败判定: 产生重复资源或数据冲突

---

## 8. 测试结果记录

### 8.1 结果记录模板

| TC-ID | 执行日期 | 结果 | 实际行为 | 偏差说明 |
|-------|----------|------|----------|----------|
| TC-FLOW-001 | | ✅/⚠️/❌/⏭️ | | |

### 8.2 缺陷记录模板

| 缺陷编号 | 严重级别 | 关联TC-ID | 描述 | 复现步骤 | 状态 |
|----------|----------|-----------|------|----------|------|
| BUG-XXX | S1/S2/S3/S4 | TC-XXX | | | 开放/已修复 |

### 8.3 严重级别定义

| 级别 | 定义 | 判定标准 |
|------|------|----------|
| S1-致命 | 核心功能完全不可用 | 核心流程无法完成，无替代方案 |
| S2-严重 | 核心功能异常 | 核心流程可完成但有明显缺陷，或有替代方案 |
| S3-一般 | 非核心功能异常 | 不影响核心流程，体验受损 |
| S4-轻微 | UI/体验问题 | 功能正常，显示或交互有瑕疵 |

---

## 附录A: 原始v3.2.4实际测试结果

### A.1 测试执行概况

| 项目 | 信息 |
|------|------|
| 执行日期 | 2026-05-19 |
| 后端版本 | NeuroSploit v3.2.4 |
| LLM配置 | Minimax (MiniMax-M2.7), Smart Router 已启用 |
| Docker | 不可用（沙箱环境限制） |

### A.2 测试结果统计

| 分类 | 通过 | 需关注 | 通过率 |
|------|------|--------|--------|
| 前置条件 | 5 | 1 | 83% |
| 配置管理 | 14 | 1 | 93% |
| 核心业务 | 15 | 5 | 75% |
| 资源管理 | 6 | 0 | 100% |
| 交互通信 | 2 | 2 | 50% |
| 报告数据 | 1 | 0 | 100% |
| 异常边界 | 4 | 3 | 57% |

### A.3 发现的缺陷

| 缺陷编号 | 级别 | 描述 |
|----------|------|------|
| BUG-001 | S2 | 空 target 被接受，可创建无目标的扫描代理 |
| BUG-002 | S2 | 空 API Key 被接受为有效凭据 |
| BUG-003 | S3 | targets 路由未注册（404） |
| BUG-004 | S3 | vulnerabilities 路由未注册（404） |
| BUG-005 | S3 | vuln-lab/categories 路由未注册（404） |
| BUG-006 | S3 | full-ia/status 路由未注册（404） |
| BUG-007 | S4 | Scheduler 创建请求体 schema 与文档不一致 |

### A.4 API响应格式参考

以下为v3.2.4实际的API响应格式，供新系统适配参考：

| 功能资源 | 实际响应格式 |
|----------|-------------|
| RES-SCAN-LIST | `{"scans": [...], "total": N}` |
| RES-AGENT-ACTIVE | `{"agents": [...]}` |
| RES-DASHBOARD-RECENT | `{"scans": [...]}` |
| RES-DASHBOARD-ACTIVITY | `{"activities": [...]}` |
| RES-REPORT-LIST | `{"reports": [...], "total": N}` |
| RES-VULNLAB-CHALLENGES | `{"challenges": [...], "total": N}` |
| RES-PROVIDER-LIST | `{"providers": [...], "enabled": bool}` |
| RES-PROVIDER-STATUS | `{"enabled": bool, "total_requests": N, "total_tokens": N}` |
| RES-PROVIDER-ENV | `{"env_vars": {...}, "allowed_keys": [...]}` |
| RES-SANDBOX-LIST | `{"active": N, "max_concurrent": N, "image": "..."}` |
| RES-KNOWLEDGE-STATS | `{"total_documents": N, "total_entries": N}` |
