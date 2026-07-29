import os
from datetime import datetime, timezone

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
host = os.getenv("MONGO_HOST")

mongo_uri = (
    f"mongodb+srv://{username}:{password}@{host}/"
    f"?appName=Cluster0"
)

client = MongoClient(mongo_uri)

db = client["covid_analytics"]
annotations = db["annotations"]

def create_annotation(country, year, metric, comment, author="anonymous"):
    document = {
        "country": country,
        "year": year,
        "metric": metric,
        "comment": comment,
        "author": author,
        "created_at": datetime.now(timezone.utc)
    }

    result = annotations.insert_one(document)

    return str(result.inserted_id)

def get_annotations(country, year=None):
    query = {
        "country": country
    }

    if year is not None:
        query["year"] = year

    results = annotations.find(query)

    return list(results)

def update_annotation(
    annotation_id,
    comment
):
    result = annotations.update_one(
        {
            
            "_id": ObjectId(annotation_id)
        },
        {
            "$set": {
                "comment": comment,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )

    return result.modified_count

def delete_annotation(annotation_id):
    result = annotations.delete_one(
        {
            "_id": ObjectId(annotation_id)
        }
    )

    return result.deleted_count


if __name__ == "__main__":
    client.admin.command("ping")
    print("MongoDB connection successful")

    annotation_id = create_annotation(
        country="Lithuania",
        year=2023,
        metric="DEATHS_PER_100K",
        comment="Mortality decreased significantly during early 2022.",
        author="Kirill"
    )

    print("Created:", annotation_id)

    print("\nAnnotations:")
    for annotation in get_annotations("Lithuania"):
        print(annotation)

    update_annotation(
        annotation_id,
        "Updated comment about Lithuania mortality."
    )

    print("\nAfter update:")
    for annotation in get_annotations("Lithuania", 2021):
        print(annotation)

    delete_annotation(annotation_id)

    print("\nAfter delete:")
    for annotation in get_annotations("Lithuania", 2021):
        print(annotation)

    annotations.create_index([
        ("country", 1),
        ("year", 1)
    ])

    # Create ascending index on country and year for faster search queries
    # annotations.create_index([
    #     ("country", 1),
    #     ("year", 1)
    # ])]

    validator = {
        "$jsonSchema": {
            "bsonType": "object",

            "required": [
                "country",
                "year",
                "metric",
                "comment"
            ],
            "properties": {
                "country": {
                    "bsonType": "string"
                },
                
                "year": {
                    "bsonType": "int",
                    "minimum": 2020,
                    "maximum": 2023
                },

                "metric": {
                    "bsonType": "string"
                },

                "comment": {
                    "bsonType": "string"
                }
            }
        }
    }

    db.command({
        "collMod": "annotations",
        "validator": validator,
        "validationLevel": "strict",
        "validationAction": "error"
    })