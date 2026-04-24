# Datos, prueba end-to-end y Docker

## 1. Obtener `database.sqlite`

El catálogo Kedro apunta a `data/raw/database.sqlite` (no se versiona en git).

### Opción A — Script automático (recomendado)

Desde la **raíz del repositorio**:

```bash
python scripts/bootstrap_data.py
```

- Intenta descargar la base pública en Hugging Face (réplica del *European Soccer Database*).
- Si la red falla, genera una SQLite **mínima sintética** (tablas del catálogo; tabla `Match` poblada) suficiente para `kedro run` y la mayoría de notebooks.

Forzar solo sintética:

```bash
python scripts/bootstrap_data.py --source minimal --force
```

Solo descarga (error si no hay red):

```bash
python scripts/bootstrap_data.py --source download --force
```

### Opción B — Kaggle u otra fuente

Si ya tienes el archivo de Kaggle, cópialo a `data/raw/database.sqlite`. El proyecto espera el esquema clásico con tablas `Match`, `League`, etc.

---

## 2. Probar el pipeline en local

Chequeo recomendado (requiere `pip install -e ".[dev]"` y `make`):

```bash
make verify
```

Equivale a: formatear con Ruff, lint, regenerar SQLite mínima, `pytest` y `kedro run`.

Pasos manuales:

```bash
pip install -r requirements.txt
pip install -e ".[dev]"
python scripts/bootstrap_data.py --source minimal --force   # o sin flags para intentar HF
kedro run
pytest -q
```

Comprobar artefactos:

- `data/05_model_input/features_for_ml.parquet`
- `data/08_reporting/classification_metrics.json`
- `data/08_reporting/regression_metrics.json`
- `data/06_models/*.pkl`

---

## 3. Docker Compose

Requisitos: **Docker Engine con el daemon en ejecución** (Docker Desktop, Colima, Rancher Desktop, etc.) y **Compose** (plugin `docker compose` o binario `docker-compose`).

Si ves `Cannot connect to the Docker daemon`, arranca el servicio antes de continuar.

```bash
docker compose build
# o, según instalación:
docker-compose build
```

Ejecutar **bootstrap + Kedro** (intenta descarga; si falla, la imagen usa modo `auto` del script = fallback sintético):

```bash
docker compose run --rm pipeline
```

Solo datos sintéticos + pipeline (sin depender de Hugging Face):

```bash
docker compose run --rm pipeline-minimal
```

**Tests** dentro del contenedor (usa base sintética):

```bash
docker compose run --rm test
```

**JupyterLab** con extensión Kedro (perfil `lab`; URL con token en logs):

```bash
docker compose --profile lab up jupyter
```

Luego abre `http://localhost:8888` y revisa el token que imprime el contenedor.

Los datos persistentes van al volumen Docker `football_data` (SQLite y salidas de Kedro).

---

## 4. Limitaciones de la base sintética

- Pensada para **CI, Docker sin red y prácticas rápidas**.
- Las tablas `Player`, `Team`, etc. existen pero están **vacías**; los notebooks que carguen esas tablas verán 0 filas.
- Para análisis realista, usa la descarga completa (Hugging Face o Kaggle).

---

## 5. Pipelines Kedro registrados

Orden del `kedro run` por defecto:

1. `data_processing` → `features_for_ml`
2. `ml_classification` → métricas, modelo, importancias
3. `ml_regression` → métricas, modelo, importancias

Ejecución parcial:

```bash
kedro run --pipeline data_processing
```
