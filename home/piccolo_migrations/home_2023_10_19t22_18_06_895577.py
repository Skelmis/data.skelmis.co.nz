from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text
from piccolo.columns.indexes import IndexMethod


ID = "2023-10-19T22:18:06:895577"
VERSION = "0.121.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="Contact",
        tablename="contact",
        column_name="email_address",
        db_column_name="email_address",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
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

    manager.rename_column(
        table_class_name="Contact",
        tablename="contact",
        old_column_name="address",
        new_column_name="home_address",
        old_db_column_name="address",
        new_db_column_name="home_address",
        schema=None,
    )

    return manager
