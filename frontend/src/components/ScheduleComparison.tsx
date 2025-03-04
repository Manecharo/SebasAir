import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import useTranslation from '../i18n/useTranslation';
import AddScheduleForm from './AddScheduleForm';

interface Schedule {
  id: string;
  flightNumber: string;
  origin: string;
  destination: string;
  departureTime: string;
  arrivalTime: string;
  days: string[];
  status: string;
  aircraft: {
    registration: string;
    type: string;
    model: string;
  };
}

const ScheduleComparison: React.FC = () => {
  const { t } = useTranslation();
  const { isAuthenticated } = useAuth();
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dateFilter, setDateFilter] = useState(new Date().toISOString().split('T')[0]);
  const [statusFilter, setStatusFilter] = useState('all');
  const [showAddForm, setShowAddForm] = useState(false);

  const fetchSchedules = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // In a real app, this would be an API call
      // For now, we'll simulate a successful response with mock data
      // const response = await fetch(`http://localhost:8000/api/schedules?date=${dateFilter}&status=${statusFilter}`);
      
      // if (!response.ok) {
      //   throw new Error('Failed to fetch schedules');
      // }
      
      // const data = await response.json();
      
      // Mock data
      const mockSchedules: Schedule[] = [
        {
          id: '1',
          flightNumber: 'COL101',
          origin: 'BOG',
          destination: 'MDE',
          departureTime: '08:00',
          arrivalTime: '09:00',
          days: ['monday', 'wednesday', 'friday'],
          status: 'scheduled',
          aircraft: {
            registration: 'HK-5432',
            type: 'Cessna',
            model: '172'
          }
        },
        {
          id: '2',
          flightNumber: 'COL202',
          origin: 'MDE',
          destination: 'CTG',
          departureTime: '12:00',
          arrivalTime: '13:30',
          days: ['tuesday', 'thursday', 'saturday'],
          status: 'scheduled',
          aircraft: {
            registration: 'HK-1234',
            type: 'Piper',
            model: 'PA-28'
          }
        },
        {
          id: '3',
          flightNumber: 'COL303',
          origin: 'CTG',
          destination: 'BOG',
          departureTime: '16:00',
          arrivalTime: '17:30',
          days: ['sunday'],
          status: 'cancelled',
          aircraft: {
            registration: 'HK-9876',
            type: 'Beechcraft',
            model: 'Baron'
          }
        }
      ];
      
      setSchedules(mockSchedules);
    } catch (err) {
      console.error('Error fetching schedules:', err);
      setError(t('errors.errorLoadingFlights'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSchedules();
  }, [dateFilter, statusFilter, t]);

  const handleDateFilterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDateFilter(e.target.value);
  };

  const handleStatusFilterChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setStatusFilter(e.target.value);
  };

  const handleScheduleAdded = () => {
    // Refresh the schedules list
    fetchSchedules();
    setShowAddForm(false);
  };

  const getDayName = (day: string) => {
    return t(`schedule.${day}`);
  };

  return (
    <div className="schedule-container">
      <div className="schedule-header">
        <div className="title-container">
          <h2 className="schedule-title">{t('schedule.title')}</h2>
        </div>
        <button 
          className="btn-primary btn-add-schedule" 
          onClick={() => setShowAddForm(!showAddForm)}
          aria-label={showAddForm ? t('common.cancel') : t('schedule.addSchedule')}
        >
          {showAddForm ? t('common.cancel') : t('schedule.addSchedule')}
        </button>
      </div>

      {showAddForm && (
        <AddScheduleForm onScheduleAdded={handleScheduleAdded} />
      )}

      <div className="schedule-filters">
        <div className="filter-group">
          <label htmlFor="date-filter">{t('schedule.date')}:</label>
          <input 
            type="date" 
            id="date-filter" 
            value={dateFilter} 
            onChange={handleDateFilterChange}
            className="form-input filter-input"
            aria-label={t('schedule.date')}
          />
        </div>
        
        <div className="filter-group">
          <label htmlFor="status-filter">{t('schedule.status')}:</label>
          <select 
            id="status-filter" 
            value={statusFilter} 
            onChange={handleStatusFilterChange}
            className="form-input filter-input"
            aria-label={t('schedule.status')}
          >
            <option value="all">{t('schedule.allStatus')}</option>
            <option value="scheduled">{t('schedule.scheduled')}</option>
            <option value="in_progress">{t('schedule.inProgress')}</option>
            <option value="completed">{t('schedule.completed')}</option>
            <option value="delayed">{t('schedule.delayed')}</option>
            <option value="cancelled">{t('schedule.cancelled')}</option>
            <option value="diverted">{t('schedule.diverted')}</option>
          </select>
        </div>
        
        <button 
          className="btn-secondary btn-filter" 
          onClick={fetchSchedules}
          aria-label={t('schedule.filterResults')}
        >
          {t('schedule.filterResults')}
        </button>
      </div>

      {loading ? (
        <div className="loading-indicator">{t('common.loading')}</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : (
        <div className="table-container">
          {schedules.length === 0 ? (
            <p className="no-data-message">{t('schedule.noResults')}</p>
          ) : (
            <table className="schedule-table">
              <thead>
                <tr>
                  <th>{t('schedule.flightNumber')}</th>
                  <th>{t('schedule.origin')}</th>
                  <th>{t('schedule.destination')}</th>
                  <th>{t('schedule.departureTime')}</th>
                  <th>{t('schedule.arrivalTime')}</th>
                  <th>{t('schedule.days')}</th>
                  <th>{t('schedule.status')}</th>
                  <th>{t('schedule.aircraft')}</th>
                </tr>
              </thead>
              <tbody>
                {schedules.map(schedule => (
                  <tr key={schedule.id}>
                    <td>{schedule.flightNumber}</td>
                    <td>{schedule.origin}</td>
                    <td>{schedule.destination}</td>
                    <td>{schedule.departureTime}</td>
                    <td>{schedule.arrivalTime}</td>
                    <td>
                      {schedule.days.map(day => getDayName(day)).join(', ')}
                    </td>
                    <td>
                      <span className={`status-badge status-${schedule.status.toLowerCase()}`}>
                        {t(`schedule.${schedule.status.toLowerCase()}`)}
                      </span>
                    </td>
                    <td>{schedule.aircraft.type} {schedule.aircraft.model} ({schedule.aircraft.registration})</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
};

export default ScheduleComparison;
