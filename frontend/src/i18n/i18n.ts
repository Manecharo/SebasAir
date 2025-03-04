import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import esTranslation from './locales/es.json';
import enTranslation from './locales/en.json';

i18n
  // pass the i18n instance to react-i18next
  .use(initReactI18next)
  // detect user language
  .use(LanguageDetector)
  // init i18next
  .init({
    resources: {
      es: {
        translation: esTranslation
      },
      en: {
        translation: enTranslation
      }
    },
    lng: 'es', // Set Spanish as the default language
    fallbackLng: 'es',
    debug: false,
    interpolation: {
      escapeValue: false, // not needed for react as it escapes by default
    }
  });

export default i18n; 