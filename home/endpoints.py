import os
from datetime import timedelta

import httpx
import humanize
import jinja2
from starlette.endpoints import HTTPEndpoint
from starlette.responses import HTMLResponse

from home.timed_cache import TimedCache, NonExistentEntry

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
                )
                if response.status_code != 200:
                    raise ValueError(
                        f"Package {package} returned {response.status_code}"
                    )

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
