# 前端交互元素完整提取分析 Spec

## Why
用户需要全面了解前端所有页面组件中的交互元素信息，包括按钮、输入字段、下拉选择、开关组件、API调用和导航链接，以便进行后续的重构或文档化工作。

## What Changes
- 本任务为纯分析/文档任务，不涉及代码修改
- 从20个文件中提取所有交互元素信息
- 识别重复模式（如Toast系统在每个页面中内联实现）

## Impact
- Affected specs: 无代码变更
- Affected code: 20个前端文件（18个页面组件 + Sidebar.tsx + App.tsx）

## ADDED Requirements
### Requirement: 交互元素完整提取
系统 SHALL 从所有20个前端文件中提取以下信息：
- 页面组件名称
- 所有按钮及其onClick处理器和调用的API
- 所有输入字段及其状态变量
- 所有选择/下拉组件及其选项
- 所有切换/开关组件
- 所有API调用（fetch/axios）及其URL和方法
- 所有导航链接（useNavigate调用）

#### Scenario: 完整提取
- **WHEN** 读取所有20个文件
- **THEN** 返回每个页面的完整交互元素清单，不跳过任何元素
