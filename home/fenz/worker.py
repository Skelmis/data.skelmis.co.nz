import asyncio
import datetime

import bs4
import httpx

from home.tables import Incidents


async def save_row(
    incident_number: str,
    date: datetime.datetime | int,
    location: str,
    duration: datetime.timedelta,
    station: str,
    result_code: int,
    result_description: str,
):
    duration = (
        duration.total_seconds()
        if isinstance(duration, datetime.timedelta)
        else duration
    )
    if await Incidents.exists().where(
        (Incidents.incident_number == incident_number) & (Incidents.station == station)
    ):
        # Callout exists, populate results as it may be finished now
        await Incidents.update(
            {
                Incidents.result_code: result_code,
                Incidents.result_description: result_description,
                Incidents.duration: duration,
            }
        ).where(
            (Incidents.incident_number == incident_number)
            & (Incidents.station == station)
        )
    else:
        date = date.timestamp() if isinstance(date, datetime.datetime) else date

        await Incidents.insert(
            Incidents(
                incident_number=incident_number,
                date=date,
                location=location,
                duration=duration,
                station=station,
                result_code=result_code,
                result_description=result_description,
            )
        )


async def parse_row(row: bs4.Tag):
    data = []
    for column in row.find_all("div", {"class": "report__table__row"}):
        raw_data: bs4.Tag = column.find(
            "div", {"class": "report__table__cell report__table__cell--value"}
        ).find("p")
        data.append(raw_data.getText())

    hour, minute, second = data[3].split(":")
    try:
        result_code, result_description = data[5].split(": ", maxsplit=1)
    except ValueError:
        result_code, result_description = "", ""

    stations = data[4].split(", ")
    for station in stations:
        await save_row(
            data[0],
            datetime.datetime.strptime(data[1], "%d/%m/%Y %H:%M:%S"),
            data[2],
            datetime.timedelta(
                hours=int(hour), minutes=int(minute), seconds=int(second)
            ),
            station,
            result_code,
            result_description,
        )


async def digest_data():
    while True:
        base_url = "https://www.fireandemergency.nz/incidents-and-news/incident-reports/incidents?region={}&day={}"
        async with httpx.AsyncClient(
            headers={"User-Agent": "User-Agent: Python 3.11"}
        ) as client:
            for region in [1, 2, 3]:
                for day in [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]:
                    url = base_url.format(region, day)
                    resp = await client.get(url)
                    soup = bs4.BeautifulSoup(resp.text, features="html.parser")
                    rows = (
                        soup.find(
                            "div",
                            {"class": "article__wrapper article__wrapper--wide"},
                        )
                        .find("div", {"class": "report"})
                        .find_all("div", {"class": "row"})
                    )
                    wanted_row = rows[-1]
                    wanted_rows = wanted_row.find_all(
                        "div", {"class": "report__table__body"}
                    )
                    for row in wanted_rows:
                        await parse_row(row)

        await asyncio.sleep(datetime.timedelta(hours=15).total_seconds())
