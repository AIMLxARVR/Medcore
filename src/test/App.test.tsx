import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';
import { DOCTORS } from '../constants/data';

// Mock the anthropic service
vi.mock('../services/anthropic', () => ({
  callClaude: vi.fn().mockResolvedValue({
    replyText: 'This is a test response from the AI assistant.',
    updatedHistory: [],
  }),
}));

describe('MedCore App Integration Tests', () => {
  it('renders the home view by default', () => {
    render(<App />);
    expect(screen.getByText('MedCore')).toBeInTheDocument();
    expect(screen.getByText('Intelligent Healthcare Management')).toBeInTheDocument();
  });

  it('navigates between different views', () => {
    render(<App />);
    
    // Should start on home view
    expect(screen.getByText('DHAKA MEDICARE — AI-ENHANCED MVP')).toBeInTheDocument();
    
    // Navigate to Doctors view
    const doctorsButton = screen.getByText('Doctors');
    fireEvent.click(doctorsButton);
    expect(screen.getByText('Our Doctors')).toBeInTheDocument();
  });

  it('displays doctor information correctly', () => {
    render(<App />);
    
    // Navigate to Doctors view
    const doctorsButton = screen.getByText('Doctors');
    fireEvent.click(doctorsButton);
    
    // Check if doctor information is displayed
    expect(screen.getByText((content, element) => {
      return element?.textContent === 'Dr. Fatima Rahman';
    })).toBeInTheDocument();
    expect(screen.getByText((content, element) => {
      return element?.textContent === 'Dr. Ahmed Hossain';
    })).toBeInTheDocument();
    expect(screen.getByText((content, element) => {
      return element?.textContent === 'Dr. Nasrin Khatun';
    })).toBeInTheDocument();
  });

  it('handles doctor booking flow', async () => {
    render(<App />);
    
    // Navigate to Doctors view
    const doctorsButton = screen.getByText('Doctors');
    fireEvent.click(doctorsButton);
    
    // Click on a doctor's Book Now button (use getAllByText and click the first one)
    const bookNowButtons = screen.getAllByText('Book Now');
    fireEvent.click(bookNowButtons[0]);
    
    // Should navigate to booking view (check for booking-related content)
    expect(screen.getByText((content, element) => {
      return element?.textContent === 'Book Appointment';
    })).toBeInTheDocument();
  });

  it('chatbot interaction works correctly', async () => {
    render(<App />);
    
    // Navigate to Chatbot view - get the first one (navigation button)
    const chatbotButton = screen.getAllByText('AI Chatbot')[0];
    fireEvent.click(chatbotButton);
    
    // Find input field and send button
    const input = screen.getByPlaceholderText('Ask MedBot...');
    const sendButton = screen.getAllByRole('button').find(btn => btn.querySelector('svg'));
    
    // Type and send message
    fireEvent.change(input, { target: { value: 'I have a headache' } });
    fireEvent.click(sendButton);
    
    // Wait for AI response
    await waitFor(() => {
      expect(screen.getByText((content, element) => {
        return element?.textContent === 'This is a test response from the AI assistant.';
      })).toBeInTheDocument();
    });
  });

  it('patient portal displays correct information', () => {
    render(<App />);
    
    // Navigate to Patient Portal
    const portalButton = screen.getByText('My Portal');
    fireEvent.click(portalButton);
    
    // Check portal statistics
    expect(screen.getByText((content, element) => {
      return element?.textContent === '3';
    })).toBeInTheDocument(); // Upcoming Appointments
    expect(screen.getByText((content, element) => {
      return element?.textContent === '12';
    })).toBeInTheDocument(); // Medical Records
    expect(screen.getByText((content, element) => {
      return element?.textContent === '2';
    })).toBeInTheDocument(); // Active Prescriptions
  });

  it('AI clinical assistant provides analysis', async () => {
    render(<App />);
    
    // Navigate to AI Clinical view
    const aiClinicalButton = screen.getByText('AI Clinical');
    fireEvent.click(aiClinicalButton);
    
    // Enter symptoms - use partial placeholder text since it's multi-line
    const textarea = screen.getByPlaceholderText(/Please describe your symptoms in detail/);
    fireEvent.change(textarea, { target: { value: 'I have a fever and cough' } });
    
    // Click analyze button
    const analyzeButton = screen.getByText('Analyze Symptoms');
    fireEvent.click(analyzeButton);
    
    // Should show analysis results with longer timeout and better selector
    await waitFor(() => {
      // Look for the urgency level text directly
      const urgencyLevel = screen.getByText(/Urgency Level:/i);
      expect(urgencyLevel).toBeInTheDocument();

      // Also verify other key elements are present
      expect(screen.getByText(/Possible Conditions/i)).toBeInTheDocument();
      expect(screen.getByText(/Recommendations/i)).toBeInTheDocument();
    }, { timeout: 5000 });
  });

  it('admin dashboard displays system information', () => {
    render(<App />);
    
    // Navigate to Admin view
    const adminButton = screen.getByText('Admin');
    fireEvent.click(adminButton);
    
    // Check admin statistics - these are in the systemStats array
    expect(screen.getByText((content, element) => {
      return element?.textContent === '247';
    })).toBeInTheDocument(); // Total Users
    expect(screen.getByText((content, element) => {
      return element?.textContent === '89';
    })).toBeInTheDocument(); // Active Sessions
    expect(screen.getByText((content, element) => {
      return element?.textContent === '42%';
    })).toBeInTheDocument(); // System Load
    expect(screen.getByText((content, element) => {
      return element?.textContent === '0.2%';
    })).toBeInTheDocument(); // Error Rate
  });

  it('ETL dashboard shows job management', () => {
    render(<App />);
    
    // Navigate to ETL view
    const etlButton = screen.getAllByText('ETL Hub')[0]; // Get the first ETL Hub button (navigation)
    fireEvent.click(etlButton);
    
    // Check ETL jobs
    expect(screen.getByText('Patient Data Sync')).toBeInTheDocument();
    expect(screen.getByText('Appointment Import')).toBeInTheDocument();
    expect(screen.getByText('Lab Results Export')).toBeInTheDocument();
  });
});