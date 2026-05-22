import React, { useState } from 'react';
import { ProLayout } from '@ant-design/pro-layout';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Avatar, Dropdown, Space, Tag } from 'antd';
import { UserOutlined, LogoutOutlined, SettingOutlined } from '@ant-design/icons';
import proSettings from '../../config/proSettings';
import menuData from '../../config/menuData';

const Layout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [pathname, setPathname] = useState(location.pathname);

  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人中心',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '系统设置',
    },
    {
      type: 'divider' as const,
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      danger: true,
    },
  ];

  const rightContentRender = () => (
    <Space size={16}>
      <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
        <Space style={{ cursor: 'pointer' }}>
          <Avatar size="small" icon={<UserOutlined />} />
          <span>admin</span>
          <Tag color="blue">管理员</Tag>
        </Space>
      </Dropdown>
    </Space>
  );

  return (
    <ProLayout
      {...proSettings}
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
