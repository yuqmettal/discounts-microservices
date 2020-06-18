from sqlalchemy.orm import Session

from .base import CRUDBase
from app.database.models import Item
from app.database.schema.item_schema import ItemCreate, ItemUpdate


class ItemCRUD(CRUDBase[Item, ItemCreate, ItemUpdate]):
    pass


item = ItemCRUD(Item)
