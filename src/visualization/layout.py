from dash import dcc, html

from src.visualization.api_client import get_countries
from src.visualization.styles import PAGE_STYLE, CONTROL_PANEL_STYLE, KPI_CONTAINER_STYLE, CONTEXT_KPI_CONTAINER_STYLE, KPI_CARD_STYLE, TWO_COLUMN_STYLE, CHART_CONTAINER_STYLE, FULL_WIDTH_CHART_STYLE, RELATIONSHIP_FILTER_STYLE, MAP_FILTER_STYLE, ANNOTATION_SECTION_STYLE, ANNOTATION_FORM_STYLE


def create_layout():
    countries = get_countries()

    return html.Div([
        dcc.Location(id="url", refresh=False),

        dcc.Store(id="annotation-refresh", data=0),

        html.Div([
            html.H1("COVID-19 Analytics Dashboard", style={"marginBottom": "5px"}),
            html.P(
                "Interactive analysis of COVID-19 outcomes together with population, population density and GDP indicators.",
                style={"color": "#555", "marginTop": "5px"}
            )
        ]),

        html.Div([
            html.Div([
                html.Label("Country"),
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[{"label": country, "value": country} for country in countries],
                    value="Lithuania",
                    clearable=False,
                    persistence=True,
                    persistence_type="session"
                )
            ]),

            html.Div([
                html.Label("Year"),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=[{"label": year, "value": year} for year in [2020, 2021, 2022, 2023]],
                    value=2021,
                    clearable=False,
                    persistence=True,
                    persistence_type="session"
                )
            ]),

            html.Div([
                html.Label("Top N countries"),
                dcc.Dropdown(
                    id="limit-dropdown",
                    options=[
                        {"label": "5", "value": 5},
                        {"label": "10", "value": 10},
                        {"label": "15", "value": 15},
                        {"label": "20", "value": 20}
                    ],
                    value=10,
                    clearable=False,
                    persistence=True,
                    persistence_type="session"
                )
            ])
        ], style=CONTROL_PANEL_STYLE),

        html.H2("COVID-19 Summary"),

        html.Div([
            html.Div([
                html.Div("Confirmed Cases", style={"color": "#555"}),
                html.H2(id="confirmed-card", style={"marginBottom": "0"})
            ], style=KPI_CARD_STYLE),

            html.Div([
                html.Div("Deaths", style={"color": "#555"}),
                html.H2(id="deaths-card", style={"marginBottom": "0"})
            ], style=KPI_CARD_STYLE),

            html.Div([
                html.Div("Cases per 100k", style={"color": "#555"}),
                html.H2(id="cases-rate-card", style={"marginBottom": "0"})
            ], style=KPI_CARD_STYLE),

            html.Div([
                html.Div("Deaths per 100k", style={"color": "#555"}),
                html.H2(id="deaths-rate-card", style={"marginBottom": "0"})
            ], style=KPI_CARD_STYLE),

            html.Div([
                html.Div("Case Fatality Rate", style={"color": "#555"}),
                html.H2(id="fatality-card", style={"marginBottom": "0"})
            ], style=KPI_CARD_STYLE)
        ], style=KPI_CONTAINER_STYLE),

        html.H2("Country Context"),

        html.Div([
            html.Div([
                html.Div("Population", style={"color": "#555"}),
                html.H2(id="population-card", style={"marginBottom": "0"})
            ], style=KPI_CARD_STYLE),

            html.Div([
                html.Div("Population Density", style={"color": "#555"}),
                html.H2(id="density-card", style={"marginBottom": "0"})
            ], style=KPI_CARD_STYLE),

            html.Div([
                html.Div("GDP per Capita", style={"color": "#555"}),
                html.H2(id="gdp-card", style={"marginBottom": "0"})
            ], style=KPI_CARD_STYLE)
        ], style=CONTEXT_KPI_CONTAINER_STYLE),

        html.H2("Country Overview"),

        html.Div([
            html.Div([dcc.Graph(id="country-cases-history")], style=CHART_CONTAINER_STYLE),
            html.Div([dcc.Graph(id="country-deaths-history")], style=CHART_CONTAINER_STYLE)
        ], style=TWO_COLUMN_STYLE),

        html.Div([
            dcc.Graph(id="country-cfr-history")
        ], style=FULL_WIDTH_CHART_STYLE),

        html.H2("Selected Country vs Global Rate"),

        html.P(
            "The selected country's population-normalized rates are compared with rates calculated across all countries with available population data."
        ),

        html.Div([
            html.Div([dcc.Graph(id="country-global-cases-chart")], style=CHART_CONTAINER_STYLE),
            html.Div([dcc.Graph(id="country-global-deaths-chart")], style=CHART_CONTAINER_STYLE)
        ], style=TWO_COLUMN_STYLE),

        html.H2("International Comparison"),

        html.Div([
            html.Div([dcc.Graph(id="top-cases-chart")], style=CHART_CONTAINER_STYLE),
            html.Div([dcc.Graph(id="top-deaths-chart")], style=CHART_CONTAINER_STYLE)
        ], style=TWO_COLUMN_STYLE),

        html.H2("Global Geographic Distribution"),

        html.Div([
            html.Label("Map Metric"),

            dcc.Dropdown(
                id="map-metric-dropdown",
                options=[
                    {"label": "Cases per 100k", "value": "cases_per_100k"},
                    {"label": "Deaths per 100k", "value": "deaths_per_100k"},
                    {"label": "Case Fatality Rate", "value": "case_fatality_rate"}
                ],
                value="cases_per_100k",
                clearable=False,
                persistence=True,
                persistence_type="session"
            )
        ], style=MAP_FILTER_STYLE),

        html.Div([
            dcc.Graph(id="world-map")
        ], style=FULL_WIDTH_CHART_STYLE),

        html.H2("Population Density Analysis"),

        html.P(
            "Q1 represents countries with the lowest population density, while Q4 represents countries with the highest."
        ),

        html.Div([
            html.Div([dcc.Graph(id="density-cases-chart")], style=CHART_CONTAINER_STYLE),
            html.Div([dcc.Graph(id="density-deaths-chart")], style=CHART_CONTAINER_STYLE)
        ], style=TWO_COLUMN_STYLE),

        html.H2("GDP Analysis"),

        html.P(
            "Q1 represents countries with the lowest GDP per capita, while Q4 represents countries with the highest."
        ),

        html.Div([
            html.Div([dcc.Graph(id="gdp-cases-chart")], style=CHART_CONTAINER_STYLE),
            html.Div([dcc.Graph(id="gdp-deaths-chart")], style=CHART_CONTAINER_STYLE)
        ], style=TWO_COLUMN_STYLE),

        html.H2("Demographic and Economic Relationships"),

        html.P(
            "Explore possible associations between demographic or economic indicators and COVID-19 outcomes. The visualizations show association, not causation."
        ),

        html.Div([
            html.Div([
                html.Label("Factor"),
                dcc.Dropdown(
                    id="factor-dropdown",
                    options=[
                        {"label": "Population Density", "value": "population_density"},
                        {"label": "GDP per Capita", "value": "gdp_per_capita"}
                    ],
                    value="population_density",
                    clearable=False,
                    persistence=True,
                    persistence_type="session"
                )
            ]),

            html.Div([
                html.Label("COVID-19 Outcome"),
                dcc.Dropdown(
                    id="outcome-dropdown",
                    options=[
                        {"label": "Cases per 100k", "value": "cases_per_100k"},
                        {"label": "Deaths per 100k", "value": "deaths_per_100k"},
                        {"label": "Case Fatality Rate", "value": "case_fatality_rate"}
                    ],
                    value="cases_per_100k",
                    clearable=False,
                    persistence=True,
                    persistence_type="session"
                )
            ])
        ], style=RELATIONSHIP_FILTER_STYLE),

        html.Div([
            dcc.Graph(id="relationship-chart")
        ], style=FULL_WIDTH_CHART_STYLE),

        html.H2("Annotations", style={"marginTop": "30px"}),

        html.Div([
            html.H3("Existing Annotations", style={"marginTop": "0"}),

            html.Div(id="annotations-container"),

            html.Div([
                html.H3("Add Annotation", style={"marginTop": "0"}),

                html.Div([
                    html.Div([
                        html.Label("Metric"),
                        dcc.Dropdown(
                            id="annotation-metric",
                            options=[
                                {"label": "Cases per 100k", "value": "CASES_PER_100K"},
                                {"label": "Deaths per 100k", "value": "DEATHS_PER_100K"},
                                {"label": "Case Fatality Rate", "value": "CASE_FATALITY_RATE"}
                            ],
                            placeholder="Select metric",
                            clearable=True
                        )
                    ]),

                    html.Div([
                        html.Label("Author"),
                        dcc.Input(
                            id="annotation-author",
                            type="text",
                            placeholder="Enter author name",
                            persistence=True,
                            persistence_type="session",
                            style={
                                "width": "100%",
                                "padding": "10px",
                                "boxSizing": "border-box"
                            }
                        )
                    ])
                ], style={
                    "display": "grid",
                    "gridTemplateColumns": "1fr 1fr",
                    "gap": "20px",
                    "marginBottom": "15px"
                }),

                html.Label("Comment"),

                dcc.Textarea(
                    id="annotation-comment",
                    placeholder="Write your annotation...",
                    style={
                        "width": "100%",
                        "height": "110px",
                        "padding": "10px",
                        "boxSizing": "border-box",
                        "marginTop": "5px",
                        "marginBottom": "15px",
                        "resize": "vertical"
                    }
                ),

                html.Div([
                    html.Button(
                        "Add Annotation",
                        id="add-annotation-button",
                        n_clicks=0,
                        style={
                            "padding": "10px 18px",
                            "border": "1px solid #aaa",
                            "borderRadius": "8px",
                            "cursor": "pointer",
                            "fontWeight": "bold"
                        }
                    ),

                    html.Div(
                        id="annotation-status",
                        style={
                            "marginLeft": "15px",
                            "alignSelf": "center"
                        }
                    )
                ], style={
                    "display": "flex",
                    "alignItems": "center"
                })
            ], style=ANNOTATION_FORM_STYLE)
        ], style=ANNOTATION_SECTION_STYLE),

        html.P(
            "Note: 2023 data is partial and covers only the period available in the source dataset through March 9, 2023.",
            style={
                "marginTop": "25px",
                "fontStyle": "italic",
                "color": "#666"
            }
        )
    ], style=PAGE_STYLE)