"""Contains endpoints of the database"""
import time
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from ...db.db import get_session
from ...core.logger import get_logger
from ...schemas.database import DatabasePing


logger = get_logger(__name__)
router = APIRouter()


@router.get('/ping', response_model=DatabasePing)
async def ping_database(database: AsyncSession = Depends(get_session)) -> Dict[str, float]:
    """Pings the database to check the connection to it.

    Args:
        database (AsyncSession, optional): database instance. Defaults to Depends(get_session).

    Raises:
        HTTPException: if the connection to the database cannot be established.

    Returns:
        Dict[str, float]: contains ping time in seconds.
    """
    try:
        start_time = time.time()
        await database.execute(text('SELECT 1'))
        end_time = time.time()
        return {'ping_time': f'{round((end_time - start_time), 2)}'}
    except OSError as exc:
        logger.error(exc)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="Database is unavailable") from exc
