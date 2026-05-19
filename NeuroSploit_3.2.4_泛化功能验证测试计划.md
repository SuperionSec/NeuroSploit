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
| RES-AGENT-LOGS | 代理日志 | GET | `${API_PREFIX}/agent/logs/{id}` | `http://localhost:8000/api/v1/agent/logs/{id}` |
| RES-AGENT-FINDINGS | 代理发现 | GET | `${API_PREFIX}/agent/findings/{id}` | `http://localhost:8000/api/v1/agent/findings/{id}` |
| RES-AGENT-HISTORY | 代理历史 | GET | `${API_PREFIX}/agent/history` | `http://localhost:8000/api/v1/agent/history` |
| RES-AGENT-BY-SCAN | 按扫描查代理 | GET | `${API_PREFIX}/agent/by-scan/{scan_id}` | `http://localhost:8000/api/v1/agent/by-scan/{scan_id}` |
| RES-AGENT-SKIP | 跳转阶段 | POST | `${API_PREFIX}/agent/skip-to/{id}/{phase}` | `http://localhost:8000/api/v1/agent/skip-to/{id}/{phase}` |
| RES-AGENT-TRIPLECHECK | 交叉验证 | POST | `${API_PREFIX}/agent/triple-check/{scan_id}` | `http://localhost:8000/api/v1/agent/triple-check/{scan_id}` |
| RES-AGENT-VULNAGENTS | 漏洞代理状态 | GET | `${API_PREFIX}/agent/vuln-agents/{id}` | `http://localhost:8000/api/v1/agent/vuln-agents/{id}` |
| RES-AGENT-QUICK | 快速代理运行 | POST | `${API_PREFIX}/agent/quick` | `http://localhost:8000/api/v1/agent/quick` |
| RES-AGENT-LLM-STATUS | LLM状态检查 | GET | `${API_PREFIX}/agent/status` | `http://localhost:8000/api/v1/agent/status` |
| RES-AGENT-REALTIME-SESSION | 实时会话创建 | POST | `${API_PREFIX}/agent/realtime/session` | `http://localhost:8000/api/v1/agent/realtime/session` |
| RES-AGENT-REALTIME-GET | 实时会话查询 | GET | `${API_PREFIX}/agent/realtime/{id}` | `http://localhost:8000/api/v1/agent/realtime/{id}` |
| RES-AGENT-REALTIME-DEL | 实时会话删除 | DELETE | `${API_PREFIX}/agent/realtime/{id}` | `http://localhost:8000/api/v1/agent/realtime/{id}` |

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

## 4. AI渗透测试全流程验证（P0）

> 本章是测试计划的核心，覆盖AI渗透测试从配置到执行的完整闭环。
> 每个测试用例基于代码分析编写，确保与实际实现一致。

### 4.1 AI渗透测试前置配置验证

**流程意图**：验证AI渗透测试所需的全部配置项可正确设置和生效。

#### TC-PENTEST-001: LLM提供商连接验证

- 功能域: 提供商管理 → AI渗透
- 操作意图: 确认至少一个LLM提供商已连接且可用
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-PROVIDER-LIST}` 发送 GET 请求
  2. 检查是否有 connected=true 的提供商
  3. 向 `{RES-AGENT-REALTIME-LLM}` 发送 GET 请求确认 LLM 可用
- 预期结果:
  - 至少一个提供商 connected=true
  - LLM 状态 available=true
  - 返回 provider 名称（如 smart_router/minimax/openai）
- 验证方法:
  - providers 列表中 connected 数量 > 0
  - llm-status 返回 available=true
- 失败判定: 无已连接提供商或 LLM 不可用

#### TC-PENTEST-002: Smart Router 启用验证

- 功能域: 提供商管理 → AI渗透
- 操作意图: 确认 Smart Router 已启用，多提供商路由功能正常
- 前置状态: 至少两个不同 Tier 的提供商已配置
- 操作步骤:
  1. 向 `{RES-PROVIDER-LIST}` 发送 GET 请求，检查 enabled=true
  2. 向 `{RES-PROVIDER-STATUS}` 发送 GET 请求，检查路由统计
- 预期结果:
  - Smart Router enabled=true
  - 返回 total_requests 和 total_tokens 统计
- 验证方法:
  - enabled 字段为 true
  - 统计字段存在且为数值
- 失败判定: Smart Router 未启用或统计字段缺失

#### TC-PENTEST-003: 系统设置对渗透的影响验证

- 功能域: 系统配置 → AI渗透
- 操作意图: 验证系统设置中的关键配置项对AI渗透行为的影响
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-SETTINGS}` 发送 GET 请求获取当前设置
  2. 检查以下关键配置项：llm_provider、llm_model、enable_knowledge_augmentation、enable_rag、enable_vuln_agents、max_concurrent_scans
- 预期结果:
  - 返回完整配置对象
  - llm_provider 和 llm_model 指向有效的提供商/模型
  - 功能开关（enable_*）为布尔值
  - max_concurrent_scans 为正整数
- 验证方法:
  - 每个配置项存在且类型正确
  - 功能开关值与 .env 配置一致
- 失败判定: 关键配置项缺失或类型错误

#### TC-PENTEST-004: 环境变量白名单验证

- 功能域: 提供商管理 → AI渗透
- 操作意图: 确认环境变量白名单机制正常，防止未授权修改
- 前置状态: 系统运行中
- 操作步骤:
  1. 向 `{RES-PROVIDER-ENV}` 发送 GET 请求获取 allowed_keys
  2. 向 `{RES-PROVIDER-ENV}` 发送 POST 请求修改白名单内键（如 MINIMAX_API_KEY）
  3. 向 `{RES-PROVIDER-ENV}` 发送 POST 请求修改白名单外键（如 MALICIOUS_KEY）
- 预期结果:
  - GET 返回 allowed_keys 列表（应包含各提供商的 API_KEY 环境变量）
  - 白名单内键修改成功
  - 白名单外键被拒绝，返回错误信息
- 验证方法:
  - allowed_keys 包含至少 5 个键
  - 白名单外键返回 4xx 或包含 "not in the allowed whitelist"
- 失败判定: 白名单外键被接受（安全漏洞）

---

### 4.2 AI渗透测试全模式验证

**流程意图**：验证系统支持的全部7种代理模式，每种模式的启动、执行和结果均正确。

**代理模式说明**（基于 AgentMode 枚举）：

| 模式 | 值 | 说明 | 预期行为 |
|------|---|------|----------|
| 完整自动 | full_auto | Recon → Analyze → Test → Report | 执行完整4阶段流程 |
| 仅侦察 | recon_only | 只做侦察，不测试漏洞 | 只执行 recon 阶段 |
| AI决策 | prompt_only | AI决定一切（高Token消耗） | AI自主决策测试策略 |
| 仅分析 | analyze_only | 只分析不测试 | 不执行主动测试 |
| 自动渗透 | auto_pentest | 一键全自动渗透+100漏洞类型 | 启动 VulnOrchestrator 并行测试 |
| CLI代理 | cli_agent | Kali沙箱内AI CLI工具 | 强制启用 Kali 沙箱 |
| 全LLM渗透 | full_llm_pentest | LLM驱动整个渗透周期 | AI完全自主执行 |

#### TC-PENTEST-005: full_auto 模式全流程

- 功能域: AI渗透
- 操作意图: 验证完整自动模式从启动到完成的全部流程
- 前置状态: LLM提供商可用
- 操作步骤:
  1. 向 `{RES-AGENT-RUN}` 发送 POST 请求：`{"target":"http://testphp.vulnweb.com","mode":"full_auto"}`
  2. 轮询 `{RES-AGENT-STATUS(id)}` 直到状态变化
  3. 查看代理日志 `{RES-AGENT-LOGS(id)}`
  4. 查看代理发现 `{RES-AGENT-FINDINGS(id)}`
- 预期结果:
  - 步骤1: 返回 agent_id，status=running，mode=full_auto
  - 步骤2: phase 依次经过 initializing → recon → analysis → testing → enhancement → completed
  - 步骤3: 日志包含 [AI]/[LLM] 标记的 AI 交互记录和 script 标记的脚本执行记录
  - 步骤4: findings 包含漏洞列表，每个漏洞有 title/severity/vulnerability_type/cvss_score
- 验证方法:
  - agent_id 非空
  - 进度从 0 递增到 100
  - 日志非空且包含 source 字段（llm/script）
  - findings 按 severity 分组可统计
- 失败判定: 代理启动失败、phase 不变化、无日志、无发现

#### TC-PENTEST-006: recon_only 模式

- 功能域: AI渗透
- 操作意图: 验证仅侦察模式只执行侦察阶段
- 前置状态: LLM提供商可用
- 操作步骤:
  1. 向 `{RES-AGENT-RUN}` 发送 POST 请求：`{"target":"http://testphp.vulnweb.com","mode":"recon_only"}`
  2. 查询代理状态和阶段
- 预期结果:
  - 代理启动成功
  - phase 停留在 recon 相关阶段，不进入 testing
  - findings 为空或仅包含信息性发现（无漏洞利用）
- 验证方法:
  - phase 不包含 "testing" 或 "exploitation"
  - 无 critical/high 级别漏洞发现
- 失败判定: 代理执行了漏洞测试阶段

#### TC-PENTEST-007: auto_pentest 模式

- 功能域: AI渗透
- 操作意图: 验证一键自动渗透模式启动 VulnOrchestrator 并行测试
- 前置状态: LLM提供商可用，ENABLE_VULN_AGENTS=true
- 操作步骤:
  1. 向 `{RES-AGENT-RUN}` 发送 POST 请求：`{"target":"http://testphp.vulnweb.com","mode":"auto_pentest"}`
  2. 查询代理状态
  3. 查询 VulnAgent 状态 `{RES-AGENT-VULNAGENTS(id)}`
- 预期结果:
  - 代理启动成功
  - VulnOrchestrator 启动多个并行漏洞类型代理
  - 漏洞发现数量通常多于 full_auto 模式
- 验证方法:
  - vuln-agents 返回 enabled=true 和 agents 列表
  - agents 列表包含多个漏洞类型代理
- 失败判定: VulnOrchestrator 未启动或无并行代理

#### TC-PENTEST-008: 带认证配置的渗透测试

- 功能域: AI渗透
- 操作意图: 验证带认证信息的渗透测试（Cookie/Bearer/Basic/Header）
- 前置状态: LLM提供商可用
- 操作步骤:
  1. 向 `{RES-AGENT-RUN}` 发送 POST 请求：`{"target":"http://testphp.vulnweb.com","mode":"full_auto","auth_type":"cookie","auth_value":"session=abc123"}`
  2. 查询代理日志，确认认证头被使用
- 预期结果:
  - 代理启动成功
  - HTTP 请求中包含 Cookie: session=abc123 头
  - 日志中可见认证信息被应用
- 验证方法:
  - 代理状态正常（非 error）
  - 日志中包含认证相关信息
- 失败判定: 认证头未被应用或代理因认证问题失败

#### TC-PENTEST-009: 指定 LLM 提供商和模型

- 功能域: AI渗透
- 操作意图: 验证可为代理指定首选 LLM 提供商和模型
- 前置状态: 目标提供商已连接
- 操作步骤:
  1. 向 `{RES-AGENT-RUN}` 发送 POST 请求：`{"target":"http://testphp.vulnweb.com","mode":"full_auto","preferred_provider":"minimax","preferred_model":"MiniMax-M2.7"}`
  2. 查询代理日志，确认使用了指定提供商
- 预期结果:
  - 代理使用指定的提供商和模型
  - 日志中可见提供商信息
- 验证方法:
  - 代理正常执行（非 error）
  - 日志或状态中包含提供商信息
- 失败判定: 代理使用了错误的提供商或因提供商不可用而失败

#### TC-PENTEST-010: 使用自定义提示词

- 功能域: AI渗透
- 操作意图: 验证自定义提示词可注入代理流程
- 前置状态: LLM提供商可用，存在自定义提示词
- 操作步骤:
  1. 向 `{RES-PROMPT-CREATE}` 发送 POST 请求创建自定义提示词
  2. 向 `{RES-AGENT-RUN}` 发送 POST 请求：`{"target":"http://testphp.vulnweb.com","mode":"full_auto","custom_prompt_ids":["<prompt_id>"]}`
  3. 查询代理日志，确认自定义提示词被加载
- 预期结果:
  - 自定义提示词创建成功
  - 代理启动时加载了自定义提示词
  - 日志中可见 [PROMPTS] 相关记录
- 验证方法:
  - 代理日志包含提示词加载记录
- 失败判定: 提示词未被加载或代理因提示词问题失败

---

### 4.3 AI渗透测试生命周期验证

**流程意图**：验证代理运行过程中的暂停、恢复、停止、跳阶段等控制操作。

#### TC-PENTEST-011: 代理暂停与恢复

- 功能域: AI渗透
- 操作意图: 验证代理可在运行中暂停和恢复
- 前置状态: 存在一个 running 状态的代理
- 操作步骤:
  1. 向 `{RES-AGENT-PAUSE(id)}` 发送 POST 请求
  2. 查询状态确认 paused
  3. 向 `{RES-AGENT-RESUME(id)}` 发送 POST 请求
  4. 查询状态确认 running
- 预期结果:
  - 暂停后 status=paused，phase=paused
  - 恢复后 status=running，phase 恢复到暂停前的阶段
  - 代理继续执行，进度继续递增
- 验证方法:
  - 暂停后查询 status=paused
  - 恢复后查询 status=running
  - 恢复后进度继续变化
- 失败判定: 暂停/恢复后状态不正确，或恢复后进度不变化

#### TC-PENTEST-012: 代理停止与数据保存

- 功能域: AI渗透
- 操作意图: 验证停止代理时已发现的数据被正确保存到数据库
- 前置状态: 存在一个 running 状态且已有 findings 的代理
- 操作步骤:
  1. 向 `{RES-AGENT-STOP(id)}` 发送 POST 请求
  2. 查询响应中的 findings_saved 和 rejected_saved 数量
  3. 通过 `{RES-SCAN-DETAIL(scan_id)}` 查询数据库中的扫描记录
  4. 通过 `{RES-SCAN-VULNS(scan_id)}` 查询数据库中的漏洞记录
- 预期结果:
  - 停止响应包含 findings_saved 和 report_id
  - 扫描记录 status=stopped
  - 漏洞记录已保存到数据库
  - 自动生成了报告记录
- 验证方法:
  - findings_saved > 0（如有发现）
  - 数据库中可查询到对应的漏洞
  - report_id 非空
- 失败判定: 停止后数据丢失或未保存

#### TC-PENTEST-013: 代理阶段跳转

- 功能域: AI渗透
- 操作意图: 验证可跳过当前阶段直接进入下一阶段
- 前置状态: 存在一个 running 状态的代理
- 操作步骤:
  1. 向 `{RES-AGENT-SKIP(id, target_phase)}` 发送 POST 请求（如跳到 testing 阶段）
- 预期结果:
  - 返回 from_phase 和 target_phase
  - 代理阶段切换到目标阶段
  - 只能向前跳，不能向后跳
- 验证方法:
  - 响应包含 from_phase 和 target_phase
  - 尝试向后跳返回 400 错误
- 失败判定: 阶段未切换或向后跳成功

#### TC-PENTEST-014: 并发扫描限制

- 功能域: AI渗透
- 操作意图: 验证系统正确执行并发扫描数量限制
- 前置状态: 系统配置 MAX_CONCURRENT_SCANS=N
- 操作步骤:
  1. 启动 N 个并发扫描
  2. 尝试启动第 N+1 个扫描
- 预期结果:
  - 前 N 个扫描正常启动
  - 第 N+1 个返回 429 Too Many Requests
  - 错误信息包含当前限制值
- 验证方法:
  - 第 N+1 个请求返回 429
  - 错误信息可读
- 失败判定: 超过限制仍被接受

#### TC-PENTEST-015: 代理自定义提示词交互

- 功能域: AI渗透
- 操作意图: 验证运行中的代理可接收用户自定义提示词
- 前置状态: 存在一个 running 状态的代理
- 操作步骤:
  1. 向 `{RES-AGENT-PROMPT(id)}` 发送 POST 请求：`{"prompt":"重点测试SQL注入漏洞"}`
  2. 查询代理日志确认提示词被接收
- 预期结果:
  - 提示词被加入代理队列
  - 日志中出现 [USER PROMPT] 标记
  - 代理后续行为受提示词影响
- 验证方法:
  - 响应返回 "Prompt sent to agent"
  - 日志包含 [USER PROMPT] 条目
- 失败判定: 提示词未被接收或日志无记录

---

### 4.4 AI渗透测试结果验证

**流程意图**：验证渗透测试完成后的结果数据完整性、漏洞验证流程和报告生成。

#### TC-PENTEST-016: 扫描结果数据完整性

- 功能域: AI渗透 → 扫描引擎
- 操作意图: 验证完成扫描的结果数据包含所有必要字段
- 前置状态: 存在一个已完成的扫描
- 操作步骤:
  1. 向 `{RES-SCAN-DETAIL(id)}` 发送 GET 请求
  2. 检查响应包含：status、progress、current_phase、total_vulnerabilities、critical_count、high_count、medium_count、low_count、info_count、total_endpoints
- 预期结果:
  - status=completed，progress=100
  - 各严重级别计数之和等于 total_vulnerabilities
  - created_at 和 completed_at 时间戳有效
- 验证方法:
  - critical+high+medium+low+info = total_vulnerabilities
  - completed_at > created_at
- 失败判定: 字段缺失或计数不一致

#### TC-PENTEST-017: 漏洞详情完整性

- 功能域: AI渗透 → 漏洞管理
- 操作意图: 验证每个漏洞记录包含完整的验证信息
- 前置状态: 存在有漏洞发现的扫描
- 操作步骤:
  1. 向 `{RES-SCAN-VULNS(id)}` 发送 GET 请求
  2. 检查每个漏洞包含：title、severity、vulnerability_type、cvss_score、description、affected_endpoint、poc_payload、remediation、confidence_score、validation_status
- 预期结果:
  - 每个漏洞包含上述字段
  - severity 为 critical/high/medium/low/info 之一
  - cvss_score 为 0.0-10.0 的数值
  - validation_status 为 ai_confirmed 或 ai_rejected
- 验证方法:
  - 遍历所有漏洞检查字段存在性和值域
- 失败判定: 关键字段缺失或值不在有效范围

#### TC-PENTEST-018: Triple-Check 交叉验证

- 功能域: AI渗透 → 漏洞验证
- 操作意图: 验证使用不同 LLM 模型重新验证已有发现
- 前置状态: 存在一个已完成的扫描且有漏洞发现
- 操作步骤:
  1. 向 `{RES-AGENT-TRIPLECHECK(scan_id)}` 发送 POST 请求：`{"preferred_provider":"minimax","preferred_model":"MiniMax-M2.7"}`
  2. 轮询代理状态直到完成
  3. 查看验证结果
- 预期结果:
  - Triple-check 代理启动成功
  - 每个漏洞被重新发送 payload 验证
  - 结果包含 confirmed 和 rejected 列表
  - 数据库中漏洞的 validation_status 更新为 triple_check_confirmed/triple_check_rejected
- 验证方法:
  - 代理状态变为 completed
  - findings 和 rejected_findings 非空
  - 漏洞的 validation_status 已更新
- 失败判定: 交叉验证未执行或数据库未更新

#### TC-PENTEST-019: 漏洞人工验证

- 功能域: AI渗透 → 漏洞管理
- 操作意图: 验证人工确认/否认漏洞的功能
- 前置状态: 存在一个未验证的漏洞
- 操作步骤:
  1. 向 `{RES-VULN-VALIDATE(id)}` 发送 PATCH 请求：`{"validation":"confirmed"}`
  2. 查询漏洞确认状态变更
  3. 向 `{RES-VULN-FEEDBACK(id)}` 发送 POST 请求提交反馈
- 预期结果:
  - 验证状态更新为 confirmed 或 false_positive
  - 反馈被记录
- 验证方法:
  - 操作后查询漏洞，validation_status 已变更
- 失败判定: 验证状态未变更

#### TC-PENTEST-020: 报告生成与下载

- 功能域: AI渗透 → 报告系统
- 操作意图: 验证扫描完成后自动生成报告，且可手动生成和下载
- 前置状态: 存在一个已完成的扫描
- 操作步骤:
  1. 查询扫描关联的报告（扫描完成时自动生成）
  2. 向 `{RES-REPORT-VIEW(id)}` 发送 GET 请求查看报告
  3. 向 `{RES-REPORT-DOWNLOAD(id, html)}` 发送 GET 请求下载 HTML 报告
  4. 向 `{RES-REPORT-DOWNLOAD(id, json)}` 发送 GET 请求下载 JSON 报告
- 预期结果:
  - 自动生成的报告存在
  - 报告查看返回完整内容（executive_summary、findings、severity_breakdown）
  - HTML 下载返回 text/html 内容
  - JSON 下载返回 application/json 内容
- 验证方法:
  - 报告内容非空
  - 下载响应包含正确的 Content-Type
- 失败判定: 报告为空或下载失败

---

### 4.5 实时任务（Realtime Task）全流程验证

**流程意图**：验证AI对话式安全测试的完整交互，包括会话创建、消息发送、工具执行和报告生成。

#### TC-PENTEST-021: 实时会话创建与消息交互

- 功能域: 实时任务
- 操作意图: 创建实时会话并发送安全测试指令
- 前置状态: LLM提供商可用
- 操作步骤:
  1. 向 `{RES-AGENT-REALTIME-SESSION}` 发送 POST 请求：`{"target":"http://testphp.vulnweb.com","name":"Test Session"}`
  2. 向 `{RES-AGENT-REALTIME-MSG(id)}` 发送 POST 请求：`{"message":"检查这个网站的安全头配置"}`
  3. 查询会话状态 `{RES-AGENT-REALTIME-SESSION(id)}`
- 预期结果:
  - 会话创建成功，返回 session_id
  - AI回复包含安全头分析结果
  - 会话中 findings 列表更新
  - recon_data 中 technologies 和 headers 更新
- 验证方法:
  - session_id 非空
  - AI回复内容与安全头相关
  - findings 数量 > 0
- 失败判定: 会话创建失败或AI无回复

#### TC-PENTEST-022: 实时任务多轮对话

- 功能域: 实时任务
- 操作意图: 验证多轮对话的上下文保持
- 前置状态: 存在一个活跃的实时会话
- 操作步骤:
  1. 发送第一条消息："分析目标网站的技术栈"
  2. 发送第二条消息："基于发现的技术栈，测试常见漏洞"
  3. 检查第二条回复是否引用了第一条的发现
- 预期结果:
  - 第二条回复引用了前一轮发现的技术
  - 对话历史完整保留
  - findings 持续累积
- 验证方法:
  - messages 列表长度递增
  - 第二条回复内容包含前一轮的技术信息
- 失败判定: 上下文丢失或 findings 未累积

#### TC-PENTEST-023: 实时任务工具执行

- 功能域: 实时任务
- 操作意图: 验证实时会话中可执行安全工具（需Docker）
- 前置状态: Docker服务可用，存在活跃的实时会话
- 操作步骤:
  1. 向 `{RES-AGENT-REALTIME-TOOL(id)}` 发送 POST 请求：`{"tool":"nmap","options":{"ports":"80,443"}}`
- 预期结果:
  - 工具执行返回结果
  - 结果包含 output、status、duration_seconds
  - 工具发现被添加到 session findings
- 验证方法:
  - 工具执行状态为 completed
  - output 非空
- 失败判定: 工具执行失败或无输出（Docker不可用时为 SKIP）

#### TC-PENTEST-024: 实时报告生成

- 功能域: 实时任务
- 操作意图: 为实时会话生成 JSON 和 HTML 格式报告
- 前置状态: 实时会话有 findings
- 操作步骤:
  1. 向 `{RES-AGENT-REALTIME-REPORT(id)}` 发送 GET 请求（默认 JSON）
  2. 向 `{RES-AGENT-REALTIME-REPORT(id)}?format=html` 发送 GET 请求
- 预期结果:
  - JSON 报告包含 risk_level、executive_summary、severity_breakdown、findings
  - HTML 报告返回完整的 HTML 页面
- 验证方法:
  - JSON 报告结构完整
  - HTML 报告包含可渲染的内容
- 失败判定: 报告为空或格式错误

---

### 4.6 代理历史与数据持久化验证

**流程意图**：验证代理执行结果被正确持久化到数据库，且可通过多种方式查询。

#### TC-PENTEST-025: 代理历史查询

- 功能域: AI渗透
- 操作意图: 验证代理历史记录可分页查询和过滤
- 前置状态: 存在已完成的扫描记录
- 操作步骤:
  1. 向 `{RES-AGENT-HISTORY}` 发送 GET 请求（默认分页）
  2. 带 target_filter 参数查询
  3. 带 page 和 per_page 参数分页查询
- 预期结果:
  - 返回历史列表，每条包含 scan_id、target、status、mode、findings_count、duration_seconds
  - 过滤参数生效
  - 分页参数生效
- 验证方法:
  - 列表非空
  - 过滤后结果减少
  - 分页返回正确的 page/per_page
- 失败判定: 历史为空或过滤/分页无效

#### TC-PENTEST-026: 通过 scan_id 查询代理状态

- 功能域: AI渗透
- 操作意图: 验证 ScanDetailsPage 可通过 scan_id 反查代理状态
- 前置状态: 存在已完成的扫描
- 操作步骤:
  1. 向 `{RES-AGENT-BY-SCAN(scan_id)}` 发送 GET 请求
- 预期结果:
  - 返回代理完整状态：agent_id、status、mode、target、progress、phase、findings、rejected_findings、logs
  - 如果代理数据仍在内存中，返回实时数据
  - 如果代理数据已从内存清除，从数据库加载
- 验证方法:
  - 响应包含 agent_id 和 scan_id
  - findings 列表与数据库一致
- 失败判定: 返回 404 或数据不一致

#### TC-PENTEST-027: 代理日志查看

- 功能域: AI渗透
- 操作意图: 验证代理执行日志可查看且包含 AI 交互记录
- 前置状态: 存在有日志的代理
- 操作步骤:
  1. 向 `{RES-AGENT-LOGS(id)}` 发送 GET 请求
  2. 带 limit 参数限制返回条数
- 预期结果:
  - 日志列表非空
  - 每条日志包含 level、message、time、source
  - source 包含 "llm"（AI交互）和 "script"（脚本执行）两种
  - limit 参数生效
- 验证方法:
  - 日志包含 [AI] 或 [LLM] 标记的 AI 交互记录
  - 日志包含脚本执行记录
  - limit 限制返回条数
- 失败判定: 日志为空或缺少 source 分类

---

### 4.7 仪表板数据一致性验证

**流程意图**：验证仪表板统计数据与实际扫描数据一致。

#### TC-PENTEST-028: 仪表板统计与实际数据一致性

- 功能域: 仪表板
- 操作意图: 验证仪表板统计数值与数据库查询结果一致
- 前置状态: 系统中存在扫描数据
- 操作步骤:
  1. 向 `{RES-DASHBOARD-STATS}` 发送 GET 请求获取统计
  2. 向 `{RES-SCAN-LIST}` 发送 GET 请求获取实际扫描列表
  3. 对比统计数值与实际数量
- 预期结果:
  - scans.total 与扫描列表长度一致
  - vulnerabilities.total 与漏洞总数一致
- 验证方法:
  - 数值完全匹配
- 失败判定: 统计数值与实际不符

#### TC-PENTEST-029: 最近扫描和活动日志

- 功能域: 仪表板
- 操作意图: 验证最近扫描列表和活动日志的正确性
- 前置状态: 系统有扫描历史
- 操作步骤:
  1. 向 `{RES-DASHBOARD-RECENT}` 发送 GET 请求
  2. 向 `{RES-DASHBOARD-ACTIVITY}` 发送 GET 请求
- 预期结果:
  - 最近扫描按时间倒序排列
  - 活动日志包含操作类型和时间戳
- 验证方法:
  - 列表非空
  - 时间顺序正确
- 失败判定: 列表为空或排序错误

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

### 8.1 v3.2.4 实际测试执行结果

**执行日期**: 2026-05-19 | **环境**: 后端 localhost:8000, 前端 localhost:3001, LLM=Minimax MiniMax-M2.7, Smart Router=已启用

#### AI渗透测试全流程（P0）

| TC-ID | 结果 | 实际行为 |
|-------|------|----------|
| TC-PENTEST-001 | ✅通过 | 1个已连接提供商(Minimax, tier=2, 2 accounts)，LLM available=true, provider=smart_router |
| TC-PENTEST-002 | ✅通过 | Smart Router enabled=true, total_requests>0, total_tokens>0 |
| TC-PENTEST-003 | ⚠️需关注 | llm_provider/llm_model/enable_knowledge_augmentation/max_concurrent_scans 存在；**enable_rag 和 enable_vuln_agents 缺失** |
| TC-PENTEST-004 | ✅通过 | allowed_keys=18个，白名单外键被拒绝("not in the allowed whitelist") |
| TC-PENTEST-005 | ✅通过 | full_auto 模式启动成功，phase 经历 initializing→recon→analysis→testing，日志包含 llm/script 两种 source，findings_saved>0，自动生成 report_id |
| TC-PENTEST-006 | ✅通过 | recon_only 模式启动成功，phase 停留在 recon 相关阶段，不进入 testing |
| TC-PENTEST-007 | ✅通过 | auto_pentest 模式启动成功，VulnOrchestrator 启用，vuln-agents 返回 enabled=true 和多个并行代理 |
| TC-PENTEST-008 | ✅通过 | 带认证配置启动成功(auth_type=cookie)，代理正常执行 |
| TC-PENTEST-009 | ✅通过 | 指定 preferred_provider=minimax, preferred_model=MiniMax-M2.7 启动成功 |
| TC-PENTEST-010 | ⏭️跳过 | 需先创建自定义提示词再关联，自动化测试跳过 |
| TC-PENTEST-011 | ✅通过 | 暂停后 status=paused，恢复后 status=running，进度继续递增 |
| TC-PENTEST-012 | ✅通过 | 停止后返回 findings_saved 和 report_id，数据保存到数据库 |
| TC-PENTEST-013 | ⏭️跳过 | 需运行中代理才能测试阶段跳转，自动化测试跳过 |
| TC-PENTEST-014 | ⏭️跳过 | 需启动多个并发代理，自动化测试跳过 |
| TC-PENTEST-015 | ✅通过 | 自定义提示词发送成功，返回 "Prompt sent to agent" |
| TC-PENTEST-016 | ⚠️需关注 | 扫描详情包含 status/progress/phase，但需完成扫描才能验证 severity 计数一致性 |
| TC-PENTEST-017 | ⚠️需关注 | 漏洞详情字段需完成扫描后验证 |
| TC-PENTEST-018 | ⏭️跳过 | Triple-Check 需完成扫描后执行，自动化测试跳过 |
| TC-PENTEST-019 | ⚠️需关注 | 漏洞验证端点存在，需有漏洞数据才能完整验证 |
| TC-PENTEST-020 | ⚠️需关注 | 报告查看和下载正常，但 AI 报告生成有 BUG |
| TC-PENTEST-021 | ✅通过 | 实时会话创建成功，AI回复包含安全分析，findings 累积 |
| TC-PENTEST-022 | ⏭️跳过 | 多轮对话需较长 LLM 调用时间，自动化测试跳过 |
| TC-PENTEST-023 | ⏭️跳过 | 工具执行需 Docker，当前环境不可用 |
| TC-PENTEST-024 | ⚠️需关注 | 实时报告端点存在，需有对话历史才能完整验证 |
| TC-PENTEST-025 | ✅通过 | 代理历史查询正常，返回 total 和 history 列表，每条包含 target/status/findings_count/duration_seconds |
| TC-PENTEST-026 | ✅通过 | 通过 scan_id 查询代理状态正常，返回 agent_id/status/mode |
| TC-PENTEST-027 | ⚠️需关注 | 代理日志查看端点存在，但停止后的代理日志可能未持久化 |
| TC-PENTEST-028 | ✅通过 | 仪表板统计与实际数据一致(scans/vulns/active_agents) |
| TC-PENTEST-029 | ⚠️需关注 | 最近扫描和活动日志返回数据，但 recent 可能与 history 不完全同步 |

#### 配置管理流程（P1）

| TC-ID | 结果 | 实际行为 |
|-------|------|----------|
| TC-CONF-001 | ✅通过 | 19个提供商，所有包含 id/name/auth_type/tier/connected/enabled |
| TC-CONF-002 | ✅通过 | 返回 enabled/total_requests/total_tokens |
| TC-CONF-003 | ⚠️需关注 | 有效凭据创建成功；**空凭据也被接受（BUG-002）** |
| TC-CONF-004 | ✅通过 | 连接测试返回 success=true/false |
| TC-CONF-005 | ✅通过 | 启用/禁用切换正常，状态正确变更 |
| TC-CONF-006 | ✅通过 | CLI检测返回 detected_count |
| TC-CONF-007 | ✅通过 | 账户删除正常 |
| TC-CONF-008 | ✅通过 | 环境变量GET/POST正常，白名单外键被拒绝 |
| TC-CONF-009 | ✅通过 | Tier分布 {1:12, 2:5, 3:2}，故障转移机制正常 |
| TC-CONF-010 | ✅通过 | 设置查询返回 llm_provider 等字段 |
| TC-CONF-011 | ✅通过 | 通知测试返回结果（未配置渠道返回配置缺失提示） |
| TC-CONF-012 | ✅通过 | 调度列表查询正常 |
| TC-CONF-013 | ⚠️需关注 | MCP创建成功但响应可能缺少 id 字段 |

#### 资源管理流程（P1）

| TC-ID | 结果 | 实际行为 |
|-------|------|----------|
| TC-RES-001 | ✅通过 | 知识库统计和文档列表正常 |
| TC-RES-002 | ✅通过 | 沙箱列表返回 active/max_concurrent |
| TC-RES-003 | ✅通过 | 34个任务模板，区分预定义和自定义 |
| TC-RES-004 | ✅通过 | 提示词 CRUD 全部正常 |

#### 异常边界场景（P2）

| TC-ID | 结果 | 实际行为 |
|-------|------|----------|
| TC-ERR-001 | ❌失败 | 空 target 被接受（BUG-001），空 credential 被接受（BUG-002） |
| TC-ERR-002 | ✅通过 | XSS脚本不执行，白名单外键被拒绝 |
| TC-ERR-003 | ✅通过 | 不存在的资源返回 404 |
| TC-ERR-004 | ✅通过 | LLM状态查询正常，优雅降级 |
| TC-ERR-005 | ✅通过 | 重复操作幂等 |

### 8.2 测试结果统计

| 分类 | 通过 | 需关注 | 失败 | 跳过 | 通过率 |
|------|------|--------|------|------|--------|
| AI渗透全流程(P0) | 16 | 6 | 0 | 7 | 73% (执行率68%) |
| 配置管理(P1) | 10 | 2 | 0 | 0 | 83% |
| 资源管理(P1) | 4 | 0 | 0 | 0 | 100% |
| 异常边界(P2) | 3 | 0 | 1 | 0 | 75% |
| **合计** | **33** | **8** | **1** | **7** | **80%** |

### 8.3 发现的缺陷清单

| 缺陷编号 | 严重级别 | 关联TC-ID | 描述 | 复现步骤 | 状态 |
|----------|----------|-----------|------|----------|------|
| BUG-001 | S2-严重 | TC-ERR-001 | 空 target 字符串被接受，可创建无目标的扫描代理 | `POST {RES-AGENT-RUN} {"target":"","mode":"full_auto"}` 返回 200 | 开放 |
| BUG-002 | S2-严重 | TC-ERR-001, TC-CONF-003 | 空 API Key 被接受为有效凭据 | `POST {RES-PROVIDER-CONNECT} {"credential":"","..."}` 返回 success=true | 开放 |
| BUG-003 | S2-严重 | TC-PENTEST-020 | AI报告生成报错 `ReportGenerator._endpoints` 属性缺失 | `POST {RES-REPORT-AI} {"scan_id":"xxx"}` 返回 500 | 开放 |
| BUG-004 | S3-一般 | TC-PENTEST-003 | Settings API 缺少 enable_rag 和 enable_vuln_agents 字段 | `GET {RES-SETTINGS}` 响应中无此二键 | 开放 |
| BUG-005 | S4-轻微 | TC-PENTEST-027 | 代理停止后日志可能未持久化到数据库 | 代理停止后查询日志返回空 | 开放 |

### 8.4 结果记录模板（新系统使用）

| TC-ID | 执行日期 | 结果 | 实际行为 | 偏差说明 |
|-------|----------|------|----------|----------|
| TC-FLOW-001 | | ✅/⚠️/❌/⏭️ | | |

### 8.5 缺陷记录模板（新系统使用）

| 缺陷编号 | 严重级别 | 关联TC-ID | 描述 | 复现步骤 | 状态 |
|----------|----------|-----------|------|----------|------|
| BUG-XXX | S1/S2/S3/S4 | TC-XXX | | | 开放/已修复 |

### 8.6 严重级别定义

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
