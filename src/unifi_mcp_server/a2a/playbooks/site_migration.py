"""Site migration playbook.

Example:
    >>> from unifi_mcp_server.a2a.prompt_playbook import render_playbook
    >>> print(render_playbook("site_migration", {"source_site_id": "default"}))
"""

from __future__ import annotations

from ..prompt_playbook import PlaybookStep, PromptPlaybook

PLAYBOOK = PromptPlaybook(
    name="site_migration",
    description="Move site settings between controllers using backups and restore validation.",
    safetyLevel="strict",
    requiredSkills=[
        "list_sites",
        "get_site_details",
        "trigger_backup",
        "list_backups",
        "validate_backup",
        "restore_backup",
        "get_restore_status",
        "get_backup_status",
    ],
    steps=[
        PlaybookStep(
            order=1,
            action="Capture the source and destination site context before changing anything.",
            tool="list_sites",
            params={},
            validation="Confirm the source site, destination controller, and migration target are unambiguous.",
            fallback="If site naming is ambiguous, gather get_site_details for both controllers and stop until the operator confirms the target.",
        ),
        PlaybookStep(
            order=2,
            action="Create or locate a fresh backup for the source site.",
            tool="trigger_backup",
            params={"site_id": "${source_site_id}"},
            validation="Verify the backup job starts and produces a usable artifact for the site snapshot.",
            fallback="If on-demand backup is unavailable, list existing backups and select the most recent validated backup.",
        ),
        PlaybookStep(
            order=3,
            action="Validate the backup before using it for the migration.",
            tool="validate_backup",
            params={"site_id": "${source_site_id}", "backup_id": "${backup_id}"},
            validation="Confirm the backup is complete, restorable, and within the intended retention window.",
            fallback="If validation fails, stop the migration and create a new backup rather than restoring an unknown snapshot.",
        ),
        PlaybookStep(
            order=4,
            action="Restore the backup into the destination controller or site.",
            tool="restore_backup",
            params={"site_id": "${destination_site_id}", "backup_id": "${backup_id}"},
            validation="Confirm the restore job is accepted and the target controller begins applying the imported configuration.",
            fallback="If restore cannot start, verify controller compatibility and re-run after correcting the destination scope.",
        ),
        PlaybookStep(
            order=5,
            action="Monitor the restore process until the controller reports success or failure.",
            tool="get_restore_status",
            params={"site_id": "${destination_site_id}", "restore_id": "${restore_id}"},
            validation="Ensure the status reaches a terminal success state and no critical objects are missing.",
            fallback="If the restore stalls, capture the error details and escalate before making any further migration attempts.",
        ),
        PlaybookStep(
            order=6,
            action="Confirm post-migration health and version alignment.",
            tool="get_backup_status",
            params={"site_id": "${destination_site_id}"},
            validation="Verify the backup/restore state and ensure the migrated site is in a supportable condition.",
            fallback="If health is degraded, roll back only after the backup and restore artifacts are independently validated.",
        ),
    ],
)
