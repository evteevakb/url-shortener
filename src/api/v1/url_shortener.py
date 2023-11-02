"""Contains API endpoints"""
from typing import Any, Dict, List, Union

from fastapi import APIRouter, Depends, Request, status, Query
from fastapi.exceptions import HTTPException
from pyshorteners import Shortener
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.paginator import get_pagination_parameters
from core.logger import get_logger
from db.db import get_session
from schemas import short_url_schemas, usage_schemas
from services.short_url_services import short_url_crud
from services.usage_services import usage_crud


logger = get_logger(__name__)
router = APIRouter()
shortener = Shortener()


@router.post('/', response_model=short_url_schemas.ShortURL, status_code=status.HTTP_201_CREATED)
async def create_short_url(*, db: AsyncSession = Depends(get_session),
                           entity_in: short_url_schemas.ShortURLBase) -> Any:
    """Creates short URL for the given original URL.

    Args:
        db (AsyncSession, optional): database session. Defaults to Depends(get_session);
        entity_in (short_url_schemas.ShortURLBase): original URL to be shortened.

    Raises:
        HTTPException (410): if the requested URL is already in the database, but marked
            as deleted.

    Returns:
        short_url_schemas.ShortURL: unique identifier of the original URL, original URL itself
            and shortened URL for it.
    """
    short_url_db = await short_url_crud.read_by_initial_url(database=db,
                                                            initial_url=entity_in.initial_url)
    if not short_url_db:
        short_url_db = await short_url_crud.create(
            database=db,
            obj_in=short_url_schemas.ShortURLCreate(
                initial_url=entity_in.initial_url,
                short_url=shortener.tinyurl.short(entity_in.initial_url)))
        logger.info("Add new shortened URL %s for the original %s", short_url_db.short_url,
                    short_url_db.initial_url)
    if short_url_db.active is False:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Item deleted")
    return short_url_schemas.ShortURL(id=short_url_db.id,
                                      initial_url=short_url_db.initial_url,
                                      short_url=short_url_db.short_url)


@router.get('/{url_id}', response_model=short_url_schemas.ShortURLBase,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get_initial_url(*, db: AsyncSession = Depends(get_session), url_id: int,
                          request: Request) -> Any:
    """Returns original URL.

    Args:
        db (AsyncSession, optional): database session. Defaults to Depends(get_session);
        url_id (int): unique identifier of the requested URL;
        request (Request): client request.

    Raises:
        HTTPException (404): if a URL with requested url_id does not exist;
        HTTPException (410): if a URL has been already marked as deleted.

    Returns:
        short_url_schemas.ShortURLBase: original URL.
    """
    short_url_db = await short_url_crud.read(database=db, entity_id=url_id)
    if not short_url_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if short_url_db.active is False:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Item deleted")
    logger.info("Accessing original URL %s via short URL %s from client with host: %s, port: %s",
                short_url_db.initial_url, short_url_db.short_url, request.client.host,
                request.client.port)
    await usage_crud.create(database=db, obj_in=usage_schemas.UsageCreate(
        url_id=short_url_db.id,
        client_host=request.client.host,
        client_port=request.client.port))
    return short_url_schemas.ShortURLBase(initial_url=short_url_db.initial_url)


@router.get('/{url_id}/status', response_model=Union[int, List[usage_schemas.Usage]])
async def get_usage_status(*, db: AsyncSession = Depends(get_session), url_id: int,
                           full_info: bool = Query(default=False, alias='full-info'),
                           pagination_parameters: Dict[str, int] =
                           Depends(get_pagination_parameters)) -> Any:
    """Returns usage status of the requested URL.

    Args:
        db (AsyncSession, optional): database session. Defaults to Depends(get_session);
        url_id (int): unique identifier of the requested URL;
        full_info (bool): False for obtaining total number of requests, True -
            for additional detailed information about each request: date and time of each
            request, information about the client who completed the request. Defaults to False;
        pagination_parameters (Dict[str, int]): dictionary with pagination parameters containing
            the following fields: max_result - number of rows returned by a query (defaults to 10)
            and offset - skips the query by the specified number of rows (defaults to 0).

    Raises:
        HTTPException (404): if a URL with requested url_id does not exist.

    Returns:
        Union[int, List[Usage]]: total number of requests in case of full_info=False,
            otherwise a dictionary with information about date and time of each request and
            client host and port who completed the request.
    """
    short_url_db = await short_url_crud.read(database=db, entity_id=url_id)
    if not short_url_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    logger.info("Accessing usage status of original URL %s with shortened version %s",
                short_url_db.initial_url, short_url_db.short_url)
    return await usage_crud.get_status(database=db, url_id=short_url_db.id, full_info=full_info,
                                       pagination_parameters=pagination_parameters)


@router.delete('/{url_id}', status_code=status.HTTP_200_OK)
async def delete_url(*, db: AsyncSession = Depends(get_session), url_id: int) -> None:
    """Removes short URL by its ID. The entry in the database remains, but is marked as 'deleted'.

    Args:
        db (AsyncSession, optional): database session. Defaults to Depends(get_session);
        url_id (int): unique identifier of the requested URL.

    Raises:
        HTTPException (404): if a URL with requested url_id does not exist;
        HTTPException (410): if a URL has been already marked as deleted.
    """
    short_url_db = await short_url_crud.read(database=db, entity_id=url_id)
    if not short_url_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if short_url_db.active is False:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="Item already deleted")
    logger.info("Original URL %s with shortened version %s was marked as deleted",
                short_url_db.initial_url, short_url_db.short_url)
    await short_url_crud.delete(database=db, entity_id=url_id)
