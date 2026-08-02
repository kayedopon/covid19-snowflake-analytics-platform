# COVID-19 Snowflake Analytics Platform

This project integrates COVID-19 epidemiological data with population, GDP per capita, and population-density data.

It provides:

- Snowflake analytical storage
- PySpark data ingestion and transformation
- FastAPI backend
- Dash and Plotly dashboard
- Redis API caching
- MongoDB annotations
- XGBoost and Prophet forecasting
- K-Means country clustering
- Snowflake query optimization experiments
- Docker Compose deployment

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
│   ├── optimization.sql
│   └── patterns.sql
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
├── Dockerfile.ingestion
├── docker-compose.yml
├── requirements_ingestion.txt
├── requirements.txt
└── README.md
```

## Requirements

You need:

- Docker
- Docker Compose
- a Snowflake account
- permission to add a dataset from Snowflake Marketplace

Check Docker:

```bash
docker --version
docker compose version
```

## 1. Add the Snowflake Marketplace Dataset

In Snowflake Marketplace, add the free COVID-19 epidemiological dataset used by this project.

The project expects this table to be available:

```text
COVID19_EPIDEMIOLOGICAL_DATA.PUBLIC.JHU_COVID_19
```

The role used by the project must be able to read this table.

## 2. Configure `.env`

Create a `.env` file in the project root.

Use the following structure:

```env
SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_URL=your_account.snowflakecomputing.com
SNOWFLAKE_ACCOUNT=your_account_identifier

MONGO_URI=mongodb://mongodb:27017
MONGO_DATABASE=covid_analytics

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_TTL=500
```


The Docker services use the Compose service names:

```text
mongodb
redis
```

Therefore, inside Docker:

```env
MONGO_URI=mongodb://mongodb:27017
REDIS_HOST=redis
```

`localhost` should not be used for MongoDB or Redis inside the API container because it would refer to the API container itself.

The Snowflake user must be able to:

- use the configured warehouse;
- read the Marketplace COVID-19 dataset;
- create and use the `COVID_ANALYTICS` database;
- create schemas, tables, views, and temporary stages.
## 3. Create the Snowflake Database and Schemas

Run this in Snowflake before ingestion:

```sql
CREATE DATABASE IF NOT EXISTS COVID_ANALYTICS;
CREATE SCHEMA IF NOT EXISTS COVID_ANALYTICS.EXTERNAL_DATA;
CREATE SCHEMA IF NOT EXISTS COVID_ANALYTICS.ANALYTICS;
```

The PySpark ingestion job creates the table, but the target database and schema must already exist.

## 4. Run the PySpark Ingestion

The ingestion job runs in a separate Docker container that includes Java and PySpark. No local Java or PySpark installation is required.

From the project root, run:

```bash
docker compose --profile ingestion run --rm ingestion
```

The ingestion pipeline:

1. reads the external demographic files from `data/`;
2. transforms the population dataset from wide to long format;
3. keeps the years 2020–2023;
4. normalizes country names;
5. joins population, GDP per capita, and population-density data;
6. validates missing values;
7. writes the result to Snowflake.

Expected output table:

```text
COVID_ANALYTICS.EXTERNAL_DATA.COUNTRY_DEMOGRAPHICS
```

Verify it in Snowflake:

```sql
SELECT COUNT(*)
FROM COVID_ANALYTICS.EXTERNAL_DATA.COUNTRY_DEMOGRAPHICS;

SELECT *
FROM COVID_ANALYTICS.EXTERNAL_DATA.COUNTRY_DEMOGRAPHICS
LIMIT 10;
```

The first ingestion run may take longer because Spark downloads the Snowflake connector and JDBC dependencies.

## 5. Create the Analytical Views

After ingestion finishes, execute:

```text
sql/integration.sql
```

Run the file in Snowflake using the same account and role configured for the project.

The main analytical view expected by the API is:

```text
COVID_ANALYTICS.ANALYTICS.COVID_DEMOGRAPHIC_ANALYSIS
```

Verify it:

```sql
SELECT *
FROM COVID_ANALYTICS.ANALYTICS.COVID_DEMOGRAPHIC_ANALYSIS
LIMIT 10;
```

## 6. Start the Application

From the project root, run:

```bash
docker compose up -d --build
```

This starts:

- FastAPI
- Dash dashboard
- Redis
- MongoDB

Check the containers:

```bash
docker compose ps
```

## 7. Open the Application

Dashboard:

```text
http://localhost:8050
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
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
GET    /annotations/{country}/{year}
POST   /annotations
PUT    /annotations/{annotation_id}
DELETE /annotations/{annotation_id}
```

## Run Forecasting

Make sure the application containers are running, then execute:

```bash
docker compose exec api python -m src.forecasting.run_forecast
```

Forecasting results are saved to:

```text
outputs/forecasting/
```

The forecasting pipeline compares:

- XGBoost
- Prophet
- naive persistence baseline

## Run Clustering

Make sure the application containers are running, then execute:

```bash
docker compose exec api python -m src.clustering.run_clustering
```

Clustering results are saved to:

```text
outputs/clustering/
```

The clustering pipeline uses country-level COVID-19 outcomes from 2020–2022 and evaluates different values of `k`.

## Redis Caching

Check Redis:

```bash
docker compose exec redis redis-cli PING
```

Expected result:

```text
PONG
```

Show cached keys:

```bash
docker compose exec redis redis-cli KEYS "*"
```

Clear the cache:

```bash
docker compose exec redis redis-cli FLUSHDB
```

Repeated API requests should return an `X-Cache: HIT` response header while a first uncached request returns `X-Cache: MISS`.

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

View MongoDB logs:

```bash
docker compose logs -f mongodb
```

Rebuild after code changes:

```bash
docker compose up -d --build
```

Stop and remove the application containers:

```bash
docker compose down
```

Stop the application and remove its volumes:

```bash
docker compose down -v
```

Use `-v` only when stored MongoDB and Redis volume data can be deleted.

## SQL Files

```text
sql/EDA.sql
```

Contains exploratory SQL queries for the JHU COVID-19 dataset.

```text
sql/integration.sql
```

Creates the integrated country-year analytical views required by the API and dashboard.

```text
sql/optimization.sql
```

Contains Snowflake query-optimization experiments.


## Complete Setup Order

```text
1. Add the COVID-19 dataset from Snowflake Marketplace
2. Add Snowflake credentials to .env
3. Create COVID_ANALYTICS and its schemas
4. Run the Dockerized PySpark ingestion
5. Execute sql/integration.sql in Snowflake
6. Start the application with Docker Compose
7. Open FastAPI and the Dash dashboard
```
