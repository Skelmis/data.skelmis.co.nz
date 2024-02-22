import datetime
from enum import Enum

from piccolo.table import Table
from piccolo.columns import Text, Date, BigInt, Varchar


class Contact(Table):
    name: str = Text(unique=True, index=True)
    phone_number: str = Text(required=False)
    email_address: str = Text(required=False)
    home_address: str = Text(required=False)
    notes: str = Text(required=False)
    full_name: str = Text(required=False)
    hidden_notes: str = Text(required=False)


class Jobs(Table):
    start_date: datetime.datetime = Date(required=True)
    end_date: datetime.datetime = Date(required=False, null=True)
    job_title: str = Text(required=True)
    company: str = Text(required=True)
    manager: str = Text(required=False, null=True)


class Notes(Table):
    topic: str = Text()
    note: str = Text()


class Incidents(Table):
    incident_number: str = Text(index=True, required=True)
    date: int = BigInt()
    location: str = Text()
    duration: int = BigInt(null=True)
    station: str = Text(required=True, index=True)
    result_code: str = Text(null=True)
    result_description: str = Text(null=True)


class F1FantasyPlayers(str, Enum):
    ETHAN = "Ethan"
    CHRIS = "Chris"
    CAMPBELL = "Campbell"
    TYLER = "Tyler"
    OLIVIA = "Olivia"
    JACK = "Jack"
    BRYN = "Bryn"


class F1Fantasy(Table):
    year: str = Varchar(length=2)
    team_name: str = Text()
    person: str = Text(choices=F1FantasyPlayers)
