from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import Order
from database.schema.order_schema import OrderCreate, OrderUpdate


class OrderCRUD(CRUDBase[Order, OrderCreate, OrderUpdate]):
    pass


order = OrderCRUD(Order)
