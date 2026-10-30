"""Settings read a dotenv file only when ``UNIFI_ENV_FILE`` names one.

An MCP client picks the server's working directory, often a project the user
just opened. A ``.env`` there must not be able to fill in settings the user
left unset, such as TLS trust, SIEM targets or the backup directory.
"""

from pathlib import Path

import pytest

from unifi_mcp_server.config import Settings
from unifi_mcp_server.config.config import AuditMaintenanceSettings

PLANTED = (
    "UNIFI_API_KEY=planted-key\n"
    "UNIFI_LOCAL_VERIFY_SSL=false\n"
    "UNIFI_AUDIT_SIEM_TARGETS=https://attacker.invalid/hook\n"
    "UNIFI_BACKUP_DOWNLOAD_DIR=/tmp/planted\n"
    "UNIFI_AUDIT_RETENTION_DAYS=1\n"
)


@pytest.fixture
def planted_dotenv() -> Path:
    """A ``.env`` in the working directory (the root conftest chdirs to a temp dir)."""
    path = Path.cwd() / ".env"
    path.write_text(PLANTED, encoding="utf-8")
    return path


def test_dotenv_in_working_directory_is_ignored(planted_dotenv, monkeypatch) -> None:
    monkeypatch.setenv("UNIFI_API_KEY", "real-key")
    monkeypatch.setenv("UNIFI_API_TYPE", "local")
    monkeypatch.setenv("UNIFI_LOCAL_HOST", "10.0.0.1")

    settings = Settings()

    assert settings.api_key == "real-key"
    assert settings.local_verify_ssl is True
    assert settings.audit_siem_targets is None
    assert settings.backup_download_dir is None


def test_dotenv_in_working_directory_cannot_supply_required_values(planted_dotenv) -> None:
    with pytest.raises(ValueError):
        Settings()


def test_audit_maintenance_settings_ignore_working_directory_dotenv(planted_dotenv) -> None:
    assert AuditMaintenanceSettings().audit_retention_days is None


def test_explicit_env_file_is_read(tmp_path, monkeypatch) -> None:
    env_file = tmp_path / "trusted.env"
    env_file.write_text("UNIFI_API_KEY=file-key\nUNIFI_LOCAL_VERIFY_SSL=false\n", encoding="utf-8")
    monkeypatch.setenv("UNIFI_ENV_FILE", str(env_file))

    settings = Settings()

    assert settings.api_key == "file-key"
    assert settings.local_verify_ssl is False


def test_environment_overrides_explicit_env_file(tmp_path, monkeypatch) -> None:
    env_file = tmp_path / "trusted.env"
    env_file.write_text("UNIFI_API_KEY=file-key\n", encoding="utf-8")
    monkeypatch.setenv("UNIFI_ENV_FILE", str(env_file))
    monkeypatch.setenv("UNIFI_API_KEY", "env-key")

    assert Settings().api_key == "env-key"


def test_explicit_env_file_for_audit_maintenance(tmp_path, monkeypatch) -> None:
    env_file = tmp_path / "trusted.env"
    env_file.write_text("UNIFI_AUDIT_RETENTION_DAYS=30\n", encoding="utf-8")
    monkeypatch.setenv("UNIFI_ENV_FILE", str(env_file))

    assert AuditMaintenanceSettings().audit_retention_days == 30


def test_explicit_env_file_init_argument_still_works(tmp_path, monkeypatch) -> None:
    env_file = tmp_path / "given.env"
    env_file.write_text("UNIFI_API_KEY=given-key\n", encoding="utf-8")

    assert Settings(_env_file=env_file).api_key == "given-key"
