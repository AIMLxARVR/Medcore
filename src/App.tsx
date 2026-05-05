import React, { useState } from 'react';
import { NavBar } from './components';
import { ErrorBoundary } from './components/ui';
import { Doctor } from './types';
import HomeView from './features/home/HomeView';
import ChatbotView from './features/chatbot/ChatbotView';
import DoctorsView from './features/doctors/DoctorsView';
import BookingView from './features/booking/BookingView';
import PortalView from './features/portal/PortalView';
import AiClinicalView from './features/ai-clinical/AiClinicalView';
import EtlView from './features/etl/EtlView';
import AdminView from './features/admin/AdminView';

// View type for navigation
type ViewName = 'home' | 'doctors' | 'booking' | 'chatbot' | 'ai-clinical' | 'etl' | 'portal' | 'admin';

function App() {
  const [selectedDoctor, setSelectedDoctor] = useState<Doctor | null>(null);

  const handleNav = (view: string) => {
    setCurrentView(view as ViewName);
  };

  const handlePickDoctor = (doctor: Doctor) => {
    setSelectedDoctor(doctor);
  };

  // State-based routing
  const [currentView, setCurrentView] = useState<ViewName>('home');

  const renderCurrentView = () => {
    switch (currentView) {
case 'home':
        return <HomeView onNav={handleNav} onPick={handlePickDoctor} />;
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
        return <HomeView onNav={handleNav} onPick={handlePickDoctor} />;
    }
  };

return (
    <div className="app-container">
      <NavBar view={currentView} onNav={handleNav} />
      <main className="app-main">
        <ErrorBoundary>
          {renderCurrentView()}
        </ErrorBoundary>
      </main>
    </div>
  );
}

export default App;
