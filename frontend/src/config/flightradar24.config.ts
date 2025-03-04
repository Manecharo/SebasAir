export const FR24_CONFIG = {
    BASE_URL: 'https://fr24api.flightradar24.com/api',
    API_VERSION: 'v1',
    ENDPOINTS: {
        LIVE_FLIGHTS: '/live/flight-positions/light',
        FLIGHT_DETAILS: '/live/flight/details',
        AIRPORTS: '/airports',
        AIRLINES: '/airlines'
    }
};

export const DEFAULT_BOUNDS = {
    north: 50.682,
    south: 46.218,
    west: 14.422,
    east: 22.243
};

// Add this to your environment variables
export const API_TOKEN = process.env.VITE_FR24_API_TOKEN || ''; 