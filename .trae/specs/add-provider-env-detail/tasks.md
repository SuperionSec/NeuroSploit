# Tasks

- [x] Task 1: 补充第2章 Providers API — 添加 19 个提供商完整配置表格
  - [x] SubTask 1.1: 在第2章 2.6 Providers API 节末尾添加"提供商完整配置清单"表格，包含 providers.json 中所有 19 个提供商的 id/name/auth_type/api_format/base_url/tier/default_model/env_key
  - [x] SubTask 1.2: 添加 Tier 分级说明（Tier 1=高级、Tier 2=经济、Tier 3=免费/本地）
  - [x] SubTask 1.3: 添加 auth_type 分类说明（oauth=CLI令牌自动检测、api_key=手动输入密钥）

- [x] Task 2: 补充第3章 ProvidersPage — 添加 ProviderCard/ConfigModal UI 细节
  - [x] SubTask 2.1: 在 Page 8: ProvidersPage 节补充 ProviderCard 组件描述（颜色映射 PROVIDER_COLORS、首字母 PROVIDER_INITIALS、Tier 标签 TIER_LABELS/TIER_COLORS、显示字段：name/default_model/tier/accounts数量/enabled状态）
  - [x] SubTask 2.2: 补充 ConfigModal 组件描述（显示 api_format/default_model、账户列表含 label/source/credential_type/is_active/tokens_used、添加凭据表单含 label+api_key 输入框、检测CLI令牌按钮、测试连接按钮、删除账户按钮）
  - [x] SubTask 2.3: 补充环境变量编辑器描述（envAllowedKeys 过滤逻辑、搜索功能、实时编辑和保存、只显示允许的键）

- [x] Task 3: 补充第5章 — 添加 Provider 完整配置清单和与 Settings 的区别
  - [x] SubTask 3.1: 在第5章补充 Provider 配置来源说明（providers.json 硬编码 + ProviderRegistry 回退 + 环境变量自动连接）
  - [x] SubTask 3.2: 补充 Provider 完整配置清单表格（19个提供商的 base_url 和 default_model）

- [x] Task 4: 补充第8章 .env 参数 — 添加每个参数的详细作用说明
  - [x] SubTask 4.1: 为 LLM API Keys 组（7个）补充详细作用：每个 Key 的用途、对应提供商、获取方式
  - [x] SubTask 4.2: 为 Local LLM 组（2个）补充详细作用：OLLAMA_BASE_URL 和 LMSTUDIO_BASE_URL 的连接方式和默认端口
  - [x] SubTask 4.3: 为 LLM Configuration 组（3个）补充详细作用：MAX_OUTPUT_TOKENS 的范围建议、DEFAULT_LLM_MODEL 的可选值、ENABLE_MODEL_ROUTING 与 Smart Router 的关系
  - [x] SubTask 4.4: 为 Feature Flags 组（2个）补充详细作用：ENABLE_KNOWLEDGE_AUGMENTATION 与 RAG 的关系、ENABLE_BROWSER_VALIDATION 的浏览器验证机制
  - [x] SubTask 4.5: 为 Agent Autonomy 组（7个活跃+7个注释）补充详细作用：每个参数的影响模块和配置建议
  - [x] SubTask 4.6: 为 Smart Router/RAG/Methodology/Vuln Agents/Notifications/Database/Server 组补充详细作用
  - [x] SubTask 4.7: 为注释变量补充"何时启用"建议

# Task Dependencies
- [Task 2] depends on [Task 1] (需要提供商配置信息来描述UI)
- [Task 3] depends on [Task 1] (需要提供商配置信息)
- [Task 4] independent
- [Task 1, Task 4] can run in parallel
