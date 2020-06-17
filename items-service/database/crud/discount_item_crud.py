from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import DiscountItem
from database.schema.discount_item_schema import DiscountItemCreate, DiscountItemUpdate


class DiscountItemCRUD(CRUDBase[DiscountItem, DiscountItemCreate, DiscountItemUpdate]):
    pass


discount_item = DiscountItemCRUD(DiscountItem)
