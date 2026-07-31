import requests
import os


API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def get_countries():
    response = requests.get(
        f"{API_URL}/analytics/countries",
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_country_year(country, year):
    response = requests.get(
        f"{API_URL}/covid/{country}/{year}",
        timeout=10
    )

    return response


def get_country_history(country):
    response = requests.get(
        f"{API_URL}/covid/{country}",
        timeout=10
    )
    response.raise_for_status()

    return response.json()


def get_top_cases(year, limit):
    response = requests.get(
        f"{API_URL}/covid/top/cases/{year}?limit={limit}",
        timeout=10
    )
    response.raise_for_status()

    return response.json()


def get_top_deaths(year, limit):
    response = requests.get(
        f"{API_URL}/covid/top/deaths/{year}?limit={limit}",
        timeout=10
    )
    response.raise_for_status()

    return response.json()


def get_density_analysis(year):
    response = requests.get(
        f"{API_URL}/analytics/density/{year}",
        timeout=10
    )
    response.raise_for_status()

    return response.json()


def get_gdp_analysis(year):
    response = requests.get(
        f"{API_URL}/analytics/gdp/{year}",
        timeout=10
    )
    response.raise_for_status()

    return response.json()


def get_comparison(year):
    response = requests.get(
        f"{API_URL}/analytics/comparison/{year}",
        timeout=10
    )
    response.raise_for_status()

    return response.json()


def get_annotations(country, year):
    response = requests.get(
        f"{API_URL}/annotations/{country}/{year}",
        timeout=10
    )
    response.raise_for_status()

    return response.json()


def create_annotation(payload):
    response = requests.post(
        f"{API_URL}/annotations",
        json=payload,
        timeout=10
    )

    return response