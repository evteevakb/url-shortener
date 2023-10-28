"""Request and response validation schemes for the Usages model"""
from pydantic import BaseModel


# Shared properties
class UsageBase(BaseModel):
    pass


# Properties to receive on usage creation
class UsageCreate(UsageBase):
    url_id: int
    client_host: str
    client_port: int
