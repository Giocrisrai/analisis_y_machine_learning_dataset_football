.PHONY: help sync verify verify-notebooks format lint test kedro-run bootstrap-minimal kedro-viz

help:
	@echo "Objetivos útiles:"
	@echo "  make sync            - instalar dependencias con uv"
	@echo "  make verify          - format, lint, SQLite mínima, pytest, kedro run"
	@echo "  make verify-notebooks - ejecutar notebooks en memoria con nbclient"
	@echo "  make test / lint / format / kedro-run / bootstrap-minimal - piezas sueltas"
	@echo "Documentación: docs/GUIA_ESTUDIANTES.md y docs/README.md"

sync:
	uv sync --extra dev

# Formato + lint + datos sintéticos + pruebas + pipeline completo
verify: format lint bootstrap-minimal test kedro-run

verify-notebooks:
	python scripts/verify_notebooks.py

format:
	ruff format src tests scripts

lint:
	ruff check src tests scripts

bootstrap-minimal:
	python scripts/bootstrap_data.py --source minimal

test:
	python -m pytest tests/ -q --tb=short

kedro-run:
	python -m kedro run

kedro-viz:
	kedro viz
