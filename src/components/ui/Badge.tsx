import React from 'react';
import styles from './Badge.module.css';

interface BadgeProps {
  text: string;
  color?: string;
  bg?: string;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'primary' | 'success' | 'warning' | 'error';
}

const Badge = ({ 
  text, 
  color, 
  bg, 
  size = 'md',
  variant = 'primary'
}: BadgeProps) => {
  const customStyle = {
    color: color || undefined,
    backgroundColor: bg || undefined,
  };

  return (
    <span 
      className={`${styles.badge} ${styles[size]} ${styles[variant]}`}
      style={customStyle}
    >
      {text}
    </span>
  );
};

export default Badge;