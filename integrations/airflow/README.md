# Airflow — DAG Kedro incluido

Archivo DAG: **`dags/kedro_football_pipeline.py`**.

Requisitos mínimos del **runtime Airflow**:

- Acceso Bash al directorio donde el repo está despachado.
- Preferible **uv** instalado (`uv`) para ejecutar comandos igual que clase; fallback a `.venv`/Python del sistema configurado antes del worker.

Recomendado **enlace simbólico** desde `$AIRFLOW_HOME/dags/` hacia este fichero en el checkout del repo (`ln -sf …`), porque el DAG deduce automáticamente la raíz Kedro subiendo desde `Path(__file__)`. Si copiás el `.py` aislado, exportá `FOOTBALL_KEDRO_PROJECT_ROOT=/ruta/completa/al/repo`.

Pasos rápidos (desarrollo local):

```bash
export AIRFLOW_HOME=~/airflow
mkdir -p "$AIRFLOW_HOME/dags"
export FOOTBALL_KEDRO_PROJECT_ROOT=/ruta/completa/al/repo
ln -sf "$FOOTBALL_KEDRO_PROJECT_ROOT/integrations/airflow/dags/kedro_football_pipeline.py" \
       "$AIRFLOW_HOME/dags/football_kedro_pipeline.py"
airflow standalone
```

Después en la UI, despertar manualmente el DAG `football_kedro_default_pipeline` (parte `schedule=None`).
