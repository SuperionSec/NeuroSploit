# NeuroSploit v3.2.4 数据存储完整清单

> 生成时间: 2026-05-20  
> 数据库: SQLite (`data/neurosploit.db`)  
> 文件存储: 12 类

---

## 一、数据库表结构（9 张表，145 个字段）

### 1.1 scans — 扫描记录表

| 字段 | 类型 | 约束 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | VARCHAR(36) | PK | uuid4 | 扫描ID |
| name | VARCHAR(255) | NULL | — | 扫描名称 |
| status | VARCHAR(50) | NOT NULL | pending | pending / running / completed / failed / stopped |
| scan_type | VARCHAR(50) | NOT NULL | full | quick / full / custom |
| recon_enabled | BOOLEAN | NOT NULL | true | 是否启用侦察 |
| progress | INTEGER | NOT NULL | 0 | 进度百分比(0-100) |
| current_phase | VARCHAR(50) | NULL | — | recon / testing / reporting / completed |
| config | JSON | NOT NULL | {} | 扫描配置(含subdomain_discovery等) |
| custom_prompt | TEXT | NULL | — | 自定义提示词内容 |
| prompt_id | VARCHAR(36) | NULL | — | 关联提示词ID |
| auth_type | VARCHAR(50) | NULL | — | none / cookie / header / basic / bearer |
| auth_credentials | JSON | NULL | — | 认证凭据(敏感数据) |
| custom_headers | JSON | NULL | — | 自定义HTTP头 |
| created_at | DATETIME | NOT NULL | utcnow | 创建时间 |
| started_at | DATETIME | NULL | — | 开始时间 |
| completed_at | DATETIME | NULL | — | 完成时间 |
| duration | INTEGER | NULL | — | 持续时间(秒) |
| error_message | TEXT | NULL | — | 错误信息 |
| total_endpoints | INTEGER | NOT NULL | 0 | 发现端点数 |
| total_vulnerabilities | INTEGER | NOT NULL | 0 | 漏洞总数 |
| critical_count | INTEGER | NOT NULL | 0 | 严重漏洞数 |
| high_count | INTEGER | NOT NULL | 0 | 高危漏洞数 |
| medium_count | INTEGER | NOT NULL | 0 | 中危漏洞数 |
| low_count | INTEGER | NOT NULL | 0 | 低危漏洞数 |
| info_count | INTEGER | NOT NULL | 0 | 信息级漏洞数 |

**关联关系**: 1→N targets, 1→N endpoints, 1→N vulnerabilities, 1→N reports, 1→N agent_tasks

---

### 1.2 targets — 目标URL表

| 字段 | 类型 | 约束 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | VARCHAR(36) | PK | uuid4 | 目标ID |
| scan_id | VARCHAR(36) | FK→scans.id(CASCADE) | NOT NULL | 所属扫描 |
| url | VARCHAR(2048) | NOT NULL | — | 目标URL |
| hostname | VARCHAR(255) | NULL | — | 主机名 |
| port | INTEGER | NULL | — | 端口号 |
| protocol | VARCHAR(10) | NULL | — | 协议(http/https) |
| path | VARCHAR(2048) | NULL | — | URL路径 |
| status | VARCHAR(50) | NOT NULL | pending | pending / scanning / completed / failed |
| created_at | DATETIME | NOT NULL | utcnow | 创建时间 |

---

### 1.3 endpoints — 发现端点表

| 字段 | 类型 | 约束 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | VARCHAR(36) | PK | uuid4 | 端点ID |
| scan_id | VARCHAR(36) | FK→scans.id(CASCADE) | NOT NULL | 所属扫描 |
| target_id | VARCHAR(36) | FK→targets.id(SET NULL) | NULL | 所属目标 |
| url | TEXT | NOT NULL | — | 端点完整URL |
| method | VARCHAR(10) | NOT NULL | GET | HTTP方法 |
| path | TEXT | NULL | — | URL路径 |
| parameters | JSON | NOT NULL | [] | 参数列表 [{name, type, value}] |
| headers | JSON | NOT NULL | {} | 响应头 |
| response_status | INTEGER | NULL | — | HTTP状态码 |
| content_type | VARCHAR(100) | NULL | — | 内容类型 |
| content_length | INTEGER | NULL | — | 内容长度(字节) |
| technologies | JSON | NOT NULL | [] | 检测到的技术栈 |
| interesting | BOOLEAN | NOT NULL | false | 是否标记为有趣(需重点测试) |
| discovered_at | DATETIME | NOT NULL | utcnow | 发现时间 |

---

### 1.4 vulnerabilities — 确认漏洞表

| 字段 | 类型 | 约束 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | VARCHAR(36) | PK | uuid4 | 漏洞ID |
| scan_id | VARCHAR(36) | FK→scans.id(CASCADE) | NOT NULL | 所属扫描 |
| test_id | VARCHAR(36) | FK→vulnerability_tests.id(SET NULL) | NULL | 关联测试记录 |
| title | VARCHAR(500) | NOT NULL | — | 漏洞标题 |
| vulnerability_type | VARCHAR(100) | NOT NULL | — | 漏洞类型(xss_reflected / sqli_union等) |
| severity | VARCHAR(20) | NOT NULL | — | critical / high / medium / low / info |
| cvss_score | FLOAT | NULL | — | CVSS评分(0.0-10.0) |
| cvss_vector | VARCHAR(100) | NULL | — | CVSS向量字符串 |
| cwe_id | VARCHAR(50) | NULL | — | CWE编号(如CWE-79) |
| description | TEXT | NULL | — | 漏洞描述 |
| affected_endpoint | TEXT | NULL | — | 受影响端点URL |
| poc_request | TEXT | NULL | — | PoC原始请求 |
| poc_response | TEXT | NULL | — | PoC原始响应 |
| poc_payload | TEXT | NULL | — | PoC载荷 |
| poc_parameter | VARCHAR(500) | NULL | — | 漏洞参数名 |
| poc_evidence | TEXT | NULL | — | PoC证据 |
| impact | TEXT | NULL | — | 影响描述 |
| remediation | TEXT | NULL | — | 修复建议 |
| references | JSON | NOT NULL | [] | 参考链接列表 |
| ai_analysis | TEXT | NULL | — | AI分析结果 |
| poc_code | TEXT | NULL | — | PoC代码(HTML/Python/curl等) |
| screenshots | JSON | NOT NULL | [] | 截图(base64或文件路径) |
| url | TEXT | NULL | — | 源URL(用于finding_id重建) |
| parameter | VARCHAR(500) | NULL | — | 源参数名 |
| confidence_score | INTEGER | NULL | — | 置信度(0-100) |
| confidence_breakdown | JSON | NOT NULL | {} | 置信度分解 {proof, impact, controls} |
| proof_of_execution | TEXT | NULL | — | 执行证明(类型+详情) |
| validation_status | VARCHAR(20) | NOT NULL | ai_confirmed | ai_confirmed / validated / false_positive / pending_review / ai_rejected |
| ai_rejection_reason | TEXT | NULL | — | AI拒绝原因 |
| created_at | DATETIME | NOT NULL | utcnow | 创建时间 |

---

### 1.5 vulnerability_tests — 漏洞测试记录表

| 字段 | 类型 | 约束 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | VARCHAR(36) | PK | uuid4 | 测试ID |
| scan_id | VARCHAR(36) | FK→scans.id(CASCADE) | NOT NULL | 所属扫描 |
| endpoint_id | VARCHAR(36) | FK→endpoints.id(SET NULL) | NULL | 关联端点 |
| vulnerability_type | VARCHAR(100) | NOT NULL | — | 测试的漏洞类型 |
| payload | TEXT | NULL | — | 测试载荷 |
| request_data | JSON | NOT NULL | {} | 请求数据 |
| response_data | JSON | NOT NULL | {} | 响应数据 |
| is_vulnerable | BOOLEAN | NOT NULL | false | 是否确认存在漏洞 |
| confidence | FLOAT | NULL | — | 置信度(0.0-1.0) |
| evidence | TEXT | NULL | — | 证据文本 |
| tested_at | DATETIME | NOT NULL | utcnow | 测试时间 |

**索引**: `idx_vulnerability_tests_scan_id`

---

### 1.6 reports — 报告表

| 字段 | 类型 | 约束 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | VARCHAR(36) | PK | uuid4 | 报告ID |
| scan_id | VARCHAR(36) | FK→scans.id(CASCADE) | NOT NULL | 所属扫描 |
| title | VARCHAR(255) | NULL | — | 报告标题 |
| format | VARCHAR(20) | NOT NULL | html | html / pdf / json |
| file_path | TEXT | NULL | — | 文件存储路径(指向data/reports/) |
| executive_summary | TEXT | NULL | — | 执行摘要 |
| auto_generated | BOOLEAN | NOT NULL | false | 是否自动生成(扫描完成/停止时) |
| is_partial | BOOLEAN | NOT NULL | false | 是否部分报告(扫描未完成) |
| generated_at | DATETIME | NOT NULL | utcnow | 生成时间 |

---

### 1.7 prompts — 提示词表

| 字段 | 类型 | 约束 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | VARCHAR(36) | PK | uuid4 | 提示词ID |
| name | VARCHAR(255) | NOT NULL | — | 名称 |
| description | TEXT | NULL | — | 描述 |
| content | TEXT | NOT NULL | — | 提示词内容 |
| is_preset | BOOLEAN | NOT NULL | false | 是否系统预设 |
| category | VARCHAR(100) | NULL | — | 分类(pentest / bug_bounty / api等) |
| parsed_vulnerabilities | JSON | NOT NULL | [] | AI提取的漏洞类型列表 |
| created_at | DATETIME | NOT NULL | utcnow | 创建时间 |
| updated_at | DATETIME | NOT NULL | utcnow | 更新时间 |

---

### 1.8 agent_tasks — 代理任务表

| 字段 | 类型 | 约束 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | VARCHAR(36) | PK | uuid4 | 任务ID |
| scan_id | VARCHAR(36) | FK→scans.id(CASCADE) | NOT NULL | 所属扫描 |
| task_type | VARCHAR(50) | NOT NULL | — | recon / analysis / testing / reporting |
| task_name | VARCHAR(255) | NOT NULL | — | 任务名称 |
| description | TEXT | NULL | — | 任务描述 |
| tool_name | VARCHAR(100) | NULL | — | 工具名(nmap / nuclei / claude / httpx等) |
| tool_category | VARCHAR(50) | NULL | — | scanner / analyzer / ai / crawler |
| status | VARCHAR(20) | NOT NULL | pending | pending / running / completed / failed / cancelled |
| started_at | DATETIME | NULL | — | 开始时间 |
| completed_at | DATETIME | NULL | — | 完成时间 |
| duration_ms | INTEGER | NULL | — | 持续时间(毫秒) |
| items_processed | INTEGER | NOT NULL | 0 | 已处理项数(URL数/主机数等) |
| items_found | INTEGER | NOT NULL | 0 | 发现项数(端点数/漏洞数等) |
| result_summary | TEXT | NULL | — | 结果摘要 |
| error_message | TEXT | NULL | — | 错误信息 |
| created_at | DATETIME | NOT NULL | utcnow | 创建时间 |

**索引**: `idx_agent_tasks_scan_id`, `idx_agent_tasks_status`

---

### 1.9 vuln_lab_challenges — 漏洞实验室挑战表

| 字段 | 类型 | 约束 | 默认值 | 说明 |
|------|------|------|--------|------|
| id | VARCHAR(36) | PK | uuid4 | 挑战ID |
| target_url | TEXT | NOT NULL | — | 目标URL |
| challenge_name | VARCHAR(255) | NULL | — | 挑战名称 |
| vuln_type | VARCHAR(100) | NOT NULL | — | 漏洞类型(xss_reflected等) |
| vuln_category | VARCHAR(50) | NULL | — | 漏洞分类(injection / auth / client_side等) |
| auth_type | VARCHAR(20) | NULL | — | 认证类型(cookie / bearer / basic / header) |
| auth_value | TEXT | NULL | — | 认证值 |
| status | VARCHAR(20) | NOT NULL | pending | pending / running / completed / failed / stopped |
| result | VARCHAR(20) | NULL | — | detected / not_detected / error |
| agent_id | VARCHAR(36) | NULL | — | 关联代理ID |
| scan_id | VARCHAR(36) | NULL | — | 关联扫描ID |
| findings_count | INTEGER | NOT NULL | 0 | 发现数量 |
| critical_count | INTEGER | NOT NULL | 0 | 严重漏洞数 |
| high_count | INTEGER | NOT NULL | 0 | 高危漏洞数 |
| medium_count | INTEGER | NOT NULL | 0 | 中危漏洞数 |
| low_count | INTEGER | NOT NULL | 0 | 低危漏洞数 |
| info_count | INTEGER | NOT NULL | 0 | 信息级漏洞数 |
| findings_detail | JSON | NOT NULL | [] | 发现详情列表 |
| started_at | DATETIME | NULL | — | 开始时间 |
| completed_at | DATETIME | NULL | — | 完成时间 |
| duration | INTEGER | NULL | — | 持续时间(秒) |
| notes | TEXT | NULL | — | 备注 |
| logs | JSON | NOT NULL | [] | 日志记录(完成后持久化) |
| endpoints_count | INTEGER | NOT NULL | 0 | 发现端点数 |
| created_at | DATETIME | NOT NULL | utcnow | 创建时间 |

**索引**: `idx_vuln_lab_status`, `idx_vuln_lab_vuln_type`

---

### 表关系图

```
scans (1) ────→ (N) targets
  │
  ├──────→ (N) endpoints ──→ (N) vulnerability_tests
  │
  ├──────→ (N) vulnerabilities ──→ (1) vulnerability_tests
  │
  ├──────→ (N) reports
  │
  └──────→ (N) agent_tasks

vuln_lab_challenges (独立表，通过 agent_id/scan_id 松散关联)
prompts (独立表，通过 prompt_id 被 scans 引用)
```

---

## 二、文件存储（12 类）

### 2.1 Provider 配置文件

| 属性 | 值 |
|------|-----|
| **路径** | `data/providers.json` |
| **源码** | `backend/core/smart_router/provider_registry.py:19` |
| **写入方式** | 原子写入(先写.tmp再rename) |
| **写入时机** | 连接/断开提供商时 |

**内容结构**:
```json
[
  {
    "id": "minimax",
    "name": "MiniMax",
    "auth_type": "api_key",
    "api_format": "openai",
    "base_url": "https://api.minimaxi.com/v1",
    "tier": 2,
    "default_model": "MiniMax-M2.7",
    "env_key": "MINIMAX_API_KEY",
    "enabled": true,
    "accounts": [
      { "id": "acct_xxx", "label": "Manual API Key", "connected": true, "model_override": null }
    ]
  }
]
```

**注意**: API Key 仅存内存，不写入文件

---

### 2.2 报告文件

| 属性 | 值 |
|------|-----|
| **路径** | `data/reports/report_{timestamp}/` |
| **源码** | `backend/core/report_engine/generator.py:84` |
| **写入时机** | 生成报告时(手动/AI/自动) |

**目录结构**:
```
data/reports/
└── report_20260520_030000/
    ├── report_20260520_030000.html    ← HTML格式报告
    ├── report_20260520_030000.json    ← JSON格式报告(附带生成)
    └── screenshots/                   ← 截图子目录
        ├── screenshot_1.png
        └── screenshot_2.png
```

---

### 2.3 知识库文件

| 属性 | 值 |
|------|-----|
| **路径** | `data/custom-knowledge/` |
| **源码** | `backend/core/knowledge_processor.py:26-28` |
| **写入时机** | 上传知识文档时 |

**目录结构**:
```
data/custom-knowledge/
├── index.json                         ← 文档索引
└── uploads/                           ← 原始上传文件
    ├── 1c4cf70f-d4a_pentest.md
    └── a86d636c-6a1_NeuroSploit_xxx.md
```

**index.json 结构**:
```json
{
  "documents": [
    {
      "id": "1c4cf70f-d4a",
      "filename": "pentest.md",
      "title": "Kali Linux Penetration Testing Fundamentals",
      "source_type": "md",
      "uploaded_at": "2026-02-16T14:50:31",
      "processed": true,
      "file_size_bytes": 20702,
      "summary": "...",
      "vuln_types": ["xss", "sqli"],
      "knowledge_entries": []
    }
  ]
}
```

**支持格式**: `.pdf`, `.md`, `.txt`, `.html`, `.htm`

---

### 2.4 RAG 向量索引

| 属性 | 值 |
|------|-----|
| **路径** | `data/vectorstore/` |
| **源码** | `backend/core/rag/vectorstore.py` |
| **写入时机** | 添加/删除知识文档时 |

**目录结构**:
```
data/vectorstore/
├── chromadb/                              ← ChromaDB持久化存储
│   ├── chroma.sqlite3                     ← 元数据SQLite
│   ├── 02a1b011-382a.../                  ← 集合1
│   │   ├── data_level0.bin                ← 向量数据
│   │   ├── header.bin
│   │   ├── length.bin
│   │   └── link_lists.bin
│   └── 60204f78-d8f2.../                  ← 集合2
│       ├── data_level0.bin
│       ├── header.bin
│       ├── index_metadata.pickle
│       ├── length.bin
│       └── link_lists.bin
└── bm25_index.json                        ← BM25降级索引
```

**降级策略**: ChromaDB(语义嵌入) → TF-IDF → BM25(关键词)

---

### 2.5 推理记忆文件

| 属性 | 值 |
|------|-----|
| **路径** | `data/reasoning_memory.json` |
| **源码** | `backend/core/rag/reasoning_memory.py:26` |
| **写入时机** | 代理发现确认漏洞后 |
| **上限** | 500条traces + 200条失败模式 + 100条策略 |

**内容结构**:
```json
{
  "traces": [
    {
      "vuln_type": "xss_reflected",
      "context_hash": "abc123",
      "reasoning_chain": "Step 1: Found input field...",
      "outcome": "confirmed",
      "timestamp": 1234567890.0
    }
  ],
  "failed_hypotheses": [
    {
      "vuln_type": "sqli",
      "hypothesis": "Union-based injection",
      "why_failed": "WAF blocked the request",
      "timestamp": 1234567890.0
    }
  ],
  "strategies": [
    {
      "tech_stack": "php",
      "vuln_type": "xss",
      "successful_approach": "Test reflected params in search forms",
      "timestamp": 1234567890.0
    }
  ]
}
```

---

### 2.6 扫描检查点文件

| 属性 | 值 |
|------|-----|
| **路径** | `data/checkpoints/{scan_id}.json` |
| **源码** | `backend/core/checkpoint_manager.py:17` |
| **写入时机** | 代理运行中定期保存 |
| **用途** | 崩溃恢复，恢复代理状态 |

**内容结构**:
```json
{
  "_checkpoint_version": 1,
  "_scan_id": "8acc2e72-...",
  "_timestamp": 1234567890.0,
  "target": "https://example.com",
  "mode": "auto_pentest",
  "scan_type": "full",
  "progress": 55,
  "phase": "Deep: attack surface analyzed",
  "recon_data": {
    "endpoints": [],
    "tech_stack": []
  },
  "findings": [],
  "test_targets": [],
  "junior_tested_types": [],
  "completed_vuln_types": []
}
```

---

### 2.7 访问控制学习文件

| 属性 | 值 |
|------|-----|
| **路径** | `data/access_control_learning.json` |
| **源码** | `backend/core/access_control_learner.py:33` |
| **写入时机** | 每次访问控制测试完成后 |
| **用途** | BOLA/BFLA/IDOR测试的响应模式学习 |

**内容结构**:
```json
{
  "patterns": [
    {
      "pattern_type": "denial",
      "indicators": ["Access Denied", "403"],
      "is_false_positive": false,
      "confidence": 0.95,
      "example_body": "...",
      "vuln_type": "bola",
      "target_domain": "example.com",
      "timestamp": "2026-05-20T10:00:00"
    }
  ],
  "test_records": [
    {
      "vuln_type": "bfla",
      "url": "https://example.com/api/admin/users",
      "response_body_hash": "sha256:...",
      "is_true_positive": true,
      "pattern_notes": "Admin data accessible with regular user"
    }
  ]
}
```

---

### 2.8 任务库文件

| 属性 | 值 |
|------|-----|
| **路径** | `prompts/task_library.json` |
| **源码** | `backend/core/task_library.py:60` |
| **写入时机** | 创建/删除自定义任务时 |

**内容**: 30+ 预设任务定义 + 用户自定义任务

---

### 2.9 提示词预设库

| 属性 | 值 |
|------|-----|
| **路径** | `prompts/library.json` |
| **写入时机** | 系统初始化时 |

---

### 2.10 代理角色提示词文件

| 属性 | 值 |
|------|-----|
| **路径** | `prompts/md_library/` |
| **写入时机** | 系统初始化时(只读) |

**文件列表**:

| 文件 | 说明 |
|------|------|
| `pentest_generalist.md` | 渗透测试通用代理 |
| `pentest.md` | 渗透测试代理 |
| `red_team_agent.md` | 红队代理 |
| `blue_team_agent.md` | 蓝队代理 |
| `bug_bounty_hunter.md` | 漏洞赏金猎人 |
| `exploit_expert.md` | 漏洞利用专家 |
| `owasp_expert.md` | OWASP 专家 |
| `cwe_expert.md` | CWE 专家 |
| `malware_analyst.md` | 恶意软件分析师 |
| `malware_analysis.md` | 恶意软件分析 |
| `replay_attack.md` | 重放攻击 |
| `replay_attack_specialist.md` | 重放攻击专家 |
| `Pentestfull.md` | 完整渗透测试 |

---

### 2.11 系统配置文件

| 属性 | 值 |
|------|-----|
| **路径** | `config/config.json` |
| **源码** | `backend/api/v1/mcp.py:16`, `backend/api/v1/scheduler.py:15` |
| **写入时机** | MCP服务器增删改、定时任务增删改时 |

**内容结构**:
```json
{
  "llm": {
    "default_profile": "gemini_pro_default",
    "profiles": {
      "gemini_pro_default": {
        "provider": "gemini",
        "model": "gemini-pro",
        "api_key": "${GEMINI_API_KEY}",
        "temperature": 0.7,
        "max_tokens": 4096
      }
    }
  },
  "agent_roles": {
    "pentest_generalist": {
      "enabled": true,
      "tools_allowed": ["nmap", "metasploit", "burpsuite", "sqlmap", "hydra"]
    }
  },
  "mcp_servers": { ... },
  "scheduler_jobs": { ... }
}
```

---

### 2.12 环境变量文件

| 属性 | 值 |
|------|-----|
| **路径** | `.env`(项目根目录) |
| **源码** | `backend/api/v1/settings.py:20` |
| **写入时机** | Settings页面保存、Providers页面更新环境变量时 |

**内容**:
```env
MINIMAX_API_KEY=sk-cp-xxx
ENABLE_SMART_ROUTER=true
ENABLE_RAG=true
ENABLE_KNOWLEDGE_AUGMENTATION=true
ENABLE_VULN_AGENTS=true
MAX_CONCURRENT_SCANS=5
```

**支持的17个环境变量**:
| 变量 | 说明 |
|------|------|
| MINIMAX_API_KEY | Minimax API密钥 |
| ANTHROPIC_API_KEY | Anthropic Claude密钥 |
| OPENAI_API_KEY | OpenAI密钥 |
| OPENROUTER_API_KEY | OpenRouter密钥 |
| GEMINI_API_KEY | Google Gemini密钥 |
| TOGETHER_API_KEY | Together AI密钥 |
| FIREWORKS_API_KEY | Fireworks AI密钥 |
| OLLAMA_BASE_URL | Ollama本地地址 |
| LMSTUDIO_BASE_URL | LM Studio本地地址 |
| ENABLE_SMART_ROUTER | 启用智能路由 |
| ENABLE_RAG | 启用RAG增强 |
| ENABLE_KNOWLEDGE_AUGMENTATION | 启用知识增强 |
| ENABLE_VULN_AGENTS | 启用漏洞代理 |
| ENABLE_MULTI_AGENT | 启用多代理 |
| ENABLE_CLI_AGENT | 启用CLI代理 |
| MAX_CONCURRENT_SCANS | 最大并发扫描数 |
| DEFAULT_LLM_MODEL | 默认LLM模型 |

---

### 2.13 漏洞知识库

| 属性 | 值 |
|------|-----|
| **路径** | `data/vuln_knowledge_base.json` |
| **写入时机** | 系统初始化时(只读) |

**内容**: 内置漏洞知识库，用于RAG增强

---

### 2.14 站点分析临时文件

| 属性 | 值 |
|------|-----|
| **路径** | 系统临时目录(`tempfile.mkdtemp`) |
| **源码** | `backend/core/site_analyzer.py:450-480` |
| **写入时机** | 深度侦察阶段爬取目标网站时 |
| **生命周期** | 临时文件，扫描结束后可能残留 |

**内容**: 爬取的HTML页面(`{safe_name}.html`)和JS文件(`{safe_name}.js`)

---

## 三、完整目录结构

```
/workspace/
├── .env                                        ← 环境变量(API Key/功能开关)
├── config/
│   ├── config.json                             ← LLM配置/代理角色/MCP/定时任务
│   ├── config-example.json                     ← 配置示例
│   └── config2.json                            ← 备用配置
├── data/
│   ├── neurosploit.db                          ← SQLite数据库(9张表)
│   ├── providers.json                          ← 19个LLM提供商元数据
│   ├── reasoning_memory.json                   ← 推理记忆(跨扫描学习)
│   ├── access_control_learning.json            ← 访问控制学习记录
│   ├── vuln_knowledge_base.json                ← 内置漏洞知识库
│   ├── checkpoints/
│   │   └── {scan_id}.json                      ← 扫描检查点(崩溃恢复)
│   ├── custom-knowledge/
│   │   ├── index.json                          ← 知识文档索引
│   │   └── uploads/                            ← 上传的知识文档(.md/.pdf/.txt/.html)
│   ├── reports/
│   │   └── report_{timestamp}/
│   │       ├── report_{ts}.html                ← HTML报告
│   │       ├── report_{ts}.json                ← JSON报告
│   │       └── screenshots/                    ← 截图目录
│   └── vectorstore/
│       ├── chromadb/                           ← ChromaDB向量数据
│       │   ├── chroma.sqlite3                  ← 元数据
│       │   └── {collection_id}/*.bin           ← 向量二进制文件
│       └── bm25_index.json                     ← BM25降级索引
└── prompts/
    ├── task_library.json                       ← 任务库(30+预设+自定义)
    ├── library.json                            ← 提示词预设库
    └── md_library/                             ← 12个代理角色MD文件
        ├── pentest_generalist.md
        ├── red_team_agent.md
        ├── blue_team_agent.md
        ├── bug_bounty_hunter.md
        ├── exploit_expert.md
        ├── owasp_expert.md
        ├── cwe_expert.md
        ├── malware_analyst.md
        ├── malware_analysis.md
        ├── replay_attack.md
        ├── replay_attack_specialist.md
        ├── Pentestfull.md
        └── pentest.md
```

---

## 四、数据流向图

```
用户操作
  │
  ├── 扫描创建 ──→ scans表 + targets表
  │
  ├── 代理运行 ──→ agent_tasks表 + checkpoints/{id}.json
  │       │
  │       ├── 侦察阶段 ──→ endpoints表 + 临时HTML/JS文件
  │       │
  │       ├── 测试阶段 ──→ vulnerability_tests表
  │       │
  │       ├── 发现漏洞 ──→ vulnerabilities表 + reasoning_memory.json
  │       │                    + access_control_learning.json
  │       │
  │       └── 完成扫描 ──→ reports表 + data/reports/文件
  │
  ├── 知识上传 ──→ custom-knowledge/uploads/ + index.json + vectorstore/
  │
  ├── Provider配置 ──→ providers.json + .env
  │
  ├── MCP/定时任务 ──→ config/config.json
  │
  └── 任务管理 ──→ task_library.json
```

---

## 五、统计汇总

### 数据库

| 表名 | 字段数 | 关联 | 说明 |
|------|--------|------|------|
| scans | 25 | 父表 | 核心扫描记录 |
| targets | 9 | 子表→scans | 目标URL |
| endpoints | 14 | 子表→scans | 发现的端点 |
| vulnerabilities | 28 | 子表→scans | 确认的漏洞(最复杂) |
| vulnerability_tests | 11 | 子表→scans | 测试记录 |
| reports | 9 | 子表→scans | 报告元数据 |
| prompts | 9 | 独立 | 提示词 |
| agent_tasks | 16 | 子表→scans | 代理任务追踪 |
| vuln_lab_challenges | 24 | 松散关联 | 漏洞实验室 |
| **合计** | **145** | | **9张表** |

### 文件存储

| 类别 | 路径 | 格式 | 读写 |
|------|------|------|------|
| Provider配置 | data/providers.json | JSON | 读写 |
| 报告文件 | data/reports/ | HTML/JSON/PNG | 写入 |
| 知识库 | data/custom-knowledge/ | MD/PDF/TXT/HTML | 读写 |
| 向量索引 | data/vectorstore/ | BIN/SQLite/JSON | 读写 |
| 推理记忆 | data/reasoning_memory.json | JSON | 读写 |
| 扫描检查点 | data/checkpoints/ | JSON | 读写 |
| 访问控制学习 | data/access_control_learning.json | JSON | 读写 |
| 任务库 | prompts/task_library.json | JSON | 读写 |
| 提示词预设 | prompts/library.json | JSON | 只读 |
| 代理角色 | prompts/md_library/ | Markdown | 只读 |
| 系统配置 | config/config.json | JSON | 读写 |
| 环境变量 | .env | ENV | 读写 |
| 漏洞知识库 | data/vuln_knowledge_base.json | JSON | 只读 |
| 站点分析临时 | tempfile | HTML/JS | 临时 |
| **合计** | **14类** | | |
