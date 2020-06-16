from sqlalchemy.orm import Session

from database.schema.cart_item_schema import CartItemCreate, CartItemUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import CartItem


def _generate_cart_item_data():
    return {
        "cart_id": 1,
        "quantity": 12,
        "notes": "Test notes",
        "item_id": 1
    }


def create_random_cart_item() -> CartItemCreate:
    return CartItemCreate(**_generate_cart_item_data())


def create_random_cart_item_data():
    return _generate_cart_item_data()


def insert_cart_item(db: Session):
    cart_item_create = create_random_cart_item()
    return crud.cart_item.create(db, cart_item_create)


def delete_cart_item(db: Session, cart_item: CartItem):
    crud.cart_item.remove(db, id=cart_item.id)
