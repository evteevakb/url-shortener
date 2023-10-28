"""Contains a class that implements validation and work with the database for the Usages model"""
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .base import RepositoryDB
from ..models.models import Usages as UsagesModel
from ..schemas.usage_schemas import UsageCreate


class RepositoryUsage(RepositoryDB[UsagesModel, UsageCreate]):
    """Validation and work with the database for the Usages model"""
    async def get_status(self, database: AsyncSession, url_id: int, full_info: bool,
                         pagination_parameters: Dict[str, int]):
        if full_info:
            statement = select(self._model).where(self._model.url_id == url_id).offset(
                pagination_parameters['offset']).limit(pagination_parameters['max_result'])
        else:
            statement = select(self._model).where(self._model.url_id == url_id)
        results = await database.execute(statement=statement)
        return results.scalars().all() if full_info else len(results.fetchall())


usage_crud = RepositoryUsage(UsagesModel)
