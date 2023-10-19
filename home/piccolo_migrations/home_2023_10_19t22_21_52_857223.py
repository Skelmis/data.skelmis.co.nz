from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2023-10-19T22:21:52:857223"
VERSION = "0.121.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.drop_table(class_name="Contact", tablename="contact", schema=None)

    return manager
