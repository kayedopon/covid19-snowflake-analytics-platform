from dash import Input, Output
import plotly.express as px

from src.visualization.api_client import get_comparison


def register_relationship_callbacks(app):

    @app.callback(
        Output("relationship-chart", "figure"),

        Input("year-dropdown", "value"),
        Input("factor-dropdown", "value"),
        Input("outcome-dropdown", "value"),
        Input("url", "pathname")
    )
    def update_relationship(year, factor, outcome, pathname):
        data = get_comparison(year)

        clean_data = []

        for row in data:
            if row.get(factor) is None:
                continue

            if row.get(outcome) is None:
                continue

            if row.get("population") is None:
                continue

            clean_row = row.copy()

            clean_row[factor] = float(row[factor])
            clean_row[outcome] = float(row[outcome])
            clean_row["population"] = float(row["population"])

            clean_data.append(clean_row)

        factor_labels = {
            "population_density": "Population Density",
            "gdp_per_capita": "GDP per Capita"
        }

        outcome_labels = {
            "cases_per_100k": "Cases per 100k",
            "deaths_per_100k": "Deaths per 100k",
            "case_fatality_rate": "Case Fatality Rate (%)"
        }

        figure = px.scatter(
            clean_data,
            x=factor,
            y=outcome,
            hover_name="country",
            size="population",
            title=f"{factor_labels[factor]} vs {outcome_labels[outcome]} ({year})"
        )

        figure.update_layout(
            xaxis_title=factor_labels[factor],
            yaxis_title=outcome_labels[outcome],
            template="plotly_white",
            margin=dict(l=40, r=20, t=60, b=40)
        )

        return figure