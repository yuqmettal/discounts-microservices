from sqlalchemy.orm import Session

from database.schema.discount_schema import DiscountCreate, DiscountUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import Discount


def _create_discount_data():
    return {
        "start_date": "2020-06-01",
        "end_date": "2020-06-30",
        "calendarized": False,
        "priority": 1,
        "discount": 10,
        "retailer_id": 1
    }


def create_random_discount() -> DiscountCreate:
    return DiscountCreate(**_create_discount_data())


def create_random_discount_data():
    return _create_discount_data()


def insert_discount(db: Session):
    discount_create = create_random_discount()
    return crud.discount.create(db, discount_create)


def delete_discount(db: Session, discount: Discount):
    crud.discount.remove(db, id=discount.id)
