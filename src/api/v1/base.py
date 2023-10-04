"""Contains router with handlers"""
from fastapi import APIRouter

from .url_shortener import router


api_router = APIRouter()
api_router.include_router(router, prefix="/url_shortener", tags=["url_shortener"])
