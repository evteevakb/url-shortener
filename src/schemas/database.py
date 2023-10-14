"""Schemas for database endpoints"""
from pydantic import BaseModel


class DatabasePing(BaseModel):
    """Response model for ping endpoint:
        ping_time (float): database ping time in seconds.
    """
    ping_time: float
