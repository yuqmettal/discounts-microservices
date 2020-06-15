from sqlalchemy.orm import Session

from database.schema.subcategory_schema import SubcategoryCreate, SubcategoryUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import Subcategory


def create_random_subcategory() -> SubcategoryCreate:
    name = random_lower_string()
    description = random_lower_string()
    category_id = 1
    return SubcategoryCreate(name=name, description=description, category_id=category_id)


def create_random_subcategory_data():
    name = random_lower_string()
    description = random_lower_string()
    category_id = 1
    return {'name': name, 'description': description, 'category_id': category_id}


def insert_subcategory(db: Session):
    subcategory_create = create_random_subcategory()
    return crud.subcategory.create(db, subcategory_create)


def delete_subcategory(db: Session, subcategory: Subcategory):
    crud.subcategory.remove(db, id=subcategory.id)
