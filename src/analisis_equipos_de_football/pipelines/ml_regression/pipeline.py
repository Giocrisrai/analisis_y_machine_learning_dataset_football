from kedro.pipeline import Pipeline, node

from .nodes import train_regression_bundle


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                train_regression_bundle,
                inputs={
                    "features_for_ml": "features_for_ml",
                    "split": "params:split",
                    "regression": "params:regression",
                },
                outputs=[
                    "regression_metrics",
                    "regression_model",
                    "regression_feature_importance",
                ],
                name="train_regression_bundle_node",
            ),
        ]
    )
