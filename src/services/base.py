"""каркас описания обязательных методов общения БД и сервиса"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from pyshorteners import Shortener

from ..models.base import Base
from ..core.logger import get_logger

ModelTypeT = TypeVar("ModelTypeT", bound=Base)
CreateSchemaTypeT = TypeVar("CreateSchemaTypeT", bound=BaseModel)
# UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

shortener = Shortener()
logger = get_logger(__name__)


class Repository:
    """контракт или договоренность, какие методы будут созданы, для реализации CRUD"""
    async def create(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelTypeT, CreateSchemaTypeT]):
    def __init__(self, model: Type[ModelTypeT]):
        self._model = model

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaTypeT) -> ModelTypeT:
        obj_in_data = jsonable_encoder(obj_in)
        short_url = shortener.tinyurl.short(obj_in_data['initial_url'])
        db_obj = self._model(initial_url=obj_in_data['initial_url'], short_url=short_url)
        db.add(db_obj)
        await db.commit()
        return db_obj
