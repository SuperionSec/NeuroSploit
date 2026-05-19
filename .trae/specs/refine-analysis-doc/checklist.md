# Checklist

## 第1章 系统概览
- [x] 技术栈表格包含所有关键依赖及版本号（FastAPI, React, SQLAlchemy, aiohttp等）
- [x] 环境变量清单覆盖 .env 文件中所有配置项
- [x] 启动流程描述与 main.py 中的实际启动逻辑一致
- [x] 端口说明与实际运行端口一致（后端8000，前端3001）

## 第2章 后端API接口
- [x] Scans API 端点数量与 scans.py 中 @router 装饰器数量一致
- [x] Agent API 端点数量与 agent.py 中 @router 装饰器数量一致
- [x] Terminal API 端点数量与 terminal.py 中 @router 装饰器数量一致
- [x] Vuln Lab API 端点数量与 vuln_lab.py 中 @router 装饰器数量一致
- [x] Providers API 端点数量与 providers.py 中 @router 装饰器数量一致
- [x] Reports API 端点数量与 reports.py 中 @router 装饰器数量一致
- [x] Dashboard API 端点数量与 dashboard.py 中 @router 装饰器数量一致
- [x] Settings API 端点数量与 settings.py 中 @router 装饰器数量一致
- [x] Sandbox API 端点数量与 sandbox.py 中 @router 装饰器数量一致
- [x] Knowledge API 端点数量与 knowledge.py 中 @router 装饰器数量一致
- [x] MCP API 端点数量与 mcp.py 中 @router 装饰器数量一致
- [x] Scheduler API 端点数量与 scheduler.py 中 @router 装饰器数量一致
- [x] Targets API 端点数量与 targets.py 中 @router 装饰器数量一致
- [x] Vulnerabilities API 端点数量与 vulnerabilities.py 中 @router 装饰器数量一致
- [x] Prompts API 端点数量与 prompts.py 中 @router 装饰器数量一致
- [x] Full IA API 端点数量与 full_ia.py 中 @router 装饰器数量一致
- [x] CLI Agent API 端点数量与 cli_agent.py 中 @router 装饰器数量一致
- [x] Agent Tasks API 端点数量与 agent_tasks.py 中 @router 装饰器数量一致
- [x] 每个端点包含请求参数说明（如有请求体）
- [x] 每个端点包含响应模型说明（如有定义response_model）
- [x] 至少5个核心API端点有真实curl测试结果记录

## 第3章 前端页面功能
- [x] TerminalAgentPage 包含VPN管理功能（上传/连接/断开/状态）
- [x] TerminalAgentPage 包含利用路径功能（创建/查看）
- [x] TerminalAgentPage 包含会话删除和详情查看
- [x] ProvidersPage 包含环境变量编辑器功能
- [x] ProvidersPage 包含单提供商检测和启用/禁用切换
- [x] RealtimeTaskPage 包含会话详情、报告生成、工具状态
- [x] ScanDetailsPage 包含阶段跳转功能
- [x] 所有18个页面的组件/按钮与代码中的事件处理函数对应
- [x] 页面路由图覆盖 Sidebar.tsx 中所有导航项
- [x] 页面间数据流转说明覆盖核心业务流程（扫描→代理→报告）

## 第4章 完整功能测试计划
- [x] 沙箱管理模块有完整测试用例
- [x] 知识库模块有完整测试用例
- [x] MCP服务器模块有完整测试用例
- [x] 调度器模块有完整测试用例
- [x] Full IA测试模块有完整测试用例
- [x] 任务库模块有完整测试用例
- [x] 实时任务模块有完整测试用例
- [x] Providers模块测试用例覆盖环境变量编辑器
- [x] Settings模块测试用例覆盖所有功能开关
- [x] 测试用例总数 >= 100

## 第5章 Providers与Settings大模型配置区别
- [x] 环境变量编辑器功能说明与 ProvidersPage.tsx 代码一致
- [x] Minimax配置实例包含正确的base_url和model
- [x] Smart Router请求路由流程包含方法调用链（route→_select_provider→_call_provider→_parse_response）

## 第6章 后端核心架构
- [x] Agent系统10个模块都有方法签名和调用链
- [x] VulnEngine系统包含11个测试器模块的详细分析
- [x] VulnEngine系统包含ai_prompts, system_prompts, pentest_playbook模块
- [x] RAG系统包含vectorstore, reasoning_templates, reasoning_memory, few_shot模块
- [x] Smart Router系统包含token_extractor, token_refresher模块
- [x] 遗漏的独立模块（autonomous_scanner, recon_integration等）已补充
- [x] 每个模块的关键方法签名与代码中def定义一致
- [x] 核心调用链描述与代码中的实际import和调用关系一致

## 第7章 数据模型详解
- [x] 所有数据库模型文件已读取和分析
- [x] 每个模型的字段定义与SQLAlchemy Column定义一致
- [x] 模型关系ER图覆盖所有外键和关联关系
- [x] 字段类型、约束、默认值与代码一致

## 第8章 配置与部署
- [x] .env配置项清单覆盖所有环境变量
- [x] 每个配置项有说明、默认值和影响范围
- [x] 部署说明与实际启动命令一致
- [x] 数据库迁移说明与代码中的init_db逻辑一致

## 总体验证
- [x] 文档总行数 >= 3000行（实际3373行）
- [x] 所有API端点数量与代码中路由装饰器总数一致（151个）
- [x] 所有前端页面组件与代码中事件处理函数总数匹配
- [x] 无编造内容，所有描述均可追溯到代码
