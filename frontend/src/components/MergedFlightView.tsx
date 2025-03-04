import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import '../App.css';
import { useTranslation } from "react-i18next";
import FlightFilters, { FilterCriteria } from './FlightFilters';
import SavedAircraft from './SavedAircraft';
import FlightHistory from './FlightHistory';

// Fix for Leaflet default icon issue
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

L.Marker.prototype.options.icon = DefaultIcon;

// Define types
interface Flight {
  flight_id: string;
  callsign: string;
  airline: string;
  aircraft_type: string;
  tail_number: string;
  origin: string;
  destination: string;
  status: string;
  altitude: number;
  speed: number;
  heading: number;
  latitude: number;
  longitude: number;
  last_updated: string;
  departure_time?: string;
  arrival_time?: string;
}

interface FlightDetails extends Flight {
  origin_name: string;
  origin_city: string;
  destination_name: string;
  destination_city: string;
  vertical_speed: number;
  ground_speed: number;
  true_airspeed: number;
  indicated_airspeed: number;
  mach: number;
  track: number;
  distance_to_destination: number;
  time_to_destination: string;
}

// Custom component to fly to a marker
interface FlyToMarkerProps {
  flight: Flight;
}

const FlyToMarker: React.FC<FlyToMarkerProps> = ({ flight }) => {
  const map = useMap();
  
  useEffect(() => {
    if (flight && flight.latitude && flight.longitude) {
      map.flyTo([flight.latitude, flight.longitude], 10, {
        duration: 1.5
      });
    }
  }, [flight, map]);
  
  return null;
};

// Use default Leaflet icons
const defaultIcon = DefaultIcon;
const redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const MergedFlightView: React.FC = () => {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<'map' | 'tracker' | 'data'>('map');
  const [flights, setFlights] = useState<Flight[]>([]);
  const [filteredFlights, setFilteredFlights] = useState<Flight[]>([]);
  const [selectedFlight, setSelectedFlight] = useState<Flight | null>(null);
  const [flightDetails, setFlightDetails] = useState<FlightDetails | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [dataSource, setDataSource] = useState<'live' | 'mock'>('mock');
  const [lastUpdate, setLastUpdate] = useState<string>('');
  const [showHistory, setShowHistory] = useState<boolean>(false);
  const [filters, setFilters] = useState<FilterCriteria>({
    registration: '',
    aircraftType: '',
    airline: '',
    status: ''
  });

  // Fetch flights data
  useEffect(() => {
    const fetchFlights = async () => {
      try {
        setLoading(true);
        // In a real app, this would be an API call
        // For now, we'll generate mock data
        const mockFlights = generateMockFlights(50);
        setFlights(mockFlights);
        setFilteredFlights(mockFlights);
        setLastUpdate(new Date().toLocaleTimeString());
        setLoading(false);
      } catch (error) {
        console.error('Error fetching flights:', error);
        setError(t('mergedFlightView.errorLoadingFlights'));
        setLoading(false);
      }
    };

    const fetchDataSource = async () => {
      try {
        // In a real app, this would check if the live API is available
        // For now, we'll just set it to mock
        setDataSource('mock');
      } catch (error) {
        console.error('Error checking data source:', error);
        setDataSource('mock');
      }
    };

    fetchFlights();
    fetchDataSource();

    // Set up polling for real-time updates
    const interval = setInterval(() => {
      fetchFlights();
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, [t]);

  // Generate mock flight data
  const generateMockFlights = (count: number): Flight[] => {
    const airlines = ['COL', 'AME', 'LAT', 'AVA', 'VVC'];
    const aircraftTypes = ['A320', 'B737', 'E190', 'A321', 'B787'];
    const origins = ['BOG', 'MDE', 'CLO', 'CTG', 'BAQ'];
    const destinations = ['MIA', 'JFK', 'MEX', 'LIM', 'MAD'];
    const statuses = ['en_route', 'scheduled', 'landed', 'departed', 'delayed'];
    
    return Array.from({ length: count }, (_, i) => {
      const airline = airlines[Math.floor(Math.random() * airlines.length)];
      const flightNumber = Math.floor(Math.random() * 1000) + 1000;
      
      return {
        flight_id: `${airline}${flightNumber}`,
        callsign: `${airline}${flightNumber}`,
        airline,
        aircraft_type: aircraftTypes[Math.floor(Math.random() * aircraftTypes.length)],
        tail_number: `HK-${Math.floor(Math.random() * 1000) + 1000}`,
        origin: origins[Math.floor(Math.random() * origins.length)],
        destination: destinations[Math.floor(Math.random() * destinations.length)],
        latitude: 4.6097 + (Math.random() - 0.5) * 10,
        longitude: -74.0817 + (Math.random() - 0.5) * 10,
        altitude: Math.floor(Math.random() * 35000) + 5000,
        speed: Math.floor(Math.random() * 500) + 300,
        heading: Math.floor(Math.random() * 360),
        status: statuses[Math.floor(Math.random() * statuses.length)],
        last_updated: new Date().toISOString()
      };
    });
  };

  // Handle flight selection
  const handleFlightSelect = async (flightId: string) => {
    const flight = flights.find(f => f.flight_id === flightId) || null;
    setSelectedFlight(flight);
    
    if (flight) {
      try {
        // In a real app, this would be an API call to get detailed flight info
        // For now, we'll generate mock details
        const mockDetails: FlightDetails = {
          ...flight,
          origin_name: 'El Dorado International Airport',
          origin_city: 'Bogotá',
          destination_name: 'Miami International Airport',
          destination_city: 'Miami',
          departure_time: new Date(Date.now() - Math.random() * 3600000).toISOString(),
          arrival_time: new Date(Date.now() + Math.random() * 3600000).toISOString(),
          vertical_speed: Math.floor(Math.random() * 1000) - 500,
          ground_speed: Math.floor(Math.random() * 500) + 300,
          true_airspeed: Math.floor(Math.random() * 500) + 300,
          indicated_airspeed: Math.floor(Math.random() * 500) + 300,
          mach: 0.78 + Math.random() * 0.1,
          track: Math.floor(Math.random() * 360),
          distance_to_destination: Math.floor(Math.random() * 1000) + 100,
          time_to_destination: `${Math.floor(Math.random() * 5) + 1}h ${Math.floor(Math.random() * 60)}m`
        };
        
        setFlightDetails(mockDetails);
      } catch (error) {
        console.error('Error fetching flight details:', error);
        setFlightDetails(null);
      }
    } else {
      setFlightDetails(null);
    }
  };

  // Function to get the appropriate icon based on flight status
  const getFlightIcon = (status: string) => {
    if (status === 'delayed' || status === 'cancelled' || status === 'diverted') {
      return redIcon;
    }
    return defaultIcon;
  };

  // Function to get translated status label
  const getStatusLabel = (statusCode: string): string => {
    const statusKey = statusCode.toLowerCase().replace(/\s+/g, '');
    return t(`mergedFlightView.statusLabels.${statusKey}`) || statusCode;
  };

  // Apply filters to flights
  useEffect(() => {
    let result = [...flights];
    
    if (filters.registration) {
      result = result.filter(flight => 
        flight.tail_number.toLowerCase().includes(filters.registration.toLowerCase())
      );
    }
    
    if (filters.aircraftType) {
      result = result.filter(flight => 
        flight.aircraft_type.toLowerCase().includes(filters.aircraftType.toLowerCase())
      );
    }
    
    if (filters.airline) {
      result = result.filter(flight => 
        flight.airline.toLowerCase().includes(filters.airline.toLowerCase())
      );
    }
    
    if (filters.status) {
      result = result.filter(flight => 
        flight.status.toLowerCase() === filters.status.toLowerCase()
      );
    }
    
    setFilteredFlights(result);
  }, [flights, filters]);

  // Handle filter changes
  const handleFilterChange = (newFilters: FilterCriteria) => {
    setFilters(newFilters);
  };

  // Handle selecting a saved aircraft
  const handleSelectSavedAircraft = (registration: string) => {
    setFilters({
      ...filters,
      registration
    });
  };

  // Toggle flight history display
  const toggleHistory = () => {
    setShowHistory(!showHistory);
  };

  return (
    <div className="merged-flight-view-container">
      <div className="section-header">
        <h2>{t('mergedFlightView.title')}</h2>
        <p className="section-subtitle">{t('mergedFlightView.subtitle')}</p>
        
        <div className="connection-status-container">
          <div className={`connection-status ${dataSource === 'live' ? 'connected' : 'disconnected'}`}>
            {dataSource === 'live' 
              ? t('mergedFlightView.connected') 
              : t('mergedFlightView.disconnected')}
          </div>
          <div className="last-update">
            {t('mergedFlightView.lastUpdate')}: {lastUpdate}
          </div>
        </div>
      </div>
      
      <div className="merged-flight-view-layout">
        <div className="sidebar">
          <SavedAircraft onSelectAircraft={handleSelectSavedAircraft} />
          
          <FlightFilters 
            onFilterChange={handleFilterChange}
            registrationOptions={flights.map(f => f.tail_number)}
          />
        </div>
        
        <div className="main-content">
          <div className="tabs">
            <button 
              className={`tab ${activeTab === 'map' ? 'active' : ''}`}
              onClick={() => setActiveTab('map')}
            >
              {t('mergedFlightView.tabs.map')}
            </button>
            <button 
              className={`tab ${activeTab === 'tracker' ? 'active' : ''}`}
              onClick={() => setActiveTab('tracker')}
            >
              {t('mergedFlightView.tabs.tracker')}
            </button>
            <button 
              className={`tab ${activeTab === 'data' ? 'active' : ''}`}
              onClick={() => setActiveTab('data')}
            >
              {t('mergedFlightView.tabs.data')}
            </button>
          </div>
          
          <div className="tab-content">
            {activeTab === 'map' && (
              <div className="map-tab">
                <div className="map-container">
                  <MapContainer 
                    center={[4.6097, -74.0817]} 
                    zoom={5} 
                    style={{ height: '100%', width: '100%' }}
                  >
                    <TileLayer
                      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    />
                    
                    {selectedFlight && (
                      <FlyToMarker flight={selectedFlight} />
                    )}
                    
                    {filteredFlights.map(flight => (
                      flight.latitude && flight.longitude ? (
                        <Marker 
                          key={flight.flight_id}
                          position={[flight.latitude, flight.longitude]}
                          icon={flight.status === 'DELAYED' ? redIcon : defaultIcon}
                          eventHandlers={{
                            click: () => handleFlightSelect(flight.flight_id)
                          }}
                        >
                          <Popup>
                            <div className="flight-popup">
                              <h3>{flight.callsign}</h3>
                              <p><strong>{t('flightData.airline')}:</strong> {flight.airline}</p>
                              <p><strong>{t('flightData.aircraft')}:</strong> {flight.aircraft_type}</p>
                              <p><strong>{t('flightData.registration')}:</strong> {flight.tail_number}</p>
                              <p><strong>{t('flightData.origin')}:</strong> {flight.origin}</p>
                              <p><strong>{t('flightData.destination')}:</strong> {flight.destination}</p>
                              <p><strong>{t('flightData.status')}:</strong> {flight.status}</p>
                              <p><strong>{t('flightData.altitude')}:</strong> {flight.altitude} ft</p>
                              <p><strong>{t('flightData.speed')}:</strong> {flight.speed} kts</p>
                              <p><strong>{t('flightData.heading')}:</strong> {flight.heading}°</p>
                            </div>
                          </Popup>
                        </Marker>
                      ) : null
                    ))}
                  </MapContainer>
                </div>
              </div>
            )}
            
            {activeTab === 'tracker' && (
              <div className="tracker-tab">
                {loading ? (
                  <div className="loading-indicator">{t('common.loading')}</div>
                ) : error ? (
                  <div className="error-message">{t('common.error')}: {error}</div>
                ) : filteredFlights.length === 0 ? (
                  <div className="no-data-message">{t('common.noData')}</div>
                ) : (
                  <div className="flights-table-container">
                    <table className="flights-table">
                      <thead>
                        <tr>
                          <th>{t('flightData.flightNumber')}</th>
                          <th>{t('flightData.airline')}</th>
                          <th>{t('flightData.aircraft')}</th>
                          <th>{t('flightData.registration')}</th>
                          <th>{t('flightData.origin')}</th>
                          <th>{t('flightData.destination')}</th>
                          <th>{t('flightData.status')}</th>
                          <th>{t('flightData.altitude')}</th>
                          <th>{t('flightData.speed')}</th>
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
                            <td>{flight.aircraft_type}</td>
                            <td>{flight.tail_number}</td>
                            <td>{flight.origin}</td>
                            <td>{flight.destination}</td>
                            <td>
                              <span className={`status-badge status-${flight.status.toLowerCase()}`}>
                                {getStatusLabel(flight.status)}
                              </span>
                            </td>
                            <td>{flight.altitude} ft</td>
                            <td>{flight.speed} kts</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}
            
            {activeTab === 'data' && (
              <div className="data-tab">
                {selectedFlight ? (
                  <div className="flight-details">
                    <h3>{t('flightData.flightDetails')}</h3>
                    <div className="flight-details-grid">
                      <div className="detail-group">
                        <h4>{t('flightData.basicInfo')}</h4>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.flightNumber')}:</span>
                          <span className="detail-value">{selectedFlight.callsign}</span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.airline')}:</span>
                          <span className="detail-value">{selectedFlight.airline}</span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.aircraft')}:</span>
                          <span className="detail-value">{selectedFlight.aircraft_type}</span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.registration')}:</span>
                          <span className="detail-value">{selectedFlight.tail_number}</span>
                        </div>
                      </div>
                      
                      <div className="detail-group">
                        <h4>{t('flightData.route')}</h4>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.origin')}:</span>
                          <span className="detail-value">{selectedFlight.origin}</span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.destination')}:</span>
                          <span className="detail-value">{selectedFlight.destination}</span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.departureTime')}:</span>
                          <span className="detail-value">
                            {selectedFlight.departure_time 
                              ? new Date(selectedFlight.departure_time).toLocaleString() 
                              : t('common.notAvailable')}
                          </span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.arrivalTime')}:</span>
                          <span className="detail-value">
                            {selectedFlight.arrival_time 
                              ? new Date(selectedFlight.arrival_time).toLocaleString() 
                              : t('common.notAvailable')}
                          </span>
                        </div>
                      </div>
                      
                      <div className="detail-group">
                        <h4>{t('flightData.status')}</h4>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.currentStatus')}:</span>
                          <span className={`detail-value status-${selectedFlight.status.toLowerCase()}`}>
                            {selectedFlight.status}
                          </span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.altitude')}:</span>
                          <span className="detail-value">{selectedFlight.altitude} ft</span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.speed')}:</span>
                          <span className="detail-value">{selectedFlight.speed} kts</span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.heading')}:</span>
                          <span className="detail-value">{selectedFlight.heading}°</span>
                        </div>
                      </div>
                      
                      <div className="detail-group">
                        <h4>{t('flightData.lastUpdate')}</h4>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.lastUpdated')}:</span>
                          <span className="detail-value">
                            {selectedFlight.last_updated 
                              ? new Date(selectedFlight.last_updated).toLocaleString() 
                              : t('common.notAvailable')}
                          </span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-label">{t('flightData.dataSource')}:</span>
                          <span className="detail-value">{dataSource}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="no-flight-selected">
                    <p>{t('flightData.selectFlight')}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MergedFlightView; 