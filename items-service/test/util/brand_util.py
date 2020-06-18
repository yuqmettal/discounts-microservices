from sqlalchemy.orm import Session

from app.database.schema.brand_schema import BrandCreate, BrandUpdate
from .utils import random_lower_string, random_upper_string
from app.database import crud
from app.database.models import Brand


def create_random_brand() -> BrandCreate:
    name = random_lower_string()
    return BrandCreate(name=name)


def create_random_brand_data():
    name = random_lower_string()
    return {'name': name}


def insert_brand(db: Session):
    brand_create = create_random_brand()
    return crud.brand.create(db, brand_create)


def delete_brand(db: Session, brand: Brand):
    crud.brand.remove(db, id=brand.id)
