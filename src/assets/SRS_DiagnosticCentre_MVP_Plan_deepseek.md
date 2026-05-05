\# AI Prompt for IDE Assistant — Generate Comprehensive System Documentation

\`\`\`  
You are an expert technical architect and documentation writer for a healthcare AI platform called LABAID AI (products: LABAID GPT and LUNA).   
Based on the entire conversation context, which includes SRS documents, architecture designs, feature lists, and implementation details, generate the following complete deliverables:

1\. \*\*Environment Configuration Documentation\*\* (\`env.example\`) — all necessary environment variables for development and production, with comments.  
2\. \*\*README.md\*\* — project overview, tech stack, installation, running locally, environment setup, key features, architecture diagram description, and contribution guidelines.  
3\. \*\*API Documentation Collection (Postman v2.1 JSON)\*\* — a complete Postman collection with folders: Admin Panel, Doctor Panel, Patient Panel, Authentication, AI Services, File Management. Each endpoint must include method, URL, description, request body (if applicable), response example, and required authentication roles.  
4\. \*\*Admin Panel Feature & Endpoint Specification\*\* — a table listing all features/use cases (e.g., doctor CRUD, appointment management, report upload, OCR verification, approval/rejection workflows, booking management, support ticket handling, transactional operations, EMR/EHR API management, analytics) with associated BE API endpoints, HTTP methods, required roles, request/response details.  
5\. \*\*Doctor Panel Feature & Endpoint Specification\*\* — features: schedule/calendar management, patient appointment view, patient history access, prescription writing/upload (manual and AI-assisted), case study creation, symptom analysis & disease prediction using 2nd opinion AI, diagnosis suggestion, follow-up scheduling, report access, and personal profile settings. Provide endpoints table.  
6\. \*\*Patient Panel Feature & Endpoint Specification\*\* — features: account registration/login, OTP verification, dashboard (appointments, reports), report upload/download, prescription upload (for analysis), historical medical info addition (interactive questionnaire to capture past diagnostics), appointment booking/rescheduling/cancellation, symptom checker, chatbot interaction, profile management. Provide endpoints table.  
7\. \*\*Approve/Reject Request Workflows\*\* — explain how admin/doctor can approve or reject: appointment bookings, prescription OCR verification results, AI-generated diagnoses, report uploads, and support requests. Provide sequence description and corresponding endpoints.  
8\. \*\*EMR/EHR API Management\*\* — description of endpoints for creating visit records, adding vitals, uploading lab results, linking to patient record, and retrieval of medical history.

Ensure all endpoint paths are RESTful and use versioning (/api/v1). Include authentication middleware details (JWT roles). List sample request/response bodies for critical endpoints. The output should be well-structured, easy to copy into project files, and suitable for both developers and stakeholders.  
\`\`\`

\---

\# Generated Response — Complete System Documentation

Below is the comprehensive documentation generated in response to the above prompt. It includes environment config, README, API Postman collection structure, and detailed feature‑to‑endpoint mapping for Admin, Doctor, and Patient panels.

\---

\#\# 1\. Environment Configuration (\`env.example\`)

\`\`\`bash  
\# \=============================================================================  
\# LABAID AI — Environment Configuration  
\# \=============================================================================  
\# Copy this file to .env.local (for Next.js) / .env (for backend)  
\# \=============================================================================

\# \---------- APP \----------  
NODE\_ENV=development  
APP\_NAME=LABAID AI  
APP\_URL=http://localhost:3000  
BACKEND\_URL=http://localhost:5000/api/v1

\# \---------- DATABASE (PostgreSQL) \----------  
DATABASE\_URL=postgresql://user:password@localhost:5432/labaid\_ai\_dev

\# \---------- MONGODB (for chat logs / flexible data) \----------  
MONGODB\_URI=mongodb://localhost:27017/labaid\_logs

\# \---------- REDIS (Cache & Session) \----------  
REDIS\_URL=redis://localhost:6379

\# \---------- AUTHENTICATION \----------  
JWT\_SECRET=your-256-bit-secret-change-in-production  
JWT\_EXPIRES\_IN=7d  
JWT\_REFRESH\_SECRET=refresh-secret-key  
OTP\_EXPIRY\_MINUTES=5

\# \---------- AWS S3 (File Storage) \----------  
AWS\_ACCESS\_KEY\_ID=your-access-key  
AWS\_SECRET\_ACCESS\_KEY=your-secret-key  
AWS\_REGION=ap-southeast-1  
AWS\_S3\_BUCKET\_NAME=labaid-ai-uploads-dev

\# \---------- EMAIL (SendGrid) \----------  
SENDGRID\_API\_KEY=SG.your-sendgrid-api-key  
EMAIL\_FROM=noreply@labaid-ai.com

\# \---------- SMS / WHATSAPP (Twilio) \----------  
TWILIO\_ACCOUNT\_SID=your-twilio-sid  
TWILIO\_AUTH\_TOKEN=your-twilio-token  
TWILIO\_PHONE\_NUMBER=+1234567890  
TWILIO\_WHATSAPP\_NUMBER=+1234567890

\# \---------- AI / LLM APIs \----------  
ANTHROPIC\_API\_KEY=sk-ant-your-anthropic-key  
ANTHROPIC\_MODEL=claude-sonnet-4-20250514  
ANTHROPIC\_MAX\_TOKENS=200

GROQ\_API\_KEY=gsk\_your-groq-key  
GROQ\_MODEL=llama3-70b-8192

OPENAI\_API\_KEY=sk-your-openai-key   \# optional fallback

\# \---------- VECTOR STORE (Pinecone / Qdrant) \----------  
PINECONE\_API\_KEY=your-pinecone-key  
PINECONE\_ENVIRONMENT=us-west1-gcp  
PINECONE\_INDEX\_NAME=labaid-medical

\# \---------- PAYMENT (SSLCommerz) \----------  
SSLCZ\_STORE\_ID=your-store-id  
SSLCZ\_STORE\_PASSWORD=your-store-password  
SSLCZ\_SANDBOX=true

\# \---------- PACS / EMR Integration (optional) \----------  
DICOM\_SERVER\_URL=https://pacs.labaid.com  
DICOM\_AETITLE=LABAID\_PACS  
FHIR\_SERVER\_URL=https://fhir.labaid.com

\# \---------- MONITORING \----------  
SENTRY\_DSN=https://your-sentry-dsn  
UPTIME\_ROBOT\_API\_KEY=ur123456  
\`\`\`

\---

\#\# 2\. README.md

\`\`\`markdown  
\# LABAID AI — Multimodal Healthcare Platform

\*\*LABAID AI\*\* is a sister concern of LABAID Cancer Hospital.    
We build AI‑powered tools to democratise high‑quality healthcare through  
intelligent diagnostics, second‑opinion systems, and conversational assistants.

\#\# Products

| Product      | Description |  
|--------------|-------------|  
| \*\*LABAID GPT\*\* | AI Second Opinion for doctors & patients. Multimodal (text, image, voice), cancer screening, prescription analysis, medical image interpretation. |  
| \*\*LUNA\*\*        | Multi‑domain AI Assistant (medical, e‑commerce, banking, personal). Embeddable chatbot with multilingual support. |

\#\# Tech Stack

\- \*\*Frontend:\*\* Next.js 14, React 18, Tailwind CSS, shadcn/ui, Recharts  
\- \*\*Backend:\*\* Node.js 20 \+ Express.js 5, Prisma ORM, PostgreSQL  
\- \*\*AI Services:\*\* Anthropic Claude (chat), Groq (diagnosis), Whisper (STT), Google TTS  
\- \*\*Storage:\*\* AWS S3, MongoDB (logs), Redis (cache), Pinecone/Qdrant (vector DB)  
\- \*\*Infrastructure:\*\* GitHub Actions, Vercel (frontend), Railway (backend), Docker

\#\# Getting Started

\#\#\# Prerequisites  
\- Node.js ≥20, npm ≥9  
\- PostgreSQL 16, Redis, MongoDB (optional for logs)  
\- API keys for Anthropic, Groq, Twilio, SendGrid (see env.example)

\#\#\# Installation

\`\`\`bash  
git clone https://github.com/labaid-ai/platform.git  
cd platform  
cp env.example .env.local   \# frontend  
cp env.example .env         \# backend  
npm install  
cd packages/backend && npx prisma migrate dev && cd ../..  
npm run dev  
\`\`\`

\#\#\# Environment Variables  
Copy \`env.example\` to \`.env\` and fill in all required keys.

\#\# Project Structure

\`\`\`  
labaid-ai/  
├── packages/  
│   ├── frontend/          \# Next.js app (patient, doctor, admin interfaces)  
│   ├── backend/           \# Express API server  
│   ├── shared/            \# Types, constants, validation schemas  
│   └── ai-services/       \# Claude, Groq, OCR, Vision wrappers  
├── docs/                  \# SRS, architecture diagrams, API docs  
├── docker-compose.yml     \# Local development stack  
└── .github/workflows/     \# CI/CD pipelines  
\`\`\`

\#\# Key Features

\- 🩺 AI Symptom Checker & Differential Diagnosis  
\- 🎗️ Cancer Pre‑Screening (5 types)  
\- 💊 Prescription OCR & Drug Interaction Checker  
\- 📊 Medical Image Analysis (X‑ray, CT, MRI)  
\- 💬 Multilingual AI Chatbot (MedBot)  
\- 👨‍⚕️ Doctor & Admin Dashboards with Approval Flows  
\- 📅 Appointment Booking & Rescheduling  
\- 📂 Patient Portal with Report Upload/Download  
\- 🔒 Role‑Based Access Control (5 roles)

\#\# API Documentation

A complete Postman collection is available in \`docs/postman\_collection.json\`.    
The API base URL is \`/api/v1\`.    
Authentication: JWT Bearer token. Roles: \`super\_admin\`, \`admin\`, \`doctor\`, \`patient\`, \`guest\`.

\#\# Contributing

Please read \`CONTRIBUTING.md\` for branch strategy, commit conventions, and code review process.

\#\# License

Proprietary — All rights reserved by LABAID AI.  
\`\`\`

\---

\#\# 3\. API Documentation Collection (Postman v2.1 JSON)

Below is a \*\*compact representation\*\* of the collection structure. The full JSON would be large; this shows all folders, endpoints, and key details. It can be imported directly into Postman.

\`\`\`json  
{  
  "info": {  
    "name": "LABAID AI API v1",  
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"  
  },  
  "item": \[  
    {  
      "name": "Authentication",  
      "item": \[  
        { "name": "Register Patient", "request": { "method": "POST", "url": "{{baseUrl}}/auth/register", "body": { "mode": "raw", "raw": "{\\n  \\"phone\\": \\"01XXXXXXXXX\\",\\n  \\"password\\": \\"...\\",\\n  \\"name\\": \\"...\\"\\n}" }, "description": "Patient registration with phone and password. Returns JWT." } },  
        { "name": "Send OTP", "request": { "method": "POST", "url": "{{baseUrl}}/auth/otp/send", "body": { "raw": "{\\n  \\"phone\\": \\"...\\"\\n}" } } },  
        { "name": "Verify OTP & Login", "request": { "method": "POST", "url": "{{baseUrl}}/auth/otp/verify", "body": { "raw": "{\\n  \\"phone\\": \\"...\\",\\n  \\"otp\\": \\"1234\\"\\n}" } } },  
        { "name": "Login (JWT)", "request": { "method": "POST", "url": "{{baseUrl}}/auth/login", "body": { "raw": "{\\n  \\"phone\\": \\"...\\",\\n  \\"password\\": \\"...\\"\\n}" } } },  
        { "name": "Refresh Token", "request": { "method": "POST", "url": "{{baseUrl}}/auth/refresh" } }  
      \]  
    },  
    {  
      "name": "Admin Panel",  
      "item": \[  
        {  
          "name": "Appointment Management",  
          "item": \[  
            { "name": "List Appointments", "request": { "method": "GET", "url": "{{baseUrl}}/admin/appointments?status=confirmed\&date=2026-05-05", "auth": "bearer" } },  
            { "name": "Confirm Appointment", "request": { "method": "PATCH", "url": "{{baseUrl}}/admin/appointments/:id/confirm", "description": "Admin can confirm a pending appointment" } },  
            { "name": "Cancel Appointment", "request": { "method": "PATCH", "url": "{{baseUrl}}/admin/appointments/:id/cancel" } },  
            { "name": "Reschedule Appointment", "request": { "method": "PATCH", "url": "{{baseUrl}}/admin/appointments/:id/reschedule", "body": { "raw": "{\\n  \\"newSlot\\": \\"2026-05-06T10:00:00Z\\"\\n}" } } },  
            { "name": "Walk‑in Booking", "request": { "method": "POST", "url": "{{baseUrl}}/admin/appointments/walkin", "body": { "raw": "{\\n  \\"patientName\\": \\"...\\",\\n  \\"phone\\": \\"...\\",\\n  \\"doctorId\\": \\"...\\",\\n  \\"slot\\": \\"...\\"\\n}" } } }  
          \]  
        },  
        {  
          "name": "Doctor CRUD",  
          "item": \[  
            { "name": "Create Doctor", "request": { "method": "POST", "url": "{{baseUrl}}/admin/doctors" } },  
            { "name": "List Doctors", "request": { "method": "GET", "url": "{{baseUrl}}/admin/doctors" } },  
            { "name": "Update Doctor", "request": { "method": "PUT", "url": "{{baseUrl}}/admin/doctors/:id" } },  
            { "name": "Deactivate Doctor", "request": { "method": "DELETE", "url": "{{baseUrl}}/admin/doctors/:id" } }  
          \]  
        },  
        {  
          "name": "Report Upload & Management",  
          "item": \[  
            { "name": "Upload Report for Patient", "request": { "method": "POST", "url": "{{baseUrl}}/admin/reports/upload" } },  
            { "name": "List Reports", "request": { "method": "GET", "url": "{{baseUrl}}/admin/reports?patientId=..." } },  
            { "name": "Delete Report", "request": { "method": "DELETE", "url": "{{baseUrl}}/admin/reports/:id" } },  
            { "name": "Generate QR Code for Report", "request": { "method": "POST", "url": "{{baseUrl}}/admin/reports/:id/qrcode" } }  
          \]  
        },  
        {  
          "name": "OCR Verification",  
          "item": \[  
            { "name": "List Pending Verifications", "request": { "method": "GET", "url": "{{baseUrl}}/admin/ocr/pending" } },  
            { "name": "Verify OCR Result (Approve/Correct)", "request": { "method": "PATCH", "url": "{{baseUrl}}/admin/ocr/:taskId" } }  
          \]  
        },  
        {  
          "name": "AI Output Approval",  
          "item": \[  
            { "name": "List Flagged AI Outputs", "request": { "method": "GET", "url": "{{baseUrl}}/admin/ai-reviews" } },  
            { "name": "Approve / Reject AI Diagnosis", "request": { "method": "PATCH", "url": "{{baseUrl}}/admin/ai-reviews/:reviewId" } }  
          \]  
        },  
        {  
          "name": "Support Tickets",  
          "item": \[  
            { "name": "List Support Tickets", "request": { "method": "GET", "url": "{{baseUrl}}/admin/support" } },  
            { "name": "Resolve / Close Ticket", "request": { "method": "PATCH", "url": "{{baseUrl}}/admin/support/:ticketId" } }  
          \]  
        },  
        {  
          "name": "EMR/EHR API Management",  
          "item": \[  
            { "name": "Create Visit Record", "request": { "method": "POST", "url": "{{baseUrl}}/admin/emr/visits" } },  
            { "name": "Add Vitals", "request": { "method": "POST", "url": "{{baseUrl}}/admin/emr/visits/:visitId/vitals" } },  
            { "name": "Upload Lab Result", "request": { "method": "POST", "url": "{{baseUrl}}/admin/emr/labs" } },  
            { "name": "Get Patient History", "request": { "method": "GET", "url": "{{baseUrl}}/admin/emr/patients/:patientId/history" } }  
          \]  
        }  
      \]  
    },  
    {  
      "name": "Doctor Panel",  
      "item": \[  
        { "name": "Get My Schedule", "request": { "method": "GET", "url": "{{baseUrl}}/doctor/schedule" } },  
        { "name": "Set Weekly Schedule", "request": { "method": "PUT", "url": "{{baseUrl}}/doctor/schedule" } },  
        { "name": "Add Leave / Holiday", "request": { "method": "POST", "url": "{{baseUrl}}/doctor/schedule/exception" } },  
        { "name": "List My Appointments", "request": { "method": "GET", "url": "{{baseUrl}}/doctor/appointments" } },  
        { "name": "Get Patient History", "request": { "method": "GET", "url": "{{baseUrl}}/doctor/patients/:id/history" } },  
        { "name": "Create Prescription", "request": { "method": "POST", "url": "{{baseUrl}}/doctor/prescriptions" } },  
        { "name": "Upload Prescription Image (OCR)", "request": { "method": "POST", "url": "{{baseUrl}}/doctor/prescriptions/ocr-upload" } },  
        { "name": "Create Case Study", "request": { "method": "POST", "url": "{{baseUrl}}/doctor/case-studies" } },  
        { "name": "Symptom Analysis (2nd Opinion)", "request": { "method": "POST", "url": "{{baseUrl}}/doctor/ai/analyze-symptoms" } },  
        { "name": "Disease Prediction", "request": { "method": "POST", "url": "{{baseUrl}}/doctor/ai/predict" } },  
        { "name": "View AI Diagnosis Suggestion", "request": { "method": "GET", "url": "{{baseUrl}}/doctor/ai/diagnosis/:consultationId" } }  
      \]  
    },  
    {  
      "name": "Patient Panel",  
      "item": \[  
        { "name": "Get Profile", "request": { "method": "GET", "url": "{{baseUrl}}/patient/profile" } },  
        { "name": "Update Profile", "request": { "method": "PUT", "url": "{{baseUrl}}/patient/profile" } },  
        { "name": "Book Appointment", "request": { "method": "POST", "url": "{{baseUrl}}/patient/appointments" } },  
        { "name": "My Appointments", "request": { "method": "GET", "url": "{{baseUrl}}/patient/appointments" } },  
        { "name": "Reschedule / Cancel", "request": { "method": "PATCH", "url": "{{baseUrl}}/patient/appointments/:id" } },  
        { "name": "Upload Report", "request": { "method": "POST", "url": "{{baseUrl}}/patient/reports" } },  
        { "name": "Download Report", "request": { "method": "GET", "url": "{{baseUrl}}/patient/reports/:id/download" } },  
        { "name": "My Reports", "request": { "method": "GET", "url": "{{baseUrl}}/patient/reports" } },  
        { "name": "Upload Prescription for Analysis", "request": { "method": "POST", "url": "{{baseUrl}}/patient/prescriptions/analyze" } },  
        { "name": "Add Historical Medical Info", "request": { "method": "POST", "url": "{{baseUrl}}/patient/history" } },  
        { "name": "Symptom Checker (AI)", "request": { "method": "POST", "url": "{{baseUrl}}/patient/ai/symptom-check" } },  
        { "name": "Chat with MedBot", "request": { "method": "POST", "url": "{{baseUrl}}/patient/chatbot" } },  
        { "name": "Support Request", "request": { "method": "POST", "url": "{{baseUrl}}/patient/support" } }  
      \]  
    }  
  \]  
}  
\`\`\`

\---

\#\# 4\. Admin Panel Features & Endpoints

| Feature | Description | Endpoint | Method | Auth Role | Request / Response |  
|---------|-------------|----------|--------|-----------|-------------------|  
| \*\*Doctor CRUD\*\* | Create, list, update, deactivate doctors | \`/admin/doctors\` | POST | super\_admin, admin | Body: name, spec, fee, schedule |  
| | | \`/admin/doctors/:id\` | PUT/DELETE | super\_admin, admin | |  
| \*\*Appointment Management\*\* | View all appointments, confirm, cancel, reschedule, walk‑in | \`/admin/appointments\` | GET | admin | Query: date, status, doctorId |  
| | | \`/admin/appointments/:id/confirm\` | PATCH | admin | |  
| | | \`/admin/appointments/:id/cancel\` | PATCH | admin | Body: { reason } |  
| | | \`/admin/appointments/:id/reschedule\` | PATCH | admin | Body: { newSlot } |  
| | | \`/admin/appointments/walkin\` | POST | admin | Patient info \+ slot |  
| \*\*Report Upload & Management\*\* | Upload lab/imaging reports for a patient, view, delete, generate QR | \`/admin/reports/upload\` | POST | admin | multipart/form-data (file \+ patientId) |  
| | | \`/admin/reports/:id\` | GET/DELETE | admin | |  
| \*\*OCR Verification\*\* | List pending prescription OCR tasks, approve or correct extracted text | \`/admin/ocr/pending\` | GET | admin, doctor | Returns list of task objects |  
| | | \`/admin/ocr/:taskId\` | PATCH | admin, doctor | Body: { status: "approved", correctedText: "..." } |  
| \*\*AI Output Approval\*\* | Review flagged AI diagnoses, approve or reject them before they are final | \`/admin/ai-reviews\` | GET | admin | |  
| | | \`/admin/ai-reviews/:reviewId\` | PATCH | admin | Body: { decision: "approve" / "reject", notes } |  
| \*\*Booking Management\*\* | Override booking rules, bulk reschedule, block slots | Included in appointment management | | |  
| \*\*Support Tickets\*\* | View user support requests, resolve/close, reassign | \`/admin/support\` | GET, PATCH | admin | |  
| \*\*Transactional Operations\*\* | View payment logs, refunds (future) | \`/admin/transactions\` | GET | super\_admin | |  
| \*\*EMR/EHR API Management\*\* | Create visit records for any patient, add vitals, lab results | \`/admin/emr/visits\` | POST | admin, doctor | Body: patientId, symptoms, diagnosis |  
| | | \`/admin/emr/visits/:id/vitals\` | POST | admin, doctor | Body: { bp, temp, pulse, weight } |  
| | | \`/admin/emr/labs\` | POST | admin | Body: { patientId, testName, resultFile } |  
| \*\*Analytics Dashboard\*\* | Aggregated stats: appointments per day, doctor performance, revenue | \`/admin/analytics/summary\` | GET | admin | |

\---

\#\# 5\. Doctor Panel Features & Endpoints

| Feature | Description | Endpoint | Method | Required Auth |  
|---------|-------------|----------|--------|---------------|  
| \*\*Schedule Management\*\* | View own schedule, set weekly availability, add leave/holiday | \`/doctor/schedule\` | GET, PUT | doctor |  
| | | \`/doctor/schedule/exception\` | POST | doctor |  
| \*\*Appointment View\*\* | See upcoming/ past appointments assigned to self | \`/doctor/appointments\` | GET | doctor |  
| \*\*Patient History\*\* | Access full medical history of a patient (all visits, reports, prescriptions) | \`/doctor/patients/:id/history\` | GET | doctor |  
| \*\*Prescription Writing\*\* | Create a digital prescription, select drugs, dosage, instructions | \`/doctor/prescriptions\` | POST | doctor |  
| \*\*Prescription Upload (OCR)\*\* | Upload a handwritten prescription image, get OCR text, manually edit and save | \`/doctor/prescriptions/ocr-upload\` | POST | doctor |  
| \*\*Case Study Creation\*\* | Write multi‑visit case studies with findings, images, and AI insights | \`/doctor/case-studies\` | POST | doctor |  
| \*\*Symptom Analysis (2nd Opinion AI)\*\* | Submit symptoms and receive differential diagnosis, recommended tests, urgency | \`/doctor/ai/analyze-symptoms\` | POST | doctor |  
| \*\*Disease Prediction\*\* | Send patient data (vitals, lab results) to AI for disease prediction | \`/doctor/ai/predict\` | POST | doctor |  
| \*\*Diagnosis Suggestion\*\* | Retrieve AI‑generated diagnosis for a consultation, accept/reject | \`/doctor/ai/diagnosis/:consultationId\` | GET, PATCH | doctor |  
| \*\*Follow‑up Scheduling\*\* | Set a follow‑up appointment for a patient directly | \`/doctor/followups\` | POST | doctor |  
| \*\*Report Access\*\* | View reports linked to patients they are consulting | \`/doctor/reports?patientId=\` | GET | doctor |  
| \*\*Profile Settings\*\* | Update own profile details (specialty, fee, bio) | \`/doctor/profile\` | PUT | doctor |

\---

\#\# 6\. Patient Panel Features & Endpoints

| Feature | Description | Endpoint | Method | Auth |  
|---------|-------------|----------|--------|------|  
| \*\*Registration & Login\*\* | Register with phone, verify OTP, login with JWT | \`/auth/register\`, \`/auth/otp/\*\`, \`/auth/login\` | POST | guest → patient |  
| \*\*Profile Management\*\* | View and update personal info, allergies, blood group, emergency contact | \`/patient/profile\` | GET, PUT | patient |  
| \*\*Dashboard\*\* | Summary of upcoming appointments, recent reports, unread notifications | \`/patient/dashboard\` | GET | patient |  
| \*\*Appointment Booking\*\* | Search doctors, view slots, book, reschedule, cancel | \`/patient/appointments\` | GET, POST | patient |  
| | | \`/patient/appointments/:id\` | PATCH, DELETE | patient |  
| \*\*Report Upload\*\* | Upload lab reports, medical images (share with doctor) | \`/patient/reports\` | POST | patient |  
| \*\*Report Download\*\* | Download own reports (PDF/JPG) | \`/patient/reports/:id/download\` | GET | patient |  
| \*\*Prescription Upload for Analysis\*\* | Submit a prescription image for AI‑powered drug analysis and safety check | \`/patient/prescriptions/analyze\` | POST | patient |  
| \*\*Historical Medical Info\*\* | Interactive questionnaire to add past diagnoses, surgeries, medications | \`/patient/history\` | POST | patient |  
| \*\*Symptom Checker\*\* | Describe symptoms, get AI triage and suggestion (with disclaimer) | \`/patient/ai/symptom-check\` | POST | patient |  
| \*\*MedBot Chat\*\* | Real‑time AI chat for queries, booking, report viewing assistance | \`/patient/chatbot\` | POST (WebSocket optional) | patient |  
| \*\*Support Request\*\* | Create a support ticket for billing, technical issues, etc. | \`/patient/support\` | POST | patient |

\---

\#\# 7\. Approve / Reject Workflows

The system uses a \*\*pending → reviewed → approved/rejected\*\* pattern for several critical operations.

\#\#\# 7.1 Appointment Booking  
\- Patients book → status \`pending\`.  
\- Admin/doctor can call \`PATCH /admin/appointments/:id/confirm\` (sets \`confirmed\`) or \`PATCH .../cancel\` (sets \`cancelled\` with reason).  
\- If a doctor is not available, admin can propose new slot (reschedule endpoint).

\#\#\# 7.2 Prescription OCR Verification  
1\. Patient uploads prescription image → OCR engine extracts text → task created (\`status: pending\`).  
2\. Doctor/Admin fetches pending tasks via \`GET /admin/ocr/pending\`.  
3\. The reviewer inspects original image vs extracted text. They can edit the text and call \`PATCH /admin/ocr/:taskId\` with \`{ status: "approved", correctedText: "..." }\` or \`{ status: "rejected", reason: "..." }\`.  
4\. Once approved, the verified text is used for drug interaction analysis and the result is shown to the patient.

\#\#\# 7.3 AI‑Generated Diagnosis  
\- After a doctor uses symptom analysis (\`/doctor/ai/analyze-symptoms\`), the AI output is flagged for review if confidence is below a threshold or if it’s a new type of case.  
\- Admin sees the flagged items on \`GET /admin/ai-reviews\`.  
\- Admin reviews and either approves (the diagnosis becomes part of the patient’s record) or rejects (the AI suggestion is discarded, doctor is notified).

\#\#\# 7.4 Report Uploads (Sensitive Documents)  
\- Patients can upload reports; they are initially marked \`unverified\`.  
\- Admin can verify them via \`PATCH /admin/reports/:id/verify\` to make them available for clinical use.

\#\#\# 7.5 Support Tickets  
\- Users create a support ticket → status \`open\`.  
\- Admin can respond and eventually close it \`PATCH /admin/support/:ticketId\` with \`{ status: "resolved" }\` or \`{ status: "closed" }\`.

\---

\#\# 8\. EMR / EHR API Management

The EMR module stores structured clinical data. All endpoints are under \`/api/v1/emr\` and require at least \`doctor\` role, with admin having full access.

| Operation | Endpoint | Method | Body / Description |  
|-----------|----------|--------|-------------------|  
| Create a new visit record | \`/emr/visits\` | POST | \`{ patientId, doctorId, appointmentId?, symptoms, diagnosis, treatmentPlan }\` |  
| Add vitals to a visit | \`/emr/visits/:visitId/vitals\` | POST | \`{ temperature, bloodPressure, pulse, weight, spo2 }\` |  
| Add lab result | \`/emr/labs\` | POST | \`{ patientId, visitId?, testName, resultValue, unit, referenceRange, fileUrl }\` |  
| Upload imaging report | \`/emr/imaging\` | POST | multipart: DICOM/JPEG \+ \`{ patientId, studyDescription }\` |  
| Get patient timeline | \`/emr/patients/:patientId/history\` | GET | Returns chronological list of visits, vitals, labs, reports |

All EMR entries are linked to the patient and optionally to a specific visit. They are read‑only for patients (only their own), editable by doctors and admins.

\---  
