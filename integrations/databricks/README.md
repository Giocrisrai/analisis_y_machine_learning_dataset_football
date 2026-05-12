# Integración Databricks — Lakehouse opcional

## Repos (rápido, docencia)

1. En el Workspace: **Repos → Add repo** con la URL Git de esta asignatura.
2. Ejecutá los notebooks desde la raíz Repo (Kedro resuelve `conf/` igual que local).
3. Si un notebook reclama librerías, una celda cabecera suficiente es:

```python
%pip install uv
# luego ejecutar instalación proyecto vía Terminal del cluster o usar wheel generado offline
```

En muchos talleres bastará con tener el cluster con **pandas / scikit-learn** acorde a tu `requirements.txt`; la guía estudiantil detalla instalación reproducible fuera del cloud (`uv sync --extra dev`).

## Jobs / automatización avanzada

Copiá **`bundle.yaml.example`**, pegalo como punto de arranque (p. ej. `databricks.yml` en una carpeta dedicada para bundles) y reemplazá `REPLACE_CLUSTER_ID`, `REPLACE_NOTEBOOK_PATH` con tus IDs y rutas reales.

Después ejecutá desde terminal autenticada:

```bash
databricks bundle deploy -t dev
```

> La CLI y el formato exacto pueden variar entre versiones; seguí la [**documentación de Asset Bundles**](https://docs.databricks.com/dev-tools/bundles/index.html) vigente antes de clase.
