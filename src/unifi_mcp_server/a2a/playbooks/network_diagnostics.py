"""Network diagnostics playbook.

Example:
    >>> from unifi_mcp_server.a2a.prompt_playbook import render_playbook
    >>> print(render_playbook("network_diagnostics", {"site_id": "default"}))
"""

from __future__ import annotations

from ..prompt_playbook import PlaybookStep, PromptPlaybook

PLAYBOOK = PromptPlaybook(
    name="network_diagnostics",
    description="Diagnose network issues across clients, devices, topology, and WAN health.",
    safetyLevel="none",
    requiredSkills=[
        "list_sites",
        "get_site_health_summary",
        "get_internet_health",
        "get_network_topology",
        "get_client_details",
        "get_device_details",
        "get_device_statistics",
        "get_client_statistics",
        "run_speed_test",
        "get_spectrum_scan",
        "list_spectrum_interference",
    ],
    steps=[
        PlaybookStep(
            order=1,
            action="Identify the target site and confirm the operational scope.",
            tool="list_sites",
            params={},
            validation="Confirm the site_id, site name, and controller scope match the incident report.",
            fallback="If the site cannot be resolved, ask for the site identifier or use get_site_details on the likely site.",
        ),
        PlaybookStep(
            order=2,
            action="Collect high-level site and internet health signals.",
            tool="get_site_health_summary",
            params={"site_id": "${site_id}"},
            validation="Check for degraded WAN status, device health warnings, and client anomaly counts.",
            fallback="Use get_internet_health and get_site_statistics if the summary endpoint is unavailable.",
        ),
        PlaybookStep(
            order=3,
            action="Inspect the physical and logical topology for weak links or down devices.",
            tool="get_network_topology",
            params={"site_id": "${site_id}"},
            validation="Verify the topology includes the affected devices, uplinks, and leaf nodes.",
            fallback="If topology is incomplete, call get_device_details for suspected devices and corroborate with get_site_inventory.",
        ),
        PlaybookStep(
            order=4,
            action="Examine the impacted client or device for connection-quality indicators.",
            tool="get_client_statistics",
            params={"site_id": "${site_id}", "client_mac": "${client_mac}"},
            validation="Look for low RSSI, high retry counts, low data rates, packet loss, or repeated reconnects.",
            fallback="If the client is unknown, use search_clients and then get_client_details for the matched MAC address.",
        ),
        PlaybookStep(
            order=5,
            action="Check radio and WAN performance for environmental or upstream causes.",
            tool="run_speed_test",
            params={"site_id": "${site_id}"},
            validation="Compare throughput and latency against the expected baseline for the site.",
            fallback="If speed testing fails, use get_spectrum_scan and list_spectrum_interference to isolate RF issues.",
        ),
        PlaybookStep(
            order=6,
            action="Summarize the likely root cause and propose the safest remediation order.",
            tool=None,
            params={},
            validation="A concise diagnosis should name the most probable fault domain, affected assets, and next action.",
            fallback="If evidence is inconclusive, recommend a controlled follow-up with device-specific checks or packet captures.",
        ),
    ],
)
