"""Built-in A2A prompt playbooks for UniFi MCP Server.

Example:
    >>> from unifi_mcp_server.a2a.playbooks import PLAYBOOKS
    >>> [playbook.name for playbook in PLAYBOOKS]
"""

from .device_provisioning import PLAYBOOK as DEVICE_PROVISIONING
from .guest_wifi_setup import PLAYBOOK as GUEST_WIFI_SETUP
from .incident_response import PLAYBOOK as INCIDENT_RESPONSE
from .network_diagnostics import PLAYBOOK as NETWORK_DIAGNOSTICS
from .security_audit import PLAYBOOK as SECURITY_AUDIT
from .site_migration import PLAYBOOK as SITE_MIGRATION

PLAYBOOKS = [
    NETWORK_DIAGNOSTICS,
    SECURITY_AUDIT,
    DEVICE_PROVISIONING,
    GUEST_WIFI_SETUP,
    SITE_MIGRATION,
    INCIDENT_RESPONSE,
]

__all__ = [
    "PLAYBOOKS",
    "NETWORK_DIAGNOSTICS",
    "SECURITY_AUDIT",
    "DEVICE_PROVISIONING",
    "GUEST_WIFI_SETUP",
    "SITE_MIGRATION",
    "INCIDENT_RESPONSE",
]
