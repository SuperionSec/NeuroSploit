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

export default Badge;
