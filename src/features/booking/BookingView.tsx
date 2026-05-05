import React, { useState } from 'react';
import { C } from '../../constants/colors';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';
import { appointmentsApi, ApiError } from '../../services/api';
import { sanitizeInput } from '../../utils/inputSanitizer';

interface Doctor {
  id: string;
  name: string;
  title?: string;
  init: string;
  color: string;
  specialty: string;
  fee?: number;
  slots?: string[];
}

interface BookingFormData {
  date: string;
  time: string;
  reason: string;
  patientName: string;
  patientPhone: string;
}

function BookingView({ doctor, onNav }: { doctor: Doctor | null, onNav: (view: string) => void }) {
  const [form, setForm] = useState<BookingFormData>({
    date: '',
    time: '',
    reason: '',
    patientName: '',
    patientPhone: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!doctor) return;
    
    setLoading(true);
    setError(null);
    
    try {
      // Sanitize user inputs
      const sanitizedData = {
        date: form.date,
        time: form.time,
        reason: sanitizeInput(form.reason),
        patientName: sanitizeInput(form.patientName),
        patientPhone: form.patientPhone.replace(/\D/g, '') // Only digits for phone
      };
      
      // Call backend API to create appointment
      await appointmentsApi.create({
        doctorId: doctor.id,
        date: sanitizedData.date,
        time: sanitizedData.time,
        patientName: sanitizedData.patientName,
        patientPhone: sanitizedData.patientPhone
      });
      
      setSuccess(true);
    } catch (e) {
      const errorMessage = e instanceof ApiError 
        ? e.message 
        : 'Failed to book appointment. Please try again.';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field: keyof BookingFormData, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };

  if (!doctor) {
    return (
      <div style={{ maxWidth: 600, margin: '0 auto', padding: '16px 12px 40px', textAlign: 'center' }}>
        <Card style={{ padding: 24 }}>
          <div style={{ fontSize: 16, color: C.muted, marginBottom: 16 }}>
            No doctor selected. Please select a doctor to book an appointment.
          </div>
          <Button onClick={() => onNav('doctors')}>
            Browse Doctors
          </Button>
        </Card>
      </div>
    );
  }

  if (success) {
    return (
      <div style={{ maxWidth: 600, margin: '0 auto', padding: '16px 12px 40px', textAlign: 'center' }}>
        <Card style={{ padding: 24 }}>
          <div style={{ 
            width: 60, 
            height: 60, 
            borderRadius: '50%', 
            backgroundColor: C.green,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 16px'
          }}>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
          <h2 style={{ fontSize: 20, fontWeight: 700, color: C.text, marginBottom: 8 }}>
            Appointment Booked!
          </h2>
          <p style={{ fontSize: 14, color: C.muted, marginBottom: 24 }}>
            Your appointment has been confirmed. You will receive an SMS confirmation shortly.
          </p>
          <div style={{ display: 'flex', gap: 12, justifyContent: 'center' }}>
            <Button onClick={() => onNav('portal')} variant="outline">
              View My Appointments
            </Button>
            <Button onClick={() => onNav('home')}>
              Back to Home
            </Button>
          </div>
        </Card>
      </div>
    );
  }

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
            {doctor.fee && (
              <div style={{ fontSize: 14, color: C.primary, fontWeight: 600, marginTop: 4 }}>
                ৳{doctor.fee} consultation fee
              </div>
            )}
          </div>
        </div>
      </Card>

      {error && (
        <Card style={{ padding: 16, marginBottom: 16, backgroundColor: C.redLight, borderColor: C.red }}>
          <div style={{ fontSize: 14, color: C.red }}>
            Error: {error}
          </div>
        </Card>
      )}

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
              min={new Date().toISOString().split('T')[0]}
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
              {doctor.slots?.map((slot) => (
                <option key={slot} value={slot}>{slot}</option>
              ))}
              {!doctor.slots && (
                <>
                  <option value="09:00">9:00 AM</option>
                  <option value="10:00">10:00 AM</option>
                  <option value="11:00">11:00 AM</option>
                  <option value="14:00">2:00 PM</option>
                  <option value="15:00">3:00 PM</option>
                  <option value="16:00">4:00 PM</option>
                </>
              )}
            </select>
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: 14, fontWeight: 600, color: C.text, marginBottom: 8 }}>
              Patient Name
            </label>
            <input
              type="text"
              value={form.patientName}
              onChange={(e) => handleChange('patientName', e.target.value)}
              placeholder="Your full name"
              required
              style={{
                width: '100%',
                padding: '12px 16px',
                border: `1px solid ${C.border}`,
                borderRadius: 8,
                fontSize: 14,
                outline: 'none'
              }}
            />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: 14, fontWeight: 600, color: C.text, marginBottom: 8 }}>
              Phone Number
            </label>
            <input
              type="tel"
              value={form.patientPhone}
              onChange={(e) => handleChange('patientPhone', e.target.value)}
              placeholder="01XXXXXXXXX"
              required
              pattern="01[3-9]\d{9}"
              style={{
                width: '100%',
                padding: '12px 16px',
                border: `1px solid ${C.border}`,
                borderRadius: 8,
                fontSize: 14,
                outline: 'none'
              }}
            />
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
              disabled={loading}
            >
              Cancel
            </Button>
            <Button 
              type="submit" 
              style={{ flex: 1 }}
              disabled={loading}
            >
              {loading ? 'Booking...' : 'Book Appointment'}
            </Button>
          </div>
        </Card>
      </form>
    </div>
  );
}

export default BookingView;
