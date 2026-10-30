"""Tests for deprecated zone-based firewall matrix tools."""

from unittest.mock import MagicMock

import pytest

from unifi_mcp_server.tools.zbf_matrix import (
    block_application_by_zone,
    delete_zbf_policy,
    get_zbf_matrix,
    get_zone_matrix_policy,
    get_zone_policies,
    list_blocked_applications,
    update_zbf_policy,
)


@pytest.fixture
def mock_settings():
    """Create mock settings for deprecated ZBF tool calls."""
    settings = MagicMock()
    settings.log_level = "INFO"
    return settings


@pytest.mark.asyncio
async def test_get_zbf_matrix_reports_missing_endpoint(mock_settings):
    """Test matrix retrieval reports that the endpoint is unavailable."""
    with pytest.raises(NotImplementedError, match="Zone policy matrix endpoint does not exist"):
        await get_zbf_matrix("default", mock_settings)


@pytest.mark.asyncio
async def test_get_zone_policies_reports_missing_endpoint(mock_settings):
    """Test zone policy listing reports that the endpoint is unavailable."""
    with pytest.raises(NotImplementedError, match="Zone policies endpoint does not exist"):
        await get_zone_policies("default", "zone-lan", mock_settings)


@pytest.mark.asyncio
async def test_update_zbf_policy_reports_missing_endpoint(mock_settings):
    """Test zone policy updates report that the endpoint is unavailable."""
    with pytest.raises(NotImplementedError, match="Zone policy update endpoint does not exist"):
        await update_zbf_policy(
            site_id="default",
            source_zone_id="zone-lan",
            destination_zone_id="zone-iot",
            action="deny",
            settings=mock_settings,
            description="Block IoT access to LAN",
            priority=100,
            enabled=True,
            confirm=True,
            dry_run=False,
        )


@pytest.mark.asyncio
async def test_block_application_by_zone_reports_missing_endpoint(mock_settings):
    """Test per-zone application blocking reports that the endpoint is unavailable."""
    with pytest.raises(
        NotImplementedError,
        match="Application blocking per zone endpoint does not exist",
    ):
        await block_application_by_zone(
            site_id="default",
            zone_id="zone-iot",
            application_id="app-video",
            settings=mock_settings,
            action="block",
            enabled=True,
            description="Block video streaming",
            confirm=True,
            dry_run=False,
        )


@pytest.mark.asyncio
async def test_list_blocked_applications_reports_missing_endpoint(mock_settings):
    """Test blocked application listing reports that the endpoint is unavailable."""
    with pytest.raises(
        NotImplementedError,
        match="Blocked applications list endpoint does not exist",
    ):
        await list_blocked_applications("default", zone_id="zone-iot", settings=mock_settings)


@pytest.mark.asyncio
async def test_get_zone_matrix_policy_reports_missing_endpoint(mock_settings):
    """Test individual matrix policy lookup reports that the endpoint is unavailable."""
    with pytest.raises(NotImplementedError, match="Zone matrix policy endpoint does not exist"):
        await get_zone_matrix_policy(
            "default",
            source_zone_id="zone-lan",
            destination_zone_id="zone-iot",
            settings=mock_settings,
        )


@pytest.mark.asyncio
async def test_delete_zbf_policy_reports_missing_endpoint(mock_settings):
    """Test zone policy deletion reports that the endpoint is unavailable."""
    with pytest.raises(NotImplementedError, match="Zone policy delete endpoint does not exist"):
        await delete_zbf_policy(
            "default",
            source_zone_id="zone-lan",
            destination_zone_id="zone-iot",
            settings=mock_settings,
            confirm=True,
            dry_run=False,
        )
