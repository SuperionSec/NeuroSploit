import React from 'react';
import { Button as AntButton, ButtonProps } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

interface CustomButtonProps extends ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger' | 'success';
}

const Button: React.FC<CustomButtonProps> = ({ 
  children, 
  variant = 'primary', 
  loading, 
  icon,
  ...props 
}) => {
  const getButtonType = () => {
    switch (variant) {
      case 'danger':
        return 'primary';
      case 'success':
        return 'primary';
      default:
        return props.type || 'default';
    }
  };

  const getButtonColor = () => {
    if (variant === 'danger') {
      return '#ff4d4f';
    }
    if (variant === 'success') {
      return '#52c41a';
    }
    return undefined;
  };

  return (
    <AntButton
      type={getButtonType()}
      style={{ 
        backgroundColor: getButtonColor(),
        borderColor: getButtonColor(),
      }}
      loading={loading}
      icon={loading ? <LoadingOutlined /> : icon}
      {...props}
    >
      {children}
    </AntButton>
  );
};

export default Button;
