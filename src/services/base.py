"""Contains mandatory methods for communication between the database and the application"""
from typing import Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from pyshorteners import Shortener

from ..models.base import Base
from ..core.logger import get_logger


ModelTypeT = TypeVar("ModelTypeT", bound=Base)
CreateSchemaTypeT = TypeVar("CreateSchemaTypeT", bound=BaseModel)
UpdateSchemaTypeT = TypeVar("UpdateSchemaTypeT", bound=BaseModel)

shortener = Shortener()
logger = get_logger(__name__)


class Repository:
    """Agreement which methods will be created to implement CRUD"""
    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def get_initial_url(self, *args, **kwargs):
        raise NotImplementedError

    async def get_short_url(self, *args, **kwargs):
        raise NotImplementedError

    async def mark_deleted(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelTypeT, CreateSchemaTypeT, UpdateSchemaTypeT]):
    """Base class for working with a database"""
    def __init__(self, model: Type[ModelTypeT]):
        self._model = model

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaTypeT) -> ModelTypeT:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = await self.get_short_url(db, obj_in_data['initial_url'])
        if not db_obj:
            db_obj = self._model(initial_url=obj_in_data['initial_url'],
                                 short_url=shortener.tinyurl.short(obj_in_data['initial_url']))
            db.add(db_obj)
            await db.commit()
        return db_obj

    async def get_short_url(self, db: AsyncSession, initial_url: str) -> Optional[ModelTypeT]:
        statement = select(self._model).where(self._model.initial_url==initial_url)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_initial_url(self, db: AsyncSession, short_url: str) -> Optional[ModelTypeT]:
        statement = select(self._model).where(self._model.short_url==short_url)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def mark_deleted(self, db: AsyncSession, *, short_url: str) -> ModelTypeT:
        db_obj = await self.get_initial_url(db, short_url)
        logger.info(db_obj)
        db_obj.active = False
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
