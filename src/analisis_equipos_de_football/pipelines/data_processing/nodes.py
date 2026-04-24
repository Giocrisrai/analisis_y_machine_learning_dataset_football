"""Nodos de preparación de datos para modelado."""

from __future__ import annotations

import numpy as np
import pandas as pd


def build_ml_features_table(match: pd.DataFrame) -> pd.DataFrame:
    """Une goles, outcome y cuotas Bet365 (filas con cuotas completas).

    Outcome: 0 visita, 1 empate, 2 local — igual que en el notebook de exploración.
    """
    required = [
        "home_team_goal",
        "away_team_goal",
        "B365H",
        "B365D",
        "B365A",
    ]
    missing = [c for c in required if c not in match.columns]
    if missing:
        msg = f"Faltan columnas en la tabla Match: {missing}"
        raise ValueError(msg)

    goal_diff = match["home_team_goal"] - match["away_team_goal"]
    outcome = np.select(
        [goal_diff > 0, goal_diff == 0, goal_diff < 0],
        [2, 1, 0],
    )
    feat_cols = ["B365H", "B365D", "B365A"]
    cols = feat_cols + ["home_team_goal", "away_team_goal"]
    df = match[cols].copy()
    df["outcome"] = outcome
    df = df.dropna(subset=feat_cols)
    return df.reset_index(drop=True)
