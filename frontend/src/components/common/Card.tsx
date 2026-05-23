import React from 'react';
import { Card as AntCard, CardProps as AntCardProps } from 'antd';
import { CSSProperties } from 'react';

interface CustomCardProps extends AntCardProps {
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  extra?: React.ReactNode;
  action?: React.ReactNode;
  children: React.ReactNode;
  style?: CSSProperties;
  className?: string;
  hoverable?: boolean;
  loading?: boolean;
}

const Card: React.FC<CustomCardProps> = ({
  title,
  subtitle,
  extra,
  action,
  children,
  style,
  className,
  hoverable = false,
  loading = false,
  ...props
}) => {
  return (
    <AntCard
      title={subtitle ? <div>{title}<div style={{fontSize: 12, color: '#999', marginTop: 4}}>{subtitle}</div></div> : title}
      extra={action || extra}
      hoverable={hoverable}
      loading={loading}
      style={style}
      className={className}
      {...props}
    >
      {children}
    </AntCard>
  );
};

export default Card;
