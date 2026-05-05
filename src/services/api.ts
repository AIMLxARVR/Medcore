/**
 * API Client Service
 * Centralized HTTP client for backend API calls
 * Handles authentication, error handling, and base URL configuration
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

// Get JWT token from localStorage
const getToken = (): string | null => {
  return localStorage.getItem('medcore_token');
};

// Set JWT token in localStorage
export const setToken = (token: string): void => {
  localStorage.setItem('medcore_token', token);
};

// Remove JWT token from localStorage
export const removeToken = (): void => {
  localStorage.removeItem('medcore_token');
};

// Get auth headers
const getAuthHeaders = (): HeadersInit => {
  const token = getToken();
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  if (token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

// API Error class
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// Generic fetch wrapper with error handling
async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config: RequestInit = {
    ...options,
    headers: {
      ...getAuthHeaders(),
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);
    
    // Handle non-JSON responses
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      if (!response.ok) {
        throw new ApiError(
          'Server error',
          response.status,
          'SERVER_ERROR'
        );
      }
      return response.json() as Promise<T>;
    }
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new ApiError(
        data.error || 'Request failed',
        response.status,
        data.code
      );
    }
    
    return data as T;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    // Network error or other issues
    throw new ApiError(
      'Network error. Please check your connection.',
      0,
      'NETWORK_ERROR'
    );
  }
}

// ==================== AUTH API ====================

export interface LoginRequest {
  phone: string;
  otp: string;
}

export interface LoginResponse {
  token: string;
  user: {
    id: string;
    firstName: string;
    lastName: string;
    phone: string;
    role: string;
  };
}

export const authApi = {
  login: (data: LoginRequest) =>
    apiFetch<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  register: (data: { phone: string; firstName: string; lastName: string }) =>
    apiFetch<{ message: string }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getMe: () =>
    apiFetch<LoginResponse['user']>('/auth/me'),

  sendOtp: (phone: string) =>
    apiFetch<{ message: string }>('/auth/send-otp', {
      method: 'POST',
      body: JSON.stringify({ phone }),
    }),
};

// ==================== DOCTORS API ====================

export interface Doctor {
  id: string;
  name: string;
  title?: string;
  specialization: string;
  consultationFee: number;
  rating?: number;
  reviews?: number;
  availableDays?: string;
  availableTimeSlots?: string;
  nextAvailable?: string;
}

export const doctorsApi = {
  getAll: (search?: string) =>
    apiFetch<Doctor[]>(`/doctors${search ? `?search=${search}` : ''}`),

  getById: (id: string) =>
    apiFetch<Doctor>(`/doctors/${id}`),

  getAvailability: (id: string, date: string) =>
    apiFetch<{ slots: string[] }>(`/doctors/${id}/availability?date=${date}`),
};

// ==================== APPOINTMENTS API ====================

export interface Appointment {
  id: string;
  doctorId: string;
  doctorName: string;
  patientName: string;
  patientPhone: string;
  date: string;
  time: string;
  serial: number;
  status: 'pending' | 'confirmed' | 'completed' | 'cancelled';
  fee: number;
}

export const appointmentsApi = {
  getAll: () =>
    apiFetch<Appointment[]>('/appointments'),

  getById: (id: string) =>
    apiFetch<Appointment>(`/appointments/${id}`),

  create: (data: {
    doctorId: string;
    date: string;
    time: string;
    patientName: string;
    patientPhone: string;
  }) =>
    apiFetch<Appointment>('/appointments', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateStatus: (id: string, status: string) =>
    apiFetch<Appointment>(`/appointments/${id}`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    }),
};

// ==================== AI API ====================

export interface AiChatRequest {
  message: string;
  history?: Array<{ role: string; content: string }>;
}

export interface AiChatResponse {
  reply: string;
  history: Array<{ role: string; content: string }>;
}

export interface SymptomAnalysis {
  conditions: Array<{
    name: string;
    confidence: number;
    icd: string;
  }>;
  tests: string[];
  urgency: 'low' | 'medium' | 'high';
  recommendation: string;
}

export interface LabReportAnalysis {
  reportType: string;
  analysis: {
    status: string;
    flag?: string;
  };
  interpretation: string;
}

export interface PrescriptionCheck {
  interactions: Array<{
    drugs: string;
    severity: string;
    note: string;
  }>;
  warnings: Array<{ note: string }>;
  recommendation: string;
}

export const aiApi = {
  // Chat with MedBot
  chat: (data: AiChatRequest) =>
    apiFetch<AiChatResponse>('/ai/chat', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Analyze symptoms
  analyzeSymptoms: (symptoms: string) =>
    apiFetch<SymptomAnalysis>('/ai/analyze-symptoms', {
      method: 'POST',
      body: JSON.stringify({ symptoms }),
    }),

  // Analyze lab report
  analyzeLabReport: (reportType: string, values: any[]) =>
    apiFetch<LabReportAnalysis>('/ai/analyze-lab-report', {
      method: 'POST',
      body: JSON.stringify({ reportType, values }),
    }),

  // Check prescription
  checkPrescription: (medications: string[]) =>
    apiFetch<PrescriptionCheck>('/ai/check-prescription', {
      method: 'POST',
      body: JSON.stringify({ medications }),
    }),
};

// ==================== REVIEWS API ====================

export interface Review {
  id: string;
  doctorId: string;
  patientName: string;
  rating: number;
  comment: string;
  createdAt: string;
}

export const reviewsApi = {
  getByDoctor: (doctorId: string) =>
    apiFetch<Review[]>(`/reviews/doctor/${doctorId}`),

  create: (data: { doctorId: string; rating: number; comment: string }) =>
    apiFetch<Review>('/reviews', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
};

// ==================== ADMIN API ====================

export interface AdminStats {
  todayAppointments: number;
  confirmedAppointments: number;
  pendingAppointments: number;
  totalPatients: number;
  totalDoctors: number;
}

export const adminApi = {
  getStats: () =>
    apiFetch<AdminStats>('/admin/stats'),

  getUsers: (role?: string) =>
    apiFetch<any[]>(`/admin/users${role ? `?role=${role}` : ''}`),

  updateUser: (userId: string, data: { isActive?: boolean; role?: string }) =>
    apiFetch<any>(`/admin/users/${userId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  getAuditLogs: (limit?: number) =>
    apiFetch<any[]>(`/admin/audit-logs${limit ? `?limit=${limit}` : ''}`),
};

export default {
  auth: authApi,
  doctors: doctorsApi,
  appointments: appointmentsApi,
  ai: aiApi,
  reviews: reviewsApi,
  admin: adminApi,
  setToken,
  removeToken,
  getToken,
};
