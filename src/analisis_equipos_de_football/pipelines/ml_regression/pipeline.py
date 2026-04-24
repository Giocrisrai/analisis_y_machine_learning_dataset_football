"""Pipeline Kedro: regresión (p. ej. goles del local).

Misma separación que en clasificación: ``params:split`` y ``params:regression``
en YAML; arquitectura numérica (Ridge, bosques, boosting) en ``nodes.py``.
"""

from kedro.pipeline import Pipeline, node

from .nodes import train_regression_bundle


def create_pipeline(**kwargs) -> Pipeline:
    """Un nodo: misma tabla de features + `params:regression` → artefactos de regresión."""
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
