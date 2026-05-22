import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Spin } from 'antd';
import { SafetyOutlined, BugOutlined, CheckCircleOutlined, ClockCircleOutlined } from '@ant-design/icons';
import { scanAPI, type Scan } from '@/services/api';

const Dashboard: React.FC = () => {
  const [scans, setScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchScans();
  }, []);

  const fetchScans = async () => {
    try {
      const res = await scanAPI.list();
      setScans(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const stats = {
    totalScans: scans.length,
    totalVulns: scans.reduce((acc, s) => acc + s.total_vulnerabilities, 0),
    criticalVulns: scans.reduce((acc, s) => acc + s.critical_count, 0),
    highVulns: scans.reduce((acc, s) => acc + s.high_count, 0),
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <Spin spinning={loading}>
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Total Scans"
                value={stats.totalScans}
                prefix={<SafetyOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Total Vulnerabilities"
                value={stats.totalVulns}
                prefix={<BugOutlined />}
                valueStyle={{ color: '#cf1322' }}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Critical Vulns"
                value={stats.criticalVulns}
                prefix={<CheckCircleOutlined />}
                valueStyle={{ color: '#cf1322' }}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="High Vulns"
                value={stats.highVulns}
                prefix={<ClockCircleOutlined />}
                valueStyle={{ color: '#faad14' }}
              />
            </Card>
          </Col>
        </Row>
      </Spin>
    </div>
  );
};

export default Dashboard;
