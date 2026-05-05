import React, { useState } from 'react';
import { C } from '../../constants/colors';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';

function AdminView({ onNav }: { onNav: (view: string) => void }) {
  const [activeTab, setActiveTab] = useState('users');

  const users = [
    { id: 1, name: 'Dr. Sarah Johnson', email: 'sarah.johnson@hospital.com', role: 'Doctor', status: 'active', lastLogin: '2024-05-05 09:30' },
    { id: 2, name: 'Mike Chen', email: 'mike.chen@hospital.com', role: 'Nurse', status: 'active', lastLogin: '2024-05-05 08:45' },
    { id: 3, name: 'Dr. Robert Brown', email: 'robert.brown@hospital.com', role: 'Doctor', status: 'inactive', lastLogin: '2024-05-03 14:20' },
    { id: 4, name: 'Lisa Martinez', email: 'lisa.martinez@hospital.com', role: 'Admin', status: 'active', lastLogin: '2024-05-05 10:15' }
  ];

  const systemStats = [
    { label: 'Total Users', value: '247', change: '+12', trend: 'up' },
    { label: 'Active Sessions', value: '89', change: '+5', trend: 'up' },
    { label: 'System Load', value: '42%', change: '-3%', trend: 'down' },
    { label: 'Error Rate', value: '0.2%', change: '-0.1%', trend: 'down' }
  ];

  const auditLogs = [
    { id: 1, user: 'Dr. Sarah Johnson', action: 'Updated patient record', timestamp: '2024-05-05 10:30', status: 'success' },
    { id: 2, user: 'Mike Chen', action: 'Scheduled appointment', timestamp: '2024-05-05 10:25', status: 'success' },
    { id: 3, user: 'Dr. Robert Brown', action: 'Accessed restricted data', timestamp: '2024-05-05 10:20', status: 'warning' },
    { id: 4, user: 'Lisa Martinez', action: 'Modified user permissions', timestamp: '2024-05-05 10:15', status: 'success' }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
      case 'success':
      case 'up': return C.green;
      case 'inactive': return C.muted;
      case 'warning': return C.amber;
      case 'down': return C.red;
      default: return C.text;
    }
  };

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '16px 12px 40px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 800, color: C.text }}>Admin Dashboard</h1>
        <Button onClick={() => onNav('home')} variant="outline">Back to Home</Button>
      </div>

      {/* System Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        {systemStats.map((stat, index) => (
          <Card key={index} style={{ padding: 16 }}>
            <div style={{ fontSize: 24, fontWeight: 700, color: C.text }}>{stat.value}</div>
            <div style={{ fontSize: 12, color: C.muted, marginBottom: 4 }}>{stat.label}</div>
            <div style={{ fontSize: 12, color: getStatusColor(stat.trend) }}>
              {stat.change} from last hour
            </div>
          </Card>
        ))}
      </div>

      {/* Tab Navigation */}
      <div style={{ display: 'flex', borderBottom: `1px solid ${C.border}`, marginBottom: 24 }}>
        {[
          { id: 'users', label: 'User Management' },
          { id: 'system', label: 'System Health' },
          { id: 'logs', label: 'Audit Logs' },
          { id: 'settings', label: 'Settings' }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: '12px 24px',
              border: 'none',
              background: 'none',
              fontSize: 14,
              fontWeight: 600,
              color: activeTab === tab.id ? C.primary : C.muted,
              borderBottom: activeTab === tab.id ? `2px solid ${C.primary}` : 'none',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div>
        {activeTab === 'users' && (
          <Card style={{ padding: 24 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
              <h2 style={{ fontSize: 18, fontWeight: 700, color: C.text }}>User Management</h2>
              <Button size="sm">Add New User</Button>
            </div>
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ borderBottom: `1px solid ${C.border}` }}>
                    <th style={{ textAlign: 'left', padding: '12px', fontSize: 14, fontWeight: 600, color: C.text }}>Name</th>
                    <th style={{ textAlign: 'left', padding: '12px', fontSize: 14, fontWeight: 600, color: C.text }}>Email</th>
                    <th style={{ textAlign: 'left', padding: '12px', fontSize: 14, fontWeight: 600, color: C.text }}>Role</th>
                    <th style={{ textAlign: 'left', padding: '12px', fontSize: 14, fontWeight: 600, color: C.text }}>Status</th>
                    <th style={{ textAlign: 'left', padding: '12px', fontSize: 14, fontWeight: 600, color: C.text }}>Last Login</th>
                    <th style={{ textAlign: 'left', padding: '12px', fontSize: 14, fontWeight: 600, color: C.text }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map(user => (
                    <tr key={user.id} style={{ borderBottom: `1px solid ${C.border}` }}>
                      <td style={{ padding: '12px', fontSize: 14, color: C.text }}>{user.name}</td>
                      <td style={{ padding: '12px', fontSize: 14, color: C.muted }}>{user.email}</td>
                      <td style={{ padding: '12px', fontSize: 14, color: C.text }}>{user.role}</td>
                      <td style={{ padding: '12px' }}>
                        <span style={{
                          padding: '4px 8px',
                          borderRadius: 12,
                          fontSize: 12,
                          fontWeight: 500,
                          backgroundColor: user.status === 'active' ? '#e8f5e8' : '#f8f9fa',
                          color: getStatusColor(user.status)
                        }}>
                          {user.status}
                        </span>
                      </td>
                      <td style={{ padding: '12px', fontSize: 12, color: C.muted }}>{user.lastLogin}</td>
                      <td style={{ padding: '12px' }}>
                        <div style={{ display: 'flex', gap: 8 }}>
                          <Button size="sm" variant="outline">Edit</Button>
                          <Button size="sm" variant="outline">Disable</Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        )}

        {activeTab === 'system' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
            <Card style={{ padding: 24 }}>
              <h3 style={{ fontSize: 16, fontWeight: 600, color: C.text, marginBottom: 16 }}>System Performance</h3>
              <div style={{ marginBottom: 16 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                  <span style={{ fontSize: 14, color: C.text }}>CPU Usage</span>
                  <span style={{ fontSize: 14, color: C.text }}>42%</span>
                </div>
                <div style={{ width: '100%', height: 8, backgroundColor: C.border, borderRadius: 4 }}>
                  <div style={{ width: '42%', height: '100%', backgroundColor: C.primary, borderRadius: 4 }}></div>
                </div>
              </div>
              <div style={{ marginBottom: 16 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                  <span style={{ fontSize: 14, color: C.text }}>Memory Usage</span>
                  <span style={{ fontSize: 14, color: C.text }}>68%</span>
                </div>
                <div style={{ width: '100%', height: 8, backgroundColor: C.border, borderRadius: 4 }}>
                  <div style={{ width: '68%', height: '100%', backgroundColor: C.warning, borderRadius: 4 }}></div>
                </div>
              </div>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                  <span style={{ fontSize: 14, color: C.text }}>Disk Usage</span>
                  <span style={{ fontSize: 14, color: C.text }}>35%</span>
                </div>
                <div style={{ width: '100%', height: 8, backgroundColor: C.border, borderRadius: 4 }}>
                  <div style={{ width: '35%', height: '100%', backgroundColor: C.success, borderRadius: 4 }}></div>
                </div>
              </div>
            </Card>
            <Card style={{ padding: 24 }}>
              <h3 style={{ fontSize: 16, fontWeight: 600, color: C.text, marginBottom: 16 }}>Database Status</h3>
              <div style={{ marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: 14, color: C.text }}>Connection Status</span>
                  <span style={{ fontSize: 14, color: C.success }}>Connected</span>
                </div>
              </div>
              <div style={{ marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: 14, color: C.text }}>Response Time</span>
                  <span style={{ fontSize: 14, color: C.text }}>45ms</span>
                </div>
              </div>
              <div style={{ marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: 14, color: C.text }}>Active Queries</span>
                  <span style={{ fontSize: 14, color: C.text }}>12</span>
                </div>
              </div>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: 14, color: C.text }}>Backup Status</span>
                  <span style={{ fontSize: 14, color: C.success }}>Current</span>
                </div>
              </div>
            </Card>
          </div>
        )}

        {activeTab === 'logs' && (
          <Card style={{ padding: 24 }}>
            <h3 style={{ fontSize: 16, fontWeight: 600, color: C.text, marginBottom: 16 }}>Recent Audit Logs</h3>
            {auditLogs.map(log => (
              <div key={log.id} style={{ padding: 12, marginBottom: 8, backgroundColor: '#f8f9fa', borderRadius: 6 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: 14, fontWeight: 500, color: C.text }}>{log.action}</div>
                    <div style={{ fontSize: 12, color: C.muted }}>{log.user}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: 12, color: C.muted }}>{log.timestamp}</div>
                    <span style={{
                      padding: '2px 8px',
                      borderRadius: 10,
                      fontSize: 11,
                      fontWeight: 500,
                      backgroundColor: log.status === 'success' ? '#e8f5e8' : '#fff3cd',
                      color: getStatusColor(log.status)
                    }}>
                      {log.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </Card>
        )}

        {activeTab === 'settings' && (
          <Card style={{ padding: 24 }}>
            <h3 style={{ fontSize: 16, fontWeight: 600, color: C.text, marginBottom: 16 }}>System Settings</h3>
            <div style={{ marginBottom: 20 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 500, color: C.text }}>Maintenance Mode</div>
                  <div style={{ fontSize: 12, color: C.muted }}>Enable system maintenance mode</div>
                </div>
                <label style={{ position: 'relative', display: 'inline-block', width: 48, height: 24 }}>
                  <input type="checkbox" style={{ opacity: 0, width: 0, height: 0 }} />
                  <span style={{
                    position: 'absolute',
                    cursor: 'pointer',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    backgroundColor: C.border,
                    transition: '.4s',
                    borderRadius: 24
                  }}></span>
                </label>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 500, color: C.text }}>Audit Logging</div>
                  <div style={{ fontSize: 12, color: C.muted }}>Enable detailed audit logging</div>
                </div>
                <label style={{ position: 'relative', display: 'inline-block', width: 48, height: 24 }}>
                  <input type="checkbox" defaultChecked style={{ opacity: 0, width: 0, height: 0 }} />
                  <span style={{
                    position: 'absolute',
                    cursor: 'pointer',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    backgroundColor: C.primary,
                    transition: '.4s',
                    borderRadius: 24
                  }}></span>
                </label>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 500, color: C.text }}>Auto Backup</div>
                  <div style={{ fontSize: 12, color: C.muted }}>Enable automatic daily backups</div>
                </div>
                <label style={{ position: 'relative', display: 'inline-block', width: 48, height: 24 }}>
                  <input type="checkbox" defaultChecked style={{ opacity: 0, width: 0, height: 0 }} />
                  <span style={{
                    position: 'absolute',
                    cursor: 'pointer',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    backgroundColor: C.primary,
                    transition: '.4s',
                    borderRadius: 24
                  }}></span>
                </label>
              </div>
            </div>
            <div style={{ display: 'flex', gap: 12 }}>
              <Button>Save Settings</Button>
              <Button variant="outline">Reset to Default</Button>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}

export default AdminView;