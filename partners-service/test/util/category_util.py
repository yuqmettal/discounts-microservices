from sqlalchemy.orm import Session

from database.schema.category_schema import CategoryCreate, CategoryUpdate
from .utils import random_lower_string, random_upper_string
from database import crud
from database.models import Category


def create_random_category() -> CategoryCreate:
    name = random_lower_string()
    description = random_lower_string()
    return CategoryCreate(name=name, description=description)


def create_random_category_data():
    name = random_lower_string()
    description = random_lower_string()
    return {'name': name, 'description': description}


def insert_category(db: Session):
    category_create = create_random_category()
    return crud.category.create(db, category_create)


def delete_category(db: Session, category: Category):
    crud.category.remove(db, id=category.id)
