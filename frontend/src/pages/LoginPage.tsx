import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, message, Tabs, Input, Button } from 'antd';
import { UserOutlined, LockOutlined, SafetyOutlined } from '@ant-design/icons';
import { authApi } from '../services/api';
import { apiClient } from '../services/apiClient';
import { useAuthStore } from '../store/authStore';

export default function LoginPage() {
  const navigate = useNavigate();
  const [loginType, setLoginType] = useState<'account' | 'register'>('account');
  const [loading, setLoading] = useState(false);
  const setAuth = useAuthStore((state) => state.setAuth);

  const handleSubmit = async (values: { username: string; password: string }) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', values.username);
      formData.append('password', values.password);

      const response = await apiClient.post('/auth/login', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const { access_token } = response.data;

      const userResponse = await apiClient.get('/auth/me');

      setAuth(access_token, userResponse.data);

      message.success('登录成功！');
      navigate('/');
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || '登录失败，请检查用户名和密码';
      message.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (values: { username: string; email: string; password: string }) => {
    setLoading(true);
    try {
      await authApi.register(values.username, values.email, values.password);
      message.success('注册成功，请登录！');
      setLoginType('account');
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || '注册失败，用户名或邮箱可能已存在';
      message.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleFinish = async (values: any) => {
    if (loginType === 'account') {
      await handleSubmit(values);
    } else {
      await handleRegister(values);
    }
  };

  return (
    <div
      style={{
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      }}
    >
      <div
        style={{
          width: 450,
          padding: 24,
          background: 'white',
          borderRadius: 8,
          boxShadow: '0 4px 24px rgba(0, 0, 0, 0.15)',
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: 24 }}>
          <h1 style={{ fontSize: 28, fontWeight: 'bold', color: '#1890ff', marginBottom: 8 }}>
            NeuroSploit v3
          </h1>
          <p style={{ color: '#666', fontSize: 14 }}>AI-Powered Penetration Testing Platform</p>
        </div>
        <Tabs
          activeKey={loginType}
          onChange={(key) => setLoginType(key as 'account' | 'register')}
          items={[
            {
              key: 'account',
              label: '账户密码登录',
              children: (
                <Form onFinish={handleFinish} size="large">
                  <Form.Item
                    name="username"
                    rules={[{ required: true, message: '请输入用户名' }]}
                  >
                    <Input prefix={<UserOutlined />} placeholder="用户名: admin" />
                  </Form.Item>
                  <Form.Item
                    name="password"
                    rules={[{ required: true, message: '请输入密码' }]}
                  >
                    <Input.Password prefix={<LockOutlined />} placeholder="密码: neurosploit" />
                  </Form.Item>
                  <Button type="primary" htmlType="submit" block loading={loading} size="large">
                    登录
                  </Button>
                </Form>
              ),
            },
            {
              key: 'register',
              label: '注册账户',
              children: (
                <Form onFinish={handleFinish} size="large">
                  <Form.Item
                    name="username"
                    rules={[{ required: true, message: '请输入用户名' }]}
                  >
                    <Input prefix={<UserOutlined />} placeholder="用户名" />
                  </Form.Item>
                  <Form.Item
                    name="email"
                    rules={[
                      { required: true, message: '请输入邮箱' },
                      { type: 'email', message: '请输入有效的邮箱地址' },
                    ]}
                  >
                    <Input prefix={<SafetyOutlined />} placeholder="邮箱" />
                  </Form.Item>
                  <Form.Item
                    name="password"
                    rules={[{ required: true, message: '请输入密码' }]}
                  >
                    <Input.Password prefix={<LockOutlined />} placeholder="密码" />
                  </Form.Item>
                  <Button type="primary" htmlType="submit" block loading={loading} size="large">
                    注册
                  </Button>
                </Form>
              ),
            },
          ]}
        />
      </div>
    </div>
  );
}
