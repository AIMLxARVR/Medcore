# MedCore Implementation Plan - Backend & Advanced Features

## Executive Summary

This document outlines the complete implementation plan for transforming MedCore from an MVP frontend prototype to a production-ready healthcare platform with AI capabilities, role-based access control, payment processing, and more.

**Target Stack:**
- Frontend: React + TypeScript + Vite (existing)
- Backend: NestJS (TypeScript) + PostgreSQL + Prisma ORM
- AI: vLLM (local) or OpenAI API (cloud)
- Container: Docker + Docker Compose

---

## 1. Architecture Overview

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Compose                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ React    │  │ NestJS   │  │ PostgreSQL│  │ vLLM    │ │
│  │ Frontend │←→│ API     │←→│ Database │  │ (AI)    │ │
│  │ :3000   │  │ :3001   │  │ :5432   │  │ :8000   │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│       ↓            ↓                            ↓             │
│  ┌──────────────────────────────────────────────┐        │
│  │ Nginx Reverse Proxy (optional)              │        │
│  └──────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Database Schema (Prisma)

```prisma
// Core entities
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  passwordHash  String
  role         Role      @default(PATIENT)
  phone        String?
  firstName    String
  lastName     String
  bloodGroup   String?
  dateOfBirth  DateTime?
  createdAt    DateTime  @default(now())
  updatedAt    DateTime  @updatedAt
  
  // Relations
  patientProfile PatientProfile?
  doctorProfile DoctorProfile?
  appointments Appointment[]
  payments     Payment[]
  reviews      Review[]
}

enum Role {
  PATIENT
  DOCTOR
  ADMIN
}

model PatientProfile {
  id              String  @id @default(cuid())
  userId           String  @unique
  user             User    @relation(fields: [userId], references: [id])
  emergencyContact String?
  insuranceId      String?
  medicalHistory  Json?
}

model DoctorProfile {
  id          String   @id @default(cuid())
  userId      String   @unique
  user       User     @relation(fields: [userId], references: [id])
  title      String   // MBBS, MD, etc.
  specialty  String   // Cardiology, Neurology, etc.
  department String
  fee        Int
  rating     Float    @default(0)
  reviewCount Int      @default(0)
  available  Boolean  @default(true)
  slots      Json     // Weekly schedule
}

model Appointment {
  id          String        @id @default(cuid())
  patientId    String
  patient     User          @relation(fields: [patientId], references: [id])
  doctorId    String
  doctor     User          @relation(fields: [doctorId], references: [id])
  dateTime    DateTime
  status     AppointmentStatus @default(PENDING)
  serialNo   Int?
  notes      String?
  createdAt  DateTime      @default(now())
  
  payment    Payment?
  review    Review?
}

enum AppointmentStatus {
  PENDING
  CONFIRMED
  COMPLETED
  CANCELLED
  NO_SHOW
}

model Payment {
  id            String      @id @default(cuid())
  appointmentId String     @unique
  appointment  Appointment @relation(fields: [appointmentId], references: [id])
  amount       Int
  method       PaymentMethod
  status       PaymentStatus @default(PENDING)
  transactionId String?
  invoiceNo    String     @unique
  paidAt       DateTime?
  createdAt    DateTime   @default(now())
}

enum PaymentMethod {
  CASH
  CARD
  BKASH
  NAGAD
  BANK_TRANSFER
}

enum PaymentStatus {
  PENDING
  COMPLETED
  FAILED
  REFUNDED
}

model Review {
  id            String   @id @default(cuid())
  appointmentId String   @unique
  appointment   Appointment @relation(fields: [appointmentId], references: [id])
  patientId     String
  patient       User     @relation(fields: [patientId], references: [id])
  doctorId      String
  rating        Int      // 1-5
  comment       String?
  createdAt     DateTime @default(now())
}

model AuditLog {
  id        String   @id @default(cuid())
  userId    String
  action   String
  entity   String
  entityId String
  metadata Json?
  createdAt DateTime @default(now())
}
```

### 1.3 API Endpoints Structure

```
/api/v1
├── /auth
│   ├── POST /login
│   ├── POST /register
│   ├── POST /refresh
│   └── POST /logout
├── /users
│   ├── GET /me
│   ├── PATCH /me
│   └── GET /:id (admin only)
├── /doctors
│   ├── GET / (with filters, pagination)
│   ├── GET /:id
│   ├── GET /:id/availability
│   └── GET /:id/reviews
├── /appointments
│   ├── GET / (role-based)
│   ├── POST /
│   ├── GET /:id
│   ├── PATCH /:id (status update)
│   └── DELETE /:id
├── /payments
│   ├── POST /create
│   ├── POST /webhook (for payment callbacks)
│   └── GET /:id
├── /reviews
│   ├── POST /
│   └── GET /doctor/:id
├── /ai
│   ├── POST /chat (chatbot)
│   ├── POST /analyze-symptoms
│   ├── POST /analyze-lab-report
│   └── POST /check-prescription
└── /admin
    ├── /stats
    ├── /audit-logs
    └── /export
```

---

## 2. Module Implementation Plan

### 2.1 Phase 1: Backend Foundation (Week 1-2)

#### Goals:
- Set up NestJS project with Prisma
- Create Docker Compose setup
- Implement authentication with JWT
- Basic RBAC implementation

#### Tasks:
1. **Setup NestJS + Prisma**
   - Initialize NestJS project
   - Configure Prisma with PostgreSQL
   - Create database migrations

2. **Docker Compose Setup**
   ```yaml
   # docker-compose.yml
   version: '3.8'
   
   services:
     postgres:
       image: postgres:15-alpine
       environment:
         POSTGRES_USER: medcore
         POSTGRES_PASSWORD: medcore_secret
         POSTGRES_DB: medcore
       volumes:
         - postgres_data:/var/lib/postgresql/data
       ports:
         - "5432:5432"
   
     api:
       build: ./backend
       ports:
         - "3001:3001"
       environment:
         DATABASE_URL: postgresql://medcore:medcore_secret@postgres:5432/medcore
       depends_on:
         - postgres
   
   volumes:
     postgres_data:
   ```

3. **Authentication Module**
   - JWT-based auth with refresh tokens
   - Password hashing with bcrypt
   - Login/Register endpoints
   - Demo user seeding

4. **RBAC Guards**
   - `@Roles('PATIENT')`
   - `@Roles('DOCTOR')`
   - `@Roles('ADMIN')`

#### Demo Credentials:
```
Patients:
  - email: patient@demo.com / password: demo123
  - email: farhan@demo.com / password: demo123

Doctors:
  - email: dr.fatima@demo.com / password: demo123 (Cardiologist)
  - email: dr.ahmed@demo.com / password: demo123 (Neurologist)

Admin:
  - email: admin@demo.com / password: demo123
```

---

### 2.2 Phase 2: AI Chatbot Enhancement (Week 2-3)

#### Goals:
- Replace demo chatbot with real AI integration
- Medical domain knowledge base
- Chain of Thought reasoning
- OCR for lab reports

#### Architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    Chatbot Flow                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  User Input → Sanitize → Intent Detection →                 │
│       │                                    │               │
│       ↓                                    ▼               │
│  ┌─────────┐     ┌────────────┐     ┌─────────────┐       │
│  │ Input   │────→│ Medical    │────→│ vLLM /     │       │
│  │ Validator│     │ Router    │     │ OpenAI API  │       │
│  └─────────┘     └────────────┘     └─────────────┘       │
│                                    │                      │
│                           Chain of Thought Prompt          │
│                                    ↓                      │
│                          ┌─────────────┐                  │
│                          │ Response   │                  │
│                          │ Generator  │                  │
│                          └─────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

#### Implementation:

1. **vLLM Setup (Local AI)**
   ```typescript
   // Use Ollama or vLLM for local deployment
   // Recommended: Ollama for easier setup
   // Model: mistral or medical-domain fine-tuned model
   ```

2. **Chain of Thought Prompting**
   ```typescript
   const MEDICAL_COT_PROMPT = `
   You are MedCore AI, a medical assistant. 
   
   Before responding:
   1. Identify key symptoms/diagnosis mentioned
   2. Check for urgency indicators (chest pain, breathing difficulty, etc.)
   3. Consider patient history if provided
   4. Formulate response with clear next steps
   
   Response format:
   - Assessment: [your analysis]
   - Confidence: [low/medium/high]
   - Recommendation: [specific action]
   - Escalation: [yes/no - should this go to a doctor?]
   `;
   ```

3. **OCR Integration**
   - Use Tesseract.js for client-side OCR
   - Or cloud vision API (Google Cloud Vision, AWS Textract)
   - Extract lab report values automatically

4. **Medical Knowledge Base**
   - Store ICD-10 codes, drug interactions
   - Use vector DB (pgvector) for RAG
   - Retrieval-augmented generation

---

### 2.3 Phase 3: Payment Module (Week 3)

#### Goals:
- Payment processing (dummy/integration ready)
- Invoice generation
- Booking payment flow

#### Features:

1. **Payment Methods (Dummy)**
   - Cash on delivery
   - Card (stripe-ready)
   - Mobile financial services (bKash, Nagad)

2. **Invoice Generation**
   ```typescript
   // Invoice structure
   {
     invoiceNo: "INV-2026-0001",
     patient: { name, phone, email },
     doctor: { name, specialty },
     appointment: { date, time, serial },
     items: [
       { description: "Consultation Fee", amount: 1500 }
     ],
     subtotal: 1500,
     discount: 0,
     total: 1500,
     paid: false,
     createdAt: Date
   }
   ```

3. **Payment Callback Handler**
   - Webhook endpoint for payment gateway
   - Automatic appointment confirmation on payment

---

### 2.4 Phase 4: Doctor Ratings & Reviews (Week 3-4)

#### Goals:
- Patients can rate doctors after appointments
- Average rating calculation
- Review display on doctor profile

#### Implementation:

1. **Review Model**
   - Only allowed after completed appointment
   - One review per appointment
   - Rating: 1-5 stars
   - Optional comment

2. **Rating Calculation**
   ```typescript
   // Automatic average calculation
   doctor.rating = reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length
   doctor.reviewCount = reviews.length
   ```

3. **Review Display**
   - Show on doctor card and detail page
   - Sort by recent/highest/lowest
   - Pagination support

---

### 2.5 Phase 5: Additional Crucial Modules

#### 2.5.1 Audit Logging
```typescript
// Track all important actions
@Injectable()
export class AuditService {
  log(userId: string, action: string, entity: string, entityId: string, metadata?: any) {
    // Log to database
    // Log to file/CloudWatch
  }
}
```

#### 2.5.2 Notification System
- SMS alerts (appointment confirmation)
- Email receipts
- In-app notifications

#### 2.5.3 Medical Records (EMR)
- Patient history timeline
- Lab reports storage
- Prescription history

#### 2.5.4 Reporting & Analytics
- Daily/weekly/monthly reports
- Revenue tracking
- Doctor performance metrics

#### 2.5.5 Inventory/Pharmacy (Future)
- Medicine stock management
- Prescription dispensing

---

## 3. Technology Recommendations

### 3.1 Database ORM: Prisma (vs TypeORM)

| Feature | Prisma | TypeORM |
|---------|--------|---------|
| Type Safety | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| DX | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Migrations | Good | Good |
| Performance | Good | ⭐⭐⭐⭐ |
| Raw SQL | Limited | Full |

**Recommendation: Prisma** - Better type safety, superior developer experience, works well with NestJS via PrismaModule.

### 3.2 AI Options

| Option | Pros | Cons |
|--------|-----|------|
| **Ollama (local)** | Free, private, no API costs | Moderate hardware needed |
| **vLLM (local)** | High performance, open weights | Complex setup |
| **OpenAI API** | Easy, reliable | Costs, data privacy concerns |
| **Anthropic API** | Great reasoning | Costs |

**Recommendation:** Start with OpenAI for reliability, migrate to Ollama for cost savings.

### 3.3 Docker Services

```yaml
services:
  postgres:
    image: postgres:15-alpine
  
  redis:
    image: redis:7-alpine
    # For session/cache
  
  api:
    build: ./backend
    environment:
      - DATABASE_URL
      - JWT_SECRET
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
  
  # Optional: Ollama for local AI
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
```

---

## 4. Implementation Timeline

| Phase | Duration | Key Deliverables |
|------|----------|------------------|
| Phase 1 | Week 1-2 | NestJS backend, Docker, Auth, RBAC |
| Phase 2 | Week 2-3 | AI chatbot with vLLM, OCR |
| Phase 3 | Week 3 | Payment module, invoicing |
| Phase 4 | Week 3-4 | Doctor ratings/reviews |
| Phase 5 | Week 4+ | Audit logs, notifications, EMR |

---

## 5. Next Steps

1. Confirm this plan
2. Create NestJS project structure
3. Set up Docker Compose
4. Implement Prisma schema
5. Start Phase 1 (Backend Foundation)

Would you like me to proceed with any specific phase or create the project scaffolding?

---

*Plan created by BLACKBOXAI - Senior Software Architect*
