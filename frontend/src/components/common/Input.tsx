import React from 'react';
import { Input as AntInput, InputProps } from 'antd';

const { TextArea: AntTextArea } = AntInput;

interface CustomInputProps extends InputProps {
  label?: string;
  error?: string;
  helper?: string;
  helperText?: string;
}

const Input: React.FC<CustomInputProps> = ({
  label,
  error,
  helper,
  helperText,
  ...props
}) => {
  const actualHelper = helperText || helper;
  return (
    <div>
      {label && (
        <label style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>
          {label}
        </label>
      )}
      <AntInput {...props} />
      {actualHelper && !error && (
        <div style={{ color: '#999', marginTop: 4, fontSize: 12 }}>
          {actualHelper}
        </div>
      )}
      {error && (
        <div style={{ color: '#ff4d4f', marginTop: 4, fontSize: 12 }}>
          {error}
        </div>
      )}
    </div>
  );
};

interface CustomTextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  helper?: string;
  helperText?: string;
}

const TextArea: React.FC<CustomTextAreaProps> = ({
  label,
  error,
  helper,
  helperText,
  ...props
}) => {
  const actualHelper = helperText || helper;
  return (
    <div>
      {label && (
        <label style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>
          {label}
        </label>
      )}
      <AntTextArea {...props} />
      {actualHelper && !error && (
        <div style={{ color: '#999', marginTop: 4, fontSize: 12 }}>
          {actualHelper}
        </div>
      )}
      {error && (
        <div style={{ color: '#ff4d4f', marginTop: 4, fontSize: 12 }}>
          {error}
        </div>
      )}
    </div>
  );
};

export { Input as default, TextArea };
