# MedCore Refactoring Workflow

This document outlines the plan to refactor the `Medcore.tsx` file into a more scalable and maintainable file structure.

## 1. Create Directory Structure

- Create the following directories:
  - `src/assets`
  - `src/components/ui`
  - `src/components/shared`
  - `src/constants`
  - `src/features` (with subdirectories for each view)
  - `src/hooks`
  - `src/services`
  - `src/styles`
  - `src/types`

## 2. Isolate UI Components

- Move the following components from `Medcore.tsx` to their own files in `src/components/ui/`:
  - `Avatar.tsx`
  - `Badge.tsx`
  - `Button.tsx`
  - `Card.tsx`
  - `StatusBadge.tsx`
- Create an `index.ts` in `src/components/ui/` to export all components.

## 3. Separate Constants

- Move constant data from `Medcore.tsx` into the following files in `src/constants/`:
  - `colors.ts`
  - `data.ts`
  - `prompts.ts`

## 4. Structure Feature Views

- Move the main application views from `Medcore.tsx` to their own files in `src/features/`:
  - `src/features/home/HomeView.tsx`
  - `src/features/doctors/DoctorsView.tsx`
  - `src/features/chatbot/ChatbotView.tsx`
  - `src/features/portal/PortalView.tsx`
  - `src/features/ai-clinical/AiClinicalView.tsx`
  - `src/features/etl/EtlView.tsx`
  - `src/features/admin/AdminView.tsx`
  - `src/features/booking/BookingView.tsx`

## 5. Extract Shared Logic

- Create a custom hook `src/hooks/useChat.ts` to handle the chatbot's logic.
- Create a service file `src/services/anthropic.ts` for the API call.

## 6. Assemble the Main App

- Create `src/App.tsx` to manage application state and routing.
- Create `src/index.tsx` as the application's entry point.