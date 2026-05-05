// Common Types

export type ViewType = 
  | 'home' 
  | 'chatbot' 
  | 'doctors' 
  | 'booking' 
  | 'portal' 
  | 'ai-clinical' 
  | 'etl' 
  | 'admin';

export interface Doctor {
  id: string;
  name: string;
  specialty: string;
  rating: number;
  availability: string;
  image?: string;
  location?: string;
  experience?: number;
  languages?: string[];
}

export interface Appointment {
  id: string;
  doctorId: string;
  patientName: string;
  date: string;
  time: string;
  type: string;
  status: 'confirmed' | 'pending' | 'cancelled' | 'completed';
  notes?: string;
}

export interface ChatMessage {
  id: string;
  from: 'user' | 'bot';
  text: string;
  timestamp: Date;
}

export interface PatientRecord {
  id: string;
  name: string;
  dateOfBirth: string;
  bloodType?: string;
  allergies?: string[];
  conditions?: string[];
  medications?: string[];
  lastVisit?: Date;
}

export interface MedicalReport {
  id: string;
  patientId: string;
  type: string;
  date: Date;
  results: string;
  doctorId: string;
  status: 'pending' | 'completed' | 'reviewed';
}

export interface NavigationProps {
  onNav: (view: ViewType) => void;
}

export interface StatusBadgeProps {
  status: 'connected' | 'disconnected' | 'pending' | 'success' | 'warning' | 'error' | 'confirmed' | 'completed' | 'cancelled' | 'syncing';
  showIndicator?: boolean;
}
