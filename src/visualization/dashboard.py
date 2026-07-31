from dash import Dash

from src.visualization.layout import create_layout

from src.visualization.callbacks import register_callbacks


app = Dash(__name__)

app.title = (
    "COVID-19 Analytics Dashboard"
)

app.layout = create_layout()

register_callbacks(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)