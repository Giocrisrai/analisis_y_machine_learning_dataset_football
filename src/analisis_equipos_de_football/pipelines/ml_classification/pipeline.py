from kedro.pipeline import Pipeline, node

from .nodes import train_classification_bundle


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                train_classification_bundle,
                inputs={
                    "features_for_ml": "features_for_ml",
                    "split": "params:split",
                    "classification": "params:classification",
                },
                outputs=[
                    "classification_metrics",
                    "classification_model",
                    "classification_feature_importance",
                ],
                name="train_classification_bundle_node",
            ),
        ]
    )
