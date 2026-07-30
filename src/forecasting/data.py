import pandas as pd

from src.api.snowflake_client import get_snowflake_connection


def load_daily_cases(country: str) -> pd.DataFrame:

    connection = get_snowflake_connection()

    query = """
        SELECT
            DATE,
            SUM(DIFFERENCE) AS DAILY_CASES
        FROM COVID19_EPIDEMIOLOGICAL_DATA.PUBLIC.JHU_COVID_19
        WHERE COUNTRY_REGION = %s
          AND CASE_TYPE = 'Confirmed'
        GROUP BY DATE
        ORDER BY DATE
    """

    cursor = connection.cursor()
    try:
        cursor.execute(
            query,
            (country,)
        )
        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "date",
                "daily_cases"
            ]
        )

    finally:
        cursor.close()
        connection.close()

    return df


def prepare_daily_cases( df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    # turn invalid data to Nan
    df["daily_cases"] = pd.to_numeric(
        df["daily_cases"],
        errors="coerce"
    )

    df["daily_cases"] = (
        df["daily_cases"]
        .fillna(0)
    )

    # negative DIFFERENCE values usually represent
    # reporting corrections rather than negative infections
    df["daily_cases"] = (
        df["daily_cases"]
        .clip(lower=0)
    )

    # make sure every calendar day is present
    df = (
        df.set_index("date")
        .asfreq("D", fill_value=0)
        .reset_index()
    )

    # calculate 7 day rolling average
    df["cases_7d_avg"] = (
        df["daily_cases"]
        .rolling(window=7, min_periods=1)
        .mean()
    )

    return df