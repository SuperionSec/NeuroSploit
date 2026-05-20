# NeuroSploit v3.2.4 前端页面功能与跳转流程完整映射

> 生成时间: 2026-05-20  
> 基于源码: `/workspace/frontend/src/`  
> API 基础路径: `/api/v1`

---

## 侧边栏导航结构

```
Operations
  ├── Dashboard          →  /
  ├── Auto Pentest       →  /auto
  ├── AI Agent           →  /scan/new
  ├── Real-time Task     →  /realtime
  └── FULL AI TESTING    →  /full-ia

Tools
  ├── Vuln Lab           →  /vuln-lab
  ├── Terminal Agent     →  /terminal
  ├── Sandboxes          →  /sandboxes
  ├── Task Library       →  /tasks
  ├── Knowledge          →  /knowledge
  ├── MCP Servers        →  /mcp
  └── Providers          →  /providers

Configuration
  ├── Scheduler          →  /scheduler
  ├── Reports            →  /reports
  └── Settings           →  /settings
```

---

## 1. Dashboard 首页

**URL**: `/`  
**组件**: `HomePage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/dashboard/stats` | GET | 获取统计卡片数据 |
| 页面挂载 | `/api/v1/dashboard/recent?limit=10` | GET | 获取最近扫描列表 |
| 页面挂载 | `/api/v1/dashboard/findings?limit=20` | GET | 获取最近漏洞发现 |
| 页面挂载 | `/api/v1/dashboard/vulnerability-types` | GET | 获取漏洞类型分布 |
| 页面挂载 | `/api/v1/dashboard/agent-tasks?limit=20` | GET | 获取代理任务 |
| 页面挂载 | `/api/v1/dashboard/activity-feed?limit=30` | GET | 获取活动动态 |
| 自动刷新(30s) | 以上全部 | GET | 轮询刷新数据 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| "New Scan" 按钮 | 点击 | — | → `/scan/new` |
| "Refresh" 按钮 | 点击 | 重新调用全部加载接口 | 停留在 `/` |
| 扫描记录名称 | 点击链接 | — | → `/scan/{scanId}` |
| 漏洞发现条目 | 点击 | — | → `/scan/{scanId}` (对应扫描) |
| 活动动态条目 | 点击 | — | → 对应页面 |
| 连接断开横幅 | 自动显示(3次连续失败) | — | 停留在 `/` |

---

## 2. Auto Pentest 页面

**URL**: `/auto`  
**组件**: `AutoPentestPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/agent/active` | GET | 获取活跃代理列表 |
| 页面挂载 | `/api/v1/agent/history?page=1&per_page=20` | GET | 获取历史代理 |
| 页面挂载 | `/api/v1/cli-agent/providers` | GET | 获取CLI代理提供商 |
| 页面挂载 | `/api/v1/cli-agent/methodologies` | GET | 获取方法论文件 |
| 页面挂载 | `/api/v1/providers/available-models` | GET | 获取可用LLM模型 |
| 页面挂载 | `/api/v1/agent/tasks` | GET | 获取任务预设列表 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| "Start Pentest" 按钮 | 输入目标URL后点击 | `POST /api/v1/agent/run` {mode:"auto_pentest", target, ...} | → `/agent/{agentId}` |
| 运行中: "Pause" 按钮 | 点击 | `POST /api/v1/agent/pause/{agentId}` | 停留在 `/auto` |
| 运行中: "Resume" 按钮 | 点击 | `POST /api/v1/agent/resume/{agentId}` | 停留在 `/auto` |
| 运行中: "Stop" 按钮 | 点击确认 | `POST /api/v1/agent/stop/{agentId}` | 停留在 `/auto` |
| 运行中: "View Details" 按钮 | 点击 | — | → `/agent/{agentId}` |
| 运行中: "View Scan" 按钮 | 点击 | — | → `/scan/{scanId}` |
| 运行中: "View Report" 链接 | 点击 | — | → `/reports/{reportId}` (或直接下载) |
| Findings 标签页 | 切换 | `GET /api/v1/agent/findings/{agentId}` | 停留在 `/auto` |
| Agents 标签页 | 切换 | `GET /api/v1/agent/vuln-agents/{agentId}` | 停留在 `/auto` |
| Log 标签页 | 切换 | `GET /api/v1/agent/logs/{agentId}?limit=100` | 停留在 `/auto` |
| 日志过滤器(All/Recon/Junior/...) | 点击 | — (前端过滤) | 停留在 `/auto` |
| 历史会话记录 | 点击 | — | → `/scan/{scanId}` |
| 自动刷新(5s) | 轮询 | `GET /api/v1/agent/status/{agentId}` | 停留在 `/auto` |

---

## 3. FULL AI Testing 页面

**URL**: `/full-ia`  
**组件**: `FullIATestingPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/agent/active` | GET | 获取活跃代理 |
| 页面挂载 | `/api/v1/providers/available-models` | GET | 获取可用LLM模型 |
| 页面挂载 | `/api/v1/agent/tasks` | GET | 获取任务预设 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| "Start Full LLM Pentest" 按钮 | 输入目标后点击 | `POST /api/v1/agent/run` {mode:"full_llm_pentest", target, ...} | → `/agent/{agentId}` |
| "Stop" 按钮 | 点击 | `POST /api/v1/agent/stop/{agentId}` | 停留在 `/full-ia` |
| "View Agent" 按钮 | 点击 | — | → `/agent/{agentId}` |
| "View Report" 链接 | 点击 | — | 直接打开 `/api/v1/reports/{id}/view` |
| "Download ZIP" 链接 | 点击 | — | 直接下载 `/api/v1/reports/{id}/download-zip` |
| Findings/Log 标签页 | 切换 | `GET /api/v1/agent/findings/{agentId}` / `GET /api/v1/agent/logs/{agentId}` | 停留在 `/full-ia` |
| 自动刷新(5s) | 轮询 | `GET /api/v1/agent/status/{agentId}` | 停留在 `/full-ia` |

---

## 4. AI Agent / New Scan 页面

**URL**: `/scan/new`  
**组件**: `NewScanPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/agent/tasks` | GET | 获取任务预设列表 |
| 页面挂载 | `/api/v1/prompts/presets` | GET | 获取提示词预设 |
| 页面挂载 | `/api/v1/providers/available-models` | GET | 获取可用LLM模型 |
| 页面挂载 | `/api/v1/cli-agent/providers` | GET | 获取CLI代理提供商 |
| 页面挂载 | `/api/v1/cli-agent/methodologies` | GET | 获取方法论文件 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| 模式选择(Full Auto/Recon Only/Prompt Only/Analyze Only) | 点击卡片 | — | 停留在 `/scan/new` |
| 目标输入-Single URL | 输入 | `POST /api/v1/targets/validate` (失焦时) | 停留在 `/scan/new` |
| 目标输入-Multiple URLs | 切换+输入 | `POST /api/v1/targets/validate/bulk` (提交时) | 停留在 `/scan/new` |
| 目标输入-Upload File | 拖拽/选择文件 | `POST /api/v1/targets/upload` | 停留在 `/scan/new` |
| Task Library 分类过滤 | 点击分类按钮 | — (前端过滤) | 停留在 `/scan/new` |
| 选择任务卡片 | 点击 | — | 停留在 `/scan/new` |
| "Use custom prompt" 复选框 | 勾选 | — | 停留在 `/scan/new` |
| Authentication Options 展开 | 点击 | — | 停留在 `/scan/new` |
| "Deploy Agent" 按钮 | 点击 | `POST /api/v1/agent/run` {target, mode, ...} | → `/agent/{agentId}` |
| 部署成功 | 自动 | — | → `/agent/{agentId}` |
| "Cancel" 按钮 | 点击 | — | → `/` |
| 从 Task Library 跳入 | 携带 state | — | 停留在 `/scan/new` (预选任务) |

---

## 5. Real-time Task 页面

**URL**: `/realtime`  
**组件**: `RealtimeTaskPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/agent/realtime/sessions/list` | GET | 获取会话列表 |
| 页面挂载 | `/api/v1/agent/realtime/llm-status` | GET | 获取LLM可用状态 |
| 页面挂载 | `/api/v1/agent/realtime/tools/list` | GET | 获取安全工具列表 |
| 页面挂载 | `/api/v1/agent/realtime/tools/status` | GET | 获取工具运行状态 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| "New Session" 按钮 | 点击弹出表单 | — | 停留在 `/realtime` |
| 创建会话 | 提交表单 | `POST /api/v1/agent/realtime/session` {target, name} | 停留在 `/realtime` (加载新会话) |
| 选择会话 | 点击左侧列表 | `GET /api/v1/agent/realtime/{sessionId}` | 停留在 `/realtime` |
| 发送消息 | 输入+Enter/点击发送 | `POST /api/v1/agent/realtime/{sessionId}/message` {message} | 停留在 `/realtime` |
| Quick Prompt 按钮 | 点击 | `POST /api/v1/agent/realtime/{sessionId}/message` {message: prompt} | 停留在 `/realtime` |
| 工具类别按钮(FFUF/Nuclei等) | 点击 | `POST /api/v1/agent/realtime/{sessionId}/execute-tool` {tool, options} | 停留在 `/realtime` |
| "Report" 按钮 | 点击 | `GET /api/v1/agent/realtime/{sessionId}/report` | 停留在 `/realtime` |
| 删除会话 | 点击删除按钮 | `DELETE /api/v1/agent/realtime/{sessionId}` | 停留在 `/realtime` |
| Findings 面板展开 | 点击漏洞条目 | — | 停留在 `/realtime` |
| 自动刷新(5s) | 轮询 | `GET /api/v1/agent/realtime/{sessionId}` | 停留在 `/realtime` |

---

## 6. Vuln Lab 页面

**URL**: `/vuln-lab`  
**组件**: `VulnLabPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/vuln-lab/types` | GET | 获取漏洞类型分类 |
| 页面挂载 | `/api/v1/vuln-lab/challenges?limit=20` | GET | 获取历史挑战 |
| 页面挂载 | `/api/v1/vuln-lab/stats` | GET | 获取实验室统计 |
| 页面挂载 | `/api/v1/providers/available-models` | GET | 获取可用LLM模型 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| Test/History/Stats 标签切换 | 点击 | — | 停留在 `/vuln-lab` |
| 漏洞类型分类卡片展开 | 点击 | — | 停留在 `/vuln-lab` |
| 搜索框过滤 | 输入 | — (前端过滤) | 停留在 `/vuln-lab` |
| 选择漏洞类型 | 点击 | — | 停留在 `/vuln-lab` |
| "Run Test" 按钮 | 输入目标后点击 | `POST /api/v1/vuln-lab/run` {target_url, vuln_type, ...} | 停留在 `/vuln-lab` (进入运行视图) |
| "Stop" 按钮 | 点击 | `POST /api/v1/vuln-lab/challenges/{id}/stop` | 停留在 `/vuln-lab` |
| "View Scan" 按钮 | 点击 | — | → `/scan/{scanId}` |
| 历史挑战点击 | 点击 | — | → `/scan/{scanId}` |
| 删除挑战 | 点击 | `DELETE /api/v1/vuln-lab/challenges/{id}` | 停留在 `/vuln-lab` |
| 自动刷新(5s) | 轮询 | `GET /api/v1/vuln-lab/challenges/{id}` | 停留在 `/vuln-lab` |

---

## 7. Terminal Agent 页面

**URL**: `/terminal`  
**组件**: `TerminalAgentPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/terminal/sessions` | GET | 获取终端会话列表 |
| 页面挂载 | `/api/v1/terminal/templates` | GET | 获取终端模板 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| "Start Terminal"/"New Session" | 点击弹出表单 | — | 停留在 `/terminal` |
| 创建终端会话 | 提交表单 | `POST /api/v1/terminal/session` {target, name, template_id} | 停留在 `/terminal` |
| 选择会话 | 点击列表 | `GET /api/v1/terminal/sessions/{sessionId}` | 停留在 `/terminal` |
| 发送命令 | 输入+Enter | `POST /api/v1/terminal/sessions/{sessionId}/message` {message} | 停留在 `/terminal` |
| 执行命令 | 点击执行 | `POST /api/v1/terminal/sessions/{sessionId}/execute` {command, execution_method} | 停留在 `/terminal` |
| "Add Step" 添加利用步骤 | 点击+填写 | `POST /api/v1/terminal/sessions/{sessionId}/exploitation-path` {description, command, result, step_type} | 停留在 `/terminal` |
| 查看利用路径 | 自动加载 | `GET /api/v1/terminal/sessions/{sessionId}/exploitation-path` | 停留在 `/terminal` |
| "VPN Status" | 点击 | `GET /api/v1/terminal/sessions/{sessionId}/vpn-status` | 停留在 `/terminal` |
| "Upload OVPN" | 选择文件 | `POST /api/v1/terminal/sessions/{sessionId}/vpn/upload` (multipart) | 停留在 `/terminal` |
| "Connect VPN" | 点击 | `POST /api/v1/terminal/sessions/{sessionId}/vpn/connect` | 停留在 `/terminal` |
| "Disconnect VPN" | 点击 | `POST /api/v1/terminal/sessions/{sessionId}/vpn/disconnect` | 停留在 `/terminal` |
| 删除会话 | 点击 | `DELETE /api/v1/terminal/sessions/{sessionId}` | 停留在 `/terminal` |

---

## 8. Task Library 页面

**URL**: `/tasks`  
**组件**: `TaskLibraryPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/agent/tasks` | GET | 获取全部任务预设 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| 分类过滤器(All/vulnerability/...) | 点击 | — (前端过滤) | 停留在 `/tasks` |
| "Create Task" 按钮 | 点击弹出表单 | — | 停留在 `/tasks` |
| 创建任务 | 提交表单 | `POST /api/v1/agent/tasks` {name, description, category, prompt, tags} | 停留在 `/tasks` |
| "Edit" 按钮(自定义任务) | 点击弹出表单 | — | 停留在 `/tasks` |
| "Delete" 按钮(自定义任务) | 点击确认 | `DELETE /api/v1/agent/tasks/{taskId}` | 停留在 `/tasks` |
| "Use" 按钮(任务卡片) | 点击 | — | → `/scan/new` (携带 state: {selectedTaskId}) |

---

## 9. Knowledge 页面

**URL**: `/knowledge`  
**组件**: `KnowledgePage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/knowledge/stats` | GET | 获取知识库统计 |
| 页面挂载 | `/api/v1/knowledge/documents` | GET | 获取文档列表 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| "Upload" / 拖拽文件 | 选择/拖入文件 | `POST /api/v1/knowledge/upload` (multipart) | 停留在 `/knowledge` |
| 搜索框 | 输入漏洞类型 | `GET /api/v1/knowledge/search?vuln_type={type}` | 停留在 `/knowledge` |
| 文档卡片展开 | 点击 | `GET /api/v1/knowledge/documents/{docId}` | 停留在 `/knowledge` |
| "Delete" 按钮 | 点击确认 | `DELETE /api/v1/knowledge/documents/{docId}` | 停留在 `/knowledge` |
| "Refresh" 按钮 | 点击 | 重新调用加载接口 | 停留在 `/knowledge` |

---

## 10. MCP Servers 页面

**URL**: `/mcp`  
**组件**: `MCPManagementPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/mcp/servers` | GET | 获取MCP服务器列表 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| "Add Server" 按钮 | 点击弹出表单 | — | 停留在 `/mcp` |
| 创建服务器 | 提交表单 | `POST /api/v1/mcp/servers` {name, transport, command, args, ...} | 停留在 `/mcp` |
| Toggle 开关 | 点击 | `POST /api/v1/mcp/servers/{name}/toggle` | 停留在 `/mcp` |
| "Test" 按钮 | 点击 | `POST /api/v1/mcp/servers/{name}/test` | 停留在 `/mcp` |
| "Tools" 标签 | 点击 | `GET /api/v1/mcp/servers/{name}/tools` | 停留在 `/mcp` |
| "Edit" 按钮 | 点击弹出表单 | `GET /api/v1/mcp/servers/{name}` | 停留在 `/mcp` |
| 更新服务器 | 提交表单 | `PUT /api/v1/mcp/servers/{name}` | 停留在 `/mcp` |
| "Delete" 按钮(自定义) | 点击确认 | `DELETE /api/v1/mcp/servers/{name}` | 停留在 `/mcp` |

---

## 11. Providers 页面

**URL**: `/providers`  
**组件**: `ProvidersPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/providers` | GET | 获取提供商列表 |
| 页面挂载 | `/api/v1/providers/status` | GET | 获取Smart Router状态 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| "Detect All CLIs" 按钮 | 点击 | `POST /api/v1/providers/detect-all` | 停留在 `/providers` |
| "Refresh" 按钮 | 点击 | 重新调用加载接口 | 停留在 `/providers` |
| 提供商卡片点击 | 点击 | — (弹出模态框) | 停留在 `/providers` |
| "Connect" 按钮 | 输入Key+Label后点击 | `POST /api/v1/providers/{id}/connect` {credential, label, model_override} | 停留在 `/providers` |
| "Test" 按钮(已连接账户) | 点击 | `POST /api/v1/providers/test/{id}/{accountId}` | 停留在 `/providers` |
| "Remove" 按钮(账户) | 点击 | `DELETE /api/v1/providers/{id}/accounts/{accountId}` | 停留在 `/providers` |
| Toggle 开关(提供商) | 点击 | `POST /api/v1/providers/{id}/toggle` {enabled} | 停留在 `/providers` |
| "Environment Variables" 按钮 | 点击展开 | `GET /api/v1/providers/env` | 停留在 `/providers` |
| 修改环境变量+Save | 输入+点击保存 | `POST /api/v1/providers/env` {key, value} | 停留在 `/providers` |
| "Available Models" 查看 | 点击 | `GET /api/v1/providers/available-models` | 停留在 `/providers` |

---

## 12. Sandboxes 页面

**URL**: `/sandboxes`  
**组件**: `SandboxDashboardPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/sandbox/` | GET | 获取沙箱池状态 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| "Cleanup" 按钮 | 点击 | `POST /api/v1/sandbox/cleanup` | 停留在 `/sandboxes` |
| "Cleanup Orphans" 按钮 | 点击 | `POST /api/v1/sandbox/cleanup-orphans` | 停留在 `/sandboxes` |
| 沙箱健康检查 | 点击 | `GET /api/v1/sandbox/{scanId}` | 停留在 `/sandboxes` |
| 销毁沙箱 | 点击 | `DELETE /api/v1/sandbox/{scanId}` | 停留在 `/sandboxes` |
| 自动刷新(10s) | 轮询 | `GET /api/v1/sandbox/` | 停留在 `/sandboxes` |

---

## 13. Scheduler 页面

**URL**: `/scheduler`  
**组件**: `SchedulerPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/scheduler/` | GET | 获取定时任务列表 |
| 页面挂载 | `/api/v1/scheduler/agent-roles` | GET | 获取代理角色列表 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| "Create Task" 按钮 | 点击弹出表单 | — | 停留在 `/scheduler` |
| 创建定时任务 | 提交表单 | `POST /api/v1/scheduler/` {name, target, cron_expression, agent_role, ...} | 停留在 `/scheduler` |
| "Pause" 按钮 | 点击 | `POST /api/v1/scheduler/{jobId}/pause` | 停留在 `/scheduler` |
| "Resume" 按钮 | 点击 | `POST /api/v1/scheduler/{jobId}/resume` | 停留在 `/scheduler` |
| "Run Now" 按钮 | 点击 | — (立即触发) | 停留在 `/scheduler` |
| "Delete" 按钮 | 点击确认 | `DELETE /api/v1/scheduler/{jobId}` | 停留在 `/scheduler` |

---

## 14. Reports 页面

**URL**: `/reports`  
**组件**: `ReportsPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/reports` | GET | 获取报告列表 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| 扫描ID过滤 | 输入 | `GET /api/v1/reports?scan_id={id}` | 停留在 `/reports` |
| "Generate Report" 按钮 | 点击弹出表单 | — | 停留在 `/reports` |
| 生成报告 | 提交表单 | `POST /api/v1/reports` {scan_id, format, title, ...} | 停留在 `/reports` |
| "AI Generate" 按钮 | 点击 | `POST /api/v1/reports/ai-generate` {scan_id, title, ...} | 停留在 `/reports` |
| "View" 按钮 | 点击 | — | → `/reports/{reportId}` |
| "Download" 按钮 | 点击 | — | 直接下载 `/api/v1/reports/{id}/download/{format}` |
| "Delete" 按钮 | 点击确认 | `DELETE /api/v1/reports/{reportId}` | 停留在 `/reports` |

---

## 15. Settings 页面

**URL**: `/settings`  
**组件**: `SettingsPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/settings` | GET | 获取当前设置 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| 修改设置项 | 输入/切换 | — (前端状态) | 停留在 `/settings` |
| "Save Settings" 按钮 | 点击 | `PUT /api/v1/settings` {全部设置} | 停留在 `/settings` |
| "Reset" 按钮 | 点击 | — (恢复默认值) | 停留在 `/settings` |

---

## 16. Scan Details 页面

**URL**: `/scan/:scanId`  
**组件**: `ScanDetailsPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/scans/{scanId}` | GET | 获取扫描详情 |
| 页面挂载 | `/api/v1/scans/{scanId}/endpoints` | GET | 获取端点列表 |
| 页面挂载 | `/api/v1/scans/{scanId}/vulnerabilities` | GET | 获取漏洞列表 |
| 页面挂载 | `/api/v1/agent/by-scan/{scanId}` | GET | 获取关联代理 |
| 页面挂载 | `/api/v1/agent-tasks/summary?scan_id={scanId}` | GET | 获取任务摘要 |
| 页面挂载 | `/api/v1/agent-tasks/scan/{scanId}/timeline` | GET | 获取任务时间线 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| Endpoints/Vulnerabilities/Tasks 标签切换 | 点击 | — | 停留在当前页 |
| "Pause" 按钮 | 点击 | `POST /api/v1/scans/{scanId}/pause` | 停留在当前页 |
| "Resume" 按钮 | 点击 | `POST /api/v1/scans/{scanId}/resume` | 停留在当前页 |
| "Stop" 按钮 | 点击 | `POST /api/v1/scans/{scanId}/stop` | 停留在当前页 |
| "Skip to Phase" 按钮 | 点击 | `POST /api/v1/scans/{scanId}/skip-to/{phase}` | 停留在当前页 |
| "View Agent" 按钮 | 点击 | — | → `/agent/{agentId}` |
| "Generate Report" 按钮 | 点击 | `POST /api/v1/reports` {scan_id, ...} | 停留在当前页 |
| "Triple Check" 按钮 | 点击 | `POST /api/v1/agent/triple-check/{scanId}` | 停留在当前页 |
| "Delete Scan" 按钮 | 点击确认 | `DELETE /api/v1/scans/{scanId}` | → `/` |
| "Go to Dashboard" 按钮 | 点击 | — | → `/` |
| 漏洞验证(确认/拒绝) | 点击 | `PATCH /api/v1/scans/vulnerabilities/{vulnId}/validate` | 停留在当前页 |
| 漏洞反馈 | 提交 | `POST /api/v1/scans/vulnerabilities/{vulnId}/feedback` | 停留在当前页 |
| CWE链接 | 点击 | — | → 外部 `https://cwe.mitre.org/...` |
| 自动刷新(5s) | 轮询 | `GET /api/v1/scans/{scanId}` | 停留在当前页 |

---

## 17. Agent Status 页面

**URL**: `/agent/:agentId`  
**组件**: `AgentStatusPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/agent/status/{agentId}` | GET | 获取代理状态 |
| 页面挂载 | `/api/v1/agent/logs/{agentId}?limit=100` | GET | 获取代理日志 |
| 页面挂载 | `/api/v1/agent/findings/{agentId}` | GET | 获取漏洞发现 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| Findings/Agents/Log 标签切换 | 点击 | — | 停留在当前页 |
| 日志过滤器(All/Recon/Junior/Tools/Deep/Errors) | 点击 | — (前端过滤) | 停留在当前页 |
| "Pause" 按钮 | 点击 | `POST /api/v1/agent/pause/{agentId}` | 停留在当前页 |
| "Resume" 按钮 | 点击 | `POST /api/v1/agent/resume/{agentId}` | 停留在当前页 |
| "Stop" 按钮 | 点击 | `POST /api/v1/agent/stop/{agentId}` | 停留在当前页 |
| "Send Prompt" 按钮 | 输入+提交 | `POST /api/v1/agent/prompt/{agentId}` {prompt} | 停留在当前页 |
| "Skip to Phase" 按钮 | 点击 | `POST /api/v1/agent/skip-to/{agentId}/{phase}` | 停留在当前页 |
| "View Scan" 按钮 | 点击 | — | → `/scan/{scanId}` |
| "Start New Agent" 按钮 | 点击 | — | → `/scan/new` |
| "Delete" 按钮 | 点击确认 | `DELETE /api/v1/agent/{agentId}` | → `/` |
| CWE链接 | 点击 | — | → 外部 `https://cwe.mitre.org/...` |
| 自动刷新(5s) | 轮询 | `GET /api/v1/agent/status/{agentId}` | 停留在当前页 |

---

## 18. Report View 页面

**URL**: `/reports/:reportId`  
**组件**: `ReportViewPage.tsx`

### 页面加载时调用的接口

| 触发时机 | 接口 | 方法 | 说明 |
|----------|------|------|------|
| 页面挂载 | `/api/v1/reports/{reportId}` | GET | 获取报告元数据 |
| 页面挂载 | `/api/v1/reports/{reportId}/view` | GET | 获取HTML报告内容 |

### 功能与跳转

| 功能/按钮 | 操作 | 调用接口 | 跳转目标 |
|-----------|------|----------|----------|
| "Download PDF" 按钮 | 点击 | — | 直接下载 `/api/v1/reports/{id}/download/pdf` |
| "Download Markdown" 按钮 | 点击 | — | 直接下载 `/api/v1/reports/{id}/download/md` |
| "Download ZIP" 按钮 | 点击 | — | 直接下载 `/api/v1/reports/{id}/download-zip` |
| "Share" 按钮 | 点击 | — | 复制链接到剪贴板 |
| "Back" 按钮 | 点击 | — | → `/reports` |

---

## 跨页面跳转流程图

```
Dashboard (/)
  ├── [New Scan] ──────────────────→ /scan/new
  ├── [扫描名称] ──────────────────→ /scan/{scanId}
  └── [漏洞条目] ──────────────────→ /scan/{scanId}

Auto Pentest (/auto)
  ├── [Start Pentest] ─────────────→ /agent/{agentId}
  ├── [View Details] ──────────────→ /agent/{agentId}
  ├── [View Scan] ─────────────────→ /scan/{scanId}
  ├── [View Report] ───────────────→ /reports/{reportId} (或直接下载)
  └── [历史记录] ──────────────────→ /scan/{scanId}

FULL AI Testing (/full-ia)
  ├── [Start Full LLM Pentest] ────→ /agent/{agentId}
  ├── [View Agent] ────────────────→ /agent/{agentId}
  └── [View Report] ───────────────→ 直接打开 /api/v1/reports/{id}/view

AI Agent / New Scan (/scan/new)
  ├── [Deploy Agent] ──────────────→ /agent/{agentId}
  ├── [Cancel] ────────────────────→ /
  └── [从Task Library跳入] ←────── /tasks [Use]

Real-time Task (/realtime)
  └── (无外部跳转，所有操作在页面内完成)

Vuln Lab (/vuln-lab)
  ├── [View Scan] ─────────────────→ /scan/{scanId}
  └── [历史挑战] ──────────────────→ /scan/{scanId}

Terminal Agent (/terminal)
  └── (无外部跳转，所有操作在页面内完成)

Task Library (/tasks)
  └── [Use] ──────────────────────→ /scan/new (携带 selectedTaskId)

Scan Details (/scan/{scanId})
  ├── [View Agent] ────────────────→ /agent/{agentId}
  ├── [Go to Dashboard] ──────────→ /
  ├── [Delete Scan] ──────────────→ /
  └── [CWE链接] ──────────────────→ 外部 mitre.org

Agent Status (/agent/{agentId})
  ├── [View Scan] ─────────────────→ /scan/{scanId}
  ├── [Start New Agent] ──────────→ /scan/new
  ├── [Delete] ────────────────────→ /
  └── [CWE链接] ──────────────────→ 外部 mitre.org

Reports (/reports)
  └── [View] ─────────────────────→ /reports/{reportId}

Report View (/reports/{reportId})
  └── [Back] ─────────────────────→ /reports
```

---

## 全部接口汇总（按模块）

| 模块 | 接口数 | 接口列表 |
|------|--------|----------|
| Dashboard | 6 | `GET /dashboard/stats`, `GET /dashboard/recent`, `GET /dashboard/findings`, `GET /dashboard/vulnerability-types`, `GET /dashboard/agent-tasks`, `GET /dashboard/activity-feed` |
| Scans | 9 | `GET /scans`, `POST /scans`, `GET /scans/{id}`, `POST /scans/{id}/start`, `POST /scans/{id}/stop`, `POST /scans/{id}/pause`, `POST /scans/{id}/resume`, `DELETE /scans/{id}`, `POST /scans/{id}/skip-to/{phase}`, `GET /scans/{id}/endpoints`, `GET /scans/{id}/vulnerabilities` |
| Targets | 3 | `POST /targets/validate`, `POST /targets/validate/bulk`, `POST /targets/upload` |
| Agent | 14 | `POST /agent/run`, `GET /agent/status/{id}`, `GET /agent/by-scan/{scanId}`, `GET /agent/logs/{id}`, `GET /agent/findings/{id}`, `DELETE /agent/{id}`, `POST /agent/stop/{id}`, `POST /agent/pause/{id}`, `POST /agent/resume/{id}`, `POST /agent/skip-to/{id}/{phase}`, `POST /agent/prompt/{id}`, `GET /agent/active`, `POST /agent/quick`, `GET /agent/vuln-agents/{id}`, `GET /agent/history`, `POST /agent/triple-check/{scanId}` |
| Agent Tasks | 5 | `GET /agent/tasks`, `GET /agent/tasks/{id}`, `POST /agent/tasks`, `DELETE /agent/tasks/{id}`, `GET /agent-tasks/summary`, `GET /agent-tasks/scan/{id}/timeline` |
| Realtime | 9 | `POST /agent/realtime/session`, `POST /agent/realtime/{id}/message`, `GET /agent/realtime/{id}`, `GET /agent/realtime/{id}/report`, `DELETE /agent/realtime/{id}`, `GET /agent/realtime/sessions/list`, `GET /agent/realtime/llm-status`, `GET /agent/realtime/tools/list`, `GET /agent/realtime/tools/status`, `POST /agent/realtime/{id}/execute-tool` |
| Providers | 10 | `GET /providers`, `GET /providers/status`, `POST /providers/detect-all`, `POST /providers/{id}/detect`, `POST /providers/{id}/connect`, `DELETE /providers/{id}/accounts/{acctId}`, `POST /providers/test/{id}/{acctId}`, `POST /providers/{id}/toggle`, `GET /providers/available-models`, `GET /providers/env`, `POST /providers/env` |
| Vuln Lab | 7 | `GET /vuln-lab/types`, `POST /vuln-lab/run`, `GET /vuln-lab/challenges`, `GET /vuln-lab/challenges/{id}`, `GET /vuln-lab/stats`, `POST /vuln-lab/challenges/{id}/stop`, `DELETE /vuln-lab/challenges/{id}`, `GET /vuln-lab/logs/{id}` |
| Terminal | 11 | `POST /terminal/session`, `GET /terminal/sessions`, `GET /terminal/sessions/{id}`, `DELETE /terminal/sessions/{id}`, `POST /terminal/sessions/{id}/message`, `POST /terminal/sessions/{id}/execute`, `POST /terminal/sessions/{id}/exploitation-path`, `GET /terminal/sessions/{id}/exploitation-path`, `GET /terminal/sessions/{id}/vpn-status`, `GET /terminal/templates`, `POST /terminal/sessions/{id}/vpn/upload`, `POST /terminal/sessions/{id}/vpn/connect`, `POST /terminal/sessions/{id}/vpn/disconnect` |
| Knowledge | 5 | `POST /knowledge/upload`, `GET /knowledge/documents`, `GET /knowledge/documents/{id}`, `DELETE /knowledge/documents/{id}`, `GET /knowledge/search`, `GET /knowledge/stats` |
| MCP | 7 | `GET /mcp/servers`, `GET /mcp/servers/{name}`, `POST /mcp/servers`, `PUT /mcp/servers/{name}`, `DELETE /mcp/servers/{name}`, `POST /mcp/servers/{name}/toggle`, `POST /mcp/servers/{name}/test`, `GET /mcp/servers/{name}/tools` |
| Scheduler | 6 | `GET /scheduler/`, `POST /scheduler/`, `DELETE /scheduler/{id}`, `POST /scheduler/{id}/pause`, `POST /scheduler/{id}/resume`, `GET /scheduler/agent-roles` |
| Reports | 7 | `GET /reports`, `GET /reports/{id}`, `POST /reports`, `POST /reports/ai-generate`, `GET /reports/{id}/view`, `GET /reports/{id}/download/{format}`, `GET /reports/{id}/download-zip`, `DELETE /reports/{id}` |
| Sandbox | 5 | `GET /sandbox/`, `GET /sandbox/{scanId}`, `DELETE /sandbox/{scanId}`, `POST /sandbox/cleanup`, `POST /sandbox/cleanup-orphans` |
| Settings | 2 | `GET /settings`, `PUT /settings` |
| Vulnerabilities | 5 | `GET /vulnerabilities/types`, `GET /vulnerabilities/{id}`, `PATCH /scans/vulnerabilities/{id}/validate`, `POST /scans/vulnerabilities/{id}/feedback`, `GET /scans/vulnerabilities/learning/stats` |
| Prompts | 6 | `GET /prompts/presets`, `GET /prompts/presets/{id}`, `POST /prompts/parse`, `GET /prompts`, `POST /prompts`, `POST /prompts/upload` |
| CLI Agent | 2 | `GET /cli-agent/providers`, `GET /cli-agent/methodologies` |
| Health | 1 | `GET /api/health` |
| **总计** | **115** | |
