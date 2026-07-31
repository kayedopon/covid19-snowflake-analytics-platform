from dash import Input, Output
import plotly.graph_objects as go

from src.visualization.api_client import get_top_cases, get_top_deaths, get_density_analysis, get_gdp_analysis


def register_comparison_callbacks(app):

    @app.callback(
        Output("top-cases-chart", "figure"),

        Input("year-dropdown", "value"),
        Input("limit-dropdown", "value"),
        Input("url", "pathname")
    )
    def update_top_cases(year, limit, pathname):
        data = get_top_cases(year, limit)

        countries = [row["country"] for row in data]
        values = [float(row["cases_per_100k"]) for row in data]

        figure = go.Figure(
            go.Bar(
                x=values,
                y=countries,
                orientation="h"
            )
        )

        figure.update_layout(
            title=f"Top {limit} countries by cases per 100k ({year})",
            xaxis_title="Cases per 100,000",
            yaxis_title="Country",
            template="plotly_white",
            height=max(400, limit * 35),
            margin=dict(l=40, r=20, t=60, b=40),
            yaxis={"categoryorder": "total ascending"}
        )

        return figure


    @app.callback(
        Output("top-deaths-chart", "figure"),

        Input("year-dropdown", "value"),
        Input("limit-dropdown", "value"),
        Input("url", "pathname")
    )
    def update_top_deaths(year, limit, pathname):
        data = get_top_deaths(year, limit)

        countries = [row["country"] for row in data]
        values = [float(row["deaths_per_100k"]) for row in data]

        figure = go.Figure(
            go.Bar(
                x=values,
                y=countries,
                orientation="h"
            )
        )

        figure.update_layout(
            title=f"Top {limit} countries by deaths per 100k ({year})",
            xaxis_title="Deaths per 100,000",
            yaxis_title="Country",
            template="plotly_white",
            height=max(400, limit * 35),
            margin=dict(l=40, r=20, t=60, b=40),
            yaxis={"categoryorder": "total ascending"}
        )

        return figure


    @app.callback(
        Output("density-cases-chart", "figure"),
        Output("density-deaths-chart", "figure"),

        Input("year-dropdown", "value"),
        Input("url", "pathname")
    )
    def update_density(year, pathname):
        data = get_density_analysis(year)

        quartiles = [f"Q{row['density_quartile']}" for row in data]

        cases = [
            float(row["avg_cases_per_100k"])
            if row["avg_cases_per_100k"] is not None
            else None
            for row in data
        ]

        deaths = [
            float(row["avg_deaths_per_100k"])
            if row["avg_deaths_per_100k"] is not None
            else None
            for row in data
        ]

        cases_figure = go.Figure(
            go.Bar(
                x=quartiles,
                y=cases
            )
        )

        cases_figure.update_layout(
            title=f"Cases per 100k by density quartile ({year})",
            xaxis_title="Population Density Quartile",
            yaxis_title="Average cases per 100,000",
            template="plotly_white"
        )

        deaths_figure = go.Figure(
            go.Bar(
                x=quartiles,
                y=deaths
            )
        )

        deaths_figure.update_layout(
            title=f"Deaths per 100k by density quartile ({year})",
            xaxis_title="Population Density Quartile",
            yaxis_title="Average deaths per 100,000",
            template="plotly_white"
        )

        return cases_figure, deaths_figure


    @app.callback(
        Output("gdp-cases-chart", "figure"),
        Output("gdp-deaths-chart", "figure"),

        Input("year-dropdown", "value"),
        Input("url", "pathname")
    )
    def update_gdp(year, pathname):
        data = get_gdp_analysis(year)

        quartiles = [f"Q{row['gdp_quartile']}" for row in data]

        cases = [
            float(row["avg_cases_per_100k"])
            if row["avg_cases_per_100k"] is not None
            else None
            for row in data
        ]

        deaths = [
            float(row["avg_deaths_per_100k"])
            if row["avg_deaths_per_100k"] is not None
            else None
            for row in data
        ]

        cases_figure = go.Figure(
            go.Bar(
                x=quartiles,
                y=cases
            )
        )

        cases_figure.update_layout(
            title=f"Cases per 100k by GDP quartile ({year})",
            xaxis_title="GDP per Capita Quartile",
            yaxis_title="Average cases per 100,000",
            template="plotly_white"
        )

        deaths_figure = go.Figure(
            go.Bar(
                x=quartiles,
                y=deaths
            )
        )

        deaths_figure.update_layout(
            title=f"Deaths per 100k by GDP quartile ({year})",
            xaxis_title="GDP per Capita Quartile",
            yaxis_title="Average deaths per 100,000",
            template="plotly_white"
        )

        return cases_figure, deaths_figure