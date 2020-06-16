from sqlalchemy.orm import Session

from database.schema.order_item_schema import OrderItemCreate, OrderItemUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import OrderItem


def _generate_order_item_data():
    return {
        "id": 1,
        "order_id": 1,
        "item_id": 1,
        "pvp": 50.63,
        "quantity": 20,
        "notes": "This is a note",
        "pvp_with_discount": 50
    }


def create_random_order_item() -> OrderItemCreate:
    return OrderItemCreate(**_generate_order_item_data())


def create_random_order_item_data():
    return _generate_order_item_data()


def insert_order_item(db: Session):
    order_item_create = create_random_order_item()
    return crud.order_item.create(db, order_item_create)


def delete_order_item(db: Session, order_item: OrderItem):
    crud.order_item.remove(db, id=order_item.id)
