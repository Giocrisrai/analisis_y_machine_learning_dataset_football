"""Preparación de datos (CRISP-DM: fase «Data preparation»).

Responsabilidad: transformar la tabla `Match` en una fila analítica por partido
lista para entrenar modelos. Misma lógica que en `02_preparacion_datos.ipynb`.

Orden lógico en el proyecto:
  raw (SQLite) → este nodo → `features_for_ml` (Parquet) → pipelines de ML.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def build_ml_features_table(match: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla de modelado: cuotas, goles y etiqueta de resultado.

    Pasos (útiles para explicar en pizarra o informe):
      1. Comprobar columnas mínimas: goles y cuotas B365.
      2. Derivar `outcome` multiclase a partir de la diferencia de goles
         (no se predice con datos posteriores al partido; solo explicamos
         el mapeo etiqueta↔gol).
      3. Quedarse solo con filas con las tres cuotas presentes
         (``dropna`` en B365) para evitar entrenar con ausencias estructurales.

    Codificación de ``outcome`` (alineada con los notebooks y clasificación):
      - 0: gana visita
      - 1: empate
      - 2: gana local
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
