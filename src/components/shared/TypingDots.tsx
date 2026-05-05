import React from 'react';
import styles from './TypingDots.module.css';

interface TypingDotsProps {
  size?: 'sm' | 'md' | 'lg';
  color?: 'primary' | 'success' | 'warning' | 'error' | 'default';
  label?: string;
}

const TypingDots = ({ 
  size = 'md', 
  color = 'default',
  label 
}: TypingDotsProps) => {
  return (
    <div className={`${styles.container} ${styles[size]} ${color !== 'default' ? styles[color] : ''}`}>
      <span className={styles.dot} />
      <span className={styles.dot} />
      <span className={styles.dot} />
      {label && <span style={{ marginLeft: '8px', fontSize: '12px', color: 'var(--color-muted)' }}>
        {label}
      </span>}
    </div>
  );
};

export default TypingDots;