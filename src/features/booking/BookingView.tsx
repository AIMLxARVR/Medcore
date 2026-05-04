import React, { useState } from 'react';
import { C } from '../../constants/colors';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';

function BookingView({ doctor, onNav }: { doctor: any, onNav: (view: string) => void }) {
  const [form, setForm] = useState({
    date: '',
    time: '',
    reason: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle booking submission
    alert(`Appointment booked with Dr. ${doctor.name} on ${form.date} at ${form.time}`);
    onNav('doctors');
  };

  const handleChange = (field: string, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div style={{ maxWidth: 600, margin: '0 auto', padding: '16px 12px 40px' }}>
      <h1 style={{ fontSize: 20, fontWeight: 800, color: C.text, marginBottom: 16 }}>
        Book Appointment
      </h1>
      
      <Card style={{ padding: 24, marginBottom: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 16 }}>
          <div style={{ 
            width: 60, 
            height: 60, 
            borderRadius: '50%', 
            backgroundColor: doctor.color,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: 700,
            fontSize: 18
          }}>
            {doctor.init}
          </div>
          <div>
            <div style={{ fontSize: 16, fontWeight: 700, color: C.text }}>
              Dr. {doctor.name}
            </div>
            <div style={{ fontSize: 14, color: C.muted }}>{doctor.title}</div>
            <div style={{ fontSize: 12, color: C.muted, marginTop: 2 }}>
              {doctor.specialty}
            </div>
          </div>
        </div>
      </Card>

      <form onSubmit={handleSubmit}>
        <Card style={{ padding: 24 }}>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: 14, fontWeight: 600, color: C.text, marginBottom: 8 }}>
              Date
            </label>
            <input
              type="date"
              value={form.date}
              onChange={(e) => handleChange('date', e.target.value)}
              required
              style={{
                width: '100%',
                padding: '12px 16px',
                border: `1px solid ${C.border}`,
                borderRadius: 8,
                fontSize: 14,
                outline: 'none',
                transition: 'border-color 0.2s'
              }}
              onFocus={(e) => e.target.style.borderColor = C.primary}
              onBlur={(e) => e.target.style.borderColor = C.border}
            />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: 14, fontWeight: 600, color: C.text, marginBottom: 8 }}>
              Time
            </label>
            <select
              value={form.time}
              onChange={(e) => handleChange('time', e.target.value)}
              required
              style={{
                width: '100%',
                padding: '12px 16px',
                border: `1px solid ${C.border}`,
                borderRadius: 8,
                fontSize: 14,
                outline: 'none',
                backgroundColor: 'white',
                cursor: 'pointer'
              }}
            >
              <option value="">Select a time</option>
              <option value="09:00">9:00 AM</option>
              <option value="10:00">10:00 AM</option>
              <option value="11:00">11:00 AM</option>
              <option value="14:00">2:00 PM</option>
              <option value="15:00">3:00 PM</option>
              <option value="16:00">4:00 PM</option>
            </select>
          </div>

          <div style={{ marginBottom: 24 }}>
            <label style={{ display: 'block', fontSize: 14, fontWeight: 600, color: C.text, marginBottom: 8 }}>
              Reason for Visit
            </label>
            <textarea
              value={form.reason}
              onChange={(e) => handleChange('reason', e.target.value)}
              placeholder="Please describe your reason for the appointment..."
              rows={4}
              required
              style={{
                width: '100%',
                padding: '12px 16px',
                border: `1px solid ${C.border}`,
                borderRadius: 8,
                fontSize: 14,
                outline: 'none',
                resize: 'vertical',
                minHeight: 80
              }}
              onFocus={(e) => e.target.style.borderColor = C.primary}
              onBlur={(e) => e.target.style.borderColor = C.border}
            />
          </div>

          <div style={{ display: 'flex', gap: 12 }}>
            <Button 
              type="button" 
              variant="outline" 
              onClick={() => onNav('doctors')}
              style={{ flex: 1 }}
            >
              Cancel
            </Button>
            <Button 
              type="submit" 
              style={{ flex: 1 }}
            >
              Book Appointment
            </Button>
          </div>
        </Card>
      </form>
    </div>
  );
}

export default BookingView;