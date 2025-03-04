import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Importing marker icons as modules
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

// Fix icon issues with Leaflet in React
const defaultIcon = L.icon({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

L.Marker.prototype.options.icon = defaultIcon;

interface Flight {
  id: string;
  position: [number, number];
  speed: number;
  altitude: number;
  heading: number;
}

const MapView: React.FC = () => {
  const [flights, setFlights] = useState<Flight[]>([]);

  useEffect(() => {
    const fetchFlights = async () => {
      try {
        const response = await fetch('/api/flights/active');
        const data = await response.json();
        setFlights(data.flights);
      } catch (error) {
        console.error('Error fetching flight data:', error);
      }
    };

    fetchFlights();
    const interval = setInterval(fetchFlights, 5000); // Fetch every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <MapContainer center={[37.7749, -122.4194]} zoom={5} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      />
      {flights.map((flight) => (
        <Marker key={flight.id} position={flight.position}>
          <Popup>
            <strong>Flight ID:</strong> {flight.id}<br />
            <strong>Speed:</strong> {flight.speed} km/h<br />
            <strong>Altitude:</strong> {flight.altitude} ft<br />
            <strong>Heading:</strong> {flight.heading}°
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapView;
