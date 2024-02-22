import logging
import os
import secrets
import textwrap
from datetime import timedelta
from string import Template
from typing import Annotated, Any

import black
import httpx
import humanize
import jinja2
from fastapi import Form, APIRouter
from piccolo.apps.user.tables import BaseUser
from piccolo.columns import Or
from piccolo.utils.pydantic import create_pydantic_model
from starlette.endpoints import HTTPEndpoint
from starlette.responses import HTMLResponse, Response

from commons.caching.timed_cache import TimedCache, NonExistentEntry

from home import fenz
from home.tables import Incidents, Contact

router = APIRouter()
log = logging.getLogger(__name__)
ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        searchpath=os.path.join(os.path.dirname(__file__), "templates")
    )
)
cache: TimedCache = TimedCache(lazy_eviction=False)
valid_pages = [
    {
        "name": "Travel information",
        "url": "/travel",
    },
    {"name": "Camera settings", "url": "/camera"},
    {"name": "Various achievements", "url": "/achievements"},
    {"name": "Burp request to Python HTTPX", "url": "/burp"},
]
packages = [
    {
        "package_name": "discord-anti-spam",
        "description": "A library agnostic Discord anti spam package.",
        "url": "https://github.com/Skelmis/Discord-Anti-Spam",
    },
    {
        "package_name": "bot-base",
        "description": "A feature rich discord bot base to subclass and hit the ground running. Archived.",
        "url": "https://github.com/Skelmis/Discord-Bot-Base",
    },
    {
        "package_name": "function-cooldowns",
        "description": "A simplistic decorator based approach to rate limiting function calls.",
        "url": "https://github.com/Skelmis/Function-Cooldowns",
    },
    {
        "package_name": "alaric",
        "description": "A simplistic yet powerful asynchronous MongoDB query engine.",
        "url": "https://github.com/Skelmis/Alaric",
    },
    {
        "package_name": "zonis",
        "description": "Agnostic IPC for Python programs.",
        "url": "https://github.com/Skelmis/Zonis",
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


class CameraEndpoint(HTTPEndpoint):
    async def get(self, request):
        template = ENVIRONMENT.get_template("camera.html.jinja")

        content = template.render(
            title="Photography related information",
        )

        return HTMLResponse(content)


class AchievementsEndpoint(HTTPEndpoint):
    @staticmethod
    async def fetch_stats_for_package(package) -> tuple[str, int]:
        try:
            return cache.get_entry(package)
        except NonExistentEntry:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.pepy.tech/api/v2/projects/{package}",
                    headers={"X-API-KEY": os.environ.get("PEPY_API_KEY", "")},
                )
                if response.status_code != 200:
                    log.warning(f"Package {package} returned {response.status_code}")
                    value = -1
                else:
                    value = response.json()["total_downloads"]
                humaized = humanize.intcomma(value)
                cache.add_entry(package, (humaized, value), ttl=timedelta(hours=12))
                return humaized, value

    async def fetch_stats(self) -> tuple[list[tuple[str, str, str, str, str]], str]:
        data = []
        total_count = 0
        for package in packages:
            human_total, raw_total = await self.fetch_stats_for_package(
                package["package_name"]
            )
            total_count += raw_total
            data.append(
                (
                    package["package_name"],
                    package["description"],
                    human_total,
                    package["url"],
                    f"https://www.pepy.tech/projects/{package['package_name']}",
                )
            )

        return data, humanize.intcomma(total_count)

    async def get(self, request):
        template = ENVIRONMENT.get_template("achievements.jinja")

        projects, total = await self.fetch_stats()
        content = template.render(
            title="Things I like to show off", projects=projects, total=total
        )

        return HTMLResponse(content)


@router.get("/burp")
async def get_burp():
    template = ENVIRONMENT.get_template("burp.jinja")

    content = template.render(
        title="Burp request to Python HTTPX",
    )

    return HTMLResponse(content)


@router.post("/burp")
async def post_burp(code: Annotated[str, Form()] = None):
    httpx_code = textwrap.dedent(
        """
    import asyncio

    import httpx
    
    
    async def main():
        async with httpx.AsyncClient() as client:
            resp: httpx.Response = await client.$TYPE(
                url="https://$URL",
                headers=$HEADERS,
                cookies=$COOKIES,
                $EXTRA
            )
            print(resp.status_code)
            print(resp.text)
    
    
    if __name__ == "__main__":
        asyncio.run(main())
    """
    )
    string_template: Template = Template(httpx_code)

    try:
        # Handle input request
        code = code.replace("\r\n", "\n")
        headers, body = code.split("\n\n")
        headers: list[str] = headers.split("\n")  # type: ignore
        request_type, uri, _ = headers.pop(0).split(" ")
        request_type: str = request_type.lower()
        header_jar: dict[str, str] = {}
        for line in headers:
            k, v = line.split(": ", maxsplit=1)
            header_jar[k] = v

        cookies: list[tuple[str, str]] = []
        raw_cookies = header_jar.pop("Cookie", "")
        for cookie in raw_cookies.split(";"):
            if "=" not in cookie:
                continue
            k, v = cookie.split("=", maxsplit=1)
            cookies.append((k.strip(), v))

        extra = ""
        if request_type.lower() == "post":
            is_json = "json" in header_jar.get("Content-Type", "")
            if is_json:
                extra = f'json="{body}"'
            else:
                fixed_body: dict[str, Any] = {}
                for entry in body.split("&"):
                    if "=" not in entry:
                        continue
                    k, v = entry.split("=", maxsplit=1)
                    fixed_body[k] = v
                extra = f"data={fixed_body}"

        url = header_jar["Host"] + uri
        result = string_template.substitute(
            URL=url,
            HEADERS=header_jar,
            COOKIES=cookies,
            TYPE=request_type.lower(),
            EXTRA=extra,
        )

        mode = black.FileMode()
        fast = False
        try:
            result = black.format_file_contents(result, fast=fast, mode=mode)
        except black.parsing.InvalidInput:
            pass

    except:
        result = "Something went wrong parsing your request"

    template = ENVIRONMENT.get_template("burp.jinja")
    content = template.render(
        title="Burp request to Python HTTPX",
        code=result,
        raw_code=code,
    )

    return HTMLResponse(content)


IncidentModel = create_pydantic_model(Incidents)


@router.post("/fenz/import/{access_key}", status_code=204)
async def create_fenz_entry(entry: IncidentModel, access_key: str):
    """Import an existing FENZ entry."""
    if access_key != os.environ.get("FENZ_IMPORT_KEY", secrets.token_hex(32)):
        return Response(status_code=401)

    await fenz.save_row(**entry.dict())
    return Response(status_code=204)


# noinspection PyTypeChecker
@router.get("/im-dead", include_in_schema=False)
async def im_dead(password: str = None):
    if password is None:
        return Response(status_code=404)

    tyler_hash = os.environ.get("TYLER_HASH")
    chris_hash = os.environ.get("CHRIS_HASH")

    algorithm, iterations_, salt, hashed = BaseUser.split_stored_password(tyler_hash)
    iterations = int(iterations_)
    computed_hash_for_tyler = BaseUser.hash_password(password, salt, iterations)
    algorithm, iterations_, salt, hashed = BaseUser.split_stored_password(chris_hash)
    iterations = int(iterations_)
    computed_hash_for_chris = BaseUser.hash_password(password, salt, iterations)
    if computed_hash_for_tyler != tyler_hash and computed_hash_for_chris != chris_hash:
        return Response(status_code=401)

    # It's one of the two by now
    name = "Tyler" if tyler_hash == computed_hash_for_tyler else "Chris"
    people = await Contact.select().where(
        Or(
            Contact.name == "Tyler Evans",
            Or(
                Contact.name == "Chris Penno",
                Or(
                    Contact.name == "Jacob Harris",
                    Contact.name == "Patrick Harris",
                ),
            ),
        )
    )
    people = list(sorted(people, key=lambda p: p["name"]))

    template = ENVIRONMENT.get_template("dead.jinja")
    content = template.render(title=f"👋 {name}", people=people)

    return HTMLResponse(content)
