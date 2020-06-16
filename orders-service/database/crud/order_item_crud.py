from sqlalchemy.orm import Session

from .base import CRUDBase
from database.models import OrderItem
from database.schema.order_item_schema import OrderItemCreate, OrderItemUpdate


class OrderItemCRUD(CRUDBase[OrderItem, OrderItemCreate, OrderItemUpdate]):
    pass


order_item = OrderItemCRUD(OrderItem)
