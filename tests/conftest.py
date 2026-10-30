"""Pytest configuration for UniFi MCP Server tests."""

import os
import sys
from pathlib import Path

import pytest

# Add the project root (for ``tests``) and ``src`` (for ``unifi_mcp_server``) to the path,
# so the tests run from a checkout with or without an editable install.
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))


@pytest.fixture(autouse=True, scope="function")
def isolate_env_file(tmp_path, monkeypatch):
    """Prevent Settings from loading .env file during unit tests.

    This ensures that tests using monkeypatch.delenv() actually work as expected,
    since Pydantic Settings loads from both environment variables AND .env file.
    """
    # Change to a temp directory so .env file won't be found
    temp_dir = tmp_path / "test_env"
    temp_dir.mkdir()
    monkeypatch.chdir(temp_dir)

    # Clear all UNIFI_* env vars so tests start clean
    for key in list(os.environ.keys()):
        if key.startswith("UNIFI_") or key.startswith("LOG_"):
            monkeypatch.delenv(key, raising=False)

    yield

    # Restore working directory (handled by monkeypatch automatically)
