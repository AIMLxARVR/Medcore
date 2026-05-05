import React from 'react';
import { Stethoscope } from 'lucide-react';
import styles from './NavBar.module.css';
import { ViewType } from '../../types';

interface NavBarProps {
  view: ViewType;
  onNav: (view: ViewType) => void;
}

interface Tab {
  k: ViewType;
  l: string;
}

function NavBar({ view, onNav }: NavBarProps) {
  const tabs: Tab[] = [
    { k: "home", l: "Home" },
    { k: "doctors", l: "Doctors" },
    { k: "chatbot", l: "AI Chatbot" },
    { k: "portal", l: "My Portal" },
    { k: "ai-clinical", l: "AI Clinical" },
    { k: "etl", l: "ETL Hub" },
    { k: "admin", l: "Admin" }
  ];

  return (
    <nav className={styles.nav}>
      <div className={styles.container}>
        <div className={styles.logo} onClick={() => onNav("home")}>
          <div className={styles.logoIcon}>
            <Stethoscope size={14} color="#fff" />
          </div>
          <div>
            <div className={styles.logoText}>MedCore</div>
            <div className={styles.logoSubtitle}>AI-ENHANCED MVP</div>
          </div>
        </div>
        {tabs.map(({ k, l }) => (
          <button
            key={k}
            onClick={() => onNav(k)}
            className={`${styles.navButton} ${view === k ? styles.active : ''}`}
          >
            {l}
          </button>
        ))}
        <div className={styles.statusIndicator}>
          <div className={styles.statusDot} />
          <span className={styles.statusText}>LIVE</span>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
