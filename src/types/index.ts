// Common Types

// User Roles for RBAC
export type UserRole = 'PATIENT' | 'DOCTOR' | 'ADMIN' | 'STAFF';

// Permission types for ABAC
export type Permission = 
  | 'view_patients' 
  | 'manage_patients'
  | 'view_doctors'
  | 'manage_doctors'
  | 'view_appointments'
  | 'manage_appointments'
  | 'view_inventory'
  | 'manage_inventory'
  | 'view_reviews'
  | 'manage_reviews'
  | 'view_audit_logs'
  | 'manage_users'
  | 'view_reports'
  | 'manage_system';

// Role-Permission mapping
export const ROLE_PERMISSIONS: Record<UserRole, Permission[]> = {
  PATIENT: ['view_doctors', 'view_appointments', 'view_reviews'],
  DOCTOR: ['view_patients', 'view_appointments', 'view_reviews'],
  STAFF: ['view_patients', 'view_doctors', 'view_appointments', 'view_inventory', 'view_reviews', 'manage_inventory'],
  ADMIN: ['view_patients', 'manage_patients', 'view_doctors', 'manage_doctors', 'view_appointments', 'manage_appointments', 'view_inventory', 'manage_inventory', 'view_reviews', 'manage_reviews', 'view_audit_logs', 'manage_users', 'view_reports', 'manage_system'],
};

export type ViewType = 
  | 'home' 
  | 'chatbot' 
  | 'doctors' 
  | 'booking' 
  | 'portal' 
  | 'patient-portal'
  | 'doctor-dashboard'
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

// Inventory/Pharmacy types
export interface InventoryItem {
  id: string;
  name: string;
  category: string;
  sku: string;
  quantity: number;
  minQuantity: number;
  unit: string;
  price: number;
  expiryDate?: string;
  supplier: string;
  status: 'in_stock' | 'low_stock' | 'out_of_stock' | 'expired';
}

export interface InventoryCategory {
  id: string;
  name: string;
  itemCount: number;
}

// Review/Rating types
export interface Review {
  id: string;
  patientId: string;
  patientName: string;
  doctorId: string;
  doctorName: string;
  rating: number;
  comment: string;
  date: string;
  status: 'published' | 'pending' | 'flagged';
}

export interface ReviewStats {
  averageRating: number;
  totalReviews: number;
  fiveStar: number;
  fourStar: number;
  threeStar: number;
  twoStar: number;
  oneStar: number;
}

// User Account types for management
export interface UserAccount {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: UserRole;
  phone?: string;
  isActive: boolean;
  createdAt: string;
  lastLogin?: string;
}
