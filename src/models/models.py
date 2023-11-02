"""Database models"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy_utils import URLType

from models.base import Base


class Usages(Base):
    """Model of the 'usages' table"""
    __tablename__ = 'usages'
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('short_urls.id'))
    usage_datetime = Column(DateTime, index=True, default=datetime.utcnow)
    client_host = Column(String, nullable=False)
    client_port = Column(Integer, nullable=False)


class ShortURLs(Base):
    """Model of the 'short_urls' table"""
    __tablename__ = 'short_urls'
    id = Column(Integer, primary_key=True)
    initial_url = Column(URLType, nullable=False, unique=True)
    short_url = Column(URLType, nullable=False, unique=True)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    active = Column(Boolean, default=True)
