from piccolo.table import Table
from piccolo.columns import Text


class Contact(Table):
    name: str = Text(primary_key=True, unique=True, index=True)
    address: str = Text(required=False)
    phone_number: str = Text(required=False)
    notes: str = Text(required=False)
