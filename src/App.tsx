import React, { useState } from 'react';
import NavBar from './components/shared/NavBar';
import HomeView from './features/home/HomeView';
import ChatbotView from './features/chatbot/ChatbotView';
import DoctorsView from './features/doctors/DoctorsView';
import BookingView from './features/booking/BookingView';
import PortalView from './features/portal/PortalView';
import AiClinicalView from './features/ai-clinical/AiClinicalView';
import EtlView from './features/etl/EtlView';
import AdminView from './features/admin/AdminView';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [selectedDoctor, setSelectedDoctor] = useState(null);

  const handleNav = (view: string) => {
    setCurrentView(view);
  };

  const handlePickDoctor = (doctor: any) => {
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
    <div style={{ minHeight: '100vh', backgroundColor: '#f8f9fa' }}>
      <NavBar currentView={currentView} onNav={handleNav} />
      <main>
        {renderCurrentView()}
      </main>
    </div>
  );
}

export default App;