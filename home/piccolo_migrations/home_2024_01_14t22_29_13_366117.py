from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text


ID = "2024-01-14T22:29:13:366117"
VERSION = "0.121.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Incidents",
        tablename="incidents",
        column_name="station",
        db_column_name="station",
        params={"index": True},
        old_params={"index": False},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    return manager
