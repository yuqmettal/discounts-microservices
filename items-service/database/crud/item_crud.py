from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import Item
from database.schema.item_schema import ItemCreate, ItemUpdate


class ItemCRUD(CRUDBase[Item, ItemCreate, ItemUpdate]):
    pass


item = ItemCRUD(Item)
