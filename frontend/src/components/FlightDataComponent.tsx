import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../App.css';

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

const FlightDataComponent: React.FC = () => {
  const [flights, setFlights] = useState<Flight[]>([]);
  const [selectedFlight, setSelectedFlight] = useState<FlightDetails | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [dataSource, setDataSource] = useState<{ using_real_data: boolean; source: string }>({
    using_real_data: false,
    source: 'Loading...'
  });

  // Fetch flights data
  useEffect(() => {
    const fetchFlights = async () => {
      try {
        setLoading(true);
        const response = await axios.get<Flight[]>('http://localhost:8000/flight-data/live-flights');
        setFlights(response.data);
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
        setDataSource(response.data);
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

  // Fetch flight details when a flight is selected
  const handleFlightSelect = async (flightId: string) => {
    try {
      setLoading(true);
      const response = await axios.get<FlightDetails>(`http://localhost:8000/flight-data/flight-details/${flightId}`);
      setSelectedFlight(response.data);
    } catch (err) {
      console.error('Error fetching flight details:', err);
      setError('Failed to fetch flight details. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flight-data-container">
      <div className="data-source-info">
        <p>
          <strong>Data Source:</strong> {dataSource.source}
          {!dataSource.using_real_data && (
            <span className="mock-data-badge">MOCK DATA</span>
          )}
        </p>
      </div>

      <div className="flight-data-content">
        <div className="flights-list">
          <h2>Live Flights</h2>
          {loading && !flights.length ? (
            <p className="loading">Loading flights...</p>
          ) : error ? (
            <p className="error">{error}</p>
          ) : (
            <>
              <p>Total flights: {flights.length}</p>
              <table className="flights-table">
                <thead>
                  <tr>
                    <th>Flight ID</th>
                    <th>Airline</th>
                    <th>Origin</th>
                    <th>Destination</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {flights.map((flight) => (
                    <tr key={flight.flight_id}>
                      <td>{flight.callsign || flight.flight_id}</td>
                      <td>{flight.airline || 'Unknown'}</td>
                      <td>{flight.origin || 'Unknown'}</td>
                      <td>{flight.destination || 'Unknown'}</td>
                      <td>
                        <span className={`status-badge status-${flight.status?.toLowerCase()}`}>
                          {flight.status || 'Unknown'}
                        </span>
                      </td>
                      <td>
                        <button
                          className="view-details-btn"
                          onClick={() => handleFlightSelect(flight.flight_id)}
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </div>

        <div className="flight-details">
          <h2>Flight Details</h2>
          {selectedFlight ? (
            <div className="details-card">
              <h3>{selectedFlight.callsign || selectedFlight.flight_id}</h3>
              <div className="details-grid">
                <div className="detail-item">
                  <span className="detail-label">Airline:</span>
                  <span className="detail-value">{selectedFlight.airline || 'Unknown'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Aircraft:</span>
                  <span className="detail-value">{selectedFlight.aircraft_type || 'Unknown'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Registration:</span>
                  <span className="detail-value">{selectedFlight.tail_number || 'Unknown'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Status:</span>
                  <span className={`status-badge status-${selectedFlight.status?.toLowerCase()}`}>
                    {selectedFlight.status || 'Unknown'}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Origin:</span>
                  <span className="detail-value">
                    {selectedFlight.origin_name ? `${selectedFlight.origin_name} (${selectedFlight.origin})` : selectedFlight.origin || 'Unknown'}
                    {selectedFlight.origin_city && `, ${selectedFlight.origin_city}`}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Destination:</span>
                  <span className="detail-value">
                    {selectedFlight.destination_name ? `${selectedFlight.destination_name} (${selectedFlight.destination})` : selectedFlight.destination || 'Unknown'}
                    {selectedFlight.destination_city && `, ${selectedFlight.destination_city}`}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Distance:</span>
                  <span className="detail-value">{selectedFlight.distance ? `${selectedFlight.distance} km` : 'Unknown'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Flight Time:</span>
                  <span className="detail-value">{selectedFlight.estimated_time_enroute || 'Unknown'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Altitude:</span>
                  <span className="detail-value">{selectedFlight.altitude ? `${selectedFlight.altitude} ft` : 'Unknown'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Speed:</span>
                  <span className="detail-value">{selectedFlight.speed ? `${selectedFlight.speed} knots` : 'Unknown'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Heading:</span>
                  <span className="detail-value">{selectedFlight.heading ? `${selectedFlight.heading}°` : 'Unknown'}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Position:</span>
                  <span className="detail-value">
                    {selectedFlight.latitude && selectedFlight.longitude
                      ? `${selectedFlight.latitude.toFixed(4)}, ${selectedFlight.longitude.toFixed(4)}`
                      : 'Unknown'}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <p className="no-selection">Select a flight to view details</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default FlightDataComponent; 