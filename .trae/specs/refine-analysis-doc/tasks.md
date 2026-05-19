# Tasks

- [x] Task 1: 细化第1章 系统概览 — 补充技术栈详情、环境变量清单、启动流程
  - [x] SubTask 1.1: 读取 backend/requirements.txt 和 frontend/package.json，提取所有关键依赖及版本
  - [x] SubTask 1.2: 读取 backend/config.py，提取所有配置项和默认值
  - [x] SubTask 1.3: 读取 .env 文件，列出所有环境变量
  - [x] SubTask 1.4: 读取 backend/main.py，分析启动流程和中间件注册
  - [x] SubTask 1.5: 更新文档第1章，补充技术栈表格、环境变量表格、启动流程图

- [x] Task 2: 细化第2章 后端API接口 — 补充遗漏端点，为每个端点补充参数和响应格式
  - [x] SubTask 2.1: 读取 backend/api/v1/scans.py，补充遗漏的3个端点（skip-to, status, learning/stats），为所有端点补充请求参数和响应模型
  - [x] SubTask 2.2: 读取 backend/api/v1/agent.py，补充遗漏的16个端点（history, by-scan, triple-check, skip-to, prompts, quick, delete, realtime系列, checkpoints, tasks系列），为所有端点补充请求参数和响应模型
  - [x] SubTask 2.3: 读取 backend/api/v1/terminal.py，补充遗漏的8个端点（session详情/删除, exploitation-path, vpn系列），为所有端点补充请求参数和响应模型
  - [x] SubTask 2.4: 读取 backend/api/v1/vuln_lab.py，补充遗漏的3个端点（stats, delete challenge, logs），为所有端点补充请求参数和响应模型
  - [x] SubTask 2.5: 读取 backend/api/v1/providers.py，补充遗漏的6个端点（detect, connect, delete account, toggle, env系列），为所有端点补充请求参数和响应模型
  - [x] SubTask 2.6: 读取 backend/api/v1/reports.py，补充遗漏的1个端点（download-zip），为所有端点补充请求参数和响应模型
  - [x] SubTask 2.7: 读取其余API文件（dashboard, settings, sandbox, knowledge, mcp, scheduler, targets, vulnerabilities, prompts, full_ia, cli_agent, agent_tasks），为每个端点补充请求参数和响应模型
  - [x] SubTask 2.8: 启动后端服务，用curl逐一验证所有API端点，记录真实响应
  - [x] SubTask 2.9: 更新文档第2章，整合所有补充内容

- [x] Task 3: 细化第3章 前端页面功能 — 补充遗漏组件，补充页面间数据流转
  - [x] SubTask 3.1: 读取 TerminalAgentPage.tsx，补充VPN管理、利用路径、会话删除/详情等遗漏组件
  - [x] SubTask 3.2: 读取 ProvidersPage.tsx，补充环境变量编辑器、单提供商检测、启用/禁用切换等遗漏组件
  - [x] SubTask 3.3: 读取 RealtimeTaskPage.tsx，补充会话详情、报告生成、工具状态、检查点等遗漏组件
  - [x] SubTask 3.4: 读取 ScanDetailsPage.tsx，补充阶段跳转、扫描进度等遗漏组件
  - [x] SubTask 3.5: 读取其余14个页面文件，逐一对照代码验证组件完整性
  - [x] SubTask 3.6: 读取 Sidebar.tsx 和 App.tsx，绘制完整的页面路由图和导航结构
  - [x] SubTask 3.7: 分析页面间数据流转（创建扫描→查看详情→查看代理→生成报告），补充流转说明
  - [x] SubTask 3.8: 更新文档第3章，整合所有补充内容

- [x] Task 4: 细化第4章 完整功能测试计划 — 补充缺失模块测试用例，补充真实测试结果
  - [x] SubTask 4.1: 为沙箱管理模块补充测试用例（SAND-001~SAND-006）
  - [x] SubTask 4.2: 为知识库模块补充测试用例（KNOW-001~KNOW-008）
  - [x] SubTask 4.3: 为MCP服务器模块补充测试用例（MCP-001~MCP-007）
  - [x] SubTask 4.4: 为调度器模块补充测试用例（SCHED-001~SCHED-006）
  - [x] SubTask 4.5: 为Full IA测试模块补充测试用例（FIA-001~FIA-006）
  - [x] SubTask 4.6: 为任务库模块补充测试用例（TASK-001~TASK-006）
  - [x] SubTask 4.7: 为实时任务模块补充测试用例（REAL-001~REAL-008）
  - [x] SubTask 4.8: 为Providers模块补充测试用例（PROV-006~PROV-010）
  - [x] SubTask 4.9: 为Settings模块补充测试用例（SET-005~SET-010）
  - [x] SubTask 4.10: 启动系统，执行所有P0测试用例，记录真实测试结果
  - [x] SubTask 4.11: 更新文档第4章，整合所有补充内容

- [x] Task 5: 细化第5章 Providers与Settings大模型配置区别 — 补充环境变量编辑器、Minimax实例
  - [x] SubTask 5.1: 读取 ProvidersPage.tsx 中环境变量编辑器相关代码，补充功能说明
  - [x] SubTask 5.2: 补充 Minimax 配置实例（base_url、model、API Key配置步骤）
  - [x] SubTask 5.3: 补充 Smart Router 请求路由的详细代码级流程（含方法调用链）
  - [x] SubTask 5.4: 更新文档第5章，整合所有补充内容

- [x] Task 6: 细化第6章 后端核心架构 — 补充方法签名、调用链、遗漏模块
  - [x] SubTask 6.1: 读取 agent_base.py，补充 AgentResult 和 SpecialistAgent 的完整方法签名
  - [x] SubTask 6.2: 读取 autonomous_agent.py，补充 AutonomousAgent 的执行流程和方法调用链
  - [x] SubTask 6.3: 读取 ai_pentest_agent.py，补充 AIPentestAgent 的核心方法和LLM交互流程
  - [x] SubTask 6.4: 读取 specialist_agents.py，补充5个专家代理的完整方法签名和职责
  - [x] SubTask 6.5: 读取 vuln_engine/ 下所有文件，补充11个测试器模块的详细分析
  - [x] SubTask 6.6: 读取 rag/ 下所有文件，补充遗漏的4个模块（vectorstore, reasoning_templates, reasoning_memory, few_shot）
  - [x] SubTask 6.7: 读取 smart_router/ 下所有文件，补充遗漏的2个模块（token_extractor, token_refresher）
  - [x] SubTask 6.8: 读取遗漏的独立模块（autonomous_scanner, recon_integration, ai_prompt_processor, response_verifier）
  - [x] SubTask 6.9: 为每个模块补充关键方法签名和核心调用链
  - [x] SubTask 6.10: 更新文档第6章，整合所有补充内容

- [x] Task 7: 新增第7章 数据模型详解 — 补充所有数据库模型字段定义
  - [x] SubTask 7.1: 读取 backend/models/ 下所有模型文件
  - [x] SubTask 7.2: 为每个模型列出完整字段定义（字段名、类型、约束、默认值）
  - [x] SubTask 7.3: 绘制模型关系ER图
  - [x] SubTask 7.4: 更新文档，添加第7章

- [x] Task 8: 新增第8章 配置与部署 — 补充.env配置项和部署说明
  - [x] SubTask 8.1: 读取 .env 和 config.py，列出所有配置项
  - [x] SubTask 8.2: 补充 Docker 部署说明（如有 docker-compose.yml）
  - [x] SubTask 8.3: 补充数据库迁移说明
  - [x] SubTask 8.4: 更新文档，添加第8章

# Task Dependencies
- [Task 2] depends on [Task 1] (需要技术栈和配置信息作为基础)
- [Task 3] depends on [Task 2] (前端组件需要与API端点对应)
- [Task 4] depends on [Task 2, Task 3] (测试用例需要覆盖所有API和前端功能)
- [Task 5] depends on [Task 2] (需要Providers API的完整信息)
- [Task 6] depends on [Task 1] (需要技术栈信息)
- [Task 7] depends on [Task 6] (数据模型是架构的一部分)
- [Task 8] depends on [Task 1] (配置项来自系统概览)
- [Task 1, Task 6, Task 7, Task 8] can run in parallel
- [Task 2, Task 3] can run in parallel after Task 1
