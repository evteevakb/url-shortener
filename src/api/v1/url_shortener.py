"""Contains API endpoints"""
from typing import Any

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.logger import get_logger
from ...db.db import get_session
from ...schemas import app_schemas
from ...services.app_services import crud


logger = get_logger(__name__)
router = APIRouter()


@router.post('/', response_model=app_schemas.ShortURL, status_code=status.HTTP_201_CREATED)
async def create_short_url(*, db: AsyncSession = Depends(get_session),
                           initial_url: app_schemas.InitialURL) -> Any:
    """Creates short URL for the given initial URL and returns a response with code `201`.
        Returns existed short URL if the entry already exists in the database. Retuns an error
        response with code `410` if the entry was marked as 'deleted'."""
    short_url_db = await crud.create(db=db, obj_in=initial_url)
    if short_url_db.active is False:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Item deleted")
    short_url = app_schemas.ShortURL(initial_url=initial_url.initial_url,
                                     short_url=short_url_db.short_url)
    return short_url


@router.get('/{short_url:path}', response_model=app_schemas.InitialURL,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_initial_url(*, db: AsyncSession = Depends(get_session), short_url: str) -> Any:
    short_url_db = await crud.get_initial_url(db=db, short_url=short_url)
    if not short_url_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if short_url_db.active is False:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Item deleted")
    # await crud.update
    return app_schemas.InitialURL(initial_url=short_url_db.initial_url)


# @router.get('/{short_url:path}/status')
# async def get_usage_status(*, db: AsyncSession = Depends(get_session), short_url: str) -> Any:
    #     """GET /<shorten-url-id>/status?[full-info]&[max-result=10]&[offset=0]
    #     Метод принимает в качестве параметра идентификатор сокращённого URL и возвращает информацию о количестве переходов, совершенных по ссылке.

    #     В ответе может содержаться как общее количество совершенных переходов, так и дополнительная детализированная информация о каждом переходе (наличие **query**-параметра **full-info** и параметров пагинации):
    #     - дата и время перехода/использования ссылки;
    #     - информация о клиенте, выполнившем запрос;
    #     """


@router.delete('/{short_url:path}', status_code=status.HTTP_200_OK)
async def delete_url(*, db: AsyncSession = Depends(get_session), short_url: str) -> None:
    """'Deleting' a saved URL. The entry in the database remains, but is marked as 'deleted'"""
    await crud.mark_deleted(db=db, short_url=short_url)
