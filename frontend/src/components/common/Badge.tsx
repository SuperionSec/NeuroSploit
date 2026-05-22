import React from 'react';
import { Badge as AntBadge, BadgeProps } from 'antd';

interface CustomBadgeProps extends BadgeProps {
  children?: React.ReactNode;
  status?: 'success' | 'processing' | 'default' | 'error' | 'warning';
  text?: string;
  color?: string;
}

const Badge: React.FC<CustomBadgeProps> = ({
  children,
  status,
  text,
  color,
  ...props
}) => {
  if (status || color) {
    return (
      <AntBadge
        status={status as any}
        text={text}
        color={color}
        {...props}
      />
    );
  }

  return (
    <AntBadge {...props}>
      {children}
    </AntBadge>
  );
};

interface SeverityBadgeProps {
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
}

const SeverityBadge: React.FC<SeverityBadgeProps> = ({ severity }) => {
  const config = {
    critical: { color: '#ff4d4f', text: '严重' },
    high: { color: '#fa8c16', text: '高危' },
    medium: { color: '#faad14', text: '中危' },
    low: { color: '#52c41a', text: '低危' },
    info: { color: '#1890ff', text: '信息' },
  };

  const { color, text } = config[severity] || config.info;

  return <AntBadge color={color} text={text} />;
};

export { Badge, SeverityBadge };
export default Badge;
