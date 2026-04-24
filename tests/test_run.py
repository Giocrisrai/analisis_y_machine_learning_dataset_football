"""
Tests for the Kedro project: registro de pipelines y ejecución opcional con SQLite local.
"""

from pathlib import Path

import pytest
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project

from analisis_equipos_de_football.pipeline_registry import register_pipelines


class TestPipelineRegistry:
    def test_default_pipeline_has_nodes(self) -> None:
        bootstrap_project(Path.cwd())
        pipelines = register_pipelines()
        assert "__default__" in pipelines
        assert len(pipelines["__default__"].nodes) > 0


_DB = Path("data/raw/database.sqlite")


@pytest.mark.skipif(
    not _DB.is_file(), reason="Requiere data/raw/database.sqlite en local"
)
class TestKedroRun:
    def test_kedro_run_end_to_end(self) -> None:
        bootstrap_project(Path.cwd())
        with KedroSession.create(project_path=Path.cwd()) as session:
            session.run()
