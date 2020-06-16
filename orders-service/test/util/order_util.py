from sqlalchemy.orm import Session

from database.schema.order_schema import OrderCreate, OrderUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import Order


def _generate_order_data():
    return {
        "retailer_id": 1,
        "address_id": 1,
        "client_id": 1,
        "total_cost": 150.6,
        "shipping_cost": 5.33,
        "delivery_date": "2020-06-12"
    }


def create_random_order() -> OrderCreate:
    return OrderCreate(**_generate_order_data())


def create_random_order_data():
    return _generate_order_data()


def insert_order(db: Session):
    order_create = create_random_order()
    return crud.order.create(db, order_create)


def delete_order(db: Session, order: Order):
    crud.order.remove(db, id=order.id)
