"""Contains API endpoints"""
from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.sql import text

from ...db.db import get_session
from ...schemas import app_schemas
from ...services.app_services import crud

router = APIRouter()


@router.post('/', response_model=app_schemas.ShortURL, status_code=status.HTTP_201_CREATED)
async def create_short_url(*, db: AsyncSession = Depends(get_session),
                           original_url_in: app_schemas.ShortURLCreate) -> Any:
    """Метод принимает в теле запроса строку URL для сокращения и возвращает ответ с кодом `201`."""
    short_url_db = await crud.create(db=db, obj_in=original_url_in)
    short_url = app_schemas.ShortURL(initial_url=original_url_in.initial_url,
                                     short_url=short_url_db.short_url)
    return short_url


# @router.post('/shorten', response_model=app_schemas.ShortURL,
#              status_code=status.HTTP_201_CREATED)
# async def create_short_url( *, db: AsyncSession = Depends(get_session),
#                            initial_url: url_shortener.InitialURL) -> Any:
#     """Creates new short URL for the given URL or returns"""
#     # check if shortened URL already exists
#     short_url = await crud.get(db=db, id=id)
#     if not short_url:
#         short_url = await crud.create(db=db, obj_in=initial_url)
#     return short_url

# @router.get('/{shorten-url-id}', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
# async def get_original_url():
#     """GET /<shorten-url-id>
#     Метод принимает в качестве параметра идентификатор сокращённого URL и возвращает ответ с кодом `307`
#     и оригинальным URL в заголовке `Location`."""
#     pass


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
