import os

import snowflake.connector
from dotenv import load_dotenv


load_dotenv()

def get_snowflake_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse="COMPUTE_WH",
        database="COVID_ANALYTICS",
        schema="ANALYTICS"
    )


def get_covid_data(country, year):
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            COUNTRY_REGION,
            YEAR,
            CONFIRMED_CASES,
            DEATHS,
            POPULATION,
            POPULATION_DENSITY,
            GDP_PER_CAPITA,
            CASES_PER_100K,
            DEATHS_PER_100K,
            CASE_FATALITY_RATE
        FROM COVID_DEMOGRAPHIC_ANALYSIS
        WHERE COUNTRY_REGION = %s
          AND YEAR = %s
    """

    cursor.execute(query, (country, year))
    row = cursor.fetchone()

    cursor.close()
    connection.close()

    return row