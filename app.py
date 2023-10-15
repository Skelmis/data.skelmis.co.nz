import typing as t

from fastapi import FastAPI
from piccolo_admin.endpoints import create_admin
from piccolo.engine import engine_finder
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from home.endpoints import HomeEndpoint, TravelEndpoint
from home.piccolo_app import APP_CONFIG

app = FastAPI(
    title="Ethan's data aggregation",
    description="All the things I like to gather data on, simplified in one place.<br>"
    "I don't propose making these public, however if you are interested in access to specific routes "
    "feel free to drop me a message. Some of these are meant to be consumed after all.",
    routes=[
        Route("/", HomeEndpoint),
        Route("/travel", TravelEndpoint),
        Mount(
            "/admin/",
            create_admin(
                tables=APP_CONFIG.table_classes,
                # Required when running under HTTPS:
                # allowed_hosts=['my_site.com']
            ),
        ),
        Mount("/static/", StaticFiles(directory="static")),
    ],
)


@app.on_event("startup")
async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


@app.on_event("shutdown")
async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")
