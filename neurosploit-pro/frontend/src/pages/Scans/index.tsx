import React, { useEffect, useState } from 'react';
import { Button, Table, Modal, Form, Input, Select, message, Space, Tag } from 'antd';
import { PlusOutlined, EyeOutlined, DeleteOutlined } from '@ant-design/icons';
import { scanAPI, type Scan } from '@/services/api';

const { Option } = Select;

const Scans: React.FC = () => {
  const [scans, setScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchScans();
  }, []);

  const fetchScans = async () => {
    setLoading(true);
    try {
      const res = await scanAPI.list();
      setScans(res.data);
    } catch (err) {
      message.error('Failed to fetch scans');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (values: any) => {
    try {
      await scanAPI.create(values);
      message.success('Scan created successfully');
      setModalVisible(false);
      form.resetFields();
      fetchScans();
    } catch (err) {
      message.error('Failed to create scan');
    }
  };

  const getStatusColor = (status: string) => {
    const map: Record<string, string> = {
      completed: 'green',
      running: 'blue',
      pending: 'orange',
      failed: 'red',
    };
    return map[status] || 'default';
  };

  const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Target', dataIndex: 'target_url', key: 'target_url' },
    { 
      title: 'Status', 
      dataIndex: 'status', 
      key: 'status', 
      render: (status: string) => <Tag color={getStatusColor(status)}>{status}</Tag>,
    },
    { title: 'Progress', dataIndex: 'progress', key: 'progress', render: (p: number) => `${p}%` },
    { title: 'Vulns', dataIndex: 'total_vulnerabilities', key: 'total_vulnerabilities' },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Scan) => (
        <Space>
          <Button icon={<EyeOutlined />} size="small">View</Button>
          <Button icon={<DeleteOutlined />} size="small" danger>Delete</Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
        <h1>Scans</h1>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
          New Scan
        </Button>
      </div>

      <Table columns={columns} dataSource={scans} rowKey="id" loading={loading} />

      <Modal
        title="Create New Scan"
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
      >
        <Form form={form} layout="vertical" onFinish={handleCreate}>
          <Form.Item
            name="name"
            label="Name"
            rules={[{ required: true, message: 'Required' }]}
          >
            <Input placeholder="Scan name" />
          </Form.Item>
          <Form.Item
            name="target_url"
            label="Target URL"
            rules={[{ required: true, message: 'Required' }]}
          >
            <Input placeholder="https://target.com" />
          </Form.Item>
          <Form.Item name="scan_type" label="Scan Type" initialValue="full">
            <Select>
              <Option value="full">Full Scan</Option>
              <Option value="quick">Quick Scan</Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">Create</Button>
              <Button onClick={() => setModalVisible(false)}>Cancel</Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Scans;
