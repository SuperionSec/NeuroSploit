# Checklist

## 第2章 Providers API
- [x] 提供商完整配置表格包含 19 个提供商
- [x] 每个提供商包含 id/name/auth_type/api_format/base_url/tier/default_model/env_key
- [x] Tier 分级说明清晰（Tier 1/2/3 含义）
- [x] auth_type 分类说明清晰（oauth vs api_key）

## 第3章 ProvidersPage
- [x] ProviderCard 组件描述包含颜色映射和首字母映射
- [x] ProviderCard 显示字段完整（name/default_model/tier/accounts/enabled）
- [x] ConfigModal 组件描述包含所有交互元素
- [x] ConfigModal 账户列表字段完整（label/source/credential_type/is_active/tokens_used）
- [x] 环境变量编辑器描述包含 envAllowedKeys 过滤逻辑

## 第5章
- [x] Provider 配置来源说明清晰（providers.json + ProviderRegistry + env）
- [x] 19个提供商的 base_url 和 default_model 完整列出

## 第8章 .env 参数
- [x] LLM API Keys 组（7个）每个有详细作用说明
- [x] Local LLM 组（2个）有连接方式和默认端口说明
- [x] LLM Configuration 组（3个）有配置建议
- [x] Feature Flags 组（2个）有与关联模块的说明
- [x] Agent Autonomy 组（14个）每个有影响模块和配置建议
- [x] Smart Router/RAG/Methodology/Vuln Agents 组有详细说明
- [x] Notifications 组（8个）有配置说明
- [x] Database/Server 组有说明
- [x] 注释变量有"何时启用"建议
