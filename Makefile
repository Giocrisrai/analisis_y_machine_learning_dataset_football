.PHONY: verify format lint test kedro-run bootstrap-minimal

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
