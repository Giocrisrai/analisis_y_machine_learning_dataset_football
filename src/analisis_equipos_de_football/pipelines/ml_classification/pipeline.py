"""Pipeline Kedro: clasificación (resultado del partido).

Parámetros de experimento (columnas, target, fracción test) vienen de
``conf/base/parameters.yml`` vía ``params:split`` y ``params:classification``.
Los hiperparámetros fijos de cada algoritmo están en ``nodes.py`` (docente puede
moverlos a YAML en una variante avanzada del curso).
"""

from kedro.pipeline import Pipeline, node

from .nodes import train_classification_bundle


def create_pipeline(**kwargs) -> Pipeline:
    """Un nodo: Parquet de features + parámetros → métricas, modelo, importancias."""
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
