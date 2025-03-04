import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import useTranslation from '../i18n/useTranslation';
import AddCompetitorForm from './AddCompetitorForm';

interface CompetitorStats {
  total_flights: number;
  operators: {
    [key: string]: {
      flights: number;
      percentage: number;
    }
  }
}

interface CompetitorFlight {
  id: string;
  flight_number: string;
  operator: string;
  origin: string;
  destination: string;
  departure_time: string;
  arrival_time: string;
  status: string;
  aircraft: {
    registration: string;
    type: string;
    model: string;
  };
}

const Competitors: React.FC = () => {
  const { t } = useTranslation();
  const { isAuthenticated } = useAuth();
  const [showAddForm, setShowAddForm] = useState(false);
  const [competitorStats, setCompetitorStats] = useState<CompetitorStats | null>(null);
  const [competitorFlights, setCompetitorFlights] = useState<CompetitorFlight[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dateFilter, setDateFilter] = useState(new Date().toISOString().split('T')[0]);

  const fetchCompetitorData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // In a real app, these would be API calls
      // For now, we'll simulate successful responses with mock data
      
      // const flightsResponse = await fetch(`http://localhost:8000/api/competitors/flights?date_str=${dateFilter}`);
      // if (!flightsResponse.ok) {
      //   throw new Error('Failed to fetch competitor flights');
      // }
      // const flightsData = await flightsResponse.json();
      
      // const statsResponse = await fetch(`http://localhost:8000/api/competitors/stats?date_str=${dateFilter}`);
      // if (!statsResponse.ok) {
      //   throw new Error('Failed to fetch competitor stats');
      // }
      // const statsData = await statsResponse.json();
      
      // Mock data
      const mockFlights: CompetitorFlight[] = [
        {
          id: '1',
          flight_number: 'AME101',
          operator: 'AirMed Express',
          origin: 'BOG',
          destination: 'MDE',
          departure_time: '09:00',
          arrival_time: '10:00',
          status: 'completed',
          aircraft: {
            registration: 'HK-5432',
            type: 'Cessna',
            model: 'Citation'
          }
        },
        {
          id: '2',
          flight_number: 'MFS202',
          operator: 'MedFlight Services',
          origin: 'MDE',
          destination: 'CTG',
          departure_time: '13:00',
          arrival_time: '14:30',
          status: 'en_route',
          aircraft: {
            registration: 'HK-9876',
            type: 'Learjet',
            model: '45'
          }
        },
        {
          id: '3',
          flight_number: 'LLA303',
          operator: 'LifeLine Aviation',
          origin: 'CTG',
          destination: 'BOG',
          departure_time: '17:00',
          arrival_time: '18:30',
          status: 'scheduled',
          aircraft: {
            registration: 'HK-1234',
            type: 'Beechcraft',
            model: 'King Air'
          }
        }
      ];
      
      const mockStats: CompetitorStats = {
        total_flights: 10,
        operators: {
          'AirMed Express': { flights: 4, percentage: 40 },
          'MedFlight Services': { flights: 3, percentage: 30 },
          'LifeLine Aviation': { flights: 3, percentage: 30 }
        }
      };
      
      setCompetitorFlights(mockFlights);
      setCompetitorStats(mockStats);
    } catch (err) {
      console.error('Error fetching competitor data:', err);
      setError(t('competitors.errorLoadingCompetitors'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCompetitorData();
  }, [dateFilter, t]);

  const handleDateFilterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDateFilter(e.target.value);
  };

  const handleCompetitorAdded = () => {
    // Refresh the competitor data
    fetchCompetitorData();
    setShowAddForm(false);
  };

  const getStatusClass = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return 'status-completed';
      case 'en_route':
        return 'status-in_progress';
      case 'scheduled':
        return 'status-scheduled';
      case 'cancelled':
        return 'status-cancelled';
      case 'delayed':
        return 'status-delayed';
      case 'diverted':
        return 'status-diverted';
      default:
        return '';
    }
  };

  const getStatusTranslation = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
        return t('schedule.completed');
      case 'en_route':
        return t('schedule.inProgress');
      case 'scheduled':
        return t('schedule.scheduled');
      case 'cancelled':
        return t('schedule.cancelled');
      case 'delayed':
        return t('schedule.delayed');
      case 'diverted':
        return t('schedule.diverted');
      default:
        return status;
    }
  };

  return (
    <div className="competitors-container">
      <div className="competitors-header">
        <div className="title-container">
          <h2 className="competitors-title">{t('competitors.title')}</h2>
        </div>
        <button 
          className="btn-primary btn-add-competitor" 
          onClick={() => setShowAddForm(!showAddForm)}
          aria-label={showAddForm ? t('common.cancel') : t('competitors.addCompetitor')}
        >
          {showAddForm ? t('common.cancel') : t('competitors.addCompetitor')}
        </button>
      </div>

      {showAddForm && (
        <AddCompetitorForm onCompetitorAdded={handleCompetitorAdded} />
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
        
        <button 
          className="btn-secondary btn-filter" 
          onClick={fetchCompetitorData}
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
        <>
          {competitorStats && (
            <div className="competitor-stats">
              <div className="stat-card">
                <h3>{t('competitors.totalFlights')}</h3>
                <div className="stat-value">{competitorStats.total_flights}</div>
                <div className="stat-details">
                  {Object.entries(competitorStats.operators).map(([operator, data]) => (
                    <div key={operator} className="stat-detail">
                      <span>{operator}</span>
                      <span className="status-badge">{data.flights} ({data.percentage}%)</span>
                    </div>
                  ))}
                </div>
              </div>
              
              <div className="stat-card">
                <h3>{t('competitors.totalAircraft')}</h3>
                <div className="stat-value">8</div>
              </div>
              
              <div className="stat-card">
                <h3>{t('competitors.activeCompetitors')}</h3>
                <div className="stat-value">3</div>
              </div>
            </div>
          )}

          <div className="recent-activity">
            <h3>{t('competitors.recentActivity')}</h3>
            {competitorFlights.length === 0 ? (
              <p className="no-data-message">{t('competitors.noRecentActivity')}</p>
            ) : (
              <table className="schedule-table">
                <thead>
                  <tr>
                    <th>{t('schedule.flightNumber')}</th>
                    <th>{t('competitors.company')}</th>
                    <th>{t('schedule.origin')}</th>
                    <th>{t('schedule.destination')}</th>
                    <th>{t('schedule.departureTime')}</th>
                    <th>{t('schedule.arrivalTime')}</th>
                    <th>{t('schedule.status')}</th>
                    <th>{t('schedule.aircraft')}</th>
                  </tr>
                </thead>
                <tbody>
                  {competitorFlights.map(flight => (
                    <tr key={flight.id}>
                      <td>{flight.flight_number}</td>
                      <td>{flight.operator}</td>
                      <td>{flight.origin}</td>
                      <td>{flight.destination}</td>
                      <td>{flight.departure_time}</td>
                      <td>{flight.arrival_time}</td>
                      <td>
                        <span className={`status-badge ${getStatusClass(flight.status)}`}>
                          {getStatusTranslation(flight.status)}
                        </span>
                      </td>
                      <td>{flight.aircraft.type} {flight.aircraft.model} ({flight.aircraft.registration})</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Competitors;
