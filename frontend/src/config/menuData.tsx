import { QuestionCircleOutlined, CrownOutlined, ToolOutlined, UserOutlined } from '@ant-design/icons';
import {
  HomeOutlined, ThunderboltOutlined, RadarChartOutlined, BugOutlined,
  ExperimentOutlined, FileTextOutlined, FormOutlined, ClockCircleOutlined, SettingOutlined
} from '@ant-design/icons';

export const menuData = [
  {
    path: '/dashboard',
    name: '仪表板',
    icon: <CrownOutlined />,
  },
  {
    path: '/users',
    name: '用户管理',
    icon: <UserOutlined />,
  },
  {
    path: '/scan',
    name: '扫描管理',
    icon: <ToolOutlined />,
  },
  {
    path: '/auto-pentest',
    name: '自动渗透',
    icon: <ToolOutlined />,
  },
  {
    path: '/full-ia',
    name: 'FULL AI Testing',
    icon: <ToolOutlined />,
  },
  {
    path: '/agent',
    name: 'AI Agent',
    icon: <ToolOutlined />,
  },
  {
    path: '/reports',
    name: '报告管理',
    icon: <ToolOutlined />,
  },
  {
    path: '/scheduler',
    name: '任务调度',
    icon: <ToolOutlined />,
  },
  {
    path: '/vuln-lab',
    name: '漏洞实验室',
    icon: <ToolOutlined />,
  },
  {
    path: '/sandbox',
    name: '沙箱管理',
    icon: <ToolOutlined />,
  },
  {
    path: '/knowledge',
    name: '知识库',
    icon: <ToolOutlined />,
  },
  {
    path: '/mcp',
    name: 'MCP 管理',
    icon: <ToolOutlined />,
  },
  {
    path: '/providers',
    name: 'LLM 提供商',
    icon: <ToolOutlined />,
  },
  {
    name: 'NeuroSploit',
    icon: '🛡️',
    children: [
      { name: 'Dashboard', path: '/neurosploit', icon: <HomeOutlined /> },
      { name: 'Auto Pentest', path: '/neurosploit/auto', icon: <ThunderboltOutlined /> },
      { name: 'Scans', path: '/neurosploit/scans', icon: <RadarChartOutlined /> },
      { name: 'Vulnerabilities', path: '/neurosploit/vulnerabilities', icon: <BugOutlined /> },
      { name: 'Vuln Lab', path: '/neurosploit/vuln-lab', icon: <ExperimentOutlined /> },
      { name: 'Reports', path: '/neurosploit/reports', icon: <FileTextOutlined /> },
      { name: 'Prompts', path: '/neurosploit/prompts', icon: <FormOutlined /> },
      { name: 'Scheduler', path: '/neurosploit/scheduler', icon: <ClockCircleOutlined /> },
      { name: 'Settings', path: '/neurosploit/settings', icon: <SettingOutlined /> },
    ],
  },
  {
    path: '/settings',
    name: '系统设置',
    icon: <ToolOutlined />,
  },
  {
    path: '/help',
    name: '帮助文档',
    icon: <QuestionCircleOutlined />,
  },
];

export default menuData;
