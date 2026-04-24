"""Regresión: predecir goles del equipo local a partir de cuotas."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline as SkPipeline
from sklearn.preprocessing import StandardScaler

_MIN_ROWS_FOR_TRAINING = 10


def train_regression_bundle(
    features_for_ml: pd.DataFrame,
    split: dict[str, Any],
    regression: dict[str, Any],
) -> tuple[dict[str, Any], Any, pd.DataFrame]:
    feat_cols = list(regression["feature_columns"])
    target = regression["target"]
    missing = [c for c in feat_cols + [target] if c not in features_for_ml.columns]
    if missing:
        msg = f"Faltan columnas en features_for_ml: {missing}"
        raise ValueError(msg)
    if len(features_for_ml) < _MIN_ROWS_FOR_TRAINING:
        msg = (
            f"Se necesitan al menos {_MIN_ROWS_FOR_TRAINING} filas en "
            "features_for_ml para regresión."
        )
        raise ValueError(msg)

    X = features_for_ml[feat_cols]
    y = features_for_ml[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=split["test_size"],
        random_state=split["random_state"],
    )

    models: dict[str, Any] = {
        "Ridge": SkPipeline(
            [
                ("scale", StandardScaler()),
                ("reg", Ridge(alpha=1.0)),
            ]
        ),
        "RandomForestRegressor": RandomForestRegressor(
            n_estimators=200,
            max_depth=16,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
        ),
        "HistGradientBoostingRegressor": HistGradientBoostingRegressor(
            max_iter=200,
            max_depth=6,
            learning_rate=0.08,
            random_state=42,
        ),
    }

    leaderboard: list[dict[str, Any]] = []
    best_name = ""
    best_r2 = -np.inf
    best_est: Any = None

    for name, est in models.items():
        est.fit(X_train, y_train)
        pred = est.predict(X_test)
        mae = float(mean_absolute_error(y_test, pred))
        rmse = float(np.sqrt(mean_squared_error(y_test, pred)))
        r2 = float(r2_score(y_test, pred))
        leaderboard.append(
            {"model": name, "mae": mae, "rmse": rmse, "r2": r2},
        )
        if r2 > best_r2:
            best_r2 = r2
            best_name = name
            best_est = est

    assert best_est is not None
    perm = permutation_importance(
        best_est,
        X_test,
        y_test,
        n_repeats=15,
        random_state=split["random_state"],
        n_jobs=-1,
    )
    importance = pd.DataFrame(
        {
            "feature": feat_cols,
            "importance_mean": perm.importances_mean,
            "importance_std": perm.importances_std,
        }
    ).sort_values("importance_mean", ascending=False)

    y_hat = best_est.predict(X_test)
    metrics: dict[str, Any] = {
        "task": "regression",
        "target": target,
        "features": feat_cols,
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "best_model": best_name,
        "leaderboard": leaderboard,
        "best_on_test": {
            "mae": float(mean_absolute_error(y_test, y_hat)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, y_hat))),
            "r2": float(r2_score(y_test, y_hat)),
        },
    }
    return metrics, best_est, importance
