from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import BigInt
from piccolo.columns.column_types import Text


ID = "2024-01-14T18:19:38:136038"
VERSION = "0.121.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Incidents",
        tablename="incidents",
        column_name="duration",
        db_column_name="duration",
        params={"null": True},
        old_params={"null": False},
        column_class=BigInt,
        old_column_class=BigInt,
        schema=None,
    )

    manager.alter_column(
        table_class_name="Incidents",
        tablename="incidents",
        column_name="result_code",
        db_column_name="result_code",
        params={"null": True},
        old_params={"null": False},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="Incidents",
        tablename="incidents",
        column_name="result_description",
        db_column_name="result_description",
        params={"null": True},
        old_params={"null": False},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    return manager
