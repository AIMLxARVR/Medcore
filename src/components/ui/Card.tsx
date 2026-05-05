import React from 'react';
import styles from './Card.module.css';

interface CardProps {
  children: React.ReactNode;
  style?: React.CSSProperties;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'interactive' | 'bordered' | 'elevated';
  onClick?: () => void;
}

const Card = ({
  children,
  style: sx = {},
  size = 'md',
  variant = 'default',
  onClick
}: CardProps) => {
  const cardClasses = [
    styles.card,
    styles[size],
    variant !== 'default' ? styles[variant] : '',
  ].filter(Boolean).join(' ');

  return (
    <div
      className={cardClasses}
      style={sx}
      onClick={onClick}
    >
      {children}
    </div>
  );
};

export default Card;