from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go

from src.visualization.api_client import get_country_year, get_comparison


COUNTRY_MAP_NAMES = {
    "Korea, Republic of": "South Korea",
    "Korea, North": "North Korea",
    "Russian Federation": "Russia",
    "Moldova, Republic of": "Moldova",
    "Bolivia, Plurinational State of": "Bolivia",
    "Iran, Islamic Republic of": "Iran",
    "Lao People's Democratic Republic": "Laos",
    "Palestine, State of": "Palestine",
    "Taiwan, Province of China": "Taiwan",
    "Tanzania, United Republic of": "Tanzania",
    "Venezuela, Bolivarian Republic of": "Venezuela",
    "Viet Nam": "Vietnam",
    "Brunei Darussalam": "Brunei",
    "Congo, The Democratic Republic of the": "Democratic Republic of the Congo"
}


def map_country_name(country):
    return COUNTRY_MAP_NAMES.get(country, country)


def calculate_global_rate(data, metric):
    valid_rows = [
        {
            "population": float(row["population"]),
            "rate": float(row[metric])
        }
        for row in data
        if row.get("population") is not None
        and row.get(metric) is not None
        and float(row["population"]) > 0
    ]

    if not valid_rows:
        return None

    total_population = sum(row["population"] for row in valid_rows)

    estimated_total = sum(
        row["rate"] / 100000 * row["population"]
        for row in valid_rows
    )

    return estimated_total / total_population * 100000


def register_insight_callbacks(app):

    @app.callback(
        Output("country-global-cases-chart", "figure"),
        Output("country-global-deaths-chart", "figure"),

        Input("country-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("url", "pathname")
    )
    def update_global_comparison(country, year, pathname):
        country_response = get_country_year(country, year)
        comparison_data = get_comparison(year)

        if country_response.status_code != 200:
            return go.Figure(), go.Figure()

        country_data = country_response.json()

        country_cases = (
            float(country_data["cases_per_100k"])
            if country_data.get("cases_per_100k") is not None
            else None
        )

        country_deaths = (
            float(country_data["deaths_per_100k"])
            if country_data.get("deaths_per_100k") is not None
            else None
        )

        global_cases = calculate_global_rate(comparison_data, "cases_per_100k")
        global_deaths = calculate_global_rate(comparison_data, "deaths_per_100k")

        cases_figure = go.Figure(
            go.Bar(
                x=[country, "Global"],
                y=[country_cases, global_cases]
            )
        )

        cases_figure.update_layout(
            title=f"{country} vs Global Cases per 100k ({year})",
            xaxis_title="",
            yaxis_title="Cases per 100,000",
            template="plotly_white"
        )

        deaths_figure = go.Figure(
            go.Bar(
                x=[country, "Global"],
                y=[country_deaths, global_deaths]
            )
        )

        deaths_figure.update_layout(
            title=f"{country} vs Global Deaths per 100k ({year})",
            xaxis_title="",
            yaxis_title="Deaths per 100,000",
            template="plotly_white"
        )

        return cases_figure, deaths_figure


    @app.callback(
        Output("world-map", "figure"),

        Input("year-dropdown", "value"),
        Input("map-metric-dropdown", "value"),
        Input("url", "pathname")
    )
    def update_world_map(year, metric, pathname):
        data = get_comparison(year)

        clean_data = [
            {
                **row,
                metric: float(row[metric]),
                "map_country": map_country_name(row["country"])
            }
            for row in data
            if row.get(metric) is not None
        ]

        metric_labels = {
            "cases_per_100k": "Cases per 100k",
            "deaths_per_100k": "Deaths per 100k",
            "case_fatality_rate": "Case Fatality Rate (%)"
        }

        figure = px.choropleth(
            clean_data,
            locations="map_country",
            locationmode="country names",
            color=metric,
            hover_name="country",
            hover_data={
                "map_country": False,
                metric: ":,.2f"
            },
            title=f"{metric_labels[metric]} by Country ({year})",
            color_continuous_scale="Viridis"
        )

        figure.update_geos(
            showcoastlines=True,
            showframe=False
        )

        figure.update_layout(
            template="plotly_white",
            margin=dict(l=0, r=0, t=60, b=0),
            coloraxis_colorbar_title=metric_labels[metric]
        )

        return figure