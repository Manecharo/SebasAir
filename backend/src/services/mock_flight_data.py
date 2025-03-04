import random
import time
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any

class MockFlightDataProvider:
    """
    Provides mock flight data for development and testing purposes.
    This is used when the Flightradar API is not available or when working offline.
    """
    
    # Major airports with their coordinates
    AIRPORTS = {
        'JFK': {'name': 'John F. Kennedy International Airport', 'lat': 40.6413, 'lon': -73.7781, 'city': 'New York'},
        'LAX': {'name': 'Los Angeles International Airport', 'lat': 33.9416, 'lon': -118.4085, 'city': 'Los Angeles'},
        'ORD': {'name': 'O\'Hare International Airport', 'lat': 41.9742, 'lon': -87.9073, 'city': 'Chicago'},
        'LHR': {'name': 'Heathrow Airport', 'lat': 51.4700, 'lon': -0.4543, 'city': 'London'},
        'CDG': {'name': 'Charles de Gaulle Airport', 'lat': 49.0097, 'lon': 2.5479, 'city': 'Paris'},
        'FRA': {'name': 'Frankfurt Airport', 'lat': 50.0379, 'lon': 8.5622, 'city': 'Frankfurt'},
        'AMS': {'name': 'Amsterdam Airport Schiphol', 'lat': 52.3105, 'lon': 4.7683, 'city': 'Amsterdam'},
        'MAD': {'name': 'Adolfo Suárez Madrid–Barajas Airport', 'lat': 40.4983, 'lon': -3.5676, 'city': 'Madrid'},
        'BCN': {'name': 'Barcelona–El Prat Airport', 'lat': 41.2974, 'lon': 2.0833, 'city': 'Barcelona'},
        'DXB': {'name': 'Dubai International Airport', 'lat': 25.2532, 'lon': 55.3657, 'city': 'Dubai'},
        'SIN': {'name': 'Singapore Changi Airport', 'lat': 1.3644, 'lon': 103.9915, 'city': 'Singapore'},
        'HND': {'name': 'Haneda Airport', 'lat': 35.5494, 'lon': 139.7798, 'city': 'Tokyo'},
        'SYD': {'name': 'Sydney Airport', 'lat': 33.9399, 'lon': 151.1753, 'city': 'Sydney'},
        'GRU': {'name': 'São Paulo–Guarulhos International Airport', 'lat': -23.4356, 'lon': -46.4731, 'city': 'São Paulo'},
        'MEX': {'name': 'Mexico City International Airport', 'lat': 19.4363, 'lon': -99.0721, 'city': 'Mexico City'},
    }
    
    # Airlines with their ICAO codes
    AIRLINES = {
        'AAL': 'American Airlines',
        'UAL': 'United Airlines',
        'DAL': 'Delta Air Lines',
        'BAW': 'British Airways',
        'AFR': 'Air France',
        'DLH': 'Lufthansa',
        'KLM': 'KLM Royal Dutch Airlines',
        'IBE': 'Iberia',
        'UAE': 'Emirates',
        'SIA': 'Singapore Airlines',
        'JAL': 'Japan Airlines',
        'QFA': 'Qantas',
        'TAM': 'LATAM Brasil',
        'AMX': 'Aeroméxico',
    }
    
    # Aircraft types
    AIRCRAFT_TYPES = [
        'B738', 'B77W', 'A320', 'A321', 'B789', 'A350', 'B748', 'A380', 'E190', 'CRJ9'
    ]
    
    # Flight statuses
    STATUSES = ['EN_ROUTE', 'SCHEDULED', 'LANDED', 'DEPARTED', 'DIVERTED', 'CANCELLED']
    
    def __init__(self, num_flights=50, seed=None):
        """
        Initialize the mock data provider.
        
        Args:
            num_flights: Number of mock flights to generate
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        
        self.flights = self._generate_flights(num_flights)
        self.last_update = datetime.now()
    
    def _generate_flights(self, num_flights: int) -> List[Dict[str, Any]]:
        """
        Generate a list of mock flights.
        
        Args:
            num_flights: Number of flights to generate
            
        Returns:
            List of flight dictionaries
        """
        flights = []
        
        for i in range(num_flights):
            # Select random origin and destination
            origin_code, origin = random.choice(list(self.AIRPORTS.items()))
            destination_code, destination = random.choice(list(self.AIRPORTS.items()))
            
            # Ensure origin and destination are different
            while origin_code == destination_code:
                destination_code, destination = random.choice(list(self.AIRPORTS.items()))
            
            # Select random airline
            airline_code, airline_name = random.choice(list(self.AIRLINES.items()))
            
            # Generate flight number
            flight_number = f"{airline_code}{random.randint(100, 9999)}"
            
            # Generate aircraft registration
            registration = f"N{random.randint(100, 999)}{chr(65 + random.randint(0, 25))}{chr(65 + random.randint(0, 25))}"
            
            # Select aircraft type
            aircraft_type = random.choice(self.AIRCRAFT_TYPES)
            
            # Generate departure and arrival times
            now = datetime.now()
            departure_time = now - timedelta(hours=random.randint(0, 5))
            flight_duration = timedelta(hours=random.randint(1, 12))
            arrival_time = departure_time + flight_duration
            
            # Calculate progress as a percentage of the flight duration
            elapsed = (now - departure_time).total_seconds()
            total_duration = flight_duration.total_seconds()
            progress = min(1.0, max(0.0, elapsed / total_duration))
            
            # Determine status based on progress
            if progress <= 0:
                status = 'SCHEDULED'
            elif progress < 0.1:
                status = 'DEPARTED'
            elif progress < 0.9:
                status = 'EN_ROUTE'
            else:
                status = 'LANDED'
            
            # Override with random status occasionally
            if random.random() < 0.05:
                status = random.choice(['DIVERTED', 'CANCELLED'])
            
            # Calculate current position based on progress
            if 0 < progress < 1:
                # Simple linear interpolation between origin and destination
                current_lat = origin['lat'] + progress * (destination['lat'] - origin['lat'])
                current_lon = origin['lon'] + progress * (destination['lon'] - origin['lon'])
                
                # Add some randomness to the path
                current_lat += random.uniform(-0.5, 0.5)
                current_lon += random.uniform(-0.5, 0.5)
            else:
                # At origin or destination
                current_lat = origin['lat'] if progress <= 0 else destination['lat']
                current_lon = origin['lon'] if progress <= 0 else destination['lon']
            
            # Calculate heading (direction from origin to destination)
            delta_lon = destination['lon'] - origin['lon']
            y = math.sin(delta_lon) * math.cos(destination['lat'])
            x = math.cos(origin['lat']) * math.sin(destination['lat']) - math.sin(origin['lat']) * math.cos(destination['lat']) * math.cos(delta_lon)
            heading = (math.degrees(math.atan2(y, x)) + 360) % 360
            
            # Generate altitude and speed based on progress
            if progress <= 0 or progress >= 1:
                altitude = 0
                speed = 0
            else:
                # Climb to cruise altitude, then descend
                if progress < 0.1:
                    altitude_factor = progress / 0.1
                elif progress > 0.9:
                    altitude_factor = (1 - progress) / 0.1
                else:
                    altitude_factor = 1.0
                
                altitude = int(35000 * altitude_factor)
                speed = int(400 + 200 * altitude_factor)
            
            flight = {
                'flight_id': flight_number,
                'callsign': flight_number,
                'tail_number': registration,
                'aircraft_type': aircraft_type,
                'airline': airline_name,
                'origin': origin_code,
                'destination': destination_code,
                'departure_time': departure_time.isoformat(),
                'arrival_time': arrival_time.isoformat(),
                'status': status,
                'latitude': current_lat,
                'longitude': current_lon,
                'altitude': altitude,
                'speed': speed,
                'heading': heading,
                'progress': progress
            }
            
            flights.append(flight)
        
        return flights
    
    def get_live_flights(self, bounds=None) -> List[Dict[str, Any]]:
        """
        Get the current list of mock flights.
        
        Args:
            bounds: Optional bounding box for filtering flights
            
        Returns:
            List of flight dictionaries
        """
        # Update flight positions if more than 10 seconds have passed
        now = datetime.now()
        if (now - self.last_update).total_seconds() > 10:
            self._update_flight_positions()
            self.last_update = now
        
        # Filter flights by bounds if provided
        if bounds:
            lat1, lon1, lat2, lon2 = bounds
            min_lat, max_lat = min(lat1, lat2), max(lat1, lat2)
            min_lon, max_lon = min(lon1, lon2), max(lon1, lon2)
            
            return [
                flight for flight in self.flights
                if min_lat <= flight['latitude'] <= max_lat and min_lon <= flight['longitude'] <= max_lon
            ]
        
        return self.flights
    
    def get_flight_details(self, flight_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a specific flight.
        
        Args:
            flight_id: The ID of the flight to fetch details for
            
        Returns:
            Dictionary containing detailed flight information
        """
        for flight in self.flights:
            if flight['flight_id'] == flight_id:
                # Add some additional details
                origin_info = self.AIRPORTS.get(flight['origin'], {})
                destination_info = self.AIRPORTS.get(flight['destination'], {})
                
                details = flight.copy()
                details.update({
                    'origin_name': origin_info.get('name'),
                    'origin_city': origin_info.get('city'),
                    'destination_name': destination_info.get('name'),
                    'destination_city': destination_info.get('city'),
                    'estimated_time_enroute': self._format_duration(
                        datetime.fromisoformat(flight['arrival_time']) - 
                        datetime.fromisoformat(flight['departure_time'])
                    ),
                    'distance': self._calculate_distance(
                        origin_info.get('lat'), origin_info.get('lon'),
                        destination_info.get('lat'), destination_info.get('lon')
                    )
                })
                
                return details
        
        return {}
    
    def _update_flight_positions(self):
        """
        Update the positions of all flights based on elapsed time.
        """
        now = datetime.now()
        
        for flight in self.flights:
            # Skip flights that are not in the air
            if flight['status'] not in ['DEPARTED', 'EN_ROUTE']:
                continue
            
            # Calculate new progress
            departure_time = datetime.fromisoformat(flight['departure_time'])
            arrival_time = datetime.fromisoformat(flight['arrival_time'])
            total_duration = (arrival_time - departure_time).total_seconds()
            elapsed = (now - departure_time).total_seconds()
            progress = min(1.0, max(0.0, elapsed / total_duration))
            
            # Update status based on progress
            if progress < 0.1:
                flight['status'] = 'DEPARTED'
            elif progress < 0.9:
                flight['status'] = 'EN_ROUTE'
            else:
                flight['status'] = 'LANDED'
            
            # Update position based on progress
            if 0 < progress < 1:
                origin = self.AIRPORTS.get(flight['origin'], {})
                destination = self.AIRPORTS.get(flight['destination'], {})
                
                # Simple linear interpolation between origin and destination
                flight['latitude'] = origin.get('lat', 0) + progress * (destination.get('lat', 0) - origin.get('lat', 0))
                flight['longitude'] = origin.get('lon', 0) + progress * (destination.get('lon', 0) - origin.get('lon', 0))
                
                # Add some randomness to the path
                flight['latitude'] += random.uniform(-0.05, 0.05)
                flight['longitude'] += random.uniform(-0.05, 0.05)
                
                # Update altitude and speed
                if progress < 0.1:
                    altitude_factor = progress / 0.1
                elif progress > 0.9:
                    altitude_factor = (1 - progress) / 0.1
                else:
                    altitude_factor = 1.0
                
                flight['altitude'] = int(35000 * altitude_factor)
                flight['speed'] = int(400 + 200 * altitude_factor)
            else:
                # At origin or destination
                origin = self.AIRPORTS.get(flight['origin'], {})
                destination = self.AIRPORTS.get(flight['destination'], {})
                
                flight['latitude'] = origin.get('lat', 0) if progress <= 0 else destination.get('lat', 0)
                flight['longitude'] = origin.get('lon', 0) if progress <= 0 else destination.get('lon', 0)
                flight['altitude'] = 0
                flight['speed'] = 0
            
            flight['progress'] = progress
    
    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points in kilometers.
        """
        if None in (lat1, lon1, lat2, lon2):
            return 0
        
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        
        return int(c * r)
    
    def _format_duration(self, duration):
        """
        Format a timedelta as hours and minutes.
        """
        total_minutes = int(duration.total_seconds() / 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        return f"{hours}h {minutes}m"


# Example usage
if __name__ == "__main__":
    provider = MockFlightDataProvider(num_flights=20)
    flights = provider.get_live_flights()
    
    print(f"Generated {len(flights)} mock flights:")
    for i, flight in enumerate(flights[:5]):  # Print first 5 flights
        print(f"\nFlight {i+1}:")
        for key, value in flight.items():
            print(f"  {key}: {value}")
    
    # Get details for the first flight
    if flights:
        flight_id = flights[0]['flight_id']
        details = provider.get_flight_details(flight_id)
        
        print(f"\nDetails for flight {flight_id}:")
        for key, value in details.items():
            print(f"  {key}: {value}") 