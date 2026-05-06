# MedCore AI — Intelligent Healthcare Management Platform

**MedCore AI** is an AI-powered diagnostic centre management system built with React, Node.js, and AI services (Anthropic Claude). It provides intelligent diagnostics, second-opinion systems, appointment booking, and conversational assistants for patients, doctors, and administrators.

## Products

| Product | Description |
|---------|-------------|
| **MedBot** | AI Assistant for symptom checking, appointment booking, and patient queries. |
| **AI Clinical Panel** | Diagnosis assistance, lab report analysis & prescription review for doctors. |
| **ETL Hub** | Real-time sync with ERP, Lab systems & Insurance. |

## Tech Stack

- **Frontend:** React 18, TypeScript, Vite, CSS Modules, Recharts
- **Backend:** Node.js, Express.js, Prisma ORM, PostgreSQL
- **AI Services:** Anthropic Claude (chat), Groq (fast diagnosis)
- **Storage:** AWS S3 (files), MongoDB (logs)
- **Infrastructure:** Docker, GitHub Actions

## Getting Started

### Prerequisites

- Node.js ≥18, npm ≥9
- PostgreSQL 16+ (via Docker)
- API keys for Anthropic, Groq (optional for full AI features)

### Local Development

```bash
# Clone the repository
git clone https://github.com/labaid-ai/medcore.git
cd medcore

# Install frontend dependencies
npm install

# Start PostgreSQL with Docker
docker-compose up -d

# Start backend (optional - for full features)
cd backend
npm install
node src/index.js

# Start frontend
npm run dev
```

### Environment Variables

Copy `env.example` to `.env.local` and configure:

```bash
cp env.example .env.local
```

Key variables:
- `VITE_ANTHROPIC_API_KEY` - For AI chat (required for MedBot)
- `DATABASE_URL` - PostgreSQL connection (for backend)

### Running Tests

```bash
npm test          # Run all tests
npm run dev      # Start dev server
```

## Project Structure

```
medcore/
├── src/
│   ├── components/      # Reusable UI components
│   ├── features/      # View components (Home, Doctors, Chatbot, etc.)
│   ├── hooks/         # Custom React hooks
│   ├── services/      # API clients
│   ├── utils/        # Utility functions
│   ├── constants/     # Design tokens, data
│   ├── types/        # TypeScript types
│   └── test/         # Test files
├── backend/          # Express.js API server
├── docs/             # Documentation
└── docker-compose.yml # PostgreSQL setup
```

## Key Features

- 🩺 **AI Symptom Checker** - Differential diagnosis with ICD-10 codes
- 📅 **Appointment Booking** - Doctor selection, slot booking, confirmation
- 💊 **Prescription Checker** - Drug interaction analysis
- 📊 **Lab Report Analysis** - Flag abnormal values, clinical interpretation
- 💬 **MedBot Chat** - Conversational AI for patient queries
- 👨‍⚕️ **Doctor Dashboard** - Schedule management, patient history
- 📂 **Patient Portal** - Reports, prescriptions, appointments
- 🔒 **Role-Based Access** - Admin, Doctor, Patient roles
- 🔄 **ETL Integration** - ERP, LIS, Insurance sync

## User Roles

| Role | Access |
|------|--------|
| **Patient** | Book appointments, view reports, chat with MedBot |
| **Doctor** | View schedule, patient history, write prescriptions |
| **Admin** | Full system control, analytics, user management |

## API Documentation

The backend provides RESTful APIs under `/api/v1`:

- `/api/v1/auth/*` - Authentication
- `/api/v1/doctors/*` - Doctor management
- `/api/v1/appointments/*` - Booking system
- `/api/v1/ai/*` - AI services (chat, diagnosis)
- `/api/v1/reviews/*` - Patient reviews
- `/api/v1/admin/*` - Admin dashboard

See `docs/postman_collection.json` for full API details.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                       │
├─────────────────────────────────────────────────────────────┤
│  Home │ Doctors │ Chatbot │ AI Clinical │ Portal │ ETL │ Admin│
├─────────────────────────────────────────────────────────────┤
│                     API Services                          │
│                 (aiApi, doctorsApi, etc.)                 │
├─────────────────────────────────────────────────────────────┤
│                   Backend (Express)                      │
│  Auth │ Doctors │ Appointments │ AI │ Reviews │ Admin        │
├─────────────────────────────────────────────────────────────┤
│                   Database (PostgreSQL)                  │
│            via Prisma ORM                                 │
└─────────────────────────────────────────────────────────────┘
```

## Contributing

1. Create a feature branch (`git checkout -b feature/your-feature`)
2. Make changes and add tests
3. Commit with clear messages
4. Push to the repository
5. Create a Pull Request

## License

Proprietary — All rights reserved by LABAID AI.

## Support

For issues and questions:
- Email: support@labaid-ai.com
- Phone: 01700-000000 (Bangladesh)
