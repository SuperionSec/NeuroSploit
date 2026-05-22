import { defineConfig } from '@umijs/max';

export default defineConfig({
  routes: [
    {
      path: '/login',
      component: './Login',
      layout: false,
    },
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      name: 'Dashboard',
      path: '/dashboard',
      icon: 'DashboardOutlined',
      component: './Dashboard',
    },
    {
      name: 'Scans',
      path: '/scans',
      icon: 'SafetyOutlined',
      component: './Scans',
    },
    {
      name: 'Vulnerabilities',
      path: '/vulnerabilities',
      icon: 'BugOutlined',
      component: './Vulnerabilities',
    },
  ],
  layout: {
    title: 'NeuroSploit Pro',
    locale: false,
  },
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
  publicPath: '/',
  history: { type: 'browser' },
  npmClient: 'npm',
});
