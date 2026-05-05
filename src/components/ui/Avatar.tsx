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

  // Build style object with explicit values to ensure they're applied
  const style: React.CSSProperties = {
    ...customStyle,
  };

  // Only apply color styles if color is provided
  if (color) {
    style.backgroundColor = `${color}22`;
    style.borderColor = `${color}44`;
    style.color = color;
  }

  return (
    <div
      className={`${styles.avatar} ${sizeClass}`}
      style={style}
    >
      {init}
    </div>
  );
};

export default Avatar;