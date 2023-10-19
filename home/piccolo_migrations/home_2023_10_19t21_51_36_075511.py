from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text


ID = "2023-10-19T21:51:36:075511"
VERSION = "0.121.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Contact",
        tablename="contact",
        column_name="name",
        db_column_name="name",
        params={"primary_key": False},
        old_params={"primary_key": True},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    return manager
