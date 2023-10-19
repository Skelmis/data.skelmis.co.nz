from piccolo.table import Table
from piccolo.columns import Text


class Contact(Table):
    name: str = Text(unique=True, index=True)
    phone_number: str = Text(required=False)
    address: str = Text(required=False)
    notes: str = Text(required=False)
