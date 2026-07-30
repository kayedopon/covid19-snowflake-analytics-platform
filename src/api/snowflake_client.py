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

def get_country_history(country):
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
        ORDER BY YEAR
    """

    cursor.execute(query, (country,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def get_countries():
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    query = """
        SELECT DISTINCT COUNTRY_REGION
        FROM COVID_DEMOGRAPHIC_ANALYSIS
        WHERE COUNTRY_REGION IS NOT NULL
        ORDER BY COUNTRY_REGION
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def get_top_cases(year, limit):
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            COUNTRY_REGION,
            CASES_PER_100K
        FROM COVID_DEMOGRAPHIC_ANALYSIS
        WHERE YEAR = %s
          AND CASES_PER_100K IS NOT NULL
        ORDER BY CASES_PER_100K DESC
        LIMIT %s
    """

    cursor.execute(query, (year, limit))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def get_top_deaths(year, limit):
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            COUNTRY_REGION,
            DEATHS_PER_100K
        FROM COVID_DEMOGRAPHIC_ANALYSIS
        WHERE YEAR = %s
          AND DEATHS_PER_100K IS NOT NULL
        ORDER BY DEATHS_PER_100K DESC
        LIMIT %s
    """

    cursor.execute(query, (year, limit))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def get_density_analysis(year):
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            DENSITY_QUARTILE,
            ROUND(AVG(CASES_PER_100K), 2) AS AVG_CASES_PER_100K,
            ROUND(AVG(DEATHS_PER_100K), 2) AS AVG_DEATHS_PER_100K
        FROM COVID_DEMOGRAPHIC_ANALYSIS
        WHERE YEAR = %s
          AND DENSITY_QUARTILE IS NOT NULL
        GROUP BY DENSITY_QUARTILE
        ORDER BY DENSITY_QUARTILE
    """

    cursor.execute(query, (year,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows

def get_gdp_analysis(year):
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            GDP_QUARTILE,
            ROUND(AVG(CASES_PER_100K), 2) AS AVG_CASES_PER_100K,
            ROUND(AVG(DEATHS_PER_100K), 2) AS AVG_DEATHS_PER_100K
        FROM COVID_DEMOGRAPHIC_ANALYSIS
        WHERE YEAR = %s
          AND GDP_QUARTILE IS NOT NULL
        GROUP BY GDP_QUARTILE
        ORDER BY GDP_QUARTILE
    """

    cursor.execute(query, (year,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows