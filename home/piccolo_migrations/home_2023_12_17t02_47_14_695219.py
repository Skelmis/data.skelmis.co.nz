from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text
from piccolo.columns.indexes import IndexMethod


ID = "2023-12-17T02:47:14:695219"
VERSION = "0.121.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="Jobs",
        tablename="jobs",
        column_name="manager",
        db_column_name="manager",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    return manager
