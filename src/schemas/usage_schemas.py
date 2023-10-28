"""Request and response validation schemes for the Usages model"""
from datetime import datetime

from pydantic import BaseModel


class UsageBase(BaseModel):
    """Base validation scheme for a usage"""


class UsageCreate(UsageBase):
    """Validation scheme for usage creation.

    Args:
        url_id (int): unique identifier of short URL record in the database;
        client_host (str): host of the client making the request;
        client_port (int): client port.
    """
    url_id: int
    client_host: str
    client_port: int


class Usage(UsageBase):
    """Validation scheme for usage returned to a client.

    Args:
        url_id (int): unique identifier of short URL record in the database;
        usage_datetime (datetime): date and time of the request;
        client_host (str): host of the client making the request;
        client_port (int): client port.
    """
    url_id: int
    usage_datetime: datetime
    client_host: str
    client_port: int
