import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import '../App.css';
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

// Create custom icons for different aircraft types
const piperIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  className: 'piper-icon',
});

const cessnaIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  className: 'cessna-icon',
});

const beechcraftIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  className: 'beechcraft-icon',
});

const otherIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  className: 'other-icon',
});

L.Marker.prototype.options.icon = DefaultIcon;

interface Aircraft {
  id: string;
  registration: string;
  type: string;
  serialNumber: string;
  status?: string;
  latitude?: number;
  longitude?: number;
  altitude?: number;
  speed?: number;
  heading?: number;
  lastSeen?: string;
}

// Component to fly to a selected aircraft
const FlyToMarker = ({ aircraft }: { aircraft: Aircraft | null }) => {
  const map = useMap();
  
  useEffect(() => {
    if (aircraft && aircraft.latitude && aircraft.longitude) {
      map.flyTo([aircraft.latitude, aircraft.longitude], 8, {
        animate: true,
        duration: 1.5
      });
    }
  }, [aircraft, map]);
  
  return null;
};

const MyFleet: React.FC = () => {
  const { t } = useTranslation();
  // Predefined fleet of aircraft to track
  const [fleet, setFleet] = useState<Aircraft[]>([
    { id: '1', registration: 'HK-5020', type: 'Piper PA-34-200T Seneca II', serialNumber: '34-7870244' },
    { id: '2', registration: 'HK-2946', type: 'Piper PA-34-220T Seneca III', serialNumber: '34-8333015' },
    { id: '3', registration: 'HK-4699', type: 'Piper PA-34-220T Seneca III', serialNumber: '34-8233079' },
    { id: '4', registration: 'HK-4714', type: 'Cessna 414', serialNumber: '414-0427' },
    { id: '5', registration: 'HK-4966', type: 'Rockwell 690A Turbo Commander', serialNumber: '11119' },
    { id: '6', registration: 'HK-5225', type: 'Swearingen SA226-AT Merlin IV', serialNumber: 'AT027' },
    { id: '7', registration: 'HK-5118', type: 'Beechcraft C90GTx King Air', serialNumber: 'LJ-2102' }
  ]);
  
  const [selectedAircraft, setSelectedAircraft] = useState<Aircraft | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [mapCenter, setMapCenter] = useState<[number, number]>([4.6097, -74.0817]); // Bogotá, Colombia as default
  const [lastUpdate, setLastUpdate] = useState<string>('');

  // Simulate fetching aircraft positions
  useEffect(() => {
    const fetchAircraftPositions = async () => {
      setLoading(true);
      try {
        // In a real application, this would call your backend API to get real positions
        // For now, we'll simulate with random positions near Colombia
        
        // Mock data - in a real app, you would fetch this from your API
        const updatedFleet = fleet.map(aircraft => {
          // Generate random positions near Colombia for demonstration
          const randomLat = 4.6097 + (Math.random() - 0.5) * 5;
          const randomLng = -74.0817 + (Math.random() - 0.5) * 5;
          
          // Random altitude between 5000 and 25000 feet
          const randomAltitude = Math.floor(5000 + Math.random() * 20000);
          
          // Random speed between 150 and 350 knots
          const randomSpeed = Math.floor(150 + Math.random() * 200);
          
          // Random heading between 0 and 359 degrees
          const randomHeading = Math.floor(Math.random() * 360);
          
          // Random status
          const statuses = ['En Route', 'Scheduled', 'Landed', 'Maintenance'];
          const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
          
          return {
            ...aircraft,
            latitude: randomLat,
            longitude: randomLng,
            altitude: randomAltitude,
            speed: randomSpeed,
            heading: randomHeading,
            status: randomStatus,
            lastSeen: new Date().toISOString()
          };
        });
        
        setFleet(updatedFleet);
        setLastUpdate(new Date().toLocaleTimeString());
        setError(null);
      } catch (err) {
        console.error('Error fetching aircraft positions:', err);
        setError(t('myFleet.errorLoadingAircraft'));
      } finally {
        setLoading(false);
      }
    };

    // Initial fetch
    fetchAircraftPositions();

    // Refresh data every 30 seconds
    const interval = setInterval(() => {
      fetchAircraftPositions();
    }, 30000);

    return () => clearInterval(interval);
  }, [fleet, t]);

  // Function to get the appropriate icon based on aircraft type
  const getAircraftIcon = (type: string) => {
    if (type.toLowerCase().includes('piper')) {
      return piperIcon;
    } else if (type.toLowerCase().includes('cessna')) {
      return cessnaIcon;
    } else if (type.toLowerCase().includes('beechcraft') || type.toLowerCase().includes('king air')) {
      return beechcraftIcon;
    }
    return otherIcon;
  };

  // Handle aircraft selection
  const handleAircraftSelect = (aircraft: Aircraft) => {
    setSelectedAircraft(aircraft);
    if (aircraft.latitude && aircraft.longitude) {
      setMapCenter([aircraft.latitude, aircraft.longitude]);
    }
  };

  return (
    <div className="my-fleet-container">
      <h1>{t('myFleet.title')}</h1>
      <p className="last-update">{t('myFleet.lastUpdated')}: {lastUpdate || t('myFleet.unknown')}</p>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="fleet-content">
        <div className="aircraft-list">
          <h2>{t('myFleet.aircraft')}</h2>
          {loading && !fleet.length ? (
            <p className="loading">{t('myFleet.loadingAircraft')}</p>
          ) : (
            <div className="table-container">
              <table className="aircraft-table">
                <thead>
                  <tr>
                    <th>{t('myFleet.registration')}</th>
                    <th>{t('myFleet.type')}</th>
                    <th>{t('myFleet.status')}</th>
                    <th>{t('myFleet.actions')}</th>
                  </tr>
                </thead>
                <tbody>
                  {fleet.map((aircraft) => (
                    <tr 
                      key={aircraft.id} 
                      className={selectedAircraft?.id === aircraft.id ? 'selected-aircraft' : ''}
                    >
                      <td>{aircraft.registration}</td>
                      <td>{aircraft.type}</td>
                      <td>
                        {aircraft.status ? (
                          <span className={`status-badge status-${aircraft.status?.toLowerCase().replace(' ', '-')}`}>
                            {aircraft.status}
                          </span>
                        ) : (
                          t('myFleet.unknown')
                        )}
                      </td>
                      <td>
                        <button
                          className="view-details-btn"
                          onClick={() => handleAircraftSelect(aircraft)}
                        >
                          {t('myFleet.track')}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="map-container">
          <MapContainer center={mapCenter} zoom={6} style={{ height: '100%', width: '100%' }}>
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            {fleet.map(aircraft => (
              aircraft.latitude && aircraft.longitude ? (
                <Marker 
                  key={aircraft.id} 
                  position={[aircraft.latitude, aircraft.longitude]}
                  icon={getAircraftIcon(aircraft.type)}
                  eventHandlers={{
                    click: () => handleAircraftSelect(aircraft)
                  }}
                >
                  <Popup>
                    <div className="aircraft-popup">
                      <h3>{aircraft.registration}</h3>
                      <p><strong>{t('myFleet.type')}:</strong> {aircraft.type}</p>
                      <p><strong>{t('myFleet.serialNumber')}:</strong> {aircraft.serialNumber}</p>
                      <p><strong>{t('myFleet.status')}:</strong> {aircraft.status || t('myFleet.unknown')}</p>
                      <p><strong>{t('myFleet.altitude')}:</strong> {aircraft.altitude} ft</p>
                      <p><strong>{t('myFleet.speed')}:</strong> {aircraft.speed} kts</p>
                      <p><strong>{t('myFleet.heading')}:</strong> {aircraft.heading}°</p>
                      <p><strong>{t('myFleet.lastSeen')}:</strong> {new Date(aircraft.lastSeen || '').toLocaleString()}</p>
                    </div>
                  </Popup>
                </Marker>
              ) : null
            ))}
            {selectedAircraft && <FlyToMarker aircraft={selectedAircraft} />}
          </MapContainer>
        </div>
      </div>
      
      {selectedAircraft && (
        <div className="aircraft-details">
          <h2>{t('myFleet.aircraftDetails')}</h2>
          <div className="details-grid">
            <div className="detail-item">
              <span className="detail-label">{t('myFleet.registration')}</span>
              <span className="detail-value">{selectedAircraft.registration}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">{t('myFleet.type')}</span>
              <span className="detail-value">{selectedAircraft.type}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">{t('myFleet.serialNumber')}</span>
              <span className="detail-value">{selectedAircraft.serialNumber}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">{t('myFleet.status')}</span>
              <span className="detail-value">{selectedAircraft.status || t('myFleet.unknown')}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">{t('myFleet.position')}</span>
              <span className="detail-value">
                {selectedAircraft.latitude?.toFixed(4)}, {selectedAircraft.longitude?.toFixed(4)}
              </span>
            </div>
            <div className="detail-item">
              <span className="detail-label">{t('myFleet.altitude')}</span>
              <span className="detail-value">{selectedAircraft.altitude} ft</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">{t('myFleet.speed')}</span>
              <span className="detail-value">{selectedAircraft.speed} kts</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">{t('myFleet.heading')}</span>
              <span className="detail-value">{selectedAircraft.heading}°</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">{t('myFleet.lastSeen')}</span>
              <span className="detail-value">{new Date(selectedAircraft.lastSeen || '').toLocaleString()}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MyFleet; 