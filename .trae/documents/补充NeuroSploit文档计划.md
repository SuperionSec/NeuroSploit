# 文档补充完善计划

## 目标
完善 `/workspace/NeuroSploit_3.2.4_全面分析文档_大模型分析的.md`，补充缺失的前端页面、后端API、后端核心架构等内容。

## 当前缺失分析

### 缺失的前端页面（8个）
1. **FullIATestingPage** - 完整AI渗透测试页
2. **MCPManagementPage** - MCP服务器管理页
3. **SchedulerPage** - 调度任务管理页
4. **KnowledgePage** - 知识库管理页
5. **RealtimeTaskPage** - 实时任务页
6. **SandboxDashboardPage** - 沙箱仪表板页
7. **TaskLibraryPage** - 任务库页
8. **ReportViewPage** - 报告查看页

### 缺失的后端API（12个模块）
1. **dashboard.py** - 仪表板统计API（7个端点）
2. **settings.py** - 设置管理API（7个端点）
3. **sandbox.py** - 沙箱管理API（5个端点）
4. **knowledge.py** - 知识库管理API（6个端点）
5. **mcp.py** - MCP服务器管理API（8个端点）
6. **scheduler.py** - 调度任务API（6个端点）
7. **targets.py** - 目标管理API（4个端点）
8. **vulnerabilities.py** - 漏洞信息API（4个端点）
9. **prompts.py** - 提示词管理API（9个端点）
10. **full_ia.py** - 完整AI测试API（1个端点）
11. **cli_agent.py** - CLI代理API（2个端点）
12. **agent_tasks.py** - 代理任务API（4个端点）

### 缺失的后端核心架构
- Agent系统架构（10个模块）
- VulnEngine系统架构（8个模块）
- Smart Router系统架构（4个模块）
- RAG系统架构（5个模块）
- 验证管线架构（6个模块）
- 请求引擎架构（5个模块）
- AI推理架构（7个模块）
- 报告引擎架构（2个模块）
- 沙箱/CLI系统架构（4个模块）
- 其他支撑模块（10个模块）

## 实施步骤

### 步骤1：补充缺失的8个前端页面功能
- 读取每个页面源码，提取路由、组件、按钮、API调用
- 按已有格式添加到"前端页面功能"章节
- 添加到"各页面布局结构分析"章节

### 步骤2：补充缺失的12个后端API模块
- 读取每个API文件，提取端点列表
- 按已有格式添加到"后端API接口"章节
- 包含方法、路径、功能描述、相关前端

### 步骤3：添加后端核心架构章节
- 按功能分组描述每个core模块
- 包含模块文件、主要类/函数、核心职责、依赖关系
- 添加架构图（文本格式）

### 步骤4：更新目录和关联性
- 更新文档目录
- 更新功能关联性分析
- 更新页面流转与导航

### 步骤5：验证文档完整性
- 确认18个页面全部覆盖
- 确认18个API模块全部覆盖
- 确认所有core模块全部覆盖
