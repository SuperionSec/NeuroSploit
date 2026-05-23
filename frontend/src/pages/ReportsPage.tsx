import { useState, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { message, Modal, Tag, Space, Button, Tooltip } from 'antd';
import {
  ProTable,
  ProColumns,
  ActionType,
} from '@ant-design/pro-components';
import {
  PlusOutlined,
  EyeOutlined,
  DeleteOutlined,
  FileTextOutlined,
  FilePdfOutlined,
  FileZipOutlined,
  ThunderboltOutlined,
} from '@ant-design/icons';
import { reportsApi, scansApi } from '../services/api';
import type { Report, Scan } from '../types';

export default function ReportsPage() {
  const navigate = useNavigate();
  const actionRef = useRef<ActionType>(null);
  const [scansMap, setScansMap] = useState<Map<string, Scan>>(new Map());

  const loadScans = useCallback(async () => {
    try {
      const data = await scansApi.list(1, 100);
      const map = new Map<string, Scan>();
      (data.scans || []).forEach((scan: Scan) => {
        map.set(scan.id, scan);
      });
      setScansMap(map);
    } catch (error) {
      console.error('Failed to load scans:', error);
    }
  }, []);

  const handleCreateScan = useCallback(() => {
    navigate('/scan/new');
  }, [navigate]);

  const handleViewReport = useCallback((record: Report) => {
    window.open(reportsApi.getViewUrl(record.id), '_blank');
  }, []);

  const handleDownload = useCallback(async (record: Report, format: string) => {
    try {
      window.open(reportsApi.getDownloadUrl(record.id, format), '_blank');
    } catch (error: any) {
      message.error(error.response?.data?.detail || '下载失败');
    }
  }, []);

  const handleDownloadZip = useCallback(async (record: Report) => {
    try {
      window.open(reportsApi.getDownloadZipUrl(record.id), '_blank');
    } catch (error: any) {
      message.error(error.response?.data?.detail || '下载失败');
    }
  }, []);

  const handleAiRegenerate = useCallback(async (record: Report) => {
    try {
      const scan = scansMap.get(record.scan_id);
      const title = scan?.name || 'AI Report';
      const report = await reportsApi.generateAiReport({
        scan_id: record.scan_id,
        title: `AI Report - ${title}`,
      });
      window.open(reportsApi.getViewUrl(report.id), '_blank');
      message.success('AI 报告生成成功');
      actionRef.current?.reload();
      await loadScans();
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'AI 报告生成失败');
    }
  }, [scansMap, loadScans]);

  const handleDeleteReport = useCallback(async (record: Report) => {
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除报告吗？此操作无法撤销。`,
      onOk: async () => {
        try {
          await reportsApi.delete(record.id);
          message.success('删除成功');
          actionRef.current?.reload();
        } catch (error: any) {
          message.error(error.response?.data?.detail || '删除失败');
        }
      },
    });
  }, []);

  const columns: ProColumns<Report>[] = [
    {
      title: '报告标题',
      dataIndex: 'title',
      key: 'title',
      search: true,
      render: (text, record) => {
        const scan = scansMap.get(record.scan_id);
        const title = text || scan?.name || 'Security Report';
        return (
          <a onClick={() => handleViewReport(record)}>
            {title}
          </a>
        );
      },
    },
    {
      title: '格式',
      dataIndex: 'format',
      key: 'format',
      search: true,
      valueEnum: {
        html: { text: 'HTML' },
        pdf: { text: 'PDF' },
        json: { text: 'JSON' },
      },
      render: (text) => {
        const icons = {
          html: <FileTextOutlined />,
          pdf: <FilePdfOutlined />,
          json: <FileTextOutlined />,
        };
        return (
          <Tag color="blue" icon={icons[text as keyof typeof icons]}>
            {((text as string) || 'html').toUpperCase()}
          </Tag>
        );
      },
    },
    {
      title: '漏洞数量',
      key: 'vulnerabilities',
      search: false,
      render: (_, record) => {
        const scan = scansMap.get(record.scan_id);
        if (!scan) return <span>-</span>;
        return (
          <Space size={[8, 4]} wrap>
            {scan.critical_count > 0 && (
              <Tag color="red">{scan.critical_count} 严重</Tag>
            )}
            {scan.high_count > 0 && (
              <Tag color="orange">{scan.high_count} 高危</Tag>
            )}
            {scan.medium_count > 0 && (
              <Tag color="gold">{scan.medium_count} 中危</Tag>
            )}
            {scan.low_count > 0 && (
              <Tag color="blue">{scan.low_count} 低危</Tag>
            )}
            {scan.info_count > 0 && (
              <Tag color="default">{scan.info_count} 信息</Tag>
            )}
          </Space>
        );
      },
    },
    {
      title: '类型',
      dataIndex: 'auto_generated',
      key: 'auto_generated',
      search: false,
      render: (_, record) => (
        <>
          {record.auto_generated && (
            <Tag color="orange" icon={<ThunderboltOutlined />}>AI 生成</Tag>
          )}
          {record.is_partial && (
            <Tag color="orange">部分报告</Tag>
          )}
        </>
      ),
    },
    {
      title: '生成时间',
      dataIndex: 'generated_at',
      key: 'generated_at',
      search: false,
      valueType: 'dateTime',
    },
    {
      title: '操作',
      valueType: 'option',
      key: 'option',
      render: (_, record) => [
        <a key="view" onClick={() => handleViewReport(record)}>
          <EyeOutlined /> 查看
        </a>,
        <Tooltip title="下载 HTML">
          <a 
            key="download-html"
            onClick={() => handleDownload(record, 'html')}
            style={{ color: '#1890ff' }}
          >
            <FileTextOutlined /> HTML
          </a>
        </Tooltip>,
        <Tooltip title="下载 JSON">
          <a 
            key="download-json"
            onClick={() => handleDownload(record, 'json')}
            style={{ color: '#52c41a' }}
          >
            <FileTextOutlined /> JSON
          </a>
        </Tooltip>,
        <Tooltip title="下载 ZIP">
          <a 
            key="download-zip"
            onClick={() => handleDownloadZip(record)}
            style={{ color: '#722ed1' }}
          >
            <FileZipOutlined /> ZIP
          </a>
        </Tooltip>,
        <Tooltip title="AI 重新生成">
          <a 
            key="ai-regenerate"
            onClick={() => handleAiRegenerate(record)}
            style={{ color: '#faad14' }}
          >
            <ThunderboltOutlined /> AI
          </a>
        </Tooltip>,
        <a 
          key="delete"
          onClick={() => handleDeleteReport(record)}
          style={{ color: '#ff4d4f' }}
        >
          <DeleteOutlined /> 删除
        </a>,
      ],
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <ProTable<Report>
        headerTitle="报告管理"
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
          await loadScans();
          const data = await reportsApi.list();
          return {
            data: data.reports || [],
            success: true,
            total: data.total || (data.reports?.length || 0),
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
