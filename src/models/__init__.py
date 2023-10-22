"""Collects all models in one place"""
__all__ = [
    "Base",
    "ShortURLs",
    "Usages",
]

from .base import Base
from .models import ShortURLs, Usages
