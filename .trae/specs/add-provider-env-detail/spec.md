# 补充 Provider 页面详情和 .env 参数作用 Spec

## Why
当前分析文档中 ProvidersPage 的描述过于简略，缺少 19 个提供商的完整配置信息（auth_type、api_format、base_url、tier、default_model、env_key），也缺少 ProviderCard/ConfigModal 组件的 UI 细节。同时 .env 参数只有简单表格，缺少每个参数的详细作用说明和配置建议。

## What Changes
- **第2章 Providers API**: 补充 providers.json 中 19 个提供商的完整配置表格
- **第3章 ProvidersPage**: 补充 ProviderCard 组件详情（颜色、首字母、Tier 标签、显示字段）、ConfigModal 组件详情（API 格式、模型信息、账户管理）、环境变量编辑器详情（envAllowedKeys 过滤逻辑）
- **第5章**: 补充 Provider 与 Settings 的配置区别中 Provider 完整配置清单
- **第8章 .env 参数**: 为每个 .env 参数补充详细作用说明、配置建议、影响范围

## Impact
- Affected specs: 第2章、第3章、第5章、第8章
- Affected code: `/workspace/NeuroSploit_3.2.4_全面分析文档_大模型分析的.md`

## ADDED Requirements

### Requirement: Provider 完整配置清单
文档 SHALL 包含 providers.json 中所有 19 个提供商的完整配置信息表格，包含：id、name、auth_type、api_format、base_url、tier、default_model、env_key。

#### Scenario: 对照 providers.json 验证
- **WHEN** 读取 `/workspace/data/providers.json`
- **THEN** 文档中列出的提供商数量和配置信息 SHALL 与文件内容一致

### Requirement: ProviderCard/ConfigModal UI 细节
文档 SHALL 描述 ProvidersPage 中 ProviderCard 和 ConfigModal 组件的 UI 元素，包括颜色映射、Tier 标签、显示字段、交互逻辑。

### Requirement: .env 参数详细作用
文档第8章 SHALL 为每个 .env 参数提供详细的作用说明，包括：参数用途、影响的功能模块、配置建议、与其他参数的关联。

#### Scenario: 对照代码验证参数作用
- **WHEN** 读取 backend/config.py 和相关代码
- **THEN** 每个参数的作用描述 SHALL 与代码中的实际使用逻辑一致
