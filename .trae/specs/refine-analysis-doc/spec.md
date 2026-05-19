# NeuroSploit 3.2.4 全面分析文档细化 Spec

## Why
当前分析文档 `NeuroSploit_3.2.4_全面分析文档_大模型分析的.md` 存在多处内容不完整、与实际代码不一致的问题。经对照代码和运行时验证，发现：API端点遗漏约30+个、前端页面组件/按钮遗漏约20+个、后端核心模块描述过于简略缺少关键方法签名和调用链、测试计划缺少多个模块的测试用例。需要逐章细化，确保所有内容与真实代码和运行情况一致。

## What Changes
- **第1章 系统概览**: 补充系统技术栈详情（Python版本、FastAPI版本、React版本、关键依赖版本）、补充环境变量配置清单、补充启动流程和端口说明
- **第2章 后端API接口**: 补充遗漏的30+个API端点（详见下方遗漏清单），为每个端点补充请求参数和响应格式
- **第3章 前端页面功能**: 补充遗漏的页面组件和按钮（VPN管理、利用路径、环境变量编辑器等），补充页面间数据流转详细说明
- **第4章 完整功能测试计划**: 补充缺失模块的测试用例（沙箱、知识库、MCP、调度器、Full IA、任务库、实时任务等），补充真实API测试结果
- **第5章 Providers与Settings大模型配置区别**: 补充环境变量编辑器功能说明、补充Minimax配置实例
- **第6章 后端核心架构**: 为每个模块补充关键方法签名、调用链、核心算法逻辑；补充遗漏的模块（vuln_engine/testers/下11个测试器、rag/下5个模块、smart_router/下token_extractor和token_refresher等）
- **新增第7章 数据模型详解**: 补充所有数据库模型的字段定义、关系图、索引信息
- **新增第8章 配置与部署**: 补充.env完整配置项、Docker部署方式、数据库迁移

### 遗漏的API端点清单

#### Scans API 遗漏:
- POST `/{scan_id}/skip-to/{target_phase}` — 跳转到指定扫描阶段
- GET `/{scan_id}/status` — 获取扫描进度（ScanProgress模型）
- GET `/vulnerabilities/learning/stats` — 获取自适应学习统计

#### Agent API 遗漏:
- GET `/history` — 获取代理历史记录
- GET `/by-scan/{scan_id}` — 按扫描ID查找代理
- POST `/triple-check/{scan_id}` — 三重验证扫描结果
- POST `/skip-to/{agent_id}/{target_phase}` — 跳转到指定代理阶段
- GET `/prompts/{agent_id}` — 获取代理提示词历史
- POST `/quick` — 快速运行代理
- DELETE `/{agent_id}` — 删除代理结果
- GET `/realtime/llm-status` — 获取LLM连接状态
- GET `/realtime/{session_id}` — 获取实时会话详情
- GET `/realtime/{session_id}/report` — 获取实时会话报告
- GET `/realtime/tools/list` — 列出实时工具
- GET `/realtime/tools/status` — 获取工具状态
- GET `/checkpoints` — 获取检查点列表
- GET `/tasks` — 获取任务列表（在agent.py中定义）
- GET `/tasks/{task_id}` — 获取特定任务
- POST `/tasks` — 创建任务
- DELETE `/tasks/{task_id}` — 删除任务

#### Terminal API 遗漏:
- GET `/sessions/{session_id}` — 获取会话详情
- DELETE `/sessions/{session_id}` — 删除会话
- POST `/sessions/{session_id}/exploitation-path` — 创建利用路径
- GET `/sessions/{session_id}/exploitation-path` — 获取利用路径
- POST `/sessions/{session_id}/vpn/upload` — 上传VPN配置
- POST `/sessions/{session_id}/vpn/connect` — 连接VPN
- POST `/sessions/{session_id}/vpn/disconnect` — 断开VPN
- GET `/sessions/{session_id}/vpn-status` — 获取VPN状态

#### Vuln Lab API 遗漏:
- GET `/stats` — 获取漏洞实验室统计
- DELETE `/challenges/{challenge_id}` — 删除挑战
- GET `/logs/{challenge_id}` — 获取挑战日志

#### Providers API 遗漏:
- POST `/{provider_id}/detect` — 检测单个提供商令牌
- POST `/{provider_id}/connect` — 连接提供商账户
- DELETE `/{provider_id}/accounts/{account_id}` — 删除账户
- POST `/{provider_id}/toggle` — 切换提供商启用状态
- GET `/env` — 获取环境变量
- POST `/env` — 更新环境变量

#### Reports API 遗漏:
- GET `/{report_id}/download-zip` — 下载ZIP格式报告

### 遗漏的前端组件/功能清单

#### TerminalAgentPage 遗漏:
- VPN管理功能（上传配置、连接、断开、状态查看）
- 利用路径（Exploitation Path）创建和查看
- 会话删除功能
- 会话详情查看

#### ProvidersPage 遗漏:
- 环境变量编辑器（GET/POST /api/v1/providers/env）
- 单个提供商令牌检测
- 提供商启用/禁用切换

#### RealtimeTaskPage 遗漏:
- 实时会话详情查看
- 实时会话报告生成
- 工具状态查看
- 检查点管理

#### ScanDetailsPage 遗漏:
- 阶段跳转功能（skip-to）
- 扫描进度获取（status端点）

### 遗漏的后端核心模块清单

#### vuln_engine/testers/ (11个测试器，文档中完全未提及):
- base_tester.py — BaseTester 基础测试器
- injection.py — 注入测试器（SQLi, XSS, Command Injection等）
- auth.py — 认证测试器
- authorization.py — 授权测试器
- client_side.py — 客户端漏洞测试器
- advanced_injection.py — 高级注入测试器
- data_exposure.py — 数据暴露测试器
- file_access.py — 文件访问测试器
- logic.py — 逻辑漏洞测试器
- request_forgery.py — 请求伪造测试器
- cloud_supply.py — 云供应链测试器
- infrastructure.py — 基础设施测试器

#### vuln_engine/ 额外模块:
- payload_generator.py — 载荷生成器（文档中列为generator.py，实际文件名不同）
- ai_prompts.py — AI提示词模板
- system_prompts.py — 系统提示词
- pentest_playbook.py — 渗透测试手册

#### rag/ 额外模块:
- vectorstore.py — 向量存储
- reasoning_templates.py — 推理模板
- reasoning_memory.py — 推理记忆
- few_shot.py — 少样本学习

#### smart_router/ 额外模块:
- token_extractor.py — Token提取器
- token_refresher.py — Token刷新器

#### 其他遗漏模块:
- autonomous_scanner.py — 自主扫描器
- recon_integration.py — 侦察集成
- ai_prompt_processor.py — AI提示处理器
- response_verifier.py — 响应验证器

## Impact
- Affected specs: 全部6个现有章节 + 2个新增章节
- Affected code: `/workspace/NeuroSploit_3.2.4_全面分析文档_大模型分析的.md`
- 预计文档从约1413行扩展到约3000+行

## ADDED Requirements

### Requirement: API端点完整性验证
文档中的每个API模块 SHALL 列出该模块路由文件中定义的所有端点，不得遗漏。每个端点 SHALL 包含：HTTP方法、路径、功能描述、请求参数（如有）、响应模型（如有）、关联前端页面。

#### Scenario: 对照代码验证API端点
- **WHEN** 读取 `/workspace/backend/api/v1/` 下所有路由文件
- **THEN** 文档中列出的端点数量 SHALL 等于代码中 `@router.get/post/put/delete/patch` 装饰器的数量

### Requirement: 前端页面组件完整性验证
文档中的每个前端页面 SHALL 列出该页面组件中所有交互元素（按钮、输入框、选择器、开关等），不得遗漏。每个组件 SHALL 包含：组件名称、功能描述、调用的API端点、事件处理逻辑。

#### Scenario: 对照代码验证前端组件
- **WHEN** 读取 `/workspace/frontend/src/pages/` 下所有页面文件
- **THEN** 文档中列出的组件/按钮 SHALL 覆盖代码中所有 onClick/handleClick/onChange 等事件处理函数

### Requirement: 后端核心模块方法签名完整性
文档中的每个后端核心模块 SHALL 列出主要类的关键方法签名和核心调用链，不得仅列出类名和一句话描述。

#### Scenario: 对照代码验证方法签名
- **WHEN** 读取 `/workspace/backend/core/` 下所有Python文件
- **THEN** 文档中列出的方法 SHALL 与代码中 `def` 定义的方法一致

### Requirement: 真实运行验证
文档中的测试结果 SHALL 基于真实的API调用，不得编造。每个API端点 SHALL 通过 `curl` 命令实际调用并记录响应。

#### Scenario: 真实API测试
- **WHEN** 执行文档中的 curl 测试命令
- **THEN** 返回的响应状态码和结构 SHALL 与文档记录一致

### Requirement: 数据模型字段完整性
新增第7章 SHALL 列出所有数据库模型的完整字段定义，包括字段名、类型、约束、默认值和关系。

#### Scenario: 对照模型文件验证字段
- **WHEN** 读取 `/workspace/backend/models/` 下所有模型文件
- **THEN** 文档中列出的字段 SHALL 与代码中 SQLAlchemy Column 定义一致

### Requirement: 配置项完整性
新增第8章 SHALL 列出 `.env` 文件中所有配置项及其说明、默认值和影响范围。

#### Scenario: 对照.env和config.py验证配置
- **WHEN** 读取 `/workspace/.env` 和 `/workspace/backend/config.py`
- **THEN** 文档中列出的配置项 SHALL 覆盖代码中所有 os.getenv/settings 引用
