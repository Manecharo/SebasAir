import React from 'react';
import { useTranslation } from 'react-i18next';
import '../App.css';

const LanguageSwitcher: React.FC = () => {
  const { i18n } = useTranslation();
  
  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };
  
  return (
    <div className="language-switcher">
      <button 
        className={`language-btn ${i18n.language === 'en' ? 'active' : ''}`}
        onClick={() => changeLanguage('en')}
      >
        EN
      </button>
      <button 
        className={`language-btn ${i18n.language === 'es' ? 'active' : ''}`}
        onClick={() => changeLanguage('es')}
      >
        ES
      </button>
    </div>
  );
};

export default LanguageSwitcher; 