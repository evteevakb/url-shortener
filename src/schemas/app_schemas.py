"""Request and response validation schemes for the models"""
from datetime import datetime

from pydantic import BaseModel


# Shared properties
class InitialURLBase(BaseModel):
    """Base validation scheme for initial URLs"""
    initial_url: str


class ShortURLBase(BaseModel):
    """Base validation scheme for short URLs"""
    short_url: str


# class UsageBase(BaseModel):
#     """Base validation scheme for URL Shortener usages"""
#     pass


# Properties to receive on entity creation
class ShortURLCreate(ShortURLBase):
    pass


# Properties to receive on entity update
class ShortURLUpdate(ShortURLBase):
    pass


# Properties shared by models stored in DB
class ShortURLInDBBase(ShortURLBase):
    id: int
    initial_url: str
    short_url: str
    created_at: datetime
    active: bool

    class Config:
        from_attributes = True


# Properties to return to client
class ShortURL(ShortURLBase):
    pass

class InitialURL(InitialURLBase):
    pass
