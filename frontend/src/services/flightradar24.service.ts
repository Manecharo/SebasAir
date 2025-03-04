import axios, { AxiosInstance } from 'axios';
import { FR24_CONFIG, API_TOKEN, DEFAULT_BOUNDS } from '../config/flightradar24.config';

export interface FlightPosition {
    id: string;
    latitude: number;
    longitude: number;
    altitude: number;
    speed: number;
    heading: number;
    registration: string;
    aircraft: string;
    airline: string;
    status: string;
}

export interface FlightDetails {
    flightId: string;
    origin: string;
    destination: string;
    scheduledDeparture: string;
    scheduledArrival: string;
    actualDeparture?: string;
    actualArrival?: string;
    status: string;
}

class FlightRadar24Service {
    private api: AxiosInstance;

    constructor() {
        this.api = axios.create({
            baseURL: FR24_CONFIG.BASE_URL,
            headers: {
                'Accept': 'application/json',
                'Authorization': `Bearer ${API_TOKEN}`,
                'Accept-Version': FR24_CONFIG.API_VERSION
            }
        });

        // Add response interceptor for error handling
        this.api.interceptors.response.use(
            response => response,
            error => {
                if (error.response) {
                    switch (error.response.status) {
                        case 401:
                            console.error('Unauthorized: Check your API token');
                            break;
                        case 402:
                            console.error('Insufficient credits');
                            break;
                        case 429:
                            console.error('Rate limit exceeded');
                            break;
                        default:
                            console.error('API Error:', error.response.data);
                    }
                }
                return Promise.reject(error);
            }
        );
    }

    async getLiveFlights(bounds = DEFAULT_BOUNDS): Promise<FlightPosition[]> {
        try {
            const boundsParam = `${bounds.north},${bounds.south},${bounds.west},${bounds.east}`;
            const response = await this.api.get(FR24_CONFIG.ENDPOINTS.LIVE_FLIGHTS, {
                params: { bounds: boundsParam }
            });
            return this.transformFlightData(response.data);
        } catch (error) {
            console.error('Error fetching live flights:', error);
            throw error;
        }
    }

    async getFlightDetails(flightId: string): Promise<FlightDetails> {
        try {
            const response = await this.api.get(`${FR24_CONFIG.ENDPOINTS.FLIGHT_DETAILS}/${flightId}`);
            return this.transformFlightDetails(response.data);
        } catch (error) {
            console.error('Error fetching flight details:', error);
            throw error;
        }
    }

    private transformFlightData(data: any): FlightPosition[] {
        // Transform the API response to match our interface
        return Object.values(data.result.response.data || {}).map((flight: any) => ({
            id: flight.id || '',
            latitude: flight.latitude || 0,
            longitude: flight.longitude || 0,
            altitude: flight.altitude || 0,
            speed: flight.speed || 0,
            heading: flight.heading || 0,
            registration: flight.registration || '',
            aircraft: flight.aircraft?.model || '',
            airline: flight.airline?.name || '',
            status: flight.status || ''
        }));
    }

    private transformFlightDetails(data: any): FlightDetails {
        const flight = data.result.response.data || {};
        return {
            flightId: flight.identification?.id || '',
            origin: flight.airport?.origin?.code || '',
            destination: flight.airport?.destination?.code || '',
            scheduledDeparture: flight.time?.scheduled?.departure || '',
            scheduledArrival: flight.time?.scheduled?.arrival || '',
            actualDeparture: flight.time?.real?.departure || undefined,
            actualArrival: flight.time?.real?.arrival || undefined,
            status: flight.status?.text || ''
        };
    }
}

export const flightRadar24Service = new FlightRadar24Service();
export default flightRadar24Service; 