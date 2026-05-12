# Databricks, DVC y Apache Airflow (uso opcional con este proyecto)

El núcleo del curso sigue siendo **Jupyter + Kedro + `make verify`**. Esta guía enlaza prácticamente **Lakehouse**, **versionado de datos** y **orquestación** cuando la institución ya usa esa pila.

| Integración | Qué aporta | Punto de partida |
|-------------|-------------|-------------------|
| **DVC** | Histórico de Parquet, modelos `.pkl`, métricas JSON e importancia CSV ante un objeto remoto | `dvc.yaml` + `integrations/dvc/README.md` |
| **Airflow** | Calendario, retries, SLA sobre el proyecto. | `integrations/airflow/` |
| **Databricks** | Repos, Jobs, Delta opcional, bundles. | `integrations/databricks/README.md` |

---

## DVC

1. Sincronizar dependencias extras:

   ```bash
   uv sync --extra dev --extra infra
   ```

2. Crear remote (ejemplo NFS local; usar S3/Azure/GCP en equipo real):

   ```bash
   dvc remote add -d equipo_store path/o/url/del/remoto
   ```

3. Reproducir pipeline versionado (= bootstrap mínimo + `kedro run`):

   ```bash
   make dvc-repro
   dvc dag
   dvc push
   ```

`dvc.lock` debe versionarse en Git; blobs viven en el remote configurado.

> **SQLite y Git LFS:** `database.sqlite` puede estar en el repositorio para la clase. **No es un output declarado (`outs`) en DVC**, por eso sólo aparece dentro del comando `kedro_ml` (generando la variante sintética mínima antes de Kedro cuando corres `dvc repro`). Haz copia antes si conservas una réplica grande distinta del dataset docente.

> **`.gitkeep`:** los artefactos versionados por DVC se listan **como ficheros concretos** (Parquet, `.pkl`, JSON y CSV del catálogo) para coexistir con los `.gitkeep` del template Kedro.

---

## Apache Airflow

Instala Airflow en un virtualenv **ajeno** al del proyecto Kedro si quieres evitar conflictos de dependencias grandes (consulta instalación oficial fijando *constraints URL*).

Ejemplo rápido (ajusta rutas):

```bash
export AIRFLOW_HOME=~/airflow
export FOOTBALL_KEDRO_PROJECT_ROOT=/abs/path/analisis-equipos-de-football
mkdir -p "$AIRFLOW_HOME/dags"
ln -sf "$FOOTBALL_KEDRO_PROJECT_ROOT/integrations/airflow/dags/kedro_football_pipeline.py" \
      "$AIRFLOW_HOME/dags/football_kedro_pipeline.py"
airflow standalone
```

El DAG `football_kedro_default_pipeline` arranca **`uv sync`** (dev+infra si hay `uv`) y luego ejecuta Kedro. Alternativa: define la Variable Airflow `FOOTBALL_KEDRO_PROJECT_ROOT`.

---

## Databricks

Camino habitual en clase:

1. **Databricks Repos**: importar este Git repo.
2. En el Repo, ejecutar notebooks con `%pip install -e .` cuando haga falta.
3. Ejecutar `06_pipeline_Kedro.ipynb` para mostrar parity con `kedro run`.

Migración opcional para datasets grandes:

- Registrar salidas grandes (`features_for_ml`, modelos…) en **Unity Catalog Delta** paralelamente a SQLite de laboratorio cambiando el catálogo Kedro cuando el equipo esté maduro para ello — no es requisito del template base.

El fichero **`integrations/databricks/bundle.yaml.example`** es una plantilla; copia valores reales tras `databricks bundle init` oficial y validar con:

```bash
databricks bundle validate
```

---

## Checklist rápido

| Escenario recomendado | Acción |
|-----------------------|--------|
| Sólo asignatura | Ignorar estas integraciones. |
| Almacenes compartidos + revisiones datos | Habilitar DVC + remote. |
| Producción institucional | Airflow llamando Kedro desde VM con `uv` o imagen reproducible + `dvc pull` previo si aplica. |
| Workspace cloud | Repos + opcional Jobs; Delta cuando el tamaño crece. |

Más enlaces relativos dentro del repo:

- Índice: [integrations/README.md](../integrations/README.md)
- Docker local (complementario): [DESARROLLO_Y_DOCKER.md](DESARROLLO_Y_DOCKER.md)
