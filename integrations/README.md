# Integraciones opcionales: Databricks, DVC y Airflow

Este directorio agrupa artefactos de **órquestación y datos** que amplían el flujo Kedro base. Todo es **opcional** para estudiantes: el curso puede seguir con `kedro run` y `make verify` sin nada de esto instalado.

| Pieza | Qué aporta | Punto de partida |
|-------|-------------|-------------------|
| **DVC** | Versionado reproducible del Parquet, modelos `.pkl`, métricas e importancia (SQLite queda gestionado por bootstrap/Git como en clase) | [`dvc.yaml`](../dvc.yaml) + [`integrations/dvc/`](./dvc/) |
| **Airflow** | Programación y dependencias sobre el proyecto (cron, SLA, retries). | `integrations/airflow/` |
| **Databricks** | Ejecución en Lakehouse: Repos, Jobs, Delta opcional y Asset Bundles. | `integrations/databricks/` |

Índice de guías cortas dentro de cada subcarpeta; la guía unificada vive en [../docs/DATABRICKS_DVC_AIRFLOW.md](../docs/DATABRICKS_DVC_AIRFLOW.md).
