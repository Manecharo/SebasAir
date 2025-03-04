import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../App.css';
import useTranslation from '../i18n/useTranslation';

interface FlightHistoryProps {
  flightId?: string;
  registration?: string;
}

interface HistoryEntry {
  date: string;
  flight_id: string;
  origin: string;
  destination: string;
  departure_time: string;
  arrival_time: string;
  status: string;
  duration: string;
}

const FlightHistory: React.FC<FlightHistoryProps> = ({ flightId, registration }) => {
  const { t } = useTranslation();
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      if (!flightId && !registration) {
        setHistory([]);
        return;
      }

      setLoading(true);
      setError(null);

      try {
        // In a real application, this would call your backend API
        // For now, we'll generate mock data
        
        // Mock data generation
        const mockHistory: HistoryEntry[] = [];
        const today = new Date();
        
        // Generate history for the past 30 days
        for (let i = 0; i < 30; i++) {
          const date = new Date(today);
          date.setDate(date.getDate() - i);
          
          // Skip some days randomly
          if (Math.random() > 0.7) continue;
          
          const departureTime = new Date(date);
          departureTime.setHours(Math.floor(Math.random() * 12) + 6); // Between 6 AM and 6 PM
          
          const durationHours = Math.floor(Math.random() * 3) + 1; // 1-3 hours
          const durationMinutes = Math.floor(Math.random() * 60);
          
          const arrivalTime = new Date(departureTime);
          arrivalTime.setHours(arrivalTime.getHours() + durationHours);
          arrivalTime.setMinutes(arrivalTime.getMinutes() + durationMinutes);
          
          // Random origin and destination
          const airports = ['BOG', 'MDE', 'CLO', 'CTG', 'BAQ', 'ADZ', 'PEI', 'BGA'];
          const origin = airports[Math.floor(Math.random() * airports.length)];
          let destination;
          do {
            destination = airports[Math.floor(Math.random() * airports.length)];
          } while (destination === origin);
          
          // Random status
          const statuses = ['COMPLETED', 'CANCELLED', 'DIVERTED', 'DELAYED', 'ON_TIME'];
          const status = statuses[Math.floor(Math.random() * statuses.length)];
          
          mockHistory.push({
            date: date.toISOString().split('T')[0],
            flight_id: flightId || `COL${Math.floor(Math.random() * 1000)}`,
            origin,
            destination,
            departure_time: departureTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            arrival_time: arrivalTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            status,
            duration: `${durationHours}h ${durationMinutes}m`
          });
        }
        
        // Sort by date (newest first)
        mockHistory.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
        
        setHistory(mockHistory);
      } catch (err) {
        console.error('Error fetching flight history:', err);
        setError(t('flightTracker.history.errorLoadingHistory'));
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [flightId, registration, t]);

  // Function to get the translated status label
  const getStatusLabel = (statusCode: string): string => {
    switch (statusCode.toUpperCase()) {
      case 'COMPLETED':
        return t('schedule.completed');
      case 'CANCELLED':
        return t('schedule.cancelled');
      case 'DIVERTED':
        return t('schedule.diverted');
      case 'DELAYED':
        return t('schedule.delayed');
      case 'ON_TIME':
        return t('flightTracker.status.onTime');
      default:
        return statusCode;
    }
  };

  if (loading) {
    return <div className="loading-indicator">{t('flightTracker.history.loadingHistory')}</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (history.length === 0) {
    return <div className="no-data-message">{t('flightTracker.history.noHistory')}</div>;
  }

  return (
    <div className="flight-history">
      <h3>{t('flightTracker.history.title')}</h3>
      <p className="history-info">
        {flightId ? 
          `${t('flightTracker.history.flight')}: ${flightId}` : 
          registration ? 
          `${t('flightTracker.registration')}: ${registration}` : 
          ''
        }
      </p>
      
      <div className="table-responsive">
        <table className="history-table">
          <thead>
            <tr>
              <th>{t('flightTracker.history.date')}</th>
              <th>{t('flightTracker.history.flight')}</th>
              <th>{t('flightTracker.history.route')}</th>
              <th>{t('flightTracker.history.departure')}</th>
              <th>{t('flightTracker.history.arrival')}</th>
              <th>{t('flightTracker.history.duration')}</th>
              <th>{t('flightTracker.history.status')}</th>
            </tr>
          </thead>
          <tbody>
            {history.map((entry, index) => (
              <tr key={`${entry.date}-${index}`}>
                <td>{entry.date}</td>
                <td>{entry.flight_id}</td>
                <td>{entry.origin} → {entry.destination}</td>
                <td>{entry.departure_time}</td>
                <td>{entry.arrival_time}</td>
                <td>{entry.duration}</td>
                <td>
                  <span className={`status-badge status-${entry.status.toLowerCase()}`}>
                    {getStatusLabel(entry.status)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FlightHistory; 