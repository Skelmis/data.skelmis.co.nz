import os

import jinja2
from starlette.endpoints import HTTPEndpoint
from starlette.responses import HTMLResponse


ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(os.path.dirname(__file__), "templates")
    )
)
valid_pages = [
    {
        "name": "Travel information",
        "url": "/travel",
    },
]


class HomeEndpoint(HTTPEndpoint):
    async def get(self, request):
        template = ENVIRONMENT.get_template("home.html.jinja")

        content = template.render(title="Landing page", routes=valid_pages)

        return HTMLResponse(content)


class TravelEndpoint(HTTPEndpoint):
    async def get(self, request):
        template = ENVIRONMENT.get_template("travel.html.jinja")

        content = template.render(
            title="How I like to travel",
        )

        return HTMLResponse(content)
