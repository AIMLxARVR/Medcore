# MedCore Backend Implementation TODO

## ✅ COMPLETED - Phase 1: Auth & Security (CRITICAL)

### 1. Auth - Logout Endpoint ✅
- [x] Create `POST /api/auth/logout` - logout with token blacklisting
- [x] In: `backend/src/routes/auth.js`

### 2. User Profile Endpoints ✅  
- [x] Create `GET /api/auth/me` - get current user profile
- [x] Create `PATCH /api/auth/me` - update current user profile
- [x] In: `backend/src/routes/auth.js`

---

## ✅ COMPLETED - Phase 2: AI Backend Proxy (HIGH)

### 4. AI Chat Endpoint ✅
- [x] Create `POST /api/ai/chat` - proxy to Anthropic with medical prompting  
- [x] New file: `backend/src/routes/ai.js`

### 5. AI Symptom Analysis ✅
- [x] Create `POST /api/ai/analyze-symptoms` - symptom analysis endpoint
- [x] Update: `backend/src/routes/ai.js`

### 6. AI Lab Report Analysis ✅
- [x] Create `POST /api/ai/analyze-lab-report` - lab report analysis
- [x] Update: `backend/src/routes/ai.js`

### 7. AI Prescription Checker ✅
- [x] Create `POST /api/ai/check-prescription` - drug interaction check
- [x] Update: `backend/src/routes/ai.js`

---

## ✅ COMPLETED - Phase 3: Reviews (MEDIUM)

### 9. Review API ✅
- [x] Create `POST /api/reviews` - create review
- [x] Create `GET /api/reviews/doctor/:id` - get doctor reviews
- [x] New file: `backend/src/routes/reviews.js`

---

## ✅ COMPLETED - Phase 4: Admin & Analytics (MEDIUM)

### 10. Admin Stats ✅
- [x] Create `GET /api/admin/stats` - dashboard statistics
- [x] New file: `backend/src/routes/admin.js`

### 11. Audit Logs ✅
- [x] Create `GET /api/admin/audit-logs` - get audit logs
- [x] Update: `backend/src/routes/admin.js`

### 12. Data Export ✅
- [x] Create `POST /api/admin/export` - export data (CSV/JSON)
- [x] Update: `backend/src/routes/admin.js`

### 13. User Management ✅
- [x] Create `GET /api/admin/users` - list users
- [x] Create `PATCH /api/admin/users/:id` - update user status

---

## 🔜 REMAINING - Payment API (POST-MVP)

### 8. Payment API 🔜
- [ ] Create `POST /api/payments` - create payment
- [ ] Create `POST /api/payments/webhook` - payment callback
- [ ] Create `GET /api/payments/:id` - get payment status
- [ ] New file: `backend/src/routes/payments.js`

---

## Routes Registered in `backend/src/index.js`:

1. `/api/auth` - authRoutes ✅
2. `/api/doctors` - doctorsRoutes ✅
3. `/api/appointments` - appointmentsRoutes ✅
4. `/api/ai` - aiRoutes ✅
5. `/api/reviews` - reviewsRoutes ✅
6. `/api/admin` - adminRoutes ✅
