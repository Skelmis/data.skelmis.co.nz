from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2024-02-22T21:20:39:200995"
VERSION = "0.121.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.drop_table(
        class_name="F1Fantasy", tablename="f1_fantasy", schema=None
    )

    return manager
