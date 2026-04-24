"""Project pipelines."""

from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

# Orden estable del `kedro run` (evita depender del orden del filesystem).
_DEFAULT_PIPELINE_ORDER = (
    "data_processing",
    "ml_classification",
    "ml_regression",
)


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines(raise_errors=True)
    modular = {k: v for k, v in pipelines.items() if k != "__default__"}
    ordered = [modular[name] for name in _DEFAULT_PIPELINE_ORDER if name in modular]
    pipelines["__default__"] = sum(ordered) if ordered else pipelines["__default__"]
    return pipelines
