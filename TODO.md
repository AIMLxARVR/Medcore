# TODO - RBAC/ABAC Panels Implementation

## Phase 1: Update Types
- [ ] Add UserRole type (PATIENT, DOCTOR, ADMIN, STAFF)
- [ ] Add Permission types
- [ ] Add Inventory types
- [ ] Add Review types

## Phase 2: Enhance Admin Panel
- [ ] Add Users Management with sub-tabs (Doctors, Staffs, Patients)
- [ ] Add Inventory (Pharma) management panel
- [ ] Add Reviews/Ratings Analysis dashboard

## Phase 3: Create Doctor Dashboard
- [ ] Create src/features/doctors/DoctorDashboard.tsx
- [ ] Add patient management
- [ ] Add appointments management
- [ ] Add medical records access
- [ ] Add prescription management
- [ ] Add reviews from patients

## Phase 4: Create Patient Portal
- [ ] Create src/features/patients/PatientPortal.tsx
- [ ] Add my appointments view
- [ ] Add my medical records view
- [ ] Add book appointment feature
- [ ] Add prescriptions/refills

## Phase 5: Update Navigation
- [ ] Update NavBar for role-based navigation
- [ ] Update App.tsx routing
- [ ] Add auth context/state for role

## Phase 6: Testing
- [ ] Verify navigation works
- [ ] Verify role-based views display correctly
