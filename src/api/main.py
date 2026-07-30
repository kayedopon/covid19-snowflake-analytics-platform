from fastapi import FastAPI, HTTPException

from src.api.schemas import AnnotationCreate, AnnotationUpdate
from src.api.snowflake_client import (
    get_covid_data,
    get_country_history,
    get_countries,
    get_top_cases,
    get_top_deaths,
    get_density_analysis,
    get_gdp_analysis,
    get_country_comparison
)
from src.nosql.mongodb import create_annotation, get_annotations, update_annotation, delete_annotation


app = FastAPI(
    title="COVID-19 data Analytics API",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "COVID-19 Analytics API is running"}

#endpoints to Snowflake
@app.get("/covid/{country}")
def country_history(country: str):
    rows = get_country_history(country)

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Country not found"
        )

    return [
        {
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
        for row in rows
    ]

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

@app.get("/covid/top/cases/{year}")
def top_cases(year: int, limit: int = 10):
    rows = get_top_cases(year, limit)

    return [
        {
            "country": row[0],
            "cases_per_100k": row[1]
        }
        for row in rows
    ]

@app.get("/covid/top/deaths/{year}")
def top_deaths(year: int, limit: int = 10):
    rows = get_top_deaths(year, limit)

    return [
        {
            "country": row[0],
            "deaths_per_100k": row[1]
        }
        for row in rows
    ]

@app.get("/analytics/countries")
def countries():
    rows = get_countries()

    return [
        row[0]
        for row in rows
    ]

@app.get("/analytics/density/{year}")
def density_analysis(year: int):
    rows = get_density_analysis(year)

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No density analysis available"
        )

    return [
        {
            "density_quartile": row[0],
            "avg_cases_per_100k": row[1],
            "avg_deaths_per_100k": row[2]
        }
        for row in rows
    ]

@app.get("/analytics/gdp/{year}")
def gdp_analysis(year: int):
    rows = get_gdp_analysis(year)

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No GDP analysis available"
        )

    return [
        {
            "gdp_quartile": row[0],
            "avg_cases_per_100k": row[1],
            "avg_deaths_per_100k": row[2]
        }
        for row in rows
    ]

@app.get("/analytics/comparison/{year}")
def country_comparison(year: int):
    rows = get_country_comparison(year)

    return [
        {
            "country": row[0],
            "population": row[1],
            "population_density": row[2],
            "gdp_per_capita": row[3],
            "cases_per_100k": row[4],
            "deaths_per_100k": row[5],
            "case_fatality_rate": row[6]
        }
        for row in rows
    ]

# endpoints to MongoDB
@app.get("/annotations/{country}/{year}")
def read_annotations(country: str, year: int):
    results = get_annotations(country, year)

    for annotation in results:
        annotation["_id"] = str(annotation["_id"])

    return results

@app.post("/annotations")
def add_annotation(annotation: AnnotationCreate):
    annotation_id = create_annotation(
        country=annotation.country,
        year=annotation.year,
        metric=annotation.metric,
        comment=annotation.comment,
        author=annotation.author
    )

    return {
        "message": "Annotation sucessfully created",
        "id": annotation_id
    }

@app.put("/annotations/{annotation_id}")
def edit_annotation(
    annotation_id: str,
    annotation: AnnotationUpdate
):
    updated = update_annotation(
        annotation_id,
        annotation.comment
    )

    if updated == 0:
        raise HTTPException(
            status_code=404,
            detail="Annotation not found"
        )

    return {
        "message": "Annotation sucessfully updated"
    }

@app.delete("/annotations/{annotation_id}")
def remove_annotation(annotation_id: str):
    deleted = delete_annotation(annotation_id)

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Annotation not found"
        )

    return {
        "message": "Annotation sucessfully deleted"
    }