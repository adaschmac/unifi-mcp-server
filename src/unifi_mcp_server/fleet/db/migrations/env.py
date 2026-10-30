"""Alembic environment for the fleet registry.

Migrations always run on a connection handed over by ``unifi_mcp_server.fleet.db.schema``
(``config.attributes["connection"]``); there is no alembic.ini and no URL here.
"""

from alembic import context

from unifi_mcp_server.fleet.db.schema import VERSION_TABLE

connection = context.config.attributes["connection"]
context.configure(
    connection=connection,
    target_metadata=context.config.attributes.get("target_metadata"),
    version_table=VERSION_TABLE,
)
with context.begin_transaction():
    context.run_migrations()
