import React, { useState } from 'react';
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

function App() {
  const [currentView, setCurrentView] = useState<ViewType>('home');
  const [selectedDoctor, setSelectedDoctor] = useState<Doctor | null>(null);

  const handleNav = (view: ViewType) => {
    setCurrentView(view);
  };

  const handlePickDoctor = (doctor: Doctor) => {
    setSelectedDoctor(doctor);
  };

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
    <div className="app-container">
      <NavBar view={currentView} onNav={handleNav} />
      <main className="app-main">
        {renderCurrentView()}
      </main>
    </div>
  );
}

export default App;