import pandas as pd

from src.api.snowflake_client import get_snowflake_connection


def load_clustering_data():
    connection = get_snowflake_connection()

    query = """
        SELECT
            COUNTRY_REGION,
            YEAR,
            CASES_PER_100K,
            DEATHS_PER_100K,
            CASE_FATALITY_RATE
        FROM COVID_ANALYTICS.ANALYTICS.COVID_DEMOGRAPHIC_ANALYSIS
        WHERE YEAR BETWEEN 2020 AND 2022
          AND CASES_PER_100K IS NOT NULL
          AND DEATHS_PER_100K IS NOT NULL
          AND CASE_FATALITY_RATE IS NOT NULL
        ORDER BY COUNTRY_REGION, YEAR
    """

    cursor = connection.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "country",
                "year",
                "cases_per_100k",
                "deaths_per_100k",
                "case_fatality_rate"
            ]
        )

    finally:
        cursor.close()
        connection.close()

    return df


def prepare_clustering_data(df):
    pivot_df = df.pivot(
        index="country",
        columns="year",
        values=[
            "cases_per_100k",
            "deaths_per_100k",
            "case_fatality_rate"
        ]
    )

    pivot_df.columns = [
        f"{metric}_{year}"
        for metric, year in pivot_df.columns
    ]

    return pivot_df.dropna().reset_index()