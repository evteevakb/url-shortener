"""Contains application middleware"""
from fastapi import Request, status
from fastapi.exceptions import HTTPException

from ...core.config import BLACK_LIST
from ...core.logger import get_logger


logger = get_logger(__name__)


async def check_allowed_ip(request: Request) -> None:
    """Checks if client address is in the black list.

    Args:
        request (Request): incoming request.

    Raises:
        HTTPException: if client host is in the black list.
    """
    client_host = request.client.host
    if client_host in BLACK_LIST:
        logger.debug("Attempt of accessing application from banned host: %s", client_host)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
