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
    """Accepts an original URL string to be shortened in the request body and returns a response
        with code `201`."""
    short_url_db = await crud.create(db=db, obj_in=initial_url)
    short_url = app_schemas.ShortURL(initial_url=initial_url.initial_url,
                                     short_url=short_url_db.short_url)
    return short_url


@router.get('/{short_url:path}', response_model=app_schemas.InitialURL,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_initial_url(*, db: AsyncSession = Depends(get_session), short_url: str) -> Any:
    logger.info(short_url)
    initial_url_db = await crud.get_initial_url(db=db, short_url=short_url)
    if not initial_url_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return app_schemas.InitialURL(initial_url=initial_url_db.initial_url)


# @router.get('/{shorten-url-id}/status')
# async def get_usage_status():
#     """GET /<shorten-url-id>/status?[full-info]&[max-result=10]&[offset=0]
#     Метод принимает в качестве параметра идентификатор сокращённого URL и возвращает информацию о количестве переходов, совершенных по ссылке.

#     В ответе может содержаться как общее количество совершенных переходов, так и дополнительная детализированная информация о каждом переходе (наличие **query**-параметра **full-info** и параметров пагинации):
#     - дата и время перехода/использования ссылки;
#     - информация о клиенте, выполнившем запрос;
    
#     """

# @router.patch('/{shorten-url-id}')
# async def delete_url():
#     """Реализуйте возможность «удаления» сохранённого URL. Запись должна остаться, но помечаться как удалённая.
#     При попытке получения полного URL возвращать ответ с кодом `410 Gone`."""
