export interface AuthConfig {
  auth_type: "none" | "cookie" | "header" | "basic" | "bearer"
  cookie?: string
  bearer_token?: string
  username?: string
  password?: string
  header_name?: string
  header_value?: string
}

export interface ScanCreate {
  name?: string
  targets: string[]
  scan_type?: "quick" | "full" | "custom"
  recon_enabled?: boolean
  custom_prompt?: string
  prompt_id?: string
  config?: Record<string, unknown>
  auth?: AuthConfig
  custom_headers?: Record<string, string>
}

export interface ScanUpdate {
  name?: string
  status?: string
  progress?: number
  current_phase?: string
  error_message?: string
}

export interface ScanProgress {
  scan_id: string
  status: string
  progress: number
  current_phase?: string
  message?: string
  total_endpoints: number
  total_vulnerabilities: number
}

export interface TargetPublic {
  id: string
  scan_id: string
  url: string
  hostname?: string
  port?: number
  protocol?: string
  path?: string
  status: string
  created_at: string
}

export interface EndpointPublic {
  id: string
  scan_id: string
  target_id?: string
  url: string
  method: string
  path?: string
  parameters: Array<{ name: string; type: string; value?: string }>
  headers: Record<string, string>
  response_status?: number
  content_type?: string
  content_length?: number
  technologies: string[]
  interesting: boolean
  discovered_at: string
}

export interface VulnerabilityTestPublic {
  id: string
  scan_id: string
  endpoint_id?: string
  vulnerability_type: string
  payload?: string
  request_data: Record<string, unknown>
  response_data: Record<string, unknown>
  is_vulnerable: boolean
  confidence?: number
  evidence?: string
  tested_at: string
}

export interface VulnerabilityPublic {
  id: string
  scan_id: string
  test_id?: string
  title: string
  vulnerability_type: string
  severity: "critical" | "high" | "medium" | "low" | "info"
  cvss_score?: number
  cvss_vector?: string
  cwe_id?: string
  description?: string
  affected_endpoint?: string
  poc_request?: string
  poc_response?: string
  poc_payload?: string
  poc_parameter?: string
  poc_evidence?: string
  impact?: string
  remediation?: string
  references: string[]
  ai_analysis?: string
  poc_code?: string
  validation_status?: "ai_confirmed" | "ai_rejected" | "validated" | "false_positive" | "pending_review"
  ai_rejection_reason?: string
  confidence_score?: number
  confidence_breakdown?: Record<string, number>
  proof_of_execution?: string
  negative_controls?: string
  url?: string
  screenshots?: unknown[]
  created_at: string
}

export interface VulnerabilitySummary {
  total: number
  critical: number
  high: number
  medium: number
  low: number
  info: number
  by_type: Record<string, number>
}

export interface VulnerabilityTypeInfo {
  type: string
  name: string
  category: string
  description: string
  severity_range: string
  owasp_category?: string
  cwe_ids: string[]
}

export interface ScanPublic {
  id: string
  name?: string
  status: "pending" | "running" | "completed" | "failed" | "stopped" | "paused"
  scan_type: string
  recon_enabled: boolean
  progress: number
  current_phase?: string
  config: Record<string, unknown>
  custom_prompt?: string
  prompt_id?: string
  auth_type?: string
  auth_credentials?: Record<string, unknown>
  custom_headers?: Record<string, string>
  created_at: string
  started_at?: string
  completed_at?: string
  duration?: number
  error_message?: string
  total_endpoints: number
  total_vulnerabilities: number
  critical_count: number
  high_count: number
  medium_count: number
  low_count: number
  info_count: number
  targets?: TargetPublic[]
  created_by?: string
}

export interface ReportGenerate {
  scan_id: string
  format?: "html" | "pdf" | "json"
  title?: string
  include_executive_summary?: boolean
  include_poc?: boolean
  include_remediation?: boolean
  preferred_provider?: string
  preferred_model?: string
}

export interface ReportPublic {
  id: string
  scan_id: string
  title?: string
  format: "html" | "pdf" | "json"
  file_path?: string
  executive_summary?: string
  auto_generated: boolean
  is_partial: boolean
  generated_at: string
}

export interface PromptCreate {
  name: string
  description?: string
  content: string
  category?: string
}

export interface PromptUpdate {
  name?: string
  description?: string
  content?: string
  category?: string
}

export interface PromptPublic {
  id: string
  name: string
  description?: string
  content: string
  is_preset: boolean
  category?: string
  parsed_vulnerabilities: unknown[]
  created_at: string
  updated_at: string
}

export interface PromptPreset {
  id: string
  name: string
  description: string
  category: string
  vulnerability_count: number
}

export interface AgentTaskCreate {
  scan_id: string
  task_type: "recon" | "analysis" | "testing" | "reporting"
  task_name: string
  description?: string
  tool_name?: string
  tool_category?: string
}

export interface AgentTaskUpdate {
  status?: string
  items_processed?: number
  items_found?: number
  result_summary?: string
  error_message?: string
}

export interface AgentTaskPublic {
  id: string
  scan_id: string
  task_type: string
  task_name: string
  description?: string
  tool_name?: string
  tool_category?: string
  status: "pending" | "running" | "completed" | "failed" | "cancelled"
  started_at?: string
  completed_at?: string
  duration_ms?: number
  items_processed: number
  items_found: number
  result_summary?: string
  error_message?: string
  created_at: string
}

export interface AgentTaskSummary {
  total: number
  pending: number
  running: number
  completed: number
  failed: number
  by_type: Record<string, number>
  by_tool: Record<string, number>
}

export interface VulnLabChallengePublic {
  id: string
  target_url: string
  challenge_name?: string
  vuln_type: string
  vuln_category?: string
  auth_type?: string
  auth_value?: string
  status: "pending" | "running" | "completed" | "failed" | "stopped" | "paused"
  result?: "detected" | "not_detected" | "error"
  agent_id?: string
  scan_id?: string
  findings_count: number
  critical_count: number
  high_count: number
  medium_count: number
  low_count: number
  info_count: number
  findings_detail: Array<{
    title: string
    vulnerability_type: string
    severity: string
    affected_endpoint: string
    evidence: string
    payload?: string
  }>
  started_at?: string
  completed_at?: string
  duration?: number
  notes?: string
  logs?: VulnLabLogEntry[]
  logs_count?: number
  endpoints_count?: number
  created_at: string
  created_by?: string
}

export interface VulnLabLogEntry {
  level: string
  message: string
  time: string
  source: string
}

export interface VulnLabCreate {
  target_url: string
  vuln_type: string
  challenge_name?: string
  auth_type?: string
  auth_value?: string
  custom_headers?: Record<string, string>
  notes?: string
}

export interface VulnLabRunResponse {
  challenge_id: string
  agent_id: string
  status: string
  message: string
}

export interface VulnLabStats {
  total: number
  running: number
  status_counts: Record<string, number>
  result_counts: Record<string, number>
  detection_rate: number
  by_type: Record<string, { detected: number; not_detected: number; error: number; total: number }>
  by_category: Record<string, { detected: number; not_detected: number; error: number; total: number }>
}

export interface DashboardStats {
  total_scans: number
  running_scans: number
  completed_scans: number
  total_vulnerabilities: number
  critical_count: number
  high_count: number
  medium_count: number
  low_count: number
  info_count: number
  by_type: Record<string, number>
}

export interface AgentRunRequest {
  target: string
  mode?: "auto_pentest" | "full_llm" | "vuln_lab"
  scan_type?: string
  vuln_types?: string[]
  custom_prompt?: string
  enable_kali_sandbox?: boolean
}

export interface AgentStatus {
  id: string
  scan_id: string
  status: string
  progress: number
  current_phase: string
  findings_count: number
  start_time?: string
  elapsed_seconds?: number
}

export interface AgentFinding {
  id: string
  title: string
  vulnerability_type: string
  severity: string
  confidence_score: number
  validation_status: string
  endpoint?: string
}

export interface VulnTypeCategoryPublic {
  label: string
  types: Array<{
    key: string
    title: string
    severity: string
    cwe_id: string
    description: string
  }>
  count: number
}

export interface ActivityFeedItem {
  type: "scan" | "vulnerability" | "agent_task" | "report"
  action: string
  title: string
  description: string
  status?: string
  severity?: "critical" | "high" | "medium" | "low" | "info"
  timestamp: string
  scan_id?: string
  link?: string
}