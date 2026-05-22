import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface Scan {
  id: string;
  name: string;
  status: string;
  scan_type: string;
  target_url: string;
  progress: number;
  created_by: string;
  created_at: string;
  total_vulnerabilities: number;
  critical_count: number;
  high_count: number;
}

export interface Vulnerability {
  id: string;
  title: string;
  vulnerability_type: string;
  severity: string;
  cvss_score: number;
  description: string;
  affected_endpoint: string;
}

export const authAPI = {
  login: (username: string, password: string) => 
    api.post('/auth/login', new URLSearchParams({ username, password })),
  register: (data: any) => api.post('/users', data),
  getCurrentUser: () => api.get('/users/me'),
};

export const scanAPI = {
  list: () => api.get<Scan[]>('/scans'),
  create: (data: any) => api.post('/scans', data),
  get: (id: string) => api.get<Scan>(`/scans/${id}`),
  update: (id: string, data: any) => api.put(`/scans/${id}`, data),
  delete: (id: string) => api.delete(`/scans/${id}`),
};

export const vulnerabilityAPI = {
  listByScan: (scanId: string) => api.get<Vulnerability[]>(`/vulnerabilities/scan/${scanId}`),
  create: (data: any) => api.post('/vulnerabilities', data),
};

export default api;
