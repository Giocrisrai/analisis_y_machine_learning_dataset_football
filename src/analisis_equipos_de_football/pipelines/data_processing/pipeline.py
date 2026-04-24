"""Pipeline Kedro: capa de preparación → tabla única para todos los modelos.

En docencia: contrastar con ``sklearn.pipeline.Pipeline`` (este archivo orquesta
*proyecto*: leer del catálogo, ejecutar nodo, escribir Parquet según ``catalog.yml``).
"""

from kedro.pipeline import Pipeline, node

from .nodes import build_ml_features_table


def create_pipeline(**kwargs) -> Pipeline:
    """Un nodo: Match → `features_for_ml` (vía ``catalog``)."""
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
