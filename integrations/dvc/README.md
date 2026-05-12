# Notas rápidas DVC

Etapas (una sola) — `kedro_ml` — encadena **`bootstrap`** con SQLite mínima y **`kedro run`**.

> **SQLite + Git:** la base grande puede estar en Git LFS; esta etapa la **sobrescribe** cuando corres `dvc repro` (solo en entorno de experimentación donde quieras paridad rápida con CI). Para versionar sólo artefactos derivados, no declaramos `database.sqlite` como `outs` — sólo ficheros listados en `dvc.lock`.

Pasos típicos:

```bash
uv sync --extra dev --extra infra
dvc repro      # mismo efecto práctico que `make dvc-repro`
dvc dag        # inspeccionar orden y dependencias
```

Configura **`dvc remote`** antes de compartir datos entre estudiantes/CI externos (ver documentación consolidada).
