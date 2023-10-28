"""Contains a class that implements validation and work with the database for the ShortURLs model"""
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .base import RepositoryDB
from ..models.models import ShortURLs as ShortURLsModel
from ..schemas.short_url_schemas import ShortURLCreate


class RepositoryShortURL(RepositoryDB[ShortURLsModel, ShortURLCreate]):
    """Validation and work with the database for the ShortURLs model"""
    async def read_by_short_url(self, database: AsyncSession,
                                short_url: int) -> Optional[ShortURLsModel]:
        statement = select(self._model).where(self._model.short_url == short_url)
        results = await database.execute(statement=statement)
        return results.scalar_one_or_none()

    async def read_by_initial_url(self, database: AsyncSession,
                                  initial_url: int) -> Optional[ShortURLsModel]:
        statement = select(self._model).where(self._model.initial_url == initial_url)
        results = await database.execute(statement=statement)
        return results.scalar_one_or_none()


short_url_crud = RepositoryShortURL(ShortURLsModel)
