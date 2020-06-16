from sqlalchemy.orm import Session

from database.schema.cart_schema import CartCreate, CartUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import Cart


def _generate_cart_data():
    return {
        "name": "Test",
    }


def create_random_cart() -> CartCreate:
    return CartCreate(**_generate_cart_data())


def create_random_cart_data():
    return _generate_cart_data()


def insert_cart(db: Session):
    cart_create = create_random_cart()
    return crud.cart.create(db, cart_create)


def delete_cart(db: Session, cart: Cart):
    crud.cart.remove(db, id=cart.id)
