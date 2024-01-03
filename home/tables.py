import datetime

from piccolo.columns.defaults import TimestampNow
from piccolo.table import Table
from piccolo.columns import Text, Date, Timestamp


class Base(Table):
    created_at: datetime.datetime = Timestamp(default=TimestampNow)
    last_modified_at: datetime.datetime = Timestamp(auto_update=datetime.datetime.now)


class Contact(Base):
    name: str = Text(unique=True, index=True)
    phone_number: str = Text(required=False)
    email_address: str = Text(required=False)
    home_address: str = Text(required=False)
    notes: str = Text(required=False)


class Jobs(Base):
    start_date: datetime.datetime = Date(required=True)
    end_date: datetime.datetime = Date(required=False, null=True)
    job_title: str = Text(required=True)
    company: str = Text(required=True)
    manager: str = Text(required=False, null=True)


class Books(Base):
    title: str = Text(required=False, null=True)
    author: str = Text(required=False, null=True)
    notes: str = Text(required=False, null=True)
