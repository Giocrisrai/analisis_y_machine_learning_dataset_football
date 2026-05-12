"""Configuración compartida de pytest."""

from __future__ import annotations

import os


def pytest_configure(config) -> None:  # noqa: ARG001 — firma del hook oficial de pytest
    """Entorno estable para ejecutar Kedro en tests sin ruido de telemetría."""
    os.environ.setdefault("KEDRO_DISABLE_TELEMETRY", "1")
