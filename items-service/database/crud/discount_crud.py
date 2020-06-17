from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import Discount
from database.schema.discount_schema import DiscountCreate, DiscountUpdate


class DiscountCRUD(CRUDBase[Discount, DiscountCreate, DiscountUpdate]):
    pass


discount = DiscountCRUD(Discount)
