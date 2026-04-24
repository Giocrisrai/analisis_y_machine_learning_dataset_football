# Análisis y modelos — datos de fútbol (Kedro)

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://docs.kedro.org)

Proyecto para **exploración de datos**, **machine learning** (clasificación y regresión) y **pipelines reproducibles** con [Kedro 1.3](https://docs.kedro.org), pensado para **docencia** (CRISP-DM, métricas, comparación de modelos).

---

## Inicio rápido (estudiantes)

1. Leer **[docs/GUIA_ESTUDIANTES.md](docs/GUIA_ESTUDIANTES.md)** (instalación, datos, Jupyter, pruebas).
2. Laboratorios en orden: **[notebooks/README.md](notebooks/README.md)**.
3. Comprobar el entorno: `make verify` (tras `pip install -e ".[dev]"`).

**Índice de toda la documentación:** [docs/README.md](docs/README.md)

---

## Docencia: teoría y guion

| Recurso | Descripción |
|---------|-------------|
| [docs/guias/crispdm_y_machine_learning.md](docs/guias/crispdm_y_machine_learning.md) | CRISP-DM, métricas, vínculo con el repositorio |
| [docs/guias/modelos_y_flujo_integrado.md](docs/guias/modelos_y_flujo_integrado.md) | Algoritmos, diagramas notebook ↔ Kedro, FAQ |
| [notebooks/README.md](notebooks/README.md) | Orden de los laboratorios y tiempos orientativos |

---

## Datos

- El archivo **`data/raw/database.sqlite`** no se versiona en Git.
- Crearlo con: `python scripts/bootstrap_data.py` (red opcional; si falla, base sintética mínima).
- Detalle y Docker: **[docs/DESARROLLO_Y_DOCKER.md](docs/DESARROLLO_Y_DOCKER.md)**

---

## Instalación (resumen)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
pip install -e ".[dev]"            # tests y make verify
python scripts/bootstrap_data.py
make verify                        # opcional: comprobar todo
```

Opcional — SHAP en notebooks: `pip install -e ".[explain]"`

---

## Pipeline Kedro

Con la base ya en `data/raw/database.sqlite`:

```bash
python -m kedro run
```

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
make help         # lista objetivos del Makefile
make verify       # format + lint + bootstrap mínimo + pytest + kedro run
pytest            # solo tests
```

---

## Docker (opcional)

Requiere Docker en ejecución. Ver [docs/DESARROLLO_Y_DOCKER.md](docs/DESARROLLO_Y_DOCKER.md):

```bash
docker compose build
docker compose run --rm pipeline-minimal
docker compose --profile lab up jupyter
```

---

## Buenas prácticas del template Kedro

- No eliminar reglas importantes del `.gitignore`.
- No commitear datos grandes ni credenciales; configuración local en `conf/local/`.
- Reproducibilidad: dependencias en `requirements.txt` / `pyproject.toml`.

---

## Más información

- [Kedro: dependencias del proyecto](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html)
- [Empaquetado y despliegue](https://docs.kedro.org/en/stable/deploy/package_a_project/)
