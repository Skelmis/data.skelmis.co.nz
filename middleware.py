import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dispatch=None, *, mappings: dict[str, str]):
        super().__init__(app, dispatch)
        self.mappings: dict[str, str] = mappings

    async def dispatch(self, request, call_next):
        route = request.url.path
        if route not in self.mappings:
            # Not an authed route
            return await call_next(request)

        auth_header = request.headers.get("X-API-KEY", None)
        if auth_header is None:
            return JSONResponse(status_code=403, content="Missing header X-API-KEY")

        expected_value = os.environ[self.mappings[route]]

        if auth_header != expected_value:
            return JSONResponse(status_code=403, content="Incorrect X-API-KEY")

        return await call_next(request)
