# COVID-19 Snowflake Analytics Platform

This project combines COVID-19 data from Snowflake with demographic data and provides:

- FastAPI backend
- Dash dashboard
- Redis caching
- MongoDB annotations
- Forecasting with XGBoost and Prophet
- Country clustering
- Snowflake optimization experiments

## Project Structure

```text
COVID19-SNOWFLAKE-ANALYTICS-PLATFORM/
├── data/
├── outputs/
│   ├── clustering/
│   └── forecasting/
├── sql/
│   ├── EDA.sql
│   ├── integration.sql
│   └── optimization.sql
├── src/
│   ├── api/
│   ├── clustering/
│   ├── forecasting/
│   ├── ingestion/
│   ├── nosql/
│   └── visualization/
├── .dockerignore
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Requirements

You need:

- Docker
- Docker Compose
- access to Snowflake
- access to MongoDB Atlas

Check Docker:

```bash
docker --version
docker compose version
```

## 1. Configure `.env`

Create or update the `.env` file in the project root.

Example:

```env
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=COVID_ANALYTICS
SNOWFLAKE_SCHEMA=ANALYTICS

MONGO_URI=your_mongodb_connection_string

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_TTL=500
```

Do not upload `.env` to GitHub.

When the application runs through Docker Compose, the API service connects to Redis using the Docker service name `redis`.

## 2. Start the Application

From the project root run:

```bash
docker compose up --build
```

This starts:

- FastAPI
- Dash dashboard
- Redis

To start everything in the background:

```bash
docker compose up -d --build
```

## 3. Open the Application

Dashboard:

```text
http://localhost:8050
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

## 4. Check Running Containers

```bash
docker compose ps
```

You should see the API, dashboard, and Redis services running.

## 5. Stop the Application

```bash
docker compose down
```

## Useful Docker Commands

View all logs:

```bash
docker compose logs -f
```

View API logs:

```bash
docker compose logs -f api
```

View dashboard logs:

```bash
docker compose logs -f dashboard
```

View Redis logs:

```bash
docker compose logs -f redis
```

Check Redis:

```bash
docker compose exec redis redis-cli PING
```

Expected result:

```text
PONG
```

Clear Redis cache:

```bash
docker compose exec redis redis-cli FLUSHDB
```

Rebuild the application after changes:

```bash
docker compose up -d --build
```

## Main API Endpoints

```text
GET /covid/{country}
GET /covid/{country}/{year}
GET /covid/top/cases/{year}
GET /covid/top/deaths/{year}
GET /analytics/countries
GET /analytics/density/{year}
GET /analytics/gdp/{year}
GET /analytics/comparison/{year}
```

Annotation endpoints:

```text
GET /annotations/{country}/{year}
POST /annotations
PUT /annotations/{annotation_id}
DELETE /annotations/{annotation_id}
```

## Forecasting

Forecasting code is located in:

```text
src/forecasting/
```

Forecasting results are saved to:

```text
outputs/forecasting/
```

## Clustering

Clustering code is located in:

```text
src/clustering/
```

Clustering results are saved to:

```text
outputs/clustering/
```

## SQL

SQL scripts are stored in:

```text
sql/
```

Files:

```text
EDA.sql
integration.sql
optimization.sql
```

## Troubleshooting

If the dashboard is blank or some charts do not load:

```bash
docker compose logs --tail=100 dashboard
```

If the API is not responding:

```bash
docker compose logs --tail=100 api
```

If Redis is not responding:

```bash
docker compose exec redis redis-cli PING
```

If Docker Compose has stale containers:

```bash
docker compose down
docker compose up --build
```
