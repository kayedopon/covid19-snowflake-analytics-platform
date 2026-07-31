from dash import Input, Output
import plotly.graph_objects as go

from src.visualization.api_client import get_country_year, get_country_history


def register_overview_callbacks(app):

    @app.callback(
        Output("confirmed-card", "children"),
        Output("deaths-card", "children"),
        Output("cases-rate-card", "children"),
        Output("deaths-rate-card", "children"),
        Output("fatality-card", "children"),
        Output("population-card", "children"),
        Output("density-card", "children"),
        Output("gdp-card", "children"),
        Input("country-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("url", "pathname")
    )
    def update_cards(country, year, pathname):
        response = get_country_year(country, year)

        if response.status_code != 200:
            return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

        data = response.json()

        confirmed = f"{float(data['confirmed_cases']):,.0f}" if data.get("confirmed_cases") is not None else "N/A"
        deaths = f"{float(data['deaths']):,.0f}" if data.get("deaths") is not None else "N/A"

        cases_rate = f"{float(data['cases_per_100k']):,.2f}" if data.get("cases_per_100k") is not None else "N/A"
        deaths_rate = f"{float(data['deaths_per_100k']):,.2f}" if data.get("deaths_per_100k") is not None else "N/A"
        fatality = f"{float(data['case_fatality_rate']):.2f}%" if data.get("case_fatality_rate") is not None else "N/A"

        population = f"{float(data['population']):,.0f}" if data.get("population") is not None else "N/A"
        density = f"{float(data['population_density']):,.2f}" if data.get("population_density") is not None else "N/A"
        gdp = f"${float(data['gdp_per_capita']):,.2f}" if data.get("gdp_per_capita") is not None else "N/A"

        return confirmed, deaths, cases_rate, deaths_rate, fatality, population, density, gdp

    @app.callback(
        Output("country-cases-history", "figure"),
        Output("country-deaths-history", "figure"),
        Output("country-cfr-history", "figure"),

        Input("country-dropdown", "value"),
        Input("url", "pathname")
    )
    def update_country_history(country, pathname):
        data = get_country_history(country)

        years = [row["year"] for row in data]
        cases = [float(row["cases_per_100k"]) if row["cases_per_100k"] is not None else None for row in data]
        deaths = [float(row["deaths_per_100k"]) if row["deaths_per_100k"] is not None else None for row in data]
        fatality = [float(row["case_fatality_rate"]) if row["case_fatality_rate"] is not None else None for row in data]

        cases_figure = go.Figure(
            go.Scatter(
                x=years,
                y=cases,
                mode="lines+markers",
                name="Cases per 100k"
            )
        )

        cases_figure.update_layout(
            title=f"Cases per 100k in {country}",
            xaxis_title="Year",
            yaxis_title="Cases per 100,000",
            template="plotly_white",
            margin=dict(l=40, r=20, t=60, b=40)
        )

        deaths_figure = go.Figure(
            go.Scatter(
                x=years,
                y=deaths,
                mode="lines+markers",
                name="Deaths per 100k"
            )
        )

        deaths_figure.update_layout(
            title=f"Deaths per 100k in {country}",
            xaxis_title="Year",
            yaxis_title="Deaths per 100,000",
            template="plotly_white",
            margin=dict(l=40, r=20, t=60, b=40)
        )

        cfr_figure = go.Figure(
            go.Scatter(
                x=years,
                y=fatality,
                mode="lines+markers",
                name="Case Fatality Rate"
            )
        )

        cfr_figure.update_layout(
            title=f"Case Fatality Rate in {country}",
            xaxis_title="Year",
            yaxis_title="Case Fatality Rate (%)",
            template="plotly_white",
            margin=dict(l=40, r=20, t=60, b=40)
        )

        return cases_figure, deaths_figure, cfr_figure