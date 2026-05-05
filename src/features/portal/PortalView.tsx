import React, { useState } from 'react';
import { C } from '../../constants/colors';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';

function PortalView({ onNav }: { onNav: (view: string) => void }) {
  const [activeTab, setActiveTab] = useState('records');

  const records = [
    { id: 1, date: '2024-01-15', doctor: 'Dr. Smith', type: 'Checkup', notes: 'Annual physical examination' },
    { id: 2, date: '2024-02-20', doctor: 'Dr. Johnson', type: 'Lab Results', notes: 'Blood work - all normal' },
    { id: 3, date: '2024-03-10', doctor: 'Dr. Williams', type: 'Consultation', notes: 'Follow-up on medication' }
  ];

  const upcoming = [
    { id: 1, date: '2024-05-15', time: '10:00 AM', doctor: 'Dr. Brown', type: 'Follow-up' },
    { id: 2, date: '2024-05-22', time: '2:00 PM', doctor: 'Dr. Davis', type: 'Lab Work' }
  ];

  const prescriptions = [
    { id: 1, name: 'Lisinopril', dosage: '10mg', frequency: 'Once daily', prescribed: '2024-03-01', refills: 2 },
    { id: 2, name: 'Metformin', dosage: '500mg', frequency: 'Twice daily', prescribed: '2024-02-15', refills: 1 }
  ];

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: '16px 12px 40px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h1 style={{ fontSize: 24, fontWeight: 800, color: C.text }}>Patient Portal</h1>
        <Button onClick={() => onNav('home')} variant="outline">Back to Home</Button>
      </div>

      {/* Quick Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 24 }}>
        <Card style={{ padding: 16, textAlign: 'center' }}>
          <div style={{ fontSize: 24, fontWeight: 700, color: C.primary }}>3</div>
          <div style={{ fontSize: 14, color: C.muted }}>Upcoming Appointments</div>
        </Card>
        <Card style={{ padding: 16, textAlign: 'center' }}>
          <div style={{ fontSize: 24, fontWeight: 700, color: C.green }}>12</div>
          <div style={{ fontSize: 14, color: C.muted }}>Medical Records</div>
        </Card>
        <Card style={{ padding: 16, textAlign: 'center' }}>
          <div style={{ fontSize: 24, fontWeight: 700, color: C.amber }}>2</div>
          <div style={{ fontSize: 14, color: C.muted }}>Active Prescriptions</div>
        </Card>
      </div>

      {/* Tab Navigation */}
      <div style={{ display: 'flex', borderBottom: `1px solid ${C.border}`, marginBottom: 24 }}>
        {[
          { id: 'records', label: 'Medical Records' },
          { id: 'appointments', label: 'Upcoming Appointments' },
          { id: 'prescriptions', label: 'Prescriptions' }
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
        {activeTab === 'records' && (
          <div>
            <h2 style={{ fontSize: 18, fontWeight: 700, color: C.text, marginBottom: 16 }}>Medical Records</h2>
            {records.map(record => (
              <Card key={record.id} style={{ padding: 16, marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: 16, fontWeight: 600, color: C.text }}>{record.type}</div>
                    <div style={{ fontSize: 14, color: C.muted }}>{record.doctor}</div>
                    <div style={{ fontSize: 12, color: C.muted, marginTop: 4 }}>{record.notes}</div>
                  </div>
                  <div style={{ fontSize: 14, color: C.muted }}>{record.date}</div>
                </div>
              </Card>
            ))}
          </div>
        )}

        {activeTab === 'appointments' && (
          <div>
            <h2 style={{ fontSize: 18, fontWeight: 700, color: C.text, marginBottom: 16 }}>Upcoming Appointments</h2>
            {upcoming.map(apt => (
              <Card key={apt.id} style={{ padding: 16, marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: 16, fontWeight: 600, color: C.text }}>{apt.type}</div>
                    <div style={{ fontSize: 14, color: C.muted }}>{apt.doctor}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: 14, fontWeight: 600, color: C.text }}>{apt.date}</div>
                    <div style={{ fontSize: 12, color: C.muted }}>{apt.time}</div>
                  </div>
                </div>
              </Card>
            ))}
            <Button onClick={() => onNav('doctors')} style={{ marginTop: 16 }}>
              Schedule New Appointment
            </Button>
          </div>
        )}

        {activeTab === 'prescriptions' && (
          <div>
            <h2 style={{ fontSize: 18, fontWeight: 700, color: C.text, marginBottom: 16 }}>Active Prescriptions</h2>
            {prescriptions.map(rx => (
              <Card key={rx.id} style={{ padding: 16, marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: 16, fontWeight: 600, color: C.text }}>{rx.name}</div>
                    <div style={{ fontSize: 14, color: C.muted }}>{rx.dosage} - {rx.frequency}</div>
                    <div style={{ fontSize: 12, color: C.muted, marginTop: 4 }}>
                      Prescribed: {rx.prescribed}
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: 14, fontWeight: 600, color: C.amber }}>
                      {rx.refills} refills
                    </div>
                    <Button size="sm" variant="outline" style={{ marginTop: 8 }}>
                      Request Refill
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default PortalView;