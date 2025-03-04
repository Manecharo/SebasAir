# Air Ambulance Fleet Tracking Dashboard

![Logo](logo.png)

A comprehensive dashboard for tracking and managing air ambulance fleet operations, providing real-time flight tracking, schedule management, and competitor analysis.

## Features

- **Real-time Flight Tracking**: Monitor active flights with position updates
- **Schedule Management**: View and compare flight schedules
- **Competitor Analysis**: Track competitor flights and statistics
- **Reporting**: Generate daily and weekly operational reports
- **Data Visualization**: Visual representation of flight data and statistics

## Project Structure

The project is divided into two main components:

### Backend (FastAPI)

- `backend/src/`: Main application code
  - `config/`: Configuration files and database setup
  - `models/`: SQLAlchemy models
  - `routers/`: API endpoints
  - `services/`: Business logic
  - `websockets/`: WebSocket implementation for real-time updates
- `backend/tests/`: Test files

### Frontend (React)

- `frontend/src/`: Main application code
  - `components/`: React components
  - `services/`: API service clients
  - `utils/`: Utility functions
  - `App.tsx`: Main application component

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/air-ambulance-tracking.git
   cd air-ambulance-tracking
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

4. Configure the environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and other settings
   ```

5. Initialize the database:
   ```bash
   cd backend
   alembic upgrade head
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   python -m src.main
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application:
   - Frontend: http://localhost:5174
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Testing

### Backend Tests

The backend includes comprehensive tests using pytest:

```bash
cd backend
python -m pytest
```

For more details on testing, see [backend/tests/README.md](backend/tests/README.md).

### Frontend Tests

The frontend includes tests using Vitest:

```bash
cd frontend
npm test
```

## Development Roadmap

- [x] Basic flight tracking functionality
- [x] Schedule comparison
- [x] Competitor analysis
- [x] Reporting
- [x] Data visualization
- [ ] User authentication and authorization
- [ ] Mobile responsiveness
- [ ] Advanced analytics
- [ ] Predictive maintenance
- [ ] Weather integration

## Technologies Used

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- WebSockets
- Pytest

### Frontend
- React
- TypeScript
- Vite
- Recharts
- Axios

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [Recharts](https://recharts.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL (optional, SQLite is used by default for development)

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env` (or create a new `.env` file)
   - Update the database URL if needed
   - Add your Flightradar24 API key:
     ```
     FLIGHTRADAR_API_KEY=your_api_key_here
     ```

4. Run the backend server:
   ```
   python -m src.main
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run dev
   ```

## Using the Flightradar24 API

The application uses the Flightradar24 API to fetch real-time flight data. To use this feature:

1. Sign up for a Flightradar24 API key at [https://www.flightradar24.com/premium/api](https://www.flightradar24.com/premium/api)
2. Add your API key to the `.env` file:
   ```
   FLIGHTRADAR_API_KEY=your_api_key_here
   ```
3. Restart the backend server

Without a valid API key, the application will fall back to simulated flight data.

## Testing

Run the backend tests:
```
cd backend
python -m pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
