import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import useTranslation from '../i18n/useTranslation';

interface Aircraft {
  id: string;
  registration: string;
  type: string;
  model: string;
}

interface ScheduleFormData {
  aircraftId: string;
  flightNumber: string;
  origin: string;
  destination: string;
  departureTime: string;
  arrivalTime: string;
  days: string[];
  startDate: string;
  endDate: string;
  status: string;
}

const AddScheduleForm: React.FC<{ onScheduleAdded: () => void }> = ({ onScheduleAdded }) => {
  const { user } = useAuth();
  const { t } = useTranslation();
  const [aircraft, setAircraft] = useState<Aircraft[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  
  const [formData, setFormData] = useState<ScheduleFormData>({
    aircraftId: '',
    flightNumber: '',
    origin: '',
    destination: '',
    departureTime: '',
    arrivalTime: '',
    days: [],
    startDate: '',
    endDate: '',
    status: 'scheduled'
  });

  useEffect(() => {
    // Fetch aircraft from the fleet
    const fetchAircraft = async () => {
      try {
        setLoading(true);
        // In a real app, this would be an API call
        // For now, we'll use mock data
        const response = await fetch('http://localhost:8000/api/fleet/aircraft');
        if (response.ok) {
          const data = await response.json();
          setAircraft(data);
        } else {
          // Mock data if API fails
          setAircraft([
            { id: '1', registration: 'HK-5432', type: 'Cessna', model: '172' },
            { id: '2', registration: 'HK-1234', type: 'Piper', model: 'PA-28' },
            { id: '3', registration: 'HK-9876', type: 'Beechcraft', model: 'Baron' }
          ]);
        }
      } catch (err) {
        console.error('Error fetching aircraft:', err);
        // Mock data if API fails
        setAircraft([
          { id: '1', registration: 'HK-5432', type: 'Cessna', model: '172' },
          { id: '2', registration: 'HK-1234', type: 'Piper', model: 'PA-28' },
          { id: '3', registration: 'HK-9876', type: 'Beechcraft', model: 'Baron' }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchAircraft();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleDayChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value, checked } = e.target;
    if (checked) {
      setFormData({
        ...formData,
        days: [...formData.days, value]
      });
    } else {
      setFormData({
        ...formData,
        days: formData.days.filter(day => day !== value)
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate form
    if (!formData.aircraftId || !formData.flightNumber || !formData.origin || 
        !formData.destination || !formData.departureTime || !formData.arrivalTime || 
        formData.days.length === 0 || !formData.startDate || !formData.endDate) {
      setError(t('forms.required'));
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // In a real app, this would be an API call
      // For now, we'll simulate a successful response
      // const response = await fetch('http://localhost:8000/api/schedules', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify(formData)
      // });
      
      // if (!response.ok) {
      //   throw new Error('Failed to add schedule');
      // }

      // Simulate successful response
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setSuccess(t('schedule.addFlightSuccess'));
      
      // Reset form
      setFormData({
        aircraftId: '',
        flightNumber: '',
        origin: '',
        destination: '',
        departureTime: '',
        arrivalTime: '',
        days: [],
        startDate: '',
        endDate: '',
        status: 'scheduled'
      });
      
      // Notify parent component
      onScheduleAdded();
      
      // Hide success message after 3 seconds
      setTimeout(() => {
        setSuccess(null);
      }, 3000);
      
    } catch (err) {
      console.error('Error adding schedule:', err);
      setError(t('schedule.addFlightError'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="add-schedule-container">
      <h3 className="form-title">{t('schedule.addSchedule')}</h3>
      
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
      
      <form className="add-schedule-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="aircraftId">{t('schedule.aircraft')} *</label>
            <select 
              id="aircraftId" 
              name="aircraftId" 
              value={formData.aircraftId}
              onChange={handleInputChange}
              required
              className="form-input"
              aria-label={t('schedule.selectAircraft')}
            >
              <option value="">{t('schedule.selectAircraft')}</option>
              {aircraft.map(aircraft => (
                <option key={aircraft.id} value={aircraft.id}>
                  {aircraft.registration} - {aircraft.type} {aircraft.model}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="flightNumber">{t('schedule.flightNumber')} *</label>
            <input 
              type="text" 
              id="flightNumber" 
              name="flightNumber" 
              value={formData.flightNumber}
              onChange={handleInputChange}
              placeholder={t('schedule.flightNumberPlaceholder')}
              required
              className="form-input"
              aria-label={t('schedule.flightNumber')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="origin">{t('schedule.origin')} *</label>
            <input 
              type="text" 
              id="origin" 
              name="origin" 
              value={formData.origin}
              onChange={handleInputChange}
              placeholder={t('schedule.originPlaceholder')}
              required
              className="form-input"
              aria-label={t('schedule.origin')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="destination">{t('schedule.destination')} *</label>
            <input 
              type="text" 
              id="destination" 
              name="destination" 
              value={formData.destination}
              onChange={handleInputChange}
              placeholder={t('schedule.destinationPlaceholder')}
              required
              className="form-input"
              aria-label={t('schedule.destination')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="departureTime">{t('schedule.departureTime')} *</label>
            <input 
              type="time" 
              id="departureTime" 
              name="departureTime" 
              value={formData.departureTime}
              onChange={handleInputChange}
              required
              className="form-input"
              aria-label={t('schedule.departureTime')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="arrivalTime">{t('schedule.arrivalTime')} *</label>
            <input 
              type="time" 
              id="arrivalTime" 
              name="arrivalTime" 
              value={formData.arrivalTime}
              onChange={handleInputChange}
              required
              className="form-input"
              aria-label={t('schedule.arrivalTime')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="startDate">{t('reports.startDate')} *</label>
            <input 
              type="date" 
              id="startDate" 
              name="startDate" 
              value={formData.startDate}
              onChange={handleInputChange}
              required
              className="form-input"
              aria-label={t('reports.startDate')}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="endDate">{t('reports.endDate')} *</label>
            <input 
              type="date" 
              id="endDate" 
              name="endDate" 
              value={formData.endDate}
              onChange={handleInputChange}
              required
              className="form-input"
              aria-label={t('reports.endDate')}
            />
          </div>
        </div>
        
        <div className="form-group days-group">
          <label>{t('schedule.days')} *</label>
          <div className="days-checkboxes">
            <div className="day-checkbox">
              <input 
                type="checkbox" 
                id="monday" 
                name="days" 
                value="monday"
                checked={formData.days.includes('monday')}
                onChange={handleDayChange}
                aria-label={t('schedule.monday')}
              />
              <label htmlFor="monday">{t('schedule.monday')}</label>
            </div>
            
            <div className="day-checkbox">
              <input 
                type="checkbox" 
                id="tuesday" 
                name="days" 
                value="tuesday"
                checked={formData.days.includes('tuesday')}
                onChange={handleDayChange}
                aria-label={t('schedule.tuesday')}
              />
              <label htmlFor="tuesday">{t('schedule.tuesday')}</label>
            </div>
            
            <div className="day-checkbox">
              <input 
                type="checkbox" 
                id="wednesday" 
                name="days" 
                value="wednesday"
                checked={formData.days.includes('wednesday')}
                onChange={handleDayChange}
                aria-label={t('schedule.wednesday')}
              />
              <label htmlFor="wednesday">{t('schedule.wednesday')}</label>
            </div>
            
            <div className="day-checkbox">
              <input 
                type="checkbox" 
                id="thursday" 
                name="days" 
                value="thursday"
                checked={formData.days.includes('thursday')}
                onChange={handleDayChange}
                aria-label={t('schedule.thursday')}
              />
              <label htmlFor="thursday">{t('schedule.thursday')}</label>
            </div>
            
            <div className="day-checkbox">
              <input 
                type="checkbox" 
                id="friday" 
                name="days" 
                value="friday"
                checked={formData.days.includes('friday')}
                onChange={handleDayChange}
                aria-label={t('schedule.friday')}
              />
              <label htmlFor="friday">{t('schedule.friday')}</label>
            </div>
            
            <div className="day-checkbox">
              <input 
                type="checkbox" 
                id="saturday" 
                name="days" 
                value="saturday"
                checked={formData.days.includes('saturday')}
                onChange={handleDayChange}
                aria-label={t('schedule.saturday')}
              />
              <label htmlFor="saturday">{t('schedule.saturday')}</label>
            </div>
            
            <div className="day-checkbox">
              <input 
                type="checkbox" 
                id="sunday" 
                name="days" 
                value="sunday"
                checked={formData.days.includes('sunday')}
                onChange={handleDayChange}
                aria-label={t('schedule.sunday')}
              />
              <label htmlFor="sunday">{t('schedule.sunday')}</label>
            </div>
          </div>
        </div>
        
        <div className="form-group">
          <label htmlFor="status">{t('schedule.status')}</label>
          <select 
            id="status" 
            name="status" 
            value={formData.status}
            onChange={handleInputChange}
            className="form-input"
            aria-label={t('schedule.status')}
          >
            <option value="active">{t('schedule.active')}</option>
            <option value="inactive">{t('schedule.inactive')}</option>
            <option value="pending">{t('schedule.pending')}</option>
          </select>
        </div>
        
        <div className="form-actions">
          <button 
            type="submit" 
            className="btn-primary btn-submit"
            disabled={loading}
            aria-label={loading ? t('common.loading') : t('common.save')}
          >
            {loading ? t('common.loading') : t('common.save')}
          </button>
          <button 
            type="button" 
            className="btn-secondary btn-cancel"
            onClick={onScheduleAdded}
            disabled={loading}
            aria-label={t('common.cancel')}
          >
            {t('common.cancel')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddScheduleForm; 