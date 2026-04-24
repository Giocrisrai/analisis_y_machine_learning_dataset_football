.PHONY: help verify format lint test kedro-run bootstrap-minimal

help:
	@echo "Objetivos útiles:"
	@echo "  make verify          - format, lint, SQLite mínima, pytest, kedro run"
	@echo "  make test / lint / format / kedro-run / bootstrap-minimal - piezas sueltas"
	@echo "Documentación: docs/GUIA_ESTUDIANTES.md y docs/README.md"

# Formato + lint + datos sintéticos + pruebas + pipeline completo
verify: format lint bootstrap-minimal test kedro-run

format:
	ruff format src tests scripts

lint:
	ruff check src tests scripts

bootstrap-minimal:
	python scripts/bootstrap_data.py --source minimal --force

test:
	python -m pytest tests/ -q --tb=short

kedro-run:
	python -m kedro run
