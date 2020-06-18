from sqlalchemy.orm import Session

from .base import CRUDBase
from app.database.models import Discount
from app.database.schema.discount_schema import DiscountCreate, DiscountUpdate


class DiscountCRUD(CRUDBase[Discount, DiscountCreate, DiscountUpdate]):
    pass


discount = DiscountCRUD(Discount)
