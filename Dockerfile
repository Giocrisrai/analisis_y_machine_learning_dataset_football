# Imagen reproducible: dependencias + proyecto. Los datos viven en volumen montado en /app/data.
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    KEDRO_DISABLE_TELEMETRY=1 \
    JUPYTER_DATA_DIR=/tmp/jupyter-data \
    JUPYTER_CONFIG_DIR=/tmp/jupyter-config

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt README.md ./
COPY src ./src
COPY conf ./conf
COPY scripts ./scripts
COPY tests ./tests

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install -e ".[dev]"

# Carpetas de datos (el volumen puede montarse encima)
RUN mkdir -p data/raw data/05_model_input data/06_models data/08_reporting

# Por defecto: datos + pipeline (sobrescribible en compose)
CMD ["sh", "-c", "python scripts/bootstrap_data.py && kedro run"]
