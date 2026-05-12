"""DAG Airflow mínimo: bootstrap SQLite minimal + Kedro estándar del proyecto."""

from __future__ import annotations

import os
import textwrap
from datetime import UTC, datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.bash import BashOperator


def _kedro_repo_root(start: Path) -> Path:
    resolved = start.resolve()
    for parent in (resolved, *resolved.parents):
        if (parent / "pyproject.toml").exists() and (parent / "src").exists():
            return parent
    raise RuntimeError(
        "No se encontró la raíz del proyecto Kedro. Exporta FOOTBALL_KEDRO_PROJECT_ROOT "
        "con la carpeta donde está este repositorio o coloca este DAG físicamente bajo él.",
    )


def _resolve_project_root() -> Path:
    """Raíz Kedro desde env absoluto (opcional) o buscando hacia arriba desde este fichero."""
    raw = os.environ.get("FOOTBALL_KEDRO_PROJECT_ROOT", "").strip()
    if raw:
        return Path(raw).resolve()
    return _kedro_repo_root(Path(__file__))


def _bash_body(root: Path) -> str:
    posix = root.as_posix()
    return textwrap.dedent(
        f"""
        set -euo pipefail
        cd "{posix}"

        if command -v uv >/dev/null 2>&1; then
          uv sync --extra dev --extra infra
          uv run python scripts/bootstrap_data.py --source minimal --force
          export KEDRO_DISABLE_TELEMETRY=1
          uv run python -m kedro run
        else
          if [ -f .venv/bin/activate ]; then
            # shellcheck disable=SC1091
            source .venv/bin/activate
          fi
          python scripts/bootstrap_data.py --source minimal --force
          export KEDRO_DISABLE_TELEMETRY=1
          python -m kedro run
        fi
        """.strip(),
    )


_REPO_ROOT = _resolve_project_root()

with DAG(
    dag_id="football_kedro_default_pipeline",
    default_args={
        "owner": "analisis-equipos",
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="Bootstrap SQLite minimal + kedro run (analisis-equipos).",
    schedule=None,
    start_date=datetime(2026, 1, 1, tzinfo=UTC),
    catchup=False,
    tags=["kedro", "ml", "docencia"],
) as kedro_ml_dag:
    BashOperator(
        task_id="bootstrap_and_run_kedro",
        bash_command=_bash_body(_REPO_ROOT),
    )
