from piccolo.engine.postgres import PostgresEngine
from piccolo.engine.sqlite import SQLiteEngine

from piccolo.conf.apps import AppRegistry


# DB = PostgresEngine(
#     config={
#         "database": "piccolo_project",
#         "user": "postgres",
#         "password": "",
#         "host": "localhost",
#         "port": 5432,
#     }
# )
DB = SQLiteEngine()

APP_REGISTRY = AppRegistry(
    apps=["home.piccolo_app", "piccolo_admin.piccolo_app"]
)
