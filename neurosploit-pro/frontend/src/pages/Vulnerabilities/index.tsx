import React, { useEffect, useState } from 'react';
import { Table, Tag, Card, Select } from 'antd';
import { scanAPI, vulnerabilityAPI, type Scan, type Vulnerability } from '@/services/api';

const { Option } = Select;

const Vulnerabilities: React.FC = () => {
  const [scans, setScans] = useState<Scan[]>([]);
  const [selectedScan, setSelectedScan] = useState<string>('');
  const [vulns, setVulns] = useState<Vulnerability[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchScans();
  }, []);

  useEffect(() => {
    if (selectedScan) {
      fetchVulnerabilities(selectedScan);
    }
  }, [selectedScan]);

  const fetchScans = async () => {
    try {
      const res = await scanAPI.list();
      setScans(res.data);
      if (res.data.length > 0) {
        setSelectedScan(res.data[0].id);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchVulnerabilities = async (scanId: string) => {
    setLoading(true);
    try {
      const res = await vulnerabilityAPI.listByScan(scanId);
      setVulns(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string) => {
    const map: Record<string, string> = {
      critical: 'red',
      high: 'orange',
      medium: 'gold',
      low: 'blue',
      info: 'green',
    };
    return map[severity] || 'default';
  };

  const columns = [
    { title: 'Title', dataIndex: 'title', key: 'title' },
    { title: 'Type', dataIndex: 'vulnerability_type', key: 'vulnerability_type' },
    {
      title: 'Severity',
      dataIndex: 'severity',
      key: 'severity',
      render: (s: string) => <Tag color={getSeverityColor(s)}>{s.toUpperCase()}</Tag>,
    },
    { title: 'CVSS', dataIndex: 'cvss_score', key: 'cvss_score' },
    { title: 'Endpoint', dataIndex: 'affected_endpoint', key: 'affected_endpoint' },
  ];

  return (
    <div>
      <h1>Vulnerabilities</h1>
      <Card style={{ marginBottom: 16 }}>
        <Select
          style={{ width: 300 }}
          placeholder="Select a scan"
          value={selectedScan}
          onChange={setSelectedScan}
          options={scans.map(s => ({ value: s.id, label: s.name }))}
        />
      </Card>
      <Table
        columns={columns}
        dataSource={vulns}
        rowKey="id"
        loading={loading}
      />
    </div>
  );
};

export default Vulnerabilities;
