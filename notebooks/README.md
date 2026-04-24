# Notebooks (ruta docente recomendada)

Ejecutar desde la **raíz del proyecto** con `kedro jupyter lab` (o `notebook`) para tener `catalog`, `context` y rutas correctas.

Si aún no tienes la base: `python scripts/bootstrap_data.py` (ver [docs/DESARROLLO_Y_DOCKER.md](../docs/DESARROLLO_Y_DOCKER.md)).

| Orden | Notebook | CRISP-DM (aprox.) | Contenido |
|-------|----------|-------------------|-----------|
| 01 | `01_comprension_negocio_y_datos.ipynb` | Fases 1–2 | Problema, tablas SQLite, calidad básica, histogramas de cuotas |
| 02 | `02_preparacion_datos.ipynb` | Fase 3 | Tabla `df_ml` = nodo Kedro; chequeo opcional vs Parquet |
| 03 | `03_clasificacion_resultado.ipynb` | Fases 4–5 | Comparación de clasificadores, métricas, matriz de confusión |
| 04 | `04_regresion_goles.ipynb` | Fases 4–5 | Regresión, MAE/RMSE/R², residuos |
| 05 | `05_explicabilidad_evaluacion.ipynb` | Fase 5 | Permutación, coeficientes logísticos, SHAP opcional |
| 06 | `06_pipeline_Kedro.ipynb` | Fase 6 | Parámetros, `session.run()`, leer JSON/Parquet de salida |

**Opcional — todo en un solo archivo:** `Exploracion_de_datos.ipynb` (mismo flujo que 03–05 compactado).

Textos de apoyo: `docs/guias/crispdm_y_machine_learning.md`, `docs/guias/modelos_y_flujo_integrado.md`.
