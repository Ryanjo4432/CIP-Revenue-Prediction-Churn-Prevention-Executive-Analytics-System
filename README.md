# CIP — Customer Intelligence & Revenue Optimization Platform

End-to-end SaaS-style platform for churn prediction, revenue forecasting, CLV modeling, and executive analytics. Fully containerized with Docker.

---

## Architecture

```
React Frontend (port 3000)
        ↓
FastAPI Backend (port 8000)
        ↓
PostgreSQL Database (port 5432)
        ↓
ML Service — FastAPI (port 8001)
        ↓
Analytics Engine + Recommendation Engine
```

---

## Tech Stack

| Layer       | Tech                              |
|-------------|-----------------------------------|
| Frontend    | React 18, Tailwind CSS, Recharts  |
| Backend     | FastAPI, SQLAlchemy, Pydantic      |
| Database    | PostgreSQL 16                     |
| ML          | Scikit-learn, Pandas, NumPy       |
| Auth        | JWT (HS256), bcrypt               |
| DevOps      | Docker, Docker Compose            |
| Tests       | pytest, SQLite (test db)          |

---

## Getting Started

### Prerequisites
- Docker Desktop running

### Run everything

```bash
git clone https://github.com/Ryanjo4432/CIP-Revenue-Prediction-Churn-Prevention-Executive-Analytics-System.git
cd CIP-Revenue-Prediction-Churn-Prevention-Executive-Analytics-System
docker compose up --build
```

| Service  | URL                          |
|----------|------------------------------|
| Frontend | http://localhost:3000        |
| Backend  | http://localhost:8000        |
| API Docs | http://localhost:8000/docs   |
| ML       | http://localhost:8001        |
| ML Docs  | http://localhost:8001/docs   |

---

## Project Structure

```
├── frontend/                  # React + Tailwind dashboard
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       └── components/
│           ├── KPICards.jsx
│           ├── CustomerTable.jsx
│           ├── RevenueChart.jsx
│           └── RecommendationCenter.jsx
│
├── backend/                   # FastAPI backend
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       ├── auth.py
│       ├── customers.py
│       ├── transactions.py
│       ├── predictions.py
│       ├── recommendations.py
│       └── analytics.py
│
├── ml/                        # ML service
│   ├── ml_service.py
│   ├── churn_model.py
│   ├── revenue_forecast.py
│   └── clv_model.py
│
├── analytics/
│   └── kpi_engine.py
│
├── recommendation_engine/
│   └── rules.py
│
├── database/
│   └── init.sql
│
├── tests/
│   ├── conftest.py
│   ├── test_customers.py
│   ├── test_transactions.py
│   ├── test_auth.py
│   └── test_ml.py
│
└── docker-compose.yml
```

---

## API Reference

### Auth
| Method | Endpoint         | Description        |
|--------|------------------|--------------------|
| POST   | /auth/register   | Create account     |
| POST   | /auth/login      | Get JWT token      |
| GET    | /auth/me         | Current user info  |

### Customers
| Method | Endpoint              | Description          |
|--------|-----------------------|----------------------|
| GET    | /customers            | List all customers   |
| POST   | /customers            | Create customer      |
| GET    | /customers/{id}       | Get one customer     |
| PUT    | /customers/{id}       | Update customer      |
| DELETE | /customers/{id}       | Delete customer      |

### Transactions
| Method | Endpoint                        | Description                    |
|--------|---------------------------------|--------------------------------|
| GET    | /transactions                   | List all transactions          |
| POST   | /transactions                   | Create transaction             |
| GET    | /transactions/customer/{id}     | Transactions for one customer  |
| DELETE | /transactions/{id}              | Delete transaction             |

### ML & Predictions
| Method | Endpoint                   | Description                    |
|--------|----------------------------|--------------------------------|
| POST   | /predictions/run/churn     | Run churn model on all         |
| POST   | /predictions/run/clv       | Run CLV model on all           |
| POST   | /predictions/run/forecast  | Run revenue forecast           |
| GET    | /predictions               | Get stored predictions         |

### Analytics
| Method | Endpoint                      | Description              |
|--------|-------------------------------|--------------------------|
| GET    | /analytics/kpi                | Full KPI report          |
| GET    | /analytics/monthly-revenue    | Revenue by month         |
| GET    | /analytics/top-customers      | Top customers by spend   |
| GET    | /analytics/revenue-by-category| Revenue by category      |

### Recommendations
| Method | Endpoint                          | Description                 |
|--------|-----------------------------------|-----------------------------|
| POST   | /recommendations/generate         | Generate all recommendations|
| GET    | /recommendations                  | List all                    |
| GET    | /recommendations/customer/{id}    | Recs for one customer       |

---

## ML Models

### Churn Prediction
- **Algorithm:** Random Forest Classifier
- **Features:** age, location, days since join, transaction count, total spend, avg transaction, days since last transaction
- **Output:** churn probability 0.0 – 1.0

### Revenue Forecasting
- **Algorithm:** Linear Regression on monthly revenue
- **Output:** predicted revenue for next N months + trend direction

### Customer Lifetime Value
- **Method:** monthly spend rate × recency score × 24-month projection
- **Segments:** champion / loyal / potential / at-risk

---

## Recommendation Engine

Rules fire based on churn probability and CLV:

| Condition                        | Action                                      |
|----------------------------------|---------------------------------------------|
| Churn ≥ 70%                      | Send retention email with 20% discount      |
| Churn ≥ 85%                      | Escalate to account manager                 |
| Churn ≥ 70% + CLV ≥ $2000        | Offer free premium upgrade 3 months         |
| Churn 40–70%                     | Re-engagement email                         |
| Churn < 40% + CLV ≥ $5000        | Thank you gift + early feature access       |
| Churn < 40% + CLV ≥ $2000        | Upsell to enterprise plan                   |

---

## Running Tests

```bash
cd backend
pip install -r requirements.txt
pip install pytest httpx

cd ../tests
pytest -v
```

---

## Dashboard

| Tab              | What it shows                                          |
|------------------|--------------------------------------------------------|
| Overview         | Revenue, AOV, churn rate, retention, CLV, top customers|
| Customers        | All customers with churn risk color coding + search    |
| Forecast         | Historical vs predicted revenue chart                  |
| Recommendations  | Action cards filtered by priority (high/medium/low)    |
