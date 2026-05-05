import React from 'react';
import styles from './Avatar.module.css';

interface AvatarProps {
  init: string;
  color?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | number;
}

const Avatar = ({ init, color, size = 'md' }: AvatarProps) => {
  const sizeClass = typeof size === 'string' ? styles[size] : '';
  const customStyle = typeof size === 'number' ? {
    width: `${size}px`,
    height: `${size}px`,
    fontSize: `${size * 0.3}px`,
  } : {};

  return (
    <div
      className={`${styles.avatar} ${sizeClass}`}
      style={{
        backgroundColor: color ? `${color}22` : undefined,
        borderColor: color ? `${color}44` : undefined,
        color: color || undefined,
        ...customStyle,
      }}
    >
      {init}
    </div>
  );
};

export default Avatar;