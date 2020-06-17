from sqlalchemy.orm import Session

from database.schema.client_cart_schema import ClientCartCreate, ClientCartUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import ClientCart


def _generate_client_cart_data():
    return {
        "cart_id": 1,
        "date_joined": "2020-01-01",
        "client_id": 1
    }


def create_random_client_cart() -> ClientCartCreate:
    return ClientCartCreate(**_generate_client_cart_data())


def create_random_client_cart_data():
    return _generate_client_cart_data()


def insert_client_cart(db: Session):
    client_cart_create = create_random_client_cart()
    return crud.client_cart.create(db, client_cart_create)


def delete_client_cart(db: Session, client_cart: ClientCart):
    crud.client_cart.remove(db, id=client_cart.id)
