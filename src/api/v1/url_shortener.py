"""Contains API endpoints"""
from typing import Any

from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from pyshorteners import Shortener
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.logger import get_logger
from ...db.db import get_session
from ...schemas import short_url_schemas, usage_schemas
from ...services.short_url_services import short_url_crud
from ...services.usage_services import usage_crud


logger = get_logger(__name__)
router = APIRouter()
shortener = Shortener()


@router.post('/', response_model=short_url_schemas.ShortURL, status_code=status.HTTP_201_CREATED)
async def create_short_url(*, db: AsyncSession = Depends(get_session),
                           entity_in: short_url_schemas.ShortURLBase) -> Any:
    """Creates short URL for the given initial URL and returns a response with code `201`.
        Returns existed short URL if the entry already exists in the database. Retuns an error
        response with code `410` if the entry was marked as 'deleted'."""
    short_url_db = await short_url_crud.read_by_initial_url(database=db,
                                                            initial_url=entity_in.initial_url)
    if not short_url_db:
        short_url_db = await short_url_crud.create(
            database=db,
            obj_in=short_url_schemas.ShortURLCreate(
                initial_url=entity_in.initial_url,
                short_url=shortener.tinyurl.short(entity_in.initial_url)))
    if short_url_db.active is False:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Item deleted")
    return short_url_schemas.ShortURL(id=short_url_db.id,
                                      initial_url=short_url_db.initial_url,
                                      short_url=short_url_db.short_url)


@router.get('/{short_url:path}', response_model=short_url_schemas.ShortURLBase,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_initial_url(*, db: AsyncSession = Depends(get_session), short_url: str,
                          request: Request) -> Any:
    logger.info("Host: %s, port: %s", request.client.host, request.client.port)
    logger.info("Host type: %s, port type: %s", type(request.client.host), type(request.client.port))
    short_url_db = await short_url_crud.read_by_short_url(database=db, short_url=short_url)
    if not short_url_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if short_url_db.active is False:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Item deleted")
    await usage_crud.create(database=db, obj_in=usage_schemas.UsageCreate(
        url_id=short_url_db.id,
        client_host=request.client.host,
        client_port=request.client.port))
    return short_url_schemas.ShortURLBase(initial_url=short_url_db.initial_url)


# @router.get('/{short_url:path}/status')
# async def get_usage_status(*, db: AsyncSession = Depends(get_session), short_url: str) -> Any:
    #     """GET /<shorten-url-id>/status?[full-info]&[max-result=10]&[offset=0]
    #     Метод принимает в качестве параметра идентификатор сокращённого URL и возвращает информацию о количестве переходов, совершенных по ссылке.

    #     В ответе может содержаться как общее количество совершенных переходов, так и дополнительная детализированная информация о каждом переходе (наличие **query**-параметра **full-info** и параметров пагинации):
    #     - дата и время перехода/использования ссылки;
    #     - информация о клиенте, выполнившем запрос;
    #     """


@router.delete('/{url_id}', status_code=status.HTTP_200_OK)
async def delete_url(*, db: AsyncSession = Depends(get_session), url_id: int) -> None:
    """Removes short URL by its ID. The entry in the database remains, but is marked as 'deleted'"""
    short_url_db = await short_url_crud.read(database=db, entity_id=url_id)
    if not short_url_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if short_url_db.active is False:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Item already deleted")
    await short_url_crud.delete(database=db, entity_id=url_id)
