import { useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { message, Modal, Tag, Space, Button } from 'antd';
import {
  ProTable,
  ProColumns,
  ActionType,
} from '@ant-design/pro-components';
import { PlusOutlined, EyeOutlined, PlayCircleOutlined, PauseCircleOutlined, StopOutlined, DeleteOutlined } from '@ant-design/icons';
import { scansApi } from '../services/api';
import type { Scan } from '../types';

const STATUS_COLOR_MAP: Record<string, string> = {
  pending: 'default',
  running: 'processing',
  paused: 'warning',
  stopped: 'default',
  completed: 'success',
  failed: 'error',
};

export default function ScansPage() {
  const navigate = useNavigate();
  const actionRef = useRef<ActionType>(null);

  const handleCreateScan = useCallback(() => {
    navigate('/scan/new');
  }, [navigate]);

  const handleViewScan = useCallback((record: Scan) => {
    navigate(`/scan/${record.id}`);
  }, [navigate]);

  const handleStartScan = useCallback(async (record: Scan) => {
    try {
      await scansApi.start(record.id);
      message.success('扫描已启动');
      actionRef.current?.reload();
    } catch (error: any) {
      message.error(error.response?.data?.detail || '启动扫描失败');
    }
  }, []);

  const handlePauseScan = useCallback(async (record: Scan) => {
    try {
      await scansApi.pause(record.id);
      message.success('扫描已暂停');
      actionRef.current?.reload();
    } catch (error: any) {
      message.error(error.response?.data?.detail || '暂停扫描失败');
    }
  }, []);

  const handleStopScan = useCallback(async (record: Scan) => {
    try {
      await scansApi.stop(record.id);
      message.success('扫描已停止');
      actionRef.current?.reload();
    } catch (error: any) {
      message.error(error.response?.data?.detail || '停止扫描失败');
    }
  }, []);

  const handleDeleteScan = useCallback(async (record: Scan) => {
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除扫描 "${record.name}" 吗？此操作无法撤销。`,
      onOk: async () => {
        try {
          await scansApi.delete(record.id);
          message.success('删除成功');
          actionRef.current?.reload();
        } catch (error: any) {
          message.error(error.response?.data?.detail || '删除失败');
        }
      },
    });
  }, []);

  const columns: ProColumns<Scan>[] = [
    {
      title: '扫描名称',
      dataIndex: 'name',
      key: 'name',
      search: true,
      render: (text, record) => (
        <a onClick={() => handleViewScan(record)}>{text}</a>
      ),
    },
    {
      title: '扫描类型',
      dataIndex: 'scan_type',
      key: 'scan_type',
      search: true,
      valueEnum: {
        quick: { text: '快速扫描' },
        full: { text: '全面扫描' },
        custom: { text: '自定义扫描' },
      },
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      search: true,
      valueEnum: {
        pending: { text: '等待中' },
        running: { text: '运行中' },
        paused: { text: '已暂停' },
        stopped: { text: '已停止' },
        completed: { text: '已完成' },
        failed: { text: '失败' },
      },
      render: (text) => (
        <Tag color={STATUS_COLOR_MAP[text as string] || 'default'}>
          {text}
        </Tag>
      ),
    },
    {
      title: '进度',
      dataIndex: 'progress',
      key: 'progress',
      render: (text, record) => (
        <div>
          <div style={{ width: 100, height: 8, background: '#f0f0f0', borderRadius: 4, overflow: 'hidden' }}>
            <div 
              style={{ 
                width: `${Math.min((text as number) || 0, 100)}%`, 
                height: '100%', 
                background: (record.status === 'failed') ? '#ff4d4f' : 
                          (record.status === 'completed') ? '#52c41a' : '#1890ff',
                transition: 'width 0.3s'
              }} 
            />
          </div>
          <span style={{ fontSize: 12, color: '#999' }}>{text}%</span>
        </div>
      ),
    },
    {
      title: '漏洞数量',
      key: 'vulnerabilities',
      search: false,
      render: (_, record) => (
        <Space size={[8, 4]} wrap>
          {record.critical_count > 0 && (
            <Tag color="red">{record.critical_count} 严重</Tag>
          )}
          {record.high_count > 0 && (
            <Tag color="orange">{record.high_count} 高危</Tag>
          )}
          {record.medium_count > 0 && (
            <Tag color="gold">{record.medium_count} 中危</Tag>
          )}
          {record.low_count > 0 && (
            <Tag color="blue">{record.low_count} 低危</Tag>
          )}
          {record.info_count > 0 && (
            <Tag color="default">{record.info_count} 信息</Tag>
          )}
        </Space>
      ),
    },
    {
      title: '当前阶段',
      dataIndex: 'current_phase',
      key: 'current_phase',
      search: false,
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      search: false,
      valueType: 'dateTime',
    },
    {
      title: '操作',
      valueType: 'option',
      key: 'option',
      render: (_, record) => [
        <a key="view" onClick={() => handleViewScan(record)}>
          <EyeOutlined /> 查看
        </a>,
        ...((record.status === 'pending' || record.status === 'stopped' || record.status === 'paused') ? [
          <a 
            key="start" 
            onClick={() => handleStartScan(record)}
            style={{ color: '#52c41a' }}
          >
            <PlayCircleOutlined /> 启动
          </a>
        ] : []),
        ...(record.status === 'running' ? [
          <a 
            key="pause" 
            onClick={() => handlePauseScan(record)}
            style={{ color: '#faad14' }}
          >
            <PauseCircleOutlined /> 暂停
          </a>
        ] : []),
        ...(record.status === 'running' || record.status === 'paused' ? [
          <a 
            key="stop" 
            onClick={() => handleStopScan(record)}
            style={{ color: '#ff4d4f' }}
          >
            <StopOutlined /> 停止
          </a>
        ] : []),
        ...(record.status !== 'running' ? [
          <a 
            key="delete" 
            onClick={() => handleDeleteScan(record)}
            style={{ color: '#ff4d4f' }}
          >
            <DeleteOutlined /> 删除
          </a>
        ] : []),
      ],
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <ProTable<Scan>
        headerTitle="扫描管理"
        actionRef={actionRef}
        columns={columns}
        rowKey="id"
        pagination={{
          pageSize: 10,
          showQuickJumper: true,
          showSizeChanger: true,
          showTotal: (total) => `共 ${total} 条记录`,
        }}
        request={async () => {
          const data = await scansApi.list(1, 100);
          return {
            data: data.scans || [],
            success: true,
            total: data.total || (data.scans?.length || 0),
          };
        }}
        toolBarRender={() => [
          <Button 
            type="primary" 
            key="button"
            onClick={handleCreateScan}
          >
            <PlusOutlined /> 新建扫描
          </Button>,
        ]}
      />
    </div>
  );
}
