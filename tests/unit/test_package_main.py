"""``python -m src`` runs the server entry point."""

import runpy
import sys
import types
from unittest.mock import MagicMock, patch


def test_module_execution_calls_main() -> None:
    # Stub unifi_mcp_server.main: importing the real one builds Settings from the environment.
    stub = types.ModuleType("unifi_mcp_server.main")
    stub.main = MagicMock()  # type: ignore[attr-defined]
    with patch.dict(sys.modules, {"unifi_mcp_server.main": stub}):
        runpy.run_module("unifi_mcp_server", run_name="__main__")

    stub.main.assert_called_once_with()
