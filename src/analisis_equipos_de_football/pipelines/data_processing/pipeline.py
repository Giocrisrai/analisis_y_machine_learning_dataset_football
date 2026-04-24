from kedro.pipeline import Pipeline, node

from .nodes import build_ml_features_table


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                build_ml_features_table,
                inputs="match",
                outputs="features_for_ml",
                name="build_ml_features_table_node",
            ),
        ]
    )
