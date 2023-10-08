"""Contains API endpoints"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.db import get_session

router = APIRouter()


@router.get('/ping')
async def ping_database(db: AsyncSession = Depends(get_session)):
    try:
        start_time = time.time()
        await db.execute('SELECT 1')
        end_time = time.time()
        return end_time - start_time
    except DBAPIError:
        return None
