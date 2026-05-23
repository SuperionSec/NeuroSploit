import {
  DashboardOutlined,
  UserOutlined,
  ScanOutlined,
  RocketOutlined,
  ExperimentOutlined,
  RobotOutlined,
  FileTextOutlined,
  ClockCircleOutlined,
  BugOutlined,
  CloudServerOutlined,
  BookOutlined,
  ApiOutlined,
  CloudOutlined,
  SettingOutlined,
  QuestionCircleOutlined,
} from '@ant-design/icons';

export const menuData = [
  {
    path: '/dashboard',
    name: '仪表板',
    icon: <DashboardOutlined />,
  },
  {
    path: '/users',
    name: '用户管理',
    icon: <UserOutlined />,
  },
  {
    path: '/scans',
    name: '扫描管理',
    icon: <ScanOutlined />,
    children: [
      { path: '/scans', name: '扫描列表' },
      { path: '/scan/new', name: '新建扫描' },
    ],
  },
  {
    path: '/auto-pentest',
    name: '自动渗透',
    icon: <RocketOutlined />,
  },
  {
    path: '/full-ia',
    name: 'FULL AI Testing',
    icon: <ExperimentOutlined />,
  },
  {
    path: '/agent',
    name: 'AI Agent',
    icon: <RobotOutlined />,
  },
  {
    path: '/reports',
    name: '报告管理',
    icon: <FileTextOutlined />,
  },
  {
    path: '/scheduler',
    name: '任务调度',
    icon: <ClockCircleOutlined />,
  },
  {
    path: '/vuln-lab',
    name: '漏洞实验室',
    icon: <BugOutlined />,
  },
  {
    path: '/sandbox',
    name: '沙箱管理',
    icon: <CloudServerOutlined />,
  },
  {
    path: '/knowledge',
    name: '知识库',
    icon: <BookOutlined />,
  },
  {
    path: '/mcp',
    name: 'MCP 管理',
    icon: <ApiOutlined />,
  },
  {
    path: '/providers',
    name: 'LLM 提供商',
    icon: <CloudOutlined />,
  },
  {
    path: '/settings',
    name: '系统设置',
    icon: <SettingOutlined />,
  },
  {
    path: '/help',
    name: '帮助文档',
    icon: <QuestionCircleOutlined />,
  },
];

export default menuData;
