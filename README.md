# Análisis y modelos — datos de fútbol (Kedro)

[![CI](https://github.com/Giocrisrai/analisis_y_machine_learning_dataset_football/actions/workflows/ci.yml/badge.svg)](https://github.com/Giocrisrai/analisis_y_machine_learning_dataset_football/actions/workflows/ci.yml)

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://docs.kedro.org)

Proyecto para **exploración de datos**, **machine learning** (clasificación y regresión), **modelos no supervisados** y **pipelines reproducibles** con [Kedro 1.3](https://docs.kedro.org), pensado para **docencia** (CRISP-DM, métricas, comparación de modelos).

**Mapa del ciclo de vida (EDA → ML → Kedro/Docker → CI):** [docs/guias/ciclo_ciencia_datos_artefactos.md](docs/guias/ciclo_ciencia_datos_artefactos.md)

---

## Inicio rápido (estudiantes)

1. Leer **[docs/GUIA_ESTUDIANTES.md](docs/GUIA_ESTUDIANTES.md)** (instalación, datos, Jupyter, pruebas).
2. Laboratorios en orden: **[notebooks/README.md](notebooks/README.md)**.
3. Comprobar el entorno: tras `uv sync --extra dev` (o `pip install -e ".[dev]"` con venv activo), ejecutar **`uv run make verify`** o `make verify` — evita ejecutar contra un Python sin `pyarrow`.

**Índice de toda la documentación:** [docs/README.md](docs/README.md)

---

## Docencia: teoría y guion

| Recurso | Descripción |
|---------|-------------|
| [docs/guias/ciclo_ciencia_datos_artefactos.md](docs/guias/ciclo_ciencia_datos_artefactos.md) | Ciclo DS end-to-end, tablas fase ↔ notebook ↔ Kedro ↔ artefactos |
| [docs/guias/crispdm_y_machine_learning.md](docs/guias/crispdm_y_machine_learning.md) | CRISP-DM, métricas, vínculo con el repositorio |
| [docs/guias/modelos_y_flujo_integrado.md](docs/guias/modelos_y_flujo_integrado.md) | Algoritmos, diagramas notebook ↔ Kedro, FAQ |
| [notebooks/README.md](notebooks/README.md) | Orden de los laboratorios y tiempos orientativos |

---

## Datos

- El archivo **`data/raw/database.sqlite`** se distribuye con **Git LFS** para la clase.
- Si al clonar no aparece la base completa, ejecuta: `git lfs pull`.
- Si no tienes LFS o quieres regenerar datos: `python scripts/bootstrap_data.py` (red opcional; si falla, base sintética mínima).
- Detalle y Docker: **[docs/DESARROLLO_Y_DOCKER.md](docs/DESARROLLO_Y_DOCKER.md)**

---

## Instalación (resumen)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip uv
uv sync --extra dev                # entorno reproducible con uv.lock
python scripts/bootstrap_data.py
uv run make verify-all             # recomendado: incluye notebooks (CI en GitHub hace algo equivalente)
```

Opcional — SHAP en notebooks: `uv sync --extra dev --extra explain`

---

## Pipeline Kedro

Con la base ya en `data/raw/database.sqlite`:

```bash
python -m kedro run
```

Si aparece el mensaje de telemetría de Kedro o quieres uniformidad con el Makefile, en macOS/Linux puedes usar `export KEDRO_DISABLE_TELEMETRY=1`, o el objetivo `make kedro-run` (equivalente).

Etapas por defecto (`pipeline_registry.py`):

1. **data_processing** → `features_for_ml` (Parquet)
2. **ml_classification** → métricas JSON, modelo `.pkl`, importancias CSV
3. **ml_regression** → igual para regresión sobre goles del local

Parcial:

```bash
python -m kedro run --pipeline data_processing
```

Configuración: `conf/base/catalog.yml`, `conf/base/parameters.yml`.

---

## Jupyter

Desde la **raíz del proyecto**:

```bash
kedro jupyter lab
```

Variables útiles: `catalog`, `context`, `session` (extensión `%load_ext kedro.ipython`).

---

## Pruebas y calidad

```bash
make help            # lista objetivos del Makefile (incluye el tip de uv run)
uv run make verify   # recomendado si no activaste el venv
make verify          # format + lint + bootstrap mínimo + pytest + kedro run
make verify-all      # como verify + notebooks
make verify-notebooks
pytest               # solo tests
```

---

## Integraciones institucionales (opcional)

Databricks, **DVC** y **Apache Airflow** están documentados como extensión (no necesarias para el laboratorio estándar). Ver **[docs/DATABRICKS_DVC_AIRFLOW.md](docs/DATABRICKS_DVC_AIRFLOW.md)** y **`integrations/`**. Comandos útiles (`make infra-sync`, `make dvc-repro`).

---

## Docker (opcional)

Requiere Docker en ejecución. Ver [docs/DESARROLLO_Y_DOCKER.md](docs/DESARROLLO_Y_DOCKER.md):

```bash
docker compose build
docker compose run --rm pipeline-minimal
docker compose --profile lab up jupyter
docker compose --profile viz up kedro-viz
```

---

## Buenas prácticas del template Kedro

- No eliminar reglas importantes del `.gitignore`.
- No commitear datos grandes ni credenciales; configuración local en `conf/local/`.
- Reproducibilidad: dependencias en `requirements.txt` / `pyproject.toml`; el workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) valida `uv.lock` contra Python 3.11 y 3.12.

---

## Más información

- [Kedro: dependencias del proyecto](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html)
- [Empaquetado y despliegue](https://docs.kedro.org/en/stable/deploy/package_a_project/)
