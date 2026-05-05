import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { NavBar } from './components';
import { ViewType, Doctor } from './types';
import HomeView from './features/home/HomeView';
import ChatbotView from './features/chatbot/ChatbotView';
import DoctorsView from './features/doctors/DoctorsView';
import BookingView from './features/booking/BookingView';
import PortalView from './features/portal/PortalView';
import AiClinicalView from './features/ai-clinical/AiClinicalView';
import EtlView from './features/etl/EtlView';
import AdminView from './features/admin/AdminView';

// Page wrapper components for React Router
// These translate between old state-based navigation and new URL-based routing
function HomePage() {
  const [view, setView] = useState<ViewType>('home');
  return <HomeView onNav={(v: ViewType) => setView(v)} />;
}

function DoctorsPage() {
  const [view, setView] = useState<ViewType>('doctors');
  const [doctor, setDoctor] = useState<Doctor | null>(null);
  return <DoctorsView onNav={(v: ViewType) => setView(v)} onPick={setDoctor} />;
}

function BookingPage({ doctor }: { doctor: Doctor | null }) {
  const [view, setView] = useState<ViewType>('booking');
  return <BookingView doctor={doctor} onNav={(v: ViewType) => setView(v)} />;
}

function App() {
  const [selectedDoctor, setSelectedDoctor] = useState<Doctor | null>(null);

  const handleNav = (view: ViewType) => {
    setCurrentView(view);
  };

  const handlePickDoctor = (doctor: Doctor) => {
    setSelectedDoctor(doctor);
  };

  // Legacy state-based routing (backward compatible)
  const [currentView, setCurrentView] = useState<ViewType>('home');

  const renderCurrentView = () => {
    switch (currentView) {
      case 'home':
        return <HomeView onNav={handleNav} />;
      case 'chatbot':
        return <ChatbotView />;
      case 'doctors':
        return <DoctorsView onNav={handleNav} onPick={handlePickDoctor} />;
      case 'booking':
        return <BookingView doctor={selectedDoctor} onNav={handleNav} />;
      case 'portal':
        return <PortalView onNav={handleNav} />;
      case 'ai-clinical':
        return <AiClinicalView onNav={handleNav} />;
      case 'etl':
        return <EtlView onNav={handleNav} />;
      case 'admin':
        return <AdminView onNav={handleNav} />;
      default:
        return <HomeView onNav={handleNav} />;
    }
  };

  return (
    <BrowserRouter>
      <div className="app-container">
        {/* Keep existing NavBar for backward compatibility */}
        <NavBar view={currentView} onNav={handleNav} />
        <main className="app-main">
          {renderCurrentView()}
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
