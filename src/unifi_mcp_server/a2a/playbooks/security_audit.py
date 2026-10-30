"""Security audit playbook.

Example:
    >>> from unifi_mcp_server.a2a.prompt_playbook import render_playbook
    >>> print(render_playbook("security_audit", {"site_id": "default"}))
"""

from __future__ import annotations

from ..prompt_playbook import PlaybookStep, PromptPlaybook

PLAYBOOK = PromptPlaybook(
    name="security_audit",
    description="Audit firewall, ACL, DPI, and port-forward posture for exposure and drift.",
    safetyLevel="none",
    requiredSkills=[
        "list_firewall_rules",
        "list_acl_rules",
        "list_firewall_policies",
        "get_zone_policy_matrix",
        "list_port_forwards",
        "list_content_filters",
        "list_top_applications",
        "get_dpi_statistics",
    ],
    steps=[
        PlaybookStep(
            order=1,
            action="Inventory the current security surface for the site.",
            tool="list_firewall_rules",
            params={"site_id": "${site_id}"},
            validation="Confirm the total rule count and any obvious duplicate or broad allow rules.",
            fallback="If firewall rules are unavailable, collect ACLs and firewall policies separately to build the audit baseline.",
        ),
        PlaybookStep(
            order=2,
            action="Review ACL coverage and identify gaps or overlapping controls.",
            tool="list_acl_rules",
            params={"site_id": "${site_id}"},
            validation="Check for missing deny rules, wide source scopes, and entries without clear intent.",
            fallback="If ACLs are not configured, note the absence and continue with firewall policy analysis.",
        ),
        PlaybookStep(
            order=3,
            action="Inspect zone policy relationships and the effective policy matrix.",
            tool="get_zone_policy_matrix",
            params={"site_id": "${site_id}"},
            validation="Validate that inter-zone flows align with the documented security model.",
            fallback="If the matrix is unavailable, use list_firewall_policies and infer policy intent from source/destination scope.",
        ),
        PlaybookStep(
            order=4,
            action="Assess public exposure through port forwards and related services.",
            tool="list_port_forwards",
            params={"site_id": "${site_id}"},
            validation="Flag externally reachable services, narrow port ranges, and any forwards without a business justification.",
            fallback="If no port-forward inventory is returned, verify the controller scope and search the network settings for NAT entries.",
        ),
        PlaybookStep(
            order=5,
            action="Review traffic visibility and content controls for risky application usage.",
            tool="get_dpi_statistics",
            params={"site_id": "${site_id}"},
            validation="Correlate blocked or unusual traffic with the configured policy posture.",
            fallback="If DPI statistics are sparse, use list_top_applications and list_content_filters for supplemental evidence.",
        ),
        PlaybookStep(
            order=6,
            action="Produce an audit summary with prioritized findings and remediation themes.",
            tool=None,
            params={},
            validation="Each finding should include severity, affected scope, and the relevant policy object.",
            fallback="If the posture is ambiguous, recommend a narrower manual review of the highest-risk rules first.",
        ),
    ],
)
