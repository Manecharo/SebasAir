import React, { useState } from 'react';
import '../App.css';
import useTranslation from '../i18n/useTranslation';

interface FlightFiltersProps {
  onFilterChange: (filters: FilterCriteria) => void;
  registrationOptions?: string[];
}

export interface FilterCriteria {
  registration: string;
  aircraftType: string;
  airline: string;
  status: string;
}

const FlightFilters: React.FC<FlightFiltersProps> = ({ onFilterChange, registrationOptions = [] }) => {
  const { t } = useTranslation();
  const [filters, setFilters] = useState<FilterCriteria>({
    registration: '',
    aircraftType: '',
    airline: '',
    status: ''
  });

  // Aircraft types commonly used in Colombia
  const aircraftTypes = [
    'Piper PA-34-200T Seneca II',
    'Piper PA-34-220T Seneca III',
    'Cessna 414',
    'Rockwell 690A Turbo Commander',
    'Swearingen SA226-AT Merlin IV',
    'Beechcraft C90GTx King Air',
    'Cessna 172',
    'Cessna 182',
    'Cessna 206',
    'Cessna 208 Caravan',
    'Piper PA-28',
    'Piper PA-31',
    'Beechcraft Baron',
    'Beechcraft King Air'
  ];

  // Airlines operating in Colombia
  const airlines = [
    'Avianca',
    'LATAM Colombia',
    'Viva Air Colombia',
    'EasyFly',
    'Satena',
    'Copa Airlines Colombia',
    'Wingo',
    'GCA Airlines',
    'AerCaribe',
    'Searca',
    'Colcharter'
  ];

  // Flight statuses
  const statuses = [
    'EN_ROUTE',
    'SCHEDULED',
    'LANDED',
    'DEPARTED',
    'DIVERTED',
    'CANCELLED',
    'DELAYED',
    'MAINTENANCE'
  ];

  // Map status codes to translated status labels
  const getStatusLabel = (statusCode: string): string => {
    switch (statusCode.toUpperCase()) {
      case 'EN_ROUTE':
        return t('mergedFlightView.statusLabels.enRoute');
      case 'SCHEDULED':
        return t('mergedFlightView.statusLabels.scheduled');
      case 'LANDED':
        return t('mergedFlightView.statusLabels.landed');
      case 'DEPARTED':
        return t('mergedFlightView.statusLabels.departed');
      case 'DIVERTED':
        return t('mergedFlightView.statusLabels.diverted');
      case 'CANCELLED':
        return t('mergedFlightView.statusLabels.cancelled');
      case 'DELAYED':
        return t('mergedFlightView.statusLabels.delayed');
      case 'MAINTENANCE':
        return t('mergedFlightView.statusLabels.maintenance');
      default:
        return statusCode;
    }
  };

  const handleFilterChange = (field: keyof FilterCriteria, value: string) => {
    const updatedFilters = { ...filters, [field]: value };
    setFilters(updatedFilters);
    onFilterChange(updatedFilters);
  };

  const clearFilters = () => {
    const resetFilters = {
      registration: '',
      aircraftType: '',
      airline: '',
      status: ''
    };
    setFilters(resetFilters);
    onFilterChange(resetFilters);
  };

  return (
    <div className="flight-filters">
      <div className="filters-header">
        <h3>{t('flightTracker.filters.title')}</h3>
        <button 
          className="btn-clear-filters" 
          onClick={clearFilters}
          aria-label={t('flightTracker.filters.clearFilters')}
        >
          {t('flightTracker.filters.clearFilters')}
        </button>
      </div>
      
      <div className="filters-grid">
        <div className="filter-group">
          <label htmlFor="registration">{t('flightTracker.filters.registration')}</label>
          <select 
            id="registration" 
            value={filters.registration}
            onChange={(e) => handleFilterChange('registration', e.target.value)}
            aria-label={t('flightTracker.filters.registration')}
          >
            <option value="">{t('flightTracker.filters.allRegistrations')}</option>
            {registrationOptions.length > 0 ? (
              registrationOptions.map(reg => (
                <option key={reg} value={reg}>{reg}</option>
              ))
            ) : (
              <>
                <option value="HK-5020">HK-5020 (Piper Seneca II)</option>
                <option value="HK-2946">HK-2946 (Piper Seneca III)</option>
                <option value="HK-4699">HK-4699 (Piper Seneca III)</option>
                <option value="HK-4714">HK-4714 (Cessna 414)</option>
                <option value="HK-4966">HK-4966 (Rockwell Commander)</option>
                <option value="HK-5225">HK-5225 (Swearingen Merlin IV)</option>
                <option value="HK-5118">HK-5118 (Beechcraft King Air)</option>
              </>
            )}
          </select>
        </div>
        
        <div className="filter-group">
          <label htmlFor="aircraftType">{t('flightTracker.filters.aircraftType')}</label>
          <select 
            id="aircraftType" 
            value={filters.aircraftType}
            onChange={(e) => handleFilterChange('aircraftType', e.target.value)}
            aria-label={t('flightTracker.filters.aircraftType')}
          >
            <option value="">{t('flightTracker.filters.allAircraftTypes')}</option>
            {aircraftTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label htmlFor="airline">{t('flightTracker.filters.airline')}</label>
          <select 
            id="airline" 
            value={filters.airline}
            onChange={(e) => handleFilterChange('airline', e.target.value)}
            aria-label={t('flightTracker.filters.airline')}
          >
            <option value="">{t('flightTracker.filters.allAirlines')}</option>
            {airlines.map(airline => (
              <option key={airline} value={airline}>{airline}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label htmlFor="status">{t('flightTracker.filters.status')}</label>
          <select 
            id="status" 
            value={filters.status}
            onChange={(e) => handleFilterChange('status', e.target.value)}
            aria-label={t('flightTracker.filters.status')}
          >
            <option value="">{t('flightTracker.filters.allStatuses')}</option>
            {statuses.map(status => (
              <option key={status} value={status}>{getStatusLabel(status)}</option>
            ))}
          </select>
        </div>
      </div>
      
      <div className="active-filters">
        {filters.registration && (
          <div className="active-filter">
            <span>{t('flightTracker.filters.registration')}: {filters.registration}</span>
            <button 
              onClick={() => handleFilterChange('registration', '')}
              aria-label={`${t('common.clear')} ${t('flightTracker.filters.registration')}`}
            >
              ×
            </button>
          </div>
        )}
        {filters.aircraftType && (
          <div className="active-filter">
            <span>{t('flightTracker.filters.aircraftType')}: {filters.aircraftType}</span>
            <button 
              onClick={() => handleFilterChange('aircraftType', '')}
              aria-label={`${t('common.clear')} ${t('flightTracker.filters.aircraftType')}`}
            >
              ×
            </button>
          </div>
        )}
        {filters.airline && (
          <div className="active-filter">
            <span>{t('flightTracker.filters.airline')}: {filters.airline}</span>
            <button 
              onClick={() => handleFilterChange('airline', '')}
              aria-label={`${t('common.clear')} ${t('flightTracker.filters.airline')}`}
            >
              ×
            </button>
          </div>
        )}
        {filters.status && (
          <div className="active-filter">
            <span>{t('flightTracker.filters.status')}: {getStatusLabel(filters.status)}</span>
            <button 
              onClick={() => handleFilterChange('status', '')}
              aria-label={`${t('common.clear')} ${t('flightTracker.filters.status')}`}
            >
              ×
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default FlightFilters; 