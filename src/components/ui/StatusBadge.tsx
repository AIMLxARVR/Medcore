import React from 'react';
import styles from './StatusBadge.module.css';

type StatusType = 
  | 'connected' 
  | 'disconnected' 
  | 'pending' 
  | 'success' 
  | 'warning' 
  | 'error' 
  | 'confirmed' 
  | 'completed' 
  | 'cancelled' 
  | 'syncing';

interface StatusBadgeProps {
  status: StatusType | string;
  showIndicator?: boolean;
}

const statusConfig: Record<StatusType, { label: string; className: string }> = {
  connected: { label: 'Connected', className: styles.connected },
  disconnected: { label: 'Disconnected', className: styles.disconnected },
  pending: { label: 'Pending', className: styles.pending },
  success: { label: 'Success', className: styles.success },
  warning: { label: 'Warning', className: styles.warning },
  error: { label: 'Error', className: styles.error },
  confirmed: { label: 'Confirmed', className: styles.confirmed },
  completed: { label: 'Completed', className: styles.completed },
  cancelled: { label: 'Cancelled', className: styles.cancelled },
  syncing: { label: 'Syncing', className: styles.syncing },
};

const StatusBadge = ({ status, showIndicator = true }: StatusBadgeProps) => {
  const statusKey = status as StatusType;
  const config = statusConfig[statusKey] || statusConfig.pending;

  return (
    <div className={`${styles.statusBadge} ${config.className}`}>
      {showIndicator && <span className={styles.statusIndicator} />}
      <span>{config.label}</span>
    </div>
  );
};

export default StatusBadge;