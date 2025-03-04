import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import axios from 'axios';
import useTranslation from '../i18n/useTranslation';

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

// Define Flight interface
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

const MapComponent: React.FC = () => {
  const { t } = useTranslation();
  const position: [number, number] = [40.0, -95.0]; // Center of US as default
  const [flights, setFlights] = useState<Flight[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [dataSource, setDataSource] = useState<string>('mock');
  const mapRef = useRef<L.Map | null>(null);
  
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

  // Function to get the appropriate icon based on flight status
  const getFlightIcon = (status: string) => {
    if (status?.toLowerCase() === 'delayed' || status?.toLowerCase() === 'cancelled' || status?.toLowerCase() === 'diverted') {
      return delayedIcon;
    }
    return activeIcon;
  };

  return (
    <div className="map-component">
      <div className="map-header">
        <h2>{t('map.title')}</h2>
        <div className="map-status">
          <div className={`connection-status ${dataSource === 'live' ? 'connected' : 'disconnected'}`}>
            {dataSource === 'live' ? 'Live Data' : t('common.noData')}
          </div>
          {lastUpdate && (
            <div className="last-update">
              {t('common.loading')}: {lastUpdate.toLocaleTimeString()}
            </div>
          )}
          <div className="flight-count">
            {flights.length} {t('flightTracker.title')}
          </div>
        </div>
      </div>
      
      {loading ? (
        <div className="loading-indicator">{t('common.loading')}</div>
      ) : error ? (
        <div className="error-message">{t('common.error')}: {error}</div>
      ) : (
        <MapContainer
          center={[4.6097, -74.0817]} // Bogotá, Colombia coordinates
          zoom={6}
          style={{ height: '600px', width: '100%' }}
          ref={(map) => {
            if (map) mapRef.current = map;
          }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          {flights.map((flight) => (
            <Marker
              key={flight.flight_id}
              position={[flight.latitude, flight.longitude]}
              icon={getFlightIcon(flight.status)}
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
          ))}
        </MapContainer>
      )}
    </div>
  );
};

export default MapComponent;
