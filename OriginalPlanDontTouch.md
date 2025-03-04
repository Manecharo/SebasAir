Below is a comprehensive document describing the **Enhanced Air Ambulance Fleet Tracking Dashboard** final project plan, aimed at guiding both development teams and LLM coding assistants from start to finish. It covers folder structure, technology setup requirements, external data integration, and step-by-step tasks needed to achieve a fully functioning MVP.

---

## 1. Project Overview

**Name:** Enhanced Air Ambulance Fleet Tracking Dashboard  
**Purpose:** Provide real-time and historical tracking of air ambulance flights, operational KPIs, and competitor insights for internal use.

**Key MVP Features**:
- **Live Flight Tracking** (map-based positions, speeds, altitudes, headings)
- **Schedule vs Actual Comparison** (planned vs real-time flights)
- **Operational Summaries** (flight hours, on-time performance, delays)
- **Competitor Tracking** (fetch competitor flight data once a day, visualize on map & summaries)
- **Alerts** (departure delays, unauthorized route deviations, excessive ground time)
- **Historical Flight Review** (past flights replay & analysis)
- **Reports** (daily/weekly PDF or CSV summaries)

**Technologies**:  
- **Frontend**: React (JavaScript/TypeScript), Leaflet (maps), Chart.js/Recharts (charts)  
- **Backend**: Node.js + Express (for REST API), or Python + FastAPI (equivalent flow)  
- **Database**: PostgreSQL (hosted on AWS RDS)  
- **Hosting**: AWS EC2 (backend), S3 (optional for frontend static hosting), or a combined approach.  
- **External Flight Data**: OpenSky (free) or FlightRadar24 (paid API)  
- **Alerts & Emails**: NodeMailer + AWS SES (or similar)  

**Deployment URL**: `https://www.manecharo.com` (replace with your domain)  
**Branding**: `logo.png` (use as site header logo or for PDF reports)

---

## 2. Folder Structure

Below is the recommended folder structure for the entire project. This structure ensures the LLM or any developer can quickly locate files, components, and configuration, minimizing confusion and helping keep the codebase organized:

```plaintext
colchartereft/
├── README.md
├── .env.example          # Example environment variables
├── backend/
│   ├── package.json      # Node dependencies (if Node used)
│   ├── src/
│   │   ├── app.js        # Main Express or FastAPI entry
│   │   ├── config/
│   │   │   ├── db.config.js      # or .ts - DB config & connections
│   │   │   ├── api.config.js     # flight API configs (keys, endpoints)
│   │   ├── controllers/
│   │   │   ├── flightController.js   # or .ts
│   │   │   ├── scheduleController.js
│   │   │   ├── competitorController.js
│   │   │   └── reportController.js
│   │   ├── routes/
│   │   │   ├── flights.js         # routes e.g. GET /api/flights
│   │   │   ├── schedule.js
│   │   │   ├── competitors.js
│   │   │   └── reports.js
│   │   ├── models/
│   │   │   ├── Flight.js          # DB schemas & ORMs
│   │   │   ├── CompetitorFlight.js
│   │   │   ├── Schedule.js
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── flightData.service.js   # handles external API calls
│   │   │   ├── competitor.service.js
│   │   │   ├── alerts.service.js
│   │   │   └── report.service.js
│   │   ├── utils/
│   │   │   ├── logger.js         # logger, if needed
│   │   │   └── ...
│   │   └── index.js              # start server script
│   ├── tests/
│   │   ├── flightController.test.js
│   │   └── ...
│   └── Dockerfile                # Docker config for backend
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── logo.png              # brand image
│   ├── src/
│   │   ├── App.js                # main React app
│   │   ├── index.js              # React entry
│   │   ├── components/
│   │   │   ├── MapView.js        # map for flight tracking
│   │   │   ├── FlightTable.js
│   │   │   ├── KPIStats.js
│   │   │   ├── CompetitorPanel.js
│   │   │   ├── AlertsPanel.js
│   │   │   └── ...
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   │   ├── CompetitorView.js
│   │   │   ├── Reports.js
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── api.js            # axios/fetch config
│   │   └── styles/
│   │       ├── main.css
│   │       └── ...
│   ├── Dockerfile                # Docker config for frontend
│   └── ...
├── deployment/
│   ├── docker-compose.yml        # Optional, for local dev
│   ├── scripts/
│   │   ├── deploy-backend.sh
│   │   ├── deploy-frontend.sh
│   │   └── ...
│   └── ...
└── docs/
    ├── project-plan.md           # This file
    ├── architecture-diagram.png
    └── ...
```

**Notes**:
- You can adapt file extensions to `.ts` if TypeScript is preferred.
- For Python, you’d replace the Node structure with something like `main.py`, `routes/`, `controllers/`, etc.
- The `deployment/` folder stores scripts for building & deploying containers (if using Docker), or you can store IaC (e.g., Terraform or CloudFormation) there.

---

## 3. Technology Setup Requirements

### 3.1 Environment & Dependencies
1. **Node.js** (v14+ or latest LTS) for backend – or Python 3.9+ if using FastAPI.
2. **React** (v18+) for the frontend.
3. **PostgreSQL** 13+ or any compatible version.
4. **AWS Account** (for EC2, RDS, S3, IAM setup).
5. **Flight Data API Key** (from FlightRadar24 or OpenSky).
6. **Email Service Credentials** (AWS SES or alternative SMTP for alerts).

**Local Setup**:
- Install Node.js, PostgreSQL locally.
- Create `.env` file from `.env.example` with secrets (API keys, DB password, etc.).

### 3.2 AWS Configuration
- Create an **EC2** instance (t2.micro) under free tier.
- Create an **RDS** Postgres database (db.t2.micro) under free tier.
- Configure **security groups** to allow inbound traffic on the necessary ports (e.g., port 80/443 for the dashboard, port 5432 for RDS).
- (Optional) Create an **S3 bucket** for hosting the React static frontend (if you want to separate from the EC2 server).
- Set up **IAM roles** or credentials that your EC2 instance uses to communicate with RDS or SES.

### 3.3 External Data Integration
- **FlightRadar24 / OpenSky**: 
  - Obtain API credentials (key/secret).
  - Whitelist the server IP if required.
  - Familiarize with rate limits and plan for caching to reduce calls.

---

## 4. Step-by-Step Development

Below are the tasks in order. The intention is to ensure an LLM coding assistant (and any dev) follows this roadmap exactly, ensuring no deviation from the plan.

### Step 1: Initialize Repositories & Environments
- **1.1** Create a Git repository (`air-ambulance-dashboard/`).
- **1.2** Push the folder structure (empty placeholders, `.gitignore`, `README.md`).
- **1.3** In AWS or local dev environment, install Node and Postgres. Create an empty database named `air_ambulance_db`.

### Step 2: Backend Boilerplate
- **2.1** In `backend/`, run `npm init` (or `pip install` if Python).
- **2.2** Install dependencies (if Node):
  ```bash
  npm install express cors pg pg-hstore axios dotenv ...
  ```
- **2.3** Create `src/app.js` (for Node) or `main.py` (for Python) with a simple “Hello World” API endpoint.
- **2.4** Connect to the Postgres database using environment variables. Test that the connection is successful.

### Step 3: Database Setup
- **3.1** Define schema (tables for `flights`, `competitor_flights`, `schedules`, etc.).
  - `flights`: For storing flight ID, aircraft tail, status, actual dep/arr, positions, etc.
  - `competitor_flights`: For competitor tail numbers, operator, flight times.
  - `schedules`: For planned flights (aircraft ID, scheduled dep/arr).
- **3.2** Create migrations or run SQL to create these tables. Ensure referencing constraints or indexes as needed.

### Step 4: Flight Data Service (Backend Integration)
- **4.1** In `services/flightData.service.js`, implement logic to call external API (FlightRadar24/OpenSky).
- **4.2** Expose endpoints in `controllers/flightController.js` for:
  - `GET /api/flights/active` -> returns current positions for our fleet.
  - `GET /api/flights/history/:flightId` -> returns historical data for a specific flight.
- **4.3** Handle caching: store results in memory or short-term Redis if needed. Respect API rate limits.

### Step 5: Competitor Tracking Service
- **5.1** In `services/competitor.service.js`, implement a daily fetch for competitor flights:
  - Possibly run a cron job or scheduled function that fetches competitor data once per day (or more frequently if desired).
  - Store in `competitor_flights` table with date/time, route, etc.
- **5.2** Create endpoints in `competitorController.js`:
  - `GET /api/competitors/daily` -> returns competitor flights data grouped by competitor.
  - `POST /api/competitors/update` -> triggers manual fetch (optional).
- **5.3** Ensure minimal API calls to keep costs low.

### Step 6: React Frontend Setup
- **6.1** In `frontend/`, run:
  ```bash
  npx create-react-app .
  ```
  or your preferred React scaffolding.
- **6.2** Update `public/logo.png` with your provided logo. 
- **6.3** In `src/App.js`, create basic layout:
  - Nav bar with logo
  - Side menu or top tabs (Dashboard, Competitors, Reports)
  - Placeholder content area

### Step 7: Live Flight Map
- **7.1** Install Leaflet & dependencies:
  ```bash
  npm install leaflet react-leaflet
  ```
- **7.2** Create `components/MapView.js`:
  - Implement a map that fetches `/api/flights/active` every X seconds to update markers.
  - Use our branding colors for markers or a default icon. 
- **7.3** Display basic flight info on marker popup (flight ID, altitude, speed).

### Step 8: Schedule vs Actual UI
- **8.1** Create `controllers/scheduleController.js` for reading/writing schedule data. 
- **8.2** In the frontend, add a table `components/FlightTable.js`:
  - Columns: Aircraft, Scheduled Dep, Actual Dep, Scheduled Arr, Actual Arr, Delay
  - Fetch data from `/api/schedule/today` (which in turn compares actual flight status).
- **8.3** Highlight delays or deviations in red. On-time flights in green.

### Step 9: Operational Summaries & KPIs
- **9.1** Implement logic in backend (`reportController.js` or `services/report.service.js`) to compute:
  - # of flights today, average delay, total flight hours, on-time percentage, etc.
- **9.2** In the frontend, add `KPIStats.js` to display these metrics as cards at the top of the dashboard.
- **9.3** Optionally integrate Chart.js or Recharts for a line chart of flights over time (day/week/month).

### Step 10: Competitor Panel & Visualization
- **10.1** Add a “Competitor” tab/page (e.g. `pages/CompetitorView.js`) that fetches data from `/api/competitors/daily`.
- **10.2** Display competitor flights in a grouped list or simple bar chart (our flights vs competitor flights).
- **10.3** Provide a toggle on the main map to show competitor markers. Use a distinct color or icon for each competitor group.

### Step 11: Alerts & Notification
- **11.1** Create a background job (`alerts.service.js`) to check for:
  - Delayed departures (difference between scheduled dep and actual > 15 min)
  - Excessive ground time
  - Route deviations (if we have lat/long route definitions)
- **11.2** If triggered, store alerts in a DB table `alerts` or send email notifications using NodeMailer + AWS SES. 
- **11.3** In frontend, add an `AlertsPanel.js` to display a list of active alerts or historical alerts.

### Step 12: Automated Reports
- **12.1** Create a daily job (cron) that generates summary data from the previous day. 
- **12.2** Format a PDF or CSV with stats (e.g. flight hours, delays, competitor highlights). 
- **12.3** Email the report to designated ops staff or store it in a `reports` table for download via the frontend.

### Step 13: Testing & Integration
- **13.1** Write unit tests (in `backend/tests/`) for controllers/services. 
- **13.2** Perform integration tests for major endpoints. 
- **13.3** Test the UI with sample data to ensure everything appears correct. 
- **13.4** Conduct user acceptance testing with ops team.

### Step 14: Performance & Cost Optimization
- **14.1** Add caching or reduce poll intervals for flight data if hitting API limits. 
- **14.2** Scale down the EC2 instance usage or shift to AWS Lambda if needed. 
- **14.3** Monitor AWS cost and set budgets/alerts to avoid overage.

### Step 15: Deployment
- **15.1** Create a production build of the frontend (`npm run build`) and either:
  - Serve it via the Node.js backend (static files), or
  - Upload it to an S3 bucket + enable CloudFront.
- **15.2** For the backend, deploy to the EC2 instance or container platform (Docker).
- **15.3** Configure environment variables in AWS (API keys, DB creds).
- **15.4** Point your domain (e.g. `https://example-your-url.com`) to the EC2 or S3/CloudFront distribution. 
- **15.5** Test live site, confirm all features (map, schedule data, competitor display, etc.).

### Step 16: Final Handover & Documentation
- **16.1** Document all endpoints and usage in `docs/`. 
- **16.2** Provide instructions in `README.md` on how to run the project locally, how to set up environment variables, and how to deploy.
- **16.3** Congratulations – MVP complete!

---

## 5. Connections & Data Flow Overview

```
[Frontend React App] <--> [Backend (Node/Express)] <--> [PostgreSQL RDS]
                                |
                                v
                          [Flight Data API]
                          [Competitor Data]
```

1. **React Frontend** calls the **Backend** for:
   - Flight positions
   - Scheduled flights
   - Competitor flights
   - Alerts
   - Summaries/Reports

2. **Backend** (Node) retrieves data from:
   - **PostgreSQL** for storing/retrieving flight logs, competitor logs, schedules, alerts.
   - **Flight Data API** (FlightRadar24/OpenSky) for live updates.
   - Possibly caches results to reduce calls/cost.
   - Performs scheduled tasks (cron) for daily competitor tracking & daily summaries.

3. **Database** (Postgres) stores:
   - Our flight logs (positions, times)
   - Competitor flight data
   - Schedules
   - Generated reports
   - Alerts history

4. **End Users** access the dashboard at:
   `https://example-your-url.com`
   - They log in (if authentication is needed).
   - See real-time map & metrics.
   - View competitor tab for competitor flights.
   - Receive alerts/reports via email or in-dashboard notifications.

---

## 6. Checklist for LLM Compliance

**LLM or developer** must follow these guidelines to avoid deviating from the MVP objective:

1. **Folder Structure** – Create and maintain the exact structure or minimal variations.  
2. **Tech Stack** – Use the specified frameworks/libraries (Node + Express or Python + FastAPI, React, Leaflet, PostgreSQL).  
3. **API Integration** – Integrate only the planned flight data provider (OpenSky or FlightRadar24).  
4. **Competitor Tracking** – Implement once-daily or relevant scheduling, store in separate DB table.  
5. **Map Implementation** – Must use Leaflet with distinct markers for our fleet vs competitors.  
6. **Alerts** – Must implement scheduled checks for delays, deviations, etc.  
7. **Daily Summaries/Reports** – Automatic email or PDF generation is required.  
8. **Cost Optimization** – Use caching, avoid excessive API calls, leverage AWS free tier.  
9. **Deployment** – Must be deployed to an AWS environment with a working domain URL.  
10. **End-to-End Testing** – Confirm each major feature in a production-like environment.

If any step or feature is unclear, reference **this plan** and do **not** deviate into unplanned functionality. The end objective is a **fully functional MVP** aligned with the provided architecture and feature set.

---

**This completes the final project plan file** that outlines all details for the **Enhanced Air Ambulance Fleet Tracking Dashboard**. This document should remain the **single source of truth** for both humans and LLMs to ensure no feature creep or deviations occur.