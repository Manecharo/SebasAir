import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import useTranslation from '../i18n/useTranslation';

interface CompetitorFormData {
  name: string;
  code: string;
  website: string;
  notes: string;
}

interface AircraftFormData {
  registration: string;
  type: string;
  model: string;
  competitorId: string;
  notes: string;
}

const AddCompetitorForm: React.FC<{ onCompetitorAdded: () => void }> = ({ onCompetitorAdded }) => {
  const { user } = useAuth();
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [showCompetitorForm, setShowCompetitorForm] = useState(true);
  const [showAircraftForm, setShowAircraftForm] = useState(false);
  const [competitors, setCompetitors] = useState<{ id: string; name: string; code: string }[]>([
    { id: '1', name: 'AirMed Express', code: 'AME' },
    { id: '2', name: 'MedFlight Services', code: 'MFS' },
    { id: '3', name: 'LifeLine Aviation', code: 'LLA' }
  ]);
  
  const [competitorFormData, setCompetitorFormData] = useState<CompetitorFormData>({
    name: '',
    code: '',
    website: '',
    notes: ''
  });
  
  const [aircraftFormData, setAircraftFormData] = useState<AircraftFormData>({
    registration: '',
    type: '',
    model: '',
    competitorId: '',
    notes: ''
  });

  const handleCompetitorInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setCompetitorFormData({
      ...competitorFormData,
      [name]: value
    });
  };
  
  const handleAircraftInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setAircraftFormData({
      ...aircraftFormData,
      [name]: value
    });
  };

  const handleCompetitorSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate form
    if (!competitorFormData.name || !competitorFormData.code) {
      setError(t('forms.required'));
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // In a real app, this would be an API call
      // For now, we'll simulate a successful response
      // const response = await fetch('http://localhost:8000/api/competitors', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(competitorFormData)
      // });
      
      // if (!response.ok) {
      //   throw new Error('Failed to add competitor');
      // }

      // Simulate successful response
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Add the new competitor to the local state
      const newCompetitor = {
        id: (competitors.length + 1).toString(),
        name: competitorFormData.name,
        code: competitorFormData.code
      };
      
      setCompetitors([...competitors, newCompetitor]);
      
      setSuccess(t('competitors.addCompetitorSuccess'));
      
      // Reset form
      setCompetitorFormData({
        name: '',
        code: '',
        website: '',
        notes: ''
      });
      
      // Notify parent component
      onCompetitorAdded();
      
      // Hide success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
      
    } catch (err) {
      console.error('Error adding competitor:', err);
      setError(t('competitors.addCompetitorError'));
    } finally {
      setLoading(false);
    }
  };
  
  const handleAircraftSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate form
    if (!aircraftFormData.registration || !aircraftFormData.type || 
        !aircraftFormData.model || !aircraftFormData.competitorId) {
      setError(t('forms.required'));
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // In a real app, this would be an API call
      // For now, we'll simulate a successful response
      // const response = await fetch('http://localhost:8000/api/competitors/aircraft', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(aircraftFormData)
      // });
      
      // if (!response.ok) {
      //   throw new Error('Failed to add aircraft');
      // }

      // Simulate successful response
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSuccess(t('competitors.addAircraftSuccess'));
      
      // Reset form
      setAircraftFormData({
        registration: '',
        type: '',
        model: '',
        competitorId: '',
        notes: ''
      });
      
      // Notify parent component
      onCompetitorAdded();
      
      // Hide success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
      
    } catch (err) {
      console.error('Error adding aircraft:', err);
      setError(t('competitors.addAircraftError'));
    } finally {
      setLoading(false);
    }
  };

  const toggleForm = (formType: 'competitor' | 'aircraft') => {
    if (formType === 'competitor') {
      setShowCompetitorForm(true);
      setShowAircraftForm(false);
    } else {
      setShowCompetitorForm(false);
      setShowAircraftForm(true);
    }
    setError(null);
    setSuccess(null);
  };

  return (
    <div className="add-competitor-container">
      <div className="form-tabs">
        <button 
          className={`tab-button ${showCompetitorForm ? 'active' : ''}`}
          onClick={() => toggleForm('competitor')}
        >
          {t('competitors.addCompetitor')}
        </button>
        <button 
          className={`tab-button ${showAircraftForm ? 'active' : ''}`}
          onClick={() => toggleForm('aircraft')}
        >
          {t('competitors.addAircraft')}
        </button>
      </div>
      
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
      
      {showCompetitorForm && (
        <form className="add-competitor-form" onSubmit={handleCompetitorSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="name">{t('competitors.company')} *</label>
              <input 
                type="text" 
                id="name" 
                name="name" 
                value={competitorFormData.name}
                onChange={handleCompetitorInputChange}
                placeholder={t('competitors.companyPlaceholder')}
                required
                className="form-input"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="code">{t('common.code')} *</label>
              <input 
                type="text" 
                id="code" 
                name="code" 
                value={competitorFormData.code}
                onChange={handleCompetitorInputChange}
                placeholder={t('competitors.codePlaceholder')}
                required
                className="form-input"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="website">{t('competitors.website')}</label>
              <input 
                type="url" 
                id="website" 
                name="website" 
                value={competitorFormData.website}
                onChange={handleCompetitorInputChange}
                placeholder={t('competitors.websitePlaceholder')}
                className="form-input"
              />
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="notes">{t('common.notes')}</label>
            <textarea 
              id="notes" 
              name="notes" 
              value={competitorFormData.notes}
              onChange={handleCompetitorInputChange}
              placeholder={t('competitors.notesPlaceholder')}
              rows={4}
              className="form-textarea"
            ></textarea>
          </div>
          
          <div className="form-actions">
            <button 
              type="submit" 
              className="btn-primary btn-submit"
              disabled={loading}
            >
              {loading ? t('common.loading') : t('common.save')}
            </button>
            <button 
              type="button" 
              className="btn-secondary btn-cancel"
              onClick={onCompetitorAdded}
              disabled={loading}
            >
              {t('common.cancel')}
            </button>
          </div>
        </form>
      )}
      
      {showAircraftForm && (
        <form className="add-aircraft-form" onSubmit={handleAircraftSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="competitorId">{t('competitors.company')} *</label>
              <select 
                id="competitorId" 
                name="competitorId" 
                value={aircraftFormData.competitorId}
                onChange={handleAircraftInputChange}
                required
                className="form-input"
              >
                <option value="">{t('common.select')}</option>
                {competitors.map(competitor => (
                  <option key={competitor.id} value={competitor.id}>
                    {competitor.name} ({competitor.code})
                  </option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="registration">{t('myFleet.registration')} *</label>
              <input 
                type="text" 
                id="registration" 
                name="registration" 
                value={aircraftFormData.registration}
                onChange={handleAircraftInputChange}
                placeholder={t('myFleet.savedAircraft.registrationPlaceholder')}
                required
                className="form-input"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="type">{t('myFleet.type')} *</label>
              <input 
                type="text" 
                id="type" 
                name="type" 
                value={aircraftFormData.type}
                onChange={handleAircraftInputChange}
                placeholder={t('competitors.aircraftTypePlaceholder')}
                required
                className="form-input"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="model">{t('competitors.model')} *</label>
              <input 
                type="text" 
                id="model" 
                name="model" 
                value={aircraftFormData.model}
                onChange={handleAircraftInputChange}
                placeholder={t('competitors.modelPlaceholder')}
                required
                className="form-input"
              />
            </div>
          </div>
          
          <div className="form-group">
            <label htmlFor="aircraft-notes">{t('common.notes')}</label>
            <textarea 
              id="aircraft-notes" 
              name="notes" 
              value={aircraftFormData.notes}
              onChange={handleAircraftInputChange}
              placeholder={t('competitors.aircraftNotesPlaceholder')}
              rows={4}
              className="form-textarea"
            ></textarea>
          </div>
          
          <div className="form-actions">
            <button 
              type="submit" 
              className="btn-primary btn-submit"
              disabled={loading}
            >
              {loading ? t('common.loading') : t('common.save')}
            </button>
            <button 
              type="button" 
              className="btn-secondary btn-cancel"
              onClick={onCompetitorAdded}
              disabled={loading}
            >
              {t('common.cancel')}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default AddCompetitorForm; 