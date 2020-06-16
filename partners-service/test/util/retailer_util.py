from sqlalchemy.orm import Session

from database.schema.retailer_schema import RetailerCreate, RetailerUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import Retailer


def create_random_retailer() -> RetailerCreate:
    name = random_lower_string()
    description = random_lower_string()
    city_id = 1
    category_id = 1
    category_enabled = True
    return RetailerCreate(name=name, description=description, city_id=city_id, category_id=category_id, category_enabled=category_enabled)


def create_random_retailer_data():
    name = random_lower_string()
    description = random_lower_string()
    city_id = 1
    category_id = 1
    category_enabled = True
    return {'name': name, 'description': description, 'city_id': city_id, 'category_id': category_id, 'category_enabled': category_enabled}


def insert_retailer(db: Session):
    retailer_create = create_random_retailer()
    return crud.retailer.create(db, retailer_create)


def delete_retailer(db: Session, retailer: Retailer):
    crud.retailer.remove(db, id=retailer.id)
