from fastapi import FastAPI, HTTPException

from src.api.schemas import AnnotationCreate, AnnotationUpdate
from src.api.snowflake_client import get_covid_data
from src.nosql.mongodb import create_annotation, get_annotations, update_annotation, delete_annotation


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