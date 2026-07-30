from fastapi import FastAPI, HTTPException

from src.api.snowflake_client import get_covid_data


app = FastAPI(
    title="COVID-19 data Analytics API",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "COVID-19 Analytics API is running"}

#endpoints to Snowflake
@app.get("/covid/{country}/{year}")
def covid_data(country: str, year: int):
    row = get_covid_data(country, year)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Data not found"
        )

    return {
        "country": row[0],
        "year": row[1],
        "confirmed_cases": row[2],
        "deaths": row[3],
        "population": row[4],
        "population_density": row[5],
        "gdp_per_capita": row[6],
        "cases_per_100k": row[7],
        "deaths_per_100k": row[8],
        "case_fatality_rate": row[9]
    }
