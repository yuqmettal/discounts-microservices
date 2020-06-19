from sqlalchemy.orm import Session

from app.database.schema.discount_schema import DiscountCreate, DiscountUpdate
from .utils import random_lower_string, random_upper_string
from app.database import crud
from app.database.models import Discount


def _create_discount_data():
    return  {
        "start_date": "2020-06-01",
        "end_date": "2020-06-30",
        "calendarized": False,
        "priority": 1,
        "discount": 10,
        "retailer_id": 1,
        "by_categories": False,
        "by_subcategories": False,
        "by_brands": False,
        "by_products": False,
        "by_clients": False,
        "to_prime_clients": False,
        "free_shipping": False,
        "free_shipping_amount": False,
        "according_deliver_day": False,
        "according_order_day": False,
        "order_and_deliver_same_day": False
    }


def create_random_discount() -> DiscountCreate:
    return DiscountCreate(**_create_discount_data())


def create_random_discount_data():
    return _create_discount_data()


def insert_discount(db: Session):
    discount_create = create_random_discount()
    return crud.discount.create(db, discount_create)


def delete_discount(db: Session, discount: Discount):
    items = crud.discount_item.get_by_discount(db, discount_id=discount.id)
    for item in items:
        crud.discount_item.remove(db, id=item.id)
    crud.discount.remove(db, id=discount.id)
