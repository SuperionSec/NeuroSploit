import React from 'react';
import { Card as AntCard, CardProps as AntCardProps } from 'antd';
import { CSSProperties } from 'react';

interface CustomCardProps extends AntCardProps {
  title?: React.ReactNode;
  extra?: React.ReactNode;
  children: React.ReactNode;
  style?: CSSProperties;
  className?: string;
  hoverable?: boolean;
  bordered?: boolean;
  loading?: boolean;
}

const Card: React.FC<CustomCardProps> = ({
  title,
  extra,
  children,
  style,
  className,
  hoverable = false,
  bordered = true,
  loading = false,
  ...props
}) => {
  return (
    <AntCard
      title={title}
      extra={extra}
      hoverable={hoverable}
      bordered={bordered}
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
