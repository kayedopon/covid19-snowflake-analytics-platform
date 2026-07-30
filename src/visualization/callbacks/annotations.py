from datetime import datetime

from dash import (
    Input,
    Output,
    State,
    html,
    no_update
)

from src.visualization.api_client import get_annotations, create_annotation

from src.visualization.styles import ANNOTATION_CARD_STYLE


def format_datetime(value):

    if not value:
        return None

    try:
        date = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

        return date.strftime(
            "%Y-%m-%d %H:%M"
        )

    except (ValueError, AttributeError):
        return str(value)


def register_annotation_callbacks(app):

    @app.callback(
        Output(
            "annotations-container",
            "children"
        ),

        Input(
            "country-dropdown",
            "value"
        ),

        Input(
            "year-dropdown",
            "value"
        ),

        Input(
            "annotation-refresh",
            "data"
        )
    )
    def update_annotations(
        country,
        year,
        refresh
    ):

        data = get_annotations(
            country,
            year
        )

        if not data:
            return html.P(
                "No annotations available.",
                style={
                    "color": "#666"
                }
            )

        annotation_cards = []

        for annotation in data:

            created_at = format_datetime(
                annotation.get(
                    "created_at"
                )
            )

            updated_at = format_datetime(
                annotation.get(
                    "updated_at"
                )
            )

            if updated_at:
                date_text = (
                    f"Updated: {updated_at}"
                )

            elif created_at:
                date_text = (
                    f"Created: {created_at}"
                )

            else:
                date_text = (
                    "Date unavailable"
                )

            card = html.Div([

                html.Div([

                    html.Strong(
                        annotation.get(
                            "metric",
                            "General"
                        )
                    ),

                    html.Span(
                        f"{country} · {year}",
                        style={
                            "color": "#666",
                            "fontSize": "14px"
                        }
                    )

                ], style={
                    "display": "flex",
                    "justifyContent":
                        "space-between",
                    "alignItems": "center"
                }),

                html.P(
                    annotation["comment"],
                    style={
                        "marginTop": "12px",
                        "marginBottom": "12px"
                    }
                ),

                html.Div([

                    html.Span(
                        "Author: "
                        f"{annotation.get('author') or 'Unknown'}"
                    ),

                    html.Span(
                        date_text
                    )

                ], style={
                    "display": "flex",
                    "justifyContent":
                        "space-between",
                    "color": "#666",
                    "fontSize": "13px"
                })

            ], style=ANNOTATION_CARD_STYLE)

            annotation_cards.append(card)

        return annotation_cards


    @app.callback(
        Output(
            "annotation-status",
            "children"
        ),

        Output(
            "annotation-refresh",
            "data"
        ),

        Output(
            "annotation-metric",
            "value"
        ),

        Output(
            "annotation-comment",
            "value"
        ),

        Input(
            "add-annotation-button",
            "n_clicks"
        ),

        State(
            "country-dropdown",
            "value"
        ),

        State(
            "year-dropdown",
            "value"
        ),

        State(
            "annotation-metric",
            "value"
        ),

        State(
            "annotation-comment",
            "value"
        ),

        State(
            "annotation-author",
            "value"
        ),

        State(
            "annotation-refresh",
            "data"
        ),

        prevent_initial_call=True
    )
    def add_annotation(
        n_clicks,
        country,
        year,
        metric,
        comment,
        author,
        refresh
    ):

        if not metric or not comment:

            return (
                html.Span(
                    "Metric and comment are required.",
                    style={
                        "color": "#a00"
                    }
                ),
                no_update,
                no_update,
                no_update
            )

        payload = {
            "country": country,
            "year": year,
            "metric": metric,
            "comment": comment,
            "author": author
        }

        response = create_annotation(
            payload
        )

        if response.status_code in (
            200,
            201
        ):

            return (
                html.Span(
                    "Annotation added successfully.",
                    style={
                        "color": "#287a3d"
                    }
                ),

                (refresh or 0) + 1,

                None,

                ""
            )

        return (
            html.Span(
                "Failed to add annotation.",
                style={
                    "color": "#a00"
                }
            ),
            no_update,
            no_update,
            no_update
        )