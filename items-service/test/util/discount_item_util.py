from sqlalchemy.orm import Session

from database.schema.discount_item_schema import DiscountItemCreate, DiscountItemUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import DiscountItem


def _create_discount_item_data():
    return {
        "discount_id": 1,
        "item_id": 1
    }


def create_random_discount_item() -> DiscountItemCreate:
    return DiscountItemCreate(**_create_discount_item_data())


def create_random_discount_item_data():
    return _create_discount_item_data()


def insert_discount_item(db: Session):
    discount_item_create = create_random_discount_item()
    return crud.discount_item.create(db, discount_item_create)


def delete_discount_item(db: Session, discount_item: DiscountItem):
    crud.discount_item.remove(db, id=discount_item.id)
