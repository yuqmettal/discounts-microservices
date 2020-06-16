from sqlalchemy.orm import Session

from database.schema.item_schema import ItemCreate, ItemUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import Item


def create_random_item() -> ItemCreate:
    retailer_id = 1
    category_id = 1
    product_id = 1
    pvp = 15.6
    margin = 13.6
    return ItemCreate(retailer_id=retailer_id, category_id=category_id, product_id=product_id, pvp=pvp, margin=margin)


def create_random_item_data():
    retailer_id = 1
    category_id = 1
    product_id = 1
    pvp = 15.6
    margin = 13.6
    return {'retailer_id': retailer_id, 'category_id': category_id, 'product_id': product_id, 'pvp': pvp, 'margin': margin}


def insert_item(db: Session):
    item_create = create_random_item()
    return crud.item.create(db, item_create)


def delete_item(db: Session, item: Item):
    crud.item.remove(db, id=item.id)
