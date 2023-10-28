"""Contains a class that implements validation and work with the database for the Usages model"""

from .base import RepositoryDB
from ..models.models import Usages as UsagesModel
from ..schemas.usage_schemas import UsageCreate


class RepositoryUsage(RepositoryDB[UsagesModel, UsageCreate]):
    pass

usage_crud = RepositoryUsage(UsagesModel)
