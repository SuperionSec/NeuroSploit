export interface ProTablePaginationParams {
  current?: number;
  pageSize?: number;
  [key: string]: any;
}

export interface ProTableResponse<T> {
  data: T[];
  success: boolean;
  total: number;
}

export interface BackendListResponse<T> {
  data?: T[];
  total?: number;
  page?: number;
  per_page?: number;
  scans?: T[];
  reports?: T[];
  users?: T[];
  [key: string]: T[] | number | undefined;
}

export interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface Scan {
  id: string;
  name: string;
  scan_type: string;
  status: string;
  progress: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  info_count: number;
  total_vulnerabilities: number;
  current_phase?: string;
  created_at: string;
  updated_at: string;
}

export interface Report {
  id: string;
  scan_id: string;
  title?: string;
  format: string;
  auto_generated: boolean;
  is_partial: boolean;
  generated_at: string;
}

export interface Vulnerability {
  id: string;
  scan_id: string;
  title: string;
  description?: string;
  severity: string;
  confidence?: string;
  cvss_score?: number;
  cwe_id?: string;
  cve_id?: string;
  url?: string;
  endpoint?: string;
  method?: string;
  payload?: string;
  evidence?: string;
  fixed?: boolean;
  created_at: string;
}

export interface AgentTask {
  id: string;
  name: string;
  description?: string;
  task_type: string;
  category?: string;
  is_preset: boolean;
  prompt?: string;
  estimated_tokens?: number;
  tags?: string[];
  created_at: string;
}
