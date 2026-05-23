import React from 'react';
import { Button as AntButton, ButtonProps } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

type CustomVariant = 'primary' | 'secondary' | 'danger' | 'success' | 'ghost';

interface CustomButtonProps extends Omit<ButtonProps, 'variant'> {
  customVariant?: CustomVariant;
  isLoading?: boolean;
}

const Button: React.FC<CustomButtonProps> = ({ 
  children, 
  customVariant = 'primary', 
  loading, 
  isLoading,
  icon,
  ...props 
}) => {
  const actualLoading = isLoading || loading;
  const getButtonType = () => {
    switch (customVariant) {
      case 'danger':
        return 'primary';
      case 'success':
        return 'primary';
      case 'ghost':
        return 'default';
      default:
        return props.type || 'default';
    }
  };

  const getButtonColor = () => {
    if (customVariant === 'danger') {
      return '#ff4d4f';
    }
    if (customVariant === 'success') {
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
      loading={actualLoading}
      icon={actualLoading ? <LoadingOutlined /> : icon}
      {...props}
    >
      {children}
    </AntButton>
  );
};

export default Button;
