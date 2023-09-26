import typing as t

from fastapi import FastAPI
from piccolo_admin.endpoints import create_admin
from piccolo.engine import engine_finder
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from home.piccolo_app import APP_CONFIG

app = FastAPI(
    routes=[
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


@app.get("/")
async def home():
    return RedirectResponse("/redoc")


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
