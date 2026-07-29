import os
from dotenv import load_dotenv


load_dotenv()


def write_to_snowflake(df):
    sf_options = {
        "sfURL": os.getenv("SNOWFLAKE_URL"),
        "sfUser": os.getenv("SNOWFLAKE_USER"),
        "sfPassword": os.getenv("SNOWFLAKE_PASSWORD"),
        "sfDatabase": "COVID_ANALYTICS",
        "sfSchema": "EXTERNAL_DATA",
        "sfWarehouse": "COMPUTE_WH"
    }

    df.write \
        .format("snowflake") \
        .options(**sf_options) \
        .option("dbtable", "COUNTRY_DEMOGRAPHICS") \
        .mode("overwrite") \
        .save()