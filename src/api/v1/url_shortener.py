"""Contains API endpoints"""
# from typing import Any

from fastapi import APIRouter #, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.sql import text

# from ...db.db import get_session
# from ...schemas import url_shortener
# from ...services.url_shortener import crud

router = APIRouter()


# @router.post('/shorten', response_model=url_shortener.ShortURL,
#              status_code=status.HTTP_201_CREATED)
# async def create_short_url( *, db: AsyncSession = Depends(get_session),
#                            initial_url: url_shortener.InitialURL) -> Any:
#     """Creates new short URL for the given URL or returns"""
#     # check if shortened URL already exists
#     short_url = await crud.get(db=db, id=id)
#     if not short_url:
#         short_url = await crud.create(db=db, obj_in=initial_url)
#     return short_url
