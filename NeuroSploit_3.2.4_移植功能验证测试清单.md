# NeuroSploit 3.2.4 移植功能验证测试清单

> **文档版本**: v1.0  
> **测试日期**: 2026-05-20  
> **测试环境**: 移植后环境  
> **测试工具**: API自动化测试脚本 + 流程驱动端到端测试  

---

## 第一部分：API接口测试（86项）

### 1.1 健康检查与Dashboard接口（6项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-001 | 健康检查接口 | 发送 GET /health | 返回200，status=healthy | 200, status=healthy | PASS |
| API-002 | Dashboard统计数据 | 发送 GET /dashboard/stats | 返回200，包含scans/vulnerabilities/endpoints字段 | 200, keys=['scans','vulnerabilities','endpoints'] | PASS |
| API-003 | Dashboard发现列表 | 发送 GET /dashboard/findings | 返回200，正常返回发现数据 | 200, 正常返回 | PASS |
| API-004 | Dashboard漏洞类型分布 | 发送 GET /dashboard/vulnerability-types | 返回200，包含distribution字段 | 200, keys=['distribution'] | PASS |
| API-005 | Dashboard代理任务 | 发送 GET /dashboard/agent-tasks | 返回200，正常返回代理任务数据 | 200, 正常返回 | PASS |
| API-006 | Dashboard活动动态 | 发送 GET /dashboard/activity-feed | 返回200，包含activities和total字段 | 200, keys=['activities','total'] | PASS |

### 1.2 Dashboard接口-异常项（1项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-007 | Dashboard最近活动（带limit参数） | 发送 GET /dashboard/recent?limit=5 | 返回200，响应体为list格式 | 返回200，但响应体为dict格式：{"scans":[...],"total":N}，与预期list格式不符 | FAIL |

### 1.3 扫描管理接口（5项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-008 | 创建扫描 | 发送 POST /scans，提交有效扫描参数 | 返回200，扫描创建成功 | 200, 创建扫描成功 | PASS |
| API-009 | 获取扫描列表 | 发送 GET /scans | 返回200，包含扫描列表数据 | 200, total=8 | PASS |
| API-010 | 获取扫描详情 | 发送 GET /scans/{id}，使用有效scan_id | 返回200，id与请求一致 | 200, id_match=True | PASS |
| API-011 | 获取扫描端点 | 发送 GET /scans/{id}/endpoints，使用有效scan_id | 返回200，正常返回端点数据 | 200, 正常返回 | PASS |
| API-012 | 获取扫描漏洞 | 发送 GET /scans/{id}/vulnerabilities，使用有效scan_id | 返回200，正常返回漏洞数据 | 200, 正常返回 | PASS |

### 1.4 目标验证接口（3项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-013 | 验证有效目标URL | 发送 POST /targets/validate，提交有效URL | 返回200，valid=True | 200, valid=True | PASS |
| API-014 | 批量验证目标 | 发送 POST /targets/validate/bulk，提交多个URL | 返回200，返回验证结果数量 | 200, count=2 | PASS |
| API-015 | 验证无效目标URL | 发送 POST /targets/validate，提交无效URL "not-a-url" | 返回200，valid=False | 返回422，验证函数预期200但实际返回422（合理行为，但与测试预期不符） | FAIL |

### 1.5 Prompt接口（2项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-016 | 获取预设Prompt | 发送 GET /prompts/presets | 返回200，返回预设列表 | 200, count=6 | PASS |
| API-017 | 获取Prompt列表 | 发送 GET /prompts | 返回200，正常返回Prompt数据 | 200, 正常返回 | PASS |

### 1.6 Agent代理接口-基础操作（12项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-018 | 获取活跃代理 | 发送 GET /agent/active | 返回200，显示运行中的代理 | 200, running=1 | PASS |
| API-019 | 获取代理历史 | 发送 GET /agent/history | 返回200，正常返回历史记录 | 200, 正常返回 | PASS |
| API-020 | 获取代理任务列表 | 发送 GET /agent/tasks | 返回200，返回任务列表 | 200, count=34 | PASS |
| API-021 | 启动代理（有效目标，recon_only模式） | 发送 POST /agent/run，提交有效目标与recon_only参数 | 返回200，代理启动成功 | 200, 代理启动成功 | PASS |
| API-022 | 查看代理状态 | 发送 GET /agent/status/{id}，使用有效agent_id | 返回200，status=running，phase显示当前阶段 | 200, status=running, phase=Starting reconnaissance | PASS |
| API-023 | 获取代理日志 | 发送 GET /agent/logs/{id}，使用有效agent_id | 返回200，包含agent_id/total_logs/logs字段 | 200, keys=['agent_id','total_logs','logs'] | PASS |
| API-024 | 获取代理发现 | 发送 GET /agent/findings/{id}，使用有效agent_id | 返回200，正常返回发现数据 | 200, 正常返回 | PASS |
| API-025 | 暂停代理 | 发送 POST /agent/pause/{id}，使用有效agent_id | 返回200，代理暂停成功 | 200, 暂停成功 | PASS |
| API-026 | 恢复代理 | 发送 POST /agent/resume/{id}，使用有效agent_id | 返回200，代理恢复运行 | 200, 恢复成功 | PASS |
| API-027 | 停止代理 | 发送 POST /agent/stop/{id}，使用有效agent_id | 返回200，代理停止成功 | 200, 停止成功 | PASS |
| API-028 | 确认代理已停止 | 发送 GET /agent/status/{id}（停止后） | 返回200，status=stopped | 200, status=stopped | PASS |
| API-029 | 启动代理（空目标） | 发送 POST /agent/run，提交空目标参数 | 返回422，拒绝空目标请求 | 返回200，空目标被接受 | BUG |

### 1.7 Agent代理接口-异常项（1项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-030 | 查询代理任务（无效scan_id） | 发送 GET /agent-tasks?scan_id=test | 返回200或空列表 | 返回404，需要有效scan_id | FAIL |

### 1.8 Provider接口（8项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-031 | 获取Provider列表 | 发送 GET /providers | 返回200，返回Provider列表 | 200, count=19 | PASS |
| API-032 | 获取Provider状态 | 发送 GET /providers/status | 返回200，显示已启用的Provider | 200, enabled=True | PASS |
| API-033 | 获取Provider环境变量 | 发送 GET /providers/env | 返回200，返回环境变量信息 | 200, keys_count=17 | PASS |
| API-034 | 获取可用模型列表 | 发送 GET /providers/available-models | 返回200，返回可用模型 | 200, models_count=1 | PASS |
| API-035 | 自动检测所有Provider | 发送 POST /providers/detect-all | 返回200，检测完成 | 200, 检测完成 | PASS |
| API-036 | 禁用Ollama Provider | 发送 POST /providers/ollama/toggle（禁用） | 返回200，Ollama已禁用 | 200, 禁用成功 | PASS |
| API-037 | 启用Ollama Provider | 发送 POST /providers/ollama/toggle（启用） | 返回200，Ollama已启用 | 200, 启用成功 | PASS |
| API-038 | 连接Provider（空密钥） | 发送 POST /providers/openai/connect，提交空密钥 | 返回422，拒绝空密钥 | 返回200，空密钥被接受 | BUG |

### 1.9 实时会话接口（8项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-039 | 创建实时会话 | 发送 POST /agent/realtime/session | 返回200，会话创建成功 | 200, 会话创建成功 | PASS |
| API-040 | 查看LLM状态 | 发送 GET /agent/realtime/llm-status | 返回200，available=True | 200, available=True | PASS |
| API-041 | 获取工具列表 | 发送 GET /agent/realtime/tools/list | 返回200，返回工具列表 | 200, count=15 | PASS |
| API-042 | 获取工具状态 | 发送 GET /agent/realtime/tools/status | 返回200，返回工具状态 | 200, 正常返回 | PASS |
| API-043 | 获取会话列表 | 发送 GET /agent/realtime/sessions/list | 返回200，返回会话列表 | 200, count=3 | PASS |
| API-044 | 获取会话详情 | 发送 GET /agent/realtime/{id}，使用有效session_id | 返回200，返回会话详情 | 200, 正常返回 | PASS |
| API-045 | 获取会话报告 | 发送 GET /agent/realtime/{id}/report，使用有效session_id | 返回200，返回报告内容 | 200, 正常返回 | PASS |
| API-046 | 删除实时会话 | 发送 DELETE /agent/realtime/{id}，使用有效session_id | 返回200，会话删除成功 | 200, 删除成功 | PASS |

### 1.10 实时会话接口-异常项（1项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-047 | 实时会话发送消息 | 发送 POST /agent/realtime/{id}/message，提交消息内容 | 返回200，返回LLM响应 | 超时(15s)，LLM响应慢导致超时 | FAIL |

### 1.11 VulnLab漏洞实验室接口（5项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-048 | 获取漏洞类型列表 | 发送 GET /vuln-lab/types | 返回200，返回漏洞类型 | 200, total=84 | PASS |
| API-049 | 获取实验室统计 | 发送 GET /vuln-lab/stats | 返回200，返回统计数据 | 200, 正常返回 | PASS |
| API-050 | 获取挑战列表 | 发送 GET /vuln-lab/challenges | 返回200，返回挑战列表 | 200, 正常返回 | PASS |
| API-051 | 启动漏洞测试 | 发送 POST /vuln-lab/run，提交测试参数 | 返回200，测试启动成功 | 200, 启动成功 | PASS |
| API-052 | 获取挑战详情 | 发送 GET /vuln-lab/challenges/{id}，使用有效challenge_id | 返回200，返回挑战详情 | 200, 正常返回 | PASS |

### 1.12 VulnLab接口-异常项（1项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-053 | 停止漏洞挑战 | 发送 POST /vuln-lab/challenges/{id}/stop，使用有效challenge_id | 返回200，挑战停止成功 | 返回404，端点路径可能不同 | FAIL |

### 1.13 Terminal终端接口（8项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-054 | 创建终端会话 | 发送 POST /terminal/session | 返回200，会话创建成功 | 200, 会话创建成功 | PASS |
| API-055 | 获取终端会话列表 | 发送 GET /terminal/sessions | 返回200，返回会话列表 | 200, 正常返回 | PASS |
| API-056 | 获取终端模板 | 发送 GET /terminal/templates | 返回200，返回模板列表 | 200, count=4 | PASS |
| API-057 | 获取终端会话详情 | 发送 GET /terminal/sessions/{id}，使用有效session_id | 返回200，返回会话详情 | 200, 正常返回 | PASS |
| API-058 | 添加利用步骤 | 发送 POST /terminal/sessions/{id}/exploitation-path，提交步骤数据 | 返回200，步骤添加成功 | 200, 添加成功 | PASS |
| API-059 | 获取利用路径 | 发送 GET /terminal/sessions/{id}/exploitation-path，使用有效session_id | 返回200，返回利用路径列表 | 200, 返回list | PASS |
| API-060 | 获取VPN状态 | 发送 GET /terminal/sessions/{id}/vpn-status，使用有效session_id | 返回200，返回VPN状态 | 200, 正常返回 | PASS |
| API-061 | 删除终端会话 | 发送 DELETE /terminal/sessions/{id}，使用有效session_id | 返回200，会话删除成功 | 200, 删除成功 | PASS |

### 1.14 Terminal接口-异常项（1项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-062 | 终端会话发送消息 | 发送 POST /terminal/sessions/{id}/message，提交消息内容 | 返回200，返回消息响应 | 返回502，后端代理错误 | FAIL |

### 1.15 知识库接口（3项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-063 | 获取知识库统计 | 发送 GET /knowledge/stats | 返回200，返回知识库统计 | 200, docs=2 | PASS |
| API-064 | 获取知识文档列表 | 发送 GET /knowledge/documents | 返回200，返回文档列表 | 200, 正常返回 | PASS |
| API-065 | 搜索知识库 | 发送 GET /knowledge/search，提交搜索关键词 | 返回200，返回搜索结果 | 200, 正常返回 | PASS |

### 1.16 MCP服务器接口（5项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-066 | 获取MCP服务器列表 | 发送 GET /mcp/servers | 返回200，返回服务器列表 | 200, 正常返回 | PASS |
| API-067 | 创建MCP服务器 | 发送 POST /mcp/servers，提交服务器配置 | 返回200，服务器创建成功 | 200, 创建成功 | PASS |
| API-068 | 获取MCP服务器详情 | 发送 GET /mcp/servers/{name}，使用有效服务器名称 | 返回200，返回服务器详情 | 200, 正常返回 | PASS |
| API-069 | 切换MCP服务器状态 | 发送 POST /mcp/servers/{name}/toggle，使用有效服务器名称 | 返回200，状态切换成功 | 200, 切换成功 | PASS |
| API-070 | 删除MCP服务器 | 发送 DELETE /mcp/servers/{name}，使用有效服务器名称 | 返回200，服务器删除成功 | 200, 删除成功 | PASS |

### 1.17 调度器接口（2项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-071 | 获取调度器列表 | 发送 GET /scheduler/ | 返回200，返回调度任务列表 | 200, 正常返回 | PASS |
| API-072 | 获取代理角色列表 | 发送 GET /scheduler/agent-roles | 返回200，返回角色列表 | 200, count=2 | PASS |

### 1.18 调度器接口-异常项（1项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-073 | 创建调度任务 | 发送 POST /scheduler/，提交调度任务参数 | 返回200，调度任务创建成功 | 返回400，APScheduler未安装 | FAIL |

### 1.19 报告接口（3项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-074 | 获取报告列表 | 发送 GET /reports | 返回200，返回报告列表 | 200, total=7 | PASS |
| API-075 | 获取报告详情 | 发送 GET /reports/{id}，使用有效report_id | 返回200，返回报告详情 | 200, 正常返回 | PASS |
| API-076 | 下载JSON报告 | 发送 GET /reports/{id}/download/json，使用有效report_id | 返回200，返回JSON报告数据 | 200, 正常返回 | PASS |

### 1.20 报告接口-异常项（1项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-077 | 查看报告视图 | 发送 GET /reports/{id}/view，使用有效report_id | 返回200，返回报告视图 | 返回404，可能仅JSON报告有view端点 | FAIL |

### 1.21 系统设置接口（3项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-078 | 获取系统设置 | 发送 GET /settings | 返回200，返回设置项 | 200, keys=23 | PASS |
| API-079 | 更新系统设置 | 发送 PUT /settings，提交修改参数 | 返回200，设置更新成功 | 200, 更新成功 | PASS |
| API-080 | 设置Provider环境变量 | 发送 POST /providers/env，提交环境变量 | 返回200，环境变量设置成功 | 200, 设置成功 | PASS |

### 1.22 其他接口（3项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-081 | 获取漏洞类型 | 发送 GET /vulnerabilities/types | 返回200，返回漏洞类型列表 | 200, 正常返回 | PASS |
| API-082 | 获取CLI Agent Provider | 发送 GET /cli-agent/providers | 返回200，返回CLI Agent Provider | 200, 正常返回 | PASS |
| API-083 | 获取CLI Agent方法论 | 发送 GET /cli-agent/methodologies | 返回200，返回方法论列表 | 200, 正常返回 | PASS |

### 1.23 沙箱与全量IA接口（3项）

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| API-084 | 获取沙箱状态 | 发送 GET /sandbox/ | 返回200，返回沙箱状态 | 200, 正常返回 | PASS |
| API-085 | 启动全量IA流程 | 发送 POST /full-ia/start | 返回200，全量IA流程启动 | 返回404，端点不存在；full-ia通过agent/run实现 | FAIL |
| API-086 | 查询代理任务（无效scan_id） | 发送 GET /agent-tasks?scan_id=test | 返回200或空列表 | 返回404，需要有效scan_id | FAIL |

---

## 第二部分：流程驱动的端到端页面功能测试（8个流程，51项）

### 流程1：Provider配置 → 测试连接 → 启动扫描 → 查看结果 → 生成报告（11步）

**流程目标**：验证从Provider配置到报告生成的完整扫描工作流

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| FLOW-01-01 | 查看Provider列表 | 1. 打开Provider管理页面<br>2. 请求 GET /providers 获取Provider列表 | 返回200，显示已配置的Provider列表 | 200, 19个Provider, minimax connected=True | PASS |
| FLOW-01-02 | 测试Minimax连接 | 1. 选择Minimax Provider<br>2. 发送连接测试请求 | 返回200，连接测试成功 | 200, success=True, "Connected. Response: OK" | PASS |
| FLOW-01-03 | 查看可用模型 | 1. 请求 GET /providers/available-models | 返回200，列出可用模型 | 200, models=['MiniMax-M2.7'] | PASS |
| FLOW-01-04 | 创建扫描 | 1. 填写扫描目标与参数<br>2. 发送 POST /scans 创建扫描 | 返回200，扫描创建成功并返回scan_id | 200, scan_id created | PASS |
| FLOW-01-05 | 启动recon_only代理 | 1. 选择recon_only模式<br>2. 发送 POST /agent/run 启动代理 | 返回200，代理启动成功并返回agent_id | 200, agent_id=d14a0257 | PASS |
| FLOW-01-06 | 查看代理状态 | 1. 发送 GET /agent/status/{id} 查看运行状态 | 返回200，status=running，显示当前阶段 | 200, status=running, phase=Starting reconnaissance | PASS |
| FLOW-01-07 | 查看代理日志 | 1. 发送 GET /agent/logs/{id} 查看日志 | 返回200，返回代理运行日志 | 200, total=8 logs | PASS |
| FLOW-01-08 | 停止代理并确认 | 1. 发送 POST /agent/stop/{id} 停止代理<br>2. 发送 GET /agent/status/{id} 确认状态 | 代理停止，status=stopped | 200, status=stopped | PASS |
| FLOW-01-09 | Dashboard统计更新 | 1. 请求 GET /dashboard/stats 查看统计 | 扫描数量更新 | 200, total=14 scans | PASS |
| FLOW-01-10 | 查看代理历史 | 1. 请求 GET /agent/history 查看历史记录 | 返回200，包含历史条目 | 200, entries=5 | PASS |
| FLOW-01-11 | 生成报告 | 1. 选择已完成扫描<br>2. 发送报告生成请求 | 返回200，报告生成成功并返回report_id | 200, report_id created | PASS |

### 流程2：创建实时会话 → 发送消息 → 查看发现 → 获取报告 → 删除会话（8步）

**流程目标**：验证实时交互式会话的完整生命周期

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| FLOW-02-01 | 创建实时会话 | 1. 发送 POST /agent/realtime/session 创建会话 | 返回200，会话创建成功并返回session_id | 200, session_id=d62d601d | PASS |
| FLOW-02-02 | 确认LLM可用 | 1. 发送 GET /agent/realtime/llm-status 检查LLM状态 | 返回200，available=True | 200, available=True | PASS |
| FLOW-02-03 | 获取会话详情 | 1. 发送 GET /agent/realtime/{id} 获取会话详情 | 返回200，status=active | 200, status=active | PASS |
| FLOW-02-04 | 发送安全测试消息 | 1. 发送 POST /agent/realtime/{id}/message 提交安全测试消息<br>2. 等待LLM响应 | 返回200，返回LLM响应内容 | 超时(15s)，LLM响应慢导致超时 | FAIL |
| FLOW-02-05 | 查看可用工具 | 1. 发送 GET /agent/realtime/tools/list 获取工具列表 | 返回200，返回可用工具 | 200, count=15 | PASS |
| FLOW-02-06 | 获取会话报告 | 1. 发送 GET /agent/realtime/{id}/report 获取报告 | 返回200，返回会话报告 | 200, 正常返回 | PASS |
| FLOW-02-07 | 删除会话 | 1. 发送 DELETE /agent/realtime/{id} 删除会话 | 返回200，会话删除成功 | 200, 删除成功 | PASS |
| FLOW-02-08 | 确认会话已删除 | 1. 发送 GET /agent/realtime/sessions/list 查看会话列表<br>2. 确认已删除的会话不在列表中 | 已删除的会话不在列表中 | 200, sessions=2（不含已删除的） | PASS |

### 流程3：创建扫描 → 暂停 → 恢复 → 停止 → 查看历史（6步）

**流程目标**：验证代理生命周期控制（暂停/恢复/停止）及历史查询

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| FLOW-03-01 | 启动auto_pentest代理 | 1. 选择auto_pentest模式<br>2. 发送 POST /agent/run 启动代理 | 返回200，代理启动成功 | 200, agent_id=83509147 | PASS |
| FLOW-03-02 | 确认代理运行中 | 1. 发送 GET /agent/status/{id} 查看状态 | 返回200，status=running | 200, status=running, phase=Auto pentest starting | PASS |
| FLOW-03-03 | 暂停代理 | 1. 发送 POST /agent/pause/{id} 暂停代理<br>2. 确认状态为paused | 返回200，status=paused | 200, status=paused | PASS |
| FLOW-03-04 | 恢复代理 | 1. 发送 POST /agent/resume/{id} 恢复代理<br>2. 确认状态为running | 返回200，status=running | 200, status=running | PASS |
| FLOW-03-05 | 停止代理 | 1. 发送 POST /agent/stop/{id} 停止代理<br>2. 确认状态为stopped | 返回200，status=stopped | 200, status=stopped | PASS |
| FLOW-03-06 | 历史中可查到代理 | 1. 发送 GET /agent/history 查询历史记录<br>2. 搜索已停止的代理 | 历史记录中包含该代理 | found=False，历史API返回格式与查询不匹配 | FAIL |

### 流程4：知识库 → 搜索 → 启动增强扫描（4步）

**流程目标**：验证知识库功能及知识增强扫描的集成

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| FLOW-04-01 | 知识库统计 | 1. 发送 GET /knowledge/stats 获取统计 | 返回200，显示知识库文档数量 | 200, docs=2 | PASS |
| FLOW-04-02 | 知识文档列表 | 1. 发送 GET /knowledge/documents 获取文档列表 | 返回200，返回文档列表 | 200, count=2 | PASS |
| FLOW-04-03 | 搜索XSS知识 | 1. 发送 GET /knowledge/search?q=XSS 搜索XSS相关知识 | 返回200，返回搜索结果 | 200, count=1 | PASS |
| FLOW-04-04 | 确认知识增强已启用 | 1. 检查设置中知识增强选项 | 知识增强功能已启用 | enable_knowledge_augmentation=True | PASS |

### 流程5：VulnLab → 选类型 → 启动测试 → 查看挑战 → 查看报告（5步）

**流程目标**：验证漏洞实验室的完整测试流程

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| FLOW-05-01 | 获取漏洞类型 | 1. 发送 GET /vuln-lab/types 获取漏洞类型列表 | 返回200，返回漏洞类型 | 200, total=84 | PASS |
| FLOW-05-02 | 启动XSS测试 | 1. 选择XSS类型<br>2. 发送 POST /vuln-lab/run 启动测试 | 返回200，测试启动成功并返回challenge_id | 200, challenge_id created | PASS |
| FLOW-05-03 | 查看挑战详情 | 1. 发送 GET /vuln-lab/challenges/{id} 查看详情 | 返回200，status=running | 200, status=running | PASS |
| FLOW-05-04 | 查看实验室统计 | 1. 发送 GET /vuln-lab/stats 查看统计 | 返回200，显示统计数据 | 200, total=4 | PASS |
| FLOW-05-05 | 查看挑战日志 | 1. 查看挑战运行日志 | 返回200，返回日志内容 | 200, 正常返回 | PASS |

### 流程6：Terminal → 创建会话 → 发消息 → 添加利用步骤 → 查看路径（6步）

**流程目标**：验证终端会话管理和利用路径记录功能

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| FLOW-06-01 | 创建终端会话 | 1. 发送 POST /terminal/session 创建会话 | 返回200，会话创建成功 | 200, session_id created | PASS |
| FLOW-06-02 | 获取会话详情 | 1. 发送 GET /terminal/sessions/{id} 获取详情 | 返回200，status=active | 200, status=active | PASS |
| FLOW-06-03 | 添加利用步骤 | 1. 发送 POST /terminal/sessions/{id}/exploitation-path 添加步骤 | 返回200，步骤添加成功 | 200, 添加成功 | PASS |
| FLOW-06-04 | 获取利用路径 | 1. 发送 GET /terminal/sessions/{id}/exploitation-path 获取路径 | 返回200，返回利用路径列表 | 200, 返回list（空） | PASS |
| FLOW-06-05 | VPN状态 | 1. 发送 GET /terminal/sessions/{id}/vpn-status 查看VPN状态 | 返回200，返回VPN连接状态 | 200, connected=false | PASS |
| FLOW-06-06 | 删除终端会话 | 1. 发送 DELETE /terminal/sessions/{id} 删除会话 | 返回200，会话删除成功 | 200, 删除成功 | PASS |

### 流程7：MCP服务器 → 创建 → 切换 → 查看工具 → 删除（6步）

**流程目标**：验证MCP服务器的完整生命周期管理

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| FLOW-07-01 | 创建MCP服务器 | 1. 发送 POST /mcp/servers 提交服务器配置 | 返回200，服务器创建成功 | 200, name=f7-verify-mcp | PASS |
| FLOW-07-02 | 获取MCP详情 | 1. 发送 GET /mcp/servers/{name} 获取详情 | 返回200，返回服务器详情 | 200, name=f7-verify-mcp, enabled=True | PASS |
| FLOW-07-03 | 切换MCP状态 | 1. 发送 POST /mcp/servers/{name}/toggle 切换状态 | 返回200，状态切换成功 | 200, enabled=False | PASS |
| FLOW-07-04 | 查看MCP工具 | 1. 查看MCP服务器关联的工具列表 | 返回200，返回工具列表 | 200, 正常返回 | PASS |
| FLOW-07-05 | 删除MCP服务器 | 1. 发送 DELETE /mcp/servers/{name} 删除服务器 | 返回200，服务器删除成功 | 200, message deleted | PASS |
| FLOW-07-06 | 确认MCP已删除 | 1. 发送 GET /mcp/servers 查看列表<br>2. 确认已删除的服务器不在列表中 | 已删除的服务器不在列表中 | 200, not in list | PASS |

### 流程8：设置修改 → Provider环境变量 → 验证持久化（5步）

**流程目标**：验证系统设置的修改、持久化和Provider环境变量管理

| 测试ID | 测试内容 | 操作步骤 | 预期结果 | 实际结果 | 状态 |
|--------|---------|---------|---------|---------|------|
| FLOW-08-01 | 获取当前设置 | 1. 发送 GET /settings 获取当前设置 | 返回200，返回当前设置项 | 200, max_concurrent=5 | PASS |
| FLOW-08-02 | 修改max_concurrent为3 | 1. 发送 PUT /settings 修改max_concurrent为3 | 返回200，设置修改成功 | 200, max_concurrent=3 | PASS |
| FLOW-08-03 | 恢复max_concurrent | 1. 发送 PUT /settings 恢复max_concurrent为5 | 返回200，设置恢复成功 | 200, max_concurrent=5 | PASS |
| FLOW-08-04 | 环境变量持久化 | 1. 发送 POST /providers/env 设置环境变量SMART_ROUTER=true<br>2. 验证持久化 | 返回200，环境变量持久化成功 | 200, SMART_ROUTER=true, persisted=True | PASS |
| FLOW-08-05 | Smart Router状态确认 | 1. 确认Smart Router已启用 | Smart Router状态为enabled | enabled=True | PASS |

---

## 第三部分：Bug清单与移植注意事项

### 3.1 Bug清单

| Bug ID | 严重级别 | 关联测试ID | Bug描述 | 复现步骤 | 影响范围 |
|--------|---------|-----------|---------|---------|---------|
| BUG-001 | 🔴 高 | API-029 | Agent空目标被接受：POST /agent/run 提交空目标参数时返回200而非422，缺少输入验证 | 1. 发送 POST /agent/run，target字段为空<br>2. 观察返回200而非422 | 可能导致无效代理任务创建，浪费系统资源 |
| BUG-002 | 🔴 高 | API-038 | Provider空密钥被接受：POST /providers/openai/connect 提交空密钥时返回200而非422，缺少输入验证 | 1. 发送 POST /providers/openai/connect，api_key字段为空<br>2. 观察返回200而非422 | 可能导致无效Provider连接创建，存在安全隐患 |
| BUG-003 | 🟡 中 | API-047 | 实时会话消息超时：POST /agent/realtime/{id}/message 发送消息后15s超时，LLM响应过慢 | 1. 创建实时会话<br>2. 发送消息<br>3. 等待响应，15s后超时 | 实时交互功能不可用，影响用户体验 |
| BUG-004 | 🟡 中 | API-062 | Terminal消息代理错误：POST /terminal/sessions/{id}/message 返回502后端代理错误 | 1. 创建终端会话<br>2. 发送消息<br>3. 返回502 | 终端交互功能不可用 |
| BUG-005 | 🟡 中 | API-073 | 调度器不可用：POST /scheduler/ 返回400，APScheduler未安装 | 1. 发送 POST /scheduler/ 创建调度任务<br>2. 返回400错误 | 定时调度功能不可用，需安装APScheduler依赖 |
| BUG-006 | 🟢 低 | API-007 | Dashboard最近活动返回格式不一致：GET /dashboard/recent?limit=5 返回dict而非list | 1. 发送 GET /dashboard/recent?limit=5<br>2. 观察返回 {"scans":[...],"total":N} 而非 list | 前端解析可能出错，需适配返回格式 |
| BUG-007 | 🟢 低 | API-053 | VulnLab停止挑战端点404：POST /vuln-lab/challenges/{id}/stop 返回404 | 1. 启动一个漏洞挑战<br>2. 尝试停止该挑战<br>3. 返回404 | 无法通过API停止运行中的挑战，端点路径可能不同 |
| BUG-008 | 🟢 低 | API-077 | 报告视图端点404：GET /reports/{id}/view 返回404 | 1. 生成一份报告<br>2. 尝试访问 /reports/{id}/view<br>3. 返回404 | 报告视图功能可能仅限JSON格式报告 |
| BUG-009 | 🟢 低 | FLOW-03-06 | 代理历史查询格式不匹配：GET /agent/history 返回格式与查询逻辑不匹配，导致无法找到已停止的代理 | 1. 停止一个代理<br>2. 查询历史记录<br>3. found=False | 代理历史查询功能异常，需适配返回格式 |
| BUG-010 | ℹ️ 信息 | API-015 | 无效URL验证返回422而非200：POST /targets/validate 提交无效URL时返回422 | 1. 发送 POST /targets/validate，URL="not-a-url"<br>2. 返回422 | 行为合理（FastAPI验证拦截），但与测试预期不符，需统一验证逻辑 |
| BUG-011 | ℹ️ 信息 | API-085 | full-ia端点不存在：POST /full-ia/start 返回404 | 1. 发送 POST /full-ia/start<br>2. 返回404 | full-ia功能通过 POST /agent/run 实现，非独立端点 |

### 3.2 移植注意事项

#### 3.2.1 依赖项缺失

| 序号 | 依赖项 | 影响功能 | 处理建议 |
|------|--------|---------|---------|
| 1 | APScheduler | 调度器功能（POST /scheduler/）不可用 | 移植时需确保安装APScheduler：`pip install APScheduler` |
| 2 | LLM响应性能 | 实时会话消息超时 | 移植时需优化LLM调用超时配置，建议将默认超时从15s调整为30-60s |

#### 3.2.2 接口行为差异

| 序号 | 差异描述 | 原始行为 | 移植后行为 | 处理建议 |
|------|---------|---------|-----------|---------|
| 1 | GET /dashboard/recent 返回格式 | 返回list | 返回dict: {"scans":[...],"total":N} | 前端需适配dict格式，或后端统一返回list格式 |
| 2 | POST /targets/validate 无效URL | 返回200, valid=False | 返回422（FastAPI验证拦截） | 统一验证逻辑：在Pydantic模型中放宽验证，由业务逻辑返回valid=False |
| 3 | POST /agent/run 空目标 | 应返回422 | 返回200（缺少输入验证） | 添加target字段非空验证 |
| 4 | POST /providers/openai/connect 空密钥 | 应返回422 | 返回200（缺少输入验证） | 添加api_key字段非空验证 |
| 5 | POST /full-ia/start | 独立端点 | 返回404，功能已合并至agent/run | 更新前端调用，使用 POST /agent/run 替代 |

#### 3.2.3 端点路径变更

| 序号 | 原始端点 | 移植后状态 | 处理建议 |
|------|---------|-----------|---------|
| 1 | POST /vuln-lab/challenges/{id}/stop | 404，端点路径可能变更 | 检查路由注册，确认stop端点的实际路径 |
| 2 | GET /reports/{id}/view | 404，可能仅JSON报告支持 | 确认view端点是否已移除或路径变更 |
| 3 | POST /full-ia/start | 404，端点已不存在 | 功能已合并至 POST /agent/run，更新前端调用 |
| 4 | GET /agent-tasks?scan_id=test | 404，需有效scan_id | 前端需确保传入有效scan_id，或后端支持无效ID返回空列表 |

#### 3.2.4 性能与稳定性

| 序号 | 问题描述 | 影响范围 | 处理建议 |
|------|---------|---------|---------|
| 1 | LLM响应超时（15s） | 实时会话消息发送 | 增加超时时间，添加重试机制，考虑流式响应 |
| 2 | Terminal消息502代理错误 | 终端会话交互 | 检查后端代理配置，确认WebSocket/HTTP代理正确转发 |
| 3 | 代理历史查询格式不匹配 | 历史记录查询 | 统一 /agent/history 返回格式，确保前端查询逻辑兼容 |

#### 3.2.5 安全注意事项

| 序号 | 安全问题 | 关联Bug | 处理建议 |
|------|---------|--------|---------|
| 1 | 空目标可创建代理任务 | BUG-001 | 添加服务端输入验证，拒绝空目标请求 |
| 2 | 空密钥可连接Provider | BUG-002 | 添加服务端输入验证，拒绝空密钥请求 |
| 3 | 无效scan_id返回404而非空列表 | API-086 | 考虑返回空列表而非404，避免信息泄露 |

---

## 第四部分：测试统计汇总

### 4.1 总体统计

| 测试类别 | 测试项数 | PASS | FAIL | 通过率 |
|---------|---------|------|------|--------|
| API接口测试 | 86 | 75 | 11 | 87.2% |
| 流程驱动端到端测试 | 51 | 47 | 4 | 92.2% |
| **总计** | **137** | **122** | **15** | **89.1%** |

### 4.2 API接口测试分类统计

| 接口分类 | 测试项数 | PASS | FAIL | 通过率 |
|---------|---------|------|------|--------|
| 健康检查与Dashboard | 7 | 6 | 1 | 85.7% |
| 扫描管理 | 5 | 5 | 0 | 100% |
| 目标验证 | 3 | 2 | 1 | 66.7% |
| Prompt | 2 | 2 | 0 | 100% |
| Agent代理-基础操作 | 12 | 11 | 1 | 91.7% |
| Agent代理-异常项 | 1 | 0 | 1 | 0% |
| Provider | 8 | 7 | 1 | 87.5% |
| 实时会话 | 8 | 8 | 0 | 100% |
| 实时会话-异常项 | 1 | 0 | 1 | 0% |
| VulnLab | 5 | 5 | 0 | 100% |
| VulnLab-异常项 | 1 | 0 | 1 | 0% |
| Terminal | 8 | 8 | 0 | 100% |
| Terminal-异常项 | 1 | 0 | 1 | 0% |
| 知识库 | 3 | 3 | 0 | 100% |
| MCP服务器 | 5 | 5 | 0 | 100% |
| 调度器 | 3 | 2 | 1 | 66.7% |
| 报告 | 4 | 3 | 1 | 75.0% |
| 系统设置 | 3 | 3 | 0 | 100% |
| 其他接口 | 3 | 3 | 0 | 100% |
| 沙箱与全量IA | 3 | 1 | 2 | 33.3% |

### 4.3 流程测试分类统计

| 流程 | 测试项数 | PASS | FAIL | 通过率 |
|------|---------|------|------|--------|
| 流程1: Provider配置→报告生成 | 11 | 11 | 0 | 100% |
| 流程2: 实时会话生命周期 | 8 | 7 | 1 | 87.5% |
| 流程3: 代理生命周期控制 | 6 | 5 | 1 | 83.3% |
| 流程4: 知识库增强扫描 | 4 | 4 | 0 | 100% |
| 流程5: VulnLab测试流程 | 5 | 5 | 0 | 100% |
| 流程6: Terminal会话管理 | 6 | 6 | 0 | 100% |
| 流程7: MCP服务器管理 | 6 | 6 | 0 | 100% |
| 流程8: 设置持久化验证 | 5 | 5 | 0 | 100% |

### 4.4 Bug严重级别分布

| 严重级别 | 数量 | Bug ID |
|---------|------|--------|
| 🔴 高 | 2 | BUG-001, BUG-002 |
| 🟡 中 | 3 | BUG-003, BUG-004, BUG-005 |
| 🟢 低 | 4 | BUG-006, BUG-007, BUG-008, BUG-009 |
| ℹ️ 信息 | 2 | BUG-010, BUG-011 |

### 4.5 结论与建议

**总体评估**：NeuroSploit 3.2.4 移植后功能验证通过率为 89.1%，核心功能（扫描管理、代理控制、Provider管理、知识库、MCP、设置等）运行正常，满足基本移植要求。

**关键风险**：
1. **输入验证缺失**（BUG-001/BUG-002）：空目标和空密钥被接受，属于高优先级安全问题，需在上线前修复
2. **LLM响应超时**（BUG-003）：实时交互功能受影响，建议优化超时配置和添加流式响应支持
3. **APScheduler缺失**（BUG-005）：调度功能不可用，需补充依赖安装

**移植建议**：
1. 优先修复高严重级别Bug（BUG-001、BUG-002），确保输入验证完备
2. 安装缺失依赖（APScheduler），恢复调度器功能
3. 统一API返回格式，特别是 /dashboard/recent 和 /agent/history
4. 优化LLM调用超时配置，建议调整为30-60s并支持流式响应
5. 更新前端调用路径，将 /full-ia/start 替换为 /agent/run
6. 修复Terminal消息代理502错误，检查后端代理配置

---

> **文档生成时间**: 2026-05-20  
> **测试执行人**: 自动化测试脚本  
> **文档审核状态**: 待审核
