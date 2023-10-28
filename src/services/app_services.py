from ..models.models import ShortURLs as ShortURLsModel
from ..schemas.app_schemas import ShortURLCreate, ShortURLUpdate
from .base import RepositoryDB


class RepositoryShortURL(RepositoryDB[ShortURLsModel, ShortURLCreate, ShortURLUpdate]):
    pass

crud = RepositoryShortURL(ShortURLsModel)
