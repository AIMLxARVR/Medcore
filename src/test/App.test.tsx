import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';
import { DOCTORS } from '../constants/data';

// Mock the anthropic service
vi.mock('../services/anthropic', () => ({
  callClaude: vi.fn().mockResolvedValue({
    content: 'This is a test response from the AI assistant.',
  }),
}));

describe('MedCore App Integration Tests', () => {
  it('renders the home view by default', () => {
    render(<App />);
    expect(screen.getByText('MedCore AI')).toBeInTheDocument();
    expect(screen.getByText('Your AI-powered medical assistant')).toBeInTheDocument();
  });

  it('navigates between different views', () => {
    render(<App />);
    
    // Navigate to Doctors view
    const doctorsButton = screen.getByText('Find Doctors');
    fireEvent.click(doctorsButton);
    expect(screen.getByText('Our Doctors')).toBeInTheDocument();
    
    // Navigate to Chatbot view
    const chatbotButton = screen.getByText('AI Chatbot');
    fireEvent.click(chatbotButton);
    expect(screen.getByText('MedCore AI Assistant')).toBeInTheDocument();
  });

  it('displays doctor information correctly', () => {
    render(<App />);
    
    // Navigate to Doctors view
    const doctorsButton = screen.getByText('Find Doctors');
    fireEvent.click(doctorsButton);
    
    // Check if doctor information is displayed
    expect(screen.getByText('Dr. Sarah Johnson')).toBeInTheDocument();
    expect(screen.getByText('Cardiology')).toBeInTheDocument();
    expect(screen.getByText('Internal Medicine')).toBeInTheDocument();
  });

  it('handles doctor booking flow', () => {
    render(<App />);
    
    // Navigate to Doctors view
    const doctorsButton = screen.getByText('Find Doctors');
    fireEvent.click(doctorsButton);
    
    // Click on Book Now for first doctor
    const bookButtons = screen.getAllByText('Book Now');
    fireEvent.click(bookButtons[0]);
    
    // Should navigate to booking view
    expect(screen.getByText('Book Appointment')).toBeInTheDocument();
  });

  it('chatbot interaction works correctly', async () => {
    render(<App />);
    
    // Navigate to Chatbot view
    const chatbotButton = screen.getByText('AI Chatbot');
    fireEvent.click(chatbotButton);
    
    // Find input field and send button
    const input = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByText('Send');
    
    // Type and send message
    fireEvent.change(input, { target: { value: 'I have a headache' } });
    fireEvent.click(sendButton);
    
    // Wait for AI response
    await waitFor(() => {
      expect(screen.getByText('This is a test response from the AI assistant.')).toBeInTheDocument();
    });
  });

  it('patient portal displays correct information', () => {
    render(<App />);
    
    // Navigate to Patient Portal
    const portalButton = screen.getByText('Patient Portal');
    fireEvent.click(portalButton);
    
    // Check portal statistics
    expect(screen.getByText('3')).toBeInTheDocument(); // Upcoming Appointments
    expect(screen.getByText('12')).toBeInTheDocument(); // Medical Records
    expect(screen.getByText('2')).toBeInTheDocument(); // Active Prescriptions
  });

  it('AI clinical assistant provides analysis', async () => {
    render(<App />);
    
    // Navigate to AI Clinical view
    const aiClinicalButton = screen.getByText('AI Clinical Assistant');
    fireEvent.click(aiClinicalButton);
    
    // Enter symptoms
    const textarea = screen.getByPlaceholderText('Please describe your symptoms in detail...');
    fireEvent.change(textarea, { target: { value: 'I have a fever and cough' } });
    
    // Click analyze button
    const analyzeButton = screen.getByText('Analyze Symptoms');
    fireEvent.click(analyzeButton);
    
    // Should show analysis results
    await waitFor(() => {
      expect(screen.getByText('Urgency Level:')).toBeInTheDocument();
    });
  });

  it('admin dashboard displays system information', () => {
    render(<App />);
    
    // Navigate to Admin view
    const adminButton = screen.getByText('Admin Dashboard');
    fireEvent.click(adminButton);
    
    // Check admin statistics
    expect(screen.getByText('247')).toBeInTheDocument(); // Total Users
    expect(screen.getByText('89')).toBeInTheDocument(); // Active Sessions
    expect(screen.getByText('42%')).toBeInTheDocument(); // System Load
  });

  it('ETL dashboard shows job management', () => {
    render(<App />);
    
    // Navigate to ETL view
    const etlButton = screen.getByText('Data Management');
    fireEvent.click(etlButton);
    
    // Check ETL jobs
    expect(screen.getByText('Patient Data Sync')).toBeInTheDocument();
    expect(screen.getByText('Appointment Import')).toBeInTheDocument();
    expect(screen.getByText('Lab Results Export')).toBeInTheDocument();
  });
});