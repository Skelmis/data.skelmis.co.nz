from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from enum import Enum
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Varchar
from piccolo.columns.indexes import IndexMethod


ID = "2024-02-22T21:01:54:997636"
VERSION = "0.121.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="home", description=DESCRIPTION
    )

    manager.add_table(
        class_name="F1Fantasy", tablename="f1_fantasy", schema=None, columns=None
    )

    manager.add_column(
        table_class_name="F1Fantasy",
        tablename="f1_fantasy",
        column_name="year",
        db_column_name="year",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 2,
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

    manager.add_column(
        table_class_name="F1Fantasy",
        tablename="f1_fantasy",
        column_name="team_name",
        db_column_name="team_name",
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

    manager.add_column(
        table_class_name="F1Fantasy",
        tablename="f1_fantasy",
        column_name="person",
        db_column_name="person",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "F1FantasyPlayers",
                {
                    "ETHAN": "Ethan",
                    "CHRIS": "Chris",
                    "CAMPBELL": "Campbell",
                    "TYLER": "Tyler",
                    "OLIVIA": "Olivia",
                    "JACK": "Jack",
                    "BRYN": "Bryn",
                },
            ),
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    return manager
