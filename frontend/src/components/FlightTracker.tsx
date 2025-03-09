import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import useTranslation from '../i18n/useTranslation';
import '../App.css';
import FlightFilters, { FilterCriteria } from './FlightFilters';
import SavedAircraft from './SavedAircraft';
import FlightHistory from './FlightHistory';

// Fix for the default icon issue in Leaflet with React
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

// Create custom icons for different flight statuses
const activeIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  className: 'active-flight-icon',
});

const delayedIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  className: 'delayed-flight-icon',
});

L.Marker.prototype.options.icon = DefaultIcon;

interface Flight {
  flight_id: string;
  callsign: string;
  tail_number: string;
  aircraft_type: string;
  airline: string;
  origin: string;
  destination: string;
  status: string;
  latitude: number;
  longitude: number;
  altitude: number;
  speed: number;
  heading: number;
}

interface FlightDetails extends Flight {
  origin_name: string;
  origin_city: string;
  destination_name: string;
  destination_city: string;
  estimated_time_enroute: string;
  distance: number;
}

interface FilterCriteria {
  registration?: string;
  aircraftType?: string;
  airline?: string;
  status?: string;
  origin?: string;
  destination?: string;
}

// Component to fly to a selected flight
const FlyToMarker = ({ flight }: { flight: Flight | null }) => {
  const map = useMap();
  
  useEffect(() => {
    if (flight && flight.latitude && flight.longitude) {
      map.flyTo([flight.latitude, flight.longitude], 8, {
        animate: true,
        duration: 1.5
      });
    }
  }, [flight, map]);
  
  return null;
};

const FlightTracker: React.FC = () => {
  const { t } = useTranslation();
  const [flights, setFlights] = useState<Flight[]>([]);
  const [filteredFlights, setFilteredFlights] = useState<Flight[]>([]);
  const [selectedFlight, setSelectedFlight] = useState<Flight | null>(null);
  const [selectedFlightDetails, setSelectedFlightDetails] = useState<FlightDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [dataSource, setDataSource] = useState<string>('mock');
  const [showHistory, setShowHistory] = useState(false);
  const [filters, setFilters] = useState<FilterCriteria>({
    airline: '',
    origin: '',
    destination: '',
    status: '',
    registration: ''
  });

  // Fetch flights data
  useEffect(() => {
    const fetchFlights = async () => {
      try {
        setLoading(true);
        const response = await axios.get<Flight[]>('http://localhost:8000/flight-data/live-flights');
        setFlights(response.data);
        setLastUpdate(new Date());
        setError(null);
      } catch (err) {
        console.error('Error fetching flights:', err);
        setError('Failed to fetch flight data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    const fetchDataSource = async () => {
      try {
        const response = await axios.get('http://localhost:8000/flight-data/data-source');
        setDataSource(response.data.using_real_data ? 'live' : 'mock');
      } catch (err) {
        console.error('Error fetching data source:', err);
      }
    };

    fetchFlights();
    fetchDataSource();

    // Refresh data every 30 seconds
    const interval = setInterval(() => {
      fetchFlights();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  // Apply filters to flights
  useEffect(() => {
    let result = [...flights];
    
    if (filters.registration) {
      result = result.filter(flight => 
        flight.tail_number?.toLowerCase().includes(filters.registration.toLowerCase())
      );
    }
    
    if (filters.aircraftType) {
      result = result.filter(flight => 
        flight.aircraft_type?.toLowerCase().includes(filters.aircraftType.toLowerCase())
      );
    }
    
    if (filters.airline) {
      result = result.filter(flight => 
        flight.airline?.toLowerCase().includes(filters.airline.toLowerCase())
      );
    }
    
    if (filters.status) {
      result = result.filter(flight => 
        flight.status?.toLowerCase() === filters.status.toLowerCase()
      );
    }
    
    setFilteredFlights(result);
  }, [flights, filters]);

  // Extract unique registration numbers for filter dropdown
  const registrationOptions = useMemo(() => {
    const registrations = flights
      .map(flight => flight.tail_number)
      .filter((reg): reg is string => !!reg);
    return [...new Set(registrations)].sort();
  }, [flights]);

  // Fetch flight details when a flight is selected
  const handleFlightSelect = async (flightId: string) => {
    try {
      setLoading(true);
      const response = await axios.get<FlightDetails>(`http://localhost:8000/flight-data/flight-details/${flightId}`);
      setSelectedFlightDetails(response.data);
      
      // Update map center to focus on the selected flight
      if (response.data.latitude && response.data.longitude) {
        setSelectedFlight(response.data);
      }
    } catch (err) {
      console.error('Error fetching flight details:', err);
      setError('Failed to fetch flight details. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Function to get the appropriate icon based on flight status
  const getFlightIcon = (status: string) => {
    if (status?.toLowerCase() === 'delayed' || status?.toLowerCase() === 'cancelled' || status?.toLowerCase() === 'diverted') {
      return delayedIcon;
    }
    return activeIcon;
  };

  // Handle filter changes
  const handleFilterChange = (newFilters: FilterCriteria) => {
    setFilters(newFilters);
  };

  // Handle selecting an aircraft from saved aircraft
  const handleSelectSavedAircraft = (registration: string) => {
    setFilters({
      ...filters,
      registration: registration
    });
  };

  // Toggle flight history display
  const toggleHistory = () => {
    setShowHistory(!showHistory);
  };

  return (
    <div className="flight-tracker-container">
      <div className="section-header">
        <h2>{t('flightTracker.title')}</h2>
        <div className="connection-status-container">
          <div className={`connection-status ${dataSource === 'live' ? 'connected' : 'disconnected'}`}>
            {dataSource === 'live' ? 'Live Data' : t('common.noData')}
          </div>
          {lastUpdate && (
            <div className="last-update">
              {t('common.loading')}: {lastUpdate.toLocaleTimeString()}
            </div>
          )}
        </div>
      </div>

      <div className="flight-tracker-content">
        <div className="flights-list">
          <FlightFilters onFilterChange={handleFilterChange} />
          
          <SavedAircraft onSelectAircraft={handleSelectSavedAircraft} />
          
          {loading ? (
            <div className="loading-indicator">{t('common.loading')}</div>
          ) : error ? (
            <div className="error-message">{t('common.error')}: {error}</div>
          ) : filteredFlights.length === 0 ? (
            <div className="no-data-message">{t('common.noData')}</div>
          ) : (
            <table className="flights-table">
              <thead>
                <tr>
                  <th>{t('flightData.flightNumber')}</th>
                  <th>{t('schedule.airline')}</th>
                  <th>{t('schedule.origin')}</th>
                  <th>{t('schedule.destination')}</th>
                  <th>{t('flightData.status')}</th>
                </tr>
              </thead>
              <tbody>
                {filteredFlights.map(flight => (
                  <tr 
                    key={flight.flight_id} 
                    className={selectedFlight?.flight_id === flight.flight_id ? 'selected-flight' : ''}
                    onClick={() => handleFlightSelect(flight.flight_id)}
                  >
                    <td>{flight.callsign}</td>
                    <td>{flight.airline}</td>
                    <td>{flight.origin}</td>
                    <td>{flight.destination}</td>
                    <td>
                      <span className={`status-badge status-${flight.status.toLowerCase()}`}>
                        {flight.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
        
        <div className="map-container">
          <MapContainer
            center={[4.6097, -74.0817]} // Bogotá, Colombia coordinates
            zoom={5}
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {filteredFlights.map(flight => (
              flight.latitude && flight.longitude ? (
                <Marker
                  key={flight.flight_id}
                  position={[flight.latitude, flight.longitude]}
                  icon={getFlightIcon(flight.status)}
                  eventHandlers={{
                    click: () => handleFlightSelect(flight.flight_id)
                  }}
                >
                  <Popup>
                    <div className="flight-popup">
                      <h3>{flight.callsign}</h3>
                      <div className="flight-details">
                        <p><strong>{t('flightData.aircraft')}:</strong> {flight.aircraft_type}</p>
                        <p><strong>{t('schedule.airline')}:</strong> {flight.airline}</p>
                        <p><strong>{t('schedule.origin')}:</strong> {flight.origin}</p>
                        <p><strong>{t('schedule.destination')}:</strong> {flight.destination}</p>
                        <p><strong>{t('flightData.status')}:</strong> {flight.status}</p>
                        <p><strong>{t('flightTracker.altitude')}:</strong> {flight.altitude} ft</p>
                        <p><strong>{t('flightTracker.speed')}:</strong> {flight.speed} kts</p>
                      </div>
                    </div>
                  </Popup>
                </Marker>
              ) : null
            ))}
            {selectedFlight && <FlyToMarker flight={selectedFlight} />}
          </MapContainer>
        </div>
        
        <div className="flight-details-panel">
          {selectedFlight ? (
            <div className="details-card">
              <div className="details-header">
                <h2>{selectedFlight.callsign}</h2>
                <button 
                  className={`btn-toggle-history ${showHistory ? 'active' : ''}`}
                  onClick={toggleHistory}
                >
                  {showHistory ? t('common.back') : t('flightTracker.history.title')}
                </button>
              </div>
              
              {showHistory ? (
                <FlightHistory registration={selectedFlight.tail_number} />
              ) : selectedFlightDetails ? (
                <div className="details-grid">
                  <div className="detail-item">
                    <span className="detail-label">{t('schedule.airline')}</span>
                    <span className="detail-value">{selectedFlightDetails.airline}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">{t('flightData.aircraft')}</span>
                    <span className="detail-value">{selectedFlightDetails.aircraft_type}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">{t('flightTracker.registration')}</span>
                    <span className="detail-value">{selectedFlightDetails.tail_number}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">{t('flightData.status')}</span>
                    <span className={`status-badge status-${selectedFlightDetails.status.toLowerCase()}`}>
                      {selectedFlightDetails.status}
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">{t('schedule.origin')}</span>
                    <span className="detail-value">
                      {selectedFlightDetails.origin} - {selectedFlightDetails.origin_name}
                      <div className="detail-subtext">{selectedFlightDetails.origin_city}</div>
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">{t('schedule.destination')}</span>
                    <span className="detail-value">
                      {selectedFlightDetails.destination} - {selectedFlightDetails.destination_name}
                      <div className="detail-subtext">{selectedFlightDetails.destination_city}</div>
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">{t('flightTracker.altitude')}</span>
                    <span className="detail-value">{selectedFlightDetails.altitude} ft</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">{t('flightTracker.speed')}</span>
                    <span className="detail-value">{selectedFlightDetails.speed} kts</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">{t('flightTracker.heading')}</span>
                    <span className="detail-value">{selectedFlightDetails.heading}°</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">{t('flightTracker.distance')}</span>
                    <span className="detail-value">{selectedFlightDetails.distance} nm</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">{t('flightTracker.estimatedTime')}</span>
                    <span className="detail-value">{selectedFlightDetails.estimated_time_enroute}</span>
                  </div>
                </div>
              ) : (
                <div className="loading">{t('common.loading')}</div>
              )}
            </div>
          ) : (
            <div className="no-selection">{t('flightTracker.selectFlight')}</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FlightTracker; 