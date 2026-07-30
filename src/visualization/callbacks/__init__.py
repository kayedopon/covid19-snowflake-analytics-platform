from src.visualization.callbacks.overview import (
    register_overview_callbacks
)

from src.visualization.callbacks.comparisons import (
    register_comparison_callbacks
)

from src.visualization.callbacks.relationships import (
    register_relationship_callbacks
)

from src.visualization.callbacks.insights import (
    register_insight_callbacks
)

from src.visualization.callbacks.annotations import (
    register_annotation_callbacks
)


def register_callbacks(app):

    register_overview_callbacks(app)

    register_comparison_callbacks(app)

    register_relationship_callbacks(app)

    register_insight_callbacks(app)

    register_annotation_callbacks(app)