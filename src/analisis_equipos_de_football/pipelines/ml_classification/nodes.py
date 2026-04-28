"""Clasificación multiclase: predecir resultado (visita / empate / local).

Flujo didáctico (alinear con notebooks 03 y 05 y con ``modelos_y_flujo_integrado.md``):

1. **Entrada** — DataFrame ``features_for_ml`` (mismas filas y columnas que en
   preparación; columnas de features y target vienen de ``params:classification``).
2. **Partición** — Un solo ``train_test_split``; en clasificación se usa
   *estratificación* cuando cada clase tiene suficientes ejemplos (ver
   ``_train_test_maybe_stratify``); evita desbalance extremo train/test.
3. **Banco de modelos** — Varios estimadores (lineales con escala, k-NN, bosques);
   hiperparámetros **fijos en este archivo**; split/columnas en ``parameters.yml``.
4. **Selección del "mejor"** — Por **F1 macro** en el conjunto de *test* (misma
   regla para todos; en investigación se discutiría validación cruzada o corte
   temporal).
5. **Salida** — Métricas (JSON), estimador entrenado (.pkl), importancia por
   permutación (CSV) sobre el modelo ganador y ``X_test``.

Nota de configuración: ``conf/base/parameters.yml`` controla *qué* columnas y
*qué* fracción de test; los *números* internos de cada algoritmo (``C``,
``n_estimators``, etc.) viven aquí salvo que el curso mueva esos dicts a YAML.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline as SkPipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

# Mínimo de filas para no romper entrenamiento en bases sintéticas pequeñas.
_MIN_ROWS_FOR_TRAINING = 10
# sklearn exige al menos 2 ejemplos por clase para stratify; si no, se omite.
_MIN_CLASS_COUNT_FOR_STRATIFY = 2


def _jsonable(obj: Any) -> Any:
    """Convierte tipos numpy / anidados a estructura serializable en JSON (métricas)."""
    if hasattr(obj, "item"):
        return obj.item()
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list | tuple):
        return [_jsonable(x) for x in obj]
    if isinstance(obj, float | int | str | bool) or obj is None:
        return obj
    return str(obj)


def _train_test_maybe_stratify(
    X: pd.DataFrame,
    y: pd.Series,
    *,
    test_size: float,
    random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Partición train/test, con estratificación solo cuando sklearn la permite.

    Con pocas filas o clases casi vacías, ``stratify=y`` lanza error; se reintenta
    sin estratificar para que ``kedro run`` no falle en datos mínimos de práctica.
    """
    kwargs: dict[str, Any] = {
        "test_size": test_size,
        "random_state": random_state,
    }
    if y.nunique() > 1 and y.value_counts().min() >= _MIN_CLASS_COUNT_FOR_STRATIFY:
        kwargs["stratify"] = y
    try:
        return train_test_split(X, y, **kwargs)
    except ValueError:
        kwargs.pop("stratify", None)
        return train_test_split(X, y, **kwargs)


def train_classification_bundle(
    features_for_ml: pd.DataFrame,
    split: dict[str, Any],
    classification: dict[str, Any],
) -> tuple[dict[str, Any], Any, pd.DataFrame]:
    """Entrena varios clasificadores, elige el mejor por F1 macro y explica con permutación.

    Args:
        features_for_ml: Tabla ya preparada (mismo esquema que el Parquet de Kedro).
        split: Desde ``params:split`` — ``test_size``, ``random_state``.
        classification: Desde ``params:classification`` — ``feature_columns``, ``target``.

    Returns:
        Tupla ``(metrics_dict, best_estimator, importance_df)`` para el catálogo
        (JSON, Pickle, CSV respectivamente).
    """
    feat_cols = list(classification["feature_columns"])
    target = classification["target"]
    missing = [c for c in feat_cols + [target] if c not in features_for_ml.columns]
    if missing:
        msg = f"Faltan columnas en features_for_ml: {missing}"
        raise ValueError(msg)
    if len(features_for_ml) < _MIN_ROWS_FOR_TRAINING:
        msg = (
            f"Se necesitan al menos {_MIN_ROWS_FOR_TRAINING} filas en "
            "features_for_ml para clasificación."
        )
        raise ValueError(msg)

    X = features_for_ml[feat_cols]
    y = features_for_ml[target]

    # --- Partición reproducible (semilla desde YAML) ---
    X_train, X_test, y_train, y_test = _train_test_maybe_stratify(
        X,
        y,
        test_size=split["test_size"],
        random_state=split["random_state"],
    )

    # --- Modelos: sklearn Pipeline = preprocesar una fila (escala + clasificador) ---
    # Lineales y k-NN llevan StandardScaler; árboles suelen ir sin escala (invariante
    # a reordenar umbrales por columna de forma monótona). Ver guía de modelos.
    knn_neighbors = min(15, len(X_train))
    models: dict[str, Any] = {
        "LogisticRegression": SkPipeline(
            [
                ("scale", StandardScaler()),
                ("clf", LogisticRegression(max_iter=2_000, solver="lbfgs")),
            ]
        ),
        "LinearSVC": SkPipeline(
            [
                ("scale", StandardScaler()),
                (
                    "clf",
                    LinearSVC(dual=False, max_iter=5_000, random_state=42),
                ),
            ]
        ),
        f"KNN_k{knn_neighbors}": SkPipeline(
            [
                ("scale", StandardScaler()),
                (
                    "clf",
                    KNeighborsClassifier(
                        n_neighbors=knn_neighbors,
                        weights="distance",
                    ),
                ),
            ]
        ),
        "RandomForest": RandomForestClassifier(
            n_estimators=200,
            max_depth=16,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=1,
        ),
        "HistGradientBoosting": HistGradientBoostingClassifier(
            max_iter=200,
            max_depth=6,
            learning_rate=0.08,
            random_state=42,
        ),
    }

    # --- Misma métrica de ranking para todos (F1 macro en test) ---
    leaderboard: list[dict[str, Any]] = []
    best_name = ""
    best_f1 = -1.0
    best_est: Any = None

    for name, est in models.items():
        est.fit(X_train, y_train)
        pred = est.predict(X_test)
        f1_macro = float(f1_score(y_test, pred, average="macro"))
        leaderboard.append(
            {
                "model": name,
                "accuracy": float(accuracy_score(y_test, pred)),
                "f1_macro": f1_macro,
                "f1_weighted": float(f1_score(y_test, pred, average="weighted")),
            }
        )
        if f1_macro > best_f1:
            best_f1 = f1_macro
            best_name = name
            best_est = est

    assert best_est is not None
    y_pred_best = best_est.predict(X_test)
    report = classification_report(
        y_test,
        y_pred_best,
        labels=[0, 1, 2],
        target_names=["away_win", "draw", "home_win"],
        output_dict=True,
        zero_division=0,
    )

    # --- Explicabilidad: solo el estimador elegido, sobre el mismo test ---
    # n_jobs=1: importancia por permutación usa joblib/loky; 1 evita fallos en CI/sandboxes
    # restringidos; con pocas filas el tiempo sigue siendo aceptable en docencia.
    perm = permutation_importance(
        best_est,
        X_test,
        y_test,
        n_repeats=15,
        random_state=split["random_state"],
        n_jobs=1,
    )
    importance = pd.DataFrame(
        {
            "feature": feat_cols,
            "importance_mean": perm.importances_mean,
            "importance_std": perm.importances_std,
        }
    ).sort_values("importance_mean", ascending=False)

    metrics: dict[str, Any] = {
        "task": "classification",
        "target": target,
        "features": feat_cols,
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "best_model": best_name,
        "leaderboard": leaderboard,
        "classification_report": _jsonable(report),
    }
    return metrics, best_est, importance
