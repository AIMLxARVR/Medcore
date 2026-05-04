import React, { useState } from 'react';
import { C } from '../../constants/colors';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';

function EtlView({ onNav }: { onNav: (view: string) => void }) {
  const [activeJob, setActiveJob] = useState(null);
  const [jobs, setJobs] = useState([
    { 
      id: 1, 
      name: 'Patient Data Sync', 
      status: 'running', 
      progress: 65, 
      lastRun: '2024-05-05 10:30',
      records: 15420,
      errors: 3
    },
    { 
      id: 2, 
      name: 'Appointment Import', 
      status: 'completed', 
      progress: 100, 
      lastRun: '2024-05-05 09:15',
      records: 892,
      errors: 0
    },
    { 
      id: 3, 
      name: 'Lab Results Export', 
      status: 'failed', 
      progress: 25, 
      lastRun: '2024-05-05 08:45',
      records: 0,
      errors: 1
    },
    { 
      id: 4, 
      name: 'Insurance Data Update', 
      status: 'pending', 
      progress: 0, 
      lastRun: '2024-05-04 16:20',
      records: 0,
      errors: 0
    }
  ]);

  const handleStartJob = (jobId: number) => {
    setJobs(jobs.map(job => 
      job.id === jobId 
        ? { ...job, status: 'running', progress: 0 }
        : job
    ));
    
    // Simulate job progress
    const interval = setInterval(() => {
      setJobs(prevJobs => prevJobs.map(job => {
        if (job.id === jobId && job.status === 'running') {
          const newProgress = Math.min(job.progress + Math.random() * 15, 100);
          return {
            ...job,
            progress: newProgress,
            status: newProgress >= 100 ? 'completed' : 'running'
          };
        }
        return job;
      }));
    }, 1000);

    setTimeout(() => clearInterval(interval), 10000);
  };

  const handleStopJob = (jobId: number) => {
    setJobs(jobs.map(job => 
      job.id === jobId 
        ? { ...job, status: 'stopped', progress: Math.max(job.progress - 10, 0) }
        : job
    ));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return C.primary;
      case 'completed': return C.success;
      case 'failed': return C.danger;
      case 'stopped': return C.warning;
      case 'pending': return C.muted;
      default: return C.text;
    }
  };

  const getStatusBgColor = (status: string) => {
    switch (status) {
      case 'running': return '#e3f2fd';
      case 'completed': return '#e8f5e8';
      case 'failed': return '#fce8e6';
      case 'stopped': return '#fff3cd';
      case 'pending': return '#f8f9fa';
      default: return 'white';
    }
  };

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '16px 12px 40px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 800, color: C.text }}>ETL Data Management</h1>
        <Button onClick={() => onNav('home')} variant="outline">Back to Home</Button>
      </div>

      {/* Summary Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
        <Card style={{ padding: 16 }}>
          <div style={{ fontSize: 24, fontWeight: 700, color: C.primary }}>4</div>
          <div style={{ fontSize: 12, color: C.muted }}>Total Jobs</div>
        </Card>
        <Card style={{ padding: 16 }}>
          <div style={{ fontSize: 24, fontWeight: 700, color: C.success }}>1</div>
          <div style={{ fontSize: 12, color: C.muted }}>Completed</div>
        </Card>
        <Card style={{ padding: 16 }}>
          <div style={{ fontSize: 24, fontWeight: 700, color: C.warning }}>1</div>
          <div style={{ fontSize: 12, color: C.muted }}>Running</div>
        </Card>
        <Card style={{ padding: 16 }}>
          <div style={{ fontSize: 24, fontWeight: 700, color: C.danger }}>1</div>
          <div style={{ fontSize: 12, color: C.muted }}>Failed</div>
        </Card>
      </div>

      {/* Jobs List */}
      <Card style={{ padding: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <h2 style={{ fontSize: 18, fontWeight: 700, color: C.text }}>ETL Jobs</h2>
          <Button size="sm">Add New Job</Button>
        </div>

        {jobs.map(job => (
          <div key={job.id} style={{ marginBottom: 16, padding: 16, border: `1px solid ${C.border}`, borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
              <div>
                <div style={{ fontSize: 16, fontWeight: 600, color: C.text }}>{job.name}</div>
                <div style={{ fontSize: 12, color: C.muted }}>Last run: {job.lastRun}</div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <div style={{ 
                  padding: '4px 12px', 
                  borderRadius: 12, 
                  fontSize: 12, 
                  fontWeight: 500,
                  backgroundColor: getStatusBgColor(job.status),
                  color: getStatusColor(job.status),
                  border: `1px solid ${getStatusColor(job.status)}`
                }}>
                  {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
                </div>
                <div style={{ fontSize: 12, color: C.muted }}>
                  {job.records} records
                </div>
                {job.errors > 0 && (
                  <div style={{ fontSize: 12, color: C.danger }}>
                    {job.errors} errors
                  </div>
                )}
              </div>
            </div>

            {/* Progress Bar */}
            <div style={{ marginBottom: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                <span style={{ fontSize: 12, color: C.muted }}>Progress</span>
                <span style={{ fontSize: 12, color: C.muted }}>{Math.round(job.progress)}%</span>
              </div>
              <div style={{ 
                width: '100%', 
                height: 8, 
                backgroundColor: C.border, 
                borderRadius: 4,
                overflow: 'hidden'
              }}>
                <div style={{ 
                  width: `${job.progress}%`, 
                  height: '100%', 
                  backgroundColor: getStatusColor(job.status),
                  transition: 'width 0.3s ease'
                }}></div>
              </div>
            </div>

            {/* Action Buttons */}
            <div style={{ display: 'flex', gap: 8 }}>
              {job.status === 'pending' && (
                <Button size="sm" onClick={() => handleStartJob(job.id)}>Start</Button>
              )}
              {job.status === 'running' && (
                <Button size="sm" variant="outline" onClick={() => handleStopJob(job.id)}>Stop</Button>
              )}
              {(job.status === 'completed' || job.status === 'failed' || job.status === 'stopped') && (
                <Button size="sm" variant="outline" onClick={() => handleStartJob(job.id)}>Restart</Button>
              )}
              <Button size="sm" variant="outline">View Logs</Button>
              <Button size="sm" variant="outline">Edit</Button>
            </div>
          </div>
        ))}
      </Card>

      {/* Data Quality Metrics */}
      <Card style={{ padding: 24, marginTop: 24 }}>
        <h3 style={{ fontSize: 16, fontWeight: 600, color: C.text, marginBottom: 16 }}>Data Quality Metrics</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 20, fontWeight: 600, color: C.success }}>98.5%</div>
            <div style={{ fontSize: 12, color: C.muted }}>Data Accuracy</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 20, fontWeight: 600, color: C.primary }}>99.2%</div>
            <div style={{ fontSize: 12, color: C.muted }}>Completeness</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 20, fontWeight: 600, color: C.warning }}>12</div>
            <div style={{ fontSize: 12, color: C.muted }}>Data Issues</div>
          </div>
        </div>
      </Card>
    </div>
  );
}

export default EtlView;