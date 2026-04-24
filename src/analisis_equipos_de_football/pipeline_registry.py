"""Registro de pipelines: orden del ``kedro run`` y pipelines por nombre.

En clase: el pipeline **__default__** encadena, en secuencia fija:
``data_processing`` → ``ml_classification`` → ``ml_regression`` (misma
dependencia lógica que en ``docs/guias/modelos_y_flujo_integrado.md``).
Cada fase se puede ejecutar aislada: ``kedro run --pipeline data_processing``.
"""

from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

# Orden explícito (no alfabético del filesystem) para lecciones reproducibles.
_DEFAULT_PIPELINE_ORDER = (
    "data_processing",
    "ml_classification",
    "ml_regression",
)


def register_pipelines() -> dict[str, Pipeline]:
    """Devuelve todos los pipelines del paquete y define ``__default__`` como la suma ordenada.

    Returns:
        Diccionario nombre → ``Pipeline``; ``__default__`` es el flujo completo
        de enseñanza (preparar tabla → entrenar clasificación → regresión).
    """
    pipelines = find_pipelines(raise_errors=True)
    modular = {k: v for k, v in pipelines.items() if k != "__default__"}
    ordered = [modular[name] for name in _DEFAULT_PIPELINE_ORDER if name in modular]
    pipelines["__default__"] = sum(ordered) if ordered else pipelines["__default__"]
    return pipelines
