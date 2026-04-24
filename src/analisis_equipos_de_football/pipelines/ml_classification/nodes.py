"""Entrenamiento y evaluación de clasificación multiclase (resultado del partido)."""

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


def _jsonable(obj: Any) -> Any:
    if hasattr(obj, "item"):
        return obj.item()
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list | tuple):
        return [_jsonable(x) for x in obj]
    if isinstance(obj, float | int | str | bool) or obj is None:
        return obj
    return str(obj)


def train_classification_bundle(
    features_for_ml: pd.DataFrame,
    split: dict[str, Any],
    classification: dict[str, Any],
) -> tuple[dict[str, Any], Any, pd.DataFrame]:
    feat_cols = list(classification["feature_columns"])
    target = classification["target"]
    X = features_for_ml[feat_cols]
    y = features_for_ml[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=split["test_size"],
        random_state=split["random_state"],
        stratify=y,
    )

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
        "KNN_k15": SkPipeline(
            [
                ("scale", StandardScaler()),
                ("clf", KNeighborsClassifier(n_neighbors=15, weights="distance")),
            ]
        ),
        "RandomForest": RandomForestClassifier(
            n_estimators=200,
            max_depth=16,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
        ),
        "HistGradientBoosting": HistGradientBoostingClassifier(
            max_iter=200,
            max_depth=6,
            learning_rate=0.08,
            random_state=42,
        ),
    }

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
        target_names=["away_win", "draw", "home_win"],
        output_dict=True,
        zero_division=0,
    )

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
