from commons import async_util
from fastapi import FastAPI
from piccolo_admin.endpoints import create_admin
from piccolo.engine import engine_finder
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from home import endpoints
from home.endpoints import (
    HomeEndpoint,
    TravelEndpoint,
    CameraEndpoint,
    AchievementsEndpoint,
)
from home.fenz.worker import digest_data
from home.piccolo_app import APP_CONFIG
from middleware import CustomHeaderMiddleware

app = FastAPI(
    title="Ethan's data aggregation",
    description="All the things I like to gather data on, simplified in one place.<br>"
    "I don't propose making these public, however if you are interested in access to specific routes "
    "feel free to drop me a message. Some of these are meant to be consumed after all.",
    routes=[
        Route("/", HomeEndpoint),
        Route("/travel", TravelEndpoint),
        Route("/camera", CameraEndpoint),
        Route("/achievements", AchievementsEndpoint),
        Mount(
            "/admin/",
            create_admin(
                tables=APP_CONFIG.table_classes,
                # Required when running under HTTPS:
                allowed_hosts=["data.skelmis.co.nz"],
                production=True,
            ),
        ),
        Mount("/static/", StaticFiles(directory="static")),
    ],
)
app.add_middleware(
    CustomHeaderMiddleware,
    mappings={
        "/authed/test": "TEST_KEY",
    },
)
app.include_router(endpoints.router)
async_util.create_task(digest_data(), task_id="FENZ_WORKER")


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
