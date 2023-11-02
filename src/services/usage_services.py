"""Contains a class that implements validation and work with the database for the Usages model"""
from typing import Dict, List, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from services.base import RepositoryDB
from models.models import Usages as UsagesModel
from schemas.usage_schemas import Usage, UsageCreate


class RepositoryUsage(RepositoryDB[UsagesModel, UsageCreate]):
    """Validation and work with the database for the Usages model"""
    async def get_status(self, database: AsyncSession, url_id: int, full_info: bool,
                         pagination_parameters: Dict[str, int]) -> Union[int, List[Usage]]:
        """Returns usage status of the requested URL.

        Args:
            database (AsyncSession): database session;
            url_id (int): unique identifier of the requested URL;
            full_info (bool): False for obtaining total number of requests, True -
                for additional detailed information about each request: date and time of each
                request, information about the client who completed the request. Defaults to False;
            pagination_parameters (Dict[str, int]): pagination parameters containing
                max_result - number of rows returned by a query (defaults to 10) and
                offset - skips the query by the specified number of rows (defaults to 0).

        Returns:
            Union[int, List[Usage]]: total number of requests in case of full_info=False,
                otherwise a dictionary with information about date and time of each request and
                client host and port who completed the request.
        """
        if full_info:
            statement = select(self._model).where(self._model.url_id == url_id).offset(
                pagination_parameters['offset']).limit(pagination_parameters['max_result'])
        else:
            statement = select(self._model).where(self._model.url_id == url_id)
        results = await database.execute(statement=statement)
        return results.scalars().all() if full_info else len(results.fetchall())


usage_crud = RepositoryUsage(UsagesModel)
