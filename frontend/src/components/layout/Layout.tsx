import React, { useState, useEffect } from 'react';
import { ProLayout } from '@ant-design/pro-layout';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Avatar, Dropdown, Space, Tag, Modal, message } from 'antd';
import { UserOutlined, LogoutOutlined, SettingOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import proSettings from '../../config/proSettings';
import menuData from '../../config/menuData';
import { useAuthStore } from '../../store/authStore';

const { confirm } = Modal;

const Layout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [pathname, setPathname] = useState(location.pathname);
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);

  useEffect(() => {
    setPathname(location.pathname);
  }, [location.pathname]);

  const showLogoutConfirm = () => {
    confirm({
      title: '确认退出',
      icon: <ExclamationCircleOutlined />,
      content: '确定要退出登录吗？',
      okText: '确认',
      cancelText: '取消',
      onOk: () => {
        logout();
        message.success('已退出登录');
      },
    });
  };

  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: user?.username || '用户',
    },
    {
      key: 'email',
      icon: <UserOutlined />,
      label: user?.email || '',
      disabled: true,
    },
    {
      type: 'divider' as const,
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '系统设置',
      onClick: () => navigate('/settings'),
    },
    {
      type: 'divider' as const,
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      danger: true,
      onClick: showLogoutConfirm,
    },
  ];

  const rightContentRender = () => (
    <Space size={16}>
      <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
        <Space style={{ cursor: 'pointer' }}>
          <Avatar size="small" icon={<UserOutlined />} style={{ backgroundColor: '#1890ff' }} />
          <span>{user?.username || '未登录'}</span>
          <Tag color={user?.role === 'admin' ? 'blue' : 'default'}>
            {user?.role === 'admin' ? '管理员' : '用户'}
          </Tag>
        </Space>
      </Dropdown>
    </Space>
  );

  return (
    <ProLayout
      {...proSettings}
      title="NeuroSploit v3"
      logo="https://gw.alipayobjects.com/zos/rmsportal/KDpgvguMpGfqaHPjicRK.svg"
      location={{
        pathname,
      }}
      menuDataRender={() => menuData}
      menuItemRender={(item, dom) => (
        <div
          onClick={() => {
            setPathname(item.path || '/');
            navigate(item.path || '/');
          }}
        >
          {dom}
        </div>
      )}
      rightContentRender={rightContentRender}
    >
      <div style={{ padding: 24 }}>
        <Outlet />
      </div>
    </ProLayout>
  );
};

export default Layout;
