"""Contains router with handlers"""
from fastapi import APIRouter

from .database import router as database_router
from .url_shortener import router


api_router = APIRouter()
api_router.include_router(database_router, prefix='/database', tags=['database'])
api_router.include_router(router, prefix='/url_shortener', tags=['url_shortener'])
