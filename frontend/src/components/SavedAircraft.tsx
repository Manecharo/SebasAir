import React, { useState, useEffect } from 'react';
import '../App.css';
import useTranslation from '../i18n/useTranslation';

interface Aircraft {
  registration: string;
  type: string;
  notes?: string;
}

interface SavedAircraftProps {
  onSelectAircraft: (registration: string) => void;
}

const SavedAircraft: React.FC<SavedAircraftProps> = ({ onSelectAircraft }) => {
  const { t } = useTranslation();
  const [savedAircraft, setSavedAircraft] = useState<Aircraft[]>([]);
  const [newAircraft, setNewAircraft] = useState<Aircraft>({ registration: '', type: '', notes: '' });
  const [isAddingNew, setIsAddingNew] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(true);

  // Load saved aircraft from localStorage on component mount
  useEffect(() => {
    const savedData = localStorage.getItem('savedAircraft');
    if (savedData) {
      try {
        const parsed = JSON.parse(savedData);
        setSavedAircraft(parsed);
      } catch (err) {
        console.error('Error parsing saved aircraft data:', err);
      }
    } else {
      // Add default aircraft if none are saved
      const defaultAircraft: Aircraft[] = [
        { registration: 'HK-5020', type: 'Piper PA-34-200T Seneca II', notes: 'Colcharter' },
        { registration: 'HK-2946', type: 'Piper PA-34-220T Seneca III', notes: 'Colcharter' },
        { registration: 'HK-4699', type: 'Piper PA-34-220T Seneca III', notes: 'Colcharter' },
        { registration: 'HK-4714', type: 'Cessna 414', notes: 'Colcharter' },
        { registration: 'HK-4966', type: 'Rockwell 690A Turbo Commander', notes: 'Colcharter' },
        { registration: 'HK-5225', type: 'Swearingen SA226-AT Merlin IV', notes: 'Colcharter' },
        { registration: 'HK-5118', type: 'Beechcraft C90GTx King Air', notes: 'Colcharter' }
      ];
      setSavedAircraft(defaultAircraft);
      localStorage.setItem('savedAircraft', JSON.stringify(defaultAircraft));
    }
  }, []);

  // Save aircraft to localStorage whenever the list changes
  useEffect(() => {
    if (savedAircraft.length > 0) {
      localStorage.setItem('savedAircraft', JSON.stringify(savedAircraft));
    }
  }, [savedAircraft]);

  const handleAddAircraft = () => {
    setError(null);
    
    // Validate input
    if (!newAircraft.registration.trim() || !newAircraft.type.trim()) {
      setError(t('myFleet.savedAircraft.registrationRequired'));
      return;
    }
    
    // Check for duplicate registration
    if (savedAircraft.some(aircraft => aircraft.registration === newAircraft.registration)) {
      setError(t('myFleet.savedAircraft.duplicateRegistration'));
      return;
    }
    
    // Add new aircraft to the list
    setSavedAircraft([...savedAircraft, newAircraft]);
    
    // Reset form
    setNewAircraft({ registration: '', type: '', notes: '' });
    setIsAddingNew(false);
  };

  const handleRemoveAircraft = (registration: string) => {
    setSavedAircraft(savedAircraft.filter(aircraft => aircraft.registration !== registration));
  };

  const handleSelectAircraft = (registration: string) => {
    onSelectAircraft(registration);
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="saved-aircraft">
      <div className="saved-aircraft-header">
        <div className="header-title-container">
          <h3>{t('myFleet.savedAircraft.title')}</h3>
          <button 
            className="btn-toggle-expand"
            onClick={toggleExpand}
            aria-label={isExpanded ? 'Collapse' : 'Expand'}
          >
            {isExpanded ? '▼' : '►'}
          </button>
        </div>
        {!isAddingNew && isExpanded && (
          <button 
            className="btn-add-aircraft"
            onClick={() => setIsAddingNew(true)}
          >
            {t('myFleet.savedAircraft.addNew')}
          </button>
        )}
      </div>
      
      {isExpanded && (
        <>
          {error && <div className="error-message">{error}</div>}
          
          {isAddingNew && (
            <div className="add-aircraft-form">
              <div className="form-group">
                <label htmlFor="registration">{t('myFleet.savedAircraft.registration')}</label>
                <input
                  type="text"
                  id="registration"
                  value={newAircraft.registration}
                  onChange={(e) => setNewAircraft({...newAircraft, registration: e.target.value})}
                  placeholder={t('myFleet.savedAircraft.registrationPlaceholder')}
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="type">{t('myFleet.savedAircraft.type')}</label>
                <input
                  type="text"
                  id="type"
                  value={newAircraft.type}
                  onChange={(e) => setNewAircraft({...newAircraft, type: e.target.value})}
                  placeholder={t('myFleet.savedAircraft.typePlaceholder')}
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="notes">{t('myFleet.savedAircraft.notesOptional')}</label>
                <input
                  type="text"
                  id="notes"
                  value={newAircraft.notes || ''}
                  onChange={(e) => setNewAircraft({...newAircraft, notes: e.target.value})}
                  placeholder={t('myFleet.savedAircraft.notesPlaceholder')}
                />
              </div>
              
              <div className="form-actions">
                <button 
                  className="btn-save"
                  onClick={handleAddAircraft}
                >
                  {t('myFleet.savedAircraft.save')}
                </button>
                <button 
                  className="btn-cancel"
                  onClick={() => {
                    setIsAddingNew(false);
                    setNewAircraft({ registration: '', type: '', notes: '' });
                    setError(null);
                  }}
                >
                  {t('myFleet.savedAircraft.cancel')}
                </button>
              </div>
            </div>
          )}
          
          <div className="aircraft-list-container">
            {savedAircraft.length === 0 ? (
              <p className="no-aircraft">{t('myFleet.savedAircraft.noAircraft')}</p>
            ) : (
              <div className="saved-aircraft-list">
                {savedAircraft.map((aircraft) => (
                  <div key={aircraft.registration} className="saved-aircraft-item">
                    <div className="aircraft-info">
                      <h4>{aircraft.registration}</h4>
                      <p>{aircraft.type}</p>
                      {aircraft.notes && <p className="aircraft-notes">{aircraft.notes}</p>}
                    </div>
                    <div className="aircraft-actions">
                      <button 
                        className="btn-track"
                        onClick={() => handleSelectAircraft(aircraft.registration)}
                      >
                        {t('myFleet.savedAircraft.track')}
                      </button>
                      <button 
                        className="btn-remove"
                        onClick={() => handleRemoveAircraft(aircraft.registration)}
                      >
                        {t('myFleet.savedAircraft.remove')}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default SavedAircraft; 