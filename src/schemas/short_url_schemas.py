"""Request and response validation schemes for the ShortURLs model"""
from pydantic import BaseModel


class ShortURLBase(BaseModel):
    """Base validation scheme for short URLs.

    Args:
       initial_url (str): original URL to be shortened.
    """
    initial_url: str


class ShortURLCreate(ShortURLBase):
    """Validation scheme for short URL creation.

    Args:
        initial_url (str): original URL;
        short_url (str): short URL.
    """
    short_url: str


class ShortURL(ShortURLBase):
    """Validation scheme for short URL returned to a client.

    Args:
        id (int): unique identifier of the record in the database;
        initial_url (str): original URL;
        short_url (str): short URL.
    """
    id: int
    short_url: str
