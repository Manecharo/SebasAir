# Project Plan for Air Ambulance Tracking Application

## Step 1: Project Setup
- [x] Initialize the project structure.
- [x] Set up version control with Git.

## Step 2: Backend Development
- [x] Implement FastAPI for the backend.
- [x] Define models for flights and reports.
- [x] Create endpoints for:
  - [x] Fetching scheduled flights.
  - [x] Fetching actual flights.
  - [x] Comparing scheduled vs. actual flights.

## Step 3: Frontend Development
- [x] Set up React with Vite for the frontend.
- [x] Create components for:
  - [x] Map view to display live flight data.
  - [x] Schedule comparison to show scheduled vs. actual flights.
  - [x] Reporting component to display flight reports.

## Step 4: Data Fetching
- [x] Implement data fetching in the frontend components.
- [x] Ensure the frontend can communicate with the backend API.

## Step 5: Testing
- [ ] Write unit tests for backend endpoints using pytest.
- [ ] Validate frontend functionality.

## Step 6: Deployment
- [ ] Prepare the application for deployment.
- [ ] Set up environment variables and configurations.

## Current Status
- Backend endpoints for scheduled flights, actual flights, and flights comparison have been implemented.
- Frontend components for map view, schedule comparison, and reporting have been created.
- Data fetching logic is in place for both components.
- Unit tests for backend endpoints have been written but not yet executed.

## Next Steps
- Run the unit tests to validate backend functionality.
- Test the frontend components to ensure they display data correctly.

---

### Project Structure
```
backend/
│   ├── src/
│   │   ├── config/
│   │   │   ├── db.py            # DB config & connections
│   │   │   ├── api.py           # flight API configs
│   │   ├── models/
│   │   │   ├── flight.py        # SQLAlchemy models
│   │   │   ├── competitor.py
│   │   │   └── schedule.py
│   │   ├── routers/
│   │   │   ├── flights.py
│   │   │   ├── schedule.py
│   │   │   ├── competitors.py
│   │   │   └── reports.py
│   │   ├── services/
│   │   │   ├── flight_data.py
│   │   │   ├── competitor.py
│   │   │   ├── alerts.py
│   │   │   ├── competitor_data_client.py
│   │   │   ├── competitor_data_service.py
│   │   │   └── report.py
│   │   ├── utils/
│   │   │   ├── logger.py
│   │   │   └── ...
│   │   └── alembic/             # Database migrations
│   ├── tests/
│   │   ├── test_flights.py
│   │   └── ...
│   └── Dockerfile
```

---

## 3. Technology Setup Requirements

### 3.1 Environment & Dependencies
1. **Python** (v3.9+) for backend.
2. **React** (v18+) for the frontend.
3. **PostgreSQL** 13+ or any compatible version.
4. **AWS Account** (for EC2, RDS, S3, IAM setup).
5. **Flight Data API Key** (from FlightRadar24 or OpenSky).
6. **Email Service Credentials** (AWS SES or alternative SMTP for alerts).

**Local Setup**:
- Install Python and PostgreSQL locally.
- Create `.env` file from `.env.example` with secrets (API keys, DB password, etc.).

### 3.2 AWS Configuration
- Create an **EC2** instance (t2.micro) under free tier.
- Create an **RDS** Postgres database (db.t2.micro) under free tier.
- Configure **security groups** to allow inbound traffic on necessary ports (e.g., port 80/443 for the dashboard, port 5432 for RDS).
- (Optional) Create an **S3 bucket** for hosting the React static frontend.
- Set up **IAM roles** or credentials that your EC2 instance uses to communicate with RDS or SES.

### 3.3 External Data Integration
- **FlightRadar24 / OpenSky**: 
  - Obtain API credentials (key/secret).
  - Whitelist the server IP if required.
  - Familiarize with rate limits and plan for caching to reduce calls.

---

## 4. Step-by-Step Development
### Step 1: Initialize Repositories & Environments
- [x] **1.1** Create a Git repository (`air-ambulance-dashboard/`)
- [x] **1.2** Push the folder structure (empty placeholders, `.gitignore`, `README.md`)
- [x] **1.3** In AWS or local dev environment, install Python and Postgres. Create an empty database named `colcharter`

### Step 2: Backend Boilerplate
- [x] **2.1** Create Python virtual environment and install dependencies
- [x] **2.2** Create FastAPI entry point with basic endpoint
- [x] **2.3** Configure database connection using SQLAlchemy
- [x] **2.4** Verify database connection works

### Step 3: Database Setup
- [x] **3.1** Define SQLAlchemy models for:
  - Flights (tail number, status, positions, times)
  - Competitor flights (operator, route, timestamps)
  - Schedules (planned flights, aircraft assignments)
- [x] **3.2** Create initial database migrations
- [x] **3.3** Apply migrations to create tables in PostgreSQL

### Step 4: Flight Data Service
- [x] **4.1** Implement OpenSky API client
- [x] **4.2** Create background service to fetch flight data
- [x] **4.3** Store live flight data in database

### Step 5: Competitor Tracking
- [x] **5.1** Create competitor flight data model
- [x] **5.2** Implement daily competitor data fetch
- [x] **5.3** Add endpoint to retrieve competitor analytics

### Step 6: React Frontend Setup
- [x] **6.1** Initialize React project in `frontend/`
- [x] **6.2** Set up basic routing and layout
- [ ] **6.3** Integrate Leaflet for map-based live flight tracking

### Step 7: Live Flight Map
- [ ] **7.1** Implement map component using Leaflet
- [ ] **7.2** Fetch and display live flight data on the map
- [ ] **7.3** Show flight details on marker popups

### Step 8: Schedule vs Actual UI
- [ ] **8.1** Create schedule comparison table component
- [ ] **8.2** Fetch and display scheduled vs actual flight data
- [ ] **8.3** Highlight discrepancies

### Step 9: Operational Summaries & KPIs
- [ ] **9.1** Implement backend logic to compute operational KPIs
- [ ] **9.2** Create frontend components to display summaries and KPIs
- [ ] **9.3** Integrate charts using Chart.js or Recharts

### Step 10: Competitor Panel & Visualization
- [ ] **10.1** Add competitors data visualization component
- [ ] **10.2** Enable toggling competitor flight data on the map
- [ ] **10.3** Display competitor analytics in the panel

### Step 11: Alerts & Notification
- [ ] **11.1** Implement alerts backend service
- [ ] **11.2** Create frontend component to display alerts
- [ ] **11.3** Integrate email notifications using AWS SES

### Step 12: Automated Reports
- [ ] **12.1** Develop backend service to generate daily/weekly reports
- [ ] **12.2** Create endpoints to fetch and download reports
- [ ] **12.3** Integrate report generation in frontend

### Step 13: Testing & Integration
- [ ] **13.1** Write unit and integration tests for backend services
- [ ] **13.2** Perform end-to-end testing of the frontend
- [ ] **13.3** Conduct user acceptance testing with ops team

### Step 14: Performance & Cost Optimization
- [ ] **14.1** Optimize API calls and implement caching strategies
- [ ] **14.2** Scale backend services based on load
- [ ] **14.3** Monitor AWS costs and set up billing alerts

### Step 15: Deployment
- [ ] **15.1** Containerize backend and frontend using Docker
- [ ] **15.2** Deploy backend to AWS EC2
- [ ] **15.3** Deploy frontend to AWS S3 or CloudFront
- [ ] **15.4** Set up CI/CD pipelines for automated deployments

### Step 16: Final Handover & Documentation
- [ ] **16.1** Document all API endpoints and services
- [ ] **16.2** Update `README.md` with comprehensive setup and deployment instructions
- [ ] **16.3** Finalize user guides and operational manuals

---

**This document is now the final guide for the project. Only checkboxes should be updated to track progress. All future actions must follow this guide.**
